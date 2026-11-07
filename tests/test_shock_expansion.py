"""Independent identities, continuum limits and controlled flow checks."""
import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss
from numart.equations import Euler
from numart.euler2d import GAMMA, conserved, primitive, physical_flux
from numart.ausm_plus import flux, mach4, pressure5
from numart.rotated_flux import normal_flux
from numart.shock_robustness import flux as old_flux
from numart.ppm_traced import trace, profiles, solve
from numart.reconstruction import contact_problem, averaged_state
from numart.benchmarks import get_problem
from numart.roe_properties import normal_shock
from numart.blunt_body import geometry, reflect, rhs, solve as solve_blunt, stagnation_pressure


@pytest.mark.parametrize('variant',['plus','up'])
def test_ausm_uniform_contacts_shocks_and_supersonic_flux(variant):
    eq = Euler()
    rng = np.random.default_rng(123)
    w = rng.uniform(.2,2,(80,3)); w[:,1] -= 1
    q = eq.conserved(w)
    np.testing.assert_allclose(flux(q,q,variant=variant),eq.flux(q),atol=4e-15)
    for u in (-.4,0.,.4):
        a,b = eq.conserved(np.array([[1,u,1],[2,u,1]]))
        np.testing.assert_allclose(flux(a,b,variant=variant),eq.flux(a if u>=0 else b),atol=3e-15)
    for mach in (1.2,3.,10.):
        a,b = normal_shock(mach)
        np.testing.assert_allclose(flux(a,b,variant=variant),eq.flux(a),rtol=8e-14,atol=2e-13)
    for sign in (-1,1):
        a,b = eq.conserved(np.array([[1,sign*5,1],[2,sign*6,1]]))
        np.testing.assert_allclose(flux(a,b,variant=variant),eq.flux(a if sign>0 else b),atol=4e-14)


def test_ausm_polynomial_partitions_sonic_continuity_and_diffusion_sign():
    m = np.linspace(-3,3,601)
    np.testing.assert_allclose(mach4(m,1)+mach4(m,-1),m,atol=3e-16)
    for alpha in (-.75,0.,3/16):
        np.testing.assert_allclose(pressure5(m,1,alpha)+pressure5(m,-1,alpha),1,atol=4e-16)
        for sign in (-1,1):
            for sonic in (-1,1):
                np.testing.assert_allclose(pressure5(sonic-1e-7,sign,alpha),pressure5(sonic+1e-7,sign,alpha),atol=2e-12)
    eq = Euler(); a,b = eq.conserved(np.array([[1,0,1.001],[1,0,.999]]))
    assert flux(a,b,variant='plus')[0] == 0
    slow = flux(a,b,mach_cutoff=.01)[0]; fast = flux(a,b,mach_cutoff=1)[0]
    assert slow > fast > 0  # Pressure diffusion goes down the pressure gradient.
    assert flux(a,b,kp=0)[0] == 0
    a,b = eq.conserved(np.array([[1,.01,1],[1,-.01,1]]))
    assert flux(a,b,ku=.75)[1] > flux(a,b,ku=0)[1]
    for cutoff in (0,-1,float('nan'),1.01):
        with pytest.raises(ValueError): flux(a,b,mach_cutoff=cutoff)


@pytest.mark.parametrize('solver',['roe','hlle','ausm-plus','ausm-up','rotated'])
def test_normal_flux_consistency_conservation_and_rotation(solver):
    rng = np.random.default_rng(33)
    left = conserved(rng.uniform(.2,2,(30,4))); right = conserved(rng.uniform(.2,2,(30,4)))
    theta = np.linspace(.1,5,30); n = np.stack((np.cos(theta),np.sin(theta)),axis=-1)
    expected = n[:,0,None]*physical_flux(left,0)+n[:,1,None]*physical_flux(left,1)
    np.testing.assert_allclose(normal_flux(left,left,n,solver),expected,atol=1e-14)
    np.testing.assert_allclose(normal_flux(left,right,n,solver),-normal_flux(right,left,-n,solver),atol=2e-14)
    angle = .37; c,s = np.cos(angle),np.sin(angle)
    def rotate(a):
        b=a.copy();b[...,0]=c*a[...,0]-s*a[...,1];b[...,1]=s*a[...,0]+c*a[...,1];return b
    a,b=left.copy(),right.copy();a[:,1:3]=rotate(left[:,1:3]);b[:,1:3]=rotate(right[:,1:3])
    original = normal_flux(left,right,n,solver); target = original.copy();target[:,1:3]=rotate(original[:,1:3])
    np.testing.assert_allclose(normal_flux(a,b,rotate(n),solver),target,atol=2e-14)


def test_rotated_hybrid_limits_distinguish_normal_shocks_and_shear():
    for w in [np.array([[1,2,0,1],[2,1,0,2]]),np.array([[1,0,2,1],[2,0,1,1]]),np.array([[1,0,0,1],[2,0,0,1]])]:
        a,b = conserved(w)
        base = 'hlle' if w[0,1] != w[1,1] else 'roe'
        np.testing.assert_allclose(normal_flux(a,b,[1.,0.],'rotated'),old_flux(a,b,0,base),atol=2e-15)


@pytest.mark.parametrize('velocity',[-3.,3.])
def test_tracing_matches_time_integrals_of_frozen_linearized_system(velocity):
    center=np.array([[1.2,velocity,1.]])
    left=center+np.array([[-.1,-.03,-.02]]);right=center+np.array([[.06,.05,.04]])
    dt=.05;gamma=1.4;rho,u,p=center[0]
    matrix=np.array([[u,rho,0],[0,u,1/rho],[0,gamma*p,u]])
    eigenvalues,r=np.linalg.eig(matrix);l=np.linalg.inv(r)
    nodes,weights=leggauss(12);times=.5*dt*(nodes+1)
    side=1 if velocity>0 else -1
    six=6*center[0]-3*(left[0]+right[0]);delta=right[0]-left[0]
    expected=np.zeros(3)
    for k,speed in enumerate(eigenvalues):
        xi=(1 if side==1 else 0)-speed*times
        values=left[0]+xi[:,None]*(delta+(1-xi[:,None])*six)
        mean=.5*np.einsum('i,ij->j',weights,values)
        expected += r[:,k]*(l[k]@mean)
    a,b=trace(center,left,right,dt,gamma)
    np.testing.assert_allclose(b[0] if side==1 else a[0],expected,atol=1e-15)


def test_contact_steepening_preserves_conserved_sums_pressure_and_velocity():
    p=contact_problem();a=solve(p,80,steepening=False);b=solve(p,80)
    initial=p.initial(a.x)
    assert np.mean(abs(b.q[:,0]-initial[:,0])) < .6*np.mean(abs(a.q[:,0]-initial[:,0]))
    for r in (a,b):
        np.testing.assert_allclose(r.q.sum(axis=0),initial.sum(axis=0),atol=4e-12)
        np.testing.assert_allclose(p.equation.primitive(r.q)[:,1:],1,atol=6e-14)
        assert r.flattened_cells==r.rejected_steps==0
    assert a.steepened_cells==0 and b.steepened_cells>0


def test_flattening_is_compressive_pressure_selective_and_smooth_wave_converges():
    p=get_problem('sod');x=p.grid(80);q=p.initial(x)
    # Give the pressure jump a compressive velocity field.
    w=p.equation.primitive(q);w[:40,1]=1
    center,left,right,eta,flat=profiles(p.equation.conserved(w),p)
    assert np.max(flat)==1 and np.max(eta)==0
    w[:40,1]=-1
    assert np.max(profiles(p.equation.conserved(w),p)[-1])==0
    errors=[];p=get_problem('entropy-wave')
    for n in (32,64,128):
        r=solve(p,n,final_time=.2);ref=averaged_state(p,r.x,1/n,.2)
        errors.append(np.mean(abs(r.q[:,0]-ref[:,0])))
        assert r.flattened_cells==0 and r.rejected_steps==0
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>1.9


def test_conforming_mesh_metrics_free_stream_wall_and_global_flux_budget():
    mesh=geometry(8);sr,st=mesh['sr'],mesh['st'];nr,nt=mesh['volume'].shape
    closure=(sr[1:]-sr[:-1])[...,None]*mesh['radial']+st[:,1:,None]*mesh['angular'][1:]-st[:,:-1,None]*mesh['angular'][:-1]
    np.testing.assert_allclose(closure,0,atol=4e-16)
    far=conserved([1.4,6,0,1]);q=np.broadcast_to(far,(nr,nt,4)).copy()
    rate,_,_=rhs(q,mesh,far,wall=False)
    np.testing.assert_allclose(rate,0,atol=2e-12)
    ghost=reflect(q[0],mesh['radial'])
    w,wr=primitive(q[0]),primitive(ghost)
    np.testing.assert_allclose(np.sum(w[:,1:3]*mesh['radial'],axis=-1),-np.sum(wr[:,1:3]*mesh['radial'],axis=-1),atol=3e-15)
    for method in ('roe','hlle','ausm-up','rotated'):
        f=normal_flux(ghost,q[0],mesh['radial'],method)
        np.testing.assert_allclose(f[:,[0,3]],0,atol=1e-12)
        r=solve_blunt(8,solver=method,final_time=.05)
        assert r.q.shape==(8,16,4) and r.rejected_steps==0
        np.testing.assert_allclose(r.conservation_residual,0,atol=2e-12)
    # Normal shock followed by isentropic stagnation, independently via compression.
    m=6.;compression=(GAMMA+1)*m*m/(2+(GAMMA-1)*m*m)
    p2=1.4*m*m+1-1.4*m*m/compression
    m2=(m/compression)/np.sqrt(GAMMA*p2/(1.4*compression))
    np.testing.assert_allclose(stagnation_pressure(),p2*(1+.2*m2*m2)**3.5)


def test_failure_retains_last_admissible_state_and_actual_time():
    from numart.ppm_traced import IntegrationFailure
    from numart.benchmarks import Problem
    from numart.reference_solutions import riemann_reference
    ref=riemann_reference('euler',(1,0,1000),(1,0,.01),final_time=.01)
    p=Problem('strong',Euler(),(0,1),.01,'outflow',lambda x:ref.point(x,0),lambda x,t:ref.point(x,t))
    with pytest.raises(IntegrationFailure) as caught:
        solve(p,40,steepening=False,flattening=True,riemann='ausm-plus')
    r=caught.value.result
    assert 0 < r.time < p.final_time and r.steps > 0 and r.rejected_steps >= 14
    assert np.all(p.equation.primitive(r.q)[:,[0,2]]>0)


def test_published_forebody_fields_reproduce_recorded_diagnostics():
    import json
    from pathlib import Path
    folder=Path(__file__).resolve().parents[1]/'docs/figures/shock-expansion'
    data=json.loads((folder/'shock-expansion.json').read_text())
    with np.load(folder/'fields.npz') as arrays:
        for run in data['body_runs']:
            q=arrays[run['id']];volume=arrays[f"mesh-{run['nr']}-volume"]
            assert q.shape==tuple(run['shape'])+(4,)
            w=primitive(q);rho=w[...,0]
            defect=np.sqrt(np.sum(volume*(rho-rho[:,::-1])**2)/volume.sum())/1.4
            np.testing.assert_allclose(defect,run['metrics']['final_symmetry_defect'],atol=1e-16)
            assert w[...,0].min()>=run['metrics']['minimum_density']-1e-12
            assert w[...,3].min()>=run['metrics']['minimum_pressure']-1e-12
            np.testing.assert_allclose(run['metrics']['conservation_residual'],0,atol=2e-9)
        for entry in data['flux_cases']:
            if entry['status']=='failed':
                q=arrays[entry['problem']+'-'+entry['config']]
                np.testing.assert_allclose(Euler().primitive(q),entry['primitive'],atol=1e-12)
