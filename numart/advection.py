"""Linear model problems connecting stability theory and modern methods."""
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander, legder, legval
from .solvers import rk3


def finite_difference(q, dx, stencil="centered", speed=1.):
    """Periodic spatial derivative. Upwind direction depends on velocity sign."""
    if dx <= 0:
        raise ValueError("dx must be positive")
    if stencil == "upwind":
        stencil = "backward" if speed >= 0 else "forward"
    if stencil == "forward":
        return (np.roll(q,-1)-q)/dx
    if stencil == "backward":
        return (q-np.roll(q,1))/dx
    if stencil == "centered":
        return (np.roll(q,-1)-np.roll(q,1))/(2*dx)
    raise ValueError("Unknown spatial stencil")


def amplification(theta, courant, method):
    """Fourier amplification G(theta), q_j^n=G^n exp(i*j*theta)."""
    if method == "lax-friedrichs":
        return np.cos(theta)-1j*courant*np.sin(theta)
    if method == "lax-wendroff":
        return 1-1j*courant*np.sin(theta)+courant**2*(np.cos(theta)-1)
    if method == "upwind":
        return 1-abs(courant)*(1-np.cos(theta))-1j*courant*np.sin(theta)
    raise ValueError("Unknown difference method")


def difference_step(q, courant, method):
    left,right = np.roll(q,1),np.roll(q,-1)
    if method == "lax-friedrichs":
        return .5*(right+left)-.5*courant*(right-left)
    if method == "lax-wendroff":
        return q-.5*courant*(right-left)+.5*courant**2*(right-2*q+left)
    if method == "upwind":
        return q-courant*(q-left) if courant >= 0 else q-courant*(right-q)
    raise ValueError("Unknown difference method")


def fourier_derivative(q, length=1., order=1):
    k = 2*np.pi*np.fft.fftfreq(len(q), d=length/len(q))
    # For real data the odd derivative of the even-grid Nyquist mode is zero.
    if len(q)%2 == 0 and order%2:
        k[len(q)//2] = 0
    return np.fft.ifft((1j*k)**order*np.fft.fft(q)).real


def spectral_advection(q, time, speed=1., length=1.):
    """Fourier collocation with exact modal time integration for linear advection."""
    k = 2*np.pi*np.fft.fftfreq(len(q), d=length/len(q))
    if len(q)%2 == 0:
        k[len(q)//2] = 0
    return np.fft.ifft(np.fft.fft(q)*np.exp(-1j*speed*k*time)).real


def dg_advection(n=32, degree=2, final_time=1., speed=1., cfl=.2, initial=None):
    """Modal Legendre DG P0/P1/P2, periodic scalar advection, upwind flux.

    Returns quadrature coordinates, reconstructed values, and modal coefficients.
    The P2 fully discrete method has third-order time accuracy (SSPRK3).
    """
    if degree not in (0,1,2) or n < 2 or not 0 < cfl <= .3 or final_time < 0:
        raise ValueError("Require degree 0..2, n>=2, 0<CFL<=.3, final_time>=0")
    initial = initial or (lambda x: np.sin(2*np.pi*x))
    dx = 1/n
    z,w = leggauss(max(degree+2,4))
    basis = legvander(z,degree)
    derivatives = np.stack([legval(z,legder(np.eye(degree+1)[m])) for m in range(degree+1)],axis=1)
    volume = np.einsum("q,qk,qm->mk",w,basis,derivatives)
    x = (np.arange(n)[:,None]+.5+.5*z)/n
    scale = 2*np.arange(degree+1)+1
    coefficients = .5*np.einsum("jq,q,qm->jm",initial(x),w,basis)*scale
    signs = (-1.)**np.arange(degree+1)
    def rhs(u):
        qright,qleft = u.sum(axis=1),u@signs
        flux = speed*qright if speed >= 0 else speed*np.roll(qleft,-1)
        return (speed*u@volume.T-flux[:,None]+np.roll(flux,1)[:,None]*signs)*scale/dx
    t = 0.
    while t < final_time and speed != 0:
        dt = min(cfl*dx/((2*degree+1)*abs(speed)),final_time-t)
        coefficients = rk3(coefficients,dt,rhs)
        t += dt
    return x,coefficients@basis.T,coefficients


def rd_residual(q, speed=1., dx=None):
    """1D P1 nodal residual distribution, lumped mass, upwind distribution.

    Element K=[i,i+1]: Phi_K=a*(u[i+1]-u[i]); distribute to downstream node.
    This introductory 1D scheme equals first-order upwind; no 2D N/LDA scheme.
    """
    dx = 1/len(q) if dx is None else dx
    phi = speed*(np.roll(q,-1)-q)
    distributed = np.roll(phi,1) if speed >= 0 else phi
    return -distributed/dx


def dual_time_advection(n=64, physical_dt=.02, final_time=.2, order=2,
                        tolerance=1.e-10, max_iterations=10000):
    """Implicit upwind + BE/BDF2 physical time; Jacobi pseudo-time iterations.

    Physical dt may exceed explicit CFL. Each inner solve must actually converge.
    Returns x,q and the infinity-norm residual history of the last inner solve.
    """
    if n < 2 or physical_dt <= 0 or final_time <= 0 or order not in (1,2) or tolerance <= 0:
        raise ValueError("Invalid dual-time parameters")
    x = (np.arange(n)+.5)/n
    q = np.sin(2*np.pi*x)
    old = q.copy()
    count = max(1,int(np.ceil(final_time/physical_dt)))
    dt = final_time/count
    history = []
    for step in range(count):
        alpha = 1.5 if order == 2 and step > 0 else 1.
        b = (2*q-.5*old)/dt if alpha == 1.5 else q/dt
        guess = q.copy()
        diagonal = alpha/dt+n
        history = []
        for _ in range(max_iterations):
            residual = alpha/dt*guess+n*(guess-np.roll(guess,1))-b
            history.append(float(np.max(abs(residual))))
            if history[-1] <= tolerance*max(1.,float(np.max(abs(b)))):
                break
            guess -= .8*residual/diagonal
        else:
            raise RuntimeError("Pseudo-time residual did not converge")
        old,q = q,guess
    return x,q,np.asarray(history)


def conditioning_example(n=40):
    """SPD model: compare kappa2(A) and kappa2(P^-1/2 A P^-1/2).

    Jacobi symmetric scaling; this is a linear-algebra example, not Turkel's
    low-Mach PDE preconditioning matrix. Both must be discussed separately.
    """
    base = 2*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
    d = np.geomspace(1,1.e3,n)
    a = d[:,None]*base*d[None,:]
    inv = 1/np.sqrt(np.diag(a))
    scaled = inv[:,None]*a*inv[None,:]
    return a,scaled
