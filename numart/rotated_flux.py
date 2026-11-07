"""Conservative directional HLLE/Roe experiment inspired by rotated hybrids.

F(n)=alpha1 F_HLLE(n1)+alpha2 F_Roe(n2), where n1 follows the velocity jump
and n2 is perpendicular. Small-jump fallback n1 is face-tangential. This
explicit two-flux construction is not the optimized 2008 dissipation formula.
"""
import numpy as np
from .euler2d import primitive
from .shock_robustness import flux as cartesian_flux
from .ausm_plus import flux as ausm_plus_flux


def normal_flux(left,right,normal,solver='hlle',entropy_fraction=.1):
    left,right = np.broadcast_arrays(np.asarray(left,float),np.asarray(right,float))
    normal = np.asarray(normal,float)
    if left.shape[-1] != 4 or normal.shape[-1] != 2 or not np.all(np.isfinite(normal)) or not np.allclose(np.sum(normal**2,axis=-1),1,atol=2e-13):
        raise ValueError('Require Euler states and finite unit normals')
    if solver == 'rotated': return rotated_flux(left,right,normal,entropy_fraction)
    nx,ny = normal[...,0],normal[...,1]
    def rotate(q):
        a = q.copy(); a[...,1] = nx*q[...,1]+ny*q[...,2]; a[...,2] = -ny*q[...,1]+nx*q[...,2]; return a
    l,r = rotate(left),rotate(right)
    f = (ausm_plus_flux(l,r,axis=0,variant='up' if solver=='ausm-up' else 'plus') if solver in ('ausm-plus','ausm-up') else
         cartesian_flux(l,r,0,solver,entropy_fraction))
    result = f.copy(); result[...,1] = nx*f[...,1]-ny*f[...,2]; result[...,2] = ny*f[...,1]+nx*f[...,2]
    return result


def rotated_flux(left,right,normal,entropy_fraction=.1,velocity_tolerance=1e-10):
    if not np.isfinite(velocity_tolerance) or velocity_tolerance <= 0: raise ValueError('Invalid velocity tolerance')
    normal = np.broadcast_to(normal,left.shape[:-1]+(2,))
    wl,wr = primitive(left),primitive(right)
    jump = wr[...,1:3]-wl[...,1:3]; length = np.linalg.norm(jump,axis=-1)
    tangent = np.stack((-normal[...,1],normal[...,0]),axis=-1)
    n1 = np.where((length>velocity_tolerance)[...,None],jump/np.maximum(length[...,None],velocity_tolerance),tangent)
    dot = np.sum(n1*normal,axis=-1); n1 = np.where((dot<0)[...,None],-n1,n1)
    n2 = np.stack((-n1[...,1],n1[...,0]),axis=-1)
    dot = np.sum(n2*normal,axis=-1); n2 = np.where((dot<0)[...,None],-n2,n2)
    a1 = np.sum(n1*normal,axis=-1); a2 = np.sum(n2*normal,axis=-1)
    return (a1[...,None]*normal_flux(left,right,n1,'hlle',entropy_fraction)+
            a2[...,None]*normal_flux(left,right,n2,'roe',entropy_fraction))
