import {METHODS,amplification,createExperiment,observedOrder} from './numerics.js';
export const notebookNav = active => `<nav class="experiment-tabs" aria-label="Experiment notebooks"><a href="#/experiments" ${active==='stability'?'aria-current="page"':''}>01 / Stability laboratory</a><a href="#/convergence" ${active==='convergence'?'aria-current="page"':''}>02 / Convergence notebook</a><a href="#/time-integration" ${active==='time'?'aria-current="page"':''}>03 / Time integration</a><a href="#/meshes" ${active==='mesh'?'aria-current="page"':''}>04 / Mesh explorer</a><a href="#/hamiltonian" ${active==='hamiltonian'?'aria-current="page"':''}>05 / Hamiltonian maps</a><a href="#/limiters" ${active==='limiters'?'aria-current="page"':''}>06 / Slope limiters</a><a href="#/runge-kutta" ${active==='rk'?'aria-current="page"':''}>07 / Runge–Kutta families</a></nav>`;
const number = v => Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=10000)?v.toExponential(2):v.toFixed(Math.abs(v)<10?3:1);
export const chart = ({series,xMin=0,xMax=1,yMin=-1.2,yMax=1.2,xTicks=[0,.25,.5,.75,1],yTicks=[-1,0,1],xLabel='POSITION x',yLabel='u',title,log=false,reference=null,square=false}) => {
 const w=600,left=62,right=25,top=28,bottom=45,h=square?w-left-right+top+bottom:310;
 const transform=v=>log?Math.log10(v):v;
 const x=v=>left+(transform(v)-transform(xMin))/(transform(xMax)-transform(xMin))*(w-left-right);
 const y=v=>h-bottom-(transform(v)-transform(yMin))/(transform(yMax)-transform(yMin))*(h-top-bottom);
 const path=points=>points.map(([a,b],i)=>`${i?'L':'M'}${x(a).toFixed(3)},${y(b).toFixed(3)}`).join(' ');
 return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${title}" class="lab-svg"><title>${title}</title>${yTicks.map(v=>`<line x1="${left}" x2="${w-right}" y1="${y(v)}" y2="${y(v)}" class="grid-line"/><text x="${left-10}" y="${y(v)+4}" text-anchor="end">${log?v.toExponential(0):number(v)}</text>`).join('')}${xTicks.map(v=>`<text x="${x(v)}" y="${h-bottom+23}" text-anchor="middle">${log?v:number(v)}</text>`).join('')}<text x="${left}" y="14" class="axis-title">${yLabel}</text><text x="${w-right}" y="${h-6}" text-anchor="end" class="axis-title">${xLabel}</text>${reference===null?'':`<line x1="${left}" x2="${w-right}" y1="${y(reference)}" y2="${y(reference)}" class="stability-threshold"/>`}${series.map(s=>`<path d="${path(s.points)}" fill="none" stroke="${s.color}" stroke-width="${s.dashed?1.8:2.5}" ${s.dashed?'stroke-dasharray="5 4"':''}/>${s.dots?s.points.map(([a,b])=>`<circle cx="${x(a)}" cy="${y(b)}" r="4" fill="${s.color}"/>`).join(''):''}`).join('')}</svg>`;
};

export function stabilityPage() {
 return `<section class="page-intro page-width">${notebookNav('stability')}<p class="eyebrow">COMPUTE IN THE BROWSER</p><h1>When does a wave <em>grow?</em></h1><p>Change the Courant number, stencil, or direction. Watch the same periodic advection problem through its solution and Fourier amplification.</p></section>
 <section class="page-width laboratory"><aside class="lab-controls"><p class="eyebrow">SET THE EXPERIMENT</p><label for="lab-method">Difference method</label><select id="lab-method">${Object.entries(METHODS).map(([key,m])=>`<option value="${key}" ${key==='lax-wendroff'?'selected':''}>${m.label}</option>`).join('')}</select><label for="lab-courant">Courant magnitude <output id="courant-output" for="lab-courant">0.80</output></label><input type="range" id="lab-courant" min="0.05" max="1.5" step="0.05" value="0.8"><div class="range-ends"><span>0.05</span><span>1.50</span></div><label for="lab-direction">Advection velocity</label><select id="lab-direction"><option value="1">a = +1 · to the right</option><option value="-1">a = −1 · to the left</option></select><label for="lab-steps">Time steps <output id="steps-output" for="lab-steps">40</output></label><input id="lab-steps" type="range" min="0" max="100" step="1" value="40"><div class="range-ends"><span>0</span><span>100</span></div><label for="lab-profile">Initial data</label><select id="lab-profile"><option value="ripple">Sine + small grid-scale ripple</option><option value="sine">Smooth sine wave</option><option value="square">Square pulse</option></select><p class="lab-settings">N = 64 · periodic [0, 1]<br>Δx = 1/64 · Δt = |C| Δx<br>Signed C = a Δt / Δx</p><button id="download-experiment" class="button lab-download">Download experiment ↓</button><a class="text-link" href="#/read/experiments">Definitions & limitations ↗</a></aside>
 <div class="lab-results"><div class="lab-presets" aria-label="Suggested experiments"><button data-preset="diffusion">Stable, but diffusive</button><button data-preset="second-order">Second order</button><button data-preset="beyond-cfl">Beyond CFL</button><button data-preset="ftcs">CFL is not enough</button></div><div id="lab-summary" class="lab-summary" aria-live="polite"></div><div class="lab-chart-card"><div class="lab-chart-header"><h2>The transported solution</h2><span id="physical-time"></span></div><div id="solution-chart"></div><div class="lab-legend"><span style="--swatch:#65796c" class="dashed">Exact translation</span><span style="--swatch:#bf5b35">Computed samples</span></div><p id="solution-scale" class="lab-chart-note"></p></div><div class="lab-lower"><div class="lab-chart-card"><div class="lab-chart-header"><h2>Fourier amplification</h2></div><div id="amplification-chart"></div><p class="lab-chart-note">The dashed line marks |G| = 1. Growth above it identifies unstable modes for this periodic linear problem.</p></div><div class="lab-explanation"><p class="eyebrow">READ THE RESULT</p><h2 id="method-name"></h2><p id="method-explanation"></p><dl id="lab-metrics"></dl><a class="text-link" href="#/read/stability">Follow the derivation ↗</a></div></div></div></section>
 <aside class="callout page-width lab-scope"><h2>A controlled model, with a precise scope.</h2><p>The browser runs the periodic finite-difference updates directly. Its numerical kernels are checked against 24 Python reference cases, including both velocity signs and unstable settings. The Fourier result applies to constant-coefficient linear advection; it does not certify nonlinear Euler, WENO, or arbitrary boundaries.</p><a class="text-link" href="https://github.com/koyamahr/the-art-of-numerical-algorithms/blob/main/numart/advection.py">Read the Python implementation ↗</a></aside>`;
}

export function convergencePage() {
 return `<section class="page-intro page-width">${notebookNav('convergence')}<p class="eyebrow">READ THE COMPUTED EVIDENCE</p><h1>Smaller cells. What gets <em>better?</em></h1><p>Inspect the first-edition grid-refinement measurements. Compare errors, read observed orders, and distinguish elements from unknowns.</p></section><section class="page-width convergence-notebook"><div class="convergence-controls"><div><label for="convergence-study">Refinement study</label><select id="convergence-study"><option value="dg">Periodic DG advection · P0 / P1 / P2</option><option value="entropy">Euler entropy wave · MUSCL / WENO5-JS</option></select></div><div id="axis-control"><label for="convergence-axis">Horizontal axis</label><select id="convergence-axis"><option value="grid">Elements N</option><option value="dof">Unknowns N × (p + 1)</option></select></div></div><div class="convergence-layout"><div class="lab-chart-card"><div class="lab-chart-header"><h2 id="convergence-title"></h2><span>LOG–LOG SCALE</span></div><div id="convergence-chart"></div><div id="convergence-legend" class="lab-legend"></div><p class="lab-chart-note" id="convergence-norm"></p></div><aside class="lab-explanation"><p class="eyebrow">WHAT IS BEING COMPARED?</p><div id="convergence-explanation"></div><a class="text-link" href="#/read/experiments?section=reading-a-refinement-study">How to read the order ↗</a></aside></div><div class="measurement-header"><h2>Inspect the measurements</h2><div><label for="convergence-series">Series</label><select id="convergence-series"></select></div></div><div class="measurement-scroll"><table class="measurement-table"><thead><tr><th scope="col" id="measurement-grid-label">Elements N</th><th scope="col">Scalar unknowns</th><th scope="col">Measured error</th><th scope="col">Observed order</th></tr></thead><tbody id="measurement-rows"></tbody></table></div><p class="lab-chart-note">Order between successive grids: p = log(E<sub>coarse</sub>/E<sub>fine</sub>) / log(N<sub>fine</sub>/N<sub>coarse</sub>). A dash means no coarser grid is listed.</p></section><aside class="callout page-width"><h2>Evidence, not a universal ranking.</h2><p>These are the existing gallery measurements, not new timings. Different degrees of freedom, stencils, time integrators, and error definitions prevent a simple cost ranking. Expected spatial order, observed fully discrete order, and nonlinear stability are separate claims.</p><a class="text-link" href="assets/validation.json">Download the original gallery manifest ↗</a></aside>`;
}

function download(data,name) {
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
export function wireStability(data) {
 const get=id=>document.getElementById(id);
 let snapshot;
 const update=()=>{
  const method=get('lab-method').value,courant=Number(get('lab-courant').value)*Number(get('lab-direction').value),steps=Number(get('lab-steps').value),profile=get('lab-profile').value;
  const settings={method,courant,steps,n:64,profile};
  snapshot=createExperiment(settings,data.advection_reference_sha256);
  const result=snapshot,stable=result.maxG<=1+1e-12;
  get('courant-output').textContent=Math.abs(courant).toFixed(2);get('steps-output').textContent=steps;
  get('lab-summary').innerHTML=`<span class="growth-status ${stable?'bounded':'growing'}">${stable?'Bounded Fourier modes':'Growing Fourier modes'}</span><span>max discrete |G| = <strong>${result.maxG.toFixed(3)}</strong></span><span>C = ${courant.toFixed(2)}</span>`;
  get('physical-time').textContent=`t = ${result.time.toFixed(3)} · ${steps} steps`;
  const scale=Math.max(1.2,...result.values.map(v=>Math.abs(v)*1.1));
  get('solution-chart').innerHTML=chart({series:[{points:result.x.map((x,j)=>[x,result.exact[j]]),color:'#65796c',dashed:true},{points:result.x.map((x,j)=>[x,result.values[j]]),color:'#bf5b35'}],yMin:-scale,yMax:scale,yTicks:[-scale,0,scale],title:`${METHODS[method].label} solution after ${steps} time steps at C=${courant.toFixed(2)}`});
  get('solution-scale').textContent=scale>2?'The vertical scale has expanded to show the growing solution. Compare the amplitude and error below.':'Exact values are sampled from the continuous periodic translation of the selected initial data.';
  const samples=Array.from({length:257},(_,j)=>[j/256*Math.PI,amplification(j/256*Math.PI,courant,method).magnitude]);
  const gMax=Math.max(1.25,...samples.map(p=>p[1]*1.08));
  get('amplification-chart').innerHTML=chart({series:[{points:samples,color:'#bf5b35'}],xMax:Math.PI,yMin:0,yMax:gMax,xTicks:[0,Math.PI/2,Math.PI],yTicks:[0,1],xLabel:'WAVENUMBER ANGLE θ (RADIANS)',yLabel:'|G(θ)|',title:`Fourier amplification for ${METHODS[method].label}`,reference:1});
  get('method-name').textContent=METHODS[method].label;get('method-explanation').textContent=METHODS[method].description;
  get('lab-metrics').innerHTML=`<div><dt>Pointwise L1 error</dt><dd>${number(result.l1)}</dd></div><div><dt>Maximum |u|</dt><dd>${number(result.amplitude)}</dd></div><div><dt>Mean drift</dt><dd>${number(result.meanDrift)}</dd></div>`;
 };
 ['lab-method','lab-courant','lab-direction','lab-steps','lab-profile'].forEach(id=>get(id).addEventListener('input',update));
 const presets={diffusion:['upwind',.8,64],'second-order':['lax-wendroff',.8,64],'beyond-cfl':['lax-wendroff',1.1,40],ftcs:['ftcs',.8,40]};
 document.querySelectorAll('[data-preset]').forEach(button=>button.addEventListener('click',()=>{
  const [method,courant,steps]=presets[button.dataset.preset];get('lab-method').value=method;get('lab-courant').value=courant;get('lab-steps').value=steps;get('lab-profile').value='ripple';get('lab-direction').value='1';update();
 }));
 get('download-experiment').addEventListener('click',()=>download(snapshot,'periodic-advection-experiment.json'));
 update();
}
export function wireConvergence(data) {
 const get=id=>document.getElementById(id),colors=['#bf5b35','#557e66','#677ea0'];
 let currentStudy='';
 const update=()=>{
  const kind=get('convergence-study').value,study=data[kind],dof=kind==='dg'&&get('convergence-axis').value==='dof';
  get('axis-control').hidden=kind!=='dg';
  if(currentStudy!==kind){get('convergence-series').innerHTML=study.series.map((s,i)=>`<option value="${i}">${s.label}</option>`).join('');currentStudy=kind;}
  const series=study.series.map((s,i)=>({points:study.n.map((n,j)=>[n*(dof?s.degree+1:1),s.errors[j]]),color:colors[i],dots:true}));
  const xAll=series.flatMap(s=>s.points.map(p=>p[0])),yAll=series.flatMap(s=>s.points.map(p=>p[1]));
  const yMin=10**Math.floor(Math.log10(Math.min(...yAll))),yMax=10**Math.ceil(Math.log10(Math.max(...yAll)));
  const yTicks=[];for(let e=Math.log10(yMin);e<=Math.log10(yMax)+.01;e++)yTicks.push(10**e);
  const xTicks=dof?[8,16,32,64,128,192]:study.n;
  get('convergence-chart').innerHTML=chart({series,xMin:Math.min(...xAll)*.9,xMax:Math.max(...xAll)*1.1,yMin,yMax,xTicks,yTicks,xLabel:dof?'SCALAR UNKNOWNS N × (p + 1)':kind==='dg'?'ELEMENTS N':'GRID POINTS / CELLS N',yLabel:'MEASURED ERROR',title:kind==='dg'?'DG grid-refinement errors':'Euler entropy-wave grid-refinement errors',log:true});
  get('convergence-title').textContent=kind==='dg'?'Periodic DG advection':'Euler entropy wave';
  get('convergence-legend').innerHTML=study.series.map((s,i)=>`<span style="--swatch:${colors[i]}">${s.label}</span>`).join('');
  get('convergence-norm').textContent=`${study.norm} · t = ${study.time} · CFL = ${study.cfl}`;
  get('convergence-explanation').innerHTML=kind==='dg'?'<h2>Elements are not unknowns.</h2><p>DG P0, P1, and P2 store 1, 2, and 3 scalar unknowns per element. Change the horizontal axis to see that distinction.</p><p>The expected smooth spatial orders are 1, 2, and 3. SSPRK3 also limits the fully discrete time order to three. Errors are sampled at the implementation’s quadrature points, rather than a separately integrated L2 norm.</p>':'<h2>Spatial order is not the whole story.</h2><p>Primitive minmod MUSCL and componentwise FD WENO5-JS evolve a smooth periodic Euler entropy wave at the listed CFL.</p><p>WENO5-JS has fifth-order spatial reconstruction, while SSPRK3 is third order in time. The measured slopes reflect this fully discrete setup; they do not guarantee fifth-order behavior under unlimited refinement. The error is a pointwise density L1 comparison.</p>';
  const s=study.series[Number(get('convergence-series').value)],orders=s.errors.map((v,i)=>i?observedOrder(s.errors[i-1],v,study.n[i]/study.n[i-1]):null);
  get('measurement-grid-label').textContent=kind==='dg'?'Elements N':'Points / cells N';
  get('measurement-rows').innerHTML=study.n.map((n,j)=>`<tr><th scope="row">${n}</th><td>${n*(kind==='dg'?s.degree+1:3)}</td><td>${s.errors[j].toExponential(5)}</td><td>${orders[j]===null?'—':orders[j].toFixed(3)}</td></tr>`).join('');
 };
 ['convergence-study','convergence-axis','convergence-series'].forEach(id=>get(id).addEventListener('change',update));
 update();
}
