import {chart,notebookNav} from './experiments.js';
import {translateText} from './i18n.js';
let dataset;
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const kindLabels={'analytic':'Analytic reference','semi-analytic':'Semi-analytic reference','manufactured':'Manufactured solution'};
const fmt=v=>v===0?'0':Number(v.toPrecision(6)).toString();
export const referencePage=()=>`<section class="page-intro page-width">${notebookNav('exact')}<p class="eyebrow">EXACT &amp; REFERENCE SOLUTIONS</p><h1>Know the answer.<br>Check the <em>approximation.</em></h1><p>Explore analytic formulas, root-solved Riemann waves and a manufactured solution. See why a point value and a finite-volume cell mean answer different questions.</p></section><section id="reference-library" class="laboratory page-width"><aside class="lab-controls"><label for="reference-case">Reference problem</label><select id="reference-case" disabled><option>Loading reference solutions…</option></select><label for="reference-component">Reference component</label><select id="reference-component" disabled></select><label for="reference-frame">Reference time <output id="reference-time" for="reference-frame">0</output></label><input id="reference-frame" type="range" min="0" max="8" step="1" value="8" disabled><label for="reference-grid">Cells for averaging</label><select id="reference-grid" disabled><option value="16">16</option><option value="32">32</option><option value="64">64</option></select><label><input id="reference-centers" type="checkbox"> Show cell-center point samples</label><p class="lab-settings">Saved formula evaluations; no PDE solver runs in this browser.</p><a class="text-link" href="#/read/reference-solutions">Formulas, API &amp; verification ↗</a><a class="text-link" href="#/equations">Compare computed profiles ↗</a><a class="text-link" href="assets/reference-solutions.json" download>Download reference evaluations ↓</a></aside><div class="lab-results"><div id="reference-summary" class="lab-summary" aria-live="polite">Loading reference solutions…</div><div class="lab-chart-card"><div class="lab-chart-header"><h2 id="reference-title">Reference solution</h2><span id="reference-kind"></span></div><p id="reference-formula" class="equation-formula" data-original></p><div id="reference-chart"></div><div id="reference-legend" class="lab-legend"></div><p id="reference-convention" class="lab-chart-note"></p></div><div class="lab-lower"><aside class="lab-explanation"><h2>Assumptions &amp; boundaries</h2><p id="reference-assumptions"></p><pre id="reference-parameters" data-original></pre><div id="reference-sources"></div></aside><div class="lab-chart-card"><h2>Reference accuracy</h2><dl id="reference-metrics" class="equation-metrics"></dl><p>Quadrature order differences estimate convergence; they are not rigorous error bounds. Root solving and quadrature both use finite precision.</p><p>A high-resolution numerical reference still has discretization error. It belongs to a separate category from these formula-based cases.</p></div></div></div></section><aside class="callout page-width"><h2>A reusable verification library.</h2><p>Python supports arbitrary one-dimensional cell edges, conserved-variable averages, volume-weighted error norms and smooth multidimensional box averages. Dry-bed and vacuum reference formulas do not extend the admissible states of the existing numerical solvers.</p><a class="text-link" href="#/read/reference-solutions">Read the reference guide ↗</a></aside>`;

export async function wireReferences(requested){
 const root=document.getElementById('reference-library'),get=id=>root.querySelector(`#${id}`);
 try{
  dataset??=fetch('assets/reference-solutions.json').then(r=>{if(!r.ok)throw Error('Cannot load reference solutions');return r.json();}).catch(e=>{dataset=undefined;throw e;});
  const data=await dataset;if(!root.isConnected)return;
  const select=get('reference-case'),component=get('reference-component'),slider=get('reference-frame'),grid=get('reference-grid'),centers=get('reference-centers');
  select.innerHTML=data.cases.map(c=>`<option value="${esc(c.id)}">${esc(translateText(c.title))}</option>`).join('');
  select.value=data.cases.some(c=>c.id===requested)?requested:'euler-sod';
  select.disabled=component.disabled=false;
  let previous;
  const metric=(label,value)=>`<div><dt>${esc(translateText(label))}</dt><dd>${esc(value)}</dd></div>`;
  const update=()=>{
   const c=data.cases.find(c=>c.id===select.value);
   if(previous!==c.id){component.innerHTML=c.components.map((name,j)=>`<option value="${j}">${esc(name)}</option>`).join('');slider.max=c.frames.length-1;slider.value=slider.max;previous=c.id;}
   const j=Number(component.value),f=c.frames[Number(slider.value)],g=f.grids.find(g=>g.n===Number(grid.value));
   slider.disabled=c.frames.length===1;grid.disabled=centers.disabled=c.dimension!==1;
   get('reference-title').textContent=c.title;get('reference-kind').textContent=kindLabels[c.kind];
   get('reference-formula').textContent=c.formula;get('reference-time').textContent=fmt(f.time);
   get('reference-summary').innerHTML=`<span>${esc(translateText(kindLabels[c.kind]))}</span><span>t = ${fmt(f.time)}</span><span>${esc(translateText(c.field_type))}</span>`;
   const series=[{points:c.x.map((x,i)=>[x,f.point[i][j]]),color:'#23392f'}];
   if(g){series.push({points:g.average.flatMap((q,i)=>[[g.edges[i],q[j]],[g.edges[i+1],q[j]]]),color:'#bf5b35'});if(centers.checked)series.push({points:g.x.map((x,i)=>[x,g.center_values[i][j]]),color:'#677ea0',dots:true,dashed:true});}
   const [lo,hi]=c.limits[j],[a,b]=c.bounds[0];
   get('reference-chart').innerHTML=chart({series,xMin:a,xMax:b,xTicks:[a,(a+b)/2,b],yMin:lo,yMax:hi,yTicks:[lo,(lo+hi)/2,hi],xLabel:c.id==='couette'||c.id==='poiseuille'?'y':'x',yLabel:esc(c.components[j]),title:esc(translateText(c.title))});
   get('reference-legend').innerHTML=`<span style="--swatch:#23392f">${esc(translateText('Point reference'))}</span>${g?`<span style="--swatch:#bf5b35">${esc(translateText('Cell mean / piecewise constant'))}</span>`:''}${g&&centers.checked?`<span style="--swatch:#677ea0">${esc(translateText('Cell-center point samples'))}</span>`:''}`;
   get('reference-convention').textContent=c.dimension===2?'Taylor–Green: x-slice at y = π/4. These are point values, not two-dimensional cell averages.':c.field_type==='conserved'?'Cell means of conserved variables, integrated across known wave fronts. Primitive variables of averaged states are not averages of primitive variables.':'Cell means of the displayed scalar or velocity profile, integrated across known fronts.';
   get('reference-assumptions').textContent=c.assumptions;
   get('reference-parameters').textContent=Object.keys(c.parameters).length?JSON.stringify(c.parameters,null,2):'';
   get('reference-sources').innerHTML=c.sources.map((url,i)=>`<p><a class="text-link" href="${esc(url)}" target="_blank" rel="noopener">${esc(translateText('Original source'))} ${i+1} ↗</a></p>`).join('');
   const d=c.diagnostics;
   get('reference-metrics').innerHTML=(g?metric('Quadrature orders','24 / 48')+metric('Maximum order difference',fmt(g.max_order_difference[j])):metric('Sampling','x; y = π/4'))+(d.iterations!==undefined?metric('Root iterations',d.iterations)+metric('Wave-matching residual',fmt(d.wave_residual))+metric('Logarithmic bracket width',fmt(d.log_bracket_width)):'');
  };
  select.addEventListener('change',update);component.addEventListener('change',update);slider.addEventListener('input',update);grid.addEventListener('change',update);centers.addEventListener('change',update);update();
 }catch(e){if(root.isConnected)get('reference-summary').textContent='Reference data could not load. Reload to retry or read the reference guide.';console.error(e);}
}
