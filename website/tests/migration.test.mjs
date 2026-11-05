import test from 'node:test';
import assert from 'node:assert/strict';
import {migrationURL} from '../migration.js';

test('legacy Pages migration retains locale, chapter, section and encoded search',()=>{
 const destination='https://koyamahr.github.io/numerical-methods-atlas/';
 for(const suffix of ['','?lang=ja#/read/stability?section=laxfriedrichs-and-laxwendroff','?lang=en&x=a%20b#/references?q=Roe%20entropy','?lang=ja#/coverage?kind=method']){
  const previous=new URL('https://koyamahr.github.io/the-art-of-numerical-algorithms/'+suffix);
  const next=new URL(migrationURL(previous.href,destination));
  assert.equal(next.origin+next.pathname,destination);
  assert.equal(next.search,previous.search);assert.equal(next.hash,previous.hash);
 }
});

test('migration also handles legacy 404 paths and requires HTTPS',()=>{
 assert.equal(migrationURL('https://koyamahr.github.io/the-art-of-numerical-algorithms/unknown?lang=ja#/equations','https://koyamahr.github.io/numerical-methods-atlas/'),'https://koyamahr.github.io/numerical-methods-atlas/?lang=ja#/equations');
 assert.throws(()=>migrationURL('https://example.org/','javascript:alert(1)'),/HTTPS/);
});
