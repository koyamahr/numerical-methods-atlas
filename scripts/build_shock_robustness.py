"""Source-checked planar-shock diagnostics and independently checked Roe algebra."""
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.shock_robustness import solve_shock
from numart.euler2d import primitive
from numart.roe_properties import roe_matrix,flux_jacobian,eigensystem,normal_shock
from numart.equations import Euler
from numart.riemann import roe_flux,exact_euler
OUT=ROOT/'website/public/assets/shock-methods';OUT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/'outputs/shock-priority/planar';CACHE.mkdir(parents=True,exist_ok=True)
SOURCES=['numart/shock_robustness.py','numart/ausm.py','numart/euler2d.py','numart/roe_properties.py','numart/reconstruction.py','numart/riemann.py','numart/equations.py','numart/limiters.py','numart/benchmarks.py','scripts/build_shock_robustness.py']
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={p:digest(ROOT/p) for p in SOURCES}
methods=[dict(id='roe-raw',solver='roe',entropy_fraction=0.,label='Roe / no entropy smoothing',color='#bb482d'),dict(id='roe-fixed',solver='roe',entropy_fraction=.1,label='Roe / acoustic smoothing 0.1c',color='#a26c44'),dict(id='hll',solver='hll',entropy_fraction=.1,label='HLL / Davis bounds',color='#6a83ac'),dict(id='hlle',solver='hlle',entropy_fraction=.1,label='HLLE / Einfeldt-type bounds',color='#437858'),dict(id='hybrid',solver='hybrid',entropy_fraction=.1,label='Pressure-sensor Roe/HLLE blend',color='#996da4'),dict(id='ausm',solver='ausm',entropy_fraction=.1,label='AUSM / common sound speed',color='#317f91')]
runs=[];arrays={};panels=[]
for n in (64,128):
 for phase in (0.,.5):
  selected=[]
  for method in methods:
   for amplitude in (0.,1e-4):
    config=dict(n=n,solver=method['solver'],entropy_fraction=method['entropy_fraction'],phase=phase,amplitude=amplitude,mach=6.,final_time=.2,cfl=.3)
    key=f'{n}-{phase:g}-{method["id"]}-{amplitude:g}';file=CACHE/(key+'.npz');meta=file.with_suffix('.json');record=dict(config=config,source_sha256={k:v for k,v in hashes.items() if k.startswith('numart/')})
    start=time.monotonic()
    if file.exists() and meta.exists() and json.loads(meta.read_text())==record:
     with np.load(file) as f:d={k:f[k] for k in f.files}
    else:
     r=solve_shock(**config)
     d=dict(q=r.q,history=r.history,x=r.x,y=r.y,time=r.time,steps=r.steps,retried_steps=r.retried_steps,location=r.location)
     np.savez_compressed(file,**d);meta.write_text(json.dumps(record,indent=2)+'\n')
    w=primitive(d['q']);h=d['history'];metrics=dict(initial_alternating_density=float(h[0,1]),final_alternating_density=float(h[-1,1]),maximum_alternating_density=float(h[:,1].max()),final_max_transverse_velocity=float(h[-1,2]),final_mass_deficit_position_spread=float(h[-1,3]),min_density=float(h[:,4].min()),min_pressure=float(h[:,5].min()),retried_steps=int(d['retried_steps']),steps=int(d['steps']))
    runs.append(dict(id=key,method=method['id'],shape=[n,n//4],**config,metrics=metrics,history=h.tolist()))
    arrays[key]=d['q']
    if amplitude:selected.append((method,d))
    print(key,metrics['final_alternating_density'],metrics['retried_steps'],round(time.monotonic()-start,2),flush=True)
  fig,axs=plt.subplots(2,3,figsize=(14,8),layout='constrained')
  visible=['roe-fixed','hll','hlle','hybrid','ausm'];vmax=max(abs(primitive(d['q'])[...,0]-primitive(d['q'])[...,0].mean(axis=1,keepdims=True)).max() for m,d in selected)
  for ax,method_id in zip(axs.flat,visible):
   method,d=next(pair for pair in selected if pair[0]['id']==method_id);rho=d['q'][...,0];deviation=rho-rho.mean(axis=1,keepdims=True)
   im=ax.imshow(deviation.T,extent=(0,1,0,.25),origin='lower',cmap='RdBu_r',vmin=-vmax,vmax=vmax,interpolation='nearest',aspect='equal');ax.set(xlim=(.35,.65),xlabel='x',ylabel='y',title=method['label']);fig.colorbar(im,ax=ax,label='rho - row mean / common scale',shrink=.8)
  ax=axs.flat[5]
  for method,d in selected:
   h=d['history'];ax.semilogy(h[:,0],np.maximum(h[:,1],1e-16),color=method['color'],label=method['label'])
  ax.set(xlabel='physical time',ylabel='max shock-band alternating density',title='Nyquist mode | display floor 1e-16');ax.legend(fontsize=7);ax.grid(alpha=.2)
  fig.suptitle(f'Independent stationary Mach-6 planar shock | {n} x {n//4} | t=0.2 | phase={phase:g} cell\nFirst order / SSPRK2 / CFL 0.3 | initial row displacement +/- 1e-4 dx | not the Quirk perturbed-grid test',fontsize=11)
  image=f'planar-{n}-{phase:g}.png';fig.savefig(OUT/image,dpi=130);plt.close(fig);panels.append(dict(n=n,phase=phase,image=image))
# Roe algebra: parameter-vector matrix and eigensystem are separate constructions.
eq=Euler();rng=np.random.default_rng(91);w=rng.uniform(.1,3,(2000,3));w[:,1]-=1.5
left=eq.conserved(w);right=eq.conserved(w[::-1]);a=roe_matrix(left,right);jump=right-left;df=eq.flux(right)-eq.flux(left)
res=np.max(abs(np.einsum('nij,nj->ni',a,jump)-df),axis=1)/np.maximum(1,np.max(abs(df),axis=1))
cons=np.max(abs(roe_matrix(left,left)-flux_jacobian(left)),axis=(1,2))/np.maximum(1,np.max(abs(flux_jacobian(left)),axis=(1,2)))
lam,r,l=eigensystem(left,right);inverse=np.max(abs(l@r-np.eye(3)),axis=(1,2))
waves=[]
for name,speed,reverse in [('stationary compression shock',0,False),('moving compression shock',.7,False),('stationary expansion discontinuity',0,True)]:
 ql,qr=normal_shock(2,speed,reverse);mat=roe_matrix(ql,qr);raw=roe_flux(ql,qr,eq,0);fixed=roe_flux(ql,qr,eq,.1)
 reference=eq.flux(eq.conserved(exact_euler(np.array([0.]),eq.primitive(ql),eq.primitive(qr)))[0])
 modal=eigensystem(ql,qr)[2]@(qr-ql)
 waves.append(dict(name=name,speed=speed,jump_residual=float(np.linalg.norm(mat@(qr-ql)-speed*(qr-ql))),modal_strengths=modal.tolist(),raw_flux_exact_reference_error=float(np.linalg.norm(raw-reference)),fixed_flux_exact_reference_error=float(np.linalg.norm(fixed-reference))))
ql,qr=eq.conserved(np.array([[1.,.7,1.],[2.,.7,1.]]));mat=roe_matrix(ql,qr)
waves.append(dict(name='moving contact',speed=.7,jump_residual=float(np.linalg.norm(mat@(qr-ql)-.7*(qr-ql))),modal_strengths=(eigensystem(ql,qr)[2]@(qr-ql)).tolist(),raw_flux_exact_reference_error=float(np.linalg.norm(roe_flux(ql,qr,eq,0)-eq.flux(ql))),fixed_flux_exact_reference_error=float(np.linalg.norm(roe_flux(ql,qr,eq,.1)-eq.flux(ql)))))
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
ax.hist(np.log10(np.maximum(res,1e-18)),bins=25,color='#65796c');ax.set(xlabel='log10 relative flux-jump residual (display floor 1e-18)',ylabel='state pairs',title='Roe parameter-vector matrix | 2000 deterministic physical state pairs');fig.savefig(OUT/'roe-property-u.png',dpi=130);plt.close(fig)
np.savez_compressed(OUT/'planar-fields.npz',**arrays)
assert hashes=={p:digest(ROOT/p) for p in SOURCES},'Source changed during build'
manifest=dict(methods=methods,runs=runs,panels=panels,history_columns=['time','max_shock_band_alternating_density','max_shock_band_abs_v','mass_deficit_position_range','minimum_density','minimum_pressure'],
 scope='Independent stationary Mach-6 normal shock in [0,1] x [0,0.25], gamma=1.4, rho1=1.4, p1=1, u1=6; exact normal-shock downstream states. Fixed x boundary states, periodic y, uniform Cartesian cells. First-order / SSPRK2 / CFL 0.3 / t=0.2. Shock phase 0 or 0.5 cell. Exact conservative x averaging of row-dependent front displacement +/- 1e-4 dx. Unperturbed controls are separate runs. This Nyquist perturbation preserves a symmetry with transverse velocity zero; it probes row decoupling, not general transverse modes or a blunt-body bulge. Mesh rotations, other wavelengths and blunt-body tests remain pending. No carbuncle-free certification.',
 sensor='Cell pressure sensor S=max over immediate x/y neighbors |p_neighbor-p|/min(p_neighbor,p). theta=clip((S-0.05)/0.2,0,1). Face theta=max of adjacent cells. F=(1-theta)*F_Roe_fixed+theta*F_HLLE. Explicit educational blend, not rotated-hybrid or a universal cure.',
 roe_property_u=dict(image='roe-property-u.png',state_pairs=2000,max_relative_jump_residual=float(res.max()),max_relative_consistency_residual=float(cons.max()),max_inverse_residual=float(inverse.max()),minimum_acoustic_speed=float(np.min((lam[:,2]-lam[:,0])/2)),waves=waves),source_sha256=hashes,
 artifact_sha256={p.name:digest(p) for p in OUT.iterdir() if p.is_file() and p.suffix in ('.png','.npz')})
(OUT/'robustness.json').write_text(json.dumps(manifest,separators=(',',':'),allow_nan=False)+'\n')
print('Shock robustness and Roe properties ready',flush=True)
