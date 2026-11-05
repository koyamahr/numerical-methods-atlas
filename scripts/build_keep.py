"""Smooth-vortex validation of the original arithmetic-mean KEEP flux."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.keep import solve_vortex,vortex_state
studies=[];solutions={}
for n in (48,96,192):
    result=solve_vortex(n,1.,cfl=.25);initial=result.history[0]
    mass=initial['mass']
    errors={key:max(abs(h[key]-initial[key]) for h in result.history)/max(abs(initial[key]),1.)
            for key in ('mass','momentum_x','momentum_y','total_energy')}
    study={'n':n,'time':result.time,'steps':result.steps,'density_l1':result.density_l1,
           'max_primary_relative_drifts':errors,
           'max_entropy_proxy_change_per_mass':max(abs(h['entropy_proxy']-initial['entropy_proxy']) for h in result.history)/mass,
           'history':result.history}
    studies.append(study);solutions[n]=result.q
refined_time=solve_vortex(96,1.,cfl=.125)
time_difference=float(np.mean(abs(refined_time.q[:, :,0]-solutions[96][:,:,0])))
figures=ROOT/'docs/figures'
sources=('numart/keep.py','numart/euler2d.py','numart/snapshots.py','scripts/build_keep.py')
data={'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
      'scheme':'Original arithmetic-mean second-order Cartesian KEEP; no shock dissipation or PEP extension',
      'time_integrator':'Classical RK4','gamma':1.4,'domain':[[-10,10],[-10,10]],
      'beta':3.,'background_velocity':[1.,.5],'cfl':.25,'studies':studies,
      'time_refinement':{'n':96,'cfl':[.25,.125],'density_difference_l1':time_difference},
      'scope':'Smooth periodic vortex, pointwise analytic reference; not original-paper TGV reproduction or a shock-capturing claim.'}
(figures/'keep-vortex.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
fig,axes=plt.subplots(2,2,figsize=(12,7))
n=96;c=(np.arange(n)+.5)*20/n-10;x,y=np.meshgrid(c,c,indexing='ij')
exact=vortex_state(x,y,1.);q=solutions[n]
# Restrict the display to the vortex neighborhood, while the solve remains on L=20.
mask=(c>=-3)&(c<=5);visible=q[:,:,0][np.ix_(mask,mask)]
image=axes[0,0].imshow(visible.T,origin='lower',extent=[c[mask][0]-.5*20/n,c[mask][-1]+.5*20/n]*2,cmap='magma',aspect='equal')
fig.colorbar(image,ax=axes[0,0],label='density')
axes[0,0].set(xlabel='x',ylabel='y',title='Advected isentropic vortex | 96², t=1')
error=(q[:,:,0]-exact[:,:,0])[np.ix_(mask,mask)];limit=max(abs(error).max(),1e-15)
image=axes[0,1].imshow(error.T,origin='lower',extent=[c[mask][0]-.5*20/n,c[mask][-1]+.5*20/n]*2,cmap='RdBu_r',vmin=-limit,vmax=limit,aspect='equal')
fig.colorbar(image,ax=axes[0,1],label='density error')
axes[0,1].set(xlabel='x',ylabel='y',title='Pointwise error against analytic translation')
ns=[s['n'] for s in studies];errs=[s['density_l1'] for s in studies]
axes[1,0].loglog(ns,errs,'o-',color='#bf5b35',label='Measured density L1')
axes[1,0].loglog(ns,[errs[0]*(ns[0]/n)**2 for n in ns],'k--',label='N^-2 reference')
axes[1,0].set(xlabel='cells per direction N',ylabel='mean |rho-rho_exact|',title='Smooth spatial refinement | fixed CFL=0.25')
for study,color in zip(studies,('#bf5b35','#557e66','#677ea0')):
    h=study['history'];s0=h[0]['entropy_proxy'];mass=h[0]['mass']
    axes[1,1].plot([v['time'] for v in h],[(v['entropy_proxy']-s0)/mass for v in h],color=color,label=str(study['n'])+'²')
axes[1,1].set(xlabel='time t',ylabel='(S_proxy - S_proxy,0) / mass',title='Entropy preservation is approximate, not exact')
for ax in (axes[1,0],axes[1,1]):ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.suptitle('Original second-order KEEP + RK4 | smooth vortex only | no shock stabilization')
fig.tight_layout();fig.savefig(figures/'keep-vortex.png',bbox_inches='tight');plt.close(fig)
for s in studies:print(s['n'],s['density_l1'],s['max_entropy_proxy_change_per_mass'],s['max_primary_relative_drifts'])
print('Temporal CFL-halving density difference:',time_difference)
