"""Reproduce RK family metadata, stability contours, stages, and refinement."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.runge_kutta import TABLEAUS,stability_polynomial,stability_function,rk_step,nonlinear_trajectory
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
colors=['#98968e','#65796c','#9872a2','#b49438','#8b6d52','#bf5b35','#687fad','#293c48','#be6579']
grid=np.linspace(-6,2,401);imag=np.linspace(-4,4,401);xx,yy=np.meshgrid(grid,imag)
methods=[];cases=[];studies=[]
for (key,m),color in zip(TABLEAUS.items(),colors):
    fig,ax=plt.subplots();contour=ax.contour(xx,yy,abs(stability_function(xx+1j*yy,key)),levels=[1.])
    boundaries=[v.tolist() for v in contour.allsegs[0] if len(v)>1];plt.close(fig)
    methods.append(dict(id=key,label=m['label'],family=m['family'],order=m['order'],stages=m['stages'],
                        ssp_coefficient=m['ssp_coefficient'],color=color,
                        A=m['A'].tolist(),b=m['b'].tolist(),c=m['c'].tolist(),
                        stability_polynomial=stability_polynomial(key).tolist(),stability_boundary=boundaries))
    for h in (.25,.5,1.):
        result,stages=rk_step(lambda t,y:-y*y,0.,1.,h,key,return_stages=True)
        cases.append(dict(method=key,dt=h,result=float(result),exact=1/(1+h),
                          error=abs(float(result)-1/(1+h)),
                          stages=[dict(stage=s['stage'],time=s['time'],value=float(s['value']),rhs=float(s['rhs'])) for s in stages]))
    ns=[10,20,40,80];errors=[]
    for n in ns:
        t,y=nonlinear_trajectory(key,n)
        errors.append(float(abs(y[-1]-.5)))
    studies.append(dict(method=key,n=ns,dt=[1/n for n in ns],rhs_calls=[m['stages']*n for n in ns],
                        error=errors,orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()))
sources=['numart/runge_kutta.py','scripts/build_runge_kutta.py']
data=dict(methods=methods,cases=cases,refinement=studies,
          stability_domain=dict(real=[-6,2],imaginary=[-4,4],grid_shape=[401,401],contour_level=1.),
          nonlinear_problem=dict(equation="y'=-y^2",initial=1.,exact='1/(1+t)',final_time=1.),
          source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
          scope='Nine fixed-step explicit RK methods. SSP coefficient is a forward-Euler inheritance bound, not a scalar stability interval or a guarantee without the spatial premise. SSPRK54 uses decimal source coefficients and a conservative rounded C=1.508. Contours are sampled |R(z)|=1 boundaries, not nonlinear stability proofs.')
target=ROOT/'docs/figures';(target/'runge-kutta.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
fig,axs=plt.subplots(2,2,figsize=(12,7.5))
for m in methods:
    for boundary in m['stability_boundary']:
        v=np.asarray(boundary);axs[0,0].plot(v[:,0],v[:,1],color=m['color'],lw=1.2)
    s=next(s for s in studies if s['method']==m['id'])
    axs[1,0].loglog(s['dt'],s['error'],'o-',color=m['color'],label=m['label'])
    axs[1,1].plot([m['stages']],[m['ssp_coefficient']],'o',color=m['color'])
    axs[1,1].annotate(m['label'],(m['stages'],m['ssp_coefficient']),xytext=(5,5 if m['id']!='explicit-midpoint' else -12),textcoords='offset points',fontsize=6)
for key in ('heun','explicit-midpoint','ralston'):
    c=next(c for c in cases if c['method']==key and c['dt']==.5)
    m=next(m for m in methods if m['id']==key)
    axs[0,1].scatter([s['time'] for s in c['stages']],[s['value'] for s in c['stages']],color=m['color'],label=m['label'])
    axs[0,1].scatter([.5],[c['result']],marker='x',color=m['color'])
t=np.linspace(0,.5,101);axs[0,1].plot(t,1/(1+t),'k--',label='Exact y=1/(1+t)')
axs[0,0].axvline(0,color='k',lw=.5);axs[0,0].axhline(0,color='k',lw=.5)
axs[0,0].set(xlabel='Re(z)',ylabel='Im(z)',title='Sampled linear stability boundaries |R(z)|=1',xlim=(-6,2),ylim=(-4,4),aspect='equal')
axs[0,1].set(xlabel='Stage time c_i h',ylabel='Stage predictor / final value',title='RK2: identical linear R, different nonlinear stages')
axs[0,1].legend(fontsize=7)
axs[1,0].set(xlabel='Step size h',ylabel='Final absolute error',title="Nonlinear y′=−y², T=1 | fixed-step refinement")
axs[1,0].legend(fontsize=6)
axs[1,1].set(xlabel='RHS evaluations per step / stages s',ylabel='Nonlinear SSP coefficient C',title='Stages, order, and SSP are independent labels',xlim=(.7,6.7),ylim=(-.2,2.35))
for ax in axs.flat:ax.grid(alpha=.2)
fig.suptitle('Runge–Kutta families | accuracy, stage structure, linear stability, and SSP inheritance')
fig.tight_layout();fig.savefig(target/'runge-kutta.png',dpi=140,bbox_inches='tight');plt.close(fig)
print(f'Built {len(methods)} RK tableaus, {len(cases)} nonlinear one-step cases, and {len(studies)} refinement studies.')
for s in studies:print(s['method'],s['orders'])
