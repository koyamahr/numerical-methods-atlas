/** Dimensions describe solved spatial fields, never the number of plot axes. */
export function matchesGallery(figure, dimension='fields', category='All figures') {
  const spatial = dimension === 'all' || (dimension === 'fields'
    ? [2, 3].includes(figure.dimension) : figure.dimension === Number(dimension));
  return spatial && (category === 'All figures' || figure.category === category);
}

export const fieldFigures = [
  {file:'movies/double-mach/frame-080.webp',dimension:2,year:'1984',title:'Double Mach Reflection',
    category:'2D shock interactions',chapter:'double-mach',movie:'double-mach',
    description:'2D Mach-10 shock reflection on 256 × 64 cells. Open the saved-state movie; first-order HLL is a diffusive baseline.'},
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
