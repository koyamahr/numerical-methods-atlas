# Remembering Philip L. Roe

Philip Lawrence Roe died on April 26, 2026, aged 87. The University of Michigan’s [memorial by Ken Powell](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/) records his contributions to aerospace engineering, numerical methods, teaching, and the computational fluid dynamics community.

This atlas remembers him through a question that remains central to its subject: how can a numerical method preserve the wave structure of the equations while making the computation practical?

## A career in computational fluid dynamics

Roe worked at the Royal Aircraft Establishment from 1962 to 1984, became a professor at Cranfield, and joined the University of Michigan in 1990. He retired in 2021. Michigan’s [official retirement memoir](https://regents.umich.edu/files/meetings/09-21/2021-09-VI-Roe.pdf) documents this chronology and his 2015 AIAA Fluid Dynamics Award. The university memorial also recalls his role with Bram van Leer and Ken Powell in establishing the Keck CFD laboratory.

## The 1981 idea, still executable

In [Approximate Riemann solvers, parameter vectors, and difference schemes](https://doi.org/10.1016/0021-9991(81)90128-5), Roe developed a way to replace a nonlinear interface problem with a carefully constructed linearized system. A defining condition is

\[
\widetilde A(U_L,U_R)(U_R-U_L)=F(U_R)-F(U_L).
\]

Together with consistency and a usable characteristic decomposition, this connects a conservative flux difference to recognizable waves. The [Sod comparison](benchmarks.md) and the atlas home-page selector let readers inspect one educational 1D Euler implementation of this idea alongside HLL, HLLC, and Rusanov.

Our code uses acoustic entropy smoothing. It is an independent teaching implementation, not Roe’s original software. His name identifies a much broader body of work than this one exhibit.

## Precision as a form of respect

The same wave resolution that makes an approximate solver useful invites careful questions about entropy, low densities, and multidimensional shocks. The [carbuncle chapter](carbuncle.md) treats these as separate numerical issues and points to later research. Studying such limits is part of understanding the method’s contribution.

Roe’s later interests included Active Flux; the [Michigan MICDE profile](https://micde.umich.edu/member/philip-roe/) provides an institutional starting point. Active Flux is a reading direction here, not an implemented solver.

We dedicate this reading room’s Roe notes to his memory: an invitation to read the original work, examine the equations, and keep testing the computation.
