"""Finite-volume MUSCL and componentwise finite-difference WENO5-JS.

    WENO uses global Lax–Friedrichs flux splitting and SSPRK(3,3).
    MUSCL uses a selectable slope limiter on primitive variables.
    Neither method is a general positivity-preserving scheme.
"""
from dataclasses import dataclass
import numpy as np
from .riemann import numerical_flux
from .limiters import LIMITERS, limited_slope, minmod


@dataclass
class Result:
    x: np.ndarray
    q: np.ndarray
    time: float
    steps: int


def rk3(q, dt, rhs):
    a = q+dt*rhs(q)
    b = .75*q+.25*(a+dt*rhs(a))
    return q/3+2/3*(b+dt*rhs(b))


def _pad(q, problem, width):
    if problem.boundary == "periodic":
        return np.pad(q, ((width,width),(0,0)), mode="wrap")
    g = np.pad(q, ((width,width),(0,0)), mode="edge")
    if problem.boundary == "fixed":
        a,b = problem.domain
        g[:width] = problem.initial(np.array([a]))[0]
        g[-width:] = problem.initial(np.array([b]))[0]
    return g


def _weno_left(v):
    """Left-biased flux at interfaces; input includes three ghost points."""
    a,b,c,d,e = v[:-4],v[1:-3],v[2:-2],v[3:-1],v[4:]
    polynomials = np.stack(((2*a-7*b+11*c)/6, (-b+5*c+2*d)/6, (2*c+5*d-e)/6))
    beta = np.stack((13/12*(a-2*b+c)**2+.25*(a-4*b+3*c)**2,
                     13/12*(b-2*c+d)**2+.25*(b-d)**2,
                     13/12*(c-2*d+e)**2+.25*(3*c-4*d+e)**2))
    alpha = np.array([.1,.6,.3])[:,None,None]/(1.e-6+beta)**2
    return np.sum(alpha*polynomials, axis=0)/np.sum(alpha, axis=0)


def solve(problem, n=200, method="muscl", riemann="hllc", cfl=.3, final_time=None, limiter="minmod"):
    if method not in ("godunov", "muscl", "weno5"):
        raise ValueError("method must be godunov, muscl, or weno5")
    if limiter not in LIMITERS or (method != "muscl" and limiter != "minmod"):
        raise ValueError("A selectable limiter applies only to MUSCL; choose a supported limiter")
    if not 0 < cfl <= .5:
        raise ValueError("These baseline implementations require 0 < CFL <= 0.5")
    if method != "weno5" and riemann in ("hllc","roe","hlle") and problem.equation.name != "euler":
        raise ValueError("Select hll or rusanov for shallow water/isothermal")
    x = problem.grid(n)
    dx = (problem.domain[1]-problem.domain[0])/n
    q = problem.initial(x)
    eq = problem.equation
    end = problem.final_time if final_time is None else final_time
    if not np.isfinite(end) or end < 0:
        raise ValueError("final_time must be finite and nonnegative")
    def rhs(q):
        if method == "weno5":
            g = _pad(q, problem, 3)
            f = eq.flux(g)
            sm,sp = eq.speeds(g)
            a = np.max(np.maximum(abs(sm),abs(sp)))
            plus,minus = .5*(f+a*g), .5*(f-a*g)
            fp = _weno_left(plus)[:-1]
            fm = _weno_left(minus[::-1])[::-1][1:]
            flux = fp+fm
        else:
            g = _pad(q, problem, 2)
            w = eq.primitive(g)
            slope = np.zeros_like(w)
            if method == "muscl":
                slope[1:-1] = limited_slope(w[1:-1]-w[:-2], w[2:]-w[1:-1], limiter)
            left = eq.conserved((w+.5*slope)[1:-2])
            right = eq.conserved((w-.5*slope)[2:-1])
            flux = numerical_flux(left, right, eq, riemann)
        return -(flux[1:]-flux[:-1])/dx
    t,steps = 0.,0
    while t < end:
        sm,sp = eq.speeds(q)
        dt = min(cfl*dx/np.max(np.maximum(abs(sm),abs(sp))), end-t)
        q = rk3(q, dt, rhs)
        eq.primitive(q)
        t += dt
        steps += 1
    return Result(x,q,t,steps)
