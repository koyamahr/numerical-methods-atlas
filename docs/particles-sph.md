# Particle methods and smoothed particle hydrodynamics

Lagrangian particles carry quantities while moving with a flow. SPH replaces a field value or derivative by a local kernel-weighted particle sum. The independent early papers by [Gingold and Monaghan (1977)](https://doi.org/10.1093/mnras/181.3.375) and [Lucy (1977)](https://doi.org/10.1086/112164) are historical starting points. The static reconstruction below does not reproduce their stellar calculations.

## From an integral to particles

A smoothed field is approximated by

\[
f_h(x)=\int f(x')W(x-x',h)\,dx'
\approx\sum_b \frac{m_b}{\rho_b} f_b W(x-x_b,h).
\]

The volume weight m_b/rho_b matters. Smoothing length h is a kernel scale, not necessarily the particle spacing. Compact support defines the neighbor search; it does not impose a fixed mesh connectivity.

Our one-dimensional example uses the normalized cubic spline, with q = |x|/h:

\[
W(x,h)=\frac{2}{3h}\begin{cases}
1-\frac32q^2+\frac34q^3,&0\le q<1,\\
\frac14(2-q)^3,&1\le q<2,\\
0,&q\ge2.
\end{cases}
\]

This prefactor is **one-dimensional**. Two- and three-dimensional kernels require different normalization constants.

## Partition of unity and correction

The raw sum of particle volumes times W need not equal one on a discrete particle set. A Shepard-normalized interpolant divides by that sum. It reproduces a constant wherever the denominator is nonzero, but this interpolation correction alone does not establish conservative dynamics, linear consistency, or stable pressure forces.

```python
import numpy as np
from numart.geometry import sph_reconstruct
p = (np.arange(64) + 0.5) / 64
x = np.linspace(0, 1, 201)
f, partition = sph_reconstruct(x, p, np.sin(2*np.pi*p), h=0.04)
f_corrected, _ = sph_reconstruct(x, p, np.sin(2*np.pi*p), h=0.04, normalize=True)
```

The routine uses periodic minimum-image distances on [0,1] and equal volume weights 1/N. It requires 0 < h < 1/4 so the support fits the minimum-image convention. It does not infer physical density from arbitrary unequal particle spacings.

## What a fluid solver would additionally need

Density estimation or a continuity update, a consistent pressure force, momentum and energy evolution, boundary particles, time stepping, neighbor-search updates, and treatment of shocks or tensile/pairing instabilities are additional modeling decisions. Artificial viscosity used in shock-capturing SPH must be distinguished from the physical Newtonian [viscous stress tensor](coordinates-viscosity.md).

Tests check the continuous kernel’s normalization and discrete constant reproduction after normalization. This edition implements **kernel reconstruction only**, not an SPH flow solver. See [time integration](time-integration.md) for why a particle kick–drift leapfrog and a two-step first-order ODE leapfrog should not be conflated.
