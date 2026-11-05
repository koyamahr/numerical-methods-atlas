"""Reproduce original-CIP scalar runs and a Hermite-remapping mass counterexample."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.cip import solve_advection,initial_profile,mass_counterexample,periodic_reconstruction
cases=[]
for profile in ('sine','square'):
    for speed in (1.,-1.):
        for cfl in (.25,.6,1.):
            for time in (.25,1.):
                linear=solve_advection(128,profile,'linear',speed,cfl,time)
                for gradient in ('analytic','centered'):
                    result=solve_advection(128,profile,'cip',speed,cfl,time,gradient)
                    exact,dexact=initial_profile(result.x,profile,time,speed)
                    initial=result.history[0];final=result.history[-1]
                    cases.append(dict(profile=profile,speed=speed,cfl=cfl,time=time,gradient=gradient,n=128,steps=result.steps,
                        x=result.x.tolist(),cip=result.q.tolist(),linear=linear.q.tolist(),exact=exact.tolist(),
                        cip_gradient=result.gradient.tolist(),exact_gradient=dexact.tolist() if profile=='sine' else None,
                        cip_l1=float(np.mean(abs(result.q-exact))),linear_l1=float(np.mean(abs(linear.q-exact))),
                        gradient_l1=float(np.mean(abs(result.gradient-dexact))) if profile=='sine' else None,
                        minimum=final['minimum'],maximum=final['maximum'],
                        mass_before=initial['mass'],mass_after=final['mass'],
                        max_mass_change=max(abs(h['mass']-initial['mass']) for h in result.history),
                        linear_mass_change=linear.history[-1]['mass']-linear.history[0]['mass']))
studies=[]
for method,gradient in (('cip','analytic'),('cip','centered'),('linear','analytic')):
    ns=[32,64,128,256];errors=[];gradient_errors=[]
    for n in ns:
        result=solve_advection(n,'sine',method,1.,.6,.37,gradient)
        exact,dexact=initial_profile(result.x,'sine',.37)
        errors.append(float(np.mean(abs(result.q-exact))))
        if method=='cip':gradient_errors.append(float(np.mean(abs(result.gradient-dexact))))
    studies.append(dict(method=method,gradient=gradient,n=ns,l1=errors,
                        orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist(),gradient_l1=gradient_errors))
counter=mass_counterexample();n=counter['n'];fine=np.linspace(0,4/n,801)
shifted,_=periodic_reconstruction(np.ones(n),np.ones(n),fine-counter['dt'])
remapped,_=periodic_reconstruction(counter['q'],counter['gradient'],fine)
counter['q']=counter['q'].tolist();counter['gradient']=counter['gradient'].tolist()
counter.update(x=fine.tolist(),exact_shifted=shifted.tolist(),remapped=remapped.tolist(),
               initial_description='Periodic C1 Hermite field: every node has q=1 and g=1; small subcell ripples, not a uniform function.')
sources=['numart/cip.py','scripts/build_cip.py']
data=dict(cases=cases,refinement=studies,counterexample=counter,
          source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
          scope='Original 1D cubic-Hermite CIP, constant velocity, point values and independent gradients, periodic uniform grid, adjacent upwind interval with |C|<=1. Linear interpolation comparison stores point values only. No TVD/positivity limiter, rational CIP, CIP-CSL, variable-velocity split, or compressible/multiphase solver.')
target=ROOT/'docs/figures';(target/'cip.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,2,figsize=(12,7.5))
for ax,profile in ((axs[0,0],'sine'),(axs[0,1],'square')):
    c=next(c for c in cases if c['profile']==profile and c['speed']==1 and c['cfl']==.6 and c['time']==1 and c['gradient']=='centered')
    for field,label,color in (('exact','Exact point samples','#23392f'),('cip','CIP / evolved gradient','#bf5b35'),('linear','Linear semi-Lagrangian','#65796c')):
        ax.plot(c['x'],c[field],color=color,label=label,ls='--' if field=='exact' else '-')
    ax.set(xlabel='x',ylabel='point value f',title=f'{profile.title()} | N=128, t=1, CFL=0.6');ax.legend(fontsize=7)
for s,color,label in zip(studies,('#bf5b35','#687fad','#65796c'),('CIP / analytic initial g','CIP / centered initial g','Linear interpolation')):
    axs[1,0].loglog(s['n'],s['l1'],'o-',color=color,label=label)
axs[1,0].set(xlabel='N point nodes',ylabel='Pointwise L1 error',title='Smooth sine refinement | t=0.37, CFL=0.6');axs[1,0].legend(fontsize=7)
axs[1,1].plot(fine,shifted,'--',color='#23392f',label='Exactly translated original field')
axs[1,1].plot(fine,remapped,color='#bf5b35',label='Reconstructed CIP field after one step')
axs[1,1].set(xlabel='x / first four intervals',ylabel='reconstructed f(x)',
             title=f"Grid-scale C1 counterexample | mass {counter['mass_before']:.6f} → {counter['mass_after']:.6f}")
axs[1,1].legend(fontsize=7)
for ax in axs.flat:ax.grid(alpha=.2)
fig.suptitle('Original cubic-Hermite CIP | value + gradient | no conservation or bounds guarantee')
fig.tight_layout();fig.savefig(target/'cip.png',dpi=140,bbox_inches='tight');plt.close(fig)
print(f'Built {len(cases)} paired CIP/linear comparisons, three refinement series, and one conservation counterexample.')
for s in studies:print(s['method'],s['gradient'],s['orders'])
print('Exact-remapping integral change:',counter['mass_after']-counter['mass_before'])
