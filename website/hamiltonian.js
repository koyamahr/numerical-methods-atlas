import {chart,notebookNav} from './experiments.js';
const labels={'symplectic-euler':'Symplectic Euler',verlet:'Störmer–Verlet / Leapfrog',yoshida4:'Yoshida fourth order',midpoint:'Implicit midpoint',rk4:'Classical RK4'};
const explanations={
 'symplectic-euler':'A first-order kick–drift canonical map. It preserves the two-form, but is not time symmetric and generally changes the original Hamiltonian.',
 verlet:'A second-order symmetric kick–drift–kick map. Small fixed steps give bounded, oscillatory energy errors in these examples; the original Hamiltonian is not exactly preserved.',
 yoshida4:'Three Verlet steps with coefficients a, b, a produce a fourth-order symmetric symplectic map. The middle coefficient is negative. Higher order does not imply unconditional stability.',
 midpoint:'An implicit second-order symmetric symplectic map. It preserves this harmonic oscillator’s quadratic energy to roundoff, but need not conserve the nonlinear quartic Hamiltonian exactly.',
 rk4:'A fourth-order accuracy comparison. Classical RK4 is generally not symplectic or time symmetric. The local canonical defect and the long-time energy trace measure different properties.'
};
let dataset;
export function hamiltonianPage(){return `<section class="page-intro page-width">${notebookNav('hamiltonian')}<p class="eyebrow">CANONICAL MAPS · FIXED TIME STEPS</p><h1>Preserve the structure.<br>Inspect the <em>energy.</em></h1><p>Compare five integrators on harmonic and nonlinear Hamiltonians. A symplectic map preserves the canonical two-form; exact conservation of the original energy is a separate property.</p></section>
<section class="page-width laboratory" id="ham-notebook"><aside class="lab-controls"><label for="ham-system">Hamiltonian</label><select id="ham-system"><option value="harmonic">H = (p² + q²) / 2</option><option value="quartic">H = (p² + q²) / 2 + q⁴ / 4</option></select><label for="ham-step">Fixed step h</label><select id="ham-step"><option value="0.1">0.1</option><option value="0.2" selected>0.2</option><option value="0.4">0.4</option></select><label for="ham-method">Inspect a map</label><select id="ham-method">${Object.entries(labels).map(([id,label])=>`<option value="${id}" ${id==='verlet'?'selected':''}>${label}</option>`).join('')}</select><label for="ham-view">Phase-space view</label><select id="ham-view"><option value="patch">One-step map of a small square</option><option value="orbit">Orbit over the first 10 time units</option></select><p class="lab-settings">q₀ = 1 · p₀ = 0.2<br>Energy history: T = 200<br>Mass = 1 · fixed h<br>Map patch center: (0.7, 0.4)</p><a class="text-link" href="#/read/symplectic">Maps, equations & assumptions ↗</a><a class="text-link" href="hamiltonian.json" download>Download computed cases ↓</a></aside><div class="lab-results"><div id="ham-summary" class="lab-summary" aria-live="polite">Loading computed maps…</div><div class="lab-chart-card"><div class="lab-chart-header"><h2>The original Hamiltonian</h2><span>ALL FIVE METHODS · SAME h AND T</span></div><div id="ham-energy"></div><div id="ham-legend" class="lab-legend"></div><p class="lab-chart-note">Relative error (Hₙ − H₀) / H₀, with zero marked by a dashed line. The scale is shared across methods. Displayed samples are reduced; maximum errors use every step.</p></div><div class="lab-lower"><div class="lab-chart-card"><div class="lab-chart-header"><h2 id="ham-phase-title">A map in phase space</h2></div><div id="ham-phase"></div><p id="ham-phase-note" class="lab-chart-note"></p></div><aside class="lab-explanation"><p class="eyebrow">THE GEOMETRIC QUESTION</p><h2 id="ham-method-name"></h2><p id="ham-explanation"></p><dl id="ham-metrics"></dl></aside></div></div></section><aside class="callout page-width"><h2>Area, energy, and time reversal are different tests.</h2><p>The local matrix defect is ‖MᵀJM − J‖, evaluated from an analytic Jacobian at the patch center. In one degree of freedom, determinant one characterizes a symplectic map. A sampled polygon illustrates its deformation; it is not the exact curved image’s area integral. No particle gravity or adaptive stepping is applied in this experiment.</p><a class="text-link" href="#/read/particle-gravity">Continue to PM, Tree, and Poisson solvers ↗</a></aside>`;}
export async function wireHamiltonian(){
 const root=document.getElementById('ham-notebook');
 try{
  dataset??=fetch('hamiltonian.json').then(r=>{if(!r.ok)throw Error('Cannot load map data');return r.json();});
  const data=await dataset;if(!root.isConnected)return;
  const get=id=>root.querySelector(`#${id}`),number=v=>Math.abs(v)<.001?v.toExponential(3):v.toFixed(5);
  const update=()=>{
   const system=get('ham-system').value,h=Number(get('ham-step').value),method=get('ham-method').value,view=get('ham-view').value;
   const cases=data.cases.filter(c=>c.system===system&&c.h===h),c=cases.find(c=>c.method===method),meta=data.methods.find(m=>m.id===method);
   get('ham-summary').innerHTML=`<span>${system==='harmonic'?'Quadratic oscillator':'Nonlinear quartic oscillator'}</span><span>${c.steps} steps · h = ${h}</span><span>${meta.symplectic?'Symplectic method':'RK4 comparison'} · order ${meta.order}</span>`;
   const scale=Math.max(1e-12,...cases.map(v=>v.max_relative_energy_error))*1.08;
   get('ham-energy').innerHTML=chart({series:cases.map(c=>({points:c.t.map((t,i)=>[t,c.relative_energy_error[i]]),color:data.methods.find(m=>m.id===c.method).color})),xMax:200,xTicks:[0,50,100,150,200],yMin:-scale,yMax:scale,yTicks:[-scale,0,scale],yLabel:'RELATIVE ENERGY ERROR',xLabel:'TIME t',title:`${system} energy errors, fixed step ${h}`,reference:0});
   get('ham-legend').innerHTML=data.methods.map(m=>`<span style="--swatch:${m.color}">${m.label}</span>`).join('');
   let series,scope;
   if(view==='patch'){
    series=[{points:data.patch,color:'#65796c',dashed:true},{points:c.mapped_patch,color:meta.color}];scope=series.flatMap(s=>s.points);
    get('ham-phase-title').textContent='One step, one canonical map';
    get('ham-phase-note').textContent='Dashed: initial square. Solid: mapped boundary samples. The tangent matrix is evaluated at (q,p) = (0.7,0.4), independently of the energy trajectory’s initial state.';
   }else{
    const alpha=system==='quartic'?1:0,e=c.initial_energy,qmax=Math.sqrt(alpha?(-1+Math.sqrt(1+4*alpha*e))/alpha:2*e);
    const q=Array.from({length:201},(_,i)=>-qmax+2*qmax*i/200),positive=q.map(x=>[x,Math.sqrt(Math.max(0,2*(e-x*x/2-alpha*x**4/4)))]);
    const contour=[...positive,...positive.toReversed().map(([q,p])=>[q,-p])];
    series=[{points:contour,color:'#65796c',dashed:true},{points:c.t.flatMap((t,i)=>t<=10?[[c.q[i],c.p[i]]]:[]),color:meta.color,dots:true}];scope=series.flatMap(s=>s.points);
    get('ham-phase-title').textContent='The phase-space orbit';get('ham-phase-note').textContent='Dashed: the exact initial-energy contour. Solid/dots: computed trajectory samples for t ≤ 10. An accurate contour alone does not establish accurate orbital phase.';
   }
   const xs=scope.map(p=>p[0]),ys=scope.map(p=>p[1]),side=Math.max(Math.max(...xs)-Math.min(...xs),Math.max(...ys)-Math.min(...ys))*1.15,cx=(Math.max(...xs)+Math.min(...xs))/2,cy=(Math.max(...ys)+Math.min(...ys))/2;
   get('ham-phase').innerHTML=chart({series,square:true,xMin:cx-side/2,xMax:cx+side/2,yMin:cy-side/2,yMax:cy+side/2,xTicks:[cx-side/2,cx,cx+side/2],yTicks:[cy-side/2,cy,cy+side/2],xLabel:'POSITION q',yLabel:'MOMENTUM p',title:`${meta.label}, ${view} view, ${system}`});
   get('ham-method-name').textContent=meta.label;get('ham-explanation').textContent=explanations[method];
   get('ham-metrics').innerHTML=`<div><dt>Max |ΔH / H₀|, all steps</dt><dd>${number(c.max_relative_energy_error)}</dd></div><div><dt>Final ΔH / H₀</dt><dd>${number(c.final_relative_energy_error)}</dd></div><div><dt>Local det(M)</dt><dd>${c.det_jacobian.toFixed(10)}</dd></div><div><dt>Local ‖MᵀJM − J‖</dt><dd>${c.symplectic_defect.toExponential(3)}</dd></div>`;
  };
  ['ham-system','ham-step','ham-method','ham-view'].forEach(id=>get(id).addEventListener('change',update));update();
 }catch(error){if(root.isConnected)root.querySelector('#ham-summary').textContent='The map data could not load. Reload the page or read the chapter.';console.error(error);}
}
