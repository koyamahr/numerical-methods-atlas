import numpy as np
import pytest
from numart.snapshots import SnapshotRecorder
from numart.euler2d import solve_double_mach
from numart.mhd import solve_orszag_tang


def test_snapshot_requests_do_not_change_euler_trajectory_and_own_their_data():
    plain=solve_double_mach(8,.01)
    times=np.linspace(0,.01,7)
    sampled=solve_double_mach(8,.01,snapshot_times=times)
    np.testing.assert_array_equal(sampled.q,plain.q)
    assert sampled.steps==plain.steps
    frames=sampled.snapshots
    assert frames[0].time==0 and frames[-1].time==.01
    assert all(a.time<b.time and a.step<b.step for a,b in zip(frames,frames[1:]))
    np.testing.assert_array_equal(frames[-1].q,sampled.q)
    frames[-1].q[:]=0
    assert sampled.q[...,0].min()>0


@pytest.mark.parametrize('method',['ct','glm'])
def test_snapshot_requests_do_not_change_mhd_trajectory_or_divergence(method):
    plain=solve_orszag_tang(8,.02,method)
    sampled=solve_orszag_tang(8,.02,method,snapshot_times=[0,.007,.02])
    np.testing.assert_array_equal(sampled.q,plain.q)
    np.testing.assert_array_equal(sampled.history,plain.history)
    assert sampled.snapshots[-1].time==.02
    assert sampled.snapshots[-1].diagnostics['max_abs_divB']==float(abs(sampled.divergence).max())


def test_coarse_steps_coalesce_crossed_requests_and_record_actual_time():
    recorder=SnapshotRecorder([0,.01,.02,.03,.04],.04)
    state=np.ones((3,3))
    recorder.capture(0,0,state)
    recorder.capture(.025,1,state)
    recorder.capture(.04,2,state)
    assert [f.time for f in recorder.frames]==[0,.025,.04]
    state[:]=0
    np.testing.assert_array_equal(recorder.frames[0].q,1)


@pytest.mark.parametrize('times',[[.2,.1],[0,0],[-.1],[float('nan')],[.6]])
def test_invalid_snapshot_schedules_fail(times):
    with pytest.raises(ValueError):SnapshotRecorder(times,.5)
