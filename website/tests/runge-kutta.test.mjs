import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {rkPage} from '../runge-kutta.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/runge-kutta.json'));
test('RK notebook ships reproducible complete tableaus, stage cases, and refinement',()=>{
 for(const [path,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read(`../../${path}`)).digest('hex'),hash);
 assert.equal(data.methods.length,9);assert.equal(data.cases.length,27);
 for(const m of data.methods){
  assert.equal(m.A.length,m.stages);assert.equal(m.b.length,m.stages);
  assert.ok(Math.abs(m.b.reduce((a,b)=>a+b,0)-1)<1e-13);
  for(let i=0;i<m.stages;i++)assert.ok(Math.abs(m.A[i].reduce((a,b)=>a+b,0)-m.c[i])<1e-13);
  for(const h of [.25,.5,1]){
   const c=data.cases.find(c=>c.method===m.id&&c.dt===h);assert.ok(c);
   assert.equal(c.stages.length,m.stages);assert.equal(c.exact,1/(1+h));
   assert.ok(Number.isFinite(c.result));
   for(const s of c.stages){assert.ok(Math.abs(s.rhs+s.value*s.value)<1e-13);assert.ok(Math.abs(s.time-m.c[s.stage-1]*h)<1e-13);}
   assert.ok(Math.abs(c.result-(1+h*c.stages.reduce((v,s,i)=>v+m.b[i]*s.rhs,0)))<1e-13);
  }
  const study=data.refinement.find(s=>s.method===m.id);assert.ok(study);
  assert.ok(study.orders.every(p=>p>m.order-.2));
  assert.deepEqual(study.rhs_calls,study.n.map(n=>n*m.stages));
  assert.ok(m.stability_boundary.length>0);
  assert.ok(m.stability_boundary.flat(2).every(Number.isFinite));
 }
 assert.match(rkPage(),/id="rk-method" disabled/);
 assert.match(rkPage(),/id="rk-step" disabled/);
});
test('RK2 equal linear factors do not collapse nonlinear methods or SSP metadata',()=>{
 const ids=['heun','explicit-midpoint','ralston'];
 for(const id of ids)assert.deepEqual(data.methods.find(m=>m.id===id).stability_polynomial,[1,1,.5]);
 assert.deepEqual(ids.map(id=>data.methods.find(m=>m.id===id).ssp_coefficient),[1,0,.5]);
 assert.equal(new Set(ids.map(id=>data.cases.find(c=>c.method===id&&c.dt===.5).result)).size,3);
 assert.equal(data.methods.find(m=>m.id==='rk4').ssp_coefficient,0);
 assert.equal(data.methods.find(m=>m.id==='ssprk43').order,3);
 assert.equal(data.methods.find(m=>m.id==='ssprk54').stages,5);
});
