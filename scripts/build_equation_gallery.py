"""Reproduce equation-gallery profiles and method-extension validation figures."""
from pathlib import Path
import hashlib, json, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.scalar_gallery import solve, riemann_cell_averages
from numart.snapshots import SnapshotRecorder
from numart.benchmarks import get_problem
from numart.solvers import solve as solve_system
from numart.fem import poisson_2d, error_norms
from numart.krylov import advection_diffusion_matrix, gmres, bicgstab, jacobi_preconditioner, ilu0_preconditioner
from numart.stiff import integrate, adaptive_sdirk2
from numart.incompressible import taylor_green
from numart.lattice_boltzmann import shear_wave, poiseuille
from numart.hyperbolic_diffusion import steady_sine
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'docs/figures';OUT.mkdir(exist_ok=True)

def digest(paths):
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}

def frame(t,step,u,exact,initial_mass,measure='cell averages'):
    return dict(time=float(t),step=int(step),u=np.asarray(u).tolist(),
                exact=None if exact is None else np.asarray(exact).tolist(),
                l1=None if exact is None else float(np.mean(abs(u-exact))),
                mean=float(np.mean(u)),mean_change=float(np.mean(u)-initial_mass),reference_measure=measure)

n=128; x=(np.arange(n)+.5)/n; cases=[]
for equation,left,right,title in [('burgers',1.,0.,'Burgers / shock'),('burgers',0.,1.,'Burgers / rarefaction'),
                                  ('traffic',.3,.9,'Traffic / upstream jam'),('traffic',.9,.1,'Traffic / clearing fan')]:
    initial=riemann_cell_averages(n,0,left,right,equation)
    run=solve(initial,.4,equation,snapshot_times=np.linspace(0,.4,41))
    frames=[frame(s.time,s.step,s.q,riemann_cell_averages(n,s.time,left,right,equation),initial.mean()) for s in run['snapshots']]
    cases.append(dict(id=title.lower().replace(' / ','-').replace(' ','-'),title=title,family='scalar conservation law',
        equation='uₜ + (u²/2)ₓ = 0' if equation=='burgers' else 'ρₜ + [ρ(1−ρ)]ₓ = 0',
        characteristic='f′(u) = u' if equation=='burgers' else 'f′(ρ) = 1−2ρ; vehicle speed = 1−ρ',
        initial=f'Left {left}, right {right}; jump at x=0.5',boundary='Outflow / endpoint continuation',
        method='Godunov flux · MUSCL minmod · SSPRK(3,3)',field='u' if equation=='burgers' else 'density ρ',
        note='Exact cell integrals of the entropy Riemann solution. An upstream traffic shock moves at −0.2 while vehicles move forward.' if equation=='traffic' else 'Convex flux: a decreasing jump shocks; an increasing jump spreads into a fan.',
        reference='burgers1948' if equation=='burgers' else 'lighthill1955',chapter='equation-gallery',
        n=n,x=x.tolist(),limits=[-.05,1.05],sampling='Completed adaptive-CFL states; output requests do not alter solver steps.',frames=frames))
for kind in ('advection','heat'):
    nu=.02; a=1.; initial=1+.25*np.sinc(1/n)*np.sin(2*np.pi*x)
    u=initial.copy();t=0.;k=0;end=1.;rec=SnapshotRecorder(np.linspace(0,end,41),end);rec.capture(t,k,u)
    while t<end:
        dt=min(end-t,.4/n if kind=='advection' else .4/(nu*n*n))
        u += -a*dt*n*(u-np.roll(u,1)) if kind=='advection' else nu*dt*n*n*(np.roll(u,1)-2*u+np.roll(u,-1))
        t+=dt;k+=1;rec.capture(t,k,u)
    frames=[]
    for s in rec.frames:
        exact=1+.25*np.sinc(1/n)*np.sin(2*np.pi*(x-s.time if kind=='advection' else x))*(1 if kind=='advection' else np.exp(-nu*(2*np.pi)**2*s.time))
        frames.append(frame(s.time,s.step,s.q,exact,initial.mean()))
    cases.append(dict(id=kind,title='Linear advection / translation' if kind=='advection' else 'Heat / mode decay',
        family='linear hyperbolic' if kind=='advection' else 'parabolic',equation='uₜ + uₓ = 0' if kind=='advection' else 'uₜ = 0.02 uₓₓ',
        characteristic='a = +1' if kind=='advection' else 'Fourier decay exp(−νk²t); no finite characteristic speed',
        initial='1 + 0.25 sin(2πx), initialized as exact cell averages',boundary='Periodic [0,1]',
        method='First-order upwind / forward Euler' if kind=='advection' else 'Centered diffusion / forward Euler; νΔt/Δx² ≤ 0.4',
        field='u',note='Exact sine-mode cell averages; the discrete mean is conserved.',reference='leveque2002',chapter='stability' if kind=='advection' else 'elliptic',
        n=n,x=x.tolist(),limits=[.7,1.3],sampling='Completed solver steps; snapshots do not change time steps.',frames=frames))
# Existing baseline has no 1D snapshot API: keep independent final-time solves
# explicit, rather than relabeling them as one uninterrupted trajectory.
for name,title,eq,characteristic in [('sod','Euler / Sod shock tube','Uₜ + F(U)ₓ = 0; γ = 1.4','u−c, u, u+c'),
    ('dam-break','Shallow water / wet dam break','hₜ + (hu)ₓ = 0; (hu)ₜ + (hu²+h²/2)ₓ = 0','u ± √h; g = 1'),
    ('isothermal','Isothermal / density jump','ρₜ + (ρu)ₓ = 0; (ρu)ₜ + (ρu²+ρ)ₓ = 0','u ± 1; cₛ = 1')]:
    p=get_problem(name);frames=[];m=p.initial(p.grid(n))[:,0].mean()
    for t in np.linspace(0,p.final_time,25):
        r=solve_system(p,n=n,riemann='hllc' if name=='sod' else 'hll',final_time=float(t))
        exact=p.reference(r.x,t)[:,0] if p.reference else None
        frames.append(frame(r.time,r.steps,r.q[:,0],exact,m,'point-sampled exact Euler density' if exact is not None else 'no exact overlay supplied'))
    cases.append(dict(id=name,title=title,family='hyperbolic system',equation=eq,characteristic=characteristic,
        initial='Rest; left/right density 1 / 0.125, pressure 1 / 0.1' if name=='sod' else 'Rest; left/right depth 2 / 1' if name=='dam-break' else 'Rest; left/right density 1 / 0.125',
        boundary='Outflow; jump at x=0.5',method='Primitive MUSCL minmod · SSPRK3 · '+('HLLC' if name=='sod' else 'HLL'),
        field='depth h' if name=='dam-break' else 'density ρ',note='Euler exact reference is point sampled; L1 is a sample comparison, not an integrated FV error.' if name=='sod' else 'Computed baseline only. Exact shallow-water/isothermal overlays, dry beds and bottom topography remain separate work.',
        reference='sod1978' if name=='sod' else 'leveque2002',chapter='benchmarks',n=n,x=x.tolist(),limits=[0,2.1] if name=='dam-break' else [0,1.1],
        sampling='Each displayed time is an independent solve from the same initial data, shortened only to its final time. Playback connects these separate runs.',frames=frames))
data=dict(schema_version=1,cases=cases,source_sha256=digest(['numart/scalar_gallery.py','numart/snapshots.py','numart/solvers.py','numart/riemann.py','numart/equations.py','numart/benchmarks.py','scripts/build_equation_gallery.py']),
          scope='Precomputed educational 1D profiles on [0,1]. Scalars use exact cell-average Riemann/sine references; Euler has point-sampled exact data; SWE/isothermal have no exact overlay. No browser PDE solver or solver-speed ranking.')
(OUT/'equation-gallery.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
fig,axs=plt.subplots(2,3,figsize=(13,7.3))
for ax,c in zip(axs.flat,[cases[i] for i in (0,1,2,3,4,5)]):
    f=c['frames'][-1];ax.plot(c['x'],f['u'],color='#bf5b35',label='Computed')
    ax.plot(c['x'],f['exact'],'--',color='#23392f',label='Exact cell averages')
    ax.set(title=c['title']+f" | t={f['time']:.2f}",xlabel='x',ylabel=c['field'],ylim=c['limits']);ax.grid(alpha=.2)
axs[0,0].legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'equation-gallery.png',dpi=140);plt.close(fig)

# FEM, nonsymmetric solvers, stiff ODE and incompressible-flow evidence.
exact=lambda p:np.sin(np.pi*p[:,0])*np.sin(np.pi*p[:,1])
grad=lambda p:np.pi*np.column_stack((np.cos(np.pi*p[:,0])*np.sin(np.pi*p[:,1]),np.sin(np.pi*p[:,0])*np.cos(np.pi*p[:,1])))
ns=[4,8,16,32];femerrors=np.array([error_norms(poisson_2d(n),exact,grad) for n in ns]);fem=poisson_2d(16)
a=advection_diffusion_matrix(16);b=a.matvec(np.sin(np.arange(256)*.173)+1);histories=[]
for name,solver,pre in [('GMRES / none',gmres,None),('GMRES / Jacobi',gmres,jacobi_preconditioner(a)),('GMRES / ILU(0)',gmres,ilu0_preconditioner(a)),('BiCGSTAB / ILU(0)',bicgstab,ilu0_preconditioner(a))]:
    r=solver(a,b,preconditioner=pre,maxiter=600)
    assert r.converged,r.reason
    histories.append(dict(name=name,residuals=(r.residuals/np.linalg.norm(b)).tolist(),iterations=r.iterations))
f=lambda t,y:-1000*(y-np.cos(t))-np.sin(t);jac=lambda t,y:-1000*np.eye(len(y))
dts=[.1,.05,.025,.0125];ode=[]
for method in ('be','bdf2','sdirk2'):
    errors=[]
    for dt in dts:
        tt,yy=integrate(f,jac,[1.],dt=dt,method=method);errors.append(float(np.max(abs(yy[:,0]-np.cos(tt)))))
    ode.append(dict(method=method,dt=dts,maximum_error=errors,orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()))
adaptive=adaptive_sdirk2(f,jac,[1.],rtol=1e-6)
mac=[taylor_green(n) for n in (16,32,64)];flow=mac[1]
fig,axs=plt.subplots(2,3,figsize=(13,7.5))
artist=axs[0,0].tripcolor(fem.points[:,0],fem.points[:,1],fem.cells,fem.u,shading='gouraud');fig.colorbar(artist,ax=axs[0,0]);axs[0,0].set(title='Continuous P1 Poisson | triangular FEM',xlabel='x',ylabel='y')
for j,label in enumerate(('L2 error','H1 seminorm')):axs[0,1].loglog(ns,femerrors[:,j],'o-',label=label)
axs[0,1].set(title='Inside-element quadrature errors',xlabel='Subdivisions per side',ylabel='Error');axs[0,1].legend(fontsize=8)
for entry in histories:axs[0,2].semilogy(entry['residuals'],label=entry['name'])
axs[0,2].set(title='Nonsymmetric advection–diffusion',xlabel='Iteration (costs differ)',ylabel='True residual / ||b||');axs[0,2].legend(fontsize=7)
for entry in ode:axs[1,0].loglog(dts,entry['maximum_error'],'o-',label=entry['method'])
axs[1,0].set(title='Stiff forced ODE | κ=1000',xlabel='Time step',ylabel='Maximum nodal-time error');axs[1,0].legend(fontsize=8)
axs[1,1].loglog([16,32,64],[r['error'] for r in mac],'o-',label='MAC / SSPRK2');axs[1,1].set(title='Taylor–Green velocity refinement',xlabel='Cells per side',ylabel='Combined velocity RMS error');axs[1,1].legend(fontsize=8)
axs[1,2].plot(flow['history'][:,0],flow['history'][:,1],label='Computed');axs[1,2].plot(flow['history'][:,0],.25*np.exp(-.4*flow['history'][:,0]),'--',label='Continuum exact');axs[1,2].set(title='Kinetic energy | periodic MAC',xlabel='Physical time',ylabel='Mean kinetic energy');axs[1,2].legend(fontsize=8)
for ax in axs.flat:ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(OUT/'solver-foundations.png',dpi=140);plt.close(fig)

shear=shear_wave(32,steps=400);channels=[poiseuille(n) for n in (8,16,32)];hyp=[steady_sine(n) for n in (32,64,128)]
fig,axs=plt.subplots(2,2,figsize=(11,7.5))
axs[0,0].plot(shear['time'],shear['amplitude'],label='D2Q9–BGK');axs[0,0].plot(shear['time'],shear['exact'],'--',label='exp(−νk²t)');axs[0,0].set(title='Shear decay | τ=0.8, ν=0.1',xlabel='Lattice time',ylabel='Shear amplitude');axs[0,0].legend()
for n,c in zip((8,16,32),channels):axs[0,1].plot(c['y']/n,c['velocity'],'.-',label=f'Ny={n}')
y=np.linspace(0,1,101);axs[0,1].plot(y,.04*y*(1-y),'--',color='black',label='Exact parabola');axs[0,1].set(title='Guo forcing + half-way bounce-back',xlabel='y / H',ylabel='Lattice velocity');axs[0,1].legend(fontsize=8)
for n,r in zip((32,64,128),hyp):axs[1,0].plot(r['x'],r['u'],label=f'N={n}')
axs[1,0].plot(hyp[-1]['x'],hyp[-1]['exact'],'--',color='black',label='Steady sin(2πx)');axs[1,0].set(title='Hyperbolic diffusion | first-order baseline',xlabel='x',ylabel='Steady solution');axs[1,0].legend(fontsize=8)
for n,r in zip((32,64,128),hyp):axs[1,1].semilogy(r['history'],label=f'N={n}')
axs[1,1].set(title='Pseudo-time convergence ≠ physical diffusion',xlabel='SSPRK2 iterations',ylabel='Weighted system residual');axs[1,1].legend(fontsize=8)
for ax in axs.flat:ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(OUT/'kinetic-hyperbolic.png',dpi=140);plt.close(fig)
manifest=dict(fem=dict(n=ns,l2=femerrors[:,0].tolist(),h1=femerrors[:,1].tolist(),orders=np.log2(femerrors[:-1]/femerrors[1:]).tolist()),
    krylov=histories,stiff=ode,adaptive=dict(times=adaptive.times.tolist(),states=adaptive.states[:,0].tolist(),accepted=adaptive.accepted,rejected=adaptive.rejected,max_error=float(max(abs(adaptive.states[:,0]-np.cos(adaptive.times))))),
    mac=dict(n=[16,32,64],velocity_rms=[r['error'] for r in mac],max_divergence=[float(max(r['history'][:,2])) for r in mac],viscosity=.1,final_time=.5),
    lbm=dict(tau=.8,viscosity=.1,ny=[8,16,32],channel_relative_l2=[c['error'] for c in channels],max_mach=[c['max_mach'] for c in channels],steps=[c['steps'] for c in channels],decay_times=12,peak_velocity=.01,
             shear_time=shear['time'].tolist(),shear_amplitude=shear['amplitude'].tolist(),shear_exact=shear['exact'].tolist(),
             channel_y_over_h=(channels[-1]['y']/32).tolist(),channel_velocity=channels[-1]['velocity'].tolist(),channel_exact=channels[-1]['exact'].tolist()),
    hyperbolic_diffusion=dict(n=[32,64,128],l2=[r['error'] for r in hyp],steps=[r['steps'] for r in hyp],dt=[r['dt'] for r in hyp],relaxation=hyp[0]['relaxation'],scope='Periodic first-order upwind FV / SSPRK2 baseline. Does not implement Nishikawa 2007 second-order RD.'),
    source_sha256=digest(['numart/fem.py','numart/krylov.py','numart/stiff.py','numart/incompressible.py','numart/lattice_boltzmann.py','numart/hyperbolic_diffusion.py','scripts/build_equation_gallery.py']),
    scope='Independent educational models, not original-paper reproductions or matched-cost performance comparisons. FEM P1 triangle Poisson; fixed right-preconditioned Krylov; ODE SDIRK2/BE/BDF2; periodic MAC; isothermal low-Mach D2Q9 BGK; pseudo-time diffusion baseline.')
(OUT/'solver-foundations.json').write_text(json.dumps(manifest,separators=(',',':'),allow_nan=False)+'\n')
print('Built',len(cases),'equation cases, 3 figures, and dedicated source manifests.')
print('FEM orders:',manifest['fem']['orders']);print('MAC errors:',manifest['mac']['velocity_rms']);print('LBM channel errors:',manifest['lbm']['channel_relative_l2'])
