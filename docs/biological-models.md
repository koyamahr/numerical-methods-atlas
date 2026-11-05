# Biological model equations and numerical verification

This survey selects 22 biological and biologically motivated model families,
from population growth to stochastic gene regulation and fluid–structure
coupling. It expands the equation map beyond conservation-law CFD. **All 22
entries are literature and proposed benchmark designs; this addition implements
no biological solver and reports no simulated biological result.**

The equations below use conventional simplified or normalized forms. A source
identifies the model lineage, not a claim that every coefficient and variable
matches that paper. The [structured catalog](figures/biological-models.json)
retains references, numerical issues, verification targets and scope for each
entry. The selection emphasizes numerical variety, rather than a comprehensive
review of present-day mathematical biology. Sources checked on 6 November 2026.

## Which biological questions exercise which algorithms

- **Population growth and ecology:** logistic, predator–prey, Fisher fronts,
  cross-diffusion and replicator dynamics test positive states, invariant sets,
  long-time behavior and spatial invasion.
- **Demography and epidemics:** age transport and compartment models test
  renewal boundaries, balances, nonnegative compartments and thresholds.
- **Biochemistry and metabolism:** enzyme kinetics and Monod growth connect
  stiff ODEs, conservation laws and reduced models.
- **Morphogenesis:** Turing analysis, Gierer–Meinhardt, Schnakenberg and
  Gray–Scott separate physical instability from numerical pattern selection.
- **Excitation:** Hodgkin–Huxley, FitzHugh–Nagumo and Aliev–Panfilov connect
  stiff reactions to pulse conduction, refractoriness and spiral waves.
- **Gene regulation and noise:** delayed feedback, toggles, repressilators and
  the chemical master equation need history interpolation, bifurcation analysis
  or jump-process simulation.
- **Biomechanics:** a fluid–elastic structure requires constitutive forces and
  a coupling discretization in addition to fluid equations.

[Existing diffusion and elliptic methods](elliptic.md), [FEM](fem.md),
[sparse/Newton methods](sparse-nonlinear.md), [stiff integrators](stiff-integration.md)
and [incompressible projection](incompressible.md) supply useful numerical
building blocks. Their current tests do not verify these new biological systems.

## Historical model catalog

Dates identify an early source or a selected development, not an exclusive
priority claim. Later spatial extensions, reductions and translations are
identified with their individual entries.

### 01 · 1838 · Logistic population growth

**Population and ecology · Survey only.** Density-limited growth with carrying capacity K. It is the simplest biological ODE baseline.

\[
\dot N=rN(1-N/K).
\]

**Numerical issue.** Positivity, preservation of equilibria and overshoot of K; an accurate-looking curve can still violate the invariant interval.

**Proposed verification.** Compare with N(t)=K/[1+(K/N0−1)exp(−rt)] for N0>0; measure temporal order and behavior near 0 and K.

**Model convention.** The linked original is the later 1847 memoir; the 1838 note itself was not audited. The differential equation is not the discrete logistic map.

Sources: [Verhulst, Pierre-François (1847)](https://doi.org/10.3406/marb.1847.3457).

### 02 · 1913 · Michaelis–Menten and full enzyme kinetics

**Biochemical reactions · Survey only.** Enzyme saturation; the full mass-action system resolves the transient complex C, while the rate law eliminates a fast variable.

\[
E+S\mathrel{\mathop{\rightleftharpoons}^{k_1}_{k_{-1}}}C\mathrel{\mathop{\longrightarrow}^{k_2}}E+P,\qquad v=V_{\max}S/(K_M+S).
\]

**Numerical issue.** Fast initial layers and stiffness; full and reduced models have different validity regimes. Under the usual quasi-steady approximation KM=(k−1+k2)/k1.

**Proposed verification.** Check E+C and S+C+P conservation in the closed mechanism. Compare reduced and full systems as enzyme/substrate scales vary, rather than calling the reduction exact.

**Model convention.** The 1913 rapid-equilibrium interpretation and the 1925 quasi-steady-state derivation must remain distinct.

Sources: [Michaelis–Menten (1913; via the 2011 translation)](https://doi.org/10.1021/bi201284u), [Briggs, George E. and Haldane, J. B. S. (1925)](https://doi.org/10.1042/bj0190338), [Johnson, Kenneth A. and Goody, Roger S. (2011)](https://doi.org/10.1021/bi201284u).

### 03 · 1920 · Lotka–Volterra predator–prey

**Population and ecology · Survey only.** Coupled prey growth and predation; a phase-plane and long-time integration test.

\[
\dot x=\alpha x-\beta xy,\qquad\dot y=\delta xy-\gamma y.
\]

**Numerical issue.** Positive states and artificial damping or growth of closed orbits. Periodic orbits of this idealized system are not attracting limit cycles.

**Proposed verification.** Monitor H=δx−γ ln(x)+βy−α ln(y) for positive x,y, and compare orbit drift under step refinement.

Sources: [Lotka, Alfred J. (1920)](https://doi.org/10.1073/pnas.6.7.410), [Volterra, Vito (1926)](https://doi.org/10.1038/118558a0).

### 04 · 1926 · McKendrick age-structured population

**Structured population transport · Survey only.** Individuals move through age a at unit speed; newborns enter through a nonlocal renewal boundary.

\[
\partial_t n+\partial_a n=-\mu(a)n,\qquad n(0,t)=\int_0^\infty b(a)n(a,t)\,da.
\]

**Numerical issue.** Upwind/FV transport in age, birth-boundary quadrature and truncation of the infinite age interval.

**Proposed verification.** Use characteristic survival along cohorts and check d∫n da/dt=births−deaths, including any artificial oldest-age outflow.

**Model convention.** This is the classical age-transport form; the later von Foerster lineage is acknowledged without treating its date as the first appearance.

Sources: [McKendrick, A. G. (1926)](https://doi.org/10.1017/S0013091500034428).

### 05 · 1927 · SIR and SEIR compartment models

**Epidemic compartments · Survey only.** Closed, well-mixed normalized population fractions. SEIR adds an exposed compartment and a progression rate.

\[
\dot s=-\beta si,\quad\dot i=\beta si-\gamma i,\quad\dot r=\gamma i,\quad s+i+r=1.
\]

**Numerical issue.** Nonnegative compartments, invariant total population and correct resolution of epidemic peak times.

**Proposed verification.** Check total 1 and i+s−(γ/β)ln(s) for β>0,s>0; compare early growth rate βs0−γ and final-size relation in the closed SIR specialization.

**Model convention.** The original general epidemic framework is broader than this SIR specialization. Population-count and fraction conventions give different β definitions.

Sources: [Kermack, W. O. and McKendrick, A. G. (1927)](https://doi.org/10.1098/rspa.1927.0118).

### 06 · 1937 · Fisher–KPP invasion front

**Population and ecology · Survey only.** Spatial spread of an invading population or advantageous allele, represented by a reaction–diffusion front.

\[
u_t=D\Delta u+ru(1-u),\qquad 0\leq u\leq1.
\]

**Numerical issue.** Spatial and temporal front-speed errors; leading-edge resolution, positivity and finite-domain boundary contamination.

**Proposed verification.** Use the Ablowitz–Zeppetella exact front at c=5√(Dr/6), or test the minimal speed 2√(Dr) only with the appropriate steep initial-data regime on a sufficiently large domain.

**Model convention.** Fisher–KPP is a conventional family name; the independent KPP 1937 original remains an archival follow-up. The exact special speed is not the minimal speed.

Sources: [Fisher, R. A. (1937)](https://doi.org/10.1111/j.1469-1809.1937.tb02153.x), [Ablowitz, Mark J. and Zeppetella, Anthony (1979)](https://doi.org/10.1007/BF02462380).

### 07 · 1949 · Monod growth and chemostat

**Biochemical reactions · Survey only.** Nutrient-limited biomass X, substrate S, yield Y and chemostat dilution d; d=0 gives a closed batch model.

\[
\mu(S)=\mu_{\max}\frac{S}{K_S+S},\quad\dot X=(\mu(S)-d)X,\quad\dot S=d(S_{in}-S)-\mu(S)X/Y.
\]

**Numerical issue.** Washout near a threshold, disparate resource/growth scales, positivity and the distinction between yield and rate constants.

**Proposed verification.** For d=0 check S+X/Y. For d>0 use d(S+X/Y)/dt=d[Sin−(S+X/Y)] and verify the washout equilibrium.

**Model convention.** This writes one constant-yield extension of saturation growth, not a universal metabolic model.

Sources: [Monod, Jacques (1949)](https://doi.org/10.1146/annurev.mi.03.100149.002103).

### 08 · 1952 · Hodgkin–Huxley membrane dynamics

**Excitable systems · Survey only.** Voltage and gating variables z=m,h,n describe an ionic excitable membrane. A cable extension adds spatial axial current.

\[
C_m\dot V=I_{app}-\bar g_{Na}m^3h(V-E_{Na})-\bar g_Kn^4(V-E_K)-g_L(V-E_L),\quad\dot z=\alpha_z(V)(1-z)-\beta_z(V)z.
\]

**Numerical issue.** Stiff gates, removable singularities in rate formulas, gating bounds, voltage/current sign and temperature conventions.

**Proposed verification.** Select an explicitly versioned CellML/reference convention, verify resting equilibrium and gate relaxation at clamped voltage, then refine spike time and waveform.

**Model convention.** The original squid-axon model is not a calibrated human cardiac model. No single rate parameter set is selected by this survey.

Sources: [Hodgkin, A. L. and Huxley, A. F. (1952)](https://doi.org/10.1113/jphysiol.1952.sp004764).

### 09 · 1952 · Turing reaction–diffusion framework

**Pattern formation · Survey only.** A framework for diffusion-driven pattern onset around a homogeneous reaction equilibrium, not a unique choice of f and g.

\[
u_t=D_u\Delta u+f(u,v),\qquad v_t=D_v\Delta v+g(u,v).
\]

**Numerical issue.** Physical versus numerical instability, domain eigenmodes and errors in the discrete Laplacian dispersion relation.

**Proposed verification.** For a selected kinetic law compare eigenvalues of J−k²diag(Du,Dv) with early-time Fourier-mode growth. Show that the k=0 reaction equilibrium is stable before asserting diffusion-driven instability.

**Model convention.** A spot image or unequal diffusion coefficients alone do not establish a Turing mechanism. Boundary conditions determine the available modes.

Sources: [Turing, Alan M. (1952)](https://doi.org/10.1098/rstb.1952.0012).

### 10 · 1961 · FitzHugh–Nagumo excitation and recovery

**Excitable systems · Survey only.** A normalized fast excitation/slow recovery model for pulses, refractoriness and spiral waves when extended in space.

\[
v_t=D\Delta v+v-v^3/3-w+I,\qquad w_t=\epsilon(v+a-bw).
\]

**Numerical issue.** Stiff time-scale separation, splitting error, wave-speed convergence and numerical wave breakup.

**Proposed verification.** Check ODE fixed points/nullclines and small-perturbation eigenvalues first; then refine a 1D pulse before a 2D spiral movie.

**Model convention.** This is a common normalized variant; cubic coefficients, recovery signs and nondimensionalization differ between formulations.

Sources: [FitzHugh, Richard (1961)](https://doi.org/10.1016/S0006-3495(61)86902-6), [Nagumo, Jinichi and Arimoto, Suguru and Yoshizawa, Shuji (1962)](https://doi.org/10.1109/JRPROC.1962.288235).

### 11 · 1970 · Keller–Segel chemotaxis

**Chemotaxis · Survey only.** Cell density n drifts up a chemoattractant gradient; τc=0 gives an elliptic chemical subproblem.

\[
n_t=D_n\Delta n-\chi\nabla\cdot(n\nabla c),\qquad\tau_c c_t=D_c\Delta c+\alpha n-\lambda c.
\]

**Numerical issue.** Cross-coupled flux, positivity, mass conservation and concentrated peaks; spurious undershoots must not be mistaken for physical aggregation or blowup.

**Proposed verification.** With zero total cell flux check ∫n conservation, homogeneous equilibria and linear growth; refine the peak and domain before discussing singularity. Use manufactured smooth solutions before aggregation cases.

**Model convention.** This is a common two-field reduction of a more detailed original formulation. Blowup thresholds depend on dimension, domain, boundary and chemical dynamics.

Sources: [Keller, Evelyn F. and Segel, Lee A. (1970)](https://doi.org/10.1016/0022-5193(70)90092-5).

### 12 · 1972 · Gierer–Meinhardt activator–inhibitor

**Pattern formation · Survey only.** A representative simplified short-range activation/long-range inhibition model.

\[
a_t=D_a\Delta a+\rho a^2/h-\mu a+\sigma_a,\qquad h_t=D_h\Delta h+\rho_h a^2-\nu h.
\]

**Numerical issue.** The inhibitor denominator can become singular; positive h, narrow peaks and reaction stiffness require explicit treatment.

**Proposed verification.** Choose a positive homogeneous equilibrium, check its dispersion relation and inhibitor positivity, then refine spike width and pattern wavelength.

**Model convention.** Source densities, saturation and baseline production vary across the model family. This simplified formula is not a verbatim transcription of every original variant.

Sources: [Gierer, Alfred and Meinhardt, Hans (1972)](https://doi.org/10.1007/BF00289234).

### 13 · 1972 · Fluid–elastic structure and immersed boundaries

**Biomechanics · Survey only.** Fluid coupled to a deformable structure; biological examples include valves and membranes, once a force/constitutive law is supplied.

\[
\rho(\boldsymbol u_t+\boldsymbol u\cdot\nabla\boldsymbol u)=-\nabla p+\mu\Delta\boldsymbol u+\boldsymbol f,\quad\nabla\cdot\boldsymbol u=0,\quad\boldsymbol X_t=\boldsymbol u(\boldsymbol X,t).
\]

**Numerical issue.** Stiff elastic forces, pressure projection, Eulerian–Lagrangian interpolation/spreading and volume leakage.

**Proposed verification.** Specify elastic energy and force before solving. Check force transfer, adjoint interpolation/spreading, fluid divergence and enclosed-volume drift on a simple relaxing boundary.

**Model convention.** Immersed boundary is a numerical coupling method, not itself a closed biological constitutive equation. The existing periodic MAC solver does not implement this coupling.

Sources: [Peskin, Charles S. (1972)](https://doi.org/10.1016/0021-9991(72)90065-4).

### 14 · 1977 · Chemical master equation and Gillespie SSA

**Stochastic reaction networks · Survey only.** Integer molecule counts, reaction jumps νj and propensities aj; SSA samples paths of this continuous-time Markov model.

\[
\partial_t P(\boldsymbol n,t)=\sum_j\left[a_j(\boldsymbol n-\boldsymbol\nu_j)P(\boldsymbol n-\boldsymbol\nu_j,t)-a_j(\boldsymbol n)P(\boldsymbol n,t)\right].
\]

**Numerical issue.** Correct combinatorial propensities, event ordering, absorbing states and statistical error; tau-leaping is a separate approximation.

**Proposed verification.** Use immigration–death reactions ∅→X at constant rate k and X→∅ at rate γn: stationary counts are Poisson(k/γ). Compare ensemble mean, variance and distribution with confidence intervals.

**Model convention.** The 1977 paper is a foundational SSA reference, not a priority claim for all master equations. SSA is a solver; the reaction network is the model. A seed documents a trajectory, not an ensemble validation.

Sources: [Gillespie, Daniel T. (1977)](https://doi.org/10.1021/j100540a008).

### 15 · 1977 · Mackey–Glass delayed physiological feedback

**Delay and gene regulation · Survey only.** Delayed feedback in a normalized physiological control model; delay can change stability and oscillatory behavior.

\[
\dot x(t)=\frac{\beta x(t-\tau)}{1+x(t-\tau)^p}-\gamma x(t).
\]

**Numerical issue.** A history function over [−τ,0], delayed interpolation, propagated derivative discontinuities and delay-aware adaptive stepping.

**Proposed verification.** Check the τ=0 ODE limit, a constant equilibrium history and a manufactured forced solution. Compare long-time statistics rather than expecting chaotic trajectories to match pointwise indefinitely.

**Model convention.** A scalar initial value alone is insufficient. The delayed ODE is distinct from a spatial reaction–diffusion model.

Sources: [Mackey, Michael C. and Glass, Leon (1977)](https://doi.org/10.1126/science.267326).

### 16 · 1978 · Replicator evolutionary game dynamics

**Evolutionary dynamics · Survey only.** Strategy fractions reproduce according to relative payoff in a specified matrix game.

\[
\dot x_i=x_i[(A\boldsymbol x)_i-\boldsymbol x^TA\boldsymbol x],\qquad x_i\geq0,\quad\sum_i x_i=1.
\]

**Numerical issue.** Preserving the probability simplex, behavior near extinction boundaries, neutral cycles versus attracting equilibria.

**Proposed verification.** Check simplex conservation, exact invariant faces and an analytically chosen game equilibrium; use the appropriate game-specific invariant or Lyapunov function.

**Model convention.** No universal Lyapunov function or equivalence of fixed point and evolutionarily stable strategy is assumed.

Sources: [Taylor, Peter D. and Jonker, Leo B. (1978)](https://doi.org/10.1016/0025-5564(78)90077-9).

### 17 · 1979 · Schnakenberg reaction–diffusion

**Pattern formation · Survey only.** A simple autocatalytic kinetic law extended in space, useful for reproducible Turing-onset tests.

\[
u_t=D_u\Delta u+a-u+u^2v,\qquad v_t=D_v\Delta v+b-u^2v.
\]

**Numerical issue.** Reaction stiffness, positive concentrations and the distinction between kinetic Hopf and spatial Turing instabilities.

**Proposed verification.** Check u*=a+b, v*=b/(a+b)², then compare mode-growth rates with the linearized discrete and continuum operators under fixed boundaries.

**Model convention.** A mathematical chemical pattern model; matching a visual biological pattern does not calibrate it to a tissue.

Sources: [Schnakenberg, Jürgen (1979)](https://doi.org/10.1016/0022-5193(79)90042-0).

### 18 · 1979 · Shigesada–Kawasaki–Teramoto cross-diffusion

**Population and ecology · Survey only.** Competition with density-dependent self- and cross-dispersal can produce spatial segregation.

\[
u_t=\Delta[(d_1+\alpha_{11}u+\alpha_{12}v)u]+u(a_1-b_1u-c_1v),\quad v_t=\Delta[(d_2+\alpha_{21}u+\alpha_{22}v)v]+v(a_2-b_2u-c_2v).
\]

**Numerical issue.** A coupled nonlinear diffusion matrix, loss of simple scalar maximum-principle arguments, positivity and entropy-compatible discretization.

**Proposed verification.** Start with manufactured smooth solutions and constant-state equilibria. With reactions removed and no normal flux, conserve each species mass; check coefficient assumptions before claiming an entropy law.

**Model convention.** The displayed homogeneous-environment reduction omits the original environmental-potential terms. It is not equivalent to two independent scalar diffusion equations.

Sources: [Shigesada, Nanako and Kawasaki, Kohkichi and Teramoto, Ei (1979)](https://doi.org/10.1016/0022-5193(79)90258-3).

### 19 · 1983 · Gray–Scott spatial autocatalysis

**Pattern formation · Survey only.** A chemical feed/decay model whose spatial extension supports diverse spot and wave patterns.

\[
u_t=D_u\Delta u-uv^2+F(1-u),\qquad v_t=D_v\Delta v+uv^2-(F+k)v.
\]

**Numerical issue.** Sensitivity to F,k, diffusion, domain and finite-amplitude initial perturbations; grid-scale patterns and floating-point variation can affect long-time morphology.

**Proposed verification.** Record every parameter and the perturbation seed. Verify the homogeneous (1,0) state and early perturbation response, then perform grid/time refinement of quantitative observables.

**Model convention.** 1983 is the well-mixed CSTR source; Pearson 1993 is the spatial pattern reference. Spot division does not by itself demonstrate cell division or a linear Turing instability.

Sources: [Gray, Peter and Scott, Stephen K. (1983)](https://doi.org/10.1016/0009-2509(83)80132-8), [Pearson, John E. (1993)](https://doi.org/10.1126/science.261.5118.189).

### 20 · 1996 · Aliev–Panfilov cardiac excitation

**Excitable systems · Survey only.** A reduced phenomenological excitation/recovery model for cardiac waves and restitution.

\[
u_t=D\Delta u-ku(u-a)(u-1)-uv,\quad v_t=\left(\epsilon_0+\frac{\mu_1v}{u+\mu_2}\right)[-v-ku(u-b-1)].
\]

**Numerical issue.** Stiff recovery, denominator behavior and sensitivity of wave speed/restitution to resolution and time splitting.

**Proposed verification.** Select a specific model encoding and parameters; establish single-cell and 1D conduction convergence before 2D reentry. Compare a restitution curve, not only a spiral image.

**Model convention.** Monodomain/bidomain tissue models add conductivity tensors and, for bidomain, an extracellular elliptic constraint. They are not automatically included by this two-variable model.

Sources: [Aliev, R. R. and Panfilov, A. V. (1996)](https://doi.org/10.1016/0960-0779(95)00089-5).

### 21 · 2000 · Repressilator mRNA–protein network

**Delay and gene regulation · Survey only.** Three repressing genes form a cyclic network; retaining mRNA and protein gives six state variables.

\[
\dot m_i=\frac{\alpha}{1+p_{i-1}^n}+\alpha_0-m_i,\quad\dot p_i=\beta(m_i-p_i),\qquad i=1,2,3\ \text{cyclic}.
\]

**Numerical issue.** Multiple degradation scales, oscillation onset, phase error and differences between deterministic cycles and noisy individual-cell behavior.

**Proposed verification.** Check the symmetric equilibrium and its linear stability. Compare period and amplitude under time refinement after a stated transient.

**Model convention.** The six-variable form is distinct from a reduced three-protein oscillator; oscillations are parameter-dependent.

Sources: [Elowitz, Michael B. and Leibler, Stanislas (2000)](https://doi.org/10.1038/35002125).

### 22 · 2000 · Genetic toggle switch

**Delay and gene regulation · Survey only.** Mutual repression produces a possible bistable genetic switch in a normalized model.

\[
\dot u=\frac{\alpha_1}{1+v^p}-u,\qquad\dot v=\frac{\alpha_2}{1+u^q}-v.
\]

**Numerical issue.** Parameter-dependent bistability, saddle separatrices, continuation and sensitivity to perturbations near basin boundaries.

**Proposed verification.** Find all positive equilibria and their Jacobian eigenvalues; verify hysteresis with sufficiently slow continuation and multiple initial conditions.

**Model convention.** Bistability is not guaranteed for arbitrary Hill exponents or production rates. Induction, mRNA dynamics and noise are additional model choices.

Sources: [Gardner, Timothy S. and Cantor, Charles R. and Collins, James J. (2000)](https://doi.org/10.1038/35002131).

## A verification path before attractive movies

A practical first sequence is **logistic/SIR → full enzyme kinetics →
Fisher front → FitzHugh–Nagumo pulse → Schnakenberg modes → Keller–Segel
aggregation**. Predator–prey can run alongside the Hamiltonian notebook as a
long-time invariant test, while a birth–death SSA provides the first stochastic
branch. Gray–Scott is a later visually useful chemical exhibit, with explicit
feed rates, spatial scales, initial perturbation and source attribution.
This order is an implementation proposal, separate from the historical order.

### An exact nonlinear front

For the scaled Fisher equation, the special front of
[Ablowitz–Zeppetella (1979)](https://doi.org/10.1007/BF02462380) gives a
particularly useful deterministic reference:

\[
u(x,t)=\left[1+\exp\left(\sqrt{\frac r{6D}}(x-ct-x_0)\right)\right]^{-2},
\qquad c=5\sqrt{\frac{Dr}{6}}.
\]

A finite interval should use matching time-dependent analytic boundary data,
or put boundaries far enough away and quantify the truncation effect. Compare
front location, profile norms and temporal/spatial refinement separately.
The special explicit front travels faster than the minimal-speed front;
confusing these two reference problems would produce a false solver error.

### Pattern onset is a quantitative test

For a chosen two-species reaction equilibrium, form its Jacobian J. On the
continuum, a Fourier mode with wavevector k evolves under

\[
L(k)=J-|k|^2\operatorname{diag}(D_u,D_v).
\]

On a uniform square grid with a centered Laplacian, replace |k|² by

\[
\kappa_h^2=\frac4{h^2}
\left[\sin^2(k_xh/2)+\sin^2(k_yh/2)\right].
\]

Seed one small eigenmode, measure its early exponential growth and compare
both dispersion relations. A stable k=0 reaction system and an unstable
nonzero mode diagnose the selected diffusion-driven instability; nonlinear
late-time spots alone do not. Schnakenberg supplies a simple kinetic law for
this exercise; it should not be silently substituted for Turing's own example.
Periodic and zero-flux boundaries admit different mode sets.

### Preserve the model before judging the method

Each future run should specify dimensional or normalized variables, the full
parameter set, boundary/initial conditions, units, random seed where relevant,
model version and source. Balances include boundary flux and source terms:
not every biological reaction–diffusion problem conserves each species mass.
Positivity fixes that clip values may change totals and extinction thresholds.
An implicit diffusion step alone does not prove positivity of a split update.

For stochastic networks, distinguish discretization/model approximation from
finite-ensemble sampling uncertainty. For nonlinear reaction networks the ODE
solution need not equal the exact stochastic mean. For delayed equations,
record the history function and interpolation rule. For biochemical reductions,
measure the model-reduction error separately from integration error.

## Sources and further branches

[Murray's third-edition introduction (2002)](https://doi.org/10.1007/b98868)
provides a broad reading route across these branches. Physiome's
[Hodgkin–Huxley workspace](https://models.cellml.org/workspace/hodgkin_huxley_1952)
and [Aliev–Panfilov encoding](https://models.cellml.org/workspace/241/file/1164ecbd63d818c0d6c9631ef6bd92f12e87ae6b/model.xml)
are model-version references to inspect before choosing implementation
parameters, rather than independent validation data.

Separate follow-up surveys could cover neural population fields, spatial
stochastic reaction–diffusion, intracellular polarity and mass-conserving
reaction networks, cell-cycle size structure, vertex/phase-field cell
mechanics, tumor/nutrient free boundaries, and population genetics with drift.
These are additional branches, not a claim that the current 22 entries exhaust
biological modeling. Numerical verification against a stated equation is also
different from validation against organism- or experiment-specific data.

Return to the [equation gallery](equation-gallery.md), the
[historical atlas](history.md), or the [full reference catalog](references.md).
