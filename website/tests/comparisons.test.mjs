import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {configureLocale,translateText} from '../i18n.js';
import {flowPage,mhdPage} from '../comparisons.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');
const json=p=>JSON.parse(read(p));
for(const [folder,name] of [['comparisons','euler-comparison'],['mhd-tests','mhd-tests']]){
 test(name+' source and downloadable artifacts match the computed manifest',()=>{
  const data=json(`../public/assets/${folder}/${name}.json`);
  for(const [path,expected] of Object.entries(data.source_sha256))assert.equal(hash(read('../../'+path)),expected,path);
  for(const [path,expected] of Object.entries(data.artifact_sha256))assert.equal(hash(read(`../public/assets/${folder}/`+path)),expected,path);
 });
}
test('Euler methods share the grids; smooth convergence is separate from shock diagnostics',()=>{
 const data=json('../public/assets/comparisons/euler-comparison.json');
 assert.equal(data.cases.length,3);assert.equal(data.cfl,.4);
 const mc=data.smooth.series.find(s=>s.id==='mc');assert.deepEqual(mc.n,[16,32,64,128]);assert.ok(mc.orders.at(-1)>1.8);
 for(const c of data.cases){
  assert.deepEqual(c.methods.map(m=>m.id),['first','minmod','mc']);assert.deepEqual(c.shape,[240,80]);
  for(const m of c.methods)assert.ok(m.metrics.min_density>0&&m.metrics.min_pressure>0);
  if(c.kind==='wedge'){
   for(const m of c.methods){assert.equal(m.refinement.length,2);assert.ok(m.refinement[1].density_cell_average_l1<m.refinement[0].density_cell_average_l1);}
   assert.ok(c.methods[2].metrics.density_cell_average_l1<c.methods[0].metrics.density_cell_average_l1);
  }
 }
 // Do not silently turn the sharper Mach-2 MC shock into a steady-convergence claim.
 assert.ok(data.cases[0].methods[2].metrics.final_maximum_conserved_update_rate>1);
 assert.match(flowPage(),/Smooth accuracy is a separate test/);
});
test('step comparison clips retain all saved-state identities and the actual adaptive timestamps',()=>{
 const c=json('../public/assets/comparisons/euler-comparison.json').cases.find(c=>c.kind==='step');
 for(const m of c.methods){
  assert.equal(m.frames.length,81);assert.equal(m.frames[0].time,0);assert.equal(m.frames.at(-1).time,4);
  assert.equal(m.frames.at(-1).step,m.metrics.steps);assert.equal(m.fps,12);assert.deepEqual(m.pixels,[960,640]);
  for(const [i,f] of m.frames.entries()){
   assert.match(f.state_sha256,/^[a-f0-9]{64}$/);
   if(i){assert.ok(f.time>m.frames[i-1].time);assert.ok(f.step>m.frames[i-1].step);}
  }
 }
 assert.equal(c.scales.length,2);assert.match(flowPage(),/actual|physical timestamps/);
});
test('HLLD tests expose refinement and operator-specific loop diagnostics',()=>{
 const data=json('../public/assets/mhd-tests/mhd-tests.json');
 assert.equal(data.brio_wu.runs.length,3);assert.match(data.brio_wu.scope,/No exact solution/);
 for(const s of data.alfven.series){assert.deepEqual(s.n,[32,64,128,256]);assert.ok(s.orders.at(-1)>1.9);}
 assert.equal(data.field_loop.modes.length,4);
 for(const m of data.field_loop.modes){
  assert.equal(m.refinement.length,2);assert.equal(m.metrics.time,1);assert.deepEqual(m.metrics.shape,[128,64]);
  assert.ok(Math.abs(m.metrics.mean_mass_change)<1e-10);assert.ok(Math.abs(m.metrics.mean_total_energy_change)<1e-10);
  assert.ok(m.metrics.magnetic_energy_fraction>0&&m.metrics.magnetic_energy_fraction<1);
  assert.equal(m.metrics.hlle_fallback_faces,0);assert.equal(m.metrics.retried_steps,0);
  if(m.method==='ct')assert.ok(m.metrics.native_max_divergence<1e-12);
 }
 assert.match(data.field_loop.scope,/not an exact finite-field solution/);
 assert.match(data.field_loop.scope,/No equal-accuracy/);assert.match(mhdPage(),/Their initial discretizations and divergence operators differ/);
});
test('new comparison controls and scope notes have Japanese presentation strings',()=>{
 configureLocale(json('../locales/messages.json'),'ja');
 for(const en of ['Compare the reconstruction.','Play both ▷','Resolve the magnetic waves.','Final max conserved update rate','HLLE fallback faces'])assert.notEqual(translateText(en),en);
 configureLocale({},'en');
});
