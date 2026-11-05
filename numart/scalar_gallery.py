"""Godunov finite volumes and exact Riemann solutions for Burgers/LWR.

LWR density is nondimensional, jam density and free-flow speed both one.
Snapshots observe completed CFL steps without changing the trajectory.
"""
import numpy as np
from .snapshots import SnapshotRecorder


def flux(u, equation='burgers'):
    if equation == 'burgers':
        return .5*np.asarray(u)**2
    if equation == 'traffic':
        return np.asarray(u)*(1-np.asarray(u))
    raise ValueError('Unknown scalar equation')


def characteristic(u, equation='burgers'):
    flux(u, equation)  # validate the equation
    return np.asarray(u) if equation == 'burgers' else 1-2*np.asarray(u)


def riemann(xi, left, right, equation='burgers'):
    xi, left, right = np.broadcast_arrays(np.asarray(xi), left, right)
    flux(left, equation)
    convex = equation == 'burgers'
    shock = left > right if convex else left < right
    speed = .5*(left+right) if convex else 1-left-right
    shock_state = np.where(xi < speed, left, right)
    cl, cr = characteristic(left, equation), characteristic(right, equation)
    fan_state = np.where(xi <= cl, left, np.where(xi >= cr, right, xi if convex else (1-xi)/2))
    return np.where(shock, shock_state, fan_state)


def godunov(left, right, equation='burgers'):
    return flux(riemann(0., left, right, equation), equation)


def solve(initial, final_time=.4, equation='burgers', cfl=.4, order=2,
          boundary='outflow', snapshot_times=None):
    u = np.array(initial, dtype=float, copy=True)
    if (u.ndim != 1 or len(u) < 8 or not np.all(np.isfinite(u)) or final_time < 0
            or not np.isfinite(final_time) or not 0 < cfl <= .5 or order not in (1, 2)
            or boundary not in ('periodic', 'outflow')):
        raise ValueError('Invalid finite-volume controls')
    flux(u, equation)
    if equation == 'traffic' and (u.min() < 0 or u.max() > 1):
        raise ValueError('LWR density must lie in [0,1]')
    h = 1/len(u); t = 0.; steps = 0
    recorder = SnapshotRecorder(snapshot_times, final_time)
    recorder.capture(t, steps, u)

    def operator(state):
        padded = np.pad(state, 2, mode='wrap' if boundary == 'periodic' else 'edge')
        slopes = np.zeros_like(padded)
        if order == 2:
            dl, dr = padded[1:-1]-padded[:-2], padded[2:]-padded[1:-1]
            slopes[1:-1] = np.where(dl*dr > 0, np.sign(dl)*np.minimum(abs(dl), abs(dr)), 0.)
        faces = godunov(padded[1:-2]+slopes[1:-2]/2, padded[2:-1]-slopes[2:-1]/2, equation)
        return -(faces[1:]-faces[:-1])/h

    while t < final_time:
        speed = max(np.max(abs(characteristic(u, equation))), 1e-14)
        # LWR wave speeds never exceed one on the invariant interval.
        if equation == 'traffic': speed = 1.
        dt = min(final_time-t, cfl*h/speed)
        if order == 1:
            u = u+dt*operator(u)
        else:
            a = u+dt*operator(u)
            b = .75*u+.25*(a+dt*operator(a))
            u = u/3+2*(b+dt*operator(b))/3
        t += dt; steps += 1
        if not np.all(np.isfinite(u)):
            raise RuntimeError('Nonfinite scalar solution')
        if equation == 'traffic' and (u.min() < -1e-12 or u.max() > 1+1e-12):
            raise RuntimeError('LWR invariant interval lost')
        recorder.capture(t, steps, u)
    return dict(x=(np.arange(len(u))+.5)*h, u=u, time=t, steps=steps, snapshots=recorder.frames)


def riemann_cell_averages(n, time, left, right, equation='burgers', origin=.5):
    """Exact cell integrals of a piecewise constant/linear Riemann solution."""
    edges = np.linspace(0., 1., n+1)
    if time == 0:
        fraction = np.clip((origin-edges[:-1])*n, 0., 1.)
        return fraction*left+(1-fraction)*right
    convex = equation == 'burgers'
    shock = left > right if convex else left < right
    if shock or left == right:
        speed = .5*(left+right) if convex else 1-left-right
        fraction = np.clip((origin+speed*time-edges[:-1])*n, 0., 1.)
        return fraction*left+(1-fraction)*right
    a, b = origin+characteristic(left, equation)*time, origin+characteristic(right, equation)*time
    lo, hi = edges[:-1], edges[1:]
    integral = left*np.maximum(0., np.minimum(hi, a)-lo)+right*np.maximum(0., hi-np.maximum(lo, b))
    q, r = np.maximum(lo, a), np.minimum(hi, b)
    active = r > q
    if convex:
        area = ((r-origin)**2-(q-origin)**2)/(2*time)
    else:
        area = (r-q)/2-((r-origin)**2-(q-origin)**2)/(4*time)
    integral += np.where(active, area, 0.)
    return integral*n
