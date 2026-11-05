# Structured, unstructured, and triangular meshes

A mesh describes geometry **and connectivity**. Cell shape and indexing are different choices: triangles may be obtained by splitting a structured lattice, or connected in an irregular unstructured triangulation. The [mesh explorer](https://koyamahr.github.io/numerical-methods-atlas/#/meshes) makes this distinction visible.

## Structured meshes

A logically rectangular mesh admits indices (i,j) and predictable neighboring indices. Cartesian rectangles are the simplest example, but a body-fitted curvilinear mesh may retain structured indexing. Metric terms, face normals, and cell volumes then come from its geometry. Multiblock grids join several such index spaces.

The explorer’s first example has 8 × 6 rectangular cells on the unit square. Connectivity is still exported explicitly so that the same inspection code can handle every example.

## Triangles and unstructured connectivity

Splitting each rectangle into two triangles changes the cell shape while preserving an underlying lattice pattern. The third example instead triangulates deterministic irregular interior points and a fixed square boundary. It uses [Matplotlib’s Delaunay triangulation](https://matplotlib.org/stable/api/tri_api.html), not a call to the Triangle package. [Shewchuk’s Triangle paper](https://www.cs.cmu.edu/~quake/tripaper/triangle0.html) is a historical and algorithmic reading reference.

An unstructured solver normally stores vertices, cells, faces, and owner/neighbor relationships. Boundary faces have one adjacent cell; interior faces have two. The explorer highlights **face-sharing neighbors**, not every cell that merely touches a vertex. Labels are vertex-average cell centers; for triangles these equal the area centroids.

## Conservation is a face contract

For a finite volume K with area |K|,

\[
\frac{d}{dt}(|K|\overline U_K)
=-\sum_{f\subset\partial K}|f|\,\widehat F(U_K,U_{K_f};n_{K,f}).
\]

An interior face contributes equal and opposite fluxes to its two cells. This cancellation is independent of whether K is a quadrilateral or triangle. With counterclockwise vertices, an edge displacement (dx,dy) has outward unit normal (dy,−dx)/length. Signed polygon areas detect reversed or degenerate cells.

## Quality and implementation scope

Small angles, skewness, aspect ratio, nonorthogonality, and volume variation influence reconstruction and stability differently. Delaunay connectivity alone does not guarantee adequate boundary-layer resolution or a suitable minimum angle for arbitrary point sets. No mesh-quality optimization is performed here.

`numart.geometry.example_meshes` supplies the three examples. Tests verify positive cell areas, unit total area, connected face-neighbor graphs, reciprocal adjacency, and the planar Euler relation V−E+F_cells = 1 for these simply connected domains. The explorer is a geometry/connectivity demonstration; an unstructured Euler or viscous flow solver remains future work.

Continue with [ALE moving cells](ale.md), [SPH particles](particles-sph.md), and [cylindrical metrics and tensors](coordinates-viscosity.md).

## Variable staggering is another choice

[Arakawa A/B/C placement](geophysical-grids.md) specifies which variables
occupy centers, corners and faces on a given mesh. It is independent of
structured versus unstructured connectivity and of temporal order. The new
chapter connects the existing MAC layout to rotating shallow-water waves,
with explicit Coriolis averaging and tested Fourier symbols.
