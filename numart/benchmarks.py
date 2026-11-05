"""Reusable test definitions. The exact parameter choices are documented here."""
from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np
from .equations import Euler, Barotropic
from .riemann import exact_euler


@dataclass(frozen=True)
class Problem:
    name: str
    equation: object
    domain: tuple
    final_time: float
    boundary: str
    initial: Callable
    reference: Optional[Callable] = None
    citation: str = ""

    def grid(self, n):
        if n < 8:
            raise ValueError("At least eight grid points/cells required")
        a, b = self.domain
        return a+(np.arange(n)+.5)*(b-a)/n


def _tube(name, left, right, domain, x0, time, citation):
    eq = Euler()
    def initial(x):
        return eq.conserved(np.where((x < x0)[..., None], left, right))
    def reference(x, t):
        return initial(x) if t == 0 else eq.conserved(exact_euler((x-x0)/t, left, right))
    return Problem(name, eq, domain, time, "outflow", initial, reference, citation)


def list_problems():
    return ("sod", "lax", "shu-osher", "entropy-wave", "dam-break", "isothermal", "double-rarefaction")


def get_problem(name):
    if name == "sod":
        return _tube(name, (1.,0.,1.), (.125,0.,.1), (0.,1.), .5, .2, "sod1978")
    if name == "lax":
        return _tube(name, (.445,.698,3.528), (.5,0.,.571), (-5.,5.), 0., 1.3, "lax1954; shu1989")
    if name == "double-rarefaction":
        return _tube(name,(1.,-2.,.4),(1.,2.,.4),(0.,1.),.5,.15,"einfeldt1991; toro2009")
    if name == "shu-osher":
        eq = Euler()
        def initial(x):
            w = np.stack((1+.2*np.sin(5*x), np.zeros_like(x), np.ones_like(x)), axis=-1)
            w[x < -4] = (3.857143, 2.629369, 10.33333)
            return eq.conserved(w)
        return Problem(name, eq, (-5.,5.), 1.8, "fixed", initial, citation="shu1989; quokka2022")
    if name == "entropy-wave":
        eq = Euler()
        def reference(x, t):
            return eq.conserved(np.stack((1+.2*np.sin(2*np.pi*(x-t)), np.ones_like(x), np.ones_like(x)), axis=-1))
        return Problem(name, eq, (0.,1.), 1., "periodic", lambda x: reference(x,0), reference, "jiang1996")
    if name in ("dam-break", "isothermal"):
        eq = Barotropic("shallow-water" if name == "dam-break" else "isothermal")
        def initial(x):
            return eq.conserved(np.stack((np.where(x < .5, 2. if name == "dam-break" else 1., 1. if name == "dam-break" else .125), np.zeros_like(x)), axis=-1))
        return Problem(name, eq, (0.,1.), .1, "outflow", initial, citation="leveque2002")
    raise ValueError(f"Unknown problem {name!r}; choose from {list_problems()}")
