"""Fixed-step canonical maps for H(q,p)=p^2/2+q^2/2+alpha*q^4/4.

One degree of freedom, unit mass. State order is (q,p). Symplecticity is
separate from exact conservation of the original Hamiltonian. No adaptive
steps, N-body gravity, constraints, or dissipative particle dynamics.
"""
import numpy as np

METHODS = ('symplectic-euler','verlet','yoshida4','midpoint','rk4')
SYSTEMS = {'harmonic':0.,'quartic':1.}
J = np.array([[0.,1.],[-1.,0.]])


def energy(state, system='harmonic'):
    z=np.asarray(state);q,p=np.moveaxis(z,-1,0)
    return .5*(q*q+p*p)+SYSTEMS[system]*q**4/4


def _gradient(q,alpha):
    return q+alpha*q**3


def _curvature(q,alpha):
    return 1+3*alpha*q*q


def _field(z,alpha):
    return np.array([z[1],-_gradient(z[0],alpha)])


def _field_jacobian(z,alpha):
    return np.array([[0.,1.],[-_curvature(z[0],alpha),0.]])


def _verlet(z,h,alpha):
    q,p=z;p_half=p-h/2*_gradient(q,alpha)
    q1=q+h*p_half;p1=p_half-h/2*_gradient(q1,alpha)
    k0=np.array([[1.,0.],[-h/2*_curvature(q,alpha),1.]])
    drift=np.array([[1.,h],[0.,1.]])
    k1=np.array([[1.,0.],[-h/2*_curvature(q1,alpha),1.]])
    return np.array([q1,p1]),k1@drift@k0


def canonical_step(state,h,method='verlet',system='harmonic',return_jacobian=False):
    """Advance a (q,p) state; optionally return the analytic map Jacobian.

    Negative h is supported for composition and reversibility checks. Implicit
    midpoint solves its scalar endpoint equation to roundoff using Newton.
    """
    z=np.asarray(state,dtype=float)
    if z.shape!=(2,) or not np.all(np.isfinite(z)) or not np.isfinite(h):
        raise ValueError('Require one finite (q,p) state and finite step')
    if method not in METHODS or system not in SYSTEMS:raise ValueError('Unknown method or system')
    alpha=SYSTEMS[system];q,p=z;identity=np.eye(2)
    if method=='symplectic-euler':
        p1=p-h*_gradient(q,alpha)
        result=np.array([q+h*p1,p1])
        derivative=np.array([[1-h*h*_curvature(q,alpha),h],[-h*_curvature(q,alpha),1.]])
    elif method=='verlet':
        result,derivative=_verlet(z,h,alpha)
    elif method=='yoshida4':
        a=1/(2-2**(1/3));b=-2**(1/3)/(2-2**(1/3))
        result=z.copy();derivative=identity
        for coefficient in (a,b,a):
            result,tangent=_verlet(result,coefficient*h,alpha)
            derivative=tangent@derivative
    elif method=='midpoint':
        q1=q+h*p
        for _ in range(30):
            middle=(q+q1)/2
            residual=q1-q-h*p+h*h/2*_gradient(middle,alpha)
            correction=residual/(1+h*h/4*_curvature(middle,alpha))
            q1-=correction
            if abs(correction)<3e-15*(1+abs(q1)):break
        else:raise RuntimeError('Implicit midpoint did not converge')
        middle=(q+q1)/2
        if abs(q1-q-h*p+h*h/2*_gradient(middle,alpha))>1e-12*(1+abs(q1)):
            raise RuntimeError('Implicit midpoint residual too large')
        result=np.array([q1,p-h*_gradient(middle,alpha)])
        a=_field_jacobian(np.array([middle,0.]),alpha)
        derivative=np.linalg.solve(identity-h/2*a,identity+h/2*a)
    else:
        k1=_field(z,alpha);d1=_field_jacobian(z,alpha)
        z2=z+h/2*k1;k2=_field(z2,alpha);d2=_field_jacobian(z2,alpha)@(identity+h/2*d1)
        z3=z+h/2*k2;k3=_field(z3,alpha);d3=_field_jacobian(z3,alpha)@(identity+h/2*d2)
        z4=z+h*k3;k4=_field(z4,alpha);d4=_field_jacobian(z4,alpha)@(identity+h*d3)
        result=z+h/6*(k1+2*k2+2*k3+k4)
        derivative=identity+h/6*(d1+2*d2+2*d3+d4)
    if not np.all(np.isfinite(result)):raise ValueError('Map produced a nonfinite state')
    return (result,derivative) if return_jacobian else result


def trajectory(h=.2,steps=1000,method='verlet',system='harmonic',initial=(1.,.2)):
    if not isinstance(steps,int) or not 0<=steps<=100000 or not np.isfinite(h) or h<=0:
        raise ValueError('Require positive finite h and 0 <= integer steps <= 100000')
    # Validate method/system/initial even for a zero-step trajectory.
    canonical_step(initial,0.,method,system)
    states=np.empty((steps+1,2));states[0]=initial
    for i in range(steps):states[i+1]=canonical_step(states[i],h,method,system)
    return np.arange(steps+1)*h,states
