import {glossaryPage,wireGlossary} from './glossary.js';
import {configureLocale,currentLanguage,resolveLanguage,t,translateText,localizeTree,observeLocalization,languageURL,captureControls,restoreControls} from './i18n.js';
import {coverageHighlights,coveragePage,wireCoverage} from './coverage.js';
import {equationsPage,wireEquations,disposeEquations} from './equations.js';
import {basisPage,wireBasis} from './basis.js';
import {cipPage,wireCIP} from './cip.js';
import {rkPage,wireRK} from './runge-kutta.js';
import {limiterPage,wireLimiters} from './limiters.js';
import {moviesPage,wireMovies,disposeMovies} from './movies.js';
import {fieldFigures,matchesGallery} from './gallery.js';
import {flowPage,wireFlow,mhdPage,wireMHD,disposeComparisons} from './comparisons.js';
import {reconstructionPage,wireReconstruction,robustnessPage,wireRobustness} from './shock-methods.js';
import {poissonPage,wirePoisson} from './poisson.js';
import {wireBookCovers} from './books.js';
import {hamiltonianPage,wireHamiltonian} from './hamiltonian.js';
import {timePage,meshPage,wireTime,wireMesh} from './foundations.js';
import {stabilityPage,convergencePage,wireStability,wireConvergence} from './experiments.js';
const main = document.querySelector('main');
let repo = 'https://github.com/koyamahr/numerical-methods-atlas', site;
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const methods = [
  {id:'stability',number:'01',title:'Differences & stability',subtitle:'Start with the stencil.',description:'Follow information through a grid. Separate spatial differences, time integration, the CFL condition, and linear stability.',formula:'uₜ + a uₓ = 0',tag:'FINITE DIFFERENCES'},
  {id:'benchmarks',number:'02',title:'Conservation laws',subtitle:'Resolve the waves.',description:'From Godunov-type finite volumes to MUSCL and WENO. Compare numerical fluxes on shared, precisely defined problems.',formula:'Uₜ + F(U)ₓ = 0',tag:'FINITE VOLUMES · WENO'},
  {id:'elliptic',number:'03',title:'Diffusion & elliptic solvers',subtitle:'Let the errors relax.',description:'Boundary conditions, implicit steps, tridiagonal elimination, iterative matrices, and a geometric multigrid V-cycle.',formula:'−∇²u = f',tag:'THOMAS · CG · MULTIGRID'},
  {id:'benchmarks',number:'04',title:'DG & spectral methods',subtitle:'Choose your basis.',description:'Local Legendre polynomials meet global Fourier modes in periodic linear advection, with exact translation as a reference.',formula:'uₕ = ∑ ûₖ φₖ',tag:'LOCAL & GLOBAL BASES'},
  {id:'mhd',number:'05',title:'Magnetic constraints',subtitle:'Keep the field in balance.',description:'Compare full-vector HLLD/HLLE standard tests, contact-upwinded CT and GLM cleaning. Each divergence measurement retains its discrete operator.',formula:'∇ · B = 0',tag:'IDEAL MHD · HLLD · CT · GLM'},
  {id:'advanced',number:'06',title:'Beyond the explicit step',subtitle:'Iterate in another time.',description:'Minimal models for dual time stepping, matrix preconditioning, and scalar residual distribution, with their limits made explicit.',formula:'∂Q/∂τ + R*(Q) = 0',tag:'ADVANCED MODELS'},
  {id:'time-integration',number:'07',title:'Time integration & leapfrog',description:'Compare twelve temporal methods on an oscillator; distinguish the physical and computational roots.',formula:'ξ² − 2z ξ − 1 = 0',tag:'ODE · TWO-STEP MODES'},
  {id:'meshes',number:'08',title:'Meshes & connectivity',description:'Structured quadrilaterals, split-lattice triangles, and irregular triangulations. Inspect face-sharing neighbors.',formula:'V − E + F = 1',tag:'STRUCTURED · UNSTRUCTURED'},
  {id:'particles-sph',number:'09',title:'Particles & SPH',description:'Kernel reconstruction, particle volume weights, normalization, and the additional requirements of fluid dynamics.',formula:'fₕ ≈ ∑ (m/ρ) f W',tag:'PARTICLE METHODS'},
  {id:'ale',number:'10',title:'Moving volumes & ALE',description:'Follow the relative face flux and test uniform-state preservation under mesh motion.',formula:'F · n − (w · n) U',tag:'GEOMETRIC CONSERVATION'},
  {id:'coordinates-viscosity',number:'11',title:'Coordinates, tensors & viscosity',description:'Physical cylindrical components, all six viscous stresses, tensor divergence, and analytic checks.',formula:'τ = 2μD + λ(∇ · u)I',tag:'POLAR · CYLINDRICAL'},
  {id:'double-mach',number:'12',title:'Double Mach Reflection',description:'An actual 2D Euler shock-reflection computation, with moving boundaries, a run manifest, and explicit resolution limits.',formula:'Uₜ + Fₓ + Gᵧ = 0',tag:'MACH 10 · COMPUTED'},
  {id:'carbuncle',number:'13',title:'The carbuncle phenomenon',description:'Strong-shock instability, transverse dissipation, and why entropy correction and positivity are different tests.',formula:'∣λ̃ₖ∣ αₖ r̃ₖ',tag:'MULTIDIMENSIONAL ROBUSTNESS'},
  {id:'symplectic',number:'14',title:'Symplectic Hamiltonian maps',description:'Canonical structure, Verlet and Yoshida compositions, time reversal, and long-time energy errors.',formula:'Mᵀ J M = J',tag:'GEOMETRIC INTEGRATION'},
  {id:'particle-gravity',number:'15',title:'Particle gravity & Poisson',description:'CIC particle–mesh forces, P³M and TreePM splitting, octrees, multipole moments, and multigrid.',formula:'∇²φ = 4πGρ',tag:'PM · TREE · MULTIPOLES'},
  {id:'gravity-boundaries',number:'16',title:'Isolated & slab gravity',description:'Hockney–Eastwood convolution and Koyama–Ostriker slab kernels, with explicit Fourier and zero-mode conventions.',formula:'Gₖ(z) ∝ exp(−k|z|)',tag:'FFT · GREEN FUNCTIONS'},
  {id:'limiters',number:'17',title:'Slope limiters & TVD',description:'Compare minmod, Superbee, MC, van Leer, and van Albada on common scalar and Euler tests.',formula:'s = φ(r) Δ⁺u',tag:'MUSCL · SWEBY'},
  {id:'advanced-limiters',number:'18',title:'TVB & positive-state scaling',description:'Relax smooth extrema with modified minmod, then scale Euler reconstruction states while preserving a consistent conservative mean.',formula:'Û = Ū + θ(U − Ū)',tag:'ADVANCED · ADMISSIBILITY'},
  {id:'keep',number:'19',title:'KEEP & smooth-flow structure',description:'Original Kuya–Totani–Kawai flux, isentropic vortex refinement, entropy diagnostics, and explicit shock/positivity caveats.',formula:'Fᴱ = C(½uᴸ · uᴿ + ē) + P',tag:'LOW DISSIPATION · EULER'},
  {id:'runge-kutta',number:'20',title:'Runge–Kutta families',description:'RK2 variants, classical RK4, SSPRK stages and orders, Butcher tableaus, linear stability contours, and nonlinear tests.',formula:'h ≤ C h_FE',tag:'STAGES · ORDER · SSP'},
  {id:'cip',number:'21',title:'CIP / value and gradient',description:'Characteristic cubic-Hermite transport, evolved derivatives, sharp-profile oscillations, refinement, and a conservation counterexample.',formula:'fⁿ⁺¹ = P(x − aΔt)',tag:'SEMI-LAGRANGIAN · HERMITE'},
  {id:'gsph',number:'22',title:'Inutsuka’s Godunov SPH',description:'Convolution, pair Riemann states, conservative particle updates, and the MHD/SR branches. Source notes and an implementation plan.',formula:'P*ᵢⱼ · V²ᵢⱼ ∇W',tag:'PARTICLES · READING NOTES'},
  {id:'relativistic-hydrodynamics',number:'23',title:'Relativistic fluid methods',description:'From SR Riemann solvers and Valencia to GRMHD, primitive recovery, high-order hybrids, radiation, and GPU merger codes. Literature through November 2026.',formula:'∇ · T = 0',tag:'SRHD · GRHD · GRMHD · READING'},
  {"id": "fem", "number": "24", "title": "Continuous finite elements", "description": "Weak forms, triangular P1 assembly, Dirichlet elimination, and measured L2/H1 convergence.", "formula": "Kᵢⱼ = ∫ ∇φᵢ · ∇φⱼ", "tag": "ASSEMBLY · POISSON"},
  {"id": "sparse-nonlinear", "number": "25", "title": "Sparse & nonlinear systems", "description": "Restarted GMRES, BiCGSTAB, Jacobi, ILU(0), and damped Newton with true-residual verification.", "formula": "A M⁻¹z = b", "tag": "KRYLOV · NEWTON"},
  {"id": "stiff-integration", "number": "26", "title": "Stiff & adaptive integration", "description": "BE, BDF2, L-stable SDIRK2, IMEX Euler, and step-doubling error control.", "formula": "yₙ₊₁ − h f(yₙ₊₁) = yₙ", "tag": "IMPLICIT STAGES"},
  {"id": "incompressible", "number": "27", "title": "Incompressible projection", "description": "Compatible MAC divergence/gradient, discrete FFT Poisson, and periodic Taylor–Green refinement.", "formula": "D(u* − Gφ) = 0", "tag": "MAC · PROJECTION"},
  {"id": "lattice-boltzmann", "number": "28", "title": "Lattice Boltzmann / D2Q9", "description": "BGK collision, Guo forcing, shear viscosity, and half-way-wall Poiseuille verification.", "formula": "ν = cₛ²(τ − ½)", "tag": "KINETIC · LOW MACH"},
  {"id": "chapman-enskog", "number": "29", "title": "Chapman–Enskog expansion", "description": "Slow scales, nonequilibrium stress, hydrodynamic moments and the lattice-time half-step correction.", "formula": "f = f⁽⁰⁾ + εf⁽¹⁾ + …", "tag": "ASYMPTOTIC DERIVATION"},
  {"id": "hyperbolic-diffusion", "number": "30", "title": "Nishikawa / hyperbolic diffusion", "description": "An equivalent first-order steady system with a tested 1D upwind baseline and RD source notes.", "formula": "p_τ − uₓ/Tᵣ = −p/Tᵣ", "tag": "PSEUDO-TIME · DIFFUSION"},
  {"id": "equation-gallery", "number": "31", "title": "Burgers & traffic equations", "description": "Entropy shocks and rarefactions, upstream traffic jams, exact cell averages and fluid-system profiles.", "formula": "ρₜ + [ρ(1−ρ)]ₓ = 0", "tag": "EQUATION GALLERY"},
  {"id": "biological-models", "number": "32", "title": "Biological model equations", "description": "Twenty-two literature-only model families: growth, epidemics, reaction–diffusion, chemotaxis, excitable membranes, delayed and stochastic gene networks, and biomechanics.", "formula": "uₜ = D∇²u + f(u)", "tag": "BIOLOGY · SURVEY / NO SOLVER"},
  {"id": "geophysical-grids", "number": "33", "title": "Spherical meshes & Arakawa grids", "description": "Compare Yin–Yang, cubed-sphere and icosahedral geometry, then inspect A/B/C placement and tested f-plane wave symbols.", "formula": "ωₕ² = fₕ² + c²(k̃² + ℓ̃²)", "tag": "GEOPHYSICS · LINEAR SYMBOLS"},
  {id:'basis-functions',number:'34',title:'Orthogonal polynomials & element bases',description:'Legendre modes, nodal Lagrange functions, Gauss and GLL quadrature, exact versus lumped mass, and triangular shape functions.',formula:'∫ Pᵢ Pⱼ = 2δᵢⱼ/(2i+1)',tag:'MODES · NODES · ELEMENTS'}
];
const figures = [
 {file:"spherical-meshes.png",year:"1996–2004",title:"Cover a sphere without polar convergence",category:"Advection & stability",chapter:"geophysical-grids",description:"Latitude–longitude, Yin–Yang, cubed-sphere and icosahedral geometry. Schematics show overlap, panel seams and five-valent vertices; no new flow simulation."},
 {file:"spherical-dual.png",year:"GEOMETRY",title:"Triangles, pentagons and hexagons",category:"Advection & stability",chapter:"geophysical-grids",description:"The same refined icosahedron and its barycentric dual. Twelve pentagons replace sixfold connectivity; the diagram is not an optimized Voronoi grid."},
 ...fieldFigures,
 {file:'basis.png',year:'Reference-element algebra',title:'A mesh needs a basis',category:'Elliptic & iterative',chapter:'basis-functions',description:'Legendre modes, GLL cardinal functions, exact nodal mass, smooth and discontinuous approximation, and a triangular P2 edge function.'},
 {"file": "geophysical-grids.png", "year": "1977", "title": "Stagger the variables. Change the waves.", "category": "Advection & stability", "chapter": "geophysical-grids", "description": "A/B/C placements and four semi-discrete shallow-water dispersion cuts, with the Coriolis interpolation and deformation-radius ratio stated."},
 {"file": "equation-gallery.png", "year": "1948–1956", "title": "Equations and their waves", "category": "Conservation laws", "chapter": "equation-gallery", "description": "Burgers shocks/fans, upstream traffic jams, translation and physical heat diffusion against exact cell averages."},
 {"file": "solver-foundations.png", "year": "1943–1992", "title": "From a weak form to a projection", "category": "Elliptic & iterative", "chapter": "fem", "description": "Triangular FEM, true Krylov residuals, stiff ODE refinement, and periodic MAC Taylor–Green verification."},
 {"file": "kinetic-hyperbolic.png", "year": "1992–2007", "title": "Kinetic and hyperbolic routes", "category": "Elliptic & iterative", "chapter": "lattice-boltzmann", "description": "D2Q9 shear decay, half-way-wall Poiseuille profiles, and an explicitly scoped hyperbolic-diffusion baseline."},
 {file:'cip.png',title:'CIP carries the gradient',category:'Advection & stability',year:'1985–2001',description:'Original cubic-Hermite CIP with smooth and square profiles, independently evolved gradients, and an analytic conservation counterexample.',chapter:'cip'},
 {file:'runge-kutta.png',title:'Runge–Kutta family relationships',category:'Advection & stability',year:'2001–2009',description:'Nine explicit RK methods: shared linear stability polynomials, different nonlinear stages, measured orders, and conditional SSP bounds.',chapter:'runge-kutta'},
 {file:'limiters.png',title:'Choose the slope limiter',category:'Conservation laws',year:'1974–2010',description:'Five slope choices on the same periodic pulse and Sod problem, plus smooth-wave refinement. TVB and positive reconstruction have a separate advanced explanation.',chapter:'limiters'},
 {file:'keep-vortex.png',title:'KEEP on a smooth vortex',category:'Advection & stability',year:'2018–2024',description:'Original second-order Cartesian KEEP + RK4: smooth-vortex refinement and approximate entropy preservation. No shock stabilization or pressure-equilibrium extension.',chapter:'keep',movie:'keep-vortex'},
 {file:'hamiltonian.png',title:'Canonical maps and energy',category:'Particles & gravity',year:'1990–2003',description:'Five fixed-step integrators on harmonic and quartic Hamiltonians. Energy histories to T=200 and phase orbits to T=10; no equal-cost ranking.',chapter:'symplectic'},
 {file:'particle-gravity.png',title:'PM, Tree, and multipole forces',category:'Particles & gravity',year:'1981–2005',description:'An isolated octree compared with the same softened direct force sum, and a separate periodic CIC/FFT Poisson example.',chapter:'particle-gravity'},
 {file:'gravity-boundaries.png',title:'Gravity follows the boundary',category:'Particles & gravity',year:'1981–2009',description:'Isolated doubled-grid convolution, a slab mean mode, and a sinusoidal sheet. Sampled DFT and continuous coefficients are distinct.',chapter:'gravity-boundaries'},
 {file:'sod.png',title:'Sod shock tube',category:'Conservation laws',year:'1978',description:'Four numerical fluxes meet the exact density, velocity, and pressure profiles.',chapter:'benchmarks'},
 {file:'shu-osher.png',title:'Shock meets a density wave',category:'Conservation laws',year:'1989',description:'MUSCL and WENO5-JS on the Shu–Osher problem. A numerical comparison, without an exact final-time reference.',chapter:'benchmarks'},
 {file:'dg-spectral.png',title:'Local polynomials, global waves',category:'Advection & stability',year:'1973–1977',description:'Periodic DG and Fourier advection, plus DG grid refinement. Degrees of freedom and costs are not matched.',chapter:'benchmarks'},
 {file:'stability.png',title:'The shape of stability',category:'Advection & stability',year:'1928–1960',description:'Fourier amplification and a seeded Nyquist mode reveal the effect of the Courant number.',chapter:'stability'},
 {file:'reconstruction/reconstruction.png',title:'PPM, characteristics and WENO-Z',category:'Conservation laws',year:'1984–2008',chapter:'reconstruction',shockmethod:'reconstruction',description:'Sod, a moving contact and Shu–Osher; compare conservative components and characteristics, then compare fluxes including an explicit AUSM baseline.'},
 {file:'mhd-tests/brio-wu.png',dimension:1,title:'Brio–Wu / HLLD and HLLE',category:'MHD',year:'1988',chapter:'mhd',mhdtest:'brio-wu',description:'Full-vector coplanar MHD shock tube at gamma 2, with MC reconstruction, SSPRK2 and numerical grid comparisons. No exact-reference overlay.'},
 {file:'mhd-tests/alfven.png',dimension:1,title:'A circularly polarized Alfvén wave',category:'MHD',year:'EXACT PERIODIC WAVE',chapter:'mhd',mhdtest:'alfven',description:'One full period against exact conservative cell averages, with transverse vectors and four-grid HLLD/HLLE refinement.'},
 {file:'glm-cleaning.png',title:'Where divergence errors go',category:'MHD',year:'2002',description:'A longitudinal magnetic error is injected into OT data to isolate propagation and damping.',chapter:'mhd'},
 {file:'diffusion-boundaries.png',title:'The boundary changes the problem',category:'Elliptic & iterative',year:'1947',description:'Diffusion time integrators and three Poisson boundary-condition sets for a manufactured solution.',chapter:'elliptic'},
 {file:'poisson-comparison/overview.png',title:'One Poisson system, different solvers',category:'Elliptic & iterative',year:'DIRECT / RELAXATION / KRYLOV / MULTILEVEL',chapter:'elliptic',experiment:'poisson-comparison',description:'Compare true residuals, same-system errors and three-trial timings. Includes Jacobi, red-black GS/SOR, CG, V-cycles, FFT/DST and separable DST+Thomas.'},
 {file:'multigrid-radius.png',title:'From smoothing to correction',category:'Elliptic & iterative',year:'1961–1977',description:'Geometric multigrid residuals and the spectral radius of stationary iteration matrices.',chapter:'elliptic'},
 {file:'implicit.png',title:'A second clock',category:'Elliptic & iterative',year:'1991',description:'Pseudo-time residuals for BDF2 advection and symmetric Jacobi scaling of an SPD model matrix.',chapter:'advanced'},
 {file:'lax-entropy.png',title:'Shocks and smooth refinement',category:'Conservation laws',year:'1954',description:'The Lax shock tube and pointwise density error for a periodic Euler entropy wave.',chapter:'benchmarks'},
 {file:'barotropic.png',title:'Two barotropic systems',category:'Conservation laws',year:'MODEL COMPARISON',description:'Shallow-water dam break and isothermal Euler. Exact Riemann references are future work.',chapter:'benchmarks'}
];
const eras = [
 ["1838–1927", "Population, cohorts and epidemics", "Verhulst · Lotka · Volterra · McKendrick · Kermack", "Read positive-state population models, renewal boundaries and epidemic invariants. Survey entries, not implemented biological solvers.", "biological-models", "lotka1920"],
 ["1937–1979", "Fronts, excitation and morphogenesis", "Fisher · Turing · Hodgkin–Huxley · FitzHugh–Nagumo · Keller–Segel", "A biological equation map connects stiff reactions, diffusion, directed migration and pattern onset. Literature-only model catalog.", "biological-models", "turing1952"],
 ["1977", "Place the variables before choosing the stencil", "Arakawa–Lamb", "Compare A/B/C placement and independently tested semi-discrete rotating shallow-water wave symbols; D/E remain reading notes.", "geophysical-grids", "arakawa1977"],
 ["1939–1943", "From asymptotics to a weak form", "Chapman–Cowling · Courant", "Separate kinetic and hydrodynamic scales; assemble continuous P1 elements from a variational problem.", "fem", "courant1943"],
 ["1948–1956", "A shock on the road", "Burgers · Lighthill–Whitham · Richards", "Compare convex and concave scalar fluxes, exact entropy fans and upstream traffic jams.", "equation-gallery", "lighthill1955"],
 ["1968", "Remove the discrete divergence", "Chorin", "Project a MAC velocity with compatible gradient and divergence operators and a discrete Poisson inverse.", "incompressible", "chorin1968"],
 ["1977", "An implicit stage for a stiff mode", "Alexander", "Explore L-stable SDIRK2, nonlinear stage residuals and separate adaptive time-error control.", "stiff-integration", "alexander1977"],
 ["1986–1992", "Minimize or stabilize the residual", "Saad–Schultz · van der Vorst", "Solve nonsymmetric sparse systems with fixed right preconditioning, true residuals and explicit failure reports.", "sparse-nonlinear", "saad1986"],
 ["1992–2002", "Collide, stream, then measure viscosity", "Qian–d’Humières–Lallemand · Guo–Zheng–Shi", "D2Q9 lattice BGK, force discretization, Chapman–Enskog moments and half-way-wall flow.", "lattice-boltzmann", "qian1992"],
 ["2007–2010", "Diffusion through a hyperbolic system", "Nishikawa", "Auxiliary gradients turn a steady second-order equation into a first-order system; distinguish the original RD from the local FV baseline.", "hyperbolic-diffusion", "nishikawa2007"],
 ['1928','The numerical domain of dependence','Courant, Friedrichs & Lewy','A discrete stencil must reach the information required by the continuous problem.','stability','cfl1928'],
 ['1947–1950','Diffusion, implicit steps, and stability','Crank–Nicolson · Thomas · Charney et al.','Connect time stepping to a linear-system solve, then ask what happens to each Fourier mode.','elliptic','crank1947'],
 ['1954–1961','Weak solutions and conservation form','Lax · Richtmyer · Godunov · Wendroff · Rusanov','Move from a difference formula to a conservative flux and the waves it resolves.','stability','godunov1959'],
 ['1961–1977','Different scales, different bases','Fedorenko · Reed–Hill · Gottlieb–Orszag · Brandt','Smooth fine-grid error, correct it on coarse grids, and explore local and global approximations.','elliptic','brandt1977'],
 ['1974–1977','Moving with the fluid, or moving the mesh','Hirt–Amsden–Cook · Gingold–Monaghan · Lucy','Separate mesh velocity from fluid velocity, then replace fixed connectivity by particle kernel sums.','ale','hirt1974'],
 ['1978–1983','A shared language of benchmarks','Sod · van Leer · Orszag–Tang · Roe · Harten et al.','Use common test problems to compare contacts, acoustic waves, and magnetic structures.','benchmarks','sod1978'],
 ['1981–1987','Particles, meshes, and far-field expansions','Hockney–Eastwood · Barnes–Hut · Greengard–Rokhlin','Assign mass to a grid, organize nearby particles in a tree, and reuse distant interactions through expansions.','particle-gravity','barnes1986'],
 ['1984–1989','Limit the oscillations, retain the smooth peaks','Sweby · Cockburn–Shu','Connect scalar TVD bounds to slope choices, then relax small extrema with a TVB threshold.','limiters','sweby1984'],
 ['1987–1989','Higher order and magnetic constraints','Harten et al. · Turkel · Einfeldt · Evans–Hawley · Shu–Osher','High order, positivity, entropy correction, and magnetic divergence become distinct design questions.','mhd','evans1988'],
 ['1990','Compose a canonical map','Yoshida','Build higher-order symplectic steps from symmetric lower-order maps, and separate energy error from geometry.','symplectic','yoshida1990'],
 ['1991–1996','Physical time and nonlinear weights','Jameson · Toro et al. · Liu–Osher–Chan · Jiang–Shu','Explore dual time, contact restoration, low-density flows, and WENO5-JS reconstruction.','advanced','jiang1996'],
 ['2000–2008','Multidimensional robustness','Tóth · Dedner et al. · Abgrall · Nishikawa–Kitamura','Examine discrete constraints and the path toward residual distribution and rotated-hybrid fluxes.','advanced','dedner2002'],
 ['2005–2009','The boundary is part of the force','Springel · Koyama–Ostriker','Split short and long ranges, then distinguish isolated kernels from periodic-horizontal disk gravity.','gravity-boundaries','koyama2009'],
 ['1994–1998','Relativistic conservative fluids','Martí–Müller · Banyuls et al. · Pons et al.','Follow conservative SR/GR fluids, magnetic constraints, state recovery, radiation, and evolving-spacetime GPU calculations. Source notes, not an implemented relativistic solver.','relativistic-hydrodynamics','banyuls1997'],
 ['1994–2026','Particles meet a Riemann problem','Inutsuka · Iwasaki · Kitajima · Seno','Trace GSPH through its detailed 2002 formulation, particle MHD, and special-relativistic SRGSPH. Literature and a staged implementation plan.','gsph','inutsuka2002']
].sort((a,b)=>parseInt(a[0],10)-parseInt(b[0],10));
let documents, references, sod, experiments, foundations, coverage, translationStatus, localeCatalog, glossary;
const documentCache = new Map();
const originalShell = new Map([...document.querySelectorAll('.site-header,.site-footer,#figure-dialog,.skip-link')].map(element => [element, element.innerHTML]));
let navigationVersion = 0, switching = false;
async function loadDocuments(language) {
 if (!documentCache.has(language)) documentCache.set(language, fetch(`content.${language}.json`).then(response => {if(!response.ok)throw Error('Cannot load reading language');return response.json();}).catch(error => {documentCache.delete(language);throw error;}));
 return documentCache.get(language);
}
function renderShell() {
 for (const [element, html] of originalShell) element.innerHTML = html;
 document.documentElement.lang = currentLanguage();
 document.querySelectorAll('[data-language]').forEach(button => {
  button.setAttribute('aria-pressed', String(button.dataset.language === currentLanguage()));
  button.addEventListener('click', () => changeLanguage(button.dataset.language));
 });
 document.querySelector('.mobile-menu').addEventListener('click',event=>{const open=document.querySelector('.site-header').classList.toggle('menu-open');event.currentTarget.setAttribute('aria-expanded',String(open));});
 document.querySelector('.dialog-close').addEventListener('click',()=>document.querySelector('#figure-dialog').close());
 const description = currentLanguage()==='ja' ? '方程式、数値計算法、原論文、再現可能なテスト計算をつなぐ数値計算アトラス。' : 'A living atlas of numerical algorithms. Explore the original papers, understand the methods, and inspect reproducible benchmark results.';
 document.querySelector('meta[name="description"]').content=description;
 document.querySelector('meta[property="og:description"]').content=description;
 document.querySelector('meta[property="og:title"]').content=site.title[currentLanguage()];
 localizeTree(document.body);
}
async function changeLanguage(language, {historyEntry=true}={}) {
 if (switching || language===currentLanguage()) return;
 switching=true;
 const previous=currentLanguage(), state=captureControls(main), scrollY=window.scrollY, originalRoute=location.hash;
 main.setAttribute('aria-busy','true');document.querySelectorAll('[data-language]').forEach(button=>button.disabled=true);
 const flux=document.querySelector('[data-flux][aria-pressed="true"]')?.dataset.flux;
 try {
  const nextDocuments=await loadDocuments(language);
  configureLocale(localeCatalog,language); documents=nextDocuments;
  try{localStorage.setItem('numart-language',language);}catch{}
  if(historyEntry)history.pushState({},'',languageURL(location.href,language));
  renderShell(); await route(location.hash===originalRoute?{state, scrollY, flux}:{});
  document.querySelector(`[data-language="${language}"]`)?.focus({preventScroll:true});
 } catch(error) {
  configureLocale(localeCatalog,previous);
  const notice=document.createElement('p');notice.className='language-error page-width';notice.setAttribute('role','alert');notice.textContent=t('translation.failed');main.prepend(notice);console.error(error);
 } finally {switching=false;main.removeAttribute('aria-busy');document.querySelectorAll('[data-language]').forEach(button=>button.disabled=false);}
}

const eyebrow = text => `<p class="eyebrow">${text}</p>`;
const arrow = '<span aria-hidden="true">↗</span>';
const plannedQuantumNotice = () => `<aside class="callout page-width planned-extension" id="quantum-plan" aria-labelledby="quantum-plan-title"><p class="eyebrow">PLANNED / QUANTUM CHEMISTRY + DFT</p><h2 id="quantum-plan-title">From basis functions to electronic structure.</h2><p>Schrödinger eigenproblems, orbital and plane-wave bases, Hartree–Fock, Kohn–Sham DFT, SCF mixing and verification examples.</p><p class="planned-status">Status: planned. Implementation and a dedicated literature review have not started. No release date is assigned.</p><a class="text-link" href="#/read/roadmap?section=planned-quantum-chemistry-and-dft">Read the development checklist ↗</a></aside>`;

const figureCard = (f, i) => `<article class="figure-card"><button class="figure-open" data-figure="${figures.indexOf(f)}" aria-label="Enlarge ${escapeHTML(f.title)}"><img src="assets/${f.file}" alt="${escapeHTML(f.description)}" loading="lazy" width="1000" height="450"><span class="enlarge" aria-hidden="true">＋</span></button><div class="figure-meta">${f.dimension?`<span>${f.dimension}D</span>`:''}<span>${f.category}</span><span>${f.year}</span></div><h3>${f.title}</h3><p>${f.description}</p><a class="text-link" href="#/read/${f.chapter}">Read the method ${arrow}</a>${f.movie?`<a class="text-link movie-card-link" href="#/movies?case=${f.movie}">${f.movie==='forward-step'?'Watch the first-order movie ▷':'Watch time evolution ▷'}</a>`:''}${f.comparison?`<a class="text-link movie-card-link" href="#/flow-comparison?case=${f.comparison}">Compare first order / MUSCL ↗</a>`:''}${f.experiment?`<a class="text-link movie-card-link" href="#/${f.experiment}">Open the solver comparison ↗</a>`:''}${f.shockmethod?`<a class="text-link movie-card-link" href="#/${f.shockmethod}">Open the shock-method comparison ↗</a>`:''}${f.mhdtest?`<a class="text-link movie-card-link" href="#/mhd-tests?case=${f.mhdtest}">Open the MHD test ↗</a>`:''}</article>`;
const methodCard = m => `<a class="method-card" href="#/read/${m.id}"><div class="method-top"><span>${m.number} / ${m.tag}</span><span aria-hidden="true">↗</span></div><p class="method-formula" aria-hidden="true">${m.formula}</p><h3>${m.title}</h3><p>${m.description}</p></a>`;
function plot(flux = 'roe') {
 const width=530, height=270, left=45, right=15, top=24, bottom=35;
 const x = v => left+v*(width-left-right);
 const y = v => height-bottom-(v/1.05)*(height-top-bottom);
 const path = values => values.map((v,i) => `${i?'L':'M'}${x(sod.x[i]).toFixed(2)},${y(v).toFixed(2)}`).join(' ');
 const ticks = [0,.25,.5,.75,1];
 return `<svg class="sod-plot" viewBox="0 0 ${width} ${height}" role="img" aria-label="Computed ${flux.toUpperCase()} and exact Sod shock-tube density at t=0.2"><title>Sod density: ${flux.toUpperCase()} and exact Riemann solution</title>${ticks.map(v=>`<line x1="${left}" x2="${width-right}" y1="${y(v)}" y2="${y(v)}" class="grid-line"/><text x="${left-12}" y="${y(v)+4}" text-anchor="end">${v.toFixed(2)}</text><text x="${x(v)}" y="${height-10}" text-anchor="middle">${v}</text>`).join('')}<text x="${left}" y="13" class="axis-title">DENSITY ρ</text><text x="${width-right}" y="13" text-anchor="end" class="axis-title">POSITION x</text><path d="${path(sod.exact)}" class="exact-line"/><path d="${path(sod.curves[flux])}" class="numerical-line"/></svg>`;
}
function home() {
 return `<section class="hero page-width"><div class="hero-copy">${eyebrow(`${coverage.counts.papers} PAPERS · ${coverage.counts.references} SOURCES · ONE ATLAS`)}<h1>The ideas behind<br>the <em>computation.</em></h1><p class="hero-description">From shock waves to living systems.<br>${coverage.counts.equations} equation &amp; model entries. ${coverage.counts.methods} numerical methods and building blocks.</p><div class="hero-actions"><a class="button primary" href="#/atlas">Explore the atlas <span aria-hidden="true">→</span></a><a class="text-link" href="#/coverage">What’s inside the atlas ${arrow}</a></div><div class="hero-footnote"><span class="status-dot"></span> Python · Reproducible examples · Public source</div></div><div class="hero-experiment"><div class="experiment-heading"><span class="eyebrow">A CLASSIC, COMPUTED</span><span class="small-mono">1978 / SOD</span></div><h2>One problem.<br>Different numerical lenses.</h2><div id="sod-chart">${plot()}</div><div class="chart-legend"><span class="legend-exact">Exact solution</span><span class="legend-numerical">MUSCL + <span id="flux-label">Roe</span></span></div><div class="flux-controls" aria-label="Choose Riemann flux">${['roe','hllc','hll','rusanov'].map((s,i)=>`<button data-flux="${s}" aria-pressed="${i===0}">${s==='roe'?'Roe':s==='rusanov'?'Rusanov':s.toUpperCase()}</button>`).join('')}</div><p class="experiment-note">N = 200 · t = 0.20 · pointwise density comparison</p><a class="experiment-source" href="#/read/benchmarks">See the setup & verification ${arrow}</a></div></section>
 ${currentLanguage()==='ja'?`<aside class="translation-progress page-width"><span>${t('translation.progress',{count:translationStatus.translated,total:translationStatus.total})}。未訳章は英語版を表示します。</span><a href="#/read/stability">日本語解説から読む →</a><a href="#/glossary">日英用語集 →</a></aside>`:''}
 ${coverageHighlights(coverage)}
 ${plannedQuantumNotice()}
 <section class="principles page-width" id="reading-guide" aria-label="How to use the atlas"><div><span>01</span><p><strong>Read the paper.</strong> Find the original idea and the sources behind it.</p></div><div><span>02</span><p><strong>Understand the method.</strong> Follow the equations, assumptions, and limits.</p></div><div><span>03</span><p><strong>Run the benchmark.</strong> Inspect the result and the evidence that checks it.</p></div></section>
 <section class="section page-width"><div class="section-heading"><div>${eyebrow('FOLLOW THE IDEAS')}<h2>A century of better questions.</h2></div><a class="text-link" href="#/atlas">Open the historical atlas ${arrow}</a></div><div class="history-strip">${[['1928','Can the stencil reach it?','CFL'],['1959','What crosses the interface?','GODUNOV'],['1977','Which scale holds the error?','MULTIGRID'],['1996','Where should the weights go?','WENO5-JS']].map(([year,title,label])=>`<a href="#/atlas"><span class="history-year">${year}</span><h3>${title}</h3><span class="small-mono">${label} <span aria-hidden="true">→</span></span></a>`).join('')}</div></section>
 <aside class="callout page-width"><p class="eyebrow">NEW / EQUATION GALLERY</p><h2>Follow a wave. Trace its equation.</h2><p>Play Burgers shocks, clearing fans, upstream traffic jams, physical diffusion, Sod, shallow water and isothermal flow. Continue into lattice Boltzmann, Chapman–Enskog and hyperbolic diffusion.</p><a class="text-link" href="#/equations">Open the equation gallery ▷</a></aside>
 <section class="experiment-invitation page-width"><div><p class="eyebrow">NEW / INTERACTIVE NOTEBOOKS</p><h2>Change a parameter.<br>Ask a better question.</h2><p>Explore stability with live calculations, then examine the measured orders behind a refinement plot.</p></div><a class="experiment-entry" href="#/experiments"><span class="small-mono">01 / COMPUTE</span><h3>The stability laboratory</h3><p>CFL, direction, and stencil.<br>One wave, four methods.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/convergence"><span class="small-mono">02 / INSPECT</span><h3>The convergence notebook</h3><p>Elements, unknowns, errors,<br>and observed orders.</p><span aria-hidden="true">↗</span></a></section>
 <section class="page-width foundation-links"><a class="experiment-entry" href="#/time-integration"><span class="small-mono">03 / TIME INTEGRATION</span><h3>Follow the orbit.</h3><p>Twelve methods, two leapfrog roots,<br>and one exact oscillator.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/meshes"><span class="small-mono">04 / MESH EXPLORER</span><h3>Inspect the neighbors.</h3><p>Structured grids, triangles,<br>and irregular connectivity.</p><span aria-hidden="true">↗</span></a></section>
 <aside class="callout page-width"><p class="eyebrow">NEW / HAMILTONIAN MAPS & PARTICLE GRAVITY</p><h2>Preserve the geometry. Choose the boundary.</h2><p>Inspect canonical maps and energy histories, then follow particles through PM, Tree forces, multipole expansions, and isolated or slab Poisson kernels.</p><a class="text-link" href="#/hamiltonian">Open the Hamiltonian notebook ↗</a> · <a class="text-link" href="#/read/gravity-boundaries">Read the gravity kernels ↗</a></aside>
 <section class="section methods-section"><div class="page-width"><div class="section-heading"><div>${eyebrow('EXPLORE BY METHOD')}<h2>From a stencil to a solver.</h2></div><a class="text-link" href="#/methods">All methods ${arrow}</a></div><div class="method-grid">${methods.slice(0,3).map(methodCard).join('')}</div></div></section>
 <section class="section page-width"><div class="section-heading"><div>${eyebrow('THE COMPUTED EVIDENCE')}<h2>See the method at work.</h2></div><a class="text-link" href="#/gallery">Browse the gallery ${arrow}</a></div><div class="figure-grid home-figures">${[figures[0],figures[3],figures[4]].map(figureCard).join('')}</div><p class="scope-note"><span aria-hidden="true">↳</span> Independent educational implementations. Each exhibit states its reference solution, assumptions, and verification limits.</p></section>
 <aside class="callout page-width"><p class="eyebrow">NEW / MODES + NODES</p><h2>A mesh needs a basis.</h2><p>Explore Legendre modes, nodal Lagrange functions, exact and quadrature mass matrices, and shape functions on a triangle.</p><a class="text-link" href="#/basis">Open the element-basis notebook ↗</a></aside>
 <aside class="callout page-width"><p class="eyebrow">NEW / CUBIC CIP</p><h2>Carry the value. Evolve the gradient.</h2><p>Compare cubic-Hermite CIP with linear interpolation, inspect smooth refinement and sharp-profile overshoots, and test a conservative-remapping claim.</p><a class="text-link" href="#/cip">Open the CIP notebook ↗</a></aside>
 <aside class="callout page-width"><p class="eyebrow">NEW / RUNGE–KUTTA FAMILIES</p><h2>More stages. A different guarantee.</h2><p>Compare RK2 variants, classical RK4, and SSPRK(2,2), (3,3), (4,3), and (5,4). Inspect actual nonlinear stages, full coefficients, linear stability, and the forward-Euler inheritance condition.</p><a class="text-link" href="#/runge-kutta">Explore the RK family ↗</a></aside>
 <aside class="callout page-width"><p class="eyebrow">NEW / LIMITERS &amp; ADVANCED RECONSTRUCTION</p><h2>Choose the slope. Preserve the mean.</h2><p>Compare minmod, Superbee, MC, van Leer, and van Albada. Inspect scalar TVD bounds, TVB extrema relaxation, and positive Euler-state scaling with explicit scope.</p><a class="text-link" href="#/limiters">Open the limiter notebook ↗</a> · <a class="text-link" href="#/read/advanced-limiters">Read TVB &amp; positivity ↗</a></aside>
 <aside class="callout page-width motion-banner"><p class="eyebrow">NEW / TIME-DEPENDENT COMPUTATIONS</p><h2>Some results need time.</h2><p>Play Double Mach Reflection, Orszag–Tang CT/GLM, and a smooth KEEP vortex. Inspect the actual solver time, step count, and fixed color scales.</p><a class="text-link" href="#/movies">Open the motion gallery ▷</a></aside>
 <section class="reading-banner page-width"><div>${eyebrow('KEEP THE PAPER CLOSE')}<h2>Every method has a history.<br>Every result needs a reference.</h2><p>${references.length} research and source records, ordered by original publication year.<br>Source notes distinguish original texts, later expositions, and open questions.</p><a class="button primary" href="#/references">Explore the references <span aria-hidden="true">→</span></a><p><a class="text-link" href="#/read/textbooks">Choose a textbook ↗</a></p></div><div class="reference-mark" aria-hidden="true">[${references.length}]<span>1928 — 2026</span></div></section>
 <aside class="memorial-note page-width"><div><p class="eyebrow">IN MEMORIAM · PHILIP L. ROE</p><h2>A legacy carried by the waves.</h2><p>Remembering his contribution to computational fluid dynamics through the original ideas, their equations, and the questions they continue to open.</p></div><a class="text-link" href="#/read/roe-memorial">Read the tribute ↗</a></aside>
 <section class="run-section page-width"><div>${eyebrow('YOUR NEXT EXPERIMENT')}<h2>Start with Sod.</h2><p>The same definitions and solvers used in this atlas are available in the Python library.</p><a class="text-link" href="${repo}#getting-started">Installation & source ${arrow}</a></div><div class="terminal"><div class="terminal-title"><span>TERMINAL · AFTER INSTALLATION</span><button class="copy-command" data-copy="python -m numart.cli run sod --method muscl --riemann roe --n 200">Copy</button></div><pre><code><span class="prompt">$</span> python -m numart.cli run sod \
    --method muscl --riemann roe --n 200</code></pre><p>Numerical arrays + a run manifest, saved together.</p></div></section>`;
}
function atlas() {
 return `<section class="page-intro page-width">${eyebrow('THE HISTORICAL ATLAS')}<h1>Follow the ideas<br>through <em>time.</em></h1><p>Read by original publication year. Trace the questions that connect a classical stencil to a modern solver.</p><a class="text-link" href="#/read/history">Read the complete historical notes ${arrow}</a></section><section class="timeline page-width">${eras.map(([year,title,authors,description,chapter,ref])=>`<article class="timeline-item"><div class="timeline-year">${year}</div><div><p class="small-mono">${authors}</p><h2>${title}</h2><p>${description}</p><div class="timeline-links"><a href="#/read/${chapter}">Explore the method →</a><a href="#/references?q=${ref}">Read the source ↗</a></div></div></article>`).join('')}</section><aside class="callout page-width"><h2>A reading path, not a priority claim.</h2><p>Publication dates distinguish originals from translations and reprints. The reference notes record source status, and the atlas does not assign every invention to a single paper.</p><a class="text-link" href="#/read/nasa-2d">Continue toward NASA verification & validation cases ${arrow}</a></aside>`;
}
function methodPage() {
 return `<section class="page-intro page-width">${eyebrow('EXPLORE BY METHOD')}<h1>Understand the<br><em>discretization.</em></h1><p>${coverage.counts.methods} named numerical methods and building blocks across ${methods.length} reading entry points. <a href="#/coverage?kind=method">Inspect the counted inventory →</a></p><p> Start with the equations, follow the numerical choices, and check the evidence.</p></section><section class="page-width method-grid full-methods">${methods.map(methodCard).join('')}</section>${plannedQuantumNotice()}<aside class="callout page-width"><h2>Implementation and ambition, clearly separated.</h2><p>The first edition includes selected educational models. Multidimensional Euler rotated-hybrid fluxes, low-Mach PDE preconditioning, Euler/MHD DG, and the cataloged NASA airfoil, viscous, and turbulence cases remain future work.</p><a class="text-link" href="#/read/roadmap">Read the implementation roadmap ${arrow}</a></aside>`;
}
function gallery() {
 return `<section class="page-intro page-width">${eyebrow('THE NUMERICAL GALLERY')}<h1>Look closely<br>at the <em>result.</em></h1><p>Start with shock waves: NASA wedge flows, a Mach-3 forward-facing step, and Double Mach Reflection. Compare computed fields with references, then follow the unsteady cases in saved-state movies.</p><a class="button primary" href="#/reconstruction">PPM, characteristics & WENO-Z ↗</a> <a class="text-link" href="#/shock-robustness">Odd–even shock diagnostic ↗</a> <a class="text-link" href="#/flow-comparison">Compare first order / MUSCL ↗</a> <a class="text-link" href="#/mhd-tests">HLLD standard tests ↗</a> <a class="text-link" href="#/movies">Watch the motion gallery ▷</a></section><section class="page-width"><div class="filter-bar" aria-label="Spatial dimension">${[['fields','2D & 3D fields'],['2','2D fields'],['3','3D fields / slices'],['all','All dimensions & diagnostics']].map(([id,label],i)=>`<button data-gallery-dimension="${id}" aria-pressed="${i===0}">${label}</button>`).join('')}</div><div class="filter-bar" aria-label="Filter gallery">${['All figures','Particles & gravity','2D shock interactions','Conservation laws','Advection & stability','MHD','Elliptic & iterative'].map((c,i)=>`<button data-gallery-filter="${c}" aria-pressed="${i===0}">${c}</button>`).join('')}</div><p id="gallery-count" aria-live="polite"></p><p id="gallery-empty" hidden>No figures match both filters. Try another dimension or category.</p><div class="figure-grid gallery-grid">${figures.map(figureCard).join('')}</div><p class="scope-note">Dimensions describe the solved spatial field. A 3D slice is a view of a three-dimensional Poisson solve, not a three-dimensional fluid simulation. Single-resolution images and movies do not establish grid convergence.</p><a class="text-link" href="assets/shock-gallery.json">Download shock-case definitions & diagnostics ${arrow}</a><br><a class="text-link" href="assets/multidimensional-fields.json">Download field definitions & diagnostics ${arrow}</a><br><a class="text-link" href="assets/multidimensional-fields.npz" download>Download computed field arrays ↓</a><br><a class="text-link" href="assets/validation.json">Download the original eleven-figure validation manifest ${arrow}</a><br><a class="text-link" href="assets/double-mach-run.json">Download the Double Mach Reflection run manifest ${arrow}</a></section>`;
}
function referenceItem(e) {
 const source=e.doi?`https://doi.org/${e.doi}`:e.source;
 return `<article class="reference-item"><div class="reference-year">${e.year}</div><div><p class="reference-authors" data-original>${escapeHTML(e.author.replace(/ and /g,'; '))}</p><h2 data-original lang="en">${escapeHTML(e.title)}</h2><p class="reference-publication" data-original>${escapeHTML(e.journal||e.publisher||e.institution||e.booktitle||'')}${e.volume?` · ${escapeHTML(e.volume)}`:''}${e.pages?` · pp. ${escapeHTML(e.pages.replace('--','–'))}`:''}</p><p class="reference-note" data-original lang="en">${escapeHTML(e.note)}</p><div class="reference-links"><a href="${escapeHTML(source)}" target="_blank" rel="noopener">Original record ↗</a><a href="${escapeHTML(e.source)}" target="_blank" rel="noopener">Text / implementation source ↗</a><code>${e.id}</code></div></div></article>`;
}
function referencePage(query='') {
 return `${currentLanguage()==='ja'?`<p class="translation-notice page-width">${t('translation.original')}</p>`:''}<section class="page-intro page-width">${eyebrow('THE REFERENCE LIBRARY')}<h1>Return to<br>the <em>source.</em></h1><p>${references.length} research and source records. Original publication dates, implementation sources, and honest notes on what has been verified.</p><p><a class="button primary" href="#/read/textbooks">Choose a textbook ↗</a> <a class="text-link" href="#/references?q=type%3Abook">Browse books only ↗</a></p></section><section class="page-width reference-layout"><aside class="reference-aside"><label for="reference-search">Search the library</label><div class="search-wrap"><span aria-hidden="true">⌕</span><input id="reference-search" type="search" value="${escapeHTML(query)}" placeholder="Author, method, year…" autocomplete="off"></div><p id="reference-count" aria-live="polite"></p><a class="text-link" href="assets/references.bib" download>Download BibTeX ↓</a><p class="aside-note">A DOI identifies a publication. It does not imply that its full text has been inspected or its figures reproduced.</p><a href="#/read/references">Read the complete catalog →</a></aside><div id="reference-results"></div></section>`;
}
function filterReferences(query) {
 const booksOnly=/(?:^|\s)type:book(?=\s|$)/i.test(query);
 const q=query.replace(/(?:^|\s)type:book(?=\s|$)/ig,' ').toLowerCase().trim();
 const matches=references.filter(e=>(!booksOnly||e.type==='book')&&[e.author,e.title,e.year,e.id,e.note,translateText(e.note)].join(' ').toLowerCase().includes(q));
 document.querySelector('#reference-results').innerHTML=matches.length?matches.map(referenceItem).join(''):'<div class="empty-state"><h2>No references found.</h2><p>Try an author, a method such as WENO, or a publication year.</p></div>';
 document.querySelector('#reference-count').textContent=`${matches.length} of ${references.length} references`;
}
function chapter(id) {
 const d=documents[id];
 if(!d) return notFound();
 const links=[['accuracy-stability','A/L stability & error norms'],['site-coverage','Coverage & counting rules'],['history','Historical atlas'],['experiments','Interactive experiment guide'],['movies','Movie definitions & provenance'],...methods.filter((m,i,a)=>a.findIndex(x=>x.id===m.id)===i).map(m=>[m.id,m.title]),['reconstruction','PPM, characteristics, WENO-Z & AUSM'],['roe-memorial','Remembering Philip L. Roe'],['nasa-2d','NASA case catalog'],['textbooks','Textbook reading guide'],['references','Reference catalog'],['roadmap','Implementation roadmap'],['release-notes-v0.1.0','First-edition notes']];
 const notice=currentLanguage()==='ja' ? `<p class="translation-notice ${d.locale==='en'?'translation-fallback':''}">${d.locale==='en'?t('translation.fallback'):t(d.translation_status==='stale'?'translation.stale':'translation.draft')} <span>${t('translation.progress',{count:translationStatus.translated,total:translationStatus.total})}</span></p>` : '';
 return `<div class="reading-shell page-width"><aside class="reading-nav"><a class="back-link" href="#/methods">← Explore the methods</a><p class="eyebrow">IN THIS EDITION</p><nav aria-label="Reading chapters">${links.map(([key,label])=>`<a href="#/read/${key}" ${id===key?'aria-current="page"':''}>${label}</a>`).join('')}</nav><p class="small-mono">FIRST EDITION · v0.1.0</p></aside><div class="chapter-wrap"><div class="chapter-topline"><span>THE READING ROOM</span><a href="${repo}/blob/main/docs/${d.locale==='ja'?'ja/':''}${id}.md">View source ↗</a></div>${notice}<article class="prose" lang="${d.locale||'en'}">${d.html}</article><div class="chapter-bottom"><span>Continue exploring</span><a href="#/atlas">Historical atlas →</a><a href="#/gallery">Computed gallery →</a></div></div><aside class="chapter-toc"><p class="eyebrow">ON THIS PAGE</p><nav aria-label="On this page">${d.headings.filter(h=>h.level===2).map(h=>`<a href="#/read/${id}?section=${h.id}">${h.title}</a>`).join('')}</nav></aside></div>`;
}
function notFound(){return `<section class="page-intro page-width"><p class="eyebrow">PAGE NOT FOUND</p><h1>Back to<br>the <em>atlas.</em></h1><p>This chapter could not be found.</p><a class="button primary" href="#/">Return home →</a></section>`;}
function wire() {
 wireBookCovers(main);
 document.querySelectorAll('[data-flux]').forEach(button=>button.addEventListener('click',()=>{
   const flux=button.dataset.flux; document.querySelector('#sod-chart').innerHTML=plot(flux);
   document.querySelector('#flux-label').textContent=button.textContent;
   document.querySelectorAll('[data-flux]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 }));
 document.querySelectorAll('[data-figure]').forEach(button=>button.addEventListener('click',()=>{
   const f=figures[Number(button.dataset.figure)],dialog=document.querySelector('#figure-dialog');
   dialog.querySelector('h2').textContent=translateText(f.title); dialog.querySelector('img').src=`assets/${f.file}`; dialog.querySelector('img').alt=translateText(f.description); dialog.querySelector('p').textContent=translateText(f.description); dialog.showModal();
 }));
 const filterGallery=()=>{
   const dimension=document.querySelector('[data-gallery-dimension][aria-pressed="true"]')?.dataset.galleryDimension;
   const category=document.querySelector('[data-gallery-filter][aria-pressed="true"]')?.dataset.galleryFilter;
   let visible=0;
   document.querySelectorAll('.gallery-grid .figure-card').forEach((card,i)=>{
     card.hidden=!matchesGallery(figures[i],dimension,category); if(!card.hidden)visible++;
   });
   const count=document.querySelector('#gallery-count');
   if(count){count.textContent=translateText(`Showing ${visible} of ${figures.length} figures`);document.querySelector('#gallery-empty').hidden=visible>0;}
 };
 for(const selector of ['[data-gallery-filter]','[data-gallery-dimension]']){
   document.querySelectorAll(selector).forEach(button=>button.addEventListener('click',()=>{
     document.querySelectorAll(selector).forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
     filterGallery();
   }));
 }
 filterGallery();
 document.querySelectorAll('.copy-command').forEach(button=>button.addEventListener('click',async()=>{
   try {await navigator.clipboard.writeText(button.dataset.copy);button.textContent='Copied';setTimeout(()=>button.textContent='Copy',1800);}
   catch {button.textContent='Select the command below';}
 }));
 document.querySelectorAll('.prose pre').forEach(pre=>{
   const button=document.createElement('button');button.className='code-copy';button.textContent='Copy';button.setAttribute('aria-label','Copy code example');
   button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(pre.querySelector('code').textContent);button.textContent='Copied';}catch{button.textContent='Select code to copy';}});pre.append(button);
 });
}
async function route(options={}) {
 const version=++navigationVersion;
 disposeMovies();disposeEquations();disposeComparisons();
 const [path,queryString='']=(location.hash.slice(1)||'/').split('?');
 const parts=path.split('/').filter(Boolean),type=parts[0]||'home',query=new URLSearchParams(queryString);
 if(type==='read' && !documents[parts[1]]) {
  const english=await loadDocuments('en');if(version!==navigationVersion)return;
  if(english[parts[1]])documents[parts[1]]=english[parts[1]];
 }
 if(version!==navigationVersion)return;
 const renderers={home,atlas,glossary:glossaryPage,coverage:()=>coveragePage(coverage),equations:equationsPage,methods:methodPage,gallery,movies:moviesPage,'flow-comparison':flowPage,'mhd-tests':mhdPage,reconstruction:reconstructionPage,'shock-robustness':robustnessPage,'poisson-comparison':poissonPage,limiters:limiterPage,'runge-kutta':rkPage,cip:cipPage,basis:basisPage,experiments:stabilityPage,convergence:convergencePage,'time-integration':timePage,meshes:meshPage,hamiltonian:hamiltonianPage,references:()=>referencePage(query.get('q')||''),read:()=>chapter(parts[1])};
 main.innerHTML=(renderers[type]||notFound)();
 document.body.dataset.page=type;
 main.lang=currentLanguage();main.removeAttribute('data-localize');
 document.querySelectorAll('[data-nav]').forEach(a=>{if(a.dataset.nav===type||(['movies','flow-comparison','mhd-tests','reconstruction','shock-robustness'].includes(type)&&a.dataset.nav==='gallery')||(['convergence','time-integration','meshes','hamiltonian','limiters','runge-kutta','cip','basis','poisson-comparison'].includes(type)&&a.dataset.nav==='experiments'))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 document.querySelector('.site-header').classList.remove('menu-open');document.querySelector('.mobile-menu').setAttribute('aria-expanded','false');
 document.title=type==='home'?site.title[currentLanguage()]:`${type==='read'?(documents[parts[1]]?.title||'Reading room'):({glossary:currentLanguage()==='ja'?'日英用語集':'Bilingual glossary',coverage:'The atlas in numbers',equations:'Equation gallery',atlas:'Historical atlas',methods:'Explore the methods',gallery:'Numerical gallery',movies:'Motion gallery',reconstruction:'High-order Euler reconstruction','poisson-comparison':'Poisson solver comparison','shock-robustness':'Odd–even shock diagnostic','flow-comparison':'Euler reconstruction comparison','mhd-tests':'HLLD standard tests',references:'Reference library',experiments:'Stability laboratory',convergence:'Convergence notebook','time-integration':'Time integration notebook',meshes:'Mesh explorer',hamiltonian:'Hamiltonian map notebook',limiters:'Slope limiter notebook','runge-kutta':'Runge–Kutta family notebook',cip:'CIP profile notebook',basis:'Element basis notebook'}[type]||'Page not found')} · ${site.title[currentLanguage()]}`;
 document.title=document.title.split(' · ').map(translateText).join(' · ');
 if(type==='read')document.querySelectorAll('.heading-anchor').forEach(a=>{a.href=`#/read/${parts[1]}?section=${a.parentElement.id}`;});
 if(type==='references') {filterReferences(query.get('q')||'');document.querySelector('#reference-search').addEventListener('input',e=>filterReferences(e.target.value));}
 wire();
 if(type==='experiments')wireStability(experiments);
 if(type==='convergence')wireConvergence(experiments);
 if(type==='time-integration')wireTime(foundations);
 if(type==='meshes')wireMesh(foundations);
 if(type==='hamiltonian')await wireHamiltonian();
 if(type==='limiters')await wireLimiters();
 if(type==='runge-kutta')await wireRK();
 if(type==='cip')await wireCIP();
 if(type==='basis')await wireBasis();
 if(type==='equations')await wireEquations();
 if(type==='coverage'&&currentLanguage()==='ja'){const note=document.createElement('p');note.className='translation-notice page-width';note.textContent='項目名は日英で検索できます。実装範囲と集計規則の詳細注記は、英語原文を表示しています。';main.prepend(note);}
 if(type==='glossary')wireGlossary(glossary,query.get('q')||'');
 if(type==='coverage')wireCoverage(coverage,query.get('kind')||'all');
 if(type==='movies')await wireMovies(query.get('case'));
 if(type==='reconstruction')await wireReconstruction(query.get('case'));
 if(type==='shock-robustness')await wireRobustness();
 if(type==='poisson-comparison')await wirePoisson();
 if(type==='flow-comparison')await wireFlow(query.get('case'),query.get('method'));
 if(type==='mhd-tests')await wireMHD(query.get('case'));
 if(version!==navigationVersion)return;
 if(options.state)restoreControls(main,options.state);
 if(options.flux)document.querySelector(`[data-flux="${options.flux}"]`)?.click();
 localizeTree(main);
 if(options.scrollY!==undefined)window.scrollTo({top:options.scrollY,behavior:'instant'});
 else if(query.get('section'))requestAnimationFrame(()=>document.getElementById(query.get('section'))?.scrollIntoView());else window.scrollTo({top:0,behavior:'instant'});
}
document.querySelector('.skip-link').addEventListener('click',e=>{e.preventDefault();main.focus();main.scrollIntoView();});
document.querySelector('#figure-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close();});
try {
 [localeCatalog,references,sod,experiments,foundations,coverage,translationStatus,glossary,site]=await Promise.all(['locales/messages.json','references.json','sod.json','experiments.json','foundations.json','coverage.json','translation-status.json','glossary.json','site.json'].map(async file=>{const response=await fetch(file);if(!response.ok)throw Error(`Cannot load ${file}`);return response.json();}));
 repo=site.repositoryUrl;
 references.sort((a,b)=>a.year-b.year||a.id.localeCompare(b.id));
 let saved;try{saved=localStorage.getItem('numart-language');}catch{}
 configureLocale(localeCatalog,resolveLanguage(location.search,saved));
 documents=await loadDocuments(currentLanguage());
 renderShell();observeLocalization(document.body);
 window.addEventListener('hashchange',()=>route().catch(console.error));
 window.addEventListener('popstate',async()=>{
  const requested=resolveLanguage(location.search);if(requested!==currentLanguage())await changeLanguage(requested,{historyEntry:false});else await route();
 });
 await route();
} catch(error) {main.innerHTML=`<section class="page-intro page-width"><h1>The atlas could not load.</h1><p>Please reload the page, or read the complete edition on GitHub.</p><a class="button primary" href="${repo}">Open the source edition ↗</a></section>`;console.error(error);}
