import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {cipPage} from '../cip.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/cip.json'));
test('CIP controls have sourced point-value and independently evolved derivative cases',()=>{
 for(const [path,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read(`../../${path}`)).digest('hex'),hash);
 assert.equal(data.cases.length,48);
 for(const profile of ['sine','square'])for(const speed of [-1,1])for(const cfl of [.25,.6,1])for(const time of [.25,1])for(const gradient of ['analytic','centered']){
  const c=data.cases.find(c=>c.profile===profile&&c.speed===speed&&c.cfl===cfl&&c.time===time&&c.gradient===gradient);
  assert.ok(c);assert.equal(c.n,128);
  for(const key of ['x','cip','linear','exact','cip_gradient']){assert.equal(c[key].length,128);assert.ok(c[key].every(Number.isFinite));}
  if(cfl===1)assert.ok(c.cip_l1<1e-13);
  if(profile==='square')assert.equal(c.exact_gradient,null);else assert.equal(c.exact_gradient.length,128);
 }
 assert.match(cipPage(),/id="cip-profile" disabled/);
});
test('CIP exhibits report refinement and the analytic mass counterexample honestly',()=>{
 assert.equal(data.refinement.length,3);
 for(const s of data.refinement)assert.ok(s.orders.every(p=>p>(s.method==='cip'?2.7:.8)));
 const c=data.counterexample;
 assert.ok(Math.abs(c.mass_after-c.mass_before)>1e-3);
 assert.ok(Math.abs(c.mass_after-c.mass_before-c.analytic_mass_change)<1e-14);
 assert.equal(c.mass_before,1);
 assert.equal(c.x.length,c.exact_shifted.length);assert.equal(c.x.length,c.remapped.length);
 const square=data.cases.find(c=>c.profile==='square'&&c.gradient==='centered'&&c.cfl===.6&&c.time===.25&&c.speed===1);
 assert.ok(square.minimum<0&&square.maximum>1);
});
