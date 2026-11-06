"""Render 2D fields and slices of a 3D solve using existing tested solvers."""
from pathlib import Path
import hashlib
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart.fem import poisson_2d, error_norms
from numart.incompressible import taylor_green, divergence
from numart.particle_gravity import periodic_poisson

OUT = ROOT / 'docs/figures'
OUT.mkdir(parents=True, exist_ok=True)


def finish(fig, name):
    fig.savefig(OUT / name, dpi=150, facecolor='white')
    plt.close(fig)


exact = lambda p: np.sin(np.pi*p[:, 0])*np.sin(np.pi*p[:, 1])
gradient = lambda p: np.pi*np.column_stack((
    np.cos(np.pi*p[:, 0])*np.sin(np.pi*p[:, 1]),
    np.sin(np.pi*p[:, 0])*np.cos(np.pi*p[:, 1])))
fem = poisson_2d(24)
l2, h1 = error_norms(fem, exact, gradient)
mesh = mtri.Triangulation(fem.points[:, 0], fem.points[:, 1], fem.cells)
nodal_error = fem.u-exact(fem.points)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), layout='constrained')
for ax, values, title, cmap in zip(axes, (fem.u, nodal_error),
        ('Computed P1 solution', 'Nodal error (not the continuous L2 norm)'), ('viridis', 'RdBu_r')):
    image = ax.tripcolor(mesh, values, shading='gouraud', cmap=cmap)
    ax.triplot(mesh, color='black', linewidth=.15, alpha=.22)
    fig.colorbar(image, ax=ax, shrink=.85)
    ax.set(title=title, xlabel='x', ylabel='y', aspect='equal')
fig.suptitle('2D Poisson | 24 x 24 squares / 1152 triangles / zero Dirichlet\n'
             f'Inside-element L2 error = {l2:.3e}; H1 seminorm error = {h1:.3e}', fontsize=11)
finish(fig, 'field-fem-poisson.png')

flow = taylor_green(64, final_time=.5, viscosity=.1)
# Interpolate native MAC face velocities to cell centers only for display.
uc = .5*(flow['u']+np.roll(flow['u'], -1, axis=0))
vc = .5*(flow['v']+np.roll(flow['v'], -1, axis=1))
speed = np.hypot(uc, vc)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), layout='constrained')
centers = (np.arange(64)+.5)*flow['h']
xx, yy = np.meshgrid(centers, centers, indexing='ij')
for ax, values, title, cmap in zip(axes, (speed, flow['pressure']),
        ('Speed | face velocities averaged to centers', 'Pressure | zero-mean discrete Poisson'), ('viridis', 'RdBu_r')):
    image = ax.imshow(values.T, origin='lower', extent=(0, 2*np.pi, 0, 2*np.pi), cmap=cmap)
    fig.colorbar(image, ax=ax, shrink=.85)
    ax.set(title=title, xlabel='x', ylabel='y')
axes[0].quiver(xx[::4, ::4], yy[::4, ::4], uc[::4, ::4], vc[::4, ::4], color='white', alpha=.8)
divmax = float(np.max(abs(divergence(flow['u'], flow['v'], flow['h']))))
fig.suptitle('2D Taylor-Green | periodic MAC / SSPRK2 / 64 x 64 / t = 0.5 / viscosity = 0.1\n'
             f'Native-face velocity RMS error = {flow["error"]:.3e}; max |D u| = {divmax:.3e}', fontsize=11)
finish(fig, 'field-taylor-green.png')

n = 32
coordinates = np.arange(n)/n
x, y, z = np.meshgrid(coordinates, coordinates, coordinates, indexing='ij')
mode = np.cos(2*np.pi*x)*np.cos(4*np.pi*y)*np.cos(2*np.pi*z)
rho = 1+.3*mode
potential, acceleration = periodic_poisson(rho)
reference = -4*np.pi*.3 / ((2*np.pi)**2*6)*mode
potential_error = float(np.max(abs(potential-reference)))
assert potential_error < 1e-12
fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), layout='constrained')
bound = float(np.max(abs(reference)))
planes = (potential[:, :, n//2], potential[:, n//2, :], potential[n//2, :, :])
for ax, values, labels, title in zip(axes, planes, (('x', 'y'), ('x', 'z'), ('y', 'z')),
        ('z = 0.5', 'y = 0.5', 'x = 0.5')):
    image = ax.imshow(values.T, origin='lower', extent=(-.5/n, 1-.5/n, -.5/n, 1-.5/n),
                      vmin=-bound, vmax=bound, cmap='RdBu_r')
    ax.set(title=title, xlabel=labels[0], ylabel=labels[1])
fig.colorbar(image, ax=axes, shrink=.72, label='Potential (same scale in all slices)')
fig.suptitle('3D periodic Poisson | 32 cubed mesh | three orthogonal slices\n'
             f'Laplacian(phi) = 4 pi (rho - mean rho); max point error = {potential_error:.3e}', fontsize=11)
finish(fig, 'field-poisson-3d.png')

arrays = OUT / 'multidimensional-fields.npz'
np.savez_compressed(arrays, fem_points=fem.points, fem_cells=fem.cells, fem_u=fem.u,
    fem_nodal_error=nodal_error, mac_u=flow['u'], mac_v=flow['v'], mac_pressure=flow['pressure'],
    poisson3d_rho=rho, poisson3d_potential=potential, poisson3d_reference=reference)

sources = ['scripts/build_multidimensional_gallery.py', 'numart/fem.py', 'numart/krylov.py',
           'numart/incompressible.py', 'numart/particle_gravity.py']
names = ['field-fem-poisson.png', 'field-taylor-green.png', 'field-poisson-3d.png', arrays.name]
manifest = dict(
    scope='New views of existing educational solvers. No new solver or 3D fluid evolution. '
          'One resolution per exhibit; the 3D spectral single-mode check is not a general convergence study.',
    fem=dict(dimension=2, subdivisions=24, triangles=len(fem.cells), l2=l2, h1_seminorm=h1,
             residual=fem.residual, boundary='zero Dirichlet', exact='sin(pi*x)*sin(pi*y)'),
    mac=dict(dimension=2, shape=[64, 64], time=flow['time'], viscosity=.1,
             velocity_rms=flow['error'], max_native_divergence=divmax,
             boundary='periodic', display='face velocities averaged to cell centers'),
    poisson3d=dict(dimension=3, shape=[n, n, n], boundary='periodic', gravity=1.,
                   density='1 + 0.3*cos(2*pi*x)*cos(4*pi*y)*cos(2*pi*z)',
                   potential_gauge='zero mean', maximum_point_error=potential_error,
                   display='x/y/z = 0.5 slices; static field, no particle evolution'),
    source_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
    artifact_sha256={p: hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in names})
assert l2 < .01 and flow['error'] < .01 and divmax < 1e-10
for values in (fem.u, flow['u'], flow['v'], flow['pressure'], potential):
    assert np.all(np.isfinite(values))
(OUT/'multidimensional-fields.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({k: manifest[k] for k in ('fem', 'mac', 'poisson3d')}, indent=2))
