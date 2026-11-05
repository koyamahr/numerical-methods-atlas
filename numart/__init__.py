"""Small, inspectable numerical methods; see docs/references.md for sources."""
from .benchmarks import get_problem, list_problems
from .solvers import solve

__all__ = ["get_problem", "list_problems", "solve"]
