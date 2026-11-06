"""Save formula/root-solved references; no numerical PDE trajectory is run."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart.reference_solutions import get_reference, list_references
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = ROOT / 'docs/figures'
cases = []
for id in list_references():
    ref = get_reference(id)
    x = np.linspace(*ref.bounds[0], 401)
    coordinates = x if ref.dimension == 1 else np.column_stack((x, np.full_like(x, np.pi/4)))
    frames = []
    for t in np.linspace(0, ref.final_time, 9) if ref.final_time else [0.]:
        grids = []
        if ref.dimension == 1:
            for n in (16, 32, 64):
                edges = np.linspace(*ref.bounds[0], n+1)
                centers = (edges[:-1]+edges[1:])/2
                report = ref.cell_average_report(edges, float(t))
                grids.append(dict(n=n, x=centers.tolist(), edges=edges.tolist(),
                    average=report['values'].tolist(), center_values=ref.point(centers, t).tolist(),
                    max_order_difference=report['max_order_difference'].tolist()))
        frames.append(dict(time=float(t), point=ref.point(coordinates, t).tolist(), grids=grids))
    values = np.concatenate([np.array(f['point']) for f in frames])
    limits = []
    for lo, hi in zip(values.min(axis=0), values.max(axis=0)):
        pad = .08*max(hi-lo, abs(hi)*.1, 1e-3)
        limits.append([float(lo-pad), float(hi+pad)])
    cases.append(dict(ref.metadata(), dimension=ref.dimension, x=x.tolist(), limits=limits, frames=frames))

paths = ['numart/reference_solutions.py', 'numart/reference_riemann.py',
         'numart/scalar_gallery.py', 'scripts/build_reference_solutions.py']
data = dict(schema_version=1, cases=cases,
    scope='Saved reference evaluations, not PDE simulations. Systems average conserved variables. Taylor–Green shows an x-slice at y=pi/4; no area means are displayed.',
    quadrature=dict(order=48, comparison_order=24,
        convention='Gauss quadrature split at known fronts; 24/48 differences are convergence estimates, not rigorous error bounds.'),
    source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
(OUT/'reference-solutions.json').write_text(json.dumps(data, separators=(',', ':'), allow_nan=False)+'\n')

fig, axes = plt.subplots(2, 3, figsize=(13, 7.2))
for ax, id in zip(axes.flat, ['euler-sod', 'swe-dam-break', 'isothermal-jump', 'euler-vacuum', 'swe-dry-bed', 'sine-advection']):
    c = next(c for c in cases if c['id']==id)
    f = c['frames'][-1]; g = f['grids'][0]
    ax.plot(c['x'], np.array(f['point'])[:, 0], color='#23392f', label='Point reference')
    ax.plot(g['x'], np.array(g['average'])[:, 0], 'o', ms=4, color='#bf5b35', label='Conserved/scalar cell means')
    ax.set(title=c['title']+f" | t={f['time']:g}", xlabel='x', ylabel=c['components'][0])
    ax.grid(alpha=.2)
axes[0,0].legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT/'reference-solutions.png', dpi=140)
plt.close(fig)
print(f'Saved {len(cases)} reference cases and their point/cell-average conventions.')
