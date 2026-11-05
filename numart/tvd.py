"""Periodic scalar MUSCL advection with exact cell-average references."""
from dataclasses import dataclass
import numpy as np
from .limiters import LIMITERS, limited_slope, tvb_minmod
from .solvers import rk3

ADVECTION_METHODS = (*LIMITERS, "upwind", "unlimited", "tvb")


def cell_average(x, dx, profile="square", time=0., speed=1.):
    if profile == "sine":
        return np.sinc(dx)*np.sin(2*np.pi*(x-speed*time))
    if profile != "square":
        raise ValueError("profile must be square or sine")
    left, right = x-.5*dx, x+.5*dx
    shift = (speed*time) % 1.
    return sum(np.maximum(0., np.minimum(right, .4+shift+k)-np.maximum(left, .2+shift+k))
               for k in (-1, 0, 1))/dx


def total_variation(q):
    return float(np.sum(abs(np.roll(q, -1)-q)))


def advection_rhs(q, dx, speed=1., limiter="minmod", tvb_M=0.):
    backward, forward = q-np.roll(q, 1), np.roll(q, -1)-q
    if limiter == "upwind":
        slope = np.zeros_like(q)
    elif limiter == "unlimited":
        slope = .5*(backward+forward)
    elif limiter == "tvb":
        slope = tvb_minmod(.5*(backward+forward), backward, forward, dx, tvb_M)
    else:
        slope = limited_slope(backward, forward, limiter)
    flux = speed*(q+.5*slope) if speed >= 0 else speed*np.roll(q-.5*slope, -1)
    return -(flux-np.roll(flux, 1))/dx


@dataclass
class AdvectionResult:
    x: np.ndarray
    q: np.ndarray
    time: float
    steps: int
    history: list


def solve_advection(n=200, profile="square", limiter="minmod", speed=1., final_time=1., cfl=.3, tvb_M=0.):
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 8:
        raise ValueError("n must be an integer >=8")
    if limiter not in ADVECTION_METHODS or not np.isfinite(speed) or not np.isfinite(final_time) or final_time < 0:
        raise ValueError("Invalid advection method, speed, or time")
    if not np.isfinite(cfl) or not 0 < cfl <= .5 or not np.isfinite(tvb_M) or tvb_M < 0:
        raise ValueError("Require 0<CFL<=0.5 and finite M>=0")
    dx = 1./n
    x = (np.arange(n)+.5)*dx
    q = cell_average(x, dx, profile)
    def diagnostics(t):
        return {"time":float(t), "mass":float(dx*q.sum()), "tv":total_variation(q),
                "minimum":float(q.min()), "maximum":float(q.max())}
    history = [diagnostics(0.)]
    time, steps = 0., 0
    while time < final_time and speed != 0:
        dt = min(cfl*dx/abs(speed), final_time-time)
        q = rk3(q, dt, lambda v: advection_rhs(v, dx, speed, limiter, tvb_M))
        time += dt
        steps += 1
        history.append(diagnostics(time))
    return AdvectionResult(x, q, final_time, steps, history)
