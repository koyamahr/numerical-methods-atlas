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
- `#/gallery`: twelve figures with category filtering and enlarged views.
- `#/references`: searchable bibliography and BibTeX download.
- `#/read/<chapter>`: complete documentation with equations and section links.

A `?section=<heading-id>` suffix opens a specific section in a chapter.

- `#/time-integration`: seven precomputed ODE integrators, startup perturbations, and leapfrog roots.
- `#/meshes`: three mesh geometries with selectable cells and face-sharing neighbors.

The nineteen chapters now include SPH/ALE models, cylindrical viscous tensors, a computed Double Mach Reflection baseline, carbuncle reading notes, and a sourced Philip L. Roe memorial. `foundations.json` records temporal/mesh source hashes; the DMR run manifest and arrays are separate downloads.
