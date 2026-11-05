# Web edition

A static, English reading site for **The Art of Numerical Algorithms**.

Public URL: https://koyamahr.github.io/the-art-of-numerical-algorithms/

## Build

Requires Node.js 22 or later. From this directory:

```bash
npm ci
npm test
npm run build
npm run dev
```

The local preview is served at `http://127.0.0.1:8765/`.
The generated `dist/` directory contains the complete static website. Markdown
and KaTeX equations are rendered at build time; fonts and figures are served
locally, with no third-party CDN needed by visitors.

## Refresh the source edition

From the repository root, with the Python environment activated:

```bash
python scripts/build_references.py
python scripts/sync_web_content.py
npm --prefix website run build
```

The sync script copies the English chapters, citation catalog, figures, and
original gallery manifest, then computes four Sod density curves using the
library's MUSCL solver. The browser switches between these precomputed curves;
it does not run the Python solver. The separate stability laboratory computes
periodic scalar advection directly in JavaScript, with tests against Python
reference arrays and amplification factors. The embedded plot data includes hashes of
the numerical source files used to produce it.

`content/` and `public/assets/` are checked-in publishing inputs. Keep them in
sync with the numerical-library edition using the commands above. The
`.openai/hosting.json` manifest preserves the optional Sites project identity.
Public hosting uses GitHub Pages through `.github/workflows/pages.yml`, because
this workspace does not enable public Sites hosting.

## Reading routes

- `#/`: introduction and interactive Sod density comparison.
- `#/atlas`: historical reading path.
- `#/methods`: methods and implementation scope.
- `#/experiments`: live periodic-advection and Fourier-amplification laboratory.
- `#/convergence`: original gallery refinement data, observed orders, and unknown counts.
- `#/gallery`: sixteen figures and four movies with category filtering and enlarged views.
- `#/references`: searchable bibliography and BibTeX download.
- `#/read/<chapter>`: complete documentation with equations and section links.

A `?section=<heading-id>` suffix opens a specific section in a chapter.

- `#/time-integration`: seven precomputed ODE integrators, startup perturbations, and leapfrog roots.
- `#/meshes`: three mesh geometries with selectable cells and face-sharing neighbors.

The twenty-six chapters now include SPH/ALE models, cylindrical viscous tensors, a computed Double Mach Reflection baseline, carbuncle reading notes, a sourced Philip L. Roe memorial, slope limiters, and advanced TVB/positivity building blocks. `foundations.json` records temporal/mesh source hashes; the DMR run manifest and arrays are separate downloads.

- `#/hamiltonian`: five canonical-map/accuracy comparisons, two Hamiltonians, energy histories, local Jacobian diagnostics, and one-step phase patches. Data loads on demand from `hamiltonian.json`.

The gallery also includes PM/Tree force studies and isolated/slab Fourier-kernel checks, with separate downloadable source manifests.

- `#/movies`: computed saved-state player, physical-time diagnostics, exact frame stepping, and MP4 export. Use `?case=double-mach`, `orszag-tang-ct`, `orszag-tang-glm`, or `keep-vortex`.

Movies load on demand. Image preloading is bounded; playback timers and native video stop on route changes. No autoplay is used. Steady solutions remain still images. Regenerate with `python scripts/build_movies.py` after installing `.[movies]`; validate all MP4 decodes with `python scripts/check_movies.py`.

- `#/limiters`: five classical slope limiters, scalar baselines, Sod, Sweby bounds, smooth refinement, TVB parameter comparisons, and positive Euler reconstruction scaling. Loads `limiters.json` on demand; all PDE and scaling curves are computed in Python. Rebuild with `python scripts/build_limiters.py` before syncing. Positivity scaling is a standalone reconstruction helper, not a change to Euler/WENO/MHD/KEEP time updates.
