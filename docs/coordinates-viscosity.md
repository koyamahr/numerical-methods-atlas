# Polar and cylindrical coordinates: tensors and viscosity

The formulas below use **physical components in the orthonormal basis** (e_r,e_phi,e_z), with cylindrical coordinates (r,phi,z), phi in radians, and r > 0. A planar polar field is obtained by setting u_z = 0 and all z derivatives to zero. Coordinate-basis tensor components have different metric factors; mixing the conventions creates incorrect viscous forces.

For a reference derivation of cylindrical fluid equations, see [Richard Fitzpatrick’s lecture notes](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html). This chapter states a general bulk-viscosity convention explicitly and checks it with analytic fields.

## Velocity gradient: differentiate the basis too

Let L_ij = e_i · ((e_j · grad)u). Its rows are velocity components and columns are differentiation directions:

\[
L=\begin{pmatrix}
\partial_r u_r & (\partial_\phi u_r-u_\phi)/r & \partial_z u_r\\
\partial_r u_\phi & (\partial_\phi u_\phi+u_r)/r & \partial_z u_\phi\\
\partial_r u_z & (\partial_\phi u_z)/r & \partial_z u_z
\end{pmatrix}.
\]

The terms −u_phi/r and +u_r/r arise from rotation of the basis. Define D = (L+L^T)/2 and theta = tr(L):

\[
\theta=\nabla\cdot u=\partial_r u_r+\frac{u_r}{r}
+\frac{\partial_\phi u_\phi}{r}+\partial_z u_z.
\]

The input `partials[...,i,j]` in `numart.coordinates` means the plain coordinate derivative of physical velocity component i with respect to coordinate j = (r,phi,z). Supply the phi derivative itself, not a derivative already divided by r.

## Newtonian stress: all six independent components

With total stress sigma = −p I + tau, dynamic shear viscosity mu, and bulk viscosity zeta, the **three-dimensional** constitutive law is

\[
\tau=2\mu D+\lambda\theta I,\qquad
\lambda=\zeta-\frac23\mu.
\]

Stokes’ hypothesis sets zeta = 0. It is a material assumption, distinct from imposing incompressibility theta = 0. Positive mu and nonnegative zeta ensure nonnegative viscous dissipation.

\[
\begin{aligned}
\tau_{rr}&=2\mu\,\partial_r u_r+\lambda\theta,\\
\tau_{\phi\phi}&=\frac{2\mu}{r}(u_r+\partial_\phi u_\phi)+\lambda\theta,\\
\tau_{zz}&=2\mu\,\partial_z u_z+\lambda\theta,\\
\tau_{r\phi}&=\mu\left(\partial_r u_\phi-\frac{u_\phi}{r}
+\frac{\partial_\phi u_r}{r}\right),\\
\tau_{rz}&=\mu(\partial_z u_r+\partial_r u_z),\\
\tau_{\phi z}&=\mu\left(\partial_z u_\phi+\frac{\partial_\phi u_z}{r}\right).
\end{aligned}
\]

The lower indices here label **physical components**, not covariant coordinate-basis components. Off-diagonal engineering shear rates are twice the corresponding D component; applying another factor of two to the formulas above would be an error.

## Stress divergence: the viscous force per volume

For a symmetric physical stress tensor, f = div(tau) has components

\[
\begin{aligned}
f_r&=\partial_r\tau_{rr}+\frac1r\partial_\phi\tau_{r\phi}
+\partial_z\tau_{rz}+\frac{\tau_{rr}-\tau_{\phi\phi}}r,\\
f_\phi&=\partial_r\tau_{r\phi}+\frac1r\partial_\phi\tau_{\phi\phi}
+\partial_z\tau_{\phi z}+\frac{2\tau_{r\phi}}r,\\
f_z&=\partial_r\tau_{rz}+\frac1r\partial_\phi\tau_{\phi z}
+\partial_z\tau_{zz}+\frac{\tau_{rz}}r.
\end{aligned}
\]

The acceleration contribution is f/rho. Pressure contributes −grad(p) separately. These divergence formulas allow spatially variable mu and zeta when stress derivatives include their variation. In the Python routine, `partials[...,i,j,k]` is the coordinate derivative k of physical stress component (i,j).

## Constant viscosity and the vector Laplacian

Only for constant mu and lambda can the force be simplified to

\[
f=\mu\nabla^2 u+(\mu+\lambda)\nabla\theta.
\]

For a scalar g, let

\[
\Delta_s g=\frac1r\partial_r(r\partial_r g)
+\frac1{r^2}\partial_\phi^2g+\partial_z^2g.
\]

The physical components of the **vector** Laplacian are

\[
\begin{aligned}
(\nabla^2u)_r&=\Delta_su_r-\frac{u_r}{r^2}
-\frac2{r^2}\partial_\phi u_\phi,\\
(\nabla^2u)_\phi&=\Delta_su_\phi-\frac{u_\phi}{r^2}
+\frac2{r^2}\partial_\phi u_r,\\
(\nabla^2u)_z&=\Delta_su_z.
\end{aligned}
\]

For incompressible constant-viscosity flow, theta vanishes, but the radial and azimuthal vector-Laplacian metric terms remain. For variable coefficients, pulling mu outside derivatives omits terms 2D·grad(mu) and theta grad(lambda). Evaluate the full stress divergence instead.

## Axisymmetry, polar slices, and material acceleration

Axisymmetry removes phi derivatives, **not** the terms u_r/r, −u_phi/r, or the stress-divergence metric terms. Axisymmetric flow may still have swirl. For a planar polar slice of a three-dimensional Newtonian fluid, retain the 2mu/3 bulk correction and tau_zz = lambda theta. A genuinely two-dimensional constitutive model uses a different deviatoric trace subtraction and must be declared separately.

The scalar advective derivative is D_s/Dt = partial_t + u_r partial_r + (u_phi/r) partial_phi + u_z partial_z. Vector material acceleration has extra radial and azimuthal terms:

\[
a_r=\frac{D_su_r}{Dt}-\frac{u_\phi^2}{r},\qquad
a_\phi=\frac{D_su_\phi}{Dt}+\frac{u_ru_\phi}{r},\qquad
a_z=\frac{D_su_z}{Dt}.
\]

These inertial terms are different from viscous metric terms.

## Coordinate-basis tensors and transformations

The cylindrical coordinate basis is (partial_r,partial_phi,partial_z) = (e_r,r e_phi,e_z), with metric diag(1,r²,1). Thus physical u_phi = r u^phi, and physical tau_phi,phi = r² tau^{phi,phi} = tau_{phi,phi}^{coordinate}/r². Covariant, contravariant, and physical arrays cannot be substituted for one another without these factors.

Nonzero Christoffel symbols include Gamma^r_phi,phi = −r and Gamma^phi_r,phi = Gamma^phi_phi,r = 1/r. Covariant differentiation accounts for the same basis changes included explicitly above. The Cartesian transformation uses the orthogonal matrix Q with columns e_r, e_phi, e_z: L_cart = Q L_cyl Q^T and tau_cart = Q tau_cyl Q^T.

## Analytic checks and the axis

- **Rigid rotation:** u_phi = Omega r gives antisymmetric L, D = 0, and zero viscous stress. Using partial_r u_phi alone would incorrectly create shear.
- **Pipe Poiseuille flow:** u_z = Umax(1−r²/R²) gives tau_rz = −2 mu Umax r/R² and f_z = −4 mu Umax/R². Steady axial momentum requires dp/dz = f_z.
- **Circular Couette flow:** u_phi = A r+B/r gives tau_rphi = −2 mu B/r² and zero azimuthal viscous-force divergence away from boundaries.
- **Cartesian affine fields:** random constant Cartesian velocity gradients are transformed into cylindrical data and back. Constant Cartesian stresses have zero divergence after angular basis derivatives are included.

The tests also verify the dissipation identity

\[
\tau:D=2\mu D_{\rm dev}:D_{\rm dev}+\zeta\theta^2\ge0.
\]

These routines require r > 0. At the axis, use regularity and analytic limits rather than replacing r by a small arbitrary number. For a smooth axisymmetric field, u_r and u_phi are O(r), and u_z = u_z(0)+O(r²). Then the axial scalar radial Laplacian tends to 2 partial_r² u_z. Nonaxisymmetric regular Cartesian fields have different component limits; even uniform Cartesian translation need not have u_r = O(r).

```python
import numpy as np
from numart.coordinates import cylindrical_velocity_gradient, newtonian_stress
r, omega = 0.7, 2.0
u = np.array([0., omega*r, 0.])
du = np.zeros((3,3)); du[1,0] = omega
L = cylindrical_velocity_gradient(r, u, du)
assert np.allclose(newtonian_stress(L), 0.)
```

The code checks tensor identities at supplied points. A cylindrical Navier–Stokes PDE solver, axis boundary scheme, and spherical-coordinate implementation remain future work.
