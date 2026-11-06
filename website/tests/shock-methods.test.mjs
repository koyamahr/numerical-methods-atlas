import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {reconstructionPage,robustnessPage} from '../shock-methods.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const json=p=>JSON.parse(read(p));
const hash=b=>createHash('sha256').update(b).digest('hex');
for(const [folder,name] of [['reconstruction','reconstruction'],['shock-methods','robustness']])test(name+' computed artifacts retain source and artifact hashes',()=>{
 const data=json(`../public/assets/${folder}/${name}.json`);
 for(const [p,v] of Object.entries(data.source_sha256))assert.equal(hash(read('../../'+p)),v,p);
 for(const [p,v] of Object.entries(data.artifact_sha256))assert.equal(hash(read(`../public/assets/${folder}/`+p)),v,p);
});
test('reconstruction comparisons distinguish FV/FD norms, references and basis choices',()=>{
 const d=json('../public/assets/reconstruction/reconstruction.json');assert.equal(d.cases.length,24);assert.equal(d.flux_cases.length,12);assert.equal(d.refinement.length,8);
 for(const c of d.cases){
  assert.equal(c.x.length,c.n);assert.equal(c.primitive.length,c.n);assert.ok(c.minimum_density>0&&c.minimum_pressure>0);assert.equal(c.rejected_steps,0);
  assert.equal(c.representation,c.method.startsWith('weno')?'point values':'cell averages');
  if(c.problem==='shu-osher')assert.equal(c.error_l1,null);else assert.ok(c.error_l1>=0);
 }
 for(const c of d.flux_cases){assert.ok(['hllc','roe','hlle','ausm'].includes(c.solver));assert.ok(c.minimum_density>0&&c.minimum_pressure>0);assert.equal(c.rejected_steps,0);}
 for(const s of d.refinement)if(s.method.startsWith('weno'))assert.ok(s.orders.at(-1)>4.7);
 assert.match(reconstructionPage(),/not a matched-cost ranking/);assert.match(reconstructionPage(),/wave tracing/);
});
test('stationary-shock comparison includes each perturbed and unperturbed configuration',()=>{
 const d=json('../public/assets/shock-methods/robustness.json');assert.equal(d.methods.length,6);assert.equal(d.runs.length,48);assert.equal(d.panels.length,4);
 for(const n of [64,128])for(const phase of [0,.5])for(const m of d.methods)for(const amplitude of [0,1e-4]){
  const r=d.runs.find(r=>r.n===n&&r.phase===phase&&r.method===m.id&&r.amplitude===amplitude);assert.ok(r);
  assert.equal(r.history[0][0],0);assert.equal(r.history.at(-1)[0],.2);assert.deepEqual(r.shape,[n,n/4]);
  assert.ok(r.metrics.min_density>0&&r.metrics.min_pressure>0);assert.equal(r.metrics.retried_steps,0);
  if(amplitude===0)assert.ok(r.metrics.maximum_alternating_density<1e-12);
 }
 const select=(id,phase)=>d.runs.find(r=>r.n===128&&r.phase===phase&&r.method===id&&r.amplitude>0).metrics;
 assert.ok(select('roe-fixed',0).final_alternating_density>100*select('roe-fixed',0).initial_alternating_density);
 assert.ok(select('roe-fixed',.5).final_alternating_density<select('roe-fixed',0).final_alternating_density/100);
 assert.ok(select('hlle',0).final_alternating_density<1e-10);
 assert.match(d.scope,/transverse velocity zero/);assert.match(d.scope,/No carbuncle-free certification/);
 assert.match(robustnessPage(),/not Quirk/);
});
test('Property U algebra and entropy counterexample are separate',()=>{
 const d=json('../public/assets/shock-methods/robustness.json').roe_property_u;
 assert.equal(d.state_pairs,2000);assert.ok(d.max_relative_jump_residual<1e-12);assert.ok(d.max_relative_consistency_residual<1e-12);assert.ok(d.max_inverse_residual<1e-12);assert.ok(d.minimum_acoustic_speed>0);
 for(const w of d.waves){assert.ok(w.jump_residual<1e-12);if(w.name.includes('expansion'))assert.ok(w.raw_flux_exact_reference_error>.1);else assert.ok(w.raw_flux_exact_reference_error<1e-12);}
});
