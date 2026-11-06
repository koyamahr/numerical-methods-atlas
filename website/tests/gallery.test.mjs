import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fieldFigures,matchesGallery} from '../gallery.js';
const read=p=>readFileSync(new URL(p,import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');

test('dimension and subject filters intersect without labeling diagnostic plots as spatial fields',()=>{
  const diagnostic={category:'Elliptic & iterative'};
  assert.equal(matchesGallery(diagnostic),false);
  assert.equal(matchesGallery(diagnostic,'all'),true);
  const three=fieldFigures.find(f=>f.dimension===3);
  assert.equal(matchesGallery(three,'3','Particles & gravity'),true);
  assert.equal(matchesGallery(three,'2'),false);
  assert.equal(matchesGallery(three,'3','MHD'),false);
  assert.equal(fieldFigures.filter(f=>matchesGallery(f,'2')).length,6);
});

test('all four multidimensional movies have reachable field cards using their actual final states',()=>{
  const catalog=JSON.parse(read('../public/assets/movies/catalog.json'));
  for(const movie of catalog.movies){
    const card=fieldFigures.find(f=>f.movie===movie.id);
    assert.ok(card,movie.id);assert.equal(card.dimension,movie.shape.length);
    assert.equal(card.file,'movies/'+movie.poster);
    assert.equal(movie.poster,movie.frames.at(-1).file);
  }
  for(const card of fieldFigures)assert.ok(read('../public/assets/'+card.file).length);
});

test('new field views retain numerical provenance, arrays and appropriate diagnostic tolerances',()=>{
  const manifest=JSON.parse(read('../public/assets/multidimensional-fields.json'));
  for(const [path,expected] of Object.entries(manifest.source_sha256))assert.equal(hash(read('../../'+path)),expected,path);
  for(const [path,expected] of Object.entries(manifest.artifact_sha256))assert.equal(hash(read('../public/assets/'+path)),expected,path);
  assert.ok(manifest.fem.l2<.01);
  assert.ok(manifest.mac.velocity_rms<.001);
  assert.ok(manifest.mac.max_native_divergence<1e-10);
  assert.deepEqual(manifest.poisson3d.shape,[32,32,32]);
  assert.ok(manifest.poisson3d.maximum_point_error<1e-12);
});
