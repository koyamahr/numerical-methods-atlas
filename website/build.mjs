import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const site = JSON.parse(fs.readFileSync('site.config.json', 'utf8'));
const publicURL = new URL(site.publicUrl);
if (publicURL.protocol !== 'https:' || publicURL.pathname !== `/${site.publicationRepository.split('/')[1]}/`) throw new Error('Publication URL and repository do not match');
fs.mkdirSync('dist', { recursive: true });
for (const f of ['index.html', 'style.css', 'app.js', 'i18n.js', 'glossary.js', 'experiments.js', 'foundations.js', 'hamiltonian.js', 'movies.js', 'gallery.js', 'limiters.js', 'runge-kutta.js', 'cip.js', 'basis.js', 'equations.js', 'coverage.js', 'numerics.js', 'favicon.svg']) fs.copyFileSync(f, `dist/${f}`);
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const substitutions = {SITE_TITLE:site.title.en, BRAND_LEAD:site.brand.lead, BRAND_SUBJECT:site.brand.subject, SITE_URL:site.publicUrl, REPOSITORY_URL:site.repositoryUrl, LEGACY_REPOSITORY_URL:site.legacyRepositoryUrl};
let index = fs.readFileSync('index.html', 'utf8');
for (const [key, value] of Object.entries(substitutions)) index = index.replaceAll(`{{${key}}}`, escapeHTML(value));
if (/\{\{[A-Z_]+\}\}/.test(index)) throw new Error('Unresolved site metadata placeholder');
fs.writeFileSync('dist/index.html', index);
fs.writeFileSync('dist/site.json', JSON.stringify(site));
fs.cpSync('public', 'dist', { recursive: true });
fs.cpSync('locales', 'dist/locales', { recursive: true });
fs.copyFileSync('../catalog/glossary.json', 'dist/glossary.json');
fs.mkdirSync('dist/vendor', { recursive: true });
fs.copyFileSync('node_modules/katex/dist/katex.min.css', 'dist/vendor/katex.min.css');
fs.cpSync('node_modules/katex/dist/fonts', 'dist/vendor/fonts', { recursive: true });
const slug = text => text.toLowerCase().replace(/<[^>]*>/g, '').replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s+/g, '-');
const translationManifest = JSON.parse(fs.readFileSync('../catalog/translations.json', 'utf8'));
function renderDocument(text, locale = 'en') {
  text = text.replace(/\\\[([\s\S]*?)\\\]/g, (_, equation) => {
    const rendered = katex.renderToString(equation, { displayMode: true, throwOnError: true, strict: 'ignore', output: 'htmlAndMathml' });
    return `\n\n<div class="math-block">${rendered}</div>\n\n`;
  });
  let html = marked.parse(text);
  const headings = [];
  html = html.replace(/<h([23])>(.*?)<\/h\1>/g, (_, level, rawTitle) => {
    const explicit = rawTitle.match(/\s*\{#([\p{L}\p{N}_-]+)\}$/u);
    if (locale === 'ja' && !explicit) throw new Error(`Japanese heading needs a stable section ID: ${rawTitle}`);
    const title = explicit ? rawTitle.slice(0, explicit.index) : rawTitle;
    const id = explicit ? explicit[1] : slug(title);
    if (headings.some(h => h.id === id)) throw new Error(`Duplicate section ID: ${id}`);
    headings.push({ level: Number(level), id, title: title.replace(/<[^>]*>/g, '') });
    return `<h${level} id="${id}">${title}<a class="heading-anchor" href="#${id}" aria-label="${locale === 'ja' ? 'この節へのリンク' : 'Link to this section'}">#</a></h${level}>`;
  });
  html = html.replace(/href="([^"#:]+\.md)(#[^"]*)?"/g, (_, url, fragment = '') => {
    const name = path.basename(url, '.md');
    return `href="${name.toLowerCase() === 'readme' ? '#/' : `#/read/${name}`}${fragment ? `?section=${fragment.slice(1)}` : ''}"`;
  }).replace(/(?:src|href)="figures\//g, match => match.replace('figures/', 'assets/')).replace(/href="(?:\.\.\/)?references\.bib"/g, 'href="assets/references.bib"');
  for (const base of [site.publicUrl, site.legacyPublicUrl]) html = html.replaceAll(`href="${base}#/`, 'href="#/');
  const title = (html.match(/<h1>(.*?)<\/h1>/) || [])[1];
  return { title, html, headings, locale };
}
const documents = {}, japanese = {}, status = {};
for (const file of fs.readdirSync('content').filter(f => f.endsWith('.md'))) {
  const id = path.basename(file, '.md');
  const text = fs.readFileSync(`content/${file}`, 'utf8');
  documents[id] = renderDocument(text);
  const translation = translationManifest.chapters[id]?.ja;
  status[id] = {status: 'missing', source_sha256: createHash('sha256').update(text).digest('hex')};
  if (!translation) continue;
  const translated = fs.readFileSync(`content/ja/${file}`, 'utf8');
  japanese[id] = renderDocument(translated, 'ja');
  const sourceSections = documents[id].headings.map(h => h.id).sort();
  const translatedSections = japanese[id].headings.map(h => h.id).sort();
  if (JSON.stringify(sourceSections) !== JSON.stringify(translatedSections)) throw new Error(`Translation section mismatch: ${id}`);
  const math = value => value.match(/\\\[[\s\S]*?\\\]/g) || [];
  if (JSON.stringify(math(text)) !== JSON.stringify(math(translated))) throw new Error(`Translation changed display mathematics: ${id}`);
  const externalLinks = html => [...new Set([...html.matchAll(/href="(https?:\/\/[^"]+)"/g)].map(match => match[1]))].sort();
  if (JSON.stringify(externalLinks(documents[id].html)) !== JSON.stringify(externalLinks(japanese[id].html))) throw new Error(`Translation changed external sources: ${id}`);

  if (!['draft','reviewed'].includes(translation.status)) throw new Error(`Unknown translation status: ${id}`);
  const code = value => value.match(/```[\s\S]*?```/g) || [];
  if (JSON.stringify(code(text)) !== JSON.stringify(code(translated))) throw new Error(`Translation changed executable code: ${id}`);
  status[id] = {...translation, status: translation.source_sha256 === status[id].source_sha256 ? translation.status : 'stale'};
  japanese[id].translation_status = status[id].status;
}
for (const id of Object.keys(translationManifest.chapters)) if (!documents[id]) throw new Error(`Unknown translated chapter: ${id}`);
fs.writeFileSync('dist/content.json', JSON.stringify(documents));
fs.writeFileSync('dist/content.en.json', JSON.stringify(documents));
fs.writeFileSync('dist/content.ja.json', JSON.stringify(japanese));
fs.writeFileSync('dist/translation-status.json', JSON.stringify({chapters: status, total: Object.keys(documents).length, translated: Object.keys(japanese).length, reviewed: Object.values(status).filter(s => s.status === 'reviewed').length}));
for (const file of ['references.json', 'sod.json', 'experiments.json', 'advection-reference.json', 'foundations.json', 'hamiltonian.json', 'limiters.json', 'runge-kutta.json', 'cip.json', 'basis.json', 'equation-gallery.json', 'coverage.json']) fs.copyFileSync(`content/${file}`, `dist/${file}`);
const hosting = JSON.parse(fs.readFileSync('.openai/hosting.json', 'utf8'));
if (hosting.static?.directory !== 'dist') throw new Error('Unexpected Site configuration');
const origin = site.publicUrl.replace(/\/$/, '');
fs.writeFileSync('dist/robots.txt', `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
fs.writeFileSync('dist/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc></url></urlset>\n`);
console.log(`Built static web edition with ${Object.keys(documents).length} complete reading chapters.`);

// Keep the old-address landing page separate from the atlas deployment artifact.
const legacyDirectory = path.resolve(root, '../outputs/legacy-redirect');
fs.mkdirSync(legacyDirectory, {recursive:true});
const legacyModule = new URL('migration.js', site.legacyPublicUrl).pathname;
const legacyHTML = `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><link rel="canonical" href="${escapeHTML(site.publicUrl)}"><title>移転のお知らせ · ${escapeHTML(site.title.en)}</title><style>body{max-width:760px;margin:12vh auto;padding:24px;background:#f5f2ea;color:#23392f;font:17px/1.8 system-ui,sans-serif}h1{font-size:30px}a{color:#a34829;overflow-wrap:anywhere}</style></head><body><h1>数値計算法アトラスは移転しました</h1><p lang="en">${escapeHTML(site.title.en)} has moved.</p><p><a href="${escapeHTML(site.publicUrl)}">新しいサイトを開く / Open the atlas →</a></p><p>言語設定と章・節へのリンクを引き継いで移動します。</p><noscript><p>JavaScriptが無効な場合は、上のリンクから移動してください。</p></noscript><script type="module">import {migrationURL} from ${JSON.stringify(legacyModule)}; location.replace(migrationURL(location.href,${JSON.stringify(site.publicUrl)}));</script></body></html>`;
fs.writeFileSync(path.join(legacyDirectory, 'index.html'), legacyHTML);
fs.writeFileSync(path.join(legacyDirectory, '404.html'), legacyHTML);
fs.copyFileSync('migration.js', path.join(legacyDirectory, 'migration.js'));
