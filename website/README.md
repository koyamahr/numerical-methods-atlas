# Web edition

A static Japanese/English reading site for **An Atlas of Numerical Methods** / **数値計算法アトラス**.

Publication target: `https://koyamahr.github.io/numerical-methods-atlas/` (not deployed yet). The old site remains live during migration. Branding and URLs are defined in `site.config.json`; see [migration preparation](../URL_MIGRATION.md).

## Build

Requires Node.js 22 or later and Python 3.9 or later (standard library only for publishing preparation). From this directory:

```bash
npm ci
npm test
npm run build
npm run dev
```

The local preview is served at `http://127.0.0.1:8765/`.
The generated `dist/` directory contains the complete static website. Markdown
and KaTeX equations are rendered at build time; fonts and figures are served
locally, with no third-party CDN needed by visitors. `npm run build` can therefore prepare
the static release on a machine without NumPy or Matplotlib.

## Refresh the source edition

From the repository root, with the Python environment activated:

```bash
npm --prefix website run prepare:content
npm --prefix website test
npm --prefix website run build
python scripts/check_web_release.py
```

`npm test` and `npm run build` both prepare source chapters, references,
coverage counts and saved data before running. This standard-library-only
step does not rerun solvers, regenerate numerical profiles, or replace their
provenance. To change a numerical exhibit, run its specific builder first.
The legacy `scripts/sync_web_content.py` additionally regenerates selected
original experiments; it is an explicit research command, not a publishing
prerequisite.

The browser switches between these precomputed curves;
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

Every available reading chapter is also published as full-text static HTML at
`/en/read/<chapter>/` and `/ja/read/<chapter>/`. These pages include rendered
equations, local figures, per-page descriptions, canonical URLs, reciprocal
language alternates, and ordinary section anchors without requiring JavaScript.
The build includes reading indexes and all 95 reading pages in `sitemap.xml`.
Untranslated chapters link to their English edition without advertising a
nonexistent Japanese URL. Old `#/read/<chapter>?section=<id>` links forward to
the corresponding static page and section. Interactive experiment routes remain
available from the chapters. `scripts/check_web_release.py` checks the generated
pages and their assets/links before deployment.

For a local preview of these project-prefixed URLs, serve a parent folder with
`dist/` mounted as `numerical-methods-atlas/`, for example from this directory:

```bash
mkdir -p .preview
ln -s ../dist .preview/numerical-methods-atlas
python3 -m http.server 8765 --directory .preview --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/numerical-methods-atlas/en/read/stability/`.

- `#/`: introduction and interactive Sod density comparison.
- `#/atlas`: historical reading path.
- `#/methods`: methods and implementation scope.
- `#/experiments`: live periodic-advection and Fourier-amplification laboratory.
- `#/convergence`: original gallery refinement data, observed orders, and unknown counts.
- `#/gallery`: computed figures and four movies with category filtering and enlarged views.
- `#/references`: searchable bibliography and BibTeX download.
- `#/read/<chapter>`: complete documentation with equations and section links.

A `?section=<heading-id>` suffix opens a specific section in a chapter.

- `#/time-integration`: twelve precomputed ODE integrators, startup perturbations, and leapfrog roots.
- `#/meshes`: three mesh geometries with selectable cells and face-sharing neighbors.

The reading chapters include SPH/ALE models, cylindrical viscous tensors, a computed Double Mach Reflection baseline, carbuncle reading notes, a sourced Philip L. Roe memorial, slope limiters, and advanced TVB/positivity building blocks. `foundations.json` records temporal/mesh source hashes; the DMR run manifest and arrays are separate downloads.

The GSPH and relativistic-hydrodynamics chapters are source-based reading notes
and implementation plans, with publication status checked in November 2026.
They add no GSPH, SRHD, GRHD, or GRMHD simulation to the numerical library.

- `#/hamiltonian`: five canonical-map/accuracy comparisons, two Hamiltonians, energy histories, local Jacobian diagnostics, and one-step phase patches. Data loads on demand from `hamiltonian.json`.

The gallery also includes PM/Tree force studies and isolated/slab Fourier-kernel checks, with separate downloadable source manifests.

- `#/movies`: computed saved-state player, physical-time diagnostics, exact frame stepping, and MP4 export. Use `?case=double-mach`, `orszag-tang-ct`, `orszag-tang-glm`, or `keep-vortex`.

Movies load on demand. Image preloading is bounded; playback timers and native video stop on route changes. No autoplay is used. Steady solutions remain still images. Regenerate with `python scripts/build_movies.py` after installing `.[movies]`; validate all MP4 decodes with `python scripts/check_movies.py`.

- `#/limiters`: five classical slope limiters, scalar baselines, Sod, Sweby bounds, smooth refinement, TVB parameter comparisons, and positive Euler reconstruction scaling. Loads `limiters.json` on demand; all PDE and scaling curves are computed in Python. Rebuild with `python scripts/build_limiters.py` before syncing. Positivity scaling is a standalone reconstruction helper, not a change to Euler/WENO/MHD/KEEP time updates.

- `#/runge-kutta`: RK1, three RK2 choices, three RK3 choices, and two RK4 choices. Shows actual nonlinear stages, full tableaus, sampled scalar stability contours, and refinement by step count or RHS count. Loads `runge-kutta.json` on demand; regenerate with `python scripts/build_runge_kutta.py` before syncing. No adaptive or embedded-pair implementation.

- `#/cip`: original cubic-Hermite CIP versus point-value linear interpolation, with evolved gradients, 48 paired configurations, smooth refinement, and an analytic remapping mass counterexample. Lazy-loads `cip.json`; regenerate using `python scripts/build_cip.py` before syncing. CIP-CSL and RCIP remain reading context.

## Prepared local expansion

`#/equations` opens nine computed cases across seven equation families.
`python scripts/build_equation_gallery.py` from the repository root builds
`equation-gallery.json`, `solver-foundations.json` and three figures.
Scalar snapshots observe completed steps; 1D fluid cases are labeled separate
final-time solves. Local copies of changed chapters/data/assets are synchronized
without regenerating unrelated exhibits. This expansion has not been deployed.

## Audited promotional counts

The homepage and `#/coverage` use `coverage.json`, generated automatically
before `npm run build`. The source is `catalog/coverage.json`, with biology
entries and bibliographic types imported from their existing catalogs.
`docs/site-coverage.md` lists every counted entry and explains publication
deduplication. Cite journal/conference paper counts separately from all
sources; local examples and reading-only entries remain labeled.

## Japanese and English

The local bilingual edition adds a language switch, a bilingual glossary and all 42 complete Japanese draft chapters. Experiment notebooks also localize their controls and explanations. Original bibliographic metadata/source notes, detailed coverage annotations and lettering baked into images/video retain their source form. The Japanese drafts have not been marked editorially reviewed. See [implementation status](../BILINGUAL_STATUS.md) and [migration plan](../BILINGUAL_PLAN.md). Translation files do not increase the logical chapter, method, model or publication counts.
