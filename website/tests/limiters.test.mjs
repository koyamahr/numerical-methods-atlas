import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {limiterPage} from '../limiters.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/limiters.json'));
test('limiter controls cover sourced computed cases and preserve scalar conservation',()=>{
 for(const [path,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read(`../../${path}`)).digest('hex'),hash);
 assert.equal(data.cases.length,45);
 for(const profile of ['square','sine'])for(const speed of [-1,1])for(const method of data.methods)for(const M of method.id==='tvb'?[0,10,50]:[0]){
  const c=data.cases.find(c=>c.profile===profile&&c.speed===speed&&c.method===method.id&&c.M===M);
  assert.ok(c,`${profile}, ${speed}, ${method.id}, M=${M}`);
  assert.equal(c.x.length,200);assert.equal(c.q.length,200);assert.equal(c.exact.length,200);
  assert.ok([...c.q,...c.exact,c.error_l1,c.max_tv].every(Number.isFinite));
  assert.ok(Math.abs(c.mass_change)<1e-12);
  if(data.methods.slice(0,5).some(m=>m.id===method.id)){
   assert.ok(c.max_tv<=c.initial_tv+1e-11);
   if(profile==='square')assert.ok(c.minimum>=-1e-12&&c.maximum<=1+1e-12);
  }
 }
 for(const method of data.methods.slice(0,5)){
  const c=data.cases.find(c=>c.profile==='sod'&&c.method===method.id);
  assert.ok(c.minimum>0&&c.min_pressure>0);assert.equal(c.time,.2);
 }
 assert.match(limiterPage(),/id="lim-profile" disabled/);
 assert.match(limiterPage(),/id="pos-case" disabled/);
});
test('published scaling states obey both floors and retain the conservative quadrature mean',()=>{
 for(const c of data.scaling){
  assert.ok(c.theta>0&&c.theta<1);
  assert.ok(c.limited.every(q=>q[0]>=c.floor*(1-1e-6)));
  assert.ok(c.limited_pressure.every(p=>p>=c.floor*(1-1e-6)));
  for(let k=0;k<3;k++)assert.ok(Math.abs(c.limited.reduce((sum,u,i)=>sum+c.weights[i]*u[k],0)-c.mean[k])<1e-14);
 }
 assert.equal(data.refinement.length,6);
 for(const s of data.refinement)assert.ok(s.error_l1[2]<s.error_l1[1]&&s.error_l1[1]<s.error_l1[0]);
});
