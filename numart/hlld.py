"""Adiabatic ideal-MHD HLLD, eight variables and all three vector components.

Primitive order: rho,vx,vy,vz,p,Bx,By,Bz; conserved replaces v by momentum,
p by total energy. mu0=1. Mathematical construction: Miyoshi & Kusano 2005,
Eqs 38--63; formula cross-check: Athena++ BSD-3-Clause HLLD implementation.
This vectorized implementation uses explicit HLLE fallback for invalid stars.
"""
import numpy as np


def conserved(w,gamma=5/3):
    w=np.asarray(w,dtype=float);q=w.copy()
    q[...,1:4]=w[...,0,None]*w[...,1:4]
    q[...,4]=w[...,4]/(gamma-1)+.5*w[...,0]*np.sum(w[...,1:4]**2,axis=-1)+.5*np.sum(w[...,5:8]**2,axis=-1)
    return q


def primitive(q,gamma=5/3):
    if np.any(q[...,0]<=0) or not np.all(np.isfinite(q)):raise ValueError('Invalid MHD density/state')
    w=q.copy();w[...,1:4]=q[...,1:4]/q[...,0,None]
    w[...,4]=(gamma-1)*(q[...,4]-.5*np.sum(q[...,1:4]**2,axis=-1)/q[...,0]-.5*np.sum(q[...,5:8]**2,axis=-1))
    if np.any(w[...,4]<=0):raise ValueError('Invalid MHD pressure')
    return w


def fast_speed(w,gamma=5/3,axis=0):
    a2=gamma*w[...,4]/w[...,0];b2=np.sum(w[...,5:8]**2,axis=-1)/w[...,0]
    return np.sqrt(.5*(a2+b2+np.sqrt(np.maximum((a2+b2)**2-4*a2*w[...,5+axis]**2/w[...,0],0.))))


def physical_flux(w,gamma=5/3,axis=0):
    q=conserved(w,gamma);v=w[...,1:4];b=w[...,5:8]
    vn=v[...,axis];bn=b[...,axis];pt=w[...,4]+.5*np.sum(b*b,axis=-1)
    f=q*vn[...,None]
    f[...,1:4]-=bn[...,None]*b;f[...,1+axis]+=pt
    f[...,4]=(q[...,4]+pt)*vn-bn*np.sum(v*b,axis=-1)
    f[...,5:8]=vn[...,None]*b-bn[...,None]*v
    return f


def riemann(left,right,gamma=5/3,axis=0,solver='hlld'):
    """Common face-normal B is required; callers implement CT or GLM coupling.

    Returns flux, maximum signal speed, and counts of fallback/degenerate faces.
    Degenerate zero-Bn fans collapse to the single-star branches.
    """
    if solver not in ('hlld','hlle','rusanov') or axis not in (0,1,2):raise ValueError('Invalid Riemann controls')
    left,right=np.broadcast_arrays(np.asarray(left,dtype=float),np.asarray(right,dtype=float))
    if left.shape[-1]!=8 or np.any(left[...,[0,4]]<=0) or np.any(right[...,[0,4]]<=0):raise ValueError('Invalid primitive states')
    if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):raise ValueError('Nonfinite primitive states')
    if not np.allclose(left[...,5+axis],right[...,5+axis],rtol=1e-12,atol=1e-14):raise ValueError('HLLD needs one normal magnetic field')
    perm=[0,1+axis,1+(axis+1)%3,1+(axis+2)%3,4,5+axis,5+(axis+1)%3,5+(axis+2)%3]
    l=left[...,perm];r=right[...,perm]
    ul,ur=conserved(l,gamma),conserved(r,gamma)
    fl,fr=physical_flux(l,gamma),physical_flux(r,gamma)
    sl=np.minimum(l[...,1]-fast_speed(l,gamma),r[...,1]-fast_speed(r,gamma))
    sr=np.maximum(l[...,1]+fast_speed(l,gamma),r[...,1]+fast_speed(r,gamma))
    amax=np.maximum(abs(sl),abs(sr))
    sl0=np.minimum(sl,0);sr0=np.maximum(sr,0)
    fallback=(sr0[...,None]*fl-sl0[...,None]*fr+(sl0*sr0)[...,None]*(ur-ul))/(sr0-sl0)[...,None]
    stats={'hlle_fallback_faces':0,'degenerate_faces':0}
    if solver=='rusanov':flux=.5*(fl+fr-amax[...,None]*(ur-ul))
    elif solver=='hlle':flux=fallback
    else:
        bn=.5*(l[...,5]+r[...,5]);bn2=bn*bn
        ptl=l[...,4]+.5*np.sum(l[...,5:8]**2,axis=-1)
        ptr=r[...,4]+.5*np.sum(r[...,5:8]**2,axis=-1)
        dl=sl-l[...,1];dr=sr-r[...,1]
        with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
            sm=(dr*r[...,0]*r[...,1]-dl*l[...,0]*l[...,1]+ptl-ptr)/(dr*r[...,0]-dl*l[...,0])
            pstar=.5*(ptl+l[...,0]*dl*(sm-l[...,1])+ptr+r[...,0]*dr*(sm-r[...,1]))
            def star(w,u,s,ds,pt):
                result=u.copy();rho=w[...,0]*ds/(s-sm)
                denominator=w[...,0]*ds*(s-sm)-bn2
                small=abs(denominator)<1e-10*np.maximum(abs(pstar),1e-30)
                safe=np.where(small,1.,denominator)
                vt=w[...,2:4]-bn[...,None]*w[...,6:8]*(sm-w[...,1])[...,None]/safe[...,None]
                bt=w[...,6:8]*(w[...,0]*ds**2-bn2)[...,None]/safe[...,None]
                vt=np.where(small[...,None],w[...,2:4],vt)
                bt=np.where(small[...,None],w[...,6:8],bt)
                result[...,0]=rho;result[...,1]=rho*sm;result[...,2:4]=rho[...,None]*vt
                result[...,5]=bn;result[...,6:8]=bt
                vb=sm*bn+np.sum(vt*bt,axis=-1)
                result[...,4]=(ds*u[...,4]-pt*w[...,1]+pstar*sm+
                    bn*(np.sum(w[...,1:4]*w[...,5:8],axis=-1)-vb))/(s-sm)
                return result,vb,small
            ls,vbl,small_l=star(l,ul,sl,dl,ptl);rs,vbr,small_r=star(r,ur,sr,dr,ptr)
            rootl=np.sqrt(ls[...,0]);rootr=np.sqrt(rs[...,0]);sign=np.sign(bn)
            sal=sm-abs(bn)/rootl;sar=sm+abs(bn)/rootr
            vl=ls[...,2:4]/ls[...,0,None];vr=rs[...,2:4]/rs[...,0,None]
            bt=(rootl[...,None]*rs[...,6:8]+rootr[...,None]*ls[...,6:8]+
                (sign*rootl*rootr)[...,None]*(vr-vl))/(rootl+rootr)[...,None]
            vt=(rootl[...,None]*vl+rootr[...,None]*vr+sign[...,None]*(rs[...,6:8]-ls[...,6:8]))/(rootl+rootr)[...,None]
            ld,rd=ls.copy(),rs.copy()
            for state in (ld,rd):state[...,2:4]=state[...,0,None]*vt;state[...,6:8]=bt
            vb=sm*bn+np.sum(vt*bt,axis=-1)
            ld[...,4]=ls[...,4]-rootl*sign*(vbl-vb)
            rd[...,4]=rs[...,4]+rootr*sign*(vbr-vb)
            zero=bn2<1e-20*np.maximum(abs(pstar),1e-30)
            ld=np.where(zero[...,None],ls,ld);rd=np.where(zero[...,None],rs,rd)
            fls=fl+sl[...,None]*(ls-ul);frs=fr+sr[...,None]*(rs-ur)
            fld=fls+sal[...,None]*(ld-ls);frd=frs+sar[...,None]*(rd-rs)
            flux=np.where((sm>=0)[...,None],fld,frd)
            flux=np.where((sal>=0)[...,None],fls,flux)
            flux=np.where((sar<=0)[...,None],frs,flux)
            flux=np.where((sl>=0)[...,None],fl,flux)
            flux=np.where((sr<=0)[...,None],fr,flux)
            bad=~np.all(np.isfinite(flux),axis=-1)
            for state in (ls,rs,ld,rd):
                internal=state[...,4]-.5*np.sum(state[...,1:4]**2,axis=-1)/state[...,0]-.5*np.sum(state[...,5:8]**2,axis=-1)
                bad|=(state[...,0]<=0)|(internal<=0)|~np.isfinite(internal)
            bad&=(sl<0)&(sr>0)
        flux=np.where(bad[...,None],fallback,flux)
        stats['hlle_fallback_faces']=int(np.count_nonzero(bad))
        stats['degenerate_faces']=int(np.count_nonzero(small_l|small_r|zero))
    result=np.empty_like(flux);result[...,perm]=flux
    return result,amax,stats
