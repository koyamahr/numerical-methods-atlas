import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>readFileSync(new URL(p,import.meta.url));
const catalog=JSON.parse(read('../public/assets/movies/catalog.json'));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
test('published movies identify current numerical and rendering sources',()=>{
 for(const [path,expected] of Object.entries(catalog.source_sha256))assert.equal(hash(read('../../'+path)),expected,path);
 assert.equal(catalog.quick,false);assert.equal(catalog.movies.length,4);
});
test('every published image and MP4 has matching hashes, positive states, fixed scales and physical endpoints',()=>{
 for(const movie of catalog.movies){
  assert.equal(movie.frames.length,81);assert.equal(movie.frames[0].time,0);assert.equal(movie.frames.at(-1).time,movie.final_time);
  assert.equal(movie.frames.at(-1).step,movie.solver_steps);
  assert.equal(hash(read('../public/assets/movies/'+movie.video)),movie.video_sha256);
  for(const [i,frame] of movie.frames.entries()){
   assert.equal(hash(read('../public/assets/movies/'+frame.file)),frame.image_sha256);
   assert.ok(frame.min_density>0&&frame.min_pressure>0);
   assert.ok(movie.scales[0].min<=frame.min_density&&movie.scales[0].max>=frame.max_density);
   assert.ok(movie.scales[1].min<=frame.min_pressure&&movie.scales[1].max>=frame.max_pressure);
   if(i){assert.ok(frame.time>movie.frames[i-1].time);assert.ok(frame.step>movie.frames[i-1].step);}
  }
 }
});
