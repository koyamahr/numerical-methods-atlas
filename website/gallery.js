/** Dimensions describe solved spatial fields, never the number of plot axes. */
export function matchesGallery(figure, dimension='fields', category='All figures') {
  const spatial = dimension === 'all' || (dimension === 'fields'
    ? [2, 3].includes(figure.dimension) : figure.dimension === Number(dimension));
  return spatial && (category === 'All figures' || figure.category === category);
}

export const fieldFigures = [
  {file:'shock-methods/planar-128-0.png',dimension:2,year:'ROE / HLL / HLLE / AUSM',title:'When neighboring shock rows decouple',category:'2D shock interactions',chapter:'carbuncle',shockmethod:'shock-robustness',description:'A controlled stationary Mach-6 odd–even diagnostic. Compare fluxes, unperturbed controls, two grids and two subcell shock positions; no carbuncle-free claim.'},
  {file:'comparisons/wedge-m2-mc.png',comparison:'wedge-m2',dimension:2,year:'NASA / MACH 2',title:'NASA wedge / Mach 2.0',
    category:'2D shock interactions',chapter:'nasa-2d',
    description:'Compare first-order, minmod and MC reconstruction on the NASA wedge. Same HLL flux, SSPRK2 and grids; exact weak-shock line and two-grid density errors.'},
  {file:'comparisons/wedge-m2.5-mc.png',comparison:'wedge-m2.5',dimension:2,year:'NASA / MACH 2.5',title:'NASA wedge / Mach 2.5',
    category:'2D shock interactions',chapter:'nasa-2d',
    description:'Compare first-order and MUSCL Mach/pressure fields, shock angle and wall pressure against the oblique-shock reference. Independent Euler calculations, not Wind-US output.'},
  {file:'comparisons/step-m3-mc.png',comparison:'forward-step',dimension:2,year:'CLASSICAL / MACH 3',title:'Mach 3 / forward-facing step',
    category:'2D shock interactions',chapter:'nasa-2d',movie:'forward-step',
    description:'First-order and MUSCL minmod/MC shock reflections, with side-by-side 81-state clips to t = 4 on common color scales. No step-corner entropy reset.'},
  {file:'movies/double-mach/frame-080.webp',dimension:2,year:'1984',title:'Double Mach Reflection',
    category:'2D shock interactions',chapter:'double-mach',movie:'double-mach',
    description:'2D Mach-10 shock reflection on 256 × 64 cells. Open the saved-state movie; first-order HLL is a diffusive baseline.'},
  {file:'mhd-tests/field-loop.png',dimension:2,year:'HLLD / HLLE / CT / GLM',title:'Advect a magnetic field loop',category:'MHD',chapter:'mhd',mhdtest:'field-loop',description:'Weak-field loop over one periodic transit. Compare HLLD/HLLE with CT-Contact and GLM; native divergence and initial magnetic discretizations differ.'},
  {file:'movies/orszag-tang-ct/frame-080.webp',dimension:2,year:'1979',title:'Orszag–Tang / constrained transport',
    category:'MHD',chapter:'mhd',movie:'orszag-tang-ct',
    description:'2D periodic MHD on 64 × 64 cells. CT uses a staggered magnetic field and its native face-divergence operator.'},
  {file:'movies/orszag-tang-glm/frame-080.webp',dimension:2,year:'2002',title:'Orszag–Tang / GLM cleaning',
    category:'MHD',chapter:'mhd',movie:'orszag-tang-glm',
    description:'2D periodic MHD on 64 × 64 cells. Inspect GLM time evolution; its cell-centered divergence is distinct from CT.'},
  {file:'movies/keep-vortex/frame-080.webp',dimension:2,year:'2018',title:'KEEP / a moving smooth vortex',
    category:'Advection & stability',chapter:'keep',movie:'keep-vortex',
    description:'2D Euler vortex on 96 × 96 cells. Original Cartesian KEEP with RK4; smooth-flow test without shock stabilization.'},
  {file:'field-fem-poisson.png',dimension:2,year:'STEADY FIELD',title:'Poisson on triangular elements',
    category:'Elliptic & iterative',chapter:'fem',
    description:'2D P1 finite elements: computed solution and nodal error on 1152 triangles. Continuous L2/H1 errors use inside-element quadrature.'},
  {file:'field-taylor-green.png',dimension:2,year:'t = 0.5',title:'Taylor–Green / speed and pressure',
    category:'Elliptic & iterative',chapter:'incompressible',
    description:'2D periodic MAC projection on 64 × 64 cells. Velocity arrows are averaged to cell centers; diagnostics use native face velocities.'},
  {file:'field-poisson-3d.png',dimension:3,year:'STEADY FIELD / SLICES',title:'A 3D Poisson field in three slices',
    category:'Particles & gravity',chapter:'particle-gravity',
    description:'3D periodic FFT Poisson on a 32 × 32 × 32 mesh, checked against one exact Fourier mode. Three orthogonal potential slices; no 3D fluid evolution.'}
];
