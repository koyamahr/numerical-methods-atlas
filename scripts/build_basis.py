"""Computed reference-element bases, exact/lumped matrices and approximations."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from numpy.polynomial import legendre as lp
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart.basis import (legendre, lobatto, interval_basis, element_matrices,
                          project_legendre, triangle_lagrange)

x = np.linspace(-1, 1, 501)
cases = []
for p in (1, 2, 3, 4, 6, 8):
    nodes, weights = lobatto(p)
    for kind in ('legendre', 'orthonormal', 'chebyshev', 'gll', 'equispaced'):
        b = interval_basis(x, p, kind)
        m, k = element_matrices(p, kind)
        lump, _ = element_matrices(p, kind, quadrature='gll')
        cases.append(dict(degree=p, kind=kind, values=b.tolist(), mass=m.tolist(),
                          stiffness=k.tolist(), quadrature_mass=lump.tolist(),
                          nodes=(nodes if kind == 'gll' else np.linspace(-1, 1, p+1)).tolist()
                                if kind in ('gll', 'equispaced') else None,
                          mass_difference_norm=float(np.linalg.norm(m-lump)),
                          nodal_vandermonde_condition=float(np.linalg.cond(legendre(
                              nodes if kind == 'gll' else np.linspace(-1, 1, p+1), p)))
                                if kind in ('gll', 'equispaced') else None))

approximations = []
qx, qw = lp.leggauss(80)
for p in (1, 2, 3, 4, 6, 8):
    z, _ = lobatto(p)
    for profile in ('smooth', 'jump'):
        fn = np.exp if profile == 'smooth' else np.sign
        if profile == 'smooth':
            modal = project_legendre(fn, p, 80)
        else:
            # Split at zero; no quadrature straddles the discontinuity.
            modal = np.einsum('qk,q->k', legendre((qx+1)/2, p)-legendre((qx-1)/2, p), qw)/2
            modal *= (2*np.arange(p+1)+1)/2
        projected = np.einsum('qk,k->q', legendre(x, p), modal)
        interpolated = np.einsum('qk,k->q', interval_basis(x, p, 'gll'), fn(z))
        errors = []
        for kind in ('projection', 'interpolation'):
            total = 0.
            for side in (-1, 1):
                points = (qx+side)/2
                approx = np.einsum('qk,k->q', legendre(points, p), modal) if kind == 'projection' else np.einsum('qk,k->q', interval_basis(points, p, 'gll'), fn(z))
                total += .5*qw@((approx-fn(points))**2)
            errors.append(float(np.sqrt(total)))
        approximations.append(dict(degree=p, profile=profile, modal=modal.tolist(),
                                   projected=projected.tolist(), interpolated=interpolated.tolist(),
                                   exact=fn(x).tolist(), projection_l2=errors[0], interpolation_l2=errors[1]))

# Triangle P2 nodal functions, sampled on a genuine simplex, not a square.
n = 16
xy = np.array([(i/n, j/n) for j in range(n+1) for i in range(n+1-j)])
index = {(i, j): k for k, (i, j) in enumerate((i, j) for j in range(n+1) for i in range(n+1-j))}
cells = []
for j in range(n):
    for i in range(n-j):
        cells.append([index[i, j], index[i+1, j], index[i, j+1]])
        if i+j < n-1:
            cells.append([index[i+1, j], index[i+1, j+1], index[i, j+1]])
triangle = dict(points=xy.tolist(), cells=cells, values=triangle_lagrange(xy, 2).tolist(),
                nodes=[[0, 0], [1, 0], [0, 1], [.5, 0], [.5, .5], [0, .5]])

source_files = ['numart/basis.py', 'scripts/build_basis.py']
data = dict(x=x.tolist(), cases=cases, approximations=approximations, triangle=triangle,
            source_sha256={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_files},
            scope='Reference-element polynomial algebra only. Unit weight on [-1,1] for interval matrices; affine physical mapping in source. No new FEM/DG flow solver. Jump projection integrals split at zero; jump interpolation uses sign(0)=0.')
out = ROOT/'docs/figures'
(out/'basis.json').write_text(json.dumps(data, separators=(',', ':'), allow_nan=False)+'\n')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 3, figsize=(13, 7))
for k in range(5):
    axs[0, 0].plot(x, legendre(x, 4)[:, k], label=f'P{k}')
axs[0, 0].set(title='Legendre modal basis | unit weight', xlabel='reference coordinate'); axs[0, 0].legend(fontsize=7)
c = next(c for c in cases if c['degree'] == 4 and c['kind'] == 'gll')
for k in range(5): axs[0, 1].plot(x, np.array(c['values'])[:, k])
axs[0, 1].plot(c['nodes'], np.ones(5), 'ko', ms=3)
axs[0, 1].set(title='GLL Lagrange nodal basis | p=4', xlabel='reference coordinate')
im = axs[0, 2].imshow(c['mass'], cmap='RdBu_r', vmin=-.7, vmax=.7)
axs[0, 2].set(title='Exact nodal mass | not diagonal', xlabel='basis j', ylabel='basis i'); fig.colorbar(im, ax=axs[0, 2])
for ax, profile in zip(axs[1, :2], ('smooth', 'jump')):
    a = next(a for a in approximations if a['degree'] == 6 and a['profile'] == profile)
    ax.plot(x, a['exact'], 'k--', label='exp(x)' if profile == 'smooth' else 'sign(x)')
    ax.plot(x, a['projected'], color='#bf5b35', label='L2 projection')
    ax.plot(x, a['interpolated'], color='#687fad', label='GLL interpolation')
    ax.set(title=f'{profile} profile | p=6', xlabel='reference coordinate'); ax.legend(fontsize=7)
from matplotlib.tri import Triangulation
tri = Triangulation(xy[:, 0], xy[:, 1], np.array(cells))
im = axs[1, 2].tripcolor(tri, np.array(triangle['values'])[:, 3], shading='gouraud', cmap='RdBu_r', vmin=-1, vmax=1)
axs[1, 2].plot(*np.array(triangle['nodes']).T, 'ko', ms=4)
axs[1, 2].set(title='Triangle P2 edge function | 4λ0λ1', aspect='equal'); fig.colorbar(im, ax=axs[1, 2])
fig.suptitle('Mesh-local bases | modes, nodes, quadrature and element shape')
fig.tight_layout(); fig.savefig(out/'basis.png', dpi=140, bbox_inches='tight'); plt.close(fig)
print('Generated 30 basis cases, 12 projection/interpolation pairs, and a triangular P2 exhibit.')
