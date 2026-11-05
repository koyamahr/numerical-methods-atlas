"""Reproduce the limiter notebook, including TVB and state-scaling exhibits."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart import solve, get_problem
from numart.limiters import LIMITERS, limiter_function, positive_reconstruction, euler_pressure
from numart.tvd import solve_advection, cell_average

labels = ['minmod', 'Superbee', 'MC / monotonized central', 'van Leer', 'van Albada / clipped']
colors = ['#65796c', '#bf5b35', '#687fad', '#9872a2', '#b49438']
methods = [dict(id=k, label=v, color=c) for k,v,c in zip(LIMITERS,labels,colors)]
methods += [dict(id='upwind',label='First-order upwind',color='#98968e'),
            dict(id='unlimited',label='Unlimited centered slope',color='#293c48'),
            dict(id='tvb',label='TVB modified minmod',color='#be6579')]
r = np.linspace(-.25, 4., 341)
cases = []
for profile in ('square', 'sine'):
    for speed in (1., -1.):
        for method in methods:
            for M in ((0.,10.,50.) if method['id']=='tvb' else (0.,)):
                result = solve_advection(200,profile,method['id'],speed,1.,.3,M)
                exact = cell_average(result.x,1/200,profile,1.,speed)
                h0,h1 = result.history[0],result.history[-1]
                cases.append(dict(profile=profile,method=method['id'],M=M,speed=speed,
                                  x=result.x.tolist(),q=result.q.tolist(),exact=exact.tolist(),
                                  n=200,time=result.time,steps=result.steps,cfl=.3,
                                  error_l1=float(np.mean(abs(result.q-exact))),
                                  initial_tv=h0['tv'],final_tv=h1['tv'],
                                  max_tv=max(h['tv'] for h in result.history),
                                  minimum=h1['minimum'],maximum=h1['maximum'],
                                  mass_change=h1['mass']-h0['mass']))
problem=get_problem('sod')
for method in methods[:5]:
    result=solve(problem,n=200,limiter=method['id'])
    exact=problem.reference(result.x,result.time)[:,0]
    cases.append(dict(profile='sod',method=method['id'],M=0.,speed=0.,
                      x=result.x.tolist(),q=result.q[:,0].tolist(),exact=exact.tolist(),n=200,
                      time=result.time,steps=result.steps,cfl=.3,
                      error_l1=float(np.mean(abs(result.q[:,0]-exact))),
                      minimum=float(result.q[:,0].min()),maximum=float(result.q[:,0].max()),
                      min_pressure=float(problem.equation.primitive(result.q)[:,2].min())))
refinement=[]
for method,M in [(k,0.) for k in LIMITERS]+[('tvb',50.)]:
    ns=[40,80,160]; errors=[]
    for n in ns:
        result=solve_advection(n,'sine',method,final_time=.2,tvb_M=M)
        errors.append(float(np.mean(abs(result.q-cell_average(result.x,1/n,'sine',.2)))))
    refinement.append(dict(method=method,M=M,n=ns,error_l1=errors,
                           orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()))
mean=np.array([1.,0.,2.5]); nodes=np.array([-1.,0.,1.]); weights=np.array([1/6,2/3,1/6])
scaling=[]
for name,delta in [('density',[1.2,0.,0.]),('pressure',[0.,3.,0.]),('combined',[1.2,3.,1.])]:
    raw=mean+nodes[:,None]*delta
    limited,theta=positive_reconstruction(mean,raw,density_floor=1.e-8,pressure_floor=1.e-8)
    scaling.append(dict(name=name,nodes=nodes.tolist(),mean=mean.tolist(),weights=weights.tolist(),
                        raw=raw.tolist(),limited=limited.tolist(),theta=theta,
                        raw_pressure=euler_pressure(raw).tolist(),limited_pressure=euler_pressure(limited).tolist(),
                        mean_error=float(abs(weights@limited-mean).max()),
                        floor=1.e-8,gamma=1.4))
sources=['numart/limiters.py','numart/tvd.py','numart/solvers.py','numart/benchmarks.py',
         'numart/equations.py','numart/riemann.py','scripts/build_limiters.py']
data=dict(methods=methods,r=r.tolist(),phi={k:limiter_function(r,k).tolist() for k in LIMITERS},
          cases=cases,refinement=refinement,scaling=scaling,
          source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
          scope='Scalar: exact cell averages, periodic MUSCL + SSPRK3. Sod: primitive MUSCL + HLLC + SSPRK3, pointwise reference. TVB: scalar modified-minmod demonstration. Positivity: reconstruction only, no Euler time-update guarantee.')
target=ROOT/'docs/figures'
(target/'limiters.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,2,figsize=(12,7.5))
for method in methods[:5]:
    k=method['id'];color=method['color'];label=method['label']
    axs[0,0].plot(r,data['phi'][k],color=color,label=label)
    for ax,profile in ((axs[0,1],'square'),(axs[1,0],'sod')):
        c=next(c for c in cases if c['profile']==profile and c['method']==k and c['speed']>=0)
        ax.plot(c['x'],c['q'],color=color,label=label)
    study=next(s for s in refinement if s['method']==k)
    axs[1,1].loglog(study['n'],study['error_l1'],'o-',color=color,label=label)
upper=np.maximum(0,np.minimum(2*r,2));axs[0,0].fill_between(r,0,upper,color='#65796c',alpha=.1)
axs[0,0].set(xlabel='r = backward / forward increment',ylabel='phi(r)',title='Sweby bounds for these scalar slope functions')
for ax,profile in ((axs[0,1],'square'),(axs[1,0],'sod')):
    c=next(c for c in cases if c['profile']==profile and c['method']=='minmod' and c['speed']>=0)
    ax.plot(c['x'],c['exact'],'k--',lw=1,label='Exact cell averages' if profile=='square' else 'Exact pointwise density')
    ax.set(xlabel='x',ylabel='u' if profile=='square' else 'density',title='Square pulse | N=200, t=1' if profile=='square' else 'Sod | N=200, t=0.2, HLLC')
axs[1,1].set(xlabel='N cells',ylabel='Cell-average L1 error',title='Smooth sine refinement | t=0.2, CFL=0.3')
for ax in axs.flat:
    ax.grid(alpha=.2);ax.legend(fontsize=6)
fig.suptitle('Slope limiters | same mesh, flux, and SSPRK3; no equal-cost ranking')
fig.tight_layout();fig.savefig(target/'limiters.png',dpi=140,bbox_inches='tight');plt.close(fig)
print(f'Built {len(cases)} computed curves, {len(refinement)} refinement studies, and {len(scaling)} state-scaling cases.')
for s in refinement: print(s['method'],s['M'],s['error_l1'],s['orders'])
