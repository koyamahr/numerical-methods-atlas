import numpy as np
import pytest
from numart import get_problem
from numart.reconstruction import (euler_eigenbasis,ppm_edges,weno_left,solve_euler,
                                  finite_volume_edges,contact_problem,averaged_state)


def test_characteristic_basis_inverts_and_diagonalizes_euler_flux():
    eq=get_problem('sod').equation;q=eq.conserved(np.array([[1.,.3,.7],[.2,-.5,.4]]))
    r,l=euler_eigenbasis(q);np.testing.assert_allclose(l@r,np.broadcast_to(np.eye(3),r.shape),atol=1e-14)
    for i in range(2):
        columns=[]
        for j in range(3):
            d=np.eye(3)[j]*1e-6
            columns.append((eq.flux(q[i]+d)-eq.flux(q[i]-d))/(2e-6))
        jacobian=np.stack(columns,axis=-1);w=eq.primitive(q[i]);c=np.sqrt(eq.gamma*w[2]/w[0])
        np.testing.assert_allclose(l[i]@jacobian@r[i],np.diag([w[1]-c,w[1],w[1]+c]),atol=2e-9)


def test_ppm_monotonicity_and_parabolic_cell_average():
    rng=np.random.default_rng(42);s=rng.normal(size=(100,5,1));left,right=ppm_edges(s);mean=s[:,2]
    t=np.linspace(0,1,101);six=6*mean-3*(left+right)
    profile=left[:,None,:]+t[None,:,None]*(right[:,None,:]-left[:,None,:]+six[:,None,:]*(1-t[None,:,None]))
    assert np.all(profile>=np.minimum(left,right)[:,None,:]-1e-14)
    assert np.all(profile<=np.maximum(left,right)[:,None,:]+1e-14)
    mid=1.5*mean-.25*(left+right)
    np.testing.assert_allclose((left+4*mid+right)/6,mean,atol=1e-15)


@pytest.mark.parametrize('method',['muscl','ppm','weno-js','weno-z'])
@pytest.mark.parametrize('basis',['component','characteristic'])
def test_uniform_state_and_periodic_primary_conservation(method,basis):
    p=get_problem('entropy-wave');n=48
    result=solve_euler(p,n,method,basis,final_time=.08)
    initial=averaged_state(p,result.x,1/n) if method in ('muscl','ppm') else p.initial(result.x)
    np.testing.assert_allclose(result.q.sum(axis=0),initial.sum(axis=0),atol=3e-12)
    assert result.rejected_steps==0
    assert np.isfinite(result.q).all()
    from dataclasses import replace
    uniform=replace(p,initial=lambda x:p.equation.conserved(np.stack((np.ones_like(x),np.full_like(x,.7),np.ones_like(x)),axis=-1)))
    constant=solve_euler(uniform,16,method,basis,final_time=.08)
    np.testing.assert_allclose(constant.q,uniform.initial(constant.x),atol=2e-14)


@pytest.mark.parametrize('method',['ppm','weno-z'])
@pytest.mark.parametrize('basis',['component','characteristic'])
def test_sod_and_moving_contact(method,basis):
    p=get_problem('sod');result=solve_euler(p,96,method,basis)
    assert p.equation.primitive(result.q)[:,[0,2]].min()>0
    p=contact_problem();result=solve_euler(p,64,method,basis,final_time=.2)
    w=p.equation.primitive(result.q)
    if basis=='characteristic':np.testing.assert_allclose(w[:,1:],1.,atol=1e-11,rtol=0)
    else:assert np.max(abs(w[:,1:]-1))<.01


def test_weno_constant_and_smooth_spatial_flux_derivative():
    for variant in ('js','z'):
        np.testing.assert_allclose(weno_left(np.ones((10,5,3)),variant),1.)
        errors=[]
        for n in (32,64,128):
            x=np.arange(n)/n;v=np.sin(2*np.pi*x)
            stencil=np.stack([np.roll(v,2-k) for k in range(5)],axis=1)[...,None]
            f=weno_left(stencil,variant)[:,0]
            derivative=n*(f-np.roll(f,1))
            errors.append(np.mean(abs(derivative-2*np.pi*np.cos(2*np.pi*x))))
        assert min(np.log2(np.array(errors[:-1])/errors[1:]))>4.5


def test_legacy_solvers_remain_unchanged_and_invalid_choices_fail():
    with pytest.raises(ValueError):solve_euler(get_problem('dam-break'))
    with pytest.raises(ValueError):solve_euler(get_problem('sod'),method='typo')
    with pytest.raises(ValueError):weno_left(np.ones((5,3)),epsilon=0.)
