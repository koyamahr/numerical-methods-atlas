"""Small implicit ODE integrators with explicit nonlinear failure reporting.

Fixed BDF2 uses a backward-Euler startup; adaptive SDIRK2 uses step doubling,
not an embedded pair. All states are real one-dimensional NumPy arrays.
"""
from dataclasses import dataclass
import numpy as np
from .krylov import newton

GAMMA = 1-1/np.sqrt(2)


def _stage(f, jac, t, base, coefficient, guess):
    identity = np.eye(len(base))
    result = newton(lambda y: y-base-coefficient*f(t, y),
                    lambda y: identity-coefficient*jac(t, y), guess,
                    tolerance=2e-12, maxiter=25)
    if not result.converged:
        raise RuntimeError('Implicit stage: '+result.reason)
    return result.x


def sdirk2_step(f, jac, t, y, h):
    y = np.asarray(y, dtype=float)
    a = _stage(f, jac, t+GAMMA*h, y, GAMMA*h, y)
    base = y+h*(1-GAMMA)*f(t+GAMMA*h, a)
    return _stage(f, jac, t+h, base, GAMMA*h, a)


def integrate(f, jac, y0, final_time=1., dt=.01, method='sdirk2', explicit=None):
    """Fixed BE, BDF2, SDIRK2, or first-order IMEX Euler.

    BDF2 retains a constant step by choosing ceil(T/dt) equal steps.
    In IMEX Euler, f/jac describe only the implicit part.
    """
    y = np.array(y0, dtype=float, copy=True)
    if (y.ndim != 1 or not np.all(np.isfinite(y)) or not np.isfinite(dt)
            or dt <= 0 or not np.isfinite(final_time) or final_time <= 0
            or method not in ('be', 'bdf2', 'sdirk2', 'imex-euler')):
        raise ValueError('Invalid ODE state, interval, step, or method')
    if method == 'imex-euler' and explicit is None:
        raise ValueError('IMEX Euler requires an explicit part')
    steps = int(np.ceil(final_time/dt)); h = final_time/steps
    times = np.linspace(0., final_time, steps+1); states = [y.copy()]
    for k, t in enumerate(times[:-1]):
        if method == 'sdirk2':
            new = sdirk2_step(f, jac, t, y, h)
        else:
            coefficient, base = h, y
            if method == 'bdf2' and k:
                coefficient, base = 2*h/3, (4*y-states[-2])/3
            if method == 'imex-euler':
                base = y+h*explicit(t, y)
            new = _stage(f, jac, t+h, base, coefficient, y)
        if not np.all(np.isfinite(new)):
            raise RuntimeError('Nonfinite ODE state')
        y = new; states.append(y.copy())
    return times, np.array(states)


@dataclass
class AdaptiveResult:
    times: np.ndarray
    states: np.ndarray
    accepted: int
    rejected: int


def adaptive_sdirk2(f, jac, y0, final_time=1., dt=.05, rtol=1e-5, atol=1e-8, maxsteps=100000):
    """Accept two half steps, estimate local error by (half-full)/3.

    Stage failures reject the trial. Failure to reach T raises, never returns
    a partial trajectory labeled complete. Tolerance controls local error.
    """
    y = np.array(y0, dtype=float, copy=True)
    if (y.ndim != 1 or not np.all(np.isfinite(y)) or not np.isfinite(final_time)
            or final_time <= 0 or not np.isfinite(dt) or dt <= 0
            or not np.isfinite(rtol) or rtol <= 0 or not np.isfinite(atol) or atol <= 0
            or maxsteps < 1):
        raise ValueError('Invalid adaptive integration controls')
    t, rejected = 0., 0; times, states = [t], [y.copy()]; h = min(dt, final_time)
    for _ in range(maxsteps):
        h = min(h, final_time-t)
        if h < 16*np.finfo(float).eps*max(1., abs(t)):
            raise RuntimeError('Adaptive step underflow')
        try:
            full = sdirk2_step(f, jac, t, y, h)
            half = sdirk2_step(f, jac, t, y, h/2)
            half = sdirk2_step(f, jac, t+h/2, half, h/2)
            scale = atol+rtol*np.maximum(abs(y), abs(half))
            error = np.sqrt(np.mean(((half-full)/(3*scale))**2))
        except (RuntimeError, np.linalg.LinAlgError):
            error = np.inf
        if np.isfinite(error) and error <= 1:
            t = min(t+h, final_time); y = half
            times.append(t); states.append(y.copy())
            if t == final_time:
                return AdaptiveResult(np.array(times), np.array(states), len(times)-1, rejected)
        else:
            rejected += 1
        factor = 5. if error == 0 else np.clip(.9*error**(-1/3), .2, 5.)
        h *= factor if np.isfinite(factor) else .2
    raise RuntimeError('Adaptive trial limit reached before final time')
