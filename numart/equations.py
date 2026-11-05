"""Conserved variables on the last axis. Invalid states fail explicitly."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Euler:
    gamma: float = 1.4
    name: str = "euler"

    def conserved(self, w):
        r, v, p = np.moveaxis(np.asarray(w), -1, 0)
        return np.stack((r, r*v, p/(self.gamma-1) + 0.5*r*v*v), axis=-1)

    def primitive(self, q):
        r, m, e = np.moveaxis(np.asarray(q), -1, 0)
        if not np.all(np.isfinite(q)) or np.any(r <= 0):
            raise ValueError("Nonfinite state or nonpositive density")
        v = m/r
        p = (self.gamma-1)*(e-0.5*m*v)
        if np.any(p <= 0):
            raise ValueError("Nonpositive pressure; reduce CFL or change method")
        return np.stack((r, v, p), axis=-1)

    def flux(self, q):
        r, v, p = np.moveaxis(self.primitive(q), -1, 0)
        return np.stack((r*v, r*v*v+p, v*(q[..., 2]+p)), axis=-1)

    def speeds(self, q):
        r, v, p = np.moveaxis(self.primitive(q), -1, 0)
        c = np.sqrt(self.gamma*p/r)
        return v-c, v+c


@dataclass(frozen=True)
class Barotropic:
    """Flat-bottom shallow water or isothermal Euler; strictly positive depth/rho.

    SWE: q=(h,hu), p=gh²/2. Isothermal: q=(rho,rho*u), p=cs²*rho.
    No energy equation is advanced for either model.
    """
    name: str = "shallow-water"
    gravity: float = 1.0
    sound_speed: float = 1.0

    def conserved(self, w):
        w = np.asarray(w)
        return np.stack((w[..., 0], w[..., 0]*w[..., 1]), axis=-1)

    def primitive(self, q):
        if not np.all(np.isfinite(q)) or np.any(q[..., 0] <= 0):
            raise ValueError("This baseline requires strictly positive depth/density")
        return np.stack((q[..., 0], q[..., 1]/q[..., 0]), axis=-1)

    def pressure(self, r):
        return 0.5*self.gravity*r*r if self.name == "shallow-water" else self.sound_speed**2*r

    def flux(self, q):
        r, v = np.moveaxis(self.primitive(q), -1, 0)
        return np.stack((r*v, r*v*v+self.pressure(r)), axis=-1)

    def speeds(self, q):
        r, v = np.moveaxis(self.primitive(q), -1, 0)
        c = np.sqrt(self.gravity*r) if self.name == "shallow-water" else self.sound_speed
        return v-c, v+c
