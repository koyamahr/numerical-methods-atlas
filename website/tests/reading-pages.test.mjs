import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { buildReadingPages } from '../build-reading.mjs';
import { readingURL, rewriteReadingLinks } from '../reading-urls.js';

const base = 'https://koyamahr.github.io/numerical-methods-atlas/';
test('reading links preserve sections, locale and missing-translation fallback', () => {
  assert.equal(readingURL(base, 'stability', 'ja', 'cfl'), `${base}ja/read/stability/#cfl`);
  const html = '<a href="#/read/stability?section=cfl">CFL</a><a href="#/read/english-only">English</a><a href="#/experiments">Experiment</a>';
  assert.equal(rewriteReadingLinks(html, base, 'ja', ['stability']), `<a href="${base}ja/read/stability/#cfl">CFL</a><a href="${base}en/read/english-only/">English</a><a href="#/experiments">Experiment</a>`);
});

test('static chapters contain the full text, localized metadata and reciprocal alternatives', t => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'atlas-reading-'));
  t.after(() => fs.rmSync(directory, {recursive:true,force:true}));
  const site = { publicUrl:base, repositoryUrl:'https://github.com/koyamahr/numerical-methods-atlas', title:{en:'An Atlas of Numerical Methods',ja:'数値計算法アトラス'} };
  const doc = {title:'Stability & error',html:'<h1>Stability &amp; error</h1><p>Follow the CFL condition.</p><h2 id="cfl">CFL</h2><img src="assets/stability.png"><a href="#/read/english-only">Next</a><a href="#/experiments">Run</a>',headings:[{level:2,id:'cfl',title:'CFL'}],locale:'en'};
  const japanese = {title:'安定性と誤差',html:'<h1>安定性と誤差</h1><p>CFL条件を学ぶ。</p>',headings:[],locale:'ja',translation_status:'draft'};
  const pages = buildReadingPages({directory,site,documents:{stability:doc,'english-only':doc},japanese:{stability:japanese}});
  assert.equal(pages.length,5);
  const english = fs.readFileSync(path.join(directory,'en/read/stability/index.html'),'utf8');
  const translated = fs.readFileSync(path.join(directory,'ja/read/stability/index.html'),'utf8');
  for (const [language, html] of [['en',english],['ja',translated]]) {
    assert(html.includes(`<html lang="${language}">`));
    assert(html.includes(`<link rel="canonical" href="${base}${language}/read/stability/">`));
    for (const alternate of ['en','ja']) assert(html.includes(`hreflang="${alternate}" href="${base}${alternate}/read/stability/"`));
    assert(!html.includes('src="app.js"'), 'Static text does not depend on the SPA');
  }
  assert(english.includes(doc.html.split('<img')[0]));
  assert(english.includes('href="#cfl"'), 'Native in-page anchors stay on the chapter');
  assert(english.includes('src="/numerical-methods-atlas/assets/stability.png"'));
  assert(english.includes('href="/numerical-methods-atlas/?lang=en#/experiments"'));
  const fallback = fs.readFileSync(path.join(directory,'en/read/english-only/index.html'),'utf8');
  assert(!fallback.includes('hreflang="ja"'));
  assert(!fs.existsSync(path.join(directory,'ja/read/english-only/index.html')));
});
