# Time-dependent tests: movies and saved states

[Open the motion gallery](https://koyamahr.github.io/numerical-methods-atlas/#/movies).

Use movies when the evolution is part of the question: a shock reflecting, a vortex advecting, or magnetic structures forming. Steady solutions, manufactured equilibrium profiles, and final elliptic fields remain still figures. A solver residual versus iteration is an algorithmic history, not a physical-time flow movie.

## Five computed movies

- **Double Mach Reflection:** Mach-10 2D Euler reflection on 256 × 64 cells, t = 0 to 0.2, first-order HLL with SSPRK2 and CFL 0.4. The fine wall jet is not resolved. Read the [setup](double-mach.md).
- **Orszag–Tang with CT:** 64² periodic planar ideal MHD, t = 0 to 0.5, first-order Rusanov with forward Euler and CFL 0.3. Magnetic divergence uses the staggered face operator.
- **Orszag–Tang with GLM:** the same resolution and physical interval, with fixed cleaning speed 3 and damping 0.18. Its native divergence uses the cell-centered central operator. The CT and GLM plots do not form an equal-accuracy ranking. Read the [MHD definitions](mhd.md).
- **Smooth isentropic vortex with original KEEP:** 96² periodic Euler on [−10,10]², t = 0 to 4, the second-order arithmetic-mean Cartesian KEEP flux and classical RK4, CFL 0.25. No shock stabilization, pressure-equilibrium-preserving extension, or exact entropy claim is included. Read the [KEEP chapter](keep.md).

- **Mach-3 forward-facing step:** 240 × 80 cells, t = 0 to 4, first-order HLL and SSPRK2 with CFL 0.4. Grid-aligned blocked cells represent a step at x = 0.6 of height 0.2. Standard reflection is applied without an entropy/enthalpy corner reset. Diagnostics exclude solid cells. This is a classical inviscid benchmark, not a NASA experimental validation. See the [shock-case definitions](nasa-2d.md).

Density and pressure appear together in every movie. These are rendered numerical states from the repository solvers, not interpolated illustrations or reproductions of original-paper movies.

## Actual physical times, unchanged time steps

Each movie requests 81 output times, including the initial and final times. The recorder saves the first completed solver state at or after each request. It does **not** shorten a numerical step to hit a requested time and does not interpolate the solution. If a coarse step crosses several requests, one state represents them. Actual times and solver step counts accompany every frame.

The production movies have 81 distinct states each. The MHD CT and GLM solvers choose different time steps, so similarly numbered frames need not have identical intermediate physical times. Read the timestamps before comparing them. Snapshot tests verify that enabling output leaves the final state and numerical history unchanged.

## Fixed scales and explicit playback

Each density and pressure color scale is fixed across its entire run using that run’s extrema over the saved states. Colors must not be interpreted as identical values across different movies unless their scale labels agree. The minima and maxima listed beside the player are measurements of the currently displayed state; they do not establish a positivity theorem.

Playback starts only after pressing **Play**. Pause, first/last, previous/next, a saved-frame slider, speed selection, and an optional loop support inspection. Speed is presentation speed, not a change to the simulation. At the nominal rate, 81 saved frames at 12 frames per second make a 6.75-second clip. All physical times remain printed inside the images.

A native MP4 player and MP4/frame downloads are also available. MP4 uses H.264 video with no audio; the inspectable image frames are lossless WebP. Video compression is a presentation step and never feeds back into the computation.

## Reproduce and verify

```bash
python -m pip install '.[movies]'
python scripts/build_movies.py
python scripts/check_movies.py
```

The builder writes the published frames, MP4 files, and [movie catalog](https://koyamahr.github.io/numerical-methods-atlas/assets/movies/catalog.json) into `website/public/assets/movies`. It also saves full numerical snapshots as compressed NumPy arrays in the ignored `outputs/movies` directory for local inspection. Source hashes, image/video hashes, numerical-state hashes, software versions, methods, boundary conditions, physical scales, and per-frame diagnostics are recorded in the catalog. The fifth movie is built by `python scripts/build_shock_gallery.py` and has a separate [shock catalog](https://koyamahr.github.io/numerical-methods-atlas/assets/movies/shock-catalog.json); the player combines both catalogs. Its full saved states are in `outputs/shock-gallery`.

The checker validates hashes and metadata, opens each saved image, and decodes each MP4 to verify its dimensions, playback rate, and complete frame count. A short small-grid build can be made with `--quick --output <directory>`; its catalog is marked as a quick check and is not the published production run.

## Multidimensional still fields

The [numerical gallery](https://koyamahr.github.io/numerical-methods-atlas/#/gallery)
opens with 2D/3D spatial fields, including the five movie entry points above.
Dimension and subject filters can be combined; all dimensions also includes
the 1D comparisons and algorithmic diagnostic figures.

Three additional still figures expose fields from existing solvers:

- **2D triangular P1 Poisson:** 24 × 24 split squares (1152 triangles), zero
  Dirichlet data and exact solution sin(πx)sin(πy). The second panel is nodal
  error; continuous L2/H1 errors are measured separately inside elements.
- **2D periodic Taylor–Green:** 64 × 64 MAC cells, viscosity 0.1, t = 0.5.
  Speed/arrows average face velocities to cell centers only for visualization;
  velocity RMS and divergence diagnostics use the native MAC arrays.
- **3D periodic Poisson:** a 32³ FFT solve with density
  1 + 0.3 cos(2πx)cos(4πy)cos(2πz), G = 1 and zero-mean potential.
  Three orthogonal slices at coordinate 0.5 use the same color limits.
  This is a static 3D field checked against one exact Fourier mode, not a
  3D fluid or particle-evolution simulation.

Reproduce these still fields with `python scripts/build_multidimensional_gallery.py`.
Download the [definitions, diagnostics and source hashes](figures/multidimensional-fields.json)
and [computed arrays](figures/multidimensional-fields.npz). These views add no new
solver or convergence study; the existing FEM and MAC refinement tests remain
separate evidence.

## What a movie does not establish

A visually smooth evolution does not establish mesh convergence, an entropy inequality, shock robustness, long-time turbulent accuracy, or agreement with experiments. The [KEEP vortex refinement](keep.md) supplies separate smooth-error measurements. The [carbuncle chapter](carbuncle.md) explains why a shock movie alone cannot certify multidimensional stability.
