import numpy as np
import pytest
from numart.geophysical_grids import symbol, gravity_frequency


@pytest.mark.parametrize('grid',['A','B','C'])
def test_gravity_geostrophic_branches_and_energy_skew_symmetry(grid):
    for k,ell in [(.3,.7),(1.2,-.8),(np.pi,0),(np.pi,np.pi)]:
        matrix=symbol(grid,k,ell,wave_speed=2.,coriolis=.4)
        np.testing.assert_allclose(matrix.conj().T,-matrix,atol=1e-15)
        eigenvalues=np.linalg.eigvals(matrix)
        frequency=gravity_frequency(grid,k,ell,wave_speed=2.,coriolis=.4)
        np.testing.assert_allclose(np.sort(eigenvalues.imag),[-frequency,0,frequency],atol=1e-14)
        assert max(abs(eigenvalues.real)) < 1e-14


@pytest.mark.parametrize('grid',['A','B','C'])
def test_long_wave_frequency_refines_to_continuum(grid):
    exact=np.sqrt(.7**2+1.3**2*(.8**2+.5**2))
    errors=[abs(gravity_frequency(grid,.8,.5,h=h,wave_speed=1.3,coriolis=.7)-exact) for h in (.2,.1,.05)]
    assert min(np.log2(np.array(errors[:-1])/errors[1:])) > 1.98


def test_shortest_height_mode_decoupling_depends_on_layout():
    height=np.array([0,0,1.])
    # A misses the x-only checkerboard. B misses the diagonal checkerboard.
    assert np.linalg.norm(symbol('A',np.pi,0)@height) < 2e-16
    assert np.linalg.norm(symbol('B',np.pi,np.pi)@height) < 3e-16
    assert np.linalg.norm(symbol('B',np.pi,0)@height) > 1.
    assert np.linalg.norm(symbol('C',np.pi,np.pi)@height) > 2.
    # With four-point C-grid Coriolis averaging, rotation disappears here.
    assert abs(symbol('C',np.pi,np.pi)[0,1]) < 1e-30


def test_invalid_grid_or_controls_fail():
    with pytest.raises(ValueError):symbol('D',1.,1.)
    with pytest.raises(ValueError):symbol('A',1.,1.,h=0)
    with pytest.raises(ValueError):symbol('C',float('nan'),1.)


@pytest.mark.parametrize('grid',['A','B','C'])
def test_fourier_symbol_matches_independent_physical_grid_stencils(grid):
    n=24; h=2*np.pi/n; k,ell=2.,3.; c,f=1.7,.8
    i,j=np.meshgrid(np.arange(n),np.arange(n),indexing='ij')
    wave=lambda ox,oy:np.exp(1j*(k*(i+ox)*h+ell*(j+oy)*h))
    z=wave(.5,.5)
    if grid=='A':uw,vw=z,z
    elif grid=='B':uw,vw=wave(0,0),wave(0,0)
    else:uw,vw=wave(0,.5),wave(.5,0)
    amplitude=np.array([.3+.2j,-.4+.1j,.7-.3j])
    u,v,eta=amplitude[0]*uw,amplitude[1]*vw,amplitude[2]*z
    r=lambda q,shift,axis:np.roll(q,shift,axis)
    if grid=='A':
        gx=(r(eta,-1,0)-r(eta,1,0))/(2*h);gy=(r(eta,-1,1)-r(eta,1,1))/(2*h)
        div=(r(u,-1,0)-r(u,1,0)+r(v,-1,1)-r(v,1,1))/(2*h);vu,uv=v,u
    elif grid=='B':
        gx=(eta+r(eta,1,1)-r(eta,1,0)-r(r(eta,1,0),1,1))/(2*h)
        gy=(eta+r(eta,1,0)-r(eta,1,1)-r(r(eta,1,0),1,1))/(2*h)
        div=(r(u,-1,0)+r(r(u,-1,0),-1,1)-u-r(u,-1,1)
            +r(v,-1,1)+r(r(v,-1,1),-1,0)-v-r(v,-1,0))/(2*h);vu,uv=v,u
    else:
        gx=(eta-r(eta,1,0))/h;gy=(eta-r(eta,1,1))/h
        div=(r(u,-1,0)-u+r(v,-1,1)-v)/h
        vu=(v+r(v,1,0)+r(v,-1,1)+r(r(v,1,0),-1,1))/4
        uv=(u+r(u,-1,0)+r(u,1,1)+r(r(u,-1,0),1,1))/4
    measured=np.array([np.mean((f*vu-c*gx)/uw),np.mean((-f*uv-c*gy)/vw),np.mean(-c*div/z)])
    expected=np.einsum('ij,j->i',symbol(grid,k,ell,h,c,f),amplitude)
    np.testing.assert_allclose(measured,expected,atol=2e-14)
