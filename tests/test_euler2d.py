import numpy as np
from numart.euler2d import (conserved,primitive,physical_flux,hll_flux,double_mach_states,
    double_mach_initial,double_mach_ghost,solve_double_mach)


def test_2d_flux_consistency_and_uniform_periodic_balance():
    q=conserved(np.array([[1.3,.7,-.4,1.2],[.9,-.2,.3,.8]]))
    for axis in (0,1):np.testing.assert_allclose(hll_flux(q,q,axis),physical_flux(q,axis))
    state=conserved([1.2,.3,-.2,.7]);grid=np.tile(state,(9,7,1))
    rhs=np.zeros_like(grid)
    for axis in (0,1):
        f=hll_flux(grid,np.roll(grid,-1,axis=axis),axis)
        rhs-=f-np.roll(f,1,axis=axis)
    np.testing.assert_allclose(rhs,0,atol=1e-14)


def test_double_mach_shock_states_satisfy_rankine_hugoniot():
    hot,cold=double_mach_states();normal=np.array([np.sqrt(3)/2,-.5]);speed=10.
    flux=lambda q:normal[0]*physical_flux(q,0)+normal[1]*physical_flux(q,1)
    np.testing.assert_allclose(flux(hot)-flux(cold),speed*(hot-cold),rtol=2e-14,atol=1e-11)


def test_moving_top_boundary_and_reflecting_wall():
    x,y,q=double_mach_initial(128,32);hot,cold=double_mach_states()
    early=double_mach_ghost(q,0,x);late=double_mach_ghost(q,.1,x)
    assert np.count_nonzero(late[1:-1,-1,0]==8)>np.count_nonzero(early[1:-1,-1,0]==8)
    wall=x>=1/6
    np.testing.assert_allclose(early[1:-1,0,2][wall],-q[:,0,2][wall])
    flux=hll_flux(early[1:-1,0][wall],q[:,0][wall],1)
    np.testing.assert_allclose(flux[:,0],0,atol=1e-14)
    np.testing.assert_allclose(flux[:,3],0,atol=1e-12)


def test_double_mach_selected_small_grid_stays_physical():
    result=solve_double_mach(ny=12,final_time=.03)
    w=primitive(result.q)
    assert w.shape==(48,12,4)
    assert result.steps>1 and result.time==.03
    assert w[...,0].min()>0 and w[...,3].min()>0


def test_double_mach_cli_persists_reproducible_arrays_and_manifest(tmp_path,monkeypatch):
    import hashlib
    import json
    import sys
    from pathlib import Path
    from numart.cli import main
    monkeypatch.setattr(sys,'argv',['numart','run','double-mach','--n','8','--time','0.005',
                                    '--cfl','0.4','--output',str(tmp_path)])
    main()
    data=np.load(tmp_path/'solution.npz')
    manifest=json.loads((tmp_path/'run.json').read_text())
    assert data['q'].shape==(32,8,4)
    assert float(data['time'])==manifest['time']==.005
    assert manifest['shape']==[32,8] and manifest['method']=='godunov'
    w=primitive(data['q'])
    np.testing.assert_allclose(w[...,0].min(),manifest['min_density'])
    np.testing.assert_allclose(w[...,3].min(),manifest['min_pressure'])
    source=Path(__file__).parents[1]/'numart/euler2d.py'
    assert manifest['source_sha256']['euler2d.py']==hashlib.sha256(source.read_bytes()).hexdigest()
    assert (tmp_path/'double-mach.png').read_bytes().startswith(b'\x89PNG')
