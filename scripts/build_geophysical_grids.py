"""Draw actual variable locations and semi-discrete f-plane wave symbols."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.geophysical_grids import gravity_frequency
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'docs/figures'
fig=plt.figure(figsize=(13,11));gs=fig.add_gridspec(3,6,height_ratios=[1,1.1,1.1])
colors={'height':'#23392f','u':'#486ba2','v':'#bf5b35'}
for j,grid in enumerate(('A','B','C')):
    ax=fig.add_subplot(gs[0,2*j:2*j+2])
    for q in range(3):
        ax.axhline(q,color='#d2cfc6',lw=1);ax.axvline(q,color='#d2cfc6',lw=1)
    cx,cy=np.meshgrid([.5,1.5],[.5,1.5]);ax.scatter(cx,cy,c=colors['height'],s=28,label='η / scalar center')
    if grid=='A':ux,uy,vx,vy=cx,cy,cx,cy
    elif grid=='B':ux,uy=np.meshgrid(range(3),range(3));vx,vy=ux,uy
    else:
        ux,uy=np.meshgrid(range(3),[.5,1.5]);vx,vy=np.meshgrid([.5,1.5],range(3))
    ax.quiver(ux,uy,np.ones_like(ux),np.zeros_like(uy),color=colors['u'],angles='xy',scale_units='xy',scale=3,width=.012,label='u / x velocity')
    ax.quiver(vx,vy,np.zeros_like(vx),np.ones_like(vy),color=colors['v'],angles='xy',scale_units='xy',scale=3,width=.012,label='v / y velocity')
    ax.set(aspect='equal',xlim=(-.15,2.4),ylim=(-.15,2.4),xticks=[0,1,2],yticks=[0,1,2],xlabel='x / Δ',ylabel='y / Δ',title=f'Arakawa {grid} grid')
    if j==0:ax.legend(loc='upper left',bbox_to_anchor=(0,1.01),fontsize=7,framealpha=.95)
q=np.linspace(0,np.pi,257);series=[]
for row,direction in enumerate(('axis','diagonal'),1):
    for j,ratio in enumerate((.25,2.)):
        ax=fig.add_subplot(gs[row,3*j:3*j+3]);f=1.;h=1.;c=ratio
        continuum=np.sqrt(f*f+(1 if direction=='axis' else 2)*c*c*q*q)
        ax.plot(q/np.pi,continuum,'--',c='black',label='Continuum')
        curves={}
        for grid,color,style in zip(('A','B','C'),('#65796c','#486ba2','#bf5b35'),('-','--','-')):
            omega=np.array([gravity_frequency(grid,k,0 if direction=='axis' else k,h,c,f) for k in q])
            ax.plot(q/np.pi,omega,c=color,ls=style,label=grid);curves[grid]=omega.tolist()
        ax.set(xlabel='kΔ/π; ℓ = 0' if direction=='axis' else 'kΔ/π = ℓΔ/π',ylabel='Gravity frequency ω / |f|',
               title=f'{direction.title()} cut | deformation radius Lᴅ / Δ = {ratio:g}')
        ax.grid(alpha=.2);ax.legend(fontsize=8)
        series.append(dict(direction=direction,deformation_radius_over_spacing=ratio,continuum=continuum.tolist(),curves=curves))
fig.suptitle('Variable staggering changes the operator | centered A/B/C baselines | square periodic f-plane',fontsize=13)
fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(OUT/'geophysical-grids.png',dpi=140);plt.close(fig)
sources=['numart/geophysical_grids.py','scripts/build_geophysical_grids.py']
data=dict(schema_version=1,phase_convention='Physical staggering phase removed; state is (u,v,c eta/H).',
    square_spacing=1.,coriolis=1.,diagonal_k_delta_over_pi=(q/np.pi).tolist(),series=series,
    source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
    scope='Semi-discrete Fourier symbols only: periodic square f-plane, centered pressure/divergence and symmetric four-point C Coriolis. No time discretization, damping, beta plane, coastlines, nonlinear advection or general grid ranking.',
    references=['arakawa1977','riddaway2002','mitgcm-c-grid'])
(OUT/'geophysical-grids.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
print('Built A/B/C placement diagrams and four axis/diagonal dispersion comparisons.')
