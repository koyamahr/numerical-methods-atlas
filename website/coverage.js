const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const statusLabel=status=>status==='local-example'?'Local example':'Reading only';
export function coverageHighlights(data){
 const c=data.counts;
 const metrics=[
  {n:c.papers,label:'Journal & conference papers',note:`${c.journal_articles} journal · ${c.conference_papers} conference · ${c.references} sources in all`,href:'#/references',className:'citation-highlight'},
  {n:c.equations,label:'Equation & model entries',note:`${c.local_equations} with local examples · ${c.reading_equations} reading only`,href:'#/coverage?kind=equation',className:''},
  {n:c.methods,label:'Methods & building blocks',note:`${c.local_methods} with local examples · ${c.reading_methods} reading only`,href:'#/coverage?kind=method',className:''},
  {n:c.gallery_cases,label:'Equation-gallery cases',note:`${c.gallery_equations} equation families · saved numerical profiles`,href:'#/equations',className:''}
 ];
 return `<section class="coverage-highlights page-width" aria-label="The atlas in numbers"><div class="coverage-metric-grid">${metrics.map(m=>`<a class="coverage-metric ${m.className}" href="${m.href}"><span class="coverage-number">${m.n}</span><h2>${m.label}</h2><p>${m.note}</p><span aria-hidden="true" class="coverage-arrow">↗</span></a>`).join('')}</div><div class="coverage-footnote"><p>Named entries, with scope shown. Paper totals include reviews, translations and accepted records. ${c.reading_chapters} reading chapters.</p><a class="text-link" href="#/coverage">See what is counted →</a></div></section>`;
}
export function coveragePage(data){
 const c=data.counts;
 return `<section class="page-intro page-width"><p class="eyebrow">THE ATLAS IN NUMBERS / COUNTED ${esc(data.counted_on)}</p><h1>${c.equations} models.<br>${c.methods} methods.<br><em>${c.papers} papers.</em></h1><p>A named inventory across fluids, fields, kinetic models and biology. Open the model or method behind each number, and see which entries have a local example.</p><a class="text-link" href="#/read/site-coverage">Read the counting rules ↗</a> · <a class="text-link" href="coverage.json" download>Download the inventory ↓</a></section>${coverageHighlights(data)}<section id="coverage-inventory" class="page-width coverage-inventory"><div class="coverage-filters"><div><label for="coverage-kind">Browse the inventory</label><select id="coverage-kind"><option value="all">All models and methods</option><option value="equation">Equations &amp; models</option><option value="method">Methods &amp; building blocks</option></select></div><div><label for="coverage-status">Scope</label><select id="coverage-status"><option value="all">All scopes</option><option value="local-example">With local examples</option><option value="reading">Reading only</option></select></div><div><label for="coverage-search">Find an entry</label><input id="coverage-search" type="search" placeholder="Burgers, GMRES, Turing…"></div></div><p id="coverage-count" class="small-mono" aria-live="polite"></p><div id="coverage-results"></div></section><section class="page-width coverage-definitions"><div><p class="eyebrow">THE COUNTING UNIT</p><h2>Equations and models</h2><p>${esc(data.policy.equations)}</p><h2>Methods and building blocks</h2><p>${esc(data.policy.methods)}</p><p>“Local example” can mean a reduced model, static force calculation, reconstruction operator or linear Fourier symbol. Each linked chapter states its verified scope. It does not imply a complete production solver.</p></div><div><p class="eyebrow">KEEP THE SOURCES VISIBLE</p><h2>${c.papers} papers.<br>${c.references} sources in all.</h2><dl class="coverage-publications">${[[c.journal_articles,'Journal articles'],[c.conference_papers,'Conference papers'],[c.books,'Books'],[c.chapters,'Book chapters'],[c.reports,'Technical / teaching reports'],[c.other_sources,'Other sources / documentation / preprint']].map(([n,label])=>`<div><dt>${label}</dt><dd>${n}</dd></div>`).join('')}</dl><p>${esc(data.policy.papers)}</p><p>Full-text inspection status remains in each source note. Catalog entries are counted once per publication identity; a separately published translation is a separate work.</p><a class="text-link" href="#/references">Open the searchable reference library ↗</a></div></section>`;
}
export function filterCoverage(data,{kind='all',status='all',query=''}={}){
 const q=query.toLocaleLowerCase().trim();
 return data.items.filter(e=>(kind==='all'||e.kind===kind)&&(status==='all'||e.status===status)&&(!q||[e.label,e.group,e.scope].join(' ').toLocaleLowerCase().includes(q)));
}
export function wireCoverage(data,initialKind='all'){
 const root=document.getElementById('coverage-inventory');
 const get=id=>root.querySelector(`#${id}`);
 const kind=get('coverage-kind');if(['equation','method'].includes(initialKind))kind.value=initialKind;
 const update=()=>{
  const entries=filterCoverage(data,{kind:kind.value,status:get('coverage-status').value,query:get('coverage-search').value});
  get('coverage-count').textContent=`${entries.length} of ${data.items.length} named model and method entries`;
  get('coverage-results').innerHTML=entries.length?[...new Set(entries.map(e=>e.group))].map(group=>`<section class="coverage-group"><h2>${esc(group)}</h2><ul>${entries.filter(e=>e.group===group).map(e=>`<li><div><a href="#/read/${esc(e.chapter)}">${esc(e.label)} <span aria-hidden="true">↗</span></a>${e.scope?`<p>${esc(e.scope)}</p>`:''}</div><span class="coverage-status ${e.status}">${statusLabel(e.status)}</span></li>`).join('')}</ul></section>`).join(''):'<p class="empty-state">No entries match. Try a different term or scope.</p>';
 };
 kind.addEventListener('change',update);get('coverage-status').addEventListener('change',update);get('coverage-search').addEventListener('input',update);update();
}
