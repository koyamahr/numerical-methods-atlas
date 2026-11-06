import {translateText} from './i18n.js';
let catalog;
let cleanup=()=>{};
const base='assets/movies/';
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const clampFrame=(index,count)=>Math.max(0,Math.min(count-1,Math.round(index)));
export function disposeMovies(){cleanup();cleanup=()=>{};}
export function combineMovieCatalogs(...catalogs){
 const movies=catalogs.flatMap(c=>c.movies);
 if(new Set(movies.map(m=>m.id)).size!==movies.length)throw Error('Duplicate movie ID');
 return {movies};
}
export function moviesPage(){return `<section class="page-intro page-width"><p class="eyebrow">THE MOTION GALLERY · GENUINE COMPUTED STATES</p><h1>Watch the computation<br><em>unfold.</em></h1><p>Time-dependent tests deserve a time history. Play saved states, pause at a shock interaction, or inspect one frame at a time. Steady solutions remain still figures.</p></section><section class="page-width laboratory" id="movie-notebook"><aside class="lab-controls"><label for="movie-case">Time-dependent test</label><select id="movie-case" disabled><option>Loading movie catalog…</option></select><div id="movie-settings" class="lab-settings"></div><label for="movie-speed">Playback speed</label><select id="movie-speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select><label class="mesh-checkbox"><input id="movie-loop" type="checkbox"> Loop playback</label><p class="lab-chart-note">Playback speed changes presentation timing. Physical simulation time is printed in each saved frame.</p><a class="text-link" id="movie-method" href="#/read/movies">Read the method ↗</a><a class="text-link" href="#/read/movies">Sampling & color-scale definitions ↗</a><a class="text-link" href="assets/movies/catalog.json" download>Download run manifests ↓</a><a class="text-link" href="assets/movies/shock-catalog.json" download>Download the forward-step manifest ↓</a></aside><div class="lab-results"><div id="movie-summary" class="lab-summary" aria-live="polite">Loading computed snapshots…</div><div class="lab-chart-card movie-stage" id="movie-display"><div class="lab-chart-header"><h2 id="movie-title">Saved simulation states</h2><span id="movie-time"></span></div><img id="movie-frame" width="960" height="640" alt="" decoding="async"><div class="movie-controls" aria-label="Saved-frame playback controls"><button id="movie-first" disabled aria-label="First frame">|←</button><button id="movie-previous" disabled aria-label="Previous frame">←</button><button id="movie-play" aria-pressed="false" disabled>Play</button><button id="movie-next" disabled aria-label="Next frame">→</button><button id="movie-last" disabled aria-label="Last frame">→|</button><span id="movie-position"></span><a id="movie-open" target="_blank" rel="noopener">Open frame ↗</a></div><label class="movie-seek-label" for="movie-seek">Saved frame <output id="movie-seek-label"></output></label><input id="movie-seek" type="range" min="0" max="1" step="1" value="0" disabled><p id="movie-scale-note" class="lab-chart-note"></p></div><div class="movie-details"><div class="lab-explanation"><p class="eyebrow">AT THIS PHYSICAL TIME</p><dl id="movie-metrics"></dl><p id="movie-scope"></p></div><div class="lab-explanation"><p class="eyebrow">EXPORT & PRESENT</p><a class="button" id="movie-download" download>Download MP4 ↓</a><a class="text-link" id="movie-frame-download" download>Download this frame ↓</a><p class="lab-chart-note">MP4 uses the same computed frames at 12 frames per second. No sound. Image frames retain the fixed scales and physical timestamps.</p><details><summary>Watch the MP4 in the native player</summary><video id="movie-video" controls playsinline preload="none" aria-label="Computed simulation movie"></video></details></div></div></div></section><aside class="callout page-width"><h2>Motion is evidence of evolution, not convergence.</h2><p>These movies use the same educational solvers as the reading chapters. Each color scale stays fixed over its complete run; frames are never interpolated. The initial and final states are included. CT and GLM use different native magnetic-divergence operators. The original KEEP example is a smooth vortex with no shock stabilization.</p><a class="text-link" href="#/gallery">Return to the still-image gallery ↗</a></aside>`;}
export async function wireMovies(requestedCase){
 const root=document.getElementById('movie-notebook');
 try{
  catalog??=Promise.all(['catalog.json','shock-catalog.json'].map(name=>fetch(base+name).then(r=>{
   if(!r.ok)throw Error('Movie catalog could not load');return r.json();
  }))).then(parts=>combineMovieCatalogs(...parts));
  const data=await catalog;if(!root.isConnected)return;
  const get=id=>root.querySelector(`#${id}`);let movie,current=0,playing=false,timer,loadId=0,playbackGeneration=0;
  const cache=new Map();
  const pause=()=>{playing=false;playbackGeneration++;clearTimeout(timer);get('movie-play').textContent='Play';get('movie-play').setAttribute('aria-pressed','false');};
  cleanup=()=>{pause();loadId++;get('movie-video').pause();};
  const preload=(index)=>{
   const path=base+movie.frames[index].file;
   if(!cache.has(path)){
    const image=new Image();image.src=path;
    const ready=image.decode().then(()=>image);ready.catch(()=>cache.delete(path));cache.set(path,ready);while(cache.size>8)cache.delete(cache.keys().next().value);
   }
   return cache.get(path);
  };
  const show=async(index)=>{
   const token=++loadId,selected=movie;index=clampFrame(index,movie.frames.length);
   root.setAttribute('aria-busy','true');get('movie-summary').textContent='Loading saved frame…';
   try{await preload(index);}catch(error){if(token===loadId&&root.isConnected){pause();root.removeAttribute('aria-busy');get('movie-summary').textContent='This frame could not load. Try another frame or the MP4.';}return false;}
   if(token!==loadId||!root.isConnected||selected!==movie)return false;
   current=index;const frame=movie.frames[current];
   get('movie-frame').src=base+frame.file;get('movie-frame').alt=`${movie.title}: density and pressure at physical time ${frame.time.toFixed(6)}, solver step ${frame.step}`;
   get('movie-time').textContent=`t = ${frame.time.toFixed(6)}`;
   get('movie-position').textContent=`${current+1} / ${movie.frames.length}`;
   get('movie-seek').value=current;get('movie-seek-label').textContent=`Frame ${current+1} of ${movie.frames.length}`;
   get('movie-summary').innerHTML=`<span>${esc(movie.title)}</span><span>Physical t = ${frame.time.toFixed(6)}</span><span>Solver step ${frame.step}</span>`;
   get('movie-first').disabled=get('movie-previous').disabled=current===0;
   get('movie-last').disabled=get('movie-next').disabled=current===movie.frames.length-1;
   const num=v=>Math.abs(v)<.001&&v!==0?v.toExponential(3):v.toPrecision(6);
   get('movie-metrics').innerHTML=`<div><dt>Density range</dt><dd>${num(frame.min_density)} — ${num(frame.max_density)}</dd></div><div><dt>Pressure range</dt><dd>${num(frame.min_pressure)} — ${num(frame.max_pressure)}</dd></div>${movie.divergence_operator?`<div><dt>max |div B| (${esc(movie.divergence_operator)})</dt><dd>${frame.max_abs_divB.toExponential(3)}</dd></div>`:''}${frame.entropy_proxy!==undefined?`<div><dt>Mass-weighted entropy-proxy change</dt><dd>${((frame.entropy_proxy-movie.frames[0].entropy_proxy)/movie.frames[0].mass).toExponential(3)}</dd></div>`:''}`;
   get('movie-frame-download').href=base+frame.file;get('movie-open').href=base+frame.file;root.removeAttribute('aria-busy');
   for(let ahead=1;ahead<=3&&current+ahead<movie.frames.length;ahead++)preload(current+ahead).catch(()=>{});
   return true;
  };
  const schedule=(generation=playbackGeneration)=>{if(playing&&root.isConnected&&generation===playbackGeneration)timer=setTimeout(async()=>{
   if(generation!==playbackGeneration)return;
   let next=current+1;if(next===movie.frames.length){if(!get('movie-loop').checked){pause();return;}next=0;}
   if(await show(next))schedule(generation);
  },1000/(movie.fps*Number(get('movie-speed').value)));};
  const choose=async()=>{
   pause();get('movie-video').pause();loadId++;cache.clear();movie=data.movies.find(m=>m.id===get('movie-case').value);current=0;
   history.replaceState(null,'',`#/movies?case=${encodeURIComponent(movie.id)}`);
   get('movie-title').textContent=movie.title;
   get('movie-settings').innerHTML=`${esc(movie.method)}<br>${movie.shape.join(' × ')} cells · CFL = ${movie.cfl}<br>Physical final time = ${movie.final_time}<br>${esc(movie.boundary)}`;
   get('movie-scope').textContent=movie.scope;get('movie-method').href=`#/read/${movie.chapter}`;
   get('movie-seek').max=movie.frames.length-1;get('movie-seek').disabled=false;
   get('movie-download').href=base+movie.video;get('movie-download').download=movie.id+'.mp4';
   get('movie-video').src=base+movie.video;get('movie-video').poster=base+movie.poster;get('movie-video').load();
   get('movie-scale-note').textContent=movie.scales.map(s=>translateText(`${s.label}: ${s.min.toPrecision(4)} to ${s.max.toPrecision(4)}`)).join(' · ')+' · '+translateText('fixed for this entire movie');
   get('movie-play').disabled=false;await show(0);
  };
  get('movie-case').innerHTML=data.movies.map(m=>`<option value="${esc(m.id)}">${esc(m.title)}</option>`).join('');get('movie-case').disabled=false;
  get('movie-case').value=data.movies.some(m=>m.id===requestedCase)?requestedCase:data.movies[0].id;
  get('movie-case').addEventListener('change',choose);
  get('movie-play').addEventListener('click',async()=>{
   if(playing){pause();return;}get('movie-video').pause();
   const selected=movie,generation=playbackGeneration;
   if(current===movie.frames.length-1&&!await show(0))return;
   if(selected!==movie||generation!==playbackGeneration||!root.isConnected)return;
   playing=true;playbackGeneration++;get('movie-play').textContent='Pause';get('movie-play').setAttribute('aria-pressed','true');schedule();
  });
  const seek=index=>{pause();show(index);};
  get('movie-first').addEventListener('click',()=>seek(0));get('movie-previous').addEventListener('click',()=>seek(current-1));
  get('movie-next').addEventListener('click',()=>seek(current+1));get('movie-last').addEventListener('click',()=>seek(movie.frames.length-1));
  get('movie-seek').addEventListener('input',()=>seek(Number(get('movie-seek').value)));
  get('movie-speed').addEventListener('change',()=>{playbackGeneration++;clearTimeout(timer);schedule();});
  get('movie-video').addEventListener('play',pause);
  await choose();
 }catch(error){if(root.isConnected)root.querySelector('#movie-summary').textContent='The movie catalog could not load. Reload the page or read the movie guide.';console.error(error);}
}
