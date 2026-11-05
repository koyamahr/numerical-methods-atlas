"""Build isolated/slab kernel figures from independent reference checks."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.gravity_boundaries import isolated_potential,slab_potential,slab_green_transform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
fig,axes=plt.subplots(2,2,figsize=(12,7))
n=24;point=np.zeros((n,4,4));point[0,1,1]=1;phi=isolated_potential(point)
x=np.arange(1,n)
axes[0,0].plot(x,-1/x,'k--',label='Isolated direct kernel -1/r')
axes[0,0].plot(x,phi[1:,1,1],'o',ms=3,color='#bf5b35',label='Doubled FFT, source at boundary')
axes[0,0].set(xlabel='grid separation r',ylabel='potential',title='Isolated 3D | no near image across the box')
nz=32;z=(np.arange(nz)+.5)/nz-.5
uniform=slab_potential(np.ones((8,8,nz)))[0,0];analytic=2*np.pi*z*z
axes[0,1].plot(z,analytic-analytic.mean(),'k--',label='2 pi z², constant removed')
axes[0,1].plot(z,uniform-uniform.mean(),'o',ms=3,color='#557e66',label='Slab FFT, horizontal k=0 retained')
axes[0,1].set(xlabel='z',ylabel='potential minus its mean',title='Mean slab | uniform density, G=1')
mode=np.zeros((16,4,nz));j=nz//2;xx=np.arange(16)/16
mode[:,:,j]=nz*np.cos(2*np.pi*xx[:,None])
wave=slab_potential(mode)[0,0];reference=-np.exp(-2*np.pi*abs(z-z[j]))
axes[1,0].plot(z,reference,'k--',label='-exp(-2 pi |z-z0|)')
axes[1,0].plot(z,wave,'o',ms=3,color='#677ea0',label='Sampled-kernel slab FFT')
axes[1,0].set(xlabel='z',ylabel='potential at x=0',title='Sinusoidal sheet | horizontal k=2 pi')
ns=[8,16,32,64,128];errors=[]
for size in ns:
    sampled=slab_green_transform(2.,size,1.).real[:4]
    continuum=slab_green_transform(2.,size,1.,'continuum')[:4]
    errors.append(float(np.linalg.norm(sampled-continuum)))
axes[1,1].loglog(ns,errors,'o-',color='#805e8b',label='First four vertical coefficients')
axes[1,1].loglog(ns,[errors[0]*(ns[0]/v)**2 for v in ns],'k--',label='Nz^-2 reference')
axes[1,1].set(xlabel='vertical cells Nz',ylabel='coefficient difference norm',title='Sampled DFT vs continuous coefficient | k=2')
for ax in axes.flat:ax.grid(alpha=.2);ax.legend(fontsize=7)
fig.suptitle('Isolated and slab gravity | different Green functions and explicit zero-mode treatment')
fig.tight_layout();figures=ROOT/'docs/figures';fig.savefig(figures/'gravity-boundaries.png',bbox_inches='tight');plt.close(fig)
source=ROOT/'numart/gravity_boundaries.py'
data={'source_sha256':{'gravity_boundaries.py':hashlib.sha256(source.read_bytes()).hexdigest()},
      'isolated_boundary_point_max_error':float(np.max(abs(phi[1:,1,1]+1/x))),
      'uniform_slab_gauge_aligned_max_error':float(np.max(abs((uniform-uniform.mean())-(analytic-analytic.mean())))),
      'sinusoidal_sheet_max_error':float(np.max(abs(wave-reference))),
      'transform_nz':ns,'transform_difference_norm':errors,
      'scope':'Discrete convolution identities and manufactured sheets; not continuum mesh-convergence certification or a reproduction of the 2009 flow simulations.'}
(figures/'gravity-boundaries.json').write_text(json.dumps(data,indent=2)+'\n')
print('Generated isolated and slab FFT kernel figure and verification manifest.')
