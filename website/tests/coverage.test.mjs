import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {coverageHighlights,filterCoverage} from '../coverage.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const data=JSON.parse(read('../content/coverage.json'));
const references=JSON.parse(read('../../catalog/references.json'));
test('advertised publication count uses unique works and excludes non-paper types',()=>{
 const doi=references.filter(e=>e.doi).map(e=>e.doi.toLowerCase());
 assert.equal(new Set(doi).size,doi.length);
 const journal=references.filter(e=>(e.type||'article')==='article');
 const conference=references.filter(e=>e.type==='inproceedings');
 assert.equal(data.counts.papers,journal.length+conference.length);
 assert.equal(data.counts.references,references.length);
 assert.equal(data.counts.papers+data.counts.books+data.counts.chapters+data.counts.reports+data.counts.other_sources,data.counts.references);
 assert.equal(references.find(e=>e.id==='burgers1948').type,'incollection');
 for(const [p,expected] of Object.entries(data.source_sha256))assert.equal(createHash('sha256').update(read('../../'+p)).digest('hex'),expected,p);
});
test('model and method inventories expose scope and collapse named aliases',()=>{
 for(const kind of ['equation','method']){
  const entries=filterCoverage(data,{kind});
  assert.equal(new Set(entries.map(e=>e.id)).size,entries.length);
  assert.equal(entries.length,data.counts[kind==='equation'?'equations':'methods']);
  assert.equal(filterCoverage(data,{kind,status:'reading'}).length,data.counts[kind==='equation'?'reading_equations':'reading_methods']);
 }
 assert.equal(filterCoverage(data,{query:'SSPRK(2,2)'}).length,1);
 assert.equal(filterCoverage(data,{kind:'equation',status:'reading',query:'Keller'}).length,1);
 assert.equal(filterCoverage(data,{kind:'equation',status:'local-example',query:'Keller'}).length,0);
 const bios=data.items.filter(e=>e.chapter==='biological-models');
 assert.equal(bios.length,22);assert.ok(bios.every(e=>e.status==='reading'));
 const html=coverageHighlights(data);
 assert.match(html,/Journal & conference papers/);
 assert.match(html,/reading only/);
 assert.doesNotMatch(html,/verified solvers|original papers|production solvers/i);
});
test('every counted item has a real reading chapter',()=>{
 for(const e of data.items)assert.ok(read(`../content/${e.chapter}.md`).length>0);
});

test('the static reading inventory lists each advertised item exactly once',()=>{
 const markdown=read('../../docs/site-coverage.md').toString();
 const labels=[...markdown.matchAll(/^- \[([^\]]+)\]\(/gm)].map(match=>match[1]);
 assert.deepEqual(labels.sort(),data.items.map(item=>item.label).sort());
});
