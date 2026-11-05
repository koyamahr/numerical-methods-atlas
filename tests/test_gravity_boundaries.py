import numpy as np
import pytest
from numart.gravity_boundaries import isolated_potential,slab_green_transform,slab_potential


def test_isolated_doubling_equals_direct_nonperiodic_discrete_convolution():
    rng=np.random.default_rng(27);rho=rng.random((4,3,5));spacing=np.array([.2,.3,.15]);self_value=-2.7
    fft=isolated_potential(rho,spacing,self_value);reference=np.zeros_like(rho)
    for target in np.ndindex(rho.shape):
        for source in np.ndindex(rho.shape):
            r=np.linalg.norm((np.array(target)-source)*spacing)
            reference[target]+=rho[source]*(self_value if r==0 else -1/r)*np.prod(spacing)
    np.testing.assert_allclose(fft,reference,atol=4e-15,rtol=3e-15)
    # Moving the source close to one boundary does not create a near image at the opposite face.
    point=np.zeros((8,4,4));point[0,1,1]=1
    phi=isolated_potential(point)
    np.testing.assert_allclose(phi[7,1,1],-1/7,atol=1e-15)


def test_slab_zero_mode_retains_uniform_plane_gravity():
    n=16;rho=np.ones((4,4,n));z=(np.arange(n)+.5)/n-.5
    phi=slab_potential(rho)[0,0]
    expected=2*np.pi*z*z
    np.testing.assert_allclose(phi-phi.mean(),expected-expected.mean(),atol=3e-15)
    acceleration=-np.gradient(phi,1/n)
    np.testing.assert_allclose(acceleration[1:-1],-4*np.pi*z[1:-1],atol=2e-14)


def test_slab_sinusoidal_sheet_matches_exponential_and_zero_mode_kernels():
    nx,ny,nz=16,4,12;j=4;sigma=.7;amplitude=.2
    x=np.arange(nx)/nx;z=(np.arange(nz)+.5)/nz
    rho=np.zeros((nx,ny,nz));rho[:,:,j]=sigma*nz*(1+amplitude*np.cos(2*np.pi*x[:,None]))
    phi=slab_potential(rho)
    expected=2*np.pi*sigma*abs(z-z[j])[None,None,:]-sigma*amplitude*np.cos(2*np.pi*x)[:,None,None]*np.exp(-2*np.pi*abs(z-z[j]))[None,None,:]
    np.testing.assert_allclose(phi,np.broadcast_to(expected,phi.shape),atol=3e-15)


def test_sampled_kernel_dft_matches_independent_direct_vertical_sum():
    rng=np.random.default_rng(2);n=13;density=rng.random(n);dz=1/n
    for k in (0.,2*np.pi,4.1):
        kernel=slab_green_transform(k,n,1.)
        fft=np.fft.ifft(np.fft.fft(np.pad(density,(0,n)))*kernel).real[:n]
        separation=abs(np.arange(n)[:,None]-np.arange(n)[None,:])*dz
        g=2*np.pi*separation if k==0 else -2*np.pi/k*np.exp(-k*separation)
        np.testing.assert_allclose(fft,g@density*dz,atol=4e-15)


def test_continuum_transform_zero_modes_and_sampled_refinement_are_distinct():
    # Compare a fixed nonzero horizontal mode and low vertical modes as dz decreases.
    errors=[]
    for n in (16,32,64):
        sampled=slab_green_transform(2.,n,1.).real[:4]
        continuum=slab_green_transform(2.,n,1.,'continuum')[:4]
        errors.append(np.linalg.norm(sampled-continuum))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>1.9
    kernel=slab_green_transform(0.,16,1.,'continuum')
    assert kernel[0]==2*np.pi
    np.testing.assert_allclose(kernel[2:16:2],0,atol=1e-15)
    np.testing.assert_allclose(kernel[1],-8/np.pi,atol=1e-15)


def test_bad_boundary_inputs_fail():
    with pytest.raises(ValueError):isolated_potential(np.ones((3,3,3)),spacing=0)
    with pytest.raises(ValueError):slab_green_transform(-1.,8,1.)
    with pytest.raises(ValueError):slab_potential(np.ones((4,4,4)),representation='periodic')


def test_sampled_transform_matches_closed_geometric_series_in_chapter():
    n=19;length=1.3;dz=length/n;ell=np.arange(2*n)
    for k in (.3,2.,7.1):
        closed=-2*np.pi*dz/k*np.sinh(k*dz)/(np.cosh(k*dz)-np.cos(np.pi*ell/n))*(1-(-1.)**ell*np.exp(-k*length))
        np.testing.assert_allclose(slab_green_transform(k,n,length),closed,rtol=4e-13,atol=2e-13)
