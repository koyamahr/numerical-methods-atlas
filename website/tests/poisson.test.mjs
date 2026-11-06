import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {poissonPage,residualChart} from '../poisson.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../public/assets/poisson-comparison/comparison.json'));
const hash=b=>createHash('sha256').update(b).digest('hex');
test('Poisson artifacts and solver source hashes match the published experiment',()=>{
 for(const [p,v] of Object.entries(data.source_sha256))assert.equal(hash(read('../../'+p)),v,p);
 for(const [p,v] of Object.entries(data.artifact_sha256))assert.equal(hash(read('../public/assets/poisson-comparison/'+p)),v,p);
});
test('all solver configurations use the same true residual threshold and retain timing trials',()=>{
 assert.equal(data.methods.length,8);assert.equal(data.runs.length,56);assert.equal(data.cases.length,7);assert.equal(data.tolerance,1e-8);
 for(const c of data.cases){
  const runs=data.runs.filter(r=>r.case===c.id&&r.n===c.n);assert.equal(runs.length,8);
  for(const r of runs){
   assert.equal(r.unknowns,c.n**2);assert.ok(r.relative_residual<=data.tolerance);assert.ok(r.algebraic_rms<1e-7);
   assert.equal(r.trial_seconds.length,3);assert.equal(r.seconds,[...r.trial_seconds].sort((a,b)=>a-b)[1]);
   assert.equal(r.trial_seconds[r.selected_trial],r.seconds);assert.equal(r.history[0][0],0);assert.equal(r.history[0][2],1);
   assert.equal(r.history.at(-1)[0],r.steps);assert.equal(r.history.at(-1)[2],r.relative_residual);assert.equal(r.full_history_length,r.steps+1);
   for(let i=1;i<r.history.length;i++)assert.ok(r.history[i][0]>r.history[i-1][0]&&r.history[i][1]>=r.history[i-1][1]);
   if(c.id==='localized')assert.equal(r.continuous_rms,null);else assert.ok(r.continuous_rms>0);
  }
 }
});
test('broad manufactured forcing and a labeled one-mode example give distinct CG behavior',()=>{
 const cg=data.runs.filter(r=>r.method==='cg');assert.equal(cg.find(r=>r.case==='single-mode').steps,1);
 for(const r of cg.filter(r=>r.case!=='single-mode'))assert.ok(r.steps>20);
 const e=data.cases.filter(c=>c.id==='manufactured').map(c=>c.discrete_continuous_rms);
 assert.ok(Math.log2(e[0]/e[1])>1.9&&Math.log2(e[1]/e[2])>1.9);
 assert.equal(data.one_dimensional.length,6);
 assert.match(poissonPage(),/Plain Thomas solves a tridiagonal 1D system/);assert.match(poissonPage(),/not a universal speed ranking/);
});
test('both residual chart axes render finite curves and direct endpoints',()=>{
 const runs=data.runs.filter(r=>r.case==='manufactured'&&r.n===63);
 for(const axis of ['units','seconds']){
  const svg=residualChart(data,runs,axis);assert.ok(!/NaN|Infinity/.test(svg));assert.equal((svg.match(/<circle /g)||[]).length,2);
  assert.equal((svg.match(/<path /g)||[]).length,6);
 }
});
