"""Explicit RK tableaus, nonlinear stages, and scalar stability polynomials.

SSPRK(5,4) coefficients follow section 3.1 of Gottlieb--Ketcheson--Shu
(2009); see the author-hosted 2008 draft's five-stage fourth-order scheme,
directly above the low-storage discussion. Decimals carry source precision.
"""
import numpy as np


def _tableau(rows, weights, label, order, ssp, family):
    b = np.asarray(weights, dtype=float)
    a = np.zeros((len(b),len(b)))
    for i,row in enumerate(rows): a[i,:len(row)] = row
    return dict(A=a, b=b, c=a.sum(axis=1), label=label, order=order,
                stages=len(b), ssp_coefficient=ssp, family=family)


TABLEAUS = {
 'forward-euler':_tableau([[]],[1.],'Forward Euler / RK1',1,1.,'RK1'),
 'heun':_tableau([[],[1.]],[.5,.5],'Heun / SSPRK(2,2)',2,1.,'RK2'),
 'explicit-midpoint':_tableau([[],[.5]],[0.,1.],'Explicit midpoint / RK2',2,0.,'RK2'),
 'ralston':_tableau([[],[2/3]],[.25,.75],'Ralston / RK2',2,.5,'RK2'),
 'kutta3':_tableau([[],[.5],[-1.,2.]],[1/6,2/3,1/6],'Kutta / RK3',3,0.,'RK3'),
 'ssprk3':_tableau([[],[1.],[.25,.25]],[1/6,1/6,2/3],'SSPRK(3,3) / Shu–Osher',3,1.,'RK3'),
 'ssprk43':_tableau([[],[.5],[.5,.5],[1/6,1/6,1/6]],[1/6,1/6,1/6,.5],'SSPRK(4,3)',3,2.,'RK3'),
 'rk4':_tableau([[],[.5],[0.,.5],[0.,0.,1.]],[1/6,1/3,1/3,1/6],'Classical RK4',4,0.,'RK4'),
}
# Convert the five-stage Shu--Osher form in section 3.1 of the author draft
# to Butcher form. Each row represents the increment relative to y_n, which
# enforces consistency of the affine state combination to source roundoff.
_a = np.zeros((5,5))
_a[1,0] = .391752226571890
_a[2] = .555629506348765*_a[1];_a[2,1] += .368410593050371
_a[3] = .379898148511597*_a[2];_a[3,2] += .251891774271694
_a[4] = .821920045606868*_a[3];_a[4,3] += .544974750228521
_b = .517231671970585*_a[2]+.096059710526147*_a[3]+.386708617503269*_a[4]
_b[3] += .063692468666290;_b[4] += .226007483236906
TABLEAUS['ssprk54'] = _tableau([list(row[:i]) for i,row in enumerate(_a)],_b,
                              'SSPRK(5,4) / Spiteri–Ruuth',4,1.508,'RK4')
EXPLICIT_METHODS = tuple(TABLEAUS)


def rk_step(rhs, time, value, dt, method='rk4', return_stages=False):
    """One explicit RK step for rhs(t,y); optional actual RHS-stage states.

    Does not add adaptivity, embedded error control, or a spatial operator.
    A stage state is an internal predictor, not an exact intermediate solution.
    """
    if method not in TABLEAUS or not np.isfinite(time) or not np.isfinite(dt) or dt <= 0:
        raise ValueError('Require an explicit RK method, finite time, and finite dt>0')
    raw = np.asarray(value)
    u = np.array(raw, dtype=np.result_type(raw.dtype, float), copy=True)
    if not np.all(np.isfinite(u)):
        raise ValueError('Initial value must be finite')
    meta = TABLEAUS[method];a,b,c = (meta[k] for k in ('A','b','c'))
    rates=[];states=[]
    for i in range(len(b)):
        stage=u.copy()
        for j in range(i):stage=stage+dt*a[i,j]*rates[j]
        rate=np.asarray(rhs(time+c[i]*dt,stage))
        if rate.shape != u.shape or not np.all(np.isfinite(rate)):
            raise ValueError('RHS must return finite values with the initial shape')
        rates.append(rate)
        if return_stages:states.append(dict(stage=i+1,time=float(time+c[i]*dt),value=stage.copy(),rhs=rate.copy()))
    result=u.copy()
    for weight,rate in zip(b,rates):result=result+dt*weight*rate
    return (result,states) if return_stages else result


def stability_polynomial(method):
    """Ascending coefficients of R(z)=1+z b^T(I-zA)^(-1) 1."""
    meta=TABLEAUS[method];a,b=meta['A'],meta['b']
    powers=np.ones(len(b));coefficients=[1.]
    for _ in b:
        coefficients.append(float(b@powers));powers=a@powers
    return np.array(coefficients)


def stability_function(z, method):
    return np.polynomial.polynomial.polyval(z,stability_polynomial(method))


def nonlinear_trajectory(method='rk4', steps=20, final_time=1.):
    """y'=-y^2, y(0)=1, exact y=1/(1+t), using the full nonlinear stages."""
    if not isinstance(steps,(int,np.integer)) or isinstance(steps,bool) or steps < 1 or not np.isfinite(final_time) or final_time <= 0:
        raise ValueError('Require integer steps>=1 and finite final_time>0')
    dt=final_time/steps;t=np.linspace(0,final_time,steps+1);y=np.ones(steps+1)
    for k in range(steps):y[k+1]=rk_step(lambda t,v:-v*v,t[k],y[k],dt,method)
    return t,y
