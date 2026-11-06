import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fieldFigures,matchesGallery} from '../gallery.js';
import {combineMovieCatalogs} from '../movies.js';
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
  assert.equal(fieldFigures.filter(f=>matchesGallery(f,'2')).length,10);
});

test('every multidimensional movie has a reachable field card',()=>{
  const catalogs=['catalog.json','shock-catalog.json'].map(name=>JSON.parse(read('../public/assets/movies/'+name)));
  for(const movie of catalogs.flatMap(c=>c.movies)){
    const card=fieldFigures.find(f=>f.movie===movie.id);
    assert.ok(card,movie.id);assert.equal(card.dimension,movie.shape.length);
    if(movie.id!=='forward-step')assert.equal(card.file,'movies/'+movie.poster);
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

test('shock-case artifacts retain numerical provenance and analytical comparison',()=>{
  const manifest=JSON.parse(read('../public/assets/shock-gallery.json'));
  for(const [path,expected] of Object.entries(manifest.source_sha256))assert.equal(hash(read('../../'+path)),expected,path);
  for(const [path,expected] of Object.entries(manifest.artifact_sha256))assert.equal(hash(read('../public/assets/'+path)),expected,path);
  for(const grids of Object.values(manifest.wedges)){
    assert.equal(grids.length,2);
    assert.ok(grids[1].density_cell_average_l1<grids[0].density_cell_average_l1);
    assert.ok(Math.abs(grids[1].wall_pressure_ratio_median/grids[1].pressure_ratio_exact-1)<.03);
  }
  const shocks=fieldFigures.filter(f=>matchesGallery(f,'2','2D shock interactions'));
  assert.equal(shocks.length,4);
});

test('movie catalogs combine all five cases without overriding existing IDs',()=>{
  const original=JSON.parse(read('../public/assets/movies/catalog.json'));
  const extension=JSON.parse(read('../public/assets/movies/shock-catalog.json'));
  assert.equal(combineMovieCatalogs(original,extension).movies.length,5);
  assert.throws(()=>combineMovieCatalogs(original,original),/Duplicate movie/);
  for(const [path,expected] of Object.entries(extension.source_sha256))assert.equal(hash(read('../../'+path)),expected,path);
  for(const movie of extension.movies){
    assert.equal(movie.frames.length,81);assert.equal(movie.frames[0].time,0);
    assert.equal(movie.frames.at(-1).time,4);assert.equal(movie.frames.at(-1).step,movie.solver_steps);
    assert.equal(hash(read('../public/assets/movies/'+movie.video)),movie.video_sha256);
    for(const [i,frame] of movie.frames.entries()){
      assert.equal(hash(read('../public/assets/movies/'+frame.file)),frame.image_sha256);
      assert.ok(frame.min_density>0&&frame.min_pressure>0);
      if(i)assert.ok(frame.time>movie.frames[i-1].time&&frame.step>movie.frames[i-1].step);
      for(const [k,min,max] of [[0,'min_density','max_density'],[1,'min_pressure','max_pressure']])
        assert.ok(movie.scales[k].min<=frame[min]&&frame[max]<=movie.scales[k].max);
    }
  }
});
