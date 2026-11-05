import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {equationsPage} from '../equations.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/equation-gallery.json'));
const foundations=JSON.parse(read('../public/assets/solver-foundations.json'));
test('equation and solver manifests match their numerical sources',()=>{
 for(const manifest of [data,foundations])for(const [p,hash] of Object.entries(manifest.source_sha256))
  assert.equal(createHash('sha256').update(read('../../'+p)).digest('hex'),hash,p);
});
test('gallery profiles retain increasing actual times and reference conventions',()=>{
 assert.equal(data.cases.length,9);
 const refs=JSON.parse(read('../content/references.json'));
 for(const c of data.cases){
  assert.ok(refs.some(r=>r.id===c.reference),c.reference);
  assert.equal(c.frames[0].time,0);assert.ok(c.frames.length>=25);
  for(const [i,f] of c.frames.entries()){
   if(i)assert.ok(f.time>c.frames[i-1].time);
   assert.equal(f.u.length,c.n);assert.ok(f.u.every(Number.isFinite));
   if(f.exact){assert.equal(f.exact.length,c.n);assert.ok(f.exact.every(Number.isFinite));
    const error=f.u.reduce((s,v,j)=>s+Math.abs(v-f.exact[j]),0)/c.n;
    assert.ok(Math.abs(error-f.l1)<1e-13);
   }else assert.equal(f.l1,null);
   if(c.boundary.startsWith('Periodic'))assert.ok(Math.abs(f.mean_change)<1e-12);
  }
 }
 for(const name of ['dam-break','isothermal'])assert.ok(data.cases.find(c=>c.id===name).frames.every(f=>f.exact===null));
 assert.match(data.cases.find(c=>c.id==='sod').sampling,/independent solve/);
 assert.match(equationsPage(),/href="#\/read\/chapman-enskog"/);
 assert.match(equationsPage(),/id="equation-case" disabled/);
});
test('reported refinements distinguish scheme order from convergence of iteration',()=>{
 const order=errors=>Math.log2(errors.at(-2)/errors.at(-1));
 assert.ok(order(foundations.fem.l2)>1.95);assert.ok(order(foundations.fem.h1)>.98);
 assert.ok(order(foundations.mac.velocity_rms)>1.95);
 assert.ok(order(foundations.lbm.channel_relative_l2)>1.95);
 assert.ok(foundations.mac.max_divergence.every(x=>x<1e-12));
 assert.ok(order(foundations.hyperbolic_diffusion.l2)>.9);
 assert.match(foundations.hyperbolic_diffusion.scope,/first-order/);
});
