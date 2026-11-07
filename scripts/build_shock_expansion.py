"""Reproduce traced PPM, specified AUSM variants and conforming forebody tests."""
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.benchmarks import get_problem,Problem
from numart.equations import Euler
from numart.reconstruction import contact_problem,averaged_state
from numart.ppm_traced import solve,IntegrationFailure
from numart.reference_solutions import get_reference,riemann_reference
from numart.ausm_plus import flux as ausm_flux
from numart.blunt_body import solve as solve_blunt,stagnation_pressure
from numart.euler2d import primitive
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=ROOT/'docs/figures/shock-expansion';OUT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/'outputs/shock-expansion-cache';CACHE.mkdir(parents=True,exist_ok=True)
SOURCES=['numart/ppm_traced.py','numart/ausm_plus.py','numart/rotated_flux.py','numart/blunt_body.py',
 'numart/reconstruction.py','numart/shock_robustness.py','numart/euler2d.py','numart/ausm.py',
 'numart/limiters.py','numart/riemann.py','numart/equations.py','numart/benchmarks.py',
 'numart/reference_solutions.py','numart/reference_riemann.py',
 'website/public/assets/reconstruction/reconstruction.json','scripts/build_shock_expansion.py']
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={p:digest(ROOT/p) for p in SOURCES}
numerical_hashes={p:v for p,v in hashes.items() if p.startswith('numart/')}
arrays={};legacy=json.loads((ROOT/'website/public/assets/reconstruction/reconstruction.json').read_text())
configs=[dict(id='plain',label='Tracing only',steepening=False,flattening=False,color='#687fad'),
 dict(id='steep',label='Tracing + contact steepening',steepening=True,flattening=False,color='#9872a2'),
 dict(id='flat',label='Tracing + shock flattening',steepening=False,flattening=True,color='#65796c'),
 dict(id='both',label='Tracing + both switches',steepening=True,flattening=True,color='#bf5b35')]
eq=Euler();strong=riemann_reference('euler',(1.,0.,1000.),(1.,0.,.01),final_time=.01)
def strong_initial(x):return strong.point(x,0)
strong_problem=Problem('strong-shock',eq,(0.,1.),.01,'outflow',strong_initial,lambda x,t:strong.point(x,t))
problems=[];ppm=[];flux_cases=[]
for name,n in [('sod',200),('moving-contact',200),('shu-osher',240),('strong-shock',200)]:
    p=contact_problem() if name=='moving-contact' else strong_problem if name=='strong-shock' else get_problem(name)
    dense=np.linspace(*p.domain,1601)
    if name=='shu-osher':
        old=next(c for c in legacy['problems'] if c['id']==name)
        rx,rw=old['reference_x'],old['reference'];reference_note='Internal numerical reference / characteristic FD WENO-Z N=960; not exact.'
    else:
        rx=dense.tolist();rw=p.equation.primitive(p.reference(dense,p.final_time)).tolist()
        reference_note='Semi-analytic Riemann point curve; density errors use front-split conserved means.' if name!='moving-contact' else 'Exact periodic contact point curve; cell means agree with the initial grid after one crossing.'
    problems.append(dict(id=name,n=n,time=p.final_time,domain=list(p.domain),reference_x=rx,reference=rw,reference_note=reference_note))
    edges=np.linspace(*p.domain,n+1);ref=None;quad=None
    if name in ('sod','strong-shock'):
        report=(get_reference('euler-sod') if name=='sod' else strong).cell_average_report(edges,p.final_time)
        ref=report['values'];quad=report['max_order_difference'].tolist()
    elif name=='moving-contact':ref=p.initial(p.grid(n))
    def record(r,config,status='completed',reason=None):
        w=p.equation.primitive(r.q);key=name+'-'+config;arrays[key]=r.q
        mean_initial=averaged_state(p,r.x,(p.domain[1]-p.domain[0])/n)
        change=(r.q-mean_initial).sum(axis=0)*(p.domain[1]-p.domain[0])/n
        return dict(problem=name,config=config,status=status,failure_reason=reason,requested_time=p.final_time,n=n,x=r.x.tolist(),primitive=w.tolist(),time=r.time,
            cfl=.4,steps=r.steps,rejected_steps=r.rejected_steps,scaled_reconstructions=r.scaled_reconstructions,
            steepened_cells=r.steepened_cells,flattened_cells=r.flattened_cells,
            minimum_density=float(w[:,0].min()),minimum_pressure=float(w[:,2].min()),
            error_l1=None if ref is None or status!='completed' else float(np.mean(abs(r.q[:,0]-ref[:,0]))),
            quadrature_difference=quad,conserved_integral_change=change.tolist(),
            pressure_departure=float(abs(w[:,2]-1).max()) if name=='moving-contact' else None,
            velocity_departure=float(abs(w[:,1]-1).max()) if name=='moving-contact' else None)
    for config in configs:
        r=solve(p,n,steepening=config['steepening'],flattening=config['flattening'])
        ppm.append(record(r,config['id']));print('ppm',name,config['id'],r.steps,r.rejected_steps,flush=True)
    for solver in ('hllc','ausm','ausm-plus','ausm-up'):
        status,reason='completed',None
        try:r=solve(p,n,steepening=False,flattening=True,riemann=solver)
        except IntegrationFailure as failure:
            r=failure.result;status,reason='failed',str(failure)
        flux_cases.append(dict(record(r,'flux-'+solver,status,reason),solver=solver,mach_cutoff=.1 if solver=='ausm-up' else None))
        print('flux',name,solver,r.steps,r.rejected_steps,flush=True)

refinement=[];p=get_problem('entropy-wave')
for config in (configs[0],configs[-1]):
    errors=[];ns=[32,64,128]
    for n in ns:
        r=solve(p,n,final_time=.2,steepening=config['steepening'],flattening=config['flattening'])
        target=averaged_state(p,r.x,1/n,.2)
        errors.append(float(np.mean(abs(r.q[:,0]-target[:,0]))))
    refinement.append(dict(config=config['id'],n=ns,error_l1=errors,orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist(),cfl=.4,time=.2))

# A flux response, not a low-Mach PDE validation or a universal performance claim.
response=[]
for cutoff in (.01,.1,1.):
    entries=[]
    for mach in np.geomspace(1e-4,1,49):
        speed=mach*np.sqrt(1.4)
        left,right=eq.conserved(np.array([[1.,speed,1.+1e-6],[1.,speed,1.-1e-6]]))
        base=eq.conserved(np.array([1.,speed,1.]))
        entries.append([float(mach),float((ausm_flux(left,right,variant='up',mach_cutoff=cutoff)[0]-speed)/2e-6),
                        float((ausm_flux(left,right,variant='plus')[0]-speed)/2e-6)])
    response.append(dict(cutoff=cutoff,columns=['background Mach','mass-flux perturbation / pressure jump, up','mass-flux perturbation / pressure jump, plus'],values=entries))

methods=[dict(id='roe',label='Roe / acoustic smoothing 0.1c',color='#bb482d'),
 dict(id='hlle',label='HLLE / Einfeldt-type bounds',color='#437858'),
 dict(id='ausm-plus',label='AUSM+',color='#687fad'),dict(id='ausm-up',label='AUSM+-up / reference Mach 0.1',color='#317f91'),
 dict(id='rotated',label='Directional HLLE/Roe',color='#996da4')]
runs=[];body_fields={};meshes={}
for n in (24,48):
    for amplitude in (0.,1e-4):
        for method in methods:
            config=dict(nr=n,solver=method['id'],mach=6.,amplitude=amplitude,final_time=2.,cfl=.4)
            key=f'forebody-{n}-{method["id"]}-{amplitude:g}';file=CACHE/(key+'.npz');meta=file.with_suffix('.json')
            provenance=dict(config=config,source_sha256=numerical_hashes)
            start=time.monotonic()
            if file.exists() and meta.exists() and json.loads(meta.read_text())==provenance:
                with np.load(file) as f:out={k:f[k] for k in f.files}
            else:
                r=solve_blunt(**config)
                out=dict(q=r.q,time=r.time,steps=r.steps,rejected_steps=r.rejected_steps,history=r.history,wall_pressure=r.wall_pressure,
                         conservation_residual=r.conservation_residual,vertices=r.mesh['vertices'],volume=r.mesh['volume'],theta=r.mesh['theta'],radius=r.mesh['r'])
                np.savez_compressed(file,**out);meta.write_text(json.dumps(provenance,sort_keys=True)+'\n')
            w=primitive(out['q']);middle=n
            nose=float(np.mean(out['wall_pressure'][middle-1:middle+1]));p0=stagnation_pressure()
            wall_theta=.5*(out['theta'][:-1]+out['theta'][1:])
            metrics=dict(nose_pressure=nose,normal_shock_stagnation_reference=p0,nose_relative_error=nose/p0-1,
                final_symmetry_defect=float(out['history'][-1,2]),maximum_symmetry_defect=float(out['history'][:,2].max()),
                minimum_density=float(out['history'][:,3].min()),minimum_pressure=float(out['history'][:,4].min()),
                final_update_rate=float(out['history'][-1,1]),conservation_residual=out['conservation_residual'].tolist(),
                steps=int(out['steps']),rejected_steps=int(out['rejected_steps']))
            runs.append(dict(id=key,method=method['id'],**config,shape=[n,2*n],metrics=metrics,history=out['history'].tolist(),
                history_columns=['time','volume-weighted normalized conserved update rate','density reflection defect / rho_inf','minimum density','minimum pressure'],
                wall_theta=wall_theta.tolist(),wall_pressure=out['wall_pressure'].tolist(),
                wall_cp=((out['wall_pressure']-1)/(.5*1.4*36)).tolist()))
            arrays[key]=out['q'];arrays[f'mesh-{n}-vertices']=out['vertices'];arrays[f'mesh-{n}-volume']=out['volume']
            body_fields[key]=w;meshes[n]=out['vertices']
            print(key,'nose',round(nose,5),'symmetry',metrics['final_symmetry_defect'],'retries',metrics['rejected_steps'],'seconds',round(time.monotonic()-start,2),flush=True)

panels=[]
for n in (24,48):
    for amplitude in (0.,1e-4):
        selected=[r for r in runs if r['nr']==n and r['amplitude']==amplitude]
        for field,index in [('density',0),('pressure',3),('Mach',None)]:
            values=[]
            for run in selected:
                w=body_fields[run['id']]
                values.append(w[...,index] if index is not None else np.linalg.norm(w[...,1:3],axis=-1)/np.sqrt(1.4*w[...,3]/w[...,0]))
            lo=min(float(v.min()) for v in values);hi=max(float(v.max()) for v in values)
            fig,axes=plt.subplots(2,3,figsize=(13,9),layout='constrained')
            for ax,method,v in zip(axes.flat,methods,values):
                vertex=meshes[n];artist=ax.pcolormesh(vertex[...,0],vertex[...,1],v,vmin=lo,vmax=hi,cmap='viridis',shading='flat',rasterized=True)
                theta=np.linspace(np.pi/2,3*np.pi/2,100);ax.fill(np.r_[0,np.cos(theta),0],np.r_[1,np.sin(theta),-1],color='#d2cfc4')
                ax.set(title=method['label'],xlabel='x / R',ylabel='y / R',aspect='equal',xlim=(-4.1,.1),ylim=(-4.1,4.1))
            fig.colorbar(artist,ax=list(axes.flat[:5]),label=field,shrink=.8)
            for method,run in zip(methods,selected):axes.flat[5].plot((np.array(run['wall_theta'])-np.pi)*180/np.pi,run['wall_cp'],label=method['label'],color=method['color'])
            axes.flat[5].set(title='Slip-wall pressure coefficient',xlabel='Angle from nose [degrees]',ylabel='Cp');axes.flat[5].grid(alpha=.2);axes.flat[5].legend(fontsize=6)
            fig.suptitle(f'Cylinder forebody | Mach 6 | {n} x {2*n} | t=2 | density seed {amplitude:g}\nFirst-order geometric FV / SSPRK2; terminal snapshots, not certified steady solutions')
            name=f'forebody-{n}-{amplitude:g}-{field.lower()}.png';fig.savefig(OUT/name,dpi=135);plt.close(fig)
            panels.append(dict(n=n,amplitude=amplitude,field=field,image=name,limits=[lo,hi]))

fig,axes=plt.subplots(2,2,figsize=(12,7.5),layout='constrained')
for ax,name in zip(axes.flat,('sod','moving-contact','shu-osher','strong-shock')):
    p=next(p for p in problems if p['id']==name)
    ax.plot(p['reference_x'],np.array(p['reference'])[:,0],'k--',lw=1,label='Internal numerical reference' if name=='shu-osher' else 'Point reference')
    for config in configs:
        entry=next(c for c in ppm if c['problem']==name and c['config']==config['id'])
        ax.plot(entry['x'],np.array(entry['primitive'])[:,0],color=config['color'],label=config['label'])
    ax.set(title=name,xlabel='x',ylabel='density');ax.grid(alpha=.2);ax.legend(fontsize=6)
    if name=='shu-osher':ax.set_xlim(-1,3)
fig.suptitle('Direct-Eulerian traced PPM | independent contact and shock switches')
fig.savefig(OUT/'ppm-switches.png',dpi=140);plt.close(fig)

np.savez_compressed(OUT/'fields.npz',**arrays)
data=dict(schema_version=1,ppm_configs=configs,problems=problems,ppm_cases=ppm,flux_cases=flux_cases,refinement=refinement,
    low_mach_response=response,body_methods=methods,body_runs=runs,body_panels=panels,
    controls=dict(ppm_cfl=.4,ppm_time_update='Single characteristic-traced conservative step; no SSPRK wrapper.',
        ausm=dict(interface_sound='Directional critical-enthalpy sound speed',kp=.25,ku=.75,sigma=1.,mach_cutoff=.1),
        forebody=dict(radius=1.,outer_radius=4.,theta=[np.pi/2,3*np.pi/2],mach=6.,cfl=.4,final_time=2.,
            representation='Cartesian conserved means on conforming polygonal annular cells',time_integrator='SSPRK2',
            perturbation='Initial density: rho_inf*(1+epsilon*exp(-((r-1.5)/.3)^2)*sin(12*(theta-pi))); u,v,p unchanged.',
            boundaries='Slip inner wall; fixed outer free stream; extrapolated angular exits. Forebody only; wake excluded.')),
    scope='Traced primitive PPM with specified steepening/flattening, not Lagrange/remap or multidimensional CTU. Directional HLLE/Roe is an explicit two-flux experiment, not the optimized 2008 formula. Low-Mach graph is a flux sensitivity, not low-Mach PDE validation. Bow-shock fields are terminal snapshots at t=2; update rates, controls and grid sensitivity prevent a carbuncle-free or steady-convergence certification.',
    source_sha256=hashes)
assert hashes=={p:digest(ROOT/p) for p in SOURCES},'Numerical source changed during build'
data['artifact_sha256']={p.name:digest(p) for p in OUT.iterdir() if p.suffix in ('.png','.npz')}
(OUT/'shock-expansion.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
print('Saved',len(ppm),'PPM cases,',len(flux_cases),'flux cases and',len(runs),'forebody runs.',flush=True)
