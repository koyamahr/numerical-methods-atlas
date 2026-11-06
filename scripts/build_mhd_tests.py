"""HLLD standard tests with explicit references, conservation and CT/GLM scope."""
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.hlld import primitive
from numart.mhd_tests import solve_1d,alfven_average,solve_loop,initial_loop
OUT=ROOT/'website/public/assets/mhd-tests';CACHE=ROOT/'outputs/mhd-tests'
SOURCES=['numart/hlld.py','numart/mhd_tests.py','numart/muscl2d.py','numart/euler2d.py','numart/shock_cases.py','numart/snapshots.py']
digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def loop(n,method,solver):
    key=f'{method}-{solver}-{n}';path=CACHE/(key+'.npz');record=CACHE/(key+'.json')
    hashes={p:digest(ROOT/p) for p in SOURCES}
    config=dict(n=n,method=method,solver=solver,limiter='mc',cfl=.3,final_time=1.,damping=.18)
    metadata=dict(source_sha256=hashes,config=config)
    if path.exists() and record.exists() and json.loads(record.read_text())==metadata:
        with np.load(path) as f:return {k:f[k] for k in f.files}
    start=time.monotonic();r=solve_loop(n,method=method,solver=solver)
    initial,bx,by,dx,dy=initial_loop(n,method)
    data=dict(q=r.q,initial=initial,time=r.time,steps=r.steps,history=r.history,
        fallback=r.stats['hlle_fallback_faces'],retries=r.stats['retried_steps'])
    if r.bx is not None:data.update(bx=r.bx,by=r.by)
    assert hashes=={p:digest(ROOT/p) for p in SOURCES},'Source changed while computing'
    np.savez_compressed(path,**data);record.write_text(json.dumps(metadata,indent=2)+'\n')
    print(key,'steps',r.steps,'seconds',round(time.monotonic()-start,1),'stats',r.stats,flush=True)
    return data


def build():
    OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
    brio=[];arrays={}
    fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    for solver,n in (('hlle',400),('hlld',400),('hlld',800)):
        r=solve_1d('brio-wu',n,solver=solver);w=primitive(r.q,2.);x=(np.arange(n)+.5)/n
        arrays[f'brio_{solver}_{n}']=r.q
        for ax,index,label in zip(axes.flat,(0,4,1,6),('Density','Gas pressure','Normal velocity','Transverse By')):
            ax.plot(x,w[:,index],label=f'{solver.upper()} / N={n}',lw=1.2,ls='--' if n==800 else '-');ax.set(xlabel='x',ylabel=label);ax.grid(alpha=.15)
        brio.append(dict(solver=solver,n=n,time=r.time,steps=r.steps,min_density=float(w[:,0].min()),min_pressure=float(w[:,4].min()),**r.stats))
    axes[0,0].legend(fontsize=8);fig.suptitle('Brio-Wu | gamma = 2 | MC + SSPRK2 | t = 0.1\nComputed profiles and grid comparison; no exact-reference overlay',fontsize=11)
    fig.savefig(OUT/'brio-wu.png',dpi=140);plt.close(fig)
    alfven=[]
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    for solver in ('hlle','hlld'):
        errors=[]
        for n in (32,64,128,256):
            r=solve_1d('alfven',n,solver=solver);reference=alfven_average(n,1)
            errors.append(float(np.mean(abs(r.q[:,6:8]-reference[:,6:8]))))
            arrays[f'alfven_{solver}_{n}']=r.q
        orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()
        alfven.append(dict(solver=solver,n=[32,64,128,256],l1_transverse_b=errors,orders=orders))
        axes[0].loglog([32,64,128,256],errors,'o-',label=solver.upper())
        axes[1].plot((np.arange(256)+.5)/256,r.q[:,6],label=solver.upper(),lw=1.2)
        assert orders[-1]>1.7
    axes[1].plot((np.arange(256)+.5)/256,alfven_average(256,1)[:,6],'k--',label='Exact cell average',lw=1)
    axes[0].set(xlabel='Cells N',ylabel='Mean absolute transverse-field error',title='Refinement');axes[1].set(xlabel='x',ylabel='By',title='One period / N=256')
    for ax in axes:ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.suptitle('Circularly polarized Alfven wave | rho=1, p=0.1, Bx=1, amplitude=0.1\nFull transverse vectors / MC + SSPRK2 / periodic / t = 1',fontsize=11)
    fig.savefig(OUT/'alfven.png',dpi=140);plt.close(fig)
    modes=[];results={}
    for method in ('ct','glm'):
        for solver in ('hlle','hlld'):
            series=[]
            for n in (32,64):
                d=loop(n,method,solver);h=d['history']
                stats=dict(n=n,shape=[2*n,n],time=1.,steps=int(d['steps']),
                    native_max_divergence=float(h[-1,1]),initial_native_max_divergence=float(h[0,1]),
                    magnetic_energy_fraction=float(h[-1,2]/h[0,2]),
                    mean_mass_change=float(h[-1,3]-h[0,3]),mean_total_energy_change=float(h[-1,4]-h[0,4]),
                    field_return_mean_absolute_error=float(np.mean(abs(d['q'][...,5:8]-d['initial'][...,5:8]))),
                    hlle_fallback_faces=int(d['fallback']),retried_steps=int(d['retries']))
                series.append(stats)
                assert abs(stats['mean_mass_change'])<1e-10 and abs(stats['mean_total_energy_change'])<1e-10
                if method=='ct':assert stats['native_max_divergence']<1e-11
            modes.append(dict(id=f'{solver}-{method}',method=method,solver=solver,refinement=series,history=h.tolist(),metrics=series[-1]))
            results[f'{solver}-{method}']=d;arrays[f'loop_{solver}_{method}']=d['q']
    bound=max(float(np.max(np.sum(d[key][...,5:8]**2,axis=-1))) for d in results.values() for key in ('initial','q'))
    fig,axes=plt.subplots(2,2,figsize=(11,6.4),layout='constrained')
    for ax,mode in zip(axes.flat,modes):
        d=results[mode['id']];b2=np.sum(d['q'][...,5:8]**2,axis=-1)
        im=ax.imshow(b2.T,extent=(-1,1,-.5,.5),origin='lower',interpolation='nearest',cmap='magma',vmin=0,vmax=bound)
        ax.add_patch(plt.Circle((0,0),.3,fill=False,color='cyan',ls='--',lw=.7))
        ax.set(title=f'{mode["solver"].upper()} / {mode["method"].upper()} | energy fraction {mode["metrics"]["magnetic_energy_fraction"]:.3f}',xlabel='x',ylabel='y')
    fig.colorbar(im,ax=axes,label='B squared (common scale)',shrink=.8)
    fig.suptitle('Weak magnetic field loop | 128 x 64 | v=(2,1,0) | one box transit / t = 1\nCT-Contact face curl vs cell-centered GLM; initialization and native divergence operators differ',fontsize=10)
    fig.savefig(OUT/'field-loop.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    for mode in modes:
        h=np.array(mode['history']);label=mode['id'].upper()
        axes[0].plot(h[:,0],h[:,2]/h[0,2],label=label)
        axes[1].semilogy(h[:,0],np.maximum(h[:,1],1e-20),label=label)
    axes[0].set(title='Magnetic energy / own initial value',xlabel='Physical time',ylabel='Fraction')
    axes[1].set(title='Native maximum magnetic divergence',xlabel='Physical time',ylabel='max |div B| (operators differ)')
    for ax in axes:ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.suptitle('Field-loop diagnostics | energy retention alone is not an accuracy or stability ranking',fontsize=11)
    fig.savefig(OUT/'loop-diagnostics.png',dpi=140);plt.close(fig)
    np.savez_compressed(OUT/'fields.npz',**arrays)
    manifest=dict(brio_wu=dict(image='brio-wu.png',runs=brio,scope='Coplanar gamma=2 Brio-Wu. No exact solution overlay or universal uniqueness claim.'),
        alfven=dict(image='alfven.png',series=alfven,scope='1D circularly polarized nonlinear wave; exact conservative cell averages, including constant total energy.'),
        field_loop=dict(image='field-loop.png',diagnostics_image='loop-diagnostics.png',modes=modes,scope='Weak-field MHD translation diagnostic, not an exact finite-field solution. CT initializes face B with a corner-potential curl; GLM uses a cell-potential central curl. No equal-accuracy or matched-cost ranking. CT uses contact-upwinded edge EMF, not UCT-HLLD. GLM has ch=4, damping=0.18*ch/h and no psi contribution to total energy.'),
        riemann_scope='HLLD fast/contact/Alfven fan, common Bn, zero-Bn and parallel-field degeneracies; invalid stars fall back to HLLE and counts are reported.',
        source_sha256={p:digest(ROOT/p) for p in SOURCES+['scripts/build_mhd_tests.py']},
        artifact_sha256={p.name:digest(p) for p in OUT.iterdir() if p.is_file() and p.name!='mhd-tests.json'})
    (OUT/'mhd-tests.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('MHD tests ready',flush=True)

if __name__=='__main__':build()
