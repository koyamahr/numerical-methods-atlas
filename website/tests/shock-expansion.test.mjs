import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {expansionPage} from '../shock-expansion.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const d=JSON.parse(read('../public/assets/shock-expansion/shock-expansion.json'));
const hash=b=>createHash('sha256').update(b).digest('hex');
test('shock expansion artifacts retain numerical sources and binary/figure hashes',()=>{
 for(const [p,v] of Object.entries(d.source_sha256))assert.equal(hash(read('../../'+p)),v,p);
 for(const [p,v] of Object.entries(d.artifact_sha256))assert.equal(hash(read('../public/assets/shock-expansion/'+p)),v,p);
 assert.match(d.scope,/not low-Mach PDE validation/);
});
test('PPM switch study separates limiting, tracing, reference and completion',()=>{
 assert.equal(d.ppm_cases.length,16);assert.equal(d.flux_cases.length,16);
 for(const c of d.ppm_cases){
  assert.equal(c.status,'completed');assert.equal(c.time,c.requested_time);
  assert.equal(c.x.length,c.n);assert.equal(c.primitive.length,c.n);
  assert.ok(c.minimum_density>0&&c.minimum_pressure>0);
  const config=d.ppm_configs.find(s=>s.id===c.config);
  if(!config.steepening)assert.equal(c.steepened_cells,0);
  if(!config.flattening)assert.equal(c.flattened_cells,0);
  if(c.problem==='shu-osher')assert.equal(c.error_l1,null);else assert.ok(c.error_l1>=0);
  if(c.problem==='moving-contact'){assert.ok(c.pressure_departure<1e-12&&c.velocity_departure<1e-12);assert.ok(c.conserved_integral_change.every(x=>Math.abs(x)<1e-11));}
 }
 const plain=d.ppm_cases.find(c=>c.problem==='moving-contact'&&c.config==='plain'),steep=d.ppm_cases.find(c=>c.problem==='moving-contact'&&c.config==='steep');
 assert.ok(steep.error_l1<.5*plain.error_l1);
 assert.ok(d.refinement.every(s=>s.orders.every(p=>p>1.9&&p<2.6)));
 const failed=d.flux_cases.filter(c=>c.status==='failed');assert.equal(failed.length,1);
 assert.equal(failed[0].solver,'ausm-plus');assert.equal(failed[0].problem,'strong-shock');
 assert.ok(failed[0].time>0&&failed[0].time<failed[0].requested_time);assert.equal(failed[0].error_l1,null);
 assert.match(failed[0].failure_reason,/retries exhausted/);
 assert.match(expansionPage(),/Only completed runs share the requested final time/);
});
test('forebody controls, wall pressures and histories remain distinguishable from a wake validation',()=>{
 assert.equal(d.body_runs.length,20);assert.equal(d.body_panels.length,12);
 const gamma=1.4,m=6,p2=1+2*gamma/(gamma+1)*(m*m-1),m2=(1+.5*(gamma-1)*m*m)/(gamma*m*m-.5*(gamma-1));
 const p0=p2*(1+.5*(gamma-1)*m2)**(gamma/(gamma-1));
 for(const r of d.body_runs){
  assert.deepEqual(r.shape,[r.nr,2*r.nr]);assert.equal(r.final_time,2);assert.equal(r.history[0][0],0);assert.equal(r.history.at(-1)[0],2);
  const a=r.metrics;assert.ok(a.minimum_density>0&&a.minimum_pressure>0);
  assert.ok(a.conservation_residual.every(v=>Math.abs(v)<2e-9));
  assert.ok(Math.abs(a.normal_shock_stagnation_reference-p0)<1e-12);
  const mid=r.nr,p=.5*(r.wall_pressure[mid-1]+r.wall_pressure[mid]);assert.ok(Math.abs(p-a.nose_pressure)<1e-13);
  for(let i=0;i<r.wall_cp.length;i++)assert.ok(Math.abs(r.wall_cp[i]-(r.wall_pressure[i]-1)/25.2)<1e-14);
  assert.ok(d.body_runs.some(c=>c.nr===r.nr&&c.method===r.method&&c.amplitude===0));
 }
 const fine=d.body_runs.find(r=>r.nr===48&&r.method==='roe'&&r.amplitude>0);
 const hlle=d.body_runs.find(r=>r.nr===48&&r.method==='hlle'&&r.amplitude>0);
 assert.ok(fine.metrics.final_symmetry_defect>1000*hlle.metrics.final_symmetry_defect);
 assert.match(expansionPage(),/no viscous wake/);assert.match(expansionPage(),/not a carbuncle-free certification/);
});
