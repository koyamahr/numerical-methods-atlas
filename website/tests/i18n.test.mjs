import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {configureLocale,resolveLanguage,t,translateText,languageURL,searchText} from '../i18n.js';
import {filterCoverage} from '../coverage.js';
import {filterTerms} from '../glossary.js';
const read = path => JSON.parse(readFileSync(new URL(path,import.meta.url),'utf8'));
const messages=read('../locales/messages.json'), glossary=read('../../catalog/glossary.json');
const coverage=read('../content/coverage.json');
const placeholders=value=>[...value.matchAll(/\{(\w+)\}/g)].map(match=>match[1]).sort();
test('UI translations retain placeholders and unambiguous original strings',()=>{
 const seen=new Map();
 for(const [id,entry] of Object.entries(messages)){
  assert.equal(typeof entry.en,'string',id);assert.equal(typeof entry.ja,'string',id);
  assert.deepEqual(placeholders(entry.en),placeholders(entry.ja),id);
  const key=entry.en.replace(/\s+/g,' ').trim();
  if(seen.has(key))assert.equal(entry.ja,seen.get(key),key);
  seen.set(key,entry.ja);
 }
});
test('language links keep the route, reference query, section and project subpath',()=>{
 assert.equal(resolveLanguage('?lang=ja','en'),'ja');
 assert.equal(resolveLanguage('?lang=en','ja'),'en');
 assert.equal(resolveLanguage('','ja'),'ja');
 assert.equal(resolveLanguage('?lang=xx',null),'en');
 const original='https://example.org/the-art-of-numerical-algorithms/?x=1#/read/stability?section=laxfriedrichs-and-laxwendroff';
 const url=new URL(languageURL(original,'ja'));
 assert.equal(url.pathname,'/the-art-of-numerical-algorithms/');
 assert.equal(url.hash,new URL(original).hash);assert.equal(url.searchParams.get('x'),'1');assert.equal(url.searchParams.get('lang'),'ja');
});
test('presentation localization leaves numerical values, formulas and unknown text intact',()=>{
 configureLocale(messages,'ja');
 assert.equal(t('language.label'),'表示言語');
 assert.equal(translateText('42 of 125 named model and method entries'),'全125項目中42項目');
 assert.equal(translateText('Frame 5 / 26'),'フレーム 5／26');
 assert.equal(translateText('Burgers / shock at physical time 0.125'),'Burgers／衝撃波・物理時刻 0.125');
 assert.equal(translateText(' uₜ + a uₓ = 0 '),' uₜ + a uₓ = 0 ');
 assert.equal(translateText('0.125'),'0.125');
 assert.equal(translateText('Unknown source note'),'Unknown source note');
 assert.match(searchText('Upwind finite differences'),/風上/);
 configureLocale(messages,'en');assert.equal(translateText('Methods'),'Methods');
});
test('Japanese and English inventory search identify the same entries without duplicating counts',()=>{
 configureLocale(messages,'en');
 const en=filterCoverage(coverage,{query:'Upwind finite differences'}),ja=filterCoverage(coverage,{query:'風上差分'});
 assert.deepEqual(ja.map(item=>item.id),en.map(item=>item.id));assert.equal(ja.length,1);
 assert.equal(filterCoverage(coverage).length,coverage.counts.equations+coverage.counts.methods);
 const ids=glossary.terms.map(term=>term.id);assert.equal(new Set(ids).size,ids.length);
 assert.deepEqual(filterTerms(glossary,'Ｎｅｕｍａｎｎ').map(term=>term.id),['concept.von-neumann','concept.neumann']);
 assert.ok(filterTerms(glossary,'風上').length);
 for(const term of glossary.terms)assert.deepEqual(messages['term.'+term.id],{en:term.en,ja:term.ja});
});
