"""1D direct-Eulerian PPM: primitive parabolas, contact/shock switches, tracing.

Single conservative update from time-averaged characteristic domains, not an
extra predictor inside SSPRK3. No Lagrangian/remap, multidimensional CTU,
artificial viscosity or bitwise replication of a particular production code.
"""
from dataclasses import dataclass
import numpy as np
from .limiters import limited_slope, positive_reconstruction
from .reconstruction import _pad, averaged_state
from .riemann import numerical_flux
from .ausm_plus import flux as ausm_plus_flux
from .ausm import flux as ausm_flux


def monotone_edges(center, left, right):
    extremum = (right-center)*(center-left) <= 0
    left, right = np.where(extremum, center, left), np.where(extremum, center, right)
    delta = right-left; six = 6*center-3*(left+right)
    return np.where(delta*six > delta**2, 3*center-2*right, left), np.where(delta*six < -delta**2, 3*center-2*left, right)


def profiles(q, problem, steepening=True, flattening=True):
    """Primitive profiles for real cells and one ghost on either side."""
    g = problem.equation.primitive(_pad(q, problem, 4))
    n = len(q)+2
    a, b, c, d, e, f, h = [g[k:k+n] for k in range(7)]
    slope_l = limited_slope(c-b, d-c, 'mc')
    slope = limited_slope(d-c, e-d, 'mc')
    slope_r = limited_slope(e-d, f-e, 'mc')
    left = .5*(c+d)-(slope-slope_l)/6
    right = .5*(d+e)-(slope_r-slope)/6
    left = np.clip(left, np.minimum(c,d), np.maximum(c,d))
    right = np.clip(right, np.minimum(d,e), np.maximum(d,e))
    eta = np.zeros(n)
    if steepening:
        jump = e[:,0]-c[:,0]
        second_l = (d[:,0]-2*c[:,0]+b[:,0])/6
        second_r = (f[:,0]-2*e[:,0]+d[:,0])/6
        indicator = np.divide(-(second_r-second_l), jump, out=np.zeros(n), where=jump != 0)
        contact = (abs(jump) > .01*np.minimum(c[:,0],e[:,0])) & (second_l*second_r < 0)
        contact &= abs(e[:,2]-c[:,2])/np.minimum(e[:,2],c[:,2]) < .1*problem.equation.gamma*abs(jump)/np.minimum(c[:,0],e[:,0])
        eta = np.where(contact, np.clip(20*(indicator-.05), 0, 1), 0)
        left[:,0] = (1-eta)*left[:,0]+eta*(c[:,0]+.5*slope_l[:,0])
        right[:,0] = (1-eta)*right[:,0]+eta*(e[:,0]-.5*slope_r[:,0])
    def shock(l2, l1, center, r1, r2):
        dp = r1[:,2]-l1[:,2]; wide = r2[:,2]-l2[:,2]
        ratio = np.divide(dp, wide, out=np.zeros(n), where=wide != 0)
        strong = (abs(dp)/np.minimum(l1[:,2],r1[:,2]) >= 1/3) & (r1[:,1] < l1[:,1])
        return np.where(strong, np.clip(10*(ratio-.75), 0, 1), 0)
    flat = np.zeros(n)
    if flattening:
        flat = np.maximum(shock(b,c,d,e,f), np.where(e[:,2] < c[:,2], shock(c,d,e,f,h), shock(a,b,c,d,e)))
        left = d+(1-flat[:,None])*(left-d)
        right = d+(1-flat[:,None])*(right-d)
    left, right = monotone_edges(d, left, right)
    return d, left, right, eta, flat


def trace(center, left, right, dt_dx, gamma=1.4):
    """Integrate parabolas over each wave's domain, using a frozen primitive basis."""
    rho, u, p = center.T; c = np.sqrt(gamma*p/rho)
    speeds = np.stack((u-c,u,u+c), axis=-1)
    delta, six = right-left, 6*center-3*(left+right)
    def integral(sigma, side):
        sigma = sigma[...,None]
        return (right[:,None,:]-.5*sigma*(delta[:,None,:]-(1-2*sigma/3)*six[:,None,:]) if side == 1 else
                left[:,None,:]+.5*sigma*(delta[:,None,:]+(1-2*sigma/3)*six[:,None,:]))
    traced = []
    for side in (-1,1):
        sigma = dt_dx*np.maximum(side*speeds,0)
        if np.any(sigma > 1+1e-12): raise ValueError('Characteristic domain exceeds a cell')
        values = integral(sigma,side)
        reference = integral(sigma.max(axis=-1)[:,None],side)[:,0,:]
        difference = values-reference[:,None,:]
        dr, du, dp = np.moveaxis(difference,-1,0)
        minus = .5*(dp/c[:,None]**2-rho[:,None]*du/c[:,None])
        plus = .5*(dp/c[:,None]**2+rho[:,None]*du/c[:,None])
        amplitudes = np.stack((minus[:,0],dr[:,1]-dp[:,1]/c**2,plus[:,2]),axis=-1)
        amplitudes *= side*speeds > 0
        am, a0, ap = amplitudes.T
        correction = np.stack((am+a0+ap,c/rho*(ap-am),c*c*(am+ap)),axis=-1)
        traced.append(reference+correction)
    return traced[0], traced[1]


@dataclass
class TracedResult:
    x: np.ndarray
    q: np.ndarray
    time: float
    steps: int
    rejected_steps: int
    scaled_reconstructions: int
    steepened_cells: int
    flattened_cells: int


class IntegrationFailure(ValueError):
    """Last accepted state and actual time, never relabeled as a final solution."""
    def __init__(self,message,result):
        super().__init__(message)
        self.result = result


def solve(problem, n=200, cfl=.4, final_time=None, steepening=True, flattening=True, riemann='hllc', mach_cutoff=.1):
    if problem.equation.name != 'euler' or not isinstance(n,int) or n < 8 or not np.isfinite(cfl) or not 0 < cfl <= .8:
        raise ValueError('Require 1D Euler, n>=8 and 0<CFL<=.8')
    end = problem.final_time if final_time is None else final_time
    if not np.isfinite(end) or end < 0: raise ValueError('Invalid final time')
    if riemann not in ('hllc','hlle','roe','ausm','ausm-plus','ausm-up'): raise ValueError('Unknown numerical flux')
    eq = problem.equation; x = problem.grid(n); dx = (problem.domain[1]-problem.domain[0])/n
    q = averaged_state(problem,x,dx); t = 0.; steps = rejected = scaled = steepened = flattened = 0
    while t < end:
        sm, sp = eq.speeds(q); dt = min(cfl*dx/np.max(np.maximum(abs(sm),abs(sp))),end-t)
        center, left, right, eta, flat = profiles(q,problem,steepening,flattening)
        for attempt in range(14):
            try:
                a,b = trace(center,left,right,dt/dx,eq.gamma)
                # Only reconstructed input states are scaled, never the conserved means.
                states = np.stack((eq.conserved(a),eq.conserved(b)),axis=1)
                base = _pad(q,problem,1)
                density = states[...,0]; pressure = (eq.gamma-1)*(states[...,2]-.5*states[...,1]**2/np.maximum(density,1e-300))
                bad = np.any((density <= 1e-12)|(pressure <= 1e-12),axis=1)
                for i in np.flatnonzero(bad):
                    states[i], _ = positive_reconstruction(base[i],states[i],gamma=eq.gamma)
                if riemann.startswith('ausm-'):
                    flux = ausm_plus_flux(states[:-1,1],states[1:,0],eq.gamma,variant='up' if riemann=='ausm-up' else 'plus',mach_cutoff=mach_cutoff)
                elif riemann == 'ausm': flux = ausm_flux(states[:-1,1],states[1:,0],eq.gamma)
                else: flux = numerical_flux(states[:-1,1],states[1:,0],eq,riemann)
                trial = q-dt/dx*(flux[1:]-flux[:-1]); eq.primitive(trial)
                break
            except ValueError as error:
                if attempt == 13:
                    partial = TracedResult(x,q.copy(),t,steps,rejected+1,scaled,steepened,flattened)
                    raise IntegrationFailure('Admissibility retries exhausted: '+str(error),partial) from error
                rejected += 1; dt *= .5
        if t+dt == t:
            raise IntegrationFailure('Time step cannot advance float64 time',TracedResult(x,q.copy(),t,steps,rejected,scaled,steepened,flattened))
        q = trial; t += dt; steps += 1; scaled += int(bad.sum())
        steepened += int(np.count_nonzero(eta[1:-1])); flattened += int(np.count_nonzero(flat[1:-1]))
    return TracedResult(x,q,t,steps,rejected,scaled,steepened,flattened)
