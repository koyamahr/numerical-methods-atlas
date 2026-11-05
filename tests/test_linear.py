import numpy as np
import pytest
from numart.linear import thomas,diffusion_1d,poisson_1d,poisson_2d,spectral_diffusion


def test_thomas_against_independent_dense_solution_and_no_mutation():
    rng=np.random.default_rng(7)
    l,u=rng.uniform(-1,1,(2,16))
    d=np.full(17,4.)
    b=rng.normal(size=17)
    copies=[v.copy() for v in (l,d,u,b)]
    a=np.diag(d)+np.diag(l,-1)+np.diag(u,1)
    np.testing.assert_allclose(thomas(l,d,u,b),np.linalg.solve(a,b),atol=2e-15)
    for original,copy in zip((l,d,u,b),copies):
        np.testing.assert_array_equal(original,copy)


def test_thomas_rejects_zero_pivot():
    with pytest.raises(np.linalg.LinAlgError):
        thomas([1.],[0.,1.],[1.],[1.,1.])


@pytest.mark.parametrize("method",["ftcs","backward-euler","crank-nicolson"])
def test_diffusion_matches_exact_and_refines(method):
    errors=[]
    for n in (31,63):
        x,q,m=diffusion_1d(n,method=method)
        errors.append(abs(q-np.exp(-np.pi**2*.1)*np.sin(np.pi*x)).max())
        assert np.all(q>0)
    assert errors[-1]<.3*errors[0]


def test_diffusion_explicit_stability_condition():
    with pytest.raises(ValueError):
        diffusion_1d(31,dt=.01,method="ftcs")
    x,q,m=diffusion_1d(31,dt=.01,method="backward-euler")
    assert m["diffusion_number"]>1
    assert np.isfinite(q).all()


@pytest.mark.parametrize("dim",[1,2])
def test_poisson_second_order(dim):
    errors=[]
    for n in (15,31):
        if dim==1:
            x,q=poisson_1d(n)
            exact=np.sin(np.pi*x)
        else:
            x,y,q,res=poisson_2d(n)
            exact=np.sin(np.pi*x)*np.sin(np.pi*y)
        errors.append(abs(q-exact).max())
    assert np.log2(errors[0]/errors[1])>1.9


def test_poisson_cg_for_general_forcing_satisfies_discrete_residual():
    n=13
    f=np.random.default_rng(8).normal(size=(n,n))
    x,y,q,res=poisson_2d(n,forcing=f)
    a=np.pad(q,1)
    actual=(4*q-a[:-2,1:-1]-a[2:,1:-1]-a[1:-1,:-2]-a[1:-1,2:])*(n+1)**2-f
    assert np.linalg.norm(actual)<1e-8
    assert len(res)>10


def test_spectral_heat_exact_mode_decay():
    x=np.arange(32)/32
    q=spectral_diffusion(np.sin(4*np.pi*x),.01)
    np.testing.assert_allclose(q,np.sin(4*np.pi*x)*np.exp(-16*np.pi**2*.01),atol=4e-16)


def test_robin_second_order_with_manufactured_exponential():
    from numart.linear import Boundary,poisson_boundary_1d
    errors=[]
    for n in (15,31):
        left=Boundary(2.,1.,1.)  # 2*u(0)-u'(0)=1
        right=Boundary(1.,1.,2*np.e)
        x,q=poisson_boundary_1d(n,lambda x:-np.exp(x),left,right)
        errors.append(abs(q-np.exp(x)).max())
    assert np.log2(errors[0]/errors[1])>1.9


def test_neumann_compatibility_and_mean_gauge():
    from numart.linear import Boundary,poisson_boundary_1d
    x,q=poisson_boundary_1d(31,-2.,Boundary.neumann(0.),Boundary.neumann(2.))
    expected=x*x
    expected-=(x[1]-x[0])*(expected.sum()-.5*(expected[0]+expected[-1]))
    np.testing.assert_allclose(q,expected,atol=3e-14)
    with pytest.raises(ValueError):
        poisson_boundary_1d(31,1.,Boundary.neumann(0.),Boundary.neumann(0.))


def test_mixed_dirichlet_neumann():
    from numart.linear import Boundary,poisson_boundary_1d
    x,q=poisson_boundary_1d(31,-2.,Boundary.dirichlet(1.),Boundary.neumann(2.))
    np.testing.assert_allclose(q,1+x*x,atol=3e-14)


def test_iteration_spectral_radii_on_poisson_matrix():
    from numart.linear import iteration_matrix,spectral_radius
    n=20
    a=2*np.eye(n)-np.eye(n,k=-1)-np.eye(n,k=1)
    rhoj=np.cos(np.pi/(n+1))
    np.testing.assert_allclose(spectral_radius(iteration_matrix(a)),rhoj,atol=2e-14)
    np.testing.assert_allclose(spectral_radius(iteration_matrix(a,"gauss-seidel")),rhoj**2,atol=2e-14)
    optimum=2/(1+np.sin(np.pi/(n+1)))
    assert spectral_radius(iteration_matrix(a,"sor",optimum))<rhoj**2
