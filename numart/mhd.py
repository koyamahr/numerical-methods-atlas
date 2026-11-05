"""Educational 2D planar ideal MHD (vz=Bz=0), periodic square, mu0=1.

CT: staggered face B, shared corner EMF, arithmetic flux averaging (flux-CT).
GLM: cell B and psi, Dedner hyperbolic/parabolic cleaning, fixed ch per run.
Both use first-order Rusanov fluxes and forward Euler. Not Athena's upwind CT.
References: Orszag & Tang (1979), Evans & Hawley (1988), Toth (2000),
Dedner et al. (2002); see docs/mhd.md for normalization and limitations.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class MHDResult:
    q: np.ndarray  # rho,mx,my,E,Bx,By,psi; arrays indexed [x,y,variable]
    time: float
    steps: int
    divergence: np.ndarray
    history: np.ndarray  # time, max(abs(divB)), mean(rho), mean(E)
    bx_face: object = None
    by_face: object = None


def primitive(q, gamma=5/3):
    r = q[...,0]
    if np.any(r <= 0) or not np.all(np.isfinite(q)):
        raise ValueError("MHD nonpositive density or nonfinite state")
    vx,vy = q[...,1]/r,q[...,2]/r
    bx,by = q[...,4],q[...,5]
    p = (gamma-1)*(q[...,3]-.5*r*(vx*vx+vy*vy)-.5*(bx*bx+by*by))
    if np.any(p <= 0):
        raise ValueError("MHD nonpositive pressure; reduce CFL or refine grid")
    return r,vx,vy,p,bx,by


def initial_orszag_tang(n):
    """Unit box: rho=25/(36pi), p=5/(12pi), B0=1/sqrt(4pi), gamma=5/3."""
    z = (np.arange(n)+.5)/n
    x,y = np.meshgrid(z,z,indexing="ij")
    bx = -np.sin(2*np.pi*y)/np.sqrt(4*np.pi)
    by = np.sin(4*np.pi*x)/np.sqrt(4*np.pi)
    vx,vy = -np.sin(2*np.pi*y),np.sin(2*np.pi*x)
    r,p = 25/(36*np.pi),5/(12*np.pi)
    q = np.zeros((n,n,7))
    q[...,0] = r
    q[...,1],q[...,2] = r*vx,r*vy
    q[...,3] = p/(5/3-1)+.5*r*(vx*vx+vy*vy)+.5*(bx*bx+by*by)
    q[...,4],q[...,5] = bx,by
    # Face index i means the right face of cell i (periodic unique faces).
    return q,bx.copy(),by.copy()


def _flux(q, axis, ch):
    r,vx,vy,p,bx,by = primitive(q)
    v,b = (vx,bx) if axis == 0 else (vy,by)
    b2 = bx*bx+by*by
    totalp = p+.5*b2
    f = np.zeros_like(q)
    f[...,0] = r*v
    f[...,1] = q[...,1]*v-bx*b
    f[...,2] = q[...,2]*v-by*b
    f[...,axis+1] += totalp
    f[...,3] = (q[...,3]+totalp)*v-b*(vx*bx+vy*by)
    f[...,4] = v*bx-vx*b
    f[...,5] = v*by-vy*b
    f[...,4+axis] = q[...,6] if ch else 0.
    f[...,6] = ch*ch*b
    a2 = (5/3)*p/r
    va2 = b2/r
    cf = np.sqrt(.5*(a2+va2+np.sqrt(np.maximum((a2+va2)**2-4*a2*b*b/r,0))))
    return f,np.maximum(abs(v)+cf,ch)


def _interfaces(q, axis, ch, normal=None):
    left,right = q.copy(),np.roll(q,-1,axis=axis).copy()
    if normal is not None:
        # Preserve gas pressure while imposing the single staggered normal B.
        for state in (left,right):
            state[...,3] += .5*(normal**2-state[...,4+axis]**2)
            state[...,4+axis] = normal
    fl,al = _flux(left,axis,ch)
    fr,ar = _flux(right,axis,ch)
    speed = np.maximum(al,ar)
    return .5*(fl+fr-speed[...,None]*(right-left)),float(speed.max())


def discrete_divergence(q, bx_face=None, by_face=None):
    n = q.shape[0]
    if bx_face is not None:
        return n*(bx_face-np.roll(bx_face,1,axis=0)+by_face-np.roll(by_face,1,axis=1))
    return .5*n*(np.roll(q[...,4],-1,axis=0)-np.roll(q[...,4],1,axis=0)
                 +np.roll(q[...,5],-1,axis=1)-np.roll(q[...,5],1,axis=1))


def solve_orszag_tang(n=64, final_time=.5, method="ct", cfl=.3, damping=.18, magnetic_error=0.):
    if (n < 8 or not 0 < cfl <= .4 or final_time < 0 or method not in ("ct","glm") or damping < 0
            or not np.all(np.isfinite([final_time,cfl,damping,magnetic_error]))):
        raise ValueError("Require n>=8, 0<CFL<=.4, t>=0, damping>=0, method ct/glm")
    q,bxf,byf = initial_orszag_tang(n)
    if magnetic_error:
        if method != "glm":
            raise ValueError("Longitudinal error injection is a GLM diagnostic only")
        x = (np.arange(n)+.5)/n
        bx = q[...,4]+magnetic_error*np.sin(2*np.pi*x)[:,None]
        q[...,3] += .5*(bx*bx-q[...,4]**2)  # preserve initial gas pressure
        q[...,4] = bx
    # Constant ch avoids changing the GLM system between timesteps.
    ch = 0. if method == "ct" else 3.
    t,steps,history = 0.,0,[]
    def record():
        div = discrete_divergence(q,bxf,byf) if method == "ct" else discrete_divergence(q)
        history.append((t,float(abs(div).max()),float(q[...,0].mean()),float(q[...,3].mean())))
        return div
    record()
    while t < final_time:
        fx,ax = _interfaces(q,0,ch,bxf if method == "ct" else None)
        fy,ay = _interfaces(q,1,ch,byf if method == "ct" else None)
        dt = min(cfl/(n*(ax+ay)),final_time-t)
        new = q-dt*n*(fx-np.roll(fx,1,axis=0)+fy-np.roll(fy,1,axis=1))
        if method == "ct":
            # Ez=-Fx(By)=Fy(Bx); unique corner (i+1/2,j+1/2).
            ez = .25*(-fx[...,5]-np.roll(fx[...,5],-1,axis=1)
                       +fy[...,4]+np.roll(fy[...,4],-1,axis=0))
            bxf -= dt*n*(ez-np.roll(ez,1,axis=1))
            byf += dt*n*(ez-np.roll(ez,1,axis=0))
            new[...,4] = .5*(bxf+np.roll(bxf,1,axis=0))
            new[...,5] = .5*(byf+np.roll(byf,1,axis=1))
            # Total energy remains conservative; no magnetic energy reset.
        else:
            new[...,6] *= np.exp(-dt*damping*ch*n)
        primitive(new)
        q = new
        t += dt
        steps += 1
        div = record()
    div = record() if steps == 0 else div
    return MHDResult(q,t,steps,div,np.asarray(history),bxf if method == "ct" else None,byf if method == "ct" else None)
