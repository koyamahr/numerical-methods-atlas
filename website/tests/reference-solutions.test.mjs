import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {referencePage} from '../reference-solutions.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../public/assets/reference-solutions.json'));
const near=(a,b,tol=2e-11)=>assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);

test('reference artifacts identify their source, type and sampling convention',()=>{
 for(const [p,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read('../../'+p)).digest('hex'),hash,p);
 assert.equal(data.cases.length,18);assert.equal(new Set(data.cases.map(c=>c.id)).size,18);
 assert.match(data.quadrature.convention,/not rigorous error bounds/);
 for(const c of data.cases){
  assert.ok(['analytic','semi-analytic','manufactured'].includes(c.kind));
  assert.ok(c.assumptions.length>25&&c.sources.every(s=>s.startsWith('https://')));
  for(const [i,f] of c.frames.entries()){
   if(i)assert.ok(f.time>c.frames[i-1].time);
   assert.equal(f.point.length,c.x.length);
   for(const q of f.point){assert.equal(q.length,c.components.length);assert.ok(q.every(Number.isFinite));}
   assert.equal(f.grids.length,c.dimension===1?3:0);
   for(const g of f.grids){
    assert.equal(g.edges.length,g.n+1);assert.equal(g.average.length,g.n);
    assert.ok(g.max_order_difference.every(v=>v>=0&&v<1e-10));
    for(const q of g.average){assert.equal(q.length,c.components.length);assert.ok(q.every(Number.isFinite));}
   }
  }
 }
 assert.match(referencePage(),/id="reference-case" disabled/);
 assert.match(referencePage(),/not rigorous error bounds/);
 assert.match(referencePage(),/href="#\/read\/reference-solutions"/);
});

test('saved sine means agree with analytic integrals and shock cut cells are averaged',()=>{
 for(const id of ['sine-advection','sine-heat']){
  const c=data.cases.find(c=>c.id===id);
  for(const f of c.frames)for(const g of f.grids)for(let i=0;i<g.n;i++){
   const a=g.edges[i],b=g.edges[i+1],shift=id==='sine-advection'?f.time:0;
   const amplitude=.25*(id==='sine-heat'?Math.exp(-.02*(2*Math.PI)**2*f.time):1);
   near(g.average[i][0],1+amplitude*(Math.cos(2*Math.PI*(a-shift))-Math.cos(2*Math.PI*(b-shift)))/(2*Math.PI*(b-a)));
  }
 }
 const c=data.cases.find(c=>c.id==='burgers-shock'),f=c.frames.find(f=>f.time>0),s=.5+.5*f.time,g=f.grids[0];
 const i=g.edges.findIndex((a,i)=>a<s&&g.edges[i+1]>s);
 assert.ok(i>=0);near(g.average[i][0],(s-g.edges[i])/(g.edges[i+1]-g.edges[i]));
 assert.ok(Math.abs(g.average[i][0]-g.center_values[i][0])>.01);
});

test('system reference means retain independent mass and momentum balances',()=>{
 const setups=[['euler-sod',[1,0,2.5],[.125,0,.25],[0,.9,0]],
  ['swe-dam-break',[2,0],[1,0],[0,1.5]],['isothermal-jump',[1,0],[.125,0],[0,.875]]];
 for(const [id,left,right,flux] of setups){
  const c=data.cases.find(c=>c.id===id);assert.equal(c.field_type,'conserved');
  for(const f of c.frames)for(const g of f.grids)for(let j=0;j<left.length;j++){
   const integral=g.average.reduce((s,q,i)=>s+q[j]*(g.edges[i+1]-g.edges[i]),0);
   near(integral,.5*(left[j]+right[j])+f.time*flux[j]);
  }
 }
 const tg=data.cases.find(c=>c.id==='taylor-green');assert.equal(tg.dimension,2);assert.match(tg.assumptions,/x-slice at y=π\/4/);
});
