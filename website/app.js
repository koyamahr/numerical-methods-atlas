import {hamiltonianPage,wireHamiltonian} from './hamiltonian.js';
import {timePage,meshPage,wireTime,wireMesh} from './foundations.js';
import {stabilityPage,convergencePage,wireStability,wireConvergence} from './experiments.js';
const main = document.querySelector('main');
const repo = 'https://github.com/koyamahr/the-art-of-numerical-algorithms';
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const methods = [
  {id:'stability',number:'01',title:'Differences & stability',subtitle:'Start with the stencil.',description:'Follow information through a grid. Separate spatial differences, time integration, the CFL condition, and linear stability.',formula:'uₜ + a uₓ = 0',tag:'FINITE DIFFERENCES'},
  {id:'benchmarks',number:'02',title:'Conservation laws',subtitle:'Resolve the waves.',description:'From Godunov-type finite volumes to MUSCL and WENO. Compare numerical fluxes on shared, precisely defined problems.',formula:'Uₜ + F(U)ₓ = 0',tag:'FINITE VOLUMES · WENO'},
  {id:'elliptic',number:'03',title:'Diffusion & elliptic solvers',subtitle:'Let the errors relax.',description:'Boundary conditions, implicit steps, tridiagonal elimination, iterative matrices, and a geometric multigrid V-cycle.',formula:'−∇²u = f',tag:'THOMAS · CG · MULTIGRID'},
  {id:'benchmarks',number:'04',title:'DG & spectral methods',subtitle:'Choose your basis.',description:'Local Legendre polynomials meet global Fourier modes in periodic linear advection, with exact translation as a reference.',formula:'uₕ = ∑ ûₖ φₖ',tag:'LOCAL & GLOBAL BASES'},
  {id:'mhd',number:'05',title:'Magnetic constraints',subtitle:'Keep the field in balance.',description:'Explore staggered constrained transport and GLM cleaning. Learn why a divergence measurement needs its discrete operator.',formula:'∇ · B = 0',tag:'PLANAR IDEAL MHD'},
  {id:'advanced',number:'06',title:'Beyond the explicit step',subtitle:'Iterate in another time.',description:'Minimal models for dual time stepping, matrix preconditioning, and scalar residual distribution, with their limits made explicit.',formula:'∂Q/∂τ + R*(Q) = 0',tag:'ADVANCED MODELS'},
  {id:'time-integration',number:'07',title:'Time integration & leapfrog',description:'Compare seven temporal methods on an oscillator; distinguish the physical and computational roots.',formula:'ξ² − 2z ξ − 1 = 0',tag:'ODE · TWO-STEP MODES'},
  {id:'meshes',number:'08',title:'Meshes & connectivity',description:'Structured quadrilaterals, split-lattice triangles, and irregular triangulations. Inspect face-sharing neighbors.',formula:'V − E + F = 1',tag:'STRUCTURED · UNSTRUCTURED'},
  {id:'particles-sph',number:'09',title:'Particles & SPH',description:'Kernel reconstruction, particle volume weights, normalization, and the additional requirements of fluid dynamics.',formula:'fₕ ≈ ∑ (m/ρ) f W',tag:'PARTICLE METHODS'},
  {id:'ale',number:'10',title:'Moving volumes & ALE',description:'Follow the relative face flux and test uniform-state preservation under mesh motion.',formula:'F · n − (w · n) U',tag:'GEOMETRIC CONSERVATION'},
  {id:'coordinates-viscosity',number:'11',title:'Coordinates, tensors & viscosity',description:'Physical cylindrical components, all six viscous stresses, tensor divergence, and analytic checks.',formula:'τ = 2μD + λ(∇ · u)I',tag:'POLAR · CYLINDRICAL'},
  {id:'double-mach',number:'12',title:'Double Mach Reflection',description:'An actual 2D Euler shock-reflection computation, with moving boundaries, a run manifest, and explicit resolution limits.',formula:'Uₜ + Fₓ + Gᵧ = 0',tag:'MACH 10 · COMPUTED'},
  {id:'carbuncle',number:'13',title:'The carbuncle phenomenon',description:'Strong-shock instability, transverse dissipation, and why entropy correction and positivity are different tests.',formula:'∣λ̃ₖ∣ αₖ r̃ₖ',tag:'MULTIDIMENSIONAL ROBUSTNESS'},
  {id:'symplectic',number:'14',title:'Symplectic Hamiltonian maps',description:'Canonical structure, Verlet and Yoshida compositions, time reversal, and long-time energy errors.',formula:'Mᵀ J M = J',tag:'GEOMETRIC INTEGRATION'},
  {id:'particle-gravity',number:'15',title:'Particle gravity & Poisson',description:'CIC particle–mesh forces, P³M and TreePM splitting, octrees, multipole moments, and multigrid.',formula:'∇²φ = 4πGρ',tag:'PM · TREE · MULTIPOLES'},
  {id:'gravity-boundaries',number:'16',title:'Isolated & slab gravity',description:'Hockney–Eastwood convolution and Koyama–Ostriker slab kernels, with explicit Fourier and zero-mode conventions.',formula:'Gₖ(z) ∝ exp(−k|z|)',tag:'FFT · GREEN FUNCTIONS'}
];
const figures = [
 {file:'hamiltonian.png',title:'Canonical maps and energy',category:'Particles & gravity',year:'1990–2003',description:'Five fixed-step integrators on harmonic and quartic Hamiltonians. Energy histories to T=200 and phase orbits to T=10; no equal-cost ranking.',chapter:'symplectic'},
 {file:'particle-gravity.png',title:'PM, Tree, and multipole forces',category:'Particles & gravity',year:'1981–2005',description:'An isolated octree compared with the same softened direct force sum, and a separate periodic CIC/FFT Poisson example.',chapter:'particle-gravity'},
 {file:'gravity-boundaries.png',title:'Gravity follows the boundary',category:'Particles & gravity',year:'1981–2009',description:'Isolated doubled-grid convolution, a slab mean mode, and a sinusoidal sheet. Sampled DFT and continuous coefficients are distinct.',chapter:'gravity-boundaries'},
 {file:'double-mach.png',title:'Double Mach Reflection',category:'2D shock interactions',year:'1984',description:'Computed Mach-10 reflection at t = 0.2 on 256 × 64 cells. First-order HLL + SSPRK2; a diffusive baseline, without a resolved fine wall jet.',chapter:'double-mach'},
 {file:'sod.png',title:'Sod shock tube',category:'Conservation laws',year:'1978',description:'Four numerical fluxes meet the exact density, velocity, and pressure profiles.',chapter:'benchmarks'},
 {file:'shu-osher.png',title:'Shock meets a density wave',category:'Conservation laws',year:'1989',description:'MUSCL and WENO5-JS on the Shu–Osher problem. A numerical comparison, without an exact final-time reference.',chapter:'benchmarks'},
 {file:'dg-spectral.png',title:'Local polynomials, global waves',category:'Advection & stability',year:'1973–1977',description:'Periodic DG and Fourier advection, plus DG grid refinement. Degrees of freedom and costs are not matched.',chapter:'benchmarks'},
 {file:'stability.png',title:'The shape of stability',category:'Advection & stability',year:'1928–1960',description:'Fourier amplification and a seeded Nyquist mode reveal the effect of the Courant number.',chapter:'stability'},
 {file:'orszag-tang.png',title:'Orszag–Tang vortex',category:'MHD',year:'1979',description:'First-order CT and GLM examples on a periodic square. Their native divergence operators differ.',chapter:'mhd'},
 {file:'glm-cleaning.png',title:'Where divergence errors go',category:'MHD',year:'2002',description:'A longitudinal magnetic error is injected into OT data to isolate propagation and damping.',chapter:'mhd'},
 {file:'diffusion-boundaries.png',title:'The boundary changes the problem',category:'Elliptic & iterative',year:'1947',description:'Diffusion time integrators and three Poisson boundary-condition sets for a manufactured solution.',chapter:'elliptic'},
 {file:'multigrid-radius.png',title:'From smoothing to correction',category:'Elliptic & iterative',year:'1961–1977',description:'Geometric multigrid residuals and the spectral radius of stationary iteration matrices.',chapter:'elliptic'},
 {file:'implicit.png',title:'A second clock',category:'Elliptic & iterative',year:'1991',description:'Pseudo-time residuals for BDF2 advection and symmetric Jacobi scaling of an SPD model matrix.',chapter:'advanced'},
 {file:'lax-entropy.png',title:'Shocks and smooth refinement',category:'Conservation laws',year:'1954',description:'The Lax shock tube and pointwise density error for a periodic Euler entropy wave.',chapter:'benchmarks'},
 {file:'barotropic.png',title:'Two barotropic systems',category:'Conservation laws',year:'MODEL COMPARISON',description:'Shallow-water dam break and isothermal Euler. Exact Riemann references are future work.',chapter:'benchmarks'}
];
const eras = [
 ['1928','The numerical domain of dependence','Courant, Friedrichs & Lewy','A discrete stencil must reach the information required by the continuous problem.','stability','cfl1928'],
 ['1947–1950','Diffusion, implicit steps, and stability','Crank–Nicolson · Thomas · Charney et al.','Connect time stepping to a linear-system solve, then ask what happens to each Fourier mode.','elliptic','crank1947'],
 ['1954–1961','Weak solutions and conservation form','Lax · Richtmyer · Godunov · Wendroff · Rusanov','Move from a difference formula to a conservative flux and the waves it resolves.','stability','godunov1959'],
 ['1961–1977','Different scales, different bases','Fedorenko · Reed–Hill · Gottlieb–Orszag · Brandt','Smooth fine-grid error, correct it on coarse grids, and explore local and global approximations.','elliptic','brandt1977'],
 ['1974–1977','Moving with the fluid, or moving the mesh','Hirt–Amsden–Cook · Gingold–Monaghan · Lucy','Separate mesh velocity from fluid velocity, then replace fixed connectivity by particle kernel sums.','ale','hirt1974'],
 ['1978–1983','A shared language of benchmarks','Sod · van Leer · Orszag–Tang · Roe · Harten et al.','Use common test problems to compare contacts, acoustic waves, and magnetic structures.','benchmarks','sod1978'],
 ['1981–1987','Particles, meshes, and far-field expansions','Hockney–Eastwood · Barnes–Hut · Greengard–Rokhlin','Assign mass to a grid, organize nearby particles in a tree, and reuse distant interactions through expansions.','particle-gravity','barnes1986'],
 ['1987–1989','Higher order and magnetic constraints','Harten et al. · Turkel · Einfeldt · Evans–Hawley · Shu–Osher','High order, positivity, entropy correction, and magnetic divergence become distinct design questions.','mhd','evans1988'],
 ['1990','Compose a canonical map','Yoshida','Build higher-order symplectic steps from symmetric lower-order maps, and separate energy error from geometry.','symplectic','yoshida1990'],
 ['1991–1996','Physical time and nonlinear weights','Jameson · Toro et al. · Liu–Osher–Chan · Jiang–Shu','Explore dual time, contact restoration, low-density flows, and WENO5-JS reconstruction.','advanced','jiang1996'],
 ['2000–2008','Multidimensional robustness','Tóth · Dedner et al. · Abgrall · Nishikawa–Kitamura','Examine discrete constraints and the path toward residual distribution and rotated-hybrid fluxes.','advanced','dedner2002'],
 ['2005–2009','The boundary is part of the force','Springel · Koyama–Ostriker','Split short and long ranges, then distinguish isolated kernels from periodic-horizontal disk gravity.','gravity-boundaries','koyama2009']
];
let documents, references, sod, experiments, foundations;
const eyebrow = text => `<p class="eyebrow">${text}</p>`;
const arrow = '<span aria-hidden="true">↗</span>';
const figureCard = (f, i) => `<article class="figure-card"><button class="figure-open" data-figure="${figures.indexOf(f)}" aria-label="Enlarge ${escapeHTML(f.title)}"><img src="assets/${f.file}" alt="${escapeHTML(f.description)}" loading="lazy" width="1000" height="450"><span class="enlarge" aria-hidden="true">＋</span></button><div class="figure-meta"><span>${f.category}</span><span>${f.year}</span></div><h3>${f.title}</h3><p>${f.description}</p><a class="text-link" href="#/read/${f.chapter}">Read the method ${arrow}</a></article>`;
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
 return `<section class="hero page-width"><div class="hero-copy">${eyebrow('AN EXECUTABLE ATLAS · FIRST EDITION')}<h1>The ideas behind<br>the <em>computation.</em></h1><p class="hero-description">A journey through numerical algorithms.<br>From the original paper to the computed solution.</p><div class="hero-actions"><a class="button primary" href="#/atlas">Explore the atlas <span aria-hidden="true">→</span></a><a class="text-link" href="#/read/benchmarks">Start with a benchmark ${arrow}</a></div><div class="hero-footnote"><span class="status-dot"></span> Python · Reproducible examples · Public source</div></div><div class="hero-experiment"><div class="experiment-heading"><span class="eyebrow">A CLASSIC, COMPUTED</span><span class="small-mono">1978 / SOD</span></div><h2>One problem.<br>Different numerical lenses.</h2><div id="sod-chart">${plot()}</div><div class="chart-legend"><span class="legend-exact">Exact solution</span><span class="legend-numerical">MUSCL + <span id="flux-label">Roe</span></span></div><div class="flux-controls" aria-label="Choose Riemann flux">${['roe','hllc','hll','rusanov'].map((s,i)=>`<button data-flux="${s}" aria-pressed="${i===0}">${s==='roe'?'Roe':s==='rusanov'?'Rusanov':s.toUpperCase()}</button>`).join('')}</div><p class="experiment-note">N = 200 · t = 0.20 · pointwise density comparison</p><a class="experiment-source" href="#/read/benchmarks">See the setup & verification ${arrow}</a></div></section>
 <section class="principles page-width" id="reading-guide" aria-label="How to use the atlas"><div><span>01</span><p><strong>Read the paper.</strong> Find the original idea and the sources behind it.</p></div><div><span>02</span><p><strong>Understand the method.</strong> Follow the equations, assumptions, and limits.</p></div><div><span>03</span><p><strong>Run the benchmark.</strong> Inspect the result and the evidence that checks it.</p></div></section>
 <section class="section page-width"><div class="section-heading"><div>${eyebrow('FOLLOW THE IDEAS')}<h2>A century of better questions.</h2></div><a class="text-link" href="#/atlas">Open the historical atlas ${arrow}</a></div><div class="history-strip">${[['1928','Can the stencil reach it?','CFL'],['1959','What crosses the interface?','GODUNOV'],['1977','Which scale holds the error?','MULTIGRID'],['1996','Where should the weights go?','WENO5-JS']].map(([year,title,label])=>`<a href="#/atlas"><span class="history-year">${year}</span><h3>${title}</h3><span class="small-mono">${label} <span aria-hidden="true">→</span></span></a>`).join('')}</div></section>
 <section class="experiment-invitation page-width"><div><p class="eyebrow">NEW / INTERACTIVE NOTEBOOKS</p><h2>Change a parameter.<br>Ask a better question.</h2><p>Explore stability with live calculations, then examine the measured orders behind a refinement plot.</p></div><a class="experiment-entry" href="#/experiments"><span class="small-mono">01 / COMPUTE</span><h3>The stability laboratory</h3><p>CFL, direction, and stencil.<br>One wave, four methods.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/convergence"><span class="small-mono">02 / INSPECT</span><h3>The convergence notebook</h3><p>Elements, unknowns, errors,<br>and observed orders.</p><span aria-hidden="true">↗</span></a></section>
 <section class="page-width foundation-links"><a class="experiment-entry" href="#/time-integration"><span class="small-mono">03 / TIME INTEGRATION</span><h3>Follow the orbit.</h3><p>Seven methods, two leapfrog roots,<br>and one exact oscillator.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/meshes"><span class="small-mono">04 / MESH EXPLORER</span><h3>Inspect the neighbors.</h3><p>Structured grids, triangles,<br>and irregular connectivity.</p><span aria-hidden="true">↗</span></a></section>
 <aside class="callout page-width"><p class="eyebrow">NEW / HAMILTONIAN MAPS & PARTICLE GRAVITY</p><h2>Preserve the geometry. Choose the boundary.</h2><p>Inspect canonical maps and energy histories, then follow particles through PM, Tree forces, multipole expansions, and isolated or slab Poisson kernels.</p><a class="text-link" href="#/hamiltonian">Open the Hamiltonian notebook ↗</a> · <a class="text-link" href="#/read/gravity-boundaries">Read the gravity kernels ↗</a></aside>
 <section class="section methods-section"><div class="page-width"><div class="section-heading"><div>${eyebrow('EXPLORE BY METHOD')}<h2>From a stencil to a solver.</h2></div><a class="text-link" href="#/methods">All methods ${arrow}</a></div><div class="method-grid">${methods.slice(0,3).map(methodCard).join('')}</div></div></section>
 <section class="section page-width"><div class="section-heading"><div>${eyebrow('THE COMPUTED EVIDENCE')}<h2>See the method at work.</h2></div><a class="text-link" href="#/gallery">Browse the gallery ${arrow}</a></div><div class="figure-grid home-figures">${[figures[0],figures[2],figures[3]].map(figureCard).join('')}</div><p class="scope-note"><span aria-hidden="true">↳</span> Independent educational implementations. Each exhibit states its reference solution, assumptions, and verification limits.</p></section>
 <section class="reading-banner page-width"><div>${eyebrow('KEEP THE PAPER CLOSE')}<h2>Every method has a history.<br>Every result needs a reference.</h2><p>${references.length} research and source records, ordered by original publication year.<br>Source notes distinguish original texts, later expositions, and open questions.</p><a class="button primary" href="#/references">Explore the references <span aria-hidden="true">→</span></a></div><div class="reference-mark" aria-hidden="true">[${references.length}]<span>1928 — 2026</span></div></section>
 <aside class="memorial-note page-width"><div><p class="eyebrow">IN MEMORIAM · PHILIP L. ROE</p><h2>A legacy carried by the waves.</h2><p>Remembering his contribution to computational fluid dynamics through the original ideas, their equations, and the questions they continue to open.</p></div><a class="text-link" href="#/read/roe-memorial">Read the tribute ↗</a></aside>
 <section class="run-section page-width"><div>${eyebrow('YOUR NEXT EXPERIMENT')}<h2>Start with Sod.</h2><p>The same definitions and solvers used in this atlas are available in the Python library.</p><a class="text-link" href="${repo}#getting-started">Installation & source ${arrow}</a></div><div class="terminal"><div class="terminal-title"><span>TERMINAL · AFTER INSTALLATION</span><button class="copy-command" data-copy="python -m numart.cli run sod --method muscl --riemann roe --n 200">Copy</button></div><pre><code><span class="prompt">$</span> python -m numart.cli run sod \
    --method muscl --riemann roe --n 200</code></pre><p>Numerical arrays + a run manifest, saved together.</p></div></section>`;
}
function atlas() {
 return `<section class="page-intro page-width">${eyebrow('THE HISTORICAL ATLAS')}<h1>Follow the ideas<br>through <em>time.</em></h1><p>Read by original publication year. Trace the questions that connect a classical stencil to a modern solver.</p><a class="text-link" href="#/read/history">Read the complete historical notes ${arrow}</a></section><section class="timeline page-width">${eras.map(([year,title,authors,description,chapter,ref])=>`<article class="timeline-item"><div class="timeline-year">${year}</div><div><p class="small-mono">${authors}</p><h2>${title}</h2><p>${description}</p><div class="timeline-links"><a href="#/read/${chapter}">Explore the method →</a><a href="#/references?q=${ref}">Read the source ↗</a></div></div></article>`).join('')}</section><aside class="callout page-width"><h2>A reading path, not a priority claim.</h2><p>Publication dates distinguish originals from translations and reprints. The reference notes record source status, and the atlas does not assign every invention to a single paper.</p><a class="text-link" href="#/read/nasa-2d">Continue toward NASA verification & validation cases ${arrow}</a></aside>`;
}
function methodPage() {
 return `<section class="page-intro page-width">${eyebrow('EXPLORE BY METHOD')}<h1>Understand the<br><em>discretization.</em></h1><p>${methods.length} entry points into tested models and method reading notes. Start with the equations, follow the numerical choices, and check the evidence.</p></section><section class="page-width method-grid full-methods">${methods.map(methodCard).join('')}</section><aside class="callout page-width"><h2>Implementation and ambition, clearly separated.</h2><p>The first edition includes selected educational models. Multidimensional Euler rotated-hybrid fluxes, low-Mach PDE preconditioning, Euler/MHD DG, and the cataloged NASA airfoil, viscous, and turbulence cases remain future work.</p><a class="text-link" href="#/read/roadmap">Read the implementation roadmap ${arrow}</a></aside>`;
}
function gallery() {
 return `<section class="page-intro page-width">${eyebrow('THE NUMERICAL GALLERY')}<h1>Look closely<br>at the <em>result.</em></h1><p>Computed figures from the first edition. Open a figure, then follow its method and benchmark definitions.</p></section><section class="page-width"><div class="filter-bar" aria-label="Filter gallery">${['All figures','Particles & gravity','2D shock interactions','Conservation laws','Advection & stability','MHD','Elliptic & iterative'].map((c,i)=>`<button data-gallery-filter="${c}" aria-pressed="${i===0}">${c}</button>`).join('')}</div><div class="figure-grid gallery-grid">${figures.map(figureCard).join('')}</div><p class="scope-note">These comparisons are educational examples, not reproductions of original-paper figures. Read the method notes before comparing accuracy, cost, or magnetic-divergence measures.</p><a class="text-link" href="assets/validation.json">Download the original eleven-figure validation manifest ${arrow}</a><br><a class="text-link" href="assets/double-mach-run.json">Download the Double Mach Reflection run manifest ${arrow}</a></section>`;
}
function referenceItem(e) {
 const source=e.doi?`https://doi.org/${e.doi}`:e.source;
 return `<article class="reference-item"><div class="reference-year">${e.year}</div><div><p class="reference-authors">${escapeHTML(e.author.replace(/ and /g,'; '))}</p><h2>${escapeHTML(e.title)}</h2><p class="reference-publication">${escapeHTML(e.journal||e.publisher||e.institution||e.booktitle||'')}${e.volume?` · ${escapeHTML(e.volume)}`:''}${e.pages?` · pp. ${escapeHTML(e.pages.replace('--','–'))}`:''}</p><p class="reference-note">${escapeHTML(e.note)}</p><div class="reference-links"><a href="${escapeHTML(source)}" target="_blank" rel="noopener">Original record ↗</a><a href="${escapeHTML(e.source)}" target="_blank" rel="noopener">Text / implementation source ↗</a><code>${e.id}</code></div></div></article>`;
}
function referencePage(query='') {
 return `<section class="page-intro page-width">${eyebrow('THE REFERENCE LIBRARY')}<h1>Return to<br>the <em>source.</em></h1><p>${references.length} research and source records. Original publication dates, implementation sources, and honest notes on what has been verified.</p></section><section class="page-width reference-layout"><aside class="reference-aside"><label for="reference-search">Search the library</label><div class="search-wrap"><span aria-hidden="true">⌕</span><input id="reference-search" type="search" value="${escapeHTML(query)}" placeholder="Author, method, year…" autocomplete="off"></div><p id="reference-count" aria-live="polite"></p><a class="text-link" href="assets/references.bib" download>Download BibTeX ↓</a><p class="aside-note">A DOI identifies a publication. It does not imply that its full text has been inspected or its figures reproduced.</p><a href="#/read/references">Read the complete catalog →</a></aside><div id="reference-results"></div></section>`;
}
function filterReferences(query) {
 const q=query.toLowerCase().trim();
 const matches=references.filter(e=>[e.author,e.title,e.year,e.id,e.note].join(' ').toLowerCase().includes(q));
 document.querySelector('#reference-results').innerHTML=matches.length?matches.map(referenceItem).join(''):'<div class="empty-state"><h2>No references found.</h2><p>Try an author, a method such as WENO, or a publication year.</p></div>';
 document.querySelector('#reference-count').textContent=`${matches.length} of ${references.length} references`;
}
function chapter(id) {
 const d=documents[id];
 if(!d) return notFound();
 const links=[['history','Historical atlas'],['experiments','Interactive experiment guide'],...methods.filter((m,i,a)=>a.findIndex(x=>x.id===m.id)===i).map(m=>[m.id,m.title]),['roe-memorial','Remembering Philip L. Roe'],['nasa-2d','NASA case catalog'],['references','Reference catalog'],['roadmap','Implementation roadmap'],['release-notes-v0.1.0','First-edition notes']];
 return `<div class="reading-shell page-width"><aside class="reading-nav"><a class="back-link" href="#/methods">← Explore the methods</a><p class="eyebrow">IN THIS EDITION</p><nav aria-label="Reading chapters">${links.map(([key,label])=>`<a href="#/read/${key}" ${id===key?'aria-current="page"':''}>${label}</a>`).join('')}</nav><p class="small-mono">FIRST EDITION · v0.1.0</p></aside><div class="chapter-wrap"><div class="chapter-topline"><span>THE READING ROOM</span><a href="${repo}/blob/main/docs/${id}.md">View source ↗</a></div><article class="prose">${d.html}</article><div class="chapter-bottom"><span>Continue exploring</span><a href="#/atlas">Historical atlas →</a><a href="#/gallery">Computed gallery →</a></div></div><aside class="chapter-toc"><p class="eyebrow">ON THIS PAGE</p><nav aria-label="On this page">${d.headings.filter(h=>h.level===2).map(h=>`<a href="#/read/${id}?section=${h.id}">${h.title}</a>`).join('')}</nav></aside></div>`;
}
function notFound(){return `<section class="page-intro page-width"><p class="eyebrow">PAGE NOT FOUND</p><h1>Back to<br>the <em>atlas.</em></h1><p>This chapter could not be found.</p><a class="button primary" href="#/">Return home →</a></section>`;}
function wire() {
 document.querySelectorAll('[data-flux]').forEach(button=>button.addEventListener('click',()=>{
   const flux=button.dataset.flux; document.querySelector('#sod-chart').innerHTML=plot(flux);
   document.querySelector('#flux-label').textContent=button.textContent;
   document.querySelectorAll('[data-flux]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 }));
 document.querySelectorAll('[data-figure]').forEach(button=>button.addEventListener('click',()=>{
   const f=figures[Number(button.dataset.figure)],dialog=document.querySelector('#figure-dialog');
   dialog.querySelector('h2').textContent=f.title; dialog.querySelector('img').src=`assets/${f.file}`; dialog.querySelector('img').alt=f.description; dialog.querySelector('p').textContent=f.description; dialog.showModal();
 }));
 document.querySelectorAll('[data-gallery-filter]').forEach(button=>button.addEventListener('click',()=>{
   const category=button.dataset.galleryFilter;
   document.querySelectorAll('[data-gallery-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
   document.querySelectorAll('.gallery-grid .figure-card').forEach((card,i)=>card.hidden=category!=='All figures'&&figures[i].category!==category);
 }));
 document.querySelectorAll('.copy-command').forEach(button=>button.addEventListener('click',async()=>{
   try {await navigator.clipboard.writeText(button.dataset.copy);button.textContent='Copied';setTimeout(()=>button.textContent='Copy',1800);}
   catch {button.textContent='Select the command below';}
 }));
 document.querySelectorAll('.prose pre').forEach(pre=>{
   const button=document.createElement('button');button.className='code-copy';button.textContent='Copy';button.setAttribute('aria-label','Copy code example');
   button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(pre.querySelector('code').textContent);button.textContent='Copied';}catch{button.textContent='Select code to copy';}});pre.append(button);
 });
}
function route() {
 const [path,queryString='']=(location.hash.slice(1)||'/').split('?');
 const parts=path.split('/').filter(Boolean),type=parts[0]||'home',query=new URLSearchParams(queryString);
 const renderers={home,atlas,methods:methodPage,gallery,experiments:stabilityPage,convergence:convergencePage,'time-integration':timePage,meshes:meshPage,hamiltonian:hamiltonianPage,references:()=>referencePage(query.get('q')||''),read:()=>chapter(parts[1])};
 main.innerHTML=(renderers[type]||notFound)();
 document.body.dataset.page=type;
 document.querySelectorAll('[data-nav]').forEach(a=>{if(a.dataset.nav===type||(['convergence','time-integration','meshes','hamiltonian'].includes(type)&&a.dataset.nav==='experiments'))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 document.querySelector('.site-header').classList.remove('menu-open');document.querySelector('.mobile-menu').setAttribute('aria-expanded','false');
 document.title=type==='home'?'The Art of Numerical Algorithms':`${type==='read'?(documents[parts[1]]?.title||'Reading room'):({atlas:'Historical atlas',methods:'Explore the methods',gallery:'Numerical gallery',references:'Reference library',experiments:'Stability laboratory',convergence:'Convergence notebook','time-integration':'Time integration notebook',meshes:'Mesh explorer',hamiltonian:'Hamiltonian map notebook'}[type]||'Page not found')} · The Art of Numerical Algorithms`;
 if(type==='read')document.querySelectorAll('.heading-anchor').forEach(a=>{a.href=`#/read/${parts[1]}?section=${a.parentElement.id}`;});
 if(type==='references') {filterReferences(query.get('q')||'');document.querySelector('#reference-search').addEventListener('input',e=>filterReferences(e.target.value));}
 wire();
 if(type==='experiments')wireStability(experiments);
 if(type==='convergence')wireConvergence(experiments);
 if(type==='time-integration')wireTime(foundations);
 if(type==='meshes')wireMesh(foundations);
 if(type==='hamiltonian')wireHamiltonian();
 if(query.get('section'))requestAnimationFrame(()=>document.getElementById(query.get('section'))?.scrollIntoView());else window.scrollTo({top:0,behavior:'instant'});
}
document.querySelector('.skip-link').addEventListener('click',e=>{e.preventDefault();main.focus();main.scrollIntoView();});
document.querySelector('.mobile-menu').addEventListener('click',e=>{const open=document.querySelector('.site-header').classList.toggle('menu-open');e.currentTarget.setAttribute('aria-expanded',String(open));});
document.querySelector('.dialog-close').addEventListener('click',()=>document.querySelector('#figure-dialog').close());
document.querySelector('#figure-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close();});
try {
 [documents,references,sod,experiments,foundations]=await Promise.all(['content.json','references.json','sod.json','experiments.json','foundations.json'].map(async file=>{const response=await fetch(file);if(!response.ok)throw Error(`Cannot load ${file}`);return response.json();}));
 references.sort((a,b)=>a.year-b.year||a.id.localeCompare(b.id));
 window.addEventListener('hashchange',route);route();
} catch(error) {main.innerHTML=`<section class="page-intro page-width"><h1>The atlas could not load.</h1><p>Please reload the page, or read the complete edition on GitHub.</p><a class="button primary" href="${repo}">Open the source edition ↗</a></section>`;console.error(error);}
