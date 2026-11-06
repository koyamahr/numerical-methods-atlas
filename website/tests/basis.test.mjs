import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/basis.json'));

test('basis controls ship complete finite arrays with current source provenance',()=>{
 for(const [file,hash] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read('../../'+file)).digest('hex'),hash,file);
 for(const p of [1,2,3,4,6,8])for(const kind of ['legendre','orthonormal','chebyshev','gll','equispaced']){
  const c=data.cases.find(c=>c.degree===p&&c.kind===kind);assert.ok(c,`${p} ${kind}`);
  assert.equal(c.values.length,data.x.length);
  for(const row of c.values){assert.equal(row.length,p+1);assert.ok(row.every(Number.isFinite));}
  for(const key of ['mass','quadrature_mass','stiffness']){
   assert.equal(c[key].length,p+1);
   c[key].forEach((row,i)=>{assert.equal(row.length,p+1);row.forEach((v,j)=>{assert.ok(Number.isFinite(v));assert.ok(Math.abs(v-c[key][j][i])<1e-11);});});
  }
 }
 assert.equal(data.triangle.nodes.length,6);
 for(const values of data.triangle.values)assert.ok(Math.abs(values.reduce((a,b)=>a+b,0)-1)<1e-13);
});

test('saved exhibits retain the exact-mass caveat and projection error definitions',()=>{
 const c=data.cases.find(c=>c.degree===4&&c.kind==='gll');
 assert.equal(c.nodes[2],0); // sign(0)=0 must not silently become sign(1e-16)=1.
 assert.ok(Math.abs(c.mass[0][1])>1e-4);
 assert.ok(Math.abs(c.quadrature_mass[0][1])<1e-13);
 assert.ok(c.mass_difference_norm>1e-3);
 const cheb=data.cases.find(c=>c.degree===4&&c.kind==='chebyshev');
 assert.ok(Math.abs(cheb.mass[0][2]+2/3)<1e-13);
 let previous=Infinity;
 for(const p of [1,2,3,4,6,8])for(const profile of ['smooth','jump']){
  const a=data.approximations.find(c=>c.degree===p&&c.profile===profile);
  assert.ok(a.projection_l2<=a.interpolation_l2+1e-12);
  for(const key of ['projected','interpolated','exact']){assert.equal(a[key].length,data.x.length);assert.ok(a[key].every(Number.isFinite));}
  if(profile==='smooth'){assert.ok(a.projection_l2<previous);previous=a.projection_l2;}
 }
});
