/** Periodic linear advection, matching numart.advection. No DOM dependencies. */
export const METHODS = {
  upwind: {label:'Upwind',order:1,description:'A direction-aware first-order stencil. Within |C| ≤ 1 it damps high-frequency errors, but also smooths the physical wave.'},
  'lax-friedrichs': {label:'Lax–Friedrichs',order:1,description:'Neighbor averaging adds numerical diffusion. This classical fully discrete LF scheme is distinct from the local Rusanov flux used in the Sod comparison.'},
  'lax-wendroff': {label:'Lax–Wendroff',order:2,description:'Second-order accuracy for smooth solutions reduces diffusion. Dispersion and oscillations near a discontinuity remain possible even within |C| ≤ 1.'},
  ftcs: {label:'FTCS',order:1,description:'Forward Euler in time and centered differences in space. Some Fourier modes grow for every nonzero C, even when the domain-of-dependence CFL condition is satisfied.'}
};
export function amplification(theta,c,method) {
  if(!METHODS[method]) throw new RangeError('Unknown difference method');
  const cosine=Math.cos(theta),sine=Math.sin(theta);
  let re=1;
  if(method==='upwind')re=1-Math.abs(c)*(1-cosine);
  if(method==='lax-friedrichs')re=cosine;
  if(method==='lax-wendroff')re=1+c*c*(cosine-1);
  const im=-c*sine;
  return {re,im,magnitude:Math.hypot(re,im)};
}
export function differenceStep(q,c,method) {
  if(!METHODS[method]) throw new RangeError('Unknown difference method');
  const n=q.length;
  return Array.from(q,(center,j)=>{
    const left=q[(j+n-1)%n],right=q[(j+1)%n];
    if(method==='ftcs')return center-.5*c*(right-left);
    if(method==='upwind')return c>=0?center-c*(center-left):center-c*(right-center);
    if(method==='lax-friedrichs')return .5*(right+left)-.5*c*(right-left);
    return center-.5*c*(right-left)+.5*c*c*(right-2*center+left);
  });
}
export function profileAt(x,n,profile='ripple') {
  const z=((x%1)+1)%1;
  if(profile==='square')return z>=.25&&z<.65?1:0;
  const smooth=Math.sin(2*Math.PI*z);
  if(profile==='sine')return smooth;
  if(profile!=='ripple')throw new RangeError('Unknown initial profile');
  return smooth+.001*(Math.sin(2*Math.PI*(n/2)*z)+Math.cos(2*Math.PI*(n/4)*z));
}
export function simulate({method='lax-wendroff',courant=.8,steps=40,n=64,profile='ripple'}={}) {
  if(!Number.isInteger(n)||n<4||n%4||!Number.isInteger(steps)||steps<0||steps>100||!Number.isFinite(courant)||Math.abs(courant)>1.5)throw new RangeError('Invalid lab parameters');
  const x=Array.from({length:n},(_,j)=>(j+.5)/n);
  const initial=x.map(z=>profileAt(z,n,profile));
  let values=initial.slice();
  for(let k=0;k<steps;k++)values=differenceStep(values,courant,method);
  const shift=courant*steps/n,exact=x.map(z=>profileAt(z-shift,n,profile));
  const modes=Array.from({length:n/2+1},(_,k)=>amplification(2*Math.PI*k/n,courant,method).magnitude);
  const maxG=Math.max(...modes);
  return {x,initial,values,exact,modes,maxG,time:Math.abs(courant)*steps/n,
    l1:values.reduce((s,v,j)=>s+Math.abs(v-exact[j]),0)/n,
    amplitude:Math.max(...values.map(Math.abs)),
    meanDrift:values.reduce((s,v,j)=>s+v-initial[j],0)/n};
}
export function observedOrder(coarse,fine,ratio=2) {
  if(!(coarse>0&&fine>0&&ratio>1))throw new RangeError('Positive errors and refinement ratio > 1 required');
  return Math.log(coarse/fine)/Math.log(ratio);
}

export function createExperiment(settings,referenceHash) {
  return {schema_version:1,model:'Periodic constant-coefficient scalar advection',
    computed_in:'Browser JavaScript',settings:{...settings},
    python_reference_sha256:referenceHash,...simulate(settings)};
}
