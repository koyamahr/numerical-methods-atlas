import {currentLanguage, translateText} from './i18n.js';
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function filterTerms(data, query = '') {
  const q = query.normalize('NFKC').toLocaleLowerCase().trim();
  return data.terms.filter(term => [term.en, term.ja, ...(term.aliases || [])].join(' ').normalize('NFKC').toLocaleLowerCase().includes(q));
}
export function glossaryPage() {
  const ja = currentLanguage() === 'ja';
  return `<section class="page-intro page-width"><p class="eyebrow">${ja?'日本語と英語をつなぐ':'CONNECT THE TERMINOLOGY'}</p><h1>${ja?'日英用語集':'Bilingual glossary'}</h1><p>${ja?'方程式・計算法・主要概念を日英で検索できます。用語の収録数は、モデル数・計算法数とは別の指標です。':'Search equations, methods and key concepts in Japanese or English. The glossary is separate from the counted model and method inventory.'}</p><label for="glossary-search">${ja?'用語を検索':'Find a term'}</label><input id="glossary-search" class="glossary-search" type="search" placeholder="風上 / upwind / CT / Neumann"><p id="glossary-count" aria-live="polite"></p><div id="glossary-results"></div></section>`;
}
export function wireGlossary(data, query = '') {
  const input = document.getElementById('glossary-search'); input.value = query;
  const update = () => {
    const terms = filterTerms(data, input.value), ja = currentLanguage() === 'ja';
    document.getElementById('glossary-count').textContent = ja ? `${data.terms.length}語中${terms.length}語` : `${terms.length} of ${data.terms.length} terms`;
    document.getElementById('glossary-results').innerHTML = terms.length ? `<dl class="glossary-list">${terms.map(term => `<div><dt lang="ja" data-original>${esc(term.ja)}</dt><dd lang="en" data-original>${esc(term.en)}</dd>${term.chapter?`<dd><a href="#/read/${esc(term.chapter)}">${ja?'解説へ':'Read the chapter'} ↗</a></dd>`:''}</div>`).join('')}</dl>` : `<p>${ja?'該当する用語がありません。':'No terms match.'}</p>`;
  };
  input.addEventListener('input', update);update();
}
