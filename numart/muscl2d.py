"""Second-order Euler FV on fixed quadrilaterals; primitive MUSCL / SSPRK2.

HLL uses the same acoustic min/max estimates as euler2d.py. Gradients are
physical, evaluated at area centroids; boundary fluxes share a single face.
Face-state positivity scaling is local; failed RK steps are retried, not clipped.
"""
from dataclasses import dataclass
import numpy as np
from .euler2d import conserved, primitive, GAMMA
from .shock_cases import wedge_mesh, step_geometry, oblique_shock, reflected
from .snapshots import SnapshotRecorder


def limited(a,b,kind='mc'):
    if kind not in ('mc','minmod','first'): raise ValueError('Unknown limiter')
    if kind=='first': return np.zeros_like(a)
    same=a*b>0
    magnitude=np.minimum(abs(a),abs(b)) if kind=='minmod' else np.minimum(.5*abs(a+b),2*np.minimum(abs(a),abs(b)))
    return np.where(same,np.sign(a)*magnitude,0.)


def gradients(w,x,y,kind='mc',fluid=None,periodic=False):
    """Limit y secants, then x secants corrected for their physical y shift.

    Columns have common x-centroid coordinates. Nonperiodic edges use one-sided
    data; solid-neighbor secants are excluded. Affine fields are reproduced.
    """
    fluid=np.ones(w.shape[:2],dtype=bool) if fluid is None else fluid
    def secants(values,coordinate,axis,correction=None):
        a=np.roll(values,1,axis=axis);b=np.roll(values,-1,axis=axis)
        dl=coordinate-np.roll(coordinate,1,axis=axis)
        dr=np.roll(coordinate,-1,axis=axis)-coordinate
        if periodic:
            dl=np.full_like(dl,1/values.shape[axis]);dr=dl
        left=fluid & np.roll(fluid,1,axis=axis);right=fluid & np.roll(fluid,-1,axis=axis)
        if not periodic:
            first=[slice(None)]*2;last=first.copy();first[axis]=0;last[axis]=-1
            left[tuple(first)]=False;right[tuple(last)]=False
        dleft=values-a;dright=b-values
        if correction is not None:
            dleft-=correction*(y-np.roll(y,1,axis=axis))[...,None]
            dright-=correction*(np.roll(y,-1,axis=axis)-y)[...,None]
        sleft=dleft/np.where(dl!=0,dl,1)[...,None]
        sright=dright/np.where(dr!=0,dr,1)[...,None]
        sleft=np.where(left[...,None],sleft,sright)
        sright=np.where(right[...,None],sright,sleft)
        return np.where((left|right)[...,None],limited(sleft,sright,kind),0.)
    gy=secants(w,y,1)
    gx=secants(w,x,0,None if periodic else gy)
    return gx,gy


@dataclass
class Geometry:
    x: np.ndarray
    y: np.ndarray
    cx: np.ndarray
    cy: np.ndarray
    volume: np.ndarray
    xf: np.ndarray
    yf: np.ndarray
    xg: np.ndarray
    yg: np.ndarray
    vertical: np.ndarray
    length: np.ndarray
    nx: np.ndarray
    ny: np.ndarray


def geometry(x,y):
    px=np.stack((x[:-1,:-1],x[1:,:-1],x[1:,1:],x[:-1,1:]),axis=-1)
    py=np.stack((y[:-1,:-1],y[1:,:-1],y[1:,1:],y[:-1,1:]),axis=-1)
    cross=px*np.roll(py,-1,axis=-1)-np.roll(px,-1,axis=-1)*py
    area=.5*cross.sum(axis=-1)
    if np.any(area<=0):raise ValueError('Nonpositive cell area')
    cx=((px+np.roll(px,-1,axis=-1))*cross).sum(axis=-1)/(6*area)
    cy=((py+np.roll(py,-1,axis=-1))*cross).sum(axis=-1)/(6*area)
    dx=np.diff(x,axis=0);dy=np.diff(y,axis=0);length=np.hypot(dx,dy)
    return Geometry(x,y,cx,cy,area,.5*(x[:,:-1]+x[:,1:]),.5*(y[:,:-1]+y[:,1:]),
        .5*(x[:-1]+x[1:]),.5*(y[:-1]+y[1:]),np.diff(y,axis=1),length,-dy/length,dx/length)


def hll(left,right,nx=1.,ny=0.):
    """Primitive inputs; oriented acoustic-HLL flux, equivalent to normal_flux."""
    ul,ur=conserved(left),conserved(right)
    vnleft=left[...,1]*nx+left[...,2]*ny
    vnright=right[...,1]*nx+right[...,2]*ny
    cl=np.sqrt(GAMMA*left[...,3]/left[...,0]);cr=np.sqrt(GAMMA*right[...,3]/right[...,0])
    sl=np.minimum(np.minimum(vnleft-cl,vnright-cr),0.)
    sr=np.maximum(np.maximum(vnleft+cl,vnright+cr),0.)
    def flux(q,w,vn):
        f=q*vn[...,None];f[...,1]+=w[...,3]*nx;f[...,2]+=w[...,3]*ny
        f[...,3]=(q[...,3]+w[...,3])*vn
        return f
    return (sr[...,None]*flux(ul,left,vnleft)-sl[...,None]*flux(ur,right,vnright)
            +(sl*sr)[...,None]*(ur-ul))/(sr-sl)[...,None]


def face_values(q,g,kind,fluid=None,periodic=False):
    w=primitive(q);gx,gy=gradients(w,g.cx,g.cy,kind,fluid,periodic)
    offsets=[(g.xf[:-1]-g.cx,g.yf[:-1]-g.cy),(g.xf[1:]-g.cx,g.yf[1:]-g.cy),
             (g.xg[:,:-1]-g.cx,g.yg[:,:-1]-g.cy),(g.xg[:,1:]-g.cx,g.yg[:,1:]-g.cy)]
    deltas=[gx*dx[...,None]+gy*dy[...,None] for dx,dy in offsets]
    theta=np.ones(w.shape[:2])
    for delta in deltas:
        for component in (0,3):
            negative=delta[...,component]<0
            theta=np.minimum(theta,np.where(negative,
                (w[...,component]-1e-12)/np.maximum(-delta[...,component],1e-300),1.))
    theta=np.clip(theta,0,1)
    return [w+theta[...,None]*d for d in deltas],int(np.count_nonzero(theta<1))


def boundary_rhs(q,g,kind,case,upstream,fluid):
    (left,right,bottom,top),scaled=face_values(q,g,kind,fluid)
    # x faces: each orientation points in +x, including boundary ghost states.
    wl=np.concatenate((upstream[None,None,:]+np.zeros_like(left[:1]),right),axis=0)
    wr=np.concatenate((left,right[-1:]),axis=0)
    fx=hll(wl,wr)*g.vertical[...,None]
    if case=='wedge':
        ghost=primitive(reflected(conserved(bottom[:,0]),g.nx[:,0],g.ny[:,0]))
        lower=ghost[:,None,:]
        upper=np.broadcast_to(upstream,top[:,-1:].shape)
    else:
        lower=bottom[:,:1].copy();lower[...,2]*=-1
        upper=top[:,-1:].copy();upper[...,2]*=-1
    wl=np.concatenate((lower,top),axis=1);wr=np.concatenate((bottom,upper),axis=1)
    fy=hll(wl,wr,g.nx,g.ny)*g.length[...,None]
    if case=='step':
        # Replace obstacle-face states by the reflection of the FLUID trace.
        for axis,flux,lo,hi in ((0,fx,right[:-1],left[1:]),(1,fy,top[:,:-1],bottom[:,1:])):
            ml,mr=(fluid[:-1],fluid[1:]) if axis==0 else (fluid[:,:-1],fluid[:,1:])
            internal=flux[1:-1] if axis==0 else flux[:,1:-1]
            for mask,state,reverse in ((ml&~mr,lo,False),(~ml&mr,hi,True)):
                if not np.any(mask):continue
                ghost=state[mask].copy();ghost[:,1+axis]*=-1
                a,b=(ghost,state[mask]) if reverse else (state[mask],ghost)
                internal[mask]=hll(a,b,int(axis==0),int(axis==1))*(1/fluid.shape[1])
    rhs=-(fx[1:]-fx[:-1]+fy[:,1:]-fy[:,:-1])/g.volume[...,None]
    rhs[~fluid]=0.
    return rhs,scaled


@dataclass
class Result:
    q: np.ndarray
    geometry: Geometry
    time: float
    steps: int
    history: np.ndarray
    fluid: np.ndarray
    snapshots: object
    retries: int
    scaled_faces: int


def _evolve(q,g,fluid,final_time,cfl,rhs,snapshot_times=None):
    recorder=SnapshotRecorder(snapshot_times,final_time);recorder.capture(0.,0,q)
    t=0.;steps=0;retries=0;scaled_total=0;history=[]
    dx=np.diff(g.x[:,0])[:,None]
    shear=np.maximum(abs(np.diff(g.y,axis=0)[:,:-1]),abs(np.diff(g.y,axis=0)[:,1:]))
    height=.5*(g.vertical[:-1]+g.vertical[1:])
    while t<final_time:
        w=primitive(q);c=np.sqrt(GAMMA*w[...,3]/w[...,0])
        sx=np.max((abs(w[...,1])+c)[fluid]);sy=np.max((abs(w[...,2])+c)[fluid])
        dt=min(final_time-t,cfl*np.min((g.volume/(sx*(height+shear)+sy*dx))[fluid]))
        before=q
        for attempt in range(16):
            try:
                r,scale1=rhs(q);first=q+dt*r;primitive(first)
                r,scale2=rhs(first);trial=.5*q+.5*(first+dt*r);primitive(trial)
                break
            except ValueError:
                dt*=.5;retries+=1
        else:raise RuntimeError('MUSCL step could not preserve positive states')
        q=trial;t+=dt;steps+=1;scaled_total+=scale1+scale2
        recorder.capture(t,steps,q)
        if steps%50==0 or t==final_time:history.append((t,np.max(abs(q-before))/dt))
    return Result(q,g,t,steps,np.asarray(history),fluid,recorder.frames,retries,scaled_total)


def solve_shock(case='wedge',ny=40,mach=2.5,limiter='mc',final_time=3.,cfl=.4,snapshot_times=None):
    if case not in ('wedge','step') or limiter not in ('first','minmod','mc'):
        raise ValueError('Require wedge/step and first/minmod/mc')
    if not np.isfinite(final_time) or final_time<0 or not 0<cfl<=.4:raise ValueError('Invalid time controls')
    if case=='wedge':
        x,y,*_=wedge_mesh(ny);fluid=np.ones((3*ny,ny),dtype=bool)
        upstream=primitive(oblique_shock(mach)['upstream'])
    else:
        x,y,fluid=step_geometry(ny);upstream=np.array([1.4,3.,0.,1.])
    g=geometry(x,y);q=np.broadcast_to(conserved(upstream),(*fluid.shape,4)).copy()
    rhs=lambda state:boundary_rhs(state,g,limiter,case,upstream,fluid)
    return _evolve(q,g,fluid,final_time,cfl,rhs,snapshot_times)


def entropy_average(n,time,u=.7,v=.3):
    x=(np.arange(n)+.5)/n
    xx,yy=np.meshgrid(x-u*time,x-v*time,indexing='ij')
    density=1+.2*np.sinc(1/n)**2*np.sin(2*np.pi*xx)*np.sin(2*np.pi*yy)
    w=np.empty((n,n,4));w[...,0]=density;w[...,1]=u;w[...,2]=v;w[...,3]=1.
    return conserved(w)


def smooth_entropy(n=32,final_time=.5,limiter='mc',cfl=.4):
    if n<8 or not np.isfinite(final_time) or final_time<0 or not 0<cfl<=.4:raise ValueError('Invalid controls')
    x,y=np.meshgrid(np.linspace(0,1,n+1),np.linspace(0,1,n+1),indexing='ij');g=geometry(x,y)
    q=entropy_average(n,0);fluid=np.ones((n,n),dtype=bool)
    def rhs(state):
        (l,r,b,t),scaled=face_values(state,g,limiter,periodic=True)
        fx=hll(r,np.roll(l,-1,axis=0));fy=hll(t,np.roll(b,-1,axis=1),0.,1.)
        return -n*(fx-np.roll(fx,1,axis=0)+fy-np.roll(fy,1,axis=1)),scaled
    return _evolve(q,g,fluid,final_time,cfl,rhs)
