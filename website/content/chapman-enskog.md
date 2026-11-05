# Chapman–Enskog expansion: from populations to transport

Chapman–Enskog（チャップマン–エンスコッグ）expansion separates kinetic
relaxation from slowly varying hydrodynamic fields. The classical kinetic
theory is treated by Chapman and Cowling's *The Mathematical Theory of
Non-Uniform Gases* (first edition 1939; third edition 1970). The book's date
is not the invention date of the expansion. This chapter gives an independent,
unforced, isothermal lattice-BGK derivation at low Mach number.

## A small parameter and solvability

Introduce a bookkeeping parameter ε for slow variation:

\[
f_q=f_q^{(0)}+\epsilon f_q^{(1)}+\epsilon^2 f_q^{(2)}+\cdots,
\quad \partial_t=\epsilon\partial_{t_1}+\epsilon^2\partial_{t_2},
\quad \nabla=\epsilon\nabla_1.
\]

Conserved moments are carried by the local equilibrium, so higher-order
corrections have zero mass and momentum moments:

\[
\sum_q f_q^{(k)}=0,\quad
\sum_q\boldsymbol c_q f_q^{(k)}=0\quad (k\geq1).
\]

These are constraints on the expansion, not instructions to erase the
nonequilibrium stress. The stress moment of f^(1) produces viscous transport.

## Keep the discrete-time Taylor term

For lattice BGK, expand the streaming side with D_q=∂t+c_q·∇. In lattice
time units the Taylor series starts as D_q f_q + D_q² f_q/2.
At successive orders,

\[
f_q^{(0)}=f_q^{eq},\qquad
f_q^{(1)}=-\tau D_{1q} f_q^{eq},
\]

\[
\partial_{t_2} f_q^{eq}
+\left(1-\frac1{2\tau}\right)D_{1q}f_q^{(1)}
=-\frac{f_q^{(2)}}{\tau}.
\]

The first-order mass and momentum moments give the continuity and Euler
parts. The second-order stress correction supplies the Newtonian viscous
part. D2Q9 equilibrium isotropy, the low-Mach approximation, and the preceding
factor give the shear viscosity

\[
\nu=c_s^2\left(\tau-\frac12\right)\Delta t.
\]

Here τ is the **dimensionless number of lattice time steps** used for
relaxation, with physical τ_relax=τΔt. Continuous-time BGK instead gives
ν=c_s²τ_relax for the corresponding isothermal model; there is no streaming
Taylor half-step in that continuous equation. Mixing those definitions yields
a wrong viscosity.

## What this derivation does and does not establish

The [D2Q9 experiment](lattice-boltzmann.md) measures shear damping rather than
only substituting this formula. [Qian et al. (1992)](https://doi.org/10.1209/0295-5075/17/6/001)
is the lattice-model source; the [BGK source](https://doi.org/10.1103/PhysRev.94.511)
concerns continuous kinetic relaxation. [Guo et al. (2002)](https://doi.org/10.1103/PhysRevE.65.046308)
treats the force discretization separately; the unforced algebra above does
not derive its source term.

This is a formal near-equilibrium asymptotic expansion, with small gradients
and small Mach number for the truncated isothermal equilibrium. It does not
prove stability near shocks, justify arbitrary relaxation times, recover an
energy equation, or make this model a general rarefied-gas Boltzmann solver.
Burnett-order transport and thermal collision models require additional
moments and analysis.
