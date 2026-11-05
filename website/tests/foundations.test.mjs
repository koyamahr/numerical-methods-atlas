import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/foundations.json'));
test('published temporal and mesh data identify current Python sources and cover the notebook controls',()=>{
 for(const [name,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read(`../../numart/${name}`)).digest('hex'),hash);
 const methods=['forward-euler','backward-euler','heun','ssprk3','rk4','midpoint','leapfrog'];
 for(const method of methods)for(const dt of [.05,.1,.2,.5,1,1.25,2])for(const epsilon of method==='leapfrog'?[0,.01,.03]:[0]){
  const c=data.time.find(c=>c.method===method&&c.dt===dt&&c.epsilon===epsilon);
  assert.ok(c,`${method}, dt=${dt}, epsilon=${epsilon}`);
  assert.equal(c.t.at(-1),20);assert.equal(c.real.length,c.t.length);assert.equal(c.imag.length,c.t.length);
  assert.ok([...c.t,...c.real,...c.imag,c.max_error,c.final_amplitude].every(Number.isFinite));
 }
 assert.deepEqual(Object.keys(data.meshes).sort(),['structured','triangular','unstructured']);
 for(const m of Object.values(data.meshes))assert.ok(Math.abs(m.areas.reduce((a,b)=>a+b,0)-1)<1e-12);
});

test('Hamiltonian and gravity exhibits retain source provenance and complete notebook cases',()=>{
 for(const file of ['hamiltonian','particle-gravity','gravity-boundaries']){
  const exhibit=JSON.parse(read(`../public/assets/${file}.json`));
  for(const [name,hash] of Object.entries(exhibit.source_sha256))assert.equal(createHash('sha256').update(read(`../../numart/${name}`)).digest('hex'),hash);
 }
 const maps=JSON.parse(read('../content/hamiltonian.json'));
 assert.equal(maps.cases.length,30);
 for(const method of maps.methods)for(const system of ['harmonic','quartic'])for(const h of [.1,.2,.4]){
  const c=maps.cases.find(c=>c.method===method.id&&c.system===system&&c.h===h);
  assert.ok(c);assert.equal(c.t.at(-1),200);assert.equal(c.steps,Math.round(200/h));
  assert.equal(c.q.length,c.t.length);assert.equal(c.p.length,c.t.length);
  assert.ok(c.relative_energy_error.every(e=>Number.isFinite(e)&&Math.abs(e)<=c.max_relative_energy_error*(1+1e-12)+1e-15));
 }
});
