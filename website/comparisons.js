import {translateText as tr} from './i18n.js';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>Number.isFinite(v)?(Math.abs(v)<.001&&v!==0?v.toExponential(3):v.toPrecision(6)):'—';
let flowData,mhdData,cleanup=()=>{};
export function disposeComparisons(){cleanup();cleanup=()=>{};}
const load=path=>fetch(path).then(r=>{if(!r.ok)throw Error('Comparison data unavailable');return r.json();});
const table=(headers,rows)=>`<div class="measurement-scroll"><table class="measurement-table"><thead><tr>${headers.map(h=>`<th scope="col">${esc(tr(h))}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(v=>`<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;

export function flowPage(){return `<section class="page-intro page-width"><p class="eyebrow">EULER / RECONSTRUCTION COMPARISON</p><h1>Compare the reconstruction.</h1><p>First order, minmod or MC on shared grids. Keep the HLL flux and SSPRK2 fixed, then inspect the shock, wall pressure and smooth-wave refinement.</p></section><section id="flow-comparison" class="laboratory page-width"><aside class="lab-controls"><label for="flow-case">Flow test</label><select id="flow-case" disabled></select><label for="flow-method">Compare with first order</label><select id="flow-method"><option value="mc">MUSCL / MC</option><option value="minmod">MUSCL / minmod</option></select><p id="flow-settings" class="lab-settings"></p><a class="text-link" href="#/read/nasa-2d">Setup, references & boundary conditions ↗</a><a class="text-link" href="assets/comparisons/euler-comparison.json" download>Download comparison diagnostics ↓</a><a class="text-link" href="assets/comparisons/final-fields.npz" download>Download computed field arrays ↓</a><a class="text-link" href="#/gallery">Return to the gallery ↗</a></aside><div class="lab-results"><div id="flow-summary" class="lab-summary" aria-live="polite">Loading comparison data…</div><div class="comparison-grid"><figure class="lab-chart-card"><h2>First order</h2><a id="flow-baseline-open" target="_blank" rel="noopener"><img id="flow-baseline" class="comparison-image" alt="First-order computed field"></a></figure><figure class="lab-chart-card"><h2 id="flow-selected-title"></h2><a id="flow-selected-open" target="_blank" rel="noopener"><img id="flow-selected" class="comparison-image" alt="Selected reconstruction computed field"></a></figure></div><div id="flow-measurements"></div><section id="flow-movies" hidden><h2>Watch the shock reflections</h2><p>Both clips use the same requested output times and playback rate. Intermediate physical timestamps can differ by one solver step; read the time printed in each frame.</p><div class="equation-playback"><button id="flow-play" class="button primary">Play both ▷</button><button id="flow-pause" class="button">Pause both</button><button id="flow-reset" class="button">Reset both</button></div><div class="comparison-grid"><figure><figcaption>First order</figcaption><video id="flow-video-first" controls muted playsinline preload="none"></video></figure><figure><figcaption id="flow-video-label"></figcaption><video id="flow-video-selected" controls muted playsinline preload="none"></video></figure></div></section></div></section><section class="page-width section"><h2>Smooth accuracy is a separate test.</h2><p>Periodic 2D entropy advection compares exact density cell averages. A sharp shock image does not establish second-order convergence.</p><img class="comparison-refinement" src="assets/comparisons/smooth-refinement.png" alt="Two-dimensional smooth entropy-wave refinement"><div id="flow-smooth-orders"></div><p class="scope-note">Same grid and nominal CFL do not mean equal step counts or equal computational cost. Reconstructed face states may be scaled for positivity; failed steps are retried and counted. Cell averages are never clipped. The step corner has no entropy reset.</p></section>`;}

export async function wireFlow(requestedCase,requestedMethod){
 const root=document.getElementById('flow-comparison');
 try{
  flowData??=load('assets/comparisons/euler-comparison.json');const data=await flowData;if(!root.isConnected)return;
  const get=id=>document.getElementById(id),videos=[get('flow-video-first'),get('flow-video-selected')];
  const pause=()=>videos.forEach(v=>v.pause());cleanup=pause;
  get('flow-case').innerHTML=data.cases.map(c=>`<option value="${esc(c.id)}">${esc(tr(c.title))}</option>`).join('');get('flow-case').disabled=false;
  get('flow-case').value=data.cases.some(c=>c.id===requestedCase)?requestedCase:'wedge-m2.5';
  get('flow-method').value=['mc','minmod'].includes(requestedMethod)?requestedMethod:'mc';
  function render(){
   pause();const c=data.cases.find(c=>c.id===get('flow-case').value);
   const baseline=c.methods.find(m=>m.id==='first'),chosen=c.methods.find(m=>m.id===get('flow-method').value);
   history.replaceState(null,'',`#/flow-comparison?case=${encodeURIComponent(c.id)}&method=${chosen.id}`);
   get('flow-selected-title').textContent=tr(chosen.label);get('flow-summary').textContent=tr(c.title);
   get('flow-settings').textContent=`${c.shape.join(' × ')} · HLL / SSPRK2 · CFL ${data.cfl} · t = ${c.final_time}`;
   for(const [id,m] of [['baseline',baseline],['selected',chosen]]){
    get('flow-'+id).src='assets/comparisons/'+m.image;get('flow-'+id+'-open').href='assets/comparisons/'+m.image;
   }
   let rows;
   if(c.kind==='wedge'){
    rows=[['Wall pressure ratio',baseline.metrics.wall_pressure_ratio_median,chosen.metrics.wall_pressure_ratio_median,chosen.metrics.pressure_ratio_exact],
          ['Fitted shock angle (degrees)',baseline.metrics.beta_gradient_fit_degrees,chosen.metrics.beta_gradient_fit_degrees,chosen.metrics.beta_exact_degrees],
          ['Density cell-average L1',baseline.metrics.density_cell_average_l1,chosen.metrics.density_cell_average_l1,null],
          ['Final max conserved update rate',baseline.metrics.final_maximum_conserved_update_rate,chosen.metrics.final_maximum_conserved_update_rate,null]];
    get('flow-measurements').innerHTML=table(['Diagnostic','First order',chosen.label,'Analytical reference'],rows.map(row=>[tr(row[0]),...row.slice(1).map(num)]))+
      (c.id==='wedge-m2'&&chosen.id==='mc'?`<p class="scope-note">${tr('Mach-2 MC retains local time variation at t = 3; this is not a converged steady solution.')}</p>`:'')+`<h3>${tr('Two-grid density errors')}</h3>`+table(['Grid','First order',chosen.label],baseline.refinement.map((m,i)=>[m.shape.join(' × '),num(m.density_cell_average_l1),num(chosen.refinement[i].density_cell_average_l1)]));
   }else{
    rows=['min_density','min_pressure','steps','retried_steps','positivity_scaled_cells'].map((key,i)=>[tr(['Minimum density','Minimum pressure','Solver steps','Retried steps','Face positivity scaling events'][i]),num(baseline.metrics[key]),num(chosen.metrics[key])]);
    get('flow-measurements').innerHTML=table(['Diagnostic','First order',chosen.label],rows);
   }
   get('flow-movies').hidden=c.kind!=='step';
   if(c.kind==='step'){
    for(const [video,m] of [[videos[0],baseline],[videos[1],chosen]]){video.src='assets/comparisons/'+m.video;video.poster='assets/comparisons/'+m.poster;video.load();}
    get('flow-video-label').textContent=tr(chosen.label);
   }else videos.forEach(v=>{v.removeAttribute('src');v.removeAttribute('poster');v.load();});
  }
  get('flow-case').addEventListener('change',render);get('flow-method').addEventListener('change',render);
  get('flow-play').addEventListener('click',()=>Promise.all(videos.map(v=>v.play())).catch(()=>{pause();}));
  get('flow-pause').addEventListener('click',pause);get('flow-reset').addEventListener('click',()=>{pause();videos.forEach(v=>v.currentTime=0);});
  get('flow-smooth-orders').innerHTML=table(['Reconstruction','Fine-grid observed order'],data.smooth.series.map(s=>[tr(s.label),num(s.orders.at(-1))]));render();
 }catch(e){if(root.isConnected)document.getElementById('flow-summary').textContent=tr('Comparison data could not load. Reload the page.');console.error(e);}
}

export function mhdPage(){return `<section class="page-intro page-width"><p class="eyebrow">HLLD / STANDARD MHD TESTS</p><h1>Resolve the magnetic waves.</h1><p>Inspect Brio–Wu, a circularly polarized Alfvén wave and a weak magnetic field loop. Separate Riemann fluxes, reconstruction and magnetic-divergence control.</p></section><section class="laboratory page-width" id="mhd-tests"><aside class="lab-controls"><label for="mhd-case">MHD test</label><select id="mhd-case"><option value="field-loop">Magnetic field loop</option><option value="brio-wu">Brio–Wu shock tube</option><option value="alfven">Circular Alfvén wave</option></select><p>MC reconstruction / SSPRK2</p><a class="text-link" href="#/read/mhd">Read the MHD definitions ↗</a><a class="text-link" href="assets/mhd-tests/mhd-tests.json" download>Download MHD diagnostics ↓</a><a class="text-link" href="assets/mhd-tests/fields.npz" download>Download computed field arrays ↓</a><a class="text-link" href="#/gallery">Return to the gallery ↗</a></aside><div class="lab-results"><div class="lab-summary" id="mhd-summary" aria-live="polite">Loading comparison data…</div><a id="mhd-open" target="_blank" rel="noopener"><img id="mhd-image" class="comparison-image" alt="Computed MHD test and comparison"></a><div id="mhd-measurements"></div><img id="mhd-diagnostics" class="comparison-image" alt="Magnetic energy and native divergence histories" hidden><p id="mhd-scope" class="scope-note"></p></div></section><aside class="callout page-width"><h2>CT and GLM need their own diagnostics.</h2><p>CT uses a face-field divergence and a contact-upwinded corner electric field. GLM uses cell-centered fields, a longitudinal cleaning-wave solve and split damping. Their initial discretizations and divergence operators differ. HLLD star-state failures fall back to HLLE and are counted.</p></aside>`;}

export async function wireMHD(requestedCase){
 const root=document.getElementById('mhd-tests');
 try{
  mhdData??=load('assets/mhd-tests/mhd-tests.json');const data=await mhdData;if(!root.isConnected)return;
  const get=id=>document.getElementById(id);get('mhd-case').value=['brio-wu','alfven','field-loop'].includes(requestedCase)?requestedCase:'field-loop';
  function render(){
   const id=get('mhd-case').value,item=data[{'brio-wu':'brio_wu','alfven':'alfven','field-loop':'field_loop'}[id]];
   history.replaceState(null,'',`#/mhd-tests?case=${id}`);get('mhd-summary').textContent=tr({'brio-wu':'Brio–Wu shock tube',alfven:'Circular Alfvén wave','field-loop':'Magnetic field loop'}[id]);
   get('mhd-image').src='assets/mhd-tests/'+item.image;get('mhd-open').href=get('mhd-image').src;
   get('mhd-diagnostics').hidden=!item.diagnostics_image;if(item.diagnostics_image)get('mhd-diagnostics').src='assets/mhd-tests/'+item.diagnostics_image;
   if(id==='field-loop')get('mhd-measurements').innerHTML=table(['Method','Magnetic energy fraction','Native max divergence','HLLE fallback faces'],item.modes.map(m=>[m.id.toUpperCase(),num(m.metrics.magnetic_energy_fraction),num(m.metrics.native_max_divergence),String(m.metrics.hlle_fallback_faces)]));
   else if(id==='brio-wu')get('mhd-measurements').innerHTML=table(['Method','Grid','Minimum density','Minimum pressure','HLLE fallback faces'],item.runs.map(r=>[r.solver.toUpperCase(),String(r.n),num(r.min_density),num(r.min_pressure),String(r.hlle_fallback_faces)]));
   else get('mhd-measurements').innerHTML=table(['Method','Fine-grid error','Fine-grid observed order'],item.series.map(s=>[s.solver.toUpperCase(),num(s.l1_transverse_b.at(-1)),num(s.orders.at(-1))]));
   get('mhd-scope').textContent=tr(item.scope);
  }
  get('mhd-case').addEventListener('change',render);render();
 }catch(e){if(root.isConnected)document.getElementById('mhd-summary').textContent=tr('Comparison data could not load. Reload the page.');console.error(e);}
}
