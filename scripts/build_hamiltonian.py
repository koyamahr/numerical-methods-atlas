"""Generate the fixed-step Hamiltonian map exhibit and its numerical provenance."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from numart.hamiltonian import METHODS,SYSTEMS,J,canonical_step,trajectory,energy

labels={'symplectic-euler':'Symplectic Euler','verlet':'Störmer–Verlet / Leapfrog',
        'yoshida4':'Yoshida fourth order','midpoint':'Implicit midpoint','rk4':'Classical RK4'}
colors={'symplectic-euler':'#956f39','verlet':'#bf5b35','yoshida4':'#557e66','midpoint':'#677ea0','rk4':'#805e8b'}
# A boundary, not a cloud of independent particles: counterclockwise square.
vertices=np.array([[.58,.28],[.82,.28],[.82,.52],[.58,.52]])
patch=np.concatenate([a+(b-a)*np.linspace(0,1,33,endpoint=False)[:,None]
                      for a,b in zip(vertices,np.roll(vertices,-1,axis=0))])
patch=np.vstack((patch,patch[0]))
cases=[]
for system in SYSTEMS:
    for h in (.1,.2,.4):
        for method in METHODS:
            t,z=trajectory(h=h,steps=round(200/h),method=method,system=system)
            e0=float(energy(z[0],system));err=(energy(z,system)-e0)/e0
            indices=np.unique(np.linspace(0,len(t)-1,min(1001,len(t)),dtype=int))
            mapped=np.array([canonical_step(p,h,method,system) for p in patch])
            _,m=canonical_step([.7,.4],h,method,system,True)
            cases.append({'system':system,'method':method,'h':h,'steps':len(t)-1,
                          't':t[indices].tolist(),'q':z[indices,0].tolist(),'p':z[indices,1].tolist(),
                          'relative_energy_error':err[indices].tolist(),
                          'max_relative_energy_error':float(np.max(abs(err))),
                          'final_relative_energy_error':float(err[-1]),'initial_energy':e0,
                          'mapped_patch':mapped.tolist(),'det_jacobian':float(np.linalg.det(m)),
                          'symplectic_defect':float(np.linalg.norm(m.T@J@m-J))})
source=ROOT/'numart/hamiltonian.py'
data={'methods':[{'id':m,'label':labels[m],'color':colors[m],'symplectic':m!='rk4',
                  'order':{'symplectic-euler':1,'verlet':2,'yoshida4':4,'midpoint':2,'rk4':4}[m]}
                 for m in METHODS], 'cases':cases,'initial':[1.,.2],'final_time':200.,
      'patch':patch.tolist(),'patch_center':[.7,.4],
      'source_sha256':{'hamiltonian.py':hashlib.sha256(source.read_bytes()).hexdigest()},
      'scope':'Fixed-step 1-DOF oscillator examples; sampled trajectories, full-step energy extrema; no equal-cost ranking.'}
figures=ROOT/'docs/figures';figures.mkdir(exist_ok=True)
(figures/'hamiltonian.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
fig,axes=plt.subplots(2,2,figsize=(12,7))
for row,system in enumerate(SYSTEMS):
    for method in METHODS:
        case=next(c for c in cases if c['system']==system and c['h']==.2 and c['method']==method)
        axes[row,0].plot(case['t'],case['relative_energy_error'],lw=.9,label=labels[method],color=colors[method])
        # Keep the first ten time units readable, rather than overplotting 30+ turns.
        t,z=trajectory(h=.2,steps=50,method=method,system=system)
        axes[row,1].plot(z[:,0],z[:,1],lw=.9,color=colors[method],label=labels[method])
    alpha=SYSTEMS[system];e0=float(energy([1.,.2],system))
    qmax=np.sqrt(2*e0 if alpha==0 else (-1+np.sqrt(1+4*alpha*e0))/alpha)
    q=np.linspace(-qmax,qmax,501);p=np.sqrt(np.maximum(0,2*(e0-.5*q*q-alpha*q**4/4)))
    axes[row,1].plot(q,p,'k--',lw=.8,label='Exact initial-energy contour')
    axes[row,1].plot(q,-p,'k--',lw=.8)
    axes[row,0].axhline(0,color='black',lw=.5,ls='--')
    axes[row,0].set(xlabel='time t',ylabel='(H_n - H_0) / H_0',title=system.capitalize()+' | energy, T=200')
    axes[row,1].set(xlabel='q',ylabel='p',title=system.capitalize()+' | phase orbit, T=10',aspect='equal')
    for ax in axes[row]:ax.grid(alpha=.2)
handles,names=axes[0,0].get_legend_handles_labels()
contour_handle,contour_name=axes[0,1].get_legend_handles_labels()
fig.legend(handles+[contour_handle[-1]],names+[contour_name[-1]],loc='lower center',ncol=3,fontsize=8)
fig.suptitle('Canonical maps | fixed step h=0.2 | H=p²/2+q²/2+alpha q⁴/4 | q0=1, p0=0.2')
fig.tight_layout(rect=(0,.07,1,.96));fig.savefig(figures/'hamiltonian.png',bbox_inches='tight');plt.close(fig)
print(f'Generated {len(cases)} Hamiltonian trajectories, phase maps, and a computed gallery figure.')
