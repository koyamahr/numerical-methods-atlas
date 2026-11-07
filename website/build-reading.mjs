import fs from 'node:fs';
import path from 'node:path';
import { readingURL, rewriteReadingLinks } from './reading-urls.js';

const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const plain = html => html.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/\s+/g, ' ').trim();

export function buildReadingPages({ directory, site, documents, japanese }) {
  const translations = Object.keys(japanese);
  const prefix = new URL(site.publicUrl).pathname;
  const home = language => `${prefix}?lang=${language}`;
  const route = (name, language) => `${home(language)}#/${name}`;
  const urls = [];

  function link(id, language) {
    return readingURL(site.publicUrl, id, language === 'ja' && !japanese[id] ? 'en' : language);
  }
  function render(id, language) {
    const entries = language === 'ja' ? japanese : documents;
    const doc = entries[id];
    const index = !id;
    const title = index ? (language === 'ja' ? '解説章の目次' : 'Reading chapters') : plain(doc.title);
    const description = index ? (language === 'ja' ? '数値計算法アトラスの解説章。安定性、保存則、衝撃波、楕円型方程式、時間積分を原論文と再現可能な計算から学ぶ。' : 'Read the numerical methods atlas: stability, conservation laws, shock waves, elliptic equations and time integration, with original sources and reproducible calculations.') : plain(doc.html.match(/<p>([\s\S]*?)<\/p>/)?.[1] || doc.title).slice(0, language === 'ja' ? 160 : 260);
    const canonical = readingURL(site.publicUrl, id, language);
    const alternatives = ['en', ...(index || japanese[id] ? ['ja'] : [])];
    const navigation = Object.entries(entries).map(([key, entry]) => `<a href="${link(key, language)}"${key === id ? ' aria-current="page"' : ''}>${plain(entry.title)}</a>`).join('');
    const body = index ? `<article class="prose"><h1>${title}</h1><p>${description}</p><ul>${Object.entries(entries).map(([key, entry]) => `<li><a href="${link(key, language)}">${entry.title}</a></li>`).join('')}</ul></article>` : `<div class="chapter-topline"><span>${language === 'ja' ? '解説章' : 'THE READING ROOM'}</span><a href="${site.repositoryUrl}/blob/main/docs/${language === 'ja' ? 'ja/' : ''}${id}.md">${language === 'ja' ? 'ソースを見る' : 'View source'} ↗</a></div>${language === 'ja' ? `<p class="translation-notice">${doc.translation_status === 'stale' ? '英語原文が更新されています。この日本語訳は旧版に対応します。' : '日本語訳はドラフトです。数式・計算・参照資料は英語原文と照合できます。'}</p>` : ''}<article class="prose" lang="${language}">${doc.html}</article>`;
    let html = `<!doctype html><html lang="${language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} · ${escape(site.title[language])}</title><meta name="description" content="${escape(description)}"><link rel="canonical" href="${canonical}">${alternatives.map(lang => `<link rel="alternate" hreflang="${lang}" href="${readingURL(site.publicUrl, id, lang)}">`).join('')}<meta property="og:title" content="${escape(title)} · ${escape(site.title[language])}"><meta property="og:description" content="${escape(description)}"><meta property="og:url" content="${canonical}"><meta property="og:type" content="article"><link rel="icon" href="${prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="${prefix}vendor/katex.min.css"><link rel="stylesheet" href="${prefix}style.css"><script type="module" src="${prefix}reading.js"></script></head><body><a class="skip-link" href="#main">${language === 'ja' ? '本文へ' : 'Skip to content'}</a><header class="site-header"><a class="brand" href="${home(language)}"><span class="brand-symbol" aria-hidden="true">∑</span><span>${site.title[language]}</span></a><button class="mobile-menu" aria-label="${language === 'ja' ? 'ナビゲーションを開く' : 'Open navigation'}" aria-expanded="false">Menu</button><nav aria-label="${language === 'ja' ? 'メインナビゲーション' : 'Main navigation'}"><a href="${route('methods', language)}">${language === 'ja' ? '数値計算法' : 'Methods'}</a><a href="${route('experiments', language)}">${language === 'ja' ? '数値実験' : 'Experiments'}</a><a href="${readingURL(site.publicUrl, '', language)}">${language === 'ja' ? '解説章の目次' : 'Reading chapters'}</a></nav><div class="language-switch" role="group" aria-label="Language">${alternatives.map(lang => `<a href="${readingURL(site.publicUrl, id, lang)}" lang="${lang}" hreflang="${lang}"${lang === language ? ' aria-current="page"' : ''}>${lang === 'ja' ? '日本語' : 'English'}</a>`).join('')}</div></header><main id="main" tabindex="-1"><div class="reading-shell page-width"><aside class="reading-nav"><a class="back-link" href="${readingURL(site.publicUrl, '', language)}">← ${language === 'ja' ? '解説章の目次' : 'Reading chapters'}</a><p class="eyebrow">${language === 'ja' ? '各章へ' : 'IN THIS EDITION'}</p><nav aria-label="${language === 'ja' ? '解説章' : 'Reading chapters'}">${navigation}</nav></aside><div class="chapter-wrap">${body}<div class="chapter-bottom"><a href="${route('atlas', language)}">${language === 'ja' ? '歴史アトラス' : 'Historical atlas'} →</a><a href="${route('gallery', language)}">${language === 'ja' ? '計算結果のギャラリー' : 'Computed gallery'} →</a></div></div><aside class="chapter-toc"><p class="eyebrow">${language === 'ja' ? 'このページの内容' : 'ON THIS PAGE'}</p><nav aria-label="${language === 'ja' ? 'このページの内容' : 'On this page'}">${(doc?.headings || []).filter(h => h.level === 2).map(h => `<a href="#${escape(h.id)}">${escape(h.title)}</a>`).join('')}</nav></aside></div></main><footer class="site-footer"><a href="${home(language)}">${site.title[language]}</a><a href="${site.repositoryUrl}">GitHub ↗</a></footer></body></html>`;
    html = rewriteReadingLinks(html, site.publicUrl, language, translations)
      .replace(/href="#\/([^"]*)"/g, (_, name) => `href="${route(name, language)}"`)
      .replace(/(src|href)="((?:assets|vendor)\/[^"\s]*)"/g, (_, attribute, asset) => `${attribute}="${prefix}${asset}"`);
    // Keep navigation on the current origin; search metadata stays absolute.
    html = html.replace(/(<body>)([\s\S]*)(<\/body>)/, (_, start, body, end) => start + body.replaceAll(`href="${site.publicUrl}`, `href="${prefix}`) + end);
    const destination = path.join(directory, language, 'read', id || '', 'index.html');
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, html);
    urls.push({ url: canonical, alternatives: alternatives.map(lang => ({ lang, url: readingURL(site.publicUrl, id, lang) })) });
  }
  for (const language of ['en', 'ja']) {
    render('', language);
    for (const id of Object.keys(language === 'ja' ? japanese : documents)) render(id, language);
  }
  return urls;
}
