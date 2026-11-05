"""Uniform-grid slopes, TVB modified minmod, and Euler state scaling.

State scaling is a reconstruction building block, not a fully discrete
positivity theorem for the existing MUSCL or WENO solvers.
"""
import numpy as np

LIMITERS = ("minmod", "superbee", "mc", "van-leer", "van-albada")


def minmod(a, b):
    a, b = np.broadcast_arrays(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    same = ((a > 0) & (b > 0)) | ((a < 0) & (b < 0))
    return np.where(same, np.sign(a)*np.minimum(abs(a), abs(b)), 0.)


def limited_slope(a, b, limiter="minmod"):
    """Limit backward/forward *increments*, without forming a ratio at plateaus.

    van Albada uses the symmetric (r^2+r)/(1+r^2) form, clipped to zero
    for r<=0, with no epsilon regularization. All inputs must be finite.
    """
    if limiter not in LIMITERS:
        raise ValueError(f"Unknown limiter {limiter!r}; choose from {LIMITERS}")
    a, b = np.broadcast_arrays(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("Slope increments must be finite")
    if limiter == "minmod":
        return minmod(a, b)
    scale = np.maximum(abs(a), abs(b))
    aa = np.divide(abs(a), scale, out=np.zeros_like(scale), where=scale > 0)
    bb = np.divide(abs(b), scale, out=np.zeros_like(scale), where=scale > 0)
    if limiter == "superbee":
        value = np.maximum(np.minimum(2*aa, bb), np.minimum(aa, 2*bb))
    elif limiter == "mc":
        value = np.minimum(np.minimum(2*aa, 2*bb), .5*(aa+bb))
    elif limiter == "van-leer":
        value = np.divide(2*aa*bb, aa+bb, out=np.zeros_like(scale), where=aa+bb > 0)
    else:
        denominator = aa*aa+bb*bb
        value = np.divide(aa*bb*(aa+bb), denominator, out=np.zeros_like(scale), where=denominator > 0)
    same = ((a > 0) & (b > 0)) | ((a < 0) & (b < 0))
    return np.where(same, np.sign(a)*value*scale, 0.)


def limiter_function(r, limiter="minmod"):
    """Sweby convention phi(r), r=backward/forward increment."""
    r = np.asarray(r, dtype=float)
    return limited_slope(r, np.ones_like(r), limiter)


def tvb_minmod(value, backward, forward, dx, M=0.):
    """Modified minmod: bypass limiting when |value| <= M dx^2.

    Here value is an increment, not a derivative. M is dimensional and
    problem-dependent. This operation need not be TVD.
    """
    if not np.isfinite(dx) or dx <= 0 or not np.isfinite(M) or M < 0:
        raise ValueError("Require finite dx>0 and M>=0")
    v, a, b = np.broadcast_arrays(value, backward, forward)
    if not all(np.all(np.isfinite(x)) for x in (v, a, b)):
        raise ValueError("TVB inputs must be finite")
    return np.where(abs(v) <= M*dx*dx, v, minmod(v, minmod(a, b)))


def euler_pressure(states, gamma=1.4):
    """Conservative states (..., rho, momentum..., total energy)."""
    u = np.asarray(states, dtype=float)
    return (gamma-1)*(u[..., -1]-.5*np.sum(u[..., 1:-1]**2, axis=-1)/u[..., 0])


def positive_reconstruction(mean, states, gamma=1.4, density_floor=1.e-12, pressure_floor=1.e-12):
    """One common affine scaling Ubar + theta*(U-Ubar), theta in [0,1].

    Preserves any quadrature mean already equal to Ubar. Requires an
    admissible mean; cannot repair an inadmissible cell average. Density is
    bounded analytically; pressure uses ideal-gas concavity and bisection.
    Returns (scaled_states, theta). No state clipping or floor injection.
    """
    mean, states = np.asarray(mean, dtype=float), np.asarray(states, dtype=float)
    if mean.ndim != 1 or mean.size < 3 or states.ndim < 2 or states.shape[-1] != mean.size or states.size == 0:
        raise ValueError("Require one mean and a nonempty array of compatible Euler states")
    if not np.isfinite(gamma) or gamma <= 1 or not all(np.isfinite(x) and x > 0 for x in (density_floor, pressure_floor)):
        raise ValueError("Require gamma>1 and finite positive floors")
    if not np.all(np.isfinite(mean)) or not np.all(np.isfinite(states)):
        raise ValueError("Euler states must be finite")
    if mean[0] < density_floor or euler_pressure(mean, gamma) < pressure_floor:
        raise ValueError("Cell mean is inadmissible; reconstruction scaling cannot repair it")
    rho_min = float(states[..., 0].min())
    theta = min(1., (mean[0]-density_floor)/(mean[0]-rho_min)) if rho_min < density_floor else 1.
    # Stay on the admissible side of floating-point boundary evaluations.
    if theta < 1:
        theta *= 1-8*np.finfo(float).eps
    delta = states-mean
    if np.all(euler_pressure(mean+theta*delta, gamma) >= pressure_floor):
        return mean+theta*delta, float(theta)
    lo, hi = 0., theta
    for _ in range(64):
        mid = .5*(lo+hi)
        if np.all(euler_pressure(mean+mid*delta, gamma) >= pressure_floor):
            lo = mid
        else:
            hi = mid
    theta = lo*(1-8*np.finfo(float).eps)
    return mean+theta*delta, float(theta)
