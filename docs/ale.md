# Arbitrary Lagrangian–Eulerian methods

Eulerian cells stay fixed while fluid crosses their faces. Lagrangian cells move with the fluid. In ALE, the mesh velocity w can be chosen independently of the fluid velocity u. [Hirt, Amsden, and Cook (1974)](https://doi.org/10.1016/0021-9991(74)90051-5) provide a classical all-speed ALE formulation.

## The flux is relative to the moving face

Reynolds transport gives, for a moving control volume K(t),

\[
\frac{d}{dt}\int_{K(t)}U\,dV
+\int_{\partial K(t)}\left[F(U)\cdot n-(w\cdot n)U\right]dS=0.
\]

With w = 0 this is Eulerian. Choosing the normal mesh speed equal to the fluid normal speed gives the Lagrangian mass-flux limit. Pressure still transfers momentum and energy across a material face; setting mass flux to zero does not set every Euler flux to zero.

## Geometry must obey a conservation law too

For a uniform state to remain uniform, changing cell volumes and face motion must agree:

\[
\frac{d|K|}{dt}=\int_{\partial K}w\cdot n\,dS.
\]

Its discrete counterpart is the geometric conservation law (GCL). A mesh-motion routine and a flow update that use inconsistent swept volumes can create a spurious flow from constant data, even if each looks accurate separately.

## A reproducible one-step check

`numart.geometry.moving_volume_uniform_test` deforms faces on [0,1] by a smooth sinusoidal displacement with fixed endpoints. Face velocity is the actual displacement divided by delta t. For constant scalar q, it updates the extensive quantity Vq with relative flux (a−w)q and divides by the new volume. The same displacement appears in both operations.

```python
import numpy as np
from numart.geometry import moving_volume_uniform_test
old_faces, new_faces, q = moving_volume_uniform_test(phase=0.8)
print(np.max(np.abs(q - 1)))
```

Uniform-state preservation is checked to roundoff over several deformation phases. The amplitude restriction ensures positive cell widths. This is a **1D moving-volume identity check**, not an ALE Euler solver or a test of accuracy for nonuniform data.

## Mesh motion, remapping, and distortion

A complete ALE method may move vertices, solve a Lagrangian or relative-flux step, and remap to a better mesh. Conservative remapping, mesh tangling, boundary motion, and temporal consistency require additional tests. A remap that preserves total mass can still violate positivity or fail to preserve a constant state.

Use the [mesh chapter](meshes.md) to separate topology from motion, and the [coordinate chapter](coordinates-viscosity.md) to distinguish moving control volumes from changing tensor bases. Neither replacing x by r nor moving plotted vertices automatically constructs an ALE method.
