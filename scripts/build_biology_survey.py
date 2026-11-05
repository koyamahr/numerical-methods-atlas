"""Render the equation survey from its structured, literature-only catalog."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'catalog/biological-models.json').read_text())
references=json.loads((ROOT/'catalog/references.json').read_text())
refs={e['id']:e for e in references}
models=data['models']
assert len({m['id'] for m in models})==len(models)
assert all(m['status']=='survey-only' and all(c in refs for c in m['citations']) for m in models)
intro=r'''# Biological model equations and numerical verification

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
'''
parts=[intro]
for index,m in enumerate(models,1):
    citations=[]
    for key in m['citations']:
        e=refs[key];url='https://doi.org/'+e['doi'] if e.get('doi') else e['source']
        label = "Michaelis–Menten (1913; via the 2011 translation)" if key == "michaelis1913" else f"{e['author']} ({e['year']})"
        citations.append(f"[{label}]({url})")
    parts.extend([f"### {index:02d} · {m['year']} · {m['name']}",
        f"**{m['family']} · Survey only.** {m['meaning']}",
        '\\[\n'+m['equation']+'\n\\]',
        '**Numerical issue.** '+m['numerics'],
        '**Proposed verification.** '+m['verification'],
        ('**Model convention.** '+m['scope']) if m['scope'] else '',
        'Sources: '+', '.join(citations)+'.'])
parts.append(r'''## A verification path before attractive movies

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
''')
# The renderer, not the source catalog, owns the chapter layout.
(ROOT/'docs/biological-models.md').write_text('\n\n'.join(p.strip() for p in parts if p.strip())+'\n')
shutil.copyfile(ROOT/'catalog/biological-models.json',ROOT/'docs/figures/biological-models.json')
print(f'Rendered {len(models)} survey-only model entries.')
