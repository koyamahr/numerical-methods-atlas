import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {amplification,differenceStep,simulate,observedOrder,createExperiment} from '../numerics.js';
const reference=JSON.parse(fs.readFileSync(new URL('../content/advection-reference.json',import.meta.url)));
function close(a,b,tolerance=2e-12){assert.ok(Math.abs(a-b)<=tolerance*Math.max(1,Math.abs(b)),`${a} != ${b}`);}

test('browser stencils and amplification factors agree with Python in 24 signed-CFL cases',()=>{
 for(const sample of reference.cases){
  let q=reference.initial.slice();
  for(let k=0;k<sample.steps;k++)q=differenceStep(q,sample.courant,sample.method);
  q.forEach((v,j)=>close(v,sample.expected[j]));
  reference.theta.forEach((theta,j)=>{
   const g=amplification(theta,sample.courant,sample.method);
   close(g.re,sample.amplification_real[j]);close(g.im,sample.amplification_imag[j]);
  });
 }
});
test('reference fixture identifies the checked-in Python implementation',()=>{
 const source=fs.readFileSync(new URL('../../numart/advection.py',import.meta.url));
 assert.equal(createHash('sha256').update(source).digest('hex'),reference.source_sha256);
});
test('unit signed CFL shifts periodic samples exactly for upwind, LF, and LW',()=>{
 for(const method of ['upwind','lax-friedrichs','lax-wendroff'])for(const c of [-1,1]){
  const result=simulate({method,courant:c,steps:17,profile:'ripple'});
  result.values.forEach((v,j)=>close(v,result.exact[j]));
 }
});
test('CFL does not make FTCS stable, and exceeding CFL grows LW grid modes',()=>{
 assert.ok(simulate({method:'ftcs',courant:.8}).maxG>1.2);
 assert.ok(simulate({method:'lax-wendroff',courant:1.1}).maxG>1.4);
 assert.ok(simulate({method:'lax-wendroff',courant:.8}).maxG<=1+1e-12);
});
test('smooth exact translations and discontinuity wrapping respect periodicity',()=>{
 for(const c of [-.8,.8])close(simulate({courant:c,steps:0}).l1,0);
 const result=simulate({method:'upwind',courant:1,steps:64,profile:'square'});
 result.values.forEach((v,j)=>close(v,result.initial[j]));
});
test('observed order uses the grid ratio rather than a hard-coded slope',()=>{
 close(observedOrder(.08,.01),3);close(observedOrder(.81,.01,3),4);
 assert.throws(()=>observedOrder(0,.1));
});
test('invalid numerical controls fail explicitly',()=>{
 assert.throws(()=>simulate({n:31}));assert.throws(()=>simulate({steps:101}));
 assert.throws(()=>differenceStep([1,2,3],.8,'unknown'));
});

test('download snapshots preserve selected settings, provenance, and complete finite arrays',()=>{
 const settings={method:'ftcs',courant:-.8,steps:40,n:64,profile:'ripple'};
 const snapshot=JSON.parse(JSON.stringify(createExperiment(settings,reference.source_sha256)));
 assert.deepEqual(snapshot.settings,settings);
 assert.equal(snapshot.python_reference_sha256,reference.source_sha256);
 assert.equal(snapshot.computed_in,'Browser JavaScript');
 for(const key of ['x','initial','values','exact']){
  assert.equal(snapshot[key].length,64);assert.ok(snapshot[key].every(Number.isFinite));
 }
 assert.ok(snapshot.maxG>1);assert.ok(snapshot.amplitude>1);
});
