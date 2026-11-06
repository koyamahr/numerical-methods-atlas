# Atlas expansion prepared for review

> Publication update, November 6, 2026: the reviewed expansion and subsequent bilingual/basis additions are now published at https://koyamahr.github.io/numerical-methods-atlas/ . The following is the retained pre-publication review record; current counts and translation scope are in README.md and BILINGUAL_STATUS.md.

This candidate adds the equation gallery, solver foundations, source-based
biology/GSPH/relativistic chapters, Arakawa-grid comparisons and audited
homepage coverage. It is prepared on a review branch and does not update the public website.
The publication guard requires the planned new repository; merging this
candidate to the legacy repository does not deploy the new edition there.

## Proposed public presentation

Use **An Atlas of Numerical Methods** / **数値計算法アトラス**, with
`https://koyamahr.github.io/numerical-methods-atlas/` as the new canonical
publication target. Keep the sibling link to *The Art of Thermal Instability*.
The existing public site remains at the old URL until cutover; see
`URL_MIGRATION.md` for the separate legacy landing artifact and publication guard.
English remains the source edition. The bilingual candidate adds a 137-term
glossary and Japanese drafts for all 42 reading chapters. All experiment
notebooks localize their controls and explanations. Original bibliographic
metadata/source notes, detailed coverage annotations and image/video lettering
remain shared. The drafts have not been marked editorially reviewed; see
`BILINGUAL_STATUS.md`.
The homepage leads with 126 journal/conference papers and distinguishes
42 equation/model entries, 83 methods/building blocks, 146 total sources,
and nine saved-profile gallery cases.

`#/coverage` makes those counts inspectable and filterable by model/method,
local example/reading-only, and text. Its linked inventory defines the counting
units. It does not advertise every survey entry as an implemented solver.
A duplicate Cockburn–Shu record was merged and Burgers 1948 was classified as
a book chapter; the earlier 146 catalog records became 145 unique works. Adding Dahlquist
(1963) for the A/L-stability and error-norm guide brings the candidate to 146
unique works, including 126 journal/conference papers.

## Numerical and editorial scope

New scoped examples include P1 FEM, GMRES/BiCGSTAB/ILU/Newton, implicit/adaptive
ODE methods, periodic MAC projection, D2Q9–BGK, first-order hyperbolic diffusion,
Burgers/LWR finite volumes and linear A/B/C shallow-water Fourier symbols.
Biology's 22 entries, GSPH and relativistic-fluid developments are reading
material and implementation plans. NASA candidates and quantum chemistry/DFT
are not promoted as completed simulations.

The existing standalone PPM/characteristic-WENO prototype files are outside
this review candidate and remain in the working directory; they are not
included in the advertised method count. This avoids incorporating an
independent unfinished exhibit into the release.

## Reproduction and publication boundary

```bash
python -m pip install '.[test]'
python -m pytest -q
npm --prefix website ci
npm --prefix website test
npm --prefix website run build
python scripts/check_web_release.py --output outputs/release-check.json
```

The Web test/build hooks use Python's standard library to prepare chapters,
references, catalogs and already saved numerical assets. They do not rerun
numerical solvers. Numerical builders remain explicit commands. The static
release checker verifies chapter synchronization, local reading/asset links,
module imports, bibliography/coverage consistency and artifact hashes.
The bilingual build also compares section IDs, display equations, executable
code blocks and external citation links against the English source. Japanese
catalog chapters reuse the same 22 model identities and 146 source records.

Both CI and the Pages workflow use the same preparation/check path. The Pages
workflow watches the catalogs, documents and preparation scripts as well as
the website. Publication keeps its `main` branch trigger, but verifies the repository against
`site.config.json` before deploying to the new URL. This candidate does not
create or rename a repository, replace the legacy site, or deploy either artifact.
