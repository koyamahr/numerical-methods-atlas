"""Inspectable sparse assembly, Krylov methods, and damped Newton iteration.

NumPy-only reference implementations; real arithmetic, fixed right
preconditioners in GMRES/BiCGSTAB, and explicit true-residual stopping tests.
See docs/sparse-nonlinear.md for scope and sources.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class CSR:
    indptr: np.ndarray
    indices: np.ndarray
    data: np.ndarray
    shape: tuple

    @classmethod
    def from_coo(cls, rows, cols, values, shape):
        if len(rows) != len(cols) or len(rows) != len(values):
            raise ValueError("COO arrays must have matching lengths")
        entries = [dict() for _ in range(shape[0])]
        for i, j, value in zip(rows, cols, values):
            if not 0 <= i < shape[0] or not 0 <= j < shape[1] or not np.isfinite(value):
                raise ValueError("Invalid COO entry")
            entries[i][j] = entries[i].get(j, 0.) + float(value)
        ptr, indices, data = [0], [], []
        for row in entries:
            for j, value in sorted(row.items()):
                # Keep structural zeros: ILU(0) uses the supplied sparsity.
                indices.append(j)
                data.append(value)
            ptr.append(len(data))
        return cls(np.array(ptr), np.array(indices, dtype=int), np.array(data), tuple(shape))

    def matvec(self, x):
        x = np.asarray(x, dtype=float)
        if x.shape != (self.shape[1],):
            raise ValueError("Matrix/vector size mismatch")
        result = np.empty(self.shape[0])
        for i in range(self.shape[0]):
            a, b = self.indptr[i:i+2]
            result[i] = self.data[a:b] @ x[self.indices[a:b]]
        return result

    def diagonal(self):
        result = np.zeros(min(self.shape))
        for i in range(len(result)):
            a, b = self.indptr[i:i+2]
            where = self.indices[a:b] == i
            result[i] = self.data[a:b][where].sum()
        return result

    def to_dense(self):
        result = np.zeros(self.shape)
        for i in range(self.shape[0]):
            a, b = self.indptr[i:i+2]
            result[i, self.indices[a:b]] = self.data[a:b]
        return result


def apply(a, x):
    return a.matvec(x) if isinstance(a, CSR) else a(x) if callable(a) else np.einsum("ij,j->i", np.asarray(a), x)


def jacobi_preconditioner(a):
    d = a.diagonal() if isinstance(a, CSR) else np.diag(a)
    if np.any(abs(d) <= np.finfo(float).eps * max(1., np.max(abs(d)))):
        raise np.linalg.LinAlgError("Jacobi preconditioner has a zero/tiny diagonal")
    return lambda x: np.asarray(x) / d


def ilu0_preconditioner(a):
    """Unpivoted ILU(0): no fill outside the CSR structure, no permutations."""
    if not isinstance(a, CSR) or a.shape[0] != a.shape[1]:
        raise ValueError("ILU(0) requires square CSR input")
    n = a.shape[0]
    rows = []
    for i in range(n):
        lo, hi = a.indptr[i:i+2]
        rows.append(dict(zip(a.indices[lo:hi], a.data[lo:hi])))
    threshold = np.finfo(float).eps * max(1., max(abs(a.data), default=0.))
    for i, row in enumerate(rows):
        for j in sorted(k for k in row if k < i):
            pivot = rows[j].get(j, 0.)
            if abs(pivot) <= threshold:
                raise np.linalg.LinAlgError("ILU(0) zero/tiny pivot; reorder or change preconditioner")
            row[j] /= pivot
            for k, value in rows[j].items():
                if k > j and k in row:
                    row[k] -= row[j] * value
        if abs(row.get(i, 0.)) <= threshold:
            raise np.linalg.LinAlgError("ILU(0) zero/tiny pivot")

    def solve(rhs):
        y = np.array(rhs, dtype=float, copy=True)
        for i, row in enumerate(rows):
            y[i] -= sum(value*y[j] for j, value in row.items() if j < i)
        for i in range(n-1, -1, -1):
            y[i] = (y[i]-sum(value*y[j] for j, value in rows[i].items() if j > i))/rows[i][i]
        return y
    return solve


@dataclass
class KrylovResult:
    x: np.ndarray
    residuals: np.ndarray
    iterations: int
    converged: bool
    reason: str


def _start(b, x0, rtol, atol, maxiter):
    b = np.asarray(b, dtype=float)
    if b.ndim != 1 or not np.all(np.isfinite(b)) or rtol <= 0 or atol < 0 or maxiter < 1:
        raise ValueError("Finite vector, rtol>0, atol>=0 and maxiter>=1 required")
    x = np.zeros_like(b) if x0 is None else np.array(x0, dtype=float, copy=True)
    if x.shape != b.shape or not np.all(np.isfinite(x)):
        raise ValueError("Invalid initial iterate")
    return b, x, max(atol, rtol*np.linalg.norm(b))


def gmres(a, b, x0=None, preconditioner=None, restart=30, maxiter=500, rtol=1e-10, atol=0.):
    """Restarted, fixed-right-preconditioned GMRES with reorthogonalization.

    Small Hessenberg least squares use NumPy QR/SVD machinery. This reference
    implementation recomputes the true residual every iteration for teaching.
    """
    b, x, target = _start(b, x0, rtol, atol, maxiter)
    if restart < 1:
        raise ValueError("restart must be positive")
    pre = preconditioner or (lambda v: v.copy())
    history = [np.linalg.norm(b-apply(a, x))]
    iterations = 0
    while history[-1] > target and iterations < maxiter:
        residual = b-apply(a, x)
        beta = np.linalg.norm(residual)
        m = min(restart, maxiter-iterations, len(b))
        basis = np.zeros((len(b), m+1))
        z = np.zeros((len(b), m))
        h = np.zeros((m+1, m))
        basis[:, 0] = residual/beta
        start = x.copy()
        for j in range(m):
            z[:, j] = pre(basis[:, j])
            w = apply(a, z[:, j])
            for _ in range(2):
                coefficients = np.einsum("ij,i->j", basis[:, :j+1], w)
                h[:j+1, j] += coefficients
                w -= np.einsum("ij,j->i", basis[:, :j+1], coefficients)
            h[j+1, j] = np.linalg.norm(w)
            breakdown = h[j+1, j] <= 1e-14 * max(1., np.linalg.norm(h[:j+1, j]))
            if not breakdown:
                basis[:, j+1] = w/h[j+1, j]
            rhs = np.zeros(j+2)
            rhs[0] = beta
            coefficients = np.linalg.lstsq(h[:j+2, :j+1], rhs, rcond=None)[0]
            x = start+np.einsum("ij,j->i", z[:, :j+1], coefficients)
            history.append(np.linalg.norm(b-apply(a, x)))
            iterations += 1
            if not np.isfinite(history[-1]):
                return KrylovResult(x, np.array(history), iterations, False, "nonfinite residual")
            if history[-1] <= target:
                break
            if breakdown:
                return KrylovResult(x, np.array(history), iterations, False, "Arnoldi breakdown before convergence")
    ok = history[-1] <= target
    return KrylovResult(x, np.array(history), iterations, ok, "true residual tolerance" if ok else "iteration limit")


def bicgstab(a, b, x0=None, preconditioner=None, maxiter=500, rtol=1e-10, atol=0.):
    """BiCGSTAB with fixed right preconditioning and true residual checks."""
    b, x, target = _start(b, x0, rtol, atol, maxiter)
    pre = preconditioner or (lambda v: v.copy())
    r = b-apply(a, x)
    shadow = r.copy()
    p, v = np.zeros_like(b), np.zeros_like(b)
    rho_old, alpha, omega = 1., 1., 1.
    history = [np.linalg.norm(r)]
    if history[-1] <= target:
        return KrylovResult(x, np.array(history), 0, True, "true residual tolerance")
    tiny = np.finfo(float).tiny
    for k in range(1, maxiter+1):
        rho = shadow @ r
        if abs(rho) <= tiny or abs(omega) <= tiny:
            return KrylovResult(x, np.array(history), k-1, False, "BiCGSTAB rho/omega breakdown")
        p = r+(rho/rho_old)*(alpha/omega)*(p-omega*v)
        phat = pre(p)
        v = apply(a, phat)
        denominator = shadow @ v
        if abs(denominator) <= tiny:
            return KrylovResult(x, np.array(history), k-1, False, "BiCGSTAB alpha breakdown")
        alpha = rho/denominator
        s = r-alpha*v
        trial = x+alpha*phat
        if np.linalg.norm(b-apply(a, trial)) <= target:
            history.append(np.linalg.norm(b-apply(a, trial)))
            return KrylovResult(trial, np.array(history), k, True, "true residual tolerance")
        shat = pre(s)
        t = apply(a, shat)
        tt = t @ t
        if tt <= tiny:
            return KrylovResult(x, np.array(history), k-1, False, "BiCGSTAB t breakdown")
        omega = (t @ s)/tt
        x = trial+omega*shat
        r = s-omega*t
        history.append(np.linalg.norm(b-apply(a, x)))
        if not np.isfinite(history[-1]):
            return KrylovResult(x, np.array(history), k, False, "nonfinite residual")
        if history[-1] <= target:
            return KrylovResult(x, np.array(history), k, True, "true residual tolerance")
        rho_old = rho
    return KrylovResult(x, np.array(history), maxiter, False, "iteration limit")


@dataclass
class NewtonResult:
    x: np.ndarray
    residuals: np.ndarray
    step_lengths: np.ndarray
    converged: bool
    reason: str


def newton(function, jacobian, x0, tolerance=1e-10, maxiter=30, linear_solver="dense"):
    """Armijo-damped Newton; GMRES option gives a small Newton–Krylov model."""
    if tolerance <= 0 or maxiter < 1 or linear_solver not in ("dense", "gmres"):
        raise ValueError("Invalid Newton controls")
    x = np.array(x0, dtype=float, copy=True)
    history, lengths = [], []
    for _ in range(maxiter+1):
        f = np.asarray(function(x))
        norm = np.linalg.norm(f)
        history.append(norm)
        if np.isfinite(norm) and norm <= tolerance:
            return NewtonResult(x, np.array(history), np.array(lengths), True, "residual tolerance")
        if not np.isfinite(norm) or len(lengths) == maxiter:
            break
        j = jacobian(x)
        if linear_solver == "dense":
            step = np.linalg.solve(j.to_dense() if isinstance(j, CSR) else j, -f)
        else:
            pre = ilu0_preconditioner(j) if isinstance(j, CSR) else jacobi_preconditioner(j)
            result = gmres(j, -f, preconditioner=pre, rtol=min(1e-4, .1*tolerance/max(norm, tolerance)), maxiter=300)
            if not result.converged:
                return NewtonResult(x, np.array(history), np.array(lengths), False, "inner GMRES: "+result.reason)
            step = result.x
        length = 1.
        while length >= 2**-20:
            candidate = x+length*step
            candidate_norm = np.linalg.norm(function(candidate))
            if np.isfinite(candidate_norm) and candidate_norm <= (1-1e-4*length)*norm:
                x = candidate
                lengths.append(length)
                break
            length *= .5
        else:
            return NewtonResult(x, np.array(history), np.array(lengths), False, "line search failed")
    return NewtonResult(x, np.array(history), np.array(lengths), False, "nonfinite residual or iteration limit")


def advection_diffusion_matrix(n=20, diffusion=.02, velocity=(1., .5)):
    """5-point diffusion + first-order upwind advection; zero Dirichlet square."""
    if n < 2 or diffusion <= 0:
        raise ValueError("n>=2 and diffusion>0 required")
    h = 1/(n+1)
    rows, cols, values = [], [], []
    for i in range(n):
        for j in range(n):
            index = i*n+j
            rows.append(index); cols.append(index)
            values.append(4*diffusion/h**2+(abs(velocity[0])+abs(velocity[1]))/h)
            for axis, speed in enumerate(velocity):
                for sign in (-1, 1):
                    neighbor = [i, j]
                    neighbor[axis] += sign
                    if 0 <= neighbor[axis] < n:
                        rows.append(index); cols.append(neighbor[0]*n+neighbor[1])
                        values.append(-diffusion/h**2-max(-sign*speed, 0.)/h)
    return CSR.from_coo(rows, cols, values, (n*n, n*n))
