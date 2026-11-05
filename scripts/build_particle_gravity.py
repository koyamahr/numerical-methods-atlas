"""Reproducible isolated-tree and periodic-PM figures; distinct problems."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.particle_gravity import direct_acceleration,tree_acceleration,pm_acceleration,periodic_poisson
rng=np.random.default_rng(17);x=rng.random((192,3));m=np.ones(192)/192
exact=direct_acceleration(x,m);measurements=[]
for order in (0,2):
    for theta in (.25,.4,.6,.8,1.):
        a,work=tree_acceleration(x,m,theta=theta,order=order)
        measurements.append({'order':order,'theta':theta,
                             'relative_rms_force_error':float(np.linalg.norm(a-exact)/np.linalg.norm(exact)),
                             'normalized_net_force':float(np.linalg.norm(np.sum(m[:,None]*a,axis=0))/np.sum(m*np.linalg.norm(exact,axis=1))),
                             **work})
a_pm,rho,phi=pm_acceleration(x,m,n=24)
n=24;axis=np.arange(n)/n
wave=np.broadcast_to((1+.2*np.cos(2*np.pi*axis))[:,None,None],(n,n,n))
wave_phi,wave_acc=periodic_poisson(wave)
reference=-.2/np.pi*np.cos(2*np.pi*axis)
source=ROOT/'numart/particle_gravity.py'
data={'source_sha256':{'particle_gravity.py':hashlib.sha256(source.read_bytes()).hexdigest()},
      'isolated_tree':{'n':192,'seed':17,'softening':.03,'gravity':1.,'boundary':'isolated',
                       'reference':'direct Plummer-softened pair sum, identical particles and softening',
                       'measurements':measurements},
      'periodic_pm':{'n':24,'length':1.,'gravity':1.,'boundary':'3D periodic, mean density subtracted',
                     'total_deposited_mass':float(rho.sum()/24**3),
                     'mass_weighted_net_force':np.sum(m[:,None]*a_pm,axis=0).tolist(),
                     'manufactured_potential_max_error':float(np.max(abs(wave_phi[:,0,0]-reference))),
                     'manufactured_density':'1+0.2*cos(2*pi*x)',
                     'scope':'Mesh Poisson accuracy only; not a periodic direct-sum force comparison'},
      'scope':'Static force/Poisson tests; no P3M, TreePM, FMM implementation or timing comparison.'}
figures=ROOT/'docs/figures';(figures/'particle-gravity.json').write_text(json.dumps(data,indent=2)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
fig,axes=plt.subplots(2,2,figsize=(12,7))
for order,label,color in ((0,'Monopole','#bf5b35'),(2,'Second moment','#557e66')):
    study=[c for c in measurements if c['order']==order]
    axes[0,0].semilogy([c['theta'] for c in study],[c['relative_rms_force_error'] for c in study],'o-',color=color,label=label)
    axes[0,1].plot([c['theta'] for c in study],[c['direct_pairs']+c['accepted_nodes'] for c in study],'o-',color=color,label=label)
axes[0,1].axhline(192*191,color='black',lw=.8,ls='--',label='Direct ordered pairs')
axes[0,0].set(xlabel='opening angle theta',ylabel='||a_tree-a_direct||2 / ||a_direct||2',title='Isolated Newton gravity | softened kernel, N=192')
axes[0,1].set(xlabel='opening angle theta',ylabel='accepted nodes + direct pairs',title='Interaction counts | unequal operation costs')
image=axes[1,0].imshow(rho.sum(axis=2).T/24,origin='lower',extent=[0,1,0,1],cmap='magma')
fig.colorbar(image,ax=axes[1,0],label='projected mass density')
axes[1,0].set(xlabel='x',ylabel='y',title='Periodic PM | CIC mass assignment, 24 cubed')
axes[1,1].plot(axis,reference,'k--',label='Analytic potential')
axes[1,1].plot(axis,wave_phi[:,0,0],'o',ms=3,color='#677ea0',label='FFT mesh potential')
axes[1,1].set(xlabel='x',ylabel='potential phi',title='Periodic manufactured density | 1 + 0.2 cos(2 pi x)')
for ax in (axes[0,0],axes[0,1],axes[1,1]):ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.suptitle('Particle gravity and Poisson solvers | isolated tree and periodic PM are different boundary problems')
fig.tight_layout();fig.savefig(figures/'particle-gravity.png',bbox_inches='tight');plt.close(fig)
print('Generated tree opening-angle study and periodic PM manufactured-solution checks.')
