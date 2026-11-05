"""D2Q9 isothermal lattice BGK with Guo force and half-way bounce-back.

Lattice units dx=dt=rho_ref=1, cs^2=1/3. Periodic x; periodic or stationary
no-slip y walls. Low-Mach educational model, not a compressible gas solver.
"""
import numpy as np

C = np.array([[0,0], [1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]])
W = np.array([4/9]+[1/9]*4+[1/36]*4)
OPPOSITE = np.array([0,3,4,1,2,7,8,5,6])
CS2 = 1/3


def equilibrium(rho, velocity):
    rho = np.asarray(rho); velocity = np.asarray(velocity)
    cu = np.einsum('qd,dxy->qxy', C, velocity)
    speed2 = np.sum(velocity**2, axis=0)
    return W[:, None, None]*rho*(1+3*cu+4.5*cu**2-1.5*speed2)


def moments(f, force=(0., 0.)):
    force = np.asarray(force, dtype=float)
    rho = f.sum(axis=0)
    if not np.all(np.isfinite(f)) or np.any(rho <= 0):
        raise RuntimeError('LBM nonfinite populations or nonpositive density')
    velocity = (np.einsum('qd,qxy->dxy', C, f)+force[:, None, None]/2)/rho
    return rho, velocity


def step(f, tau=.8, force=(0., 0.), walls=False):
    if not np.isfinite(tau) or tau <= .5:
        raise ValueError('Positive viscosity requires finite tau>1/2')
    force = np.asarray(force, dtype=float)
    if force.shape != (2,) or not np.all(np.isfinite(force)):
        raise ValueError('Force density must be a finite two-vector')
    rho, velocity = moments(f, force)
    cu = np.einsum('qd,dxy->qxy', C, velocity)
    # Guo F_q = w_q (1-1/(2tau)) [3(c_q-u)+9(c_q.u)c_q].F
    cf = np.einsum('qd,d->q', C, force)[:, None, None]
    uf = np.einsum('dxy,d->xy', velocity, force)
    source = W[:, None, None]*(1-.5/tau)*(3*(cf-uf)+9*cu*cf)
    post = f-(f-equilibrium(rho, velocity))/tau+source
    streamed = np.empty_like(post)
    for q, (cx, cy) in enumerate(C):
        streamed[q] = np.roll(post[q], (int(cx), int(cy)), axis=(0, 1))
        if walls and cy:
            j = 0 if cy == 1 else -1
            streamed[q, :, j] = post[OPPOSITE[q], :, j]
    return streamed


def shear_wave(n=32, steps=200, tau=.8, amplitude=.01):
    if n < 4 or steps < 0 or amplitude <= 0:
        raise ValueError('Invalid shear wave controls')
    y = np.arange(n)
    velocity = np.zeros((2, 4, n)); velocity[0] = amplitude*np.sin(2*np.pi*y/n)
    f = equilibrium(np.ones((4, n)), velocity)
    times, measured = [0], [amplitude]
    mode = np.sin(2*np.pi*y/n)
    for k in range(steps):
        f = step(f, tau)
        _, u = moments(f)
        times.append(k+1); measured.append(2*np.mean(u[0]*mode))
    nu = CS2*(tau-.5)
    return dict(time=np.array(times), amplitude=np.array(measured),
                exact=amplitude*np.exp(-nu*(2*np.pi/n)**2*np.array(times)),
                f=f, viscosity=nu)


def poiseuille(ny=16, tau=.8, peak_velocity=.01, decay_times=12.):
    if ny < 4 or peak_velocity <= 0 or decay_times <= 0 or tau <= .5:
        raise ValueError('Invalid channel controls')
    nu = CS2*(tau-.5); force = (8*nu*peak_velocity/ny**2, 0.)
    f = equilibrium(np.ones((4, ny)), np.zeros((2, 4, ny)))
    steps = int(np.ceil(decay_times*ny**2/(np.pi**2*nu)))
    for _ in range(steps):
        f = step(f, tau, force, walls=True)
    rho, u = moments(f, force)
    y = np.arange(ny)+.5
    exact = force[0]*y*(ny-y)/(2*nu)
    profile = u[0].mean(axis=0)
    return dict(y=y, velocity=profile, exact=exact, rho=rho, steps=steps,
                viscosity=nu, tau=tau, force=force,
                error=float(np.linalg.norm(profile-exact)/np.linalg.norm(exact)),
                max_mach=float(np.max(abs(u))/np.sqrt(CS2)))
