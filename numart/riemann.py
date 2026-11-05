"""Rusanov, HLL, HLLC and exact ideal-gas Euler sampling.

References: Harten et al. (1983), Toro et al. (1994), Toro (2009).
HLL/HLLC use Davis min/max acoustic wave-speed estimates.
"""
import numpy as np
from .equations import Euler


def numerical_flux(left, right, equation, solver="hll"):
    if solver not in ("rusanov", "hll", "hlle", "hllc", "roe"):
        raise ValueError(f"Unknown Riemann solver: {solver}")
    fl, fr = equation.flux(left), equation.flux(right)
    lm, lp = equation.speeds(left)
    rm, rp = equation.speeds(right)
    if solver == "roe":
        return roe_flux(left,right,equation)
    if solver == "rusanov":
        a = np.maximum.reduce((abs(lm), abs(lp), abs(rm), abs(rp)))
        return 0.5*(fl+fr-a[..., None]*(right-left))
    sl, sr = np.minimum(lm, rm), np.maximum(lp, rp)
    if solver == "hlle":
        if not isinstance(equation,Euler):
            raise ValueError("Einfeldt wave speeds are implemented for Euler only; use hll")
        rl,ul,pl = np.moveaxis(equation.primitive(left),-1,0)
        rr,ur,pr = np.moveaxis(equation.primitive(right),-1,0)
        wl,wr = np.sqrt(rl),np.sqrt(rr)
        u = (wl*ul+wr*ur)/(wl+wr)
        h = (wl*(left[...,2]+pl)/rl+wr*(right[...,2]+pr)/rr)/(wl+wr)
        a = np.sqrt((equation.gamma-1)*(h-.5*u*u))
        sl,sr = np.minimum(lm,u-a),np.maximum(rp,u+a)
    hll = (sr[..., None]*fl-sl[..., None]*fr
           +(sl*sr)[..., None]*(right-left))/(sr-sl)[..., None]
    if solver in ("hll","hlle"):
        return np.where((sl >= 0)[..., None], fl, np.where((sr <= 0)[..., None], fr, hll))
    if not isinstance(equation, Euler):
        raise ValueError("HLLC is implemented for ideal-gas Euler only")
    rl, vl, pl = np.moveaxis(equation.primitive(left), -1, 0)
    rr, vr, pr = np.moveaxis(equation.primitive(right), -1, 0)
    sm = (pr-pl+rl*vl*(sl-vl)-rr*vr*(sr-vr))/(rl*(sl-vl)-rr*(sr-vr))

    def star(q, r, v, p, s):
        rs = r*(s-v)/(s-sm)
        es = rs*(q[..., 2]/r+(sm-v)*(sm+p/(r*(s-v))))
        return np.stack((rs, rs*sm, es), axis=-1)

    fsl = fl+sl[..., None]*(star(left, rl, vl, pl, sl)-left)
    fsr = fr+sr[..., None]*(star(right, rr, vr, pr, sr)-right)
    return np.where((sl >= 0)[..., None], fl,
                    np.where((sm >= 0)[..., None], fsl,
                             np.where((sr > 0)[..., None], fsr, fr)))


def roe_flux(left, right, equation, entropy_fraction=.1):
    """Roe (1981); quadratic entropy smoothing of acoustic eigenvalues only.

    No positivity guarantee; this is not an all-speed or rotated solver.
    entropy_fraction=0 disables the acoustic entropy fix.
    """
    if not isinstance(equation,Euler):
        raise ValueError("Roe is implemented for ideal-gas Euler only")
    rl,ul,pl = np.moveaxis(equation.primitive(left),-1,0)
    rr,ur,pr = np.moveaxis(equation.primitive(right),-1,0)
    sl,sr = np.sqrt(rl),np.sqrt(rr)
    u = (sl*ul+sr*ur)/(sl+sr)
    h = (sl*(left[...,2]+pl)/rl+sr*(right[...,2]+pr)/rr)/(sl+sr)
    a2 = (equation.gamma-1)*(h-.5*u*u)
    a = np.sqrt(a2)
    dq = right-left
    dp = (equation.gamma-1)*(dq[...,2]-u*dq[...,1]+.5*u*u*dq[...,0])
    rdu = dq[...,1]-u*dq[...,0]
    alpha = np.stack(((dp-a*rdu)/(2*a2),dq[...,0]-dp/a2,(dp+a*rdu)/(2*a2)),axis=-1)
    speeds = np.stack((abs(u-a),abs(u),abs(u+a)),axis=-1)
    delta = entropy_fraction*a
    if entropy_fraction > 0:
        for k in (0,2):
            speeds[...,k] = np.where(speeds[...,k]<delta,.5*(speeds[...,k]**2/delta+delta),speeds[...,k])
    one = np.ones_like(u)
    vectors = np.stack((np.stack((one,u-a,h-u*a),axis=-1),
                        np.stack((one,u,.5*u*u),axis=-1),
                        np.stack((one,u+a,h+u*a),axis=-1)),axis=-2)
    dissipation = np.einsum("...k,...kv->...v",alpha*speeds,vectors)
    return .5*(equation.flux(left)+equation.flux(right)-dissipation)


def exact_euler(xi, left=(1., 0., 1.), right=(.125, 0., .1), gamma=1.4):
    """Primitive state at similarity coordinate xi=(x-x0)/t. No vacuum support.

    Pressure matching is solved by bracketed bisection (not an analytic root).
    This reference is independent of numerical_flux.
    """
    rl, ul, pl = left
    rr, ur, pr = right
    if min(rl, rr, pl, pr) <= 0 or gamma <= 1:
        raise ValueError("Positive density/pressure and gamma>1 required")
    cl, cr = np.sqrt(gamma*pl/rl), np.sqrt(gamma*pr/rr)
    if ur-ul >= 2*(cl+cr)/(gamma-1):
        raise ValueError("Vacuum Riemann problems are not supported")

    def wave(p, r, pk, ck):
        if p > pk:
            return (p-pk)*np.sqrt(2/((gamma+1)*r)/(p+(gamma-1)/(gamma+1)*pk))
        return 2*ck/(gamma-1)*((p/pk)**((gamma-1)/(2*gamma))-1)

    def residual(p):
        return wave(p, rl, pl, cl)+wave(p, rr, pr, cr)+ur-ul

    lo, hi = 0., max(pl, pr)
    while residual(hi) < 0:
        hi *= 2
    for _ in range(100):
        mid = (lo+hi)/2
        if residual(mid) > 0:
            hi = mid
        else:
            lo = mid
    ps = (lo+hi)/2
    us = 0.5*(ul+ur+wave(ps, rr, pr, cr)-wave(ps, rl, pl, cl))
    xi = np.asarray(xi)
    out = np.empty(xi.shape+(3,))
    beta = (gamma-1)/(gamma+1)
    for isleft, (r, u, p, c) in enumerate(((rr, ur, pr, cr), (rl, ul, pl, cl))):
        sign = -1 if isleft else 1
        side = xi <= us if isleft else xi > us
        if ps > p:
            speed = u+sign*c*np.sqrt((gamma+1)/(2*gamma)*ps/p+(gamma-1)/(2*gamma))
            rs = r*(ps/p+beta)/(beta*ps/p+1)
            outside = xi < speed if isleft else xi > speed
            values = np.where(outside[..., None], np.array((r, u, p)), np.array((rs, us, ps)))
        else:
            cs = c*(ps/p)**((gamma-1)/(2*gamma))
            head, tail = u+sign*c, us+sign*cs
            outside = xi < head if isleft else xi > head
            inside = xi > tail if isleft else xi < tail
            vf = 2/(gamma+1)*(-sign*c+(gamma-1)*u/2+xi)
            cf = 2/(gamma+1)*(c+sign*(gamma-1)*(xi-u)/2)
            ratio = np.maximum(cf/c, 0)
            fan = np.stack((r*ratio**(2/(gamma-1)), vf, p*ratio**(2*gamma/(gamma-1))), axis=-1)
            values = np.where(outside[..., None], np.array((r, u, p)),
                              np.where(inside[..., None], np.array((r*(ps/p)**(1/gamma), us, ps)), fan))
        out[side] = values[side]
    return out
