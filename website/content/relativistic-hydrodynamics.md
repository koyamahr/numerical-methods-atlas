# Relativistic hydrodynamics: SRHD, GRHD, and GRMHD

**Literature review, checked 6 November 2026.** These methods are not implemented
in the atlas's Newtonian Euler library. The development has several interacting
branches: conservative shock capture, curved and evolving geometry, magnetic
constraints, physical-state recovery, high-order methods, radiation, and
portable parallel computation. Dates below distinguish publication from
preprint and acceptance dates. This is a selected reading path, not an
exhaustive review or a ranking of codes.

## What changes from the existing Euler examples?

SRHD evolves relativistic matter in flat spacetime. GRHD includes a curved
metric, which may be prescribed or evolved with Einstein's equations. GRMHD
also evolves the electromagnetic contribution. A Kerr-background accretion
calculation and a binary-neutron-star calculation with dynamical spacetime
therefore test different systems.

With c = G = 1 and metric signature (-,+,+,+), ideal-fluid equations are

\[
\nabla_\mu(\rho_0 u^\mu)=0,\qquad
\nabla_\mu T^{\mu\nu}=0,\qquad
T^{\mu\nu}=\rho_0 h u^\mu u^\nu+p g^{\mu\nu},\qquad
h=1+\epsilon+\frac{p}{\rho_0}.
\]

Here rho0 is rest-mass density and epsilon is specific internal energy. In
Cartesian SRHD, a common conservative state is

\[
W=(1-v^2)^{-1/2},\qquad
D=\rho_0W,\quad S_i=\rho_0hW^2v_i,\quad
\tau=\rho_0hW^2-p-D.
\]

It differs from the Newtonian state in [the existing benchmarks](benchmarks.md).
Primitive recovery is nonlinear. One-dimensional acoustic speeds with zero
transverse velocity are (v +/- cs)/(1 +/- v cs), not v +/- cs. In a 3+1 GR
formulation, lapse, shift, spatial volume factors, and metric derivatives
enter the fluxes and sources. These are structural changes, not a different
value of gamma. [Font (2008)](https://doi.org/10.12942/lrr-2008-7) is the
formulation review used here; the original Valencia reference is below.

## 1972–1998: from curved-background flows to conservative HRSC

[Wilson (1972)](https://adsabs.harvard.edu/pdf/1972ApJ...173..431W)
is an early numerical study of gas falling into a Kerr black hole. It provides
historical context for relativistic fluid computation, rather than a claim
that fixed-background hydrodynamics solves the full evolving Einstein system.

The high-resolution shock-capturing (HRSC) branch brings the characteristic
and conservative methods of classical CFD into relativity.
[Martí and Müller (1994)](https://doi.org/10.1017/S0022112094003344)
give an exact SR Riemann solution for flow normal to the initial discontinuity.
That scope matters when selecting multidimensional tests with transverse
velocities; the original normal-flow reference is not a general transverse
Riemann solution.

[Banyuls et al. (1997)](https://doi.org/10.1086/303604) present the 3+1 local
characteristic formulation commonly called Valencia. Its conservative state,
characteristic information, and geometric source terms make modern shock
capture applicable in GR. It is a central reference, not a claim that all
earlier relativistic methods were nonconservative.
[Pons et al. (1998)](https://arxiv.org/abs/astro-ph/9807215) connect GRHD to SR
Riemann solvers through a local coordinate transformation. Curvature and
coordinate effects still have to be accounted for outside that local solve.

## 1999–2006: magnetic constraints and dynamical spacetime

[Komissarov (1999)](https://doi.org/10.1046/j.1365-8711.1999.02244.x)
develops a multidimensional Godunov-type relativistic MHD scheme with magnetic
flux conservation. [HARM, Gammie–McKinney–Tóth (2003)](https://arxiv.org/abs/astro-ph/0301509)
combines conservative GRMHD, HLL fluxes, and a Tóth-type CT construction, with
black-hole torus calculations among its examples. Its original formulation
must be distinguished from later dynamical-spacetime frameworks.

[Duez et al. (2005)](https://arxiv.org/abs/astro-ph/0503420) evolve the coupled
Einstein–Maxwell–MHD system, using BSSN for spacetime and conservative shock
capture for the matter. This is the additional step needed when matter and
geometry affect one another dynamically.

Conservation variables do not remove the need to recover physical fluid
states. [Noble et al. (2006)](https://arxiv.org/abs/astro-ph/0512420)
compare nonlinear recovery algorithms, including reductions to one or two
unknowns. Recovery failure, atmosphere floors, and repairs must be tracked
separately from truncation error and conserved-variable residuals.

## 2011–2026: the particle branch from GSPH

[Inutsuka's original GSPH](gsph.md) connects to
[Iwasaki–Inutsuka (2011)](https://arxiv.org/abs/1106.3389), a Newtonian
particle MHD method using Riemann problems and Alfvén characteristics.
It is not itself relativistic.

[Kitajima–Inutsuka–Seno (2026)](https://doi.org/10.1016/j.jcp.2025.114448)
then formulate **special relativistic Godunov SPH (SRGSPH)**. The paper addresses
convolution-based interactions, unequal baryon numbers, and variable smoothing
lengths, with shock-tube and Kelvin–Helmholtz examples. It is a direct bridge
between the requested particle and relativistic branches. The preprint is
from October 2025; the journal issue is January 2026, despite the DOI's 2025
identifier. It should not be described as a GRHD implementation.

## 2013 onward: radiation and microphysics add stiff systems

[Sądowski et al. (2013)](https://arxiv.org/abs/1212.5050) describe KORAL's
covariant M1 radiation moments with semi-implicit interaction sources. This
connects relativistic fluid methods to the atlas's planned implicit and IMEX
chapters. M1 closes angular moments; it does not solve the full radiation
distribution without approximation.

For neutron-star mergers, [Foucart (2023)](https://doi.org/10.1007/s41115-023-00016-y)
reviews leakage, moment, and Monte Carlo neutrino transport and the remaining
interaction-modeling limitations. Tabulated finite-temperature equations of
state, composition, transport, and their uncertainties are separate advances
from the choice of a Riemann flux. Ideal relativistic hydrodynamics also does
not automatically supply a causal relativistic viscous theory.

## A parallel 1979–2019 branch: causal viscous fluid theory

The Newtonian [viscous stress](coordinates-viscosity.md) cannot simply be
inserted into relativistic Euler equations without examining causality and
the initial-value problem. [Israel–Stewart (1979)](https://doi.org/10.1016/0003-4916(79)90130-1)
provides a central reference for transient dissipative theories with additional
relaxation variables.

[Bemfica–Disconzi–Noronha (2019)](https://arxiv.org/abs/1907.12695) and
[Kovtun (2019)](https://arxiv.org/abs/1907.08191) develop a different line:
appropriate first-gradient constitutive choices and hydrodynamic frames can
support causal or stable formulations under specified conditions. The former
paper addresses nonlinear causality without extra extended variables; the
latter examines stable first-order frames. Their results should not be merged
into an unconditional claim for every equation of state or transport choice.
Physical causality, PDE well-posedness, and stability of a discrete time step
are separate checks. This branch is theory and reading context in the atlas,
not an implemented viscous relativistic solver.

## 2022–2025: high order with shocks, surfaces, and physical constraints

[Deppe et al. (2022)](https://arxiv.org/abs/2109.11645) develop a DG–finite
difference hybrid: attempt a high-order DG update and recompute inadmissible
regions with robust FD. The 2021 preprint and 2022 publication dates should
remain distinct. [Their binary-neutron-star study (2024 preprint)](https://arxiv.org/abs/2406.19038)
extends the hybrid approach to dynamical spacetime and merger calculations.
The latter is cited here as a preprint; a separate journal record has not been
verified in this review.

[Cao–Peng–Wu (2025)](https://doi.org/10.1016/j.jcp.2025.113770)
study physical-constraint-preserving, oscillation-eliminating DG for GRHD,
including positive thermodynamic states and subluminal velocity under their
stated scheme assumptions. Their results are not a guarantee for arbitrary
limiters, fluxes, EOS, or spacetime discretizations. A theorem for a selected
GRHD formulation and an astrophysical merger-code demonstration are different
types of evidence.

## 2025–2026: portable GPU computation of the coupled system

[AthenaK, Fields et al. (2025)](https://arxiv.org/abs/2409.10384)
demonstrates dynamical-spacetime GRMHD and binary-neutron-star mergers on GPUs,
with CT and first-order flux correction among its numerical ingredients.
Its preprint is from 2024; the journal reference is ApJS 276, 35 (2025).
[AsterX, Kalinani et al. (2025 issue)](https://doi.org/10.1088/1361-6382/ad9c11)
provides another open GPU-oriented GRMHD framework, based on Valencia and Z4c.
Its online publication was December 2024. Refinement infrastructure is part
of those source codes; implementing AMR in this atlas remains deferred.

[GRACE, Musolino et al.](https://journals.aps.org/prd/accepted/10.1103/yq78-m749)
was **accepted by Physical Review D on 2 November 2026**, as checked on
6 November. Its [July 2026 preprint](https://arxiv.org/abs/2607.09854)
describes Kokkos-based portability, CT, Z4c coupling, and neutron-star merger
examples. Acceptance is not a verified final volume/page citation.
These papers establish examples of portable implementations; they do not
establish a universal speed or accuracy ranking across hardware and physics.

## What the atlas can reproduce in stages

The following is an implementation proposal, not a result of this review:

1. **SRHD:** primitive/conservative round trips, characteristic speeds, smooth
   waves, shock tubes, reflection, and transverse-velocity cases. Check EOS
   validity, rho and pressure positivity, and speeds below c.
2. **SRMHD:** add relativistic Alfvén waves, magnetic shock tubes, and a rotor;
   specify the magnetic-divergence operator and every repair/floor.
3. **Fixed-metric GR:** metric-aware flat-space limits, Michel/Bondi accretion,
   equilibrium stars, and torus configurations, with geometric source balance.
4. **Dynamical GR:** couple a separately verified spacetime evolution; monitor
   Einstein constraints, baryon conservation, stellar oscillations, and waveform
   convergence before attempting mergers.
5. **Radiation or SRGSPH:** keep each branch's state, boundary, conservation,
   transport closure, and reference tests explicit. Reuse the Newtonian examples
   as comparisons, not as evidence that a relativistic solver already exists.

The historical conclusion is that progress comes from the *combination* of
these layers. A new high-order reconstruction or a larger GPU run alone does
not resolve primitive recovery, surface/atmosphere handling, constraint errors,
or microphysical uncertainty.
