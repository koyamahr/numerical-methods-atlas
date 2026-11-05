"""Read-only snapshots of existing adaptive-CFL trajectories.

Output requests never shorten a solver step. A frame is the first completed
state at or after the requested time; several requests crossed by one step
produce one frame. Actual physical times and solver step counts are retained.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class Snapshot:
    time: float
    step: int
    q: np.ndarray
    diagnostics: dict


class SnapshotRecorder:
    def __init__(self,times,final_time):
        self.frames=[];self.next=0
        self.times=np.asarray([] if times is None else times,dtype=float)
        if (self.times.ndim!=1 or not np.all(np.isfinite(self.times))
                or np.any(self.times<0) or np.any(self.times>final_time)
                or np.any(np.diff(self.times)<=0)):
            raise ValueError('Snapshot times must be finite, strictly increasing and within the run')

    def capture(self,time,step,q,diagnostics=None):
        if self.next==len(self.times) or time<self.times[self.next]:return
        while self.next<len(self.times) and self.times[self.next]<=time:self.next+=1
        self.frames.append(Snapshot(float(time),int(step),q.copy(),dict(diagnostics or {})))
