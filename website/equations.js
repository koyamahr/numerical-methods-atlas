import {chart} from './experiments.js';
let dataset, timer;
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=value=>value===0?'0':Math.abs(value)<.0001?value.toExponential(3):Number(value.toPrecision(6)).toString();
export function disposeEquations(){if(timer){clearInterval(timer);timer=undefined;}}
export function equationsPage(){return `<section class="page-intro page-width"><p class="eyebrow">THE EQUATION GALLERY / COMPUTED PROFILES</p><h1>Choose the equation.<br>Follow its <em>waves.</em></h1><p>A shock, a rarefaction, an upstream traffic jam, or a diffusing mode. Compare actual numerical profiles with the reference appropriate to each equation.</p></section><section id="equation-gallery" class="laboratory page-width"><aside class="lab-controls"><p class="eyebrow">NINE CASES / SEVEN FAMILIES</p><label for="equation-case">Equation and initial data</label><select id="equation-case" disabled><option>Loading computed cases…</option></select><label for="equation-frame">Saved physical time <output id="equation-time" for="equation-frame">0</output></label><input id="equation-frame" type="range" min="0" max="0" value="0" step="1" disabled><div class="equation-playback"><button id="equation-play" type="button" class="button primary" aria-pressed="false" disabled>Play ▷</button><button id="equation-reset" type="button" class="button" disabled>Reset</button></div><p id="equation-initial" class="lab-settings"></p><p id="equation-boundary" class="lab-settings"></p><a class="text-link" href="#/read/equation-gallery">Definitions &amp; reference conventions ↗</a><a class="text-link" href="#/read/accuracy-stability">A/L stability &amp; error norms ↗</a><a class="text-link" href="equation-gallery.json" download>Download all profiles ↓</a></aside><div class="lab-results"><div id="equation-summary" class="lab-summary" aria-live="polite">Loading numerical data…</div><div class="lab-chart-card"><div class="lab-chart-header"><h2 id="equation-title">The solution</h2><span id="equation-family"></span></div><p id="equation-formula" class="equation-formula"></p><div id="equation-chart"></div><div id="equation-legend" class="lab-legend"></div><p id="equation-note" class="lab-chart-note"></p></div><div class="lab-lower"><aside class="lab-explanation"><p class="eyebrow">READ THE PROPAGATION</p><h2>Characteristic speed</h2><p id="equation-speed"></p><p id="equation-method"></p><a id="equation-method-link" class="text-link">Read the method ↗</a></aside><div class="lab-chart-card"><div class="lab-chart-header"><h2>Inspect the frame</h2></div><dl id="equation-metrics" class="equation-metrics"></dl><p id="equation-sampling" class="lab-chart-note"></p><a id="equation-source" class="text-link">Find the source ↗</a></div></div></div></section><aside class="callout page-width"><p class="eyebrow">EXPAND THE EQUATION MAP / STATUS SHOWN IN EACH CHAPTER</p><h2>From living systems to rotating fluids.</h2><p>Read a survey of 22 biological model families, then inspect Arakawa A/B/C variable placement and linear shallow-water wave dispersion.</p><a class="text-link" href="#/read/biological-models">Biological models / literature survey ↗</a> · <a class="text-link" href="#/read/geophysical-grids">Arakawa grids / tested linear symbols ↗</a></aside><section class="page-width equation-branches"><div class="section-heading"><div><p class="eyebrow">KINETIC &amp; AUXILIARY SYSTEMS</p><h2>Another route to the fluid.</h2></div></div><div class="method-grid"><a class="experiment-entry" href="#/read/lattice-boltzmann"><span class="small-mono">D2Q9 / BGK</span><h3>Collide and stream.</h3><p>Shear-mode viscosity, forced Poiseuille flow, and half-way walls.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/read/chapman-enskog"><span class="small-mono">CHAPMAN–ENSKOG</span><h3>Recover transport.</h3><p>Equilibrium, nonequilibrium stress, and the discrete-time τ−1/2 correction.</p><span aria-hidden="true">↗</span></a><a class="experiment-entry" href="#/read/hyperbolic-diffusion"><span class="small-mono">NISHIKAWA / STEADY DIFFUSION</span><h3>Evolve the gradient.</h3><p>A first-order hyperbolic system converges in pseudo-time to a steady elliptic solution.</p><span aria-hidden="true">↗</span></a></div></section><aside class="callout page-width"><h2>Keep the reference convention visible.</h2><p>Scalar curves compare exact cell averages. Euler, shallow-water and isothermal profiles compare conserved cell means of semi-analytic Riemann references. Fluid-system playback links independent final-time solves; the frame notes identify this explicitly.</p><a class="text-link" href="#/exact-solutions">Explore exact &amp; reference solutions ↗</a> · <a class="text-link" href="#/read/equation-gallery">Read the equation definitions ↗</a> · <a class="text-link" href="#/read/incompressible">Periodic incompressible flow ↗</a></aside>`;}

export async function wireEquations(){
 const root=document.getElementById('equation-gallery');
 const get=id=>root.querySelector(`#${id}`);
 try{
  dataset??=fetch('equation-gallery.json').then(r=>{if(!r.ok)throw Error('Cannot load equation data');return r.json();}).catch(e=>{dataset=undefined;throw e;});
  const data=await dataset;if(!root.isConnected)return;
  const select=get('equation-case'),slider=get('equation-frame'),play=get('equation-play');
  select.innerHTML=data.cases.map((c,i)=>`<option value="${i}">${esc(c.title)}</option>`).join('');
  for(const id of ['equation-case','equation-frame','equation-play','equation-reset'])get(id).disabled=false;
  const pause=()=>{disposeEquations();play.textContent='Play ▷';play.setAttribute('aria-pressed','false');};
  const update=()=>{
   if(!root.isConnected){disposeEquations();return;}
   const c=data.cases[Number(select.value)],index=Number(slider.value),f=c.frames[index];
   slider.max=c.frames.length-1;
   get('equation-title').textContent=c.title;get('equation-family').textContent=c.family;
   get('equation-formula').textContent=c.equation;get('equation-time').textContent=fmt(f.time);
   get('equation-initial').textContent=c.initial;get('equation-boundary').textContent=c.boundary;
   get('equation-summary').innerHTML=`<span>N = ${c.n} · t = ${fmt(f.time)}</span><span>Solver steps: ${f.step}</span><span>Frame ${index+1} / ${c.frames.length}</span>`;
   const series=[{points:c.x.map((x,i)=>[x,f.u[i]]),color:'#bf5b35'}];
   if(f.exact)series.push({points:c.x.map((x,i)=>[x,f.exact[i]]),color:'#23392f',dashed:true});
   const [lo,hi]=c.limits;
   get('equation-chart').innerHTML=chart({series,yMin:lo,yMax:hi,yTicks:[Math.max(0,lo),(lo+hi)/2,hi-.05],yLabel:c.field,title:`${c.title} at physical time ${fmt(f.time)}`});
   get('equation-legend').innerHTML=`<span style="--swatch:#bf5b35">Computed profile</span>${f.exact?`<span style="--swatch:#23392f">${esc(f.reference_measure)} / dashed</span>`:'<span>No exact overlay supplied</span>'}`;
   get('equation-note').textContent=c.note;get('equation-speed').textContent=c.characteristic;
   get('equation-method').textContent=c.method;get('equation-sampling').textContent=c.sampling;
   get('equation-method-link').href=`#/read/${c.chapter}`;
   const metric=(name,value)=>`<div><dt>${esc(name)}</dt><dd>${esc(value)}</dd></div>`;
   get('equation-metrics').innerHTML=metric('L1 / mean absolute error',f.l1===null?'Not supplied':fmt(f.l1))+metric('L2 / RMS error',f.l2===null?'Not supplied':fmt(f.l2))+metric('L∞ / maximum sampled error',f.linf===null?'Not supplied':fmt(f.linf))+metric('Discrete mean',fmt(f.mean))+metric(c.boundary.startsWith('Periodic')?'Mean change / conserved quantity':'Mean change / includes boundary flux',fmt(f.mean_change))+metric('Reference convention',f.reference_measure);
   get('equation-source').href=`#/references?q=${encodeURIComponent(c.reference)}`;
  };
  select.addEventListener('change',()=>{pause();slider.value=0;update();});
  slider.addEventListener('input',()=>{pause();update();});
  get('equation-reset').addEventListener('click',()=>{pause();slider.value=0;update();});
  play.addEventListener('click',()=>{
   if(timer){pause();return;}
   if(Number(slider.value)>=Number(slider.max))slider.value=0;
   play.textContent='Pause Ⅱ';play.setAttribute('aria-pressed','true');update();
   timer=setInterval(()=>{if(!root.isConnected){disposeEquations();return;}if(document.hidden){pause();return;}slider.value=Number(slider.value)+1;update();if(Number(slider.value)>=Number(slider.max))pause();},180);
  });
  update();
 }catch(e){if(root.isConnected)get('equation-summary').textContent='The equation profiles could not load. Reload to retry, or read the equation definitions below.';console.error(e);}
}
