"""Full-vector ideal-MHD standard tests, HLLD/HLLE, MC + SSPRK2.

1D: common longitudinal field. 2D: CT-Contact corner EMF (Gardiner--Stone;
Mignone--Del Zanna 2020 Eqs 20--22) or conservative cell-centered GLM with
an exact Bn/psi interface solve and split damping (Mignone--Tzeferacos 2010).
Not CTU, UCT-HLLD, AMR, or a new implementation of the old planar OT solver.
"""
from dataclasses import dataclass
import numpy as np
from .hlld import conserved,primitive,riemann,fast_speed
from .muscl2d import limited
from .snapshots import SnapshotRecorder


def slopes(w,axis,limiter='mc',periodic=True):
    a=w-np.roll(w,1,axis=axis);b=np.roll(w,-1,axis=axis)-w
    if not periodic:
        first=[slice(None)]*w.ndim;last=first.copy();first[axis]=0;last[axis]=-1
        a[tuple(first)]=0;b[tuple(last)]=0
    result=limited(a,b,limiter)
    theta=np.ones(w.shape[:-1])
    for component in (0,4):
        delta=.5*abs(result[...,component])
        theta=np.minimum(theta,(w[...,component]-1e-12)/np.maximum(delta,1e-300))
    return result*np.clip(theta,0,1)[...,None]


@dataclass
class MHDTestResult:
    q: np.ndarray
    time: float
    steps: int
    history: np.ndarray
    stats: dict
    snapshots: object = None
    bx: object = None
    by: object = None


def alfven_average(n,time=0.,amplitude=.1,gamma=5/3):
    phase=2*np.pi*((np.arange(n)+.5)/n-time)
    w=np.zeros((n,8));w[:,0]=1;w[:,4]=.1;w[:,5]=1.
    w[:,6]=amplitude*np.cos(phase);w[:,7]=amplitude*np.sin(phase);w[:,2:4]=-w[:,6:8]
    q=conserved(w,gamma)
    # Integrate transverse sinusoids; the exact energy density is constant.
    q[:,2:4]*=np.sinc(1/n);q[:,6:8]*=np.sinc(1/n)
    return q


def solve_1d(case='brio-wu',n=400,final_time=None,solver='hlld',limiter='mc',cfl=.35):
    if case not in ('brio-wu','alfven') or n<16 or not 0<cfl<=.4:raise ValueError('Invalid MHD 1D controls')
    gamma=2. if case=='brio-wu' else 5/3
    final_time=(.1 if case=='brio-wu' else 1.) if final_time is None else final_time
    if final_time<0 or not np.isfinite(final_time):raise ValueError('Invalid time')
    periodic=case=='alfven';x=(np.arange(n)+.5)/n
    if periodic:q=alfven_average(n)
    else:
        w=np.where((x<.5)[:,None],np.array([1.,0,0,0,1.,.75,1.,0]),np.array([.125,0,0,0,.1,.75,-1.,0]));q=conserved(w,gamma)
    t=0.;steps=0;history=[];total_fallback=0;retries=0
    def rhs(state):
        w=primitive(state,gamma);s=slopes(w,0,limiter,periodic)
        if periodic:left=w+.5*s;right=np.roll(w-.5*s,-1,axis=0)
        else:
            left=np.concatenate((w[:1],w+.5*s));right=np.concatenate((w-.5*s,w[-1:]));
        f,a,stats=riemann(left,right,gamma,solver=solver)
        r=-n*(f-np.roll(f,1,axis=0)) if periodic else -n*(f[1:]-f[:-1])
        return r,stats['hlle_fallback_faces']
    while t<final_time:
        w=primitive(q,gamma);dt=min(cfl/(n*np.max(abs(w[:,1])+fast_speed(w,gamma))),final_time-t)
        for attempt in range(12):
            try:
                r,s1=rhs(q);a=q+dt*r;primitive(a,gamma)
                r,s2=rhs(a);b=.5*q+.5*(a+dt*r);primitive(b,gamma);break
            except ValueError:dt*=.5;retries+=1
        else:raise RuntimeError('MHD 1D positivity failure')
        q=b;t+=dt;steps+=1;total_fallback+=s1+s2
    return MHDTestResult(q,t,steps,np.asarray(history),dict(hlle_fallback_faces=total_fallback,retried_steps=retries))


def ct_contact_emf(fx,fy,w,dx,dy):
    """One corner (i+1/2,j+1/2), contact-upwinded transverse derivatives."""
    ex=-fx[...,6];ey=fy[...,5]
    ec=w[...,2]*w[...,5]-w[...,1]*w[...,6]
    choose=lambda mass,a,b:np.where(mass>0,a,np.where(mass<0,b,.5*(a+b)))
    east=lambda a:np.roll(a,-1,axis=0)
    north=lambda a:np.roll(a,-1,axis=1)
    sy=choose(fx[...,0],ey-ec,east(ey-ec))*2/dy
    ny=choose(north(fx[...,0]),north(ec)-ey,east(north(ec)-ey))*2/dy
    wx=choose(fy[...,0],ex-ec,north(ex-ec))*2/dx
    ee=choose(east(fy[...,0]),east(ec)-ex,north(east(ec)-ex))*2/dx
    return .25*(ex+north(ex)+ey+east(ey))+.125*(dy*(sy-ny)+dx*(wx-ee))


def initial_loop(n=32,method='ct'):
    """[-1,1] x [-.5,.5], v=(2,1,0), rho=p=1, Az=1e-3 max(.3-r,0).

    CT: curl of corner potential, then face-to-cell averaging. GLM: central
    curl of cell potential. Each starts with zero divergence in its own operator.
    """
    if n<8:raise ValueError('n>=8 required')
    dx=dy=1/n
    x=-1+(np.arange(2*n)+.5)*dx;y=-.5+(np.arange(n)+.5)*dy
    def potential(x,y):return 1e-3*np.maximum(.3-np.hypot(x[:,None],y[None,:]),0.)
    if method=='ct':
        a=potential(x+.5*dx,y+.5*dy)
        bx=(a-np.roll(a,1,axis=1))/dy;by=-(a-np.roll(a,1,axis=0))/dx
        bxc=.5*(bx+np.roll(bx,1,axis=0));byc=.5*(by+np.roll(by,1,axis=1))
    elif method=='glm':
        a=potential(x,y)
        bxc=(np.roll(a,-1,axis=1)-np.roll(a,1,axis=1))/(2*dy)
        byc=-(np.roll(a,-1,axis=0)-np.roll(a,1,axis=0))/(2*dx);bx=by=None
    else:raise ValueError('ct/glm required')
    w=np.zeros((2*n,n,8));w[...,0]=1.;w[...,1]=2.;w[...,2]=1.;w[...,4]=1.
    w[...,5]=bxc;w[...,6]=byc
    q=conserved(w)
    if method=='glm':q=np.concatenate((q,np.zeros((*q.shape[:2],1))),axis=-1)
    return q,bx,by,dx,dy


def divergence(q,dx,dy,bx=None,by=None):
    if bx is not None:return (bx-np.roll(bx,1,axis=0))/dx+(by-np.roll(by,1,axis=1))/dy
    return (np.roll(q[...,5],-1,axis=0)-np.roll(q[...,5],1,axis=0))/(2*dx)+(np.roll(q[...,6],-1,axis=1)-np.roll(q[...,6],1,axis=1))/(2*dy)


def interface_flux(q,axis,solver,limiter,bnormal=None,ch=0.):
    w=primitive(q[...,:8]);
    if ch:w=np.concatenate((w,q[...,8,None]),axis=-1)
    s=slopes(w,axis,limiter);left=w+.5*s;right=np.roll(w-.5*s,-1,axis=axis)
    index=5+axis
    if bnormal is not None:left[...,index]=right[...,index]=bnormal
    if ch:
        normal=.5*(left[...,index]+right[...,index])-.5*(right[...,8]-left[...,8])/ch
        psi=.5*(left[...,8]+right[...,8])-.5*ch*(right[...,index]-left[...,index])
        left[...,index]=right[...,index]=normal
    f,a,stats=riemann(left[...,:8],right[...,:8],axis=axis,solver=solver)
    if ch:
        f[...,index]=psi;f=np.concatenate((f,(ch*ch*normal)[...,None]),axis=-1)
        a=np.maximum(a,ch)
    return f,float(np.max(a)),stats


def loop_rhs(q,bx,by,dx,dy,method,solver,limiter,ch):
    fx,ax,sx=interface_flux(q,0,solver,limiter,bx if method=='ct' else None,ch)
    fy,ay,sy=interface_flux(q,1,solver,limiter,by if method=='ct' else None,ch)
    r=-(fx-np.roll(fx,1,axis=0))/dx-(fy-np.roll(fy,1,axis=1))/dy
    if method=='ct':
        ez=ct_contact_emf(fx,fy,primitive(q),dx,dy)
        rx=-(ez-np.roll(ez,1,axis=1))/dy;ry=(ez-np.roll(ez,1,axis=0))/dx
    else:rx=ry=None
    return r,rx,ry,sx['hlle_fallback_faces']+sy['hlle_fallback_faces']


def solve_loop(n=32,final_time=1.,method='ct',solver='hlld',limiter='mc',cfl=.3,damping=.18,snapshot_times=None):
    if final_time<0 or not np.isfinite(final_time) or not 0<cfl<=.35 or damping<0:raise ValueError('Invalid controls')
    q,bx,by,dx,dy=initial_loop(n,method);ch=4. if method=='glm' else 0.
    recorder=SnapshotRecorder(snapshot_times,final_time);t=0.;steps=0;history=[];fallback=0;retries=0
    def record():
        div=divergence(q,dx,dy,bx,by);benergy=.5*np.mean(q[...,5]**2+q[...,6]**2+q[...,7]**2)
        history.append((t,float(np.max(abs(div))),float(benergy),float(q[...,0].mean()),float(q[...,4].mean())))
        recorder.capture(t,steps,q,dict(max_abs_divB=float(np.max(abs(div)))))
    def update(state,x,y,r,rx,ry,dt):
        new=state+dt*r
        if method=='ct':
            x=x+dt*rx;y=y+dt*ry
            new[...,5]=.5*(x+np.roll(x,1,axis=0));new[...,6]=.5*(y+np.roll(y,1,axis=1))
        primitive(new[...,:8]);return new,x,y
    record()
    while t<final_time:
        w=primitive(q[...,:8]);ax=max(float(np.max(abs(w[...,1])+fast_speed(w))),ch)
        ay=max(float(np.max(abs(w[...,2])+fast_speed(w,axis=1))),ch)
        dt=min(cfl/(ax/dx+ay/dy),final_time-t)
        for attempt in range(12):
            try:
                start=q.copy()
                if ch:start[...,8]*=np.exp(-.5*dt*damping*ch/min(dx,dy))
                r,rx,ry,f1=loop_rhs(start,bx,by,dx,dy,method,solver,limiter,ch)
                a,xa,ya=update(start,bx,by,r,rx,ry,dt)
                r,rx,ry,f2=loop_rhs(a,xa,ya,dx,dy,method,solver,limiter,ch)
                b,xb,yb=update(a,xa,ya,r,rx,ry,dt)
                trial=.5*(start+b)
                if method=='ct':
                    xb=.5*(bx+xb);yb=.5*(by+yb)
                    trial[...,5]=.5*(xb+np.roll(xb,1,axis=0));trial[...,6]=.5*(yb+np.roll(yb,1,axis=1))
                else:trial[...,8]*=np.exp(-.5*dt*damping*ch/min(dx,dy))
                primitive(trial[...,:8]);break
            except ValueError:dt*=.5;retries+=1
        else:raise RuntimeError('MHD loop positivity failure')
        q=trial;bx,by=xb,yb;t+=dt;steps+=1;fallback+=f1+f2;record()
    return MHDTestResult(q,t,steps,np.asarray(history),dict(hlle_fallback_faces=fallback,retried_steps=retries),recorder.frames,bx,by)
