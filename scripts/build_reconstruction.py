"""Controlled Euler reconstruction comparisons; legacy exhibits are unchanged."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart import get_problem
from numart.reconstruction import solve_euler,contact_problem,averaged_state
SOURCES=['numart/reconstruction.py','numart/ausm.py','numart/limiters.py','numart/riemann.py','numart/equations.py','numart/benchmarks.py','scripts/build_reconstruction.py']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
arrays={}
methods=[dict(id='muscl',label='MUSCL / MC',color='#65796c'),
         dict(id='ppm',label='Limited PPM reconstruction',color='#bf5b35'),
         dict(id='weno-js',label='FD WENO5-JS',color='#687fad'),
         dict(id='weno-z',label='FD WENO5-Z / exponent 2',color='#9872a2')]
cases=[];problems=[]
for name,n in [('sod',200),('moving-contact',200),('shu-osher',240)]:
    p=contact_problem() if name=='moving-contact' else get_problem(name)
    reference=None;reference_meta='Analytic pointwise solution'
    if name=='shu-osher':
        high=solve_euler(p,960,'weno-z','characteristic')
        reference=(high.x, p.equation.primitive(high.q));reference_meta='Internal numerical reference: characteristic FD WENO-Z, N=960; not exact'
    else:
        dense=np.linspace(*p.domain,2001);reference=(dense,p.equation.primitive(p.reference(dense,p.final_time)))
    problems.append(dict(id=name,n=n,time=p.final_time,domain=list(p.domain),
                         reference_x=reference[0].tolist(),reference=reference[1].tolist(),reference_note=reference_meta))
    for method in methods:
        for basis in ('component','characteristic'):
            r=solve_euler(p,n,method['id'],basis)
            arrays[name+'-'+method['id']+'-'+basis]=r.q
            w=p.equation.primitive(r.q);ref=None;quadrature_difference=None
            if p.reference:
                if r.representation=='point values':ref=p.reference(r.x,r.time);norm='Pointwise density L1'
                else:
                    dx=(p.domain[1]-p.domain[0])/n
                    ref=averaged_state(p,r.x,dx,r.time,128)
                    less=averaged_state(p,r.x,dx,r.time,64)
                    quadrature_difference=float(np.mean(abs(ref[:,0]-less[:,0])))
                    norm='Density cell-mean L1 against 128-node quadrature of the analytic solution'
            case=dict(problem=name,method=method['id'],basis=basis,n=n,time=r.time,x=r.x.tolist(),primitive=w.tolist(),
                      cfl=.3,epsilon=1e-6,steps=r.steps,rejected_steps=r.rejected_steps,
                      scaled_reconstructions=r.scaled_reconstructions,representation=r.representation,
                      minimum_density=float(w[:,0].min()),minimum_pressure=float(w[:,2].min()),
                      error_l1=float(np.mean(abs(r.q[:,0]-ref[:,0]))) if ref is not None else None,
                      error_norm=norm if ref is not None else 'No exact final-time reference',
                      reference_quadrature_difference=quadrature_difference,
                      max_pressure_departure=float(abs(w[:,2]-1).max()) if name=='moving-contact' else None,
                      max_velocity_departure=float(abs(w[:,1]-1).max()) if name=='moving-contact' else None)
            cases.append(case)
            print(name,method['id'],basis,r.steps,r.rejected_steps,flush=True)
flux_cases=[]
for name,n in [('sod',200),('moving-contact',200),('shu-osher',240)]:
    p=contact_problem() if name=='moving-contact' else get_problem(name)
    for solver in ('hllc','roe','hlle','ausm'):
        r=solve_euler(p,n,'muscl','characteristic',riemann=solver)
        w=p.equation.primitive(r.q)
        arrays[name+'-flux-'+solver]=r.q
        flux_cases.append(dict(problem=name,solver=solver,n=n,time=r.time,x=r.x.tolist(),primitive=w.tolist(),steps=r.steps,rejected_steps=r.rejected_steps,minimum_density=float(w[:,0].min()),minimum_pressure=float(w[:,2].min())))
        print('flux',name,solver,r.steps,r.rejected_steps,flush=True)
studies=[];p=get_problem('entropy-wave')
for method in methods:
    for basis in ('component','characteristic'):
        ns=[32,64,128];errors=[]
        for n in ns:
            # SSPRK3 temporal error is O(dx^5) with dt proportional to dx^(5/3).
            cfl=.25*(32/n)**(2/3)
            r=solve_euler(p,n,method['id'],basis,cfl=cfl,final_time=.2)
            ref=averaged_state(p,r.x,1/n,.2,16) if r.representation=='cell averages' else p.reference(r.x,.2)
            errors.append(float(np.mean(abs(r.q[:,0]-ref[:,0]))))
        studies.append(dict(method=method['id'],basis=basis,n=ns,error_l1=errors,
                            orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist(),
                            cfl=[.25*(32/n)**(2/3) for n in ns],time=.2,
                            norm='Cell-mean density L1' if method['id'] in ('muscl','ppm') else 'Pointwise density L1'))
sources=['numart/reconstruction.py','numart/ausm.py','numart/limiters.py','numart/riemann.py','numart/equations.py','numart/benchmarks.py','scripts/build_reconstruction.py']
data=dict(methods=methods,cases=cases,problems=problems,refinement=studies,flux_cases=flux_cases,
          source_sha256=hashes,
          scope='1D Euler only. FV MUSCL/limited PPM + HLLC; FD JS/Z + global LF splitting. Local conservative characteristics for FV, face-frozen Roe characteristics for FD. SSPRK3. PPM excludes original wave tracing, contact steepening, shock flattening and Lagrange/remap. Reconstruction scaling and rejected inadmissible stages are safeguards, not a full positivity theorem.')
target=ROOT/'website/public/assets/reconstruction';target.mkdir(parents=True,exist_ok=True);(target/'reconstruction.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,2,figsize=(12,7.5))
for ax,name in zip(axs.flat[:3],('sod','moving-contact','shu-osher')):
    p=next(p for p in problems if p['id']==name);ref=np.array(p['reference'])
    ax.plot(p['reference_x'],ref[:,0],'k--',lw=1,label='Analytic' if name!='shu-osher' else 'Internal N=960 reference')
    for m in methods:
        c=next(c for c in cases if c['problem']==name and c['method']==m['id'] and c['basis']=='characteristic')
        ax.plot(c['x'],np.array(c['primitive'])[:,0],color=m['color'],label=m['label'])
    ax.set(xlabel='x',ylabel='density',title=f'{name} | characteristic reconstruction, N={p["n"]}')
    if name=='shu-osher':ax.set_xlim(-1,3)
    ax.legend(fontsize=6)
for m in methods:
    s=next(s for s in studies if s['method']==m['id'] and s['basis']=='characteristic')
    axs[1,1].loglog(s['n'],s['error_l1'],'o-',color=m['color'],label=m['label'])
axs[1,1].set(xlabel='N',ylabel='density L1 / stated representation',title='Smooth entropy wave | temporal refinement controlled');axs[1,1].legend(fontsize=6)
for ax in axs.flat:ax.grid(alpha=.2)
fig.suptitle('Euler reconstruction | PPM-style finite volumes and characteristic FD WENO-Z')
fig.tight_layout();fig.savefig(target/'reconstruction.png',dpi=140,bbox_inches='tight');plt.close(fig)
for s in studies:print(s['method'],s['basis'],s['orders'])

np.savez_compressed(target/"fields.npz",**arrays)
assert hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},"Source changed during build"
data["artifact_sha256"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in target.iterdir() if p.suffix in (".png",".npz")}
(target/"reconstruction.json").write_text(json.dumps(data,separators=(",",":"),allow_nan=False)+"\n")
