import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
fs.mkdirSync('dist', { recursive: true });
for (const f of ['index.html', 'style.css', 'app.js', 'i18n.js', 'glossary.js', 'experiments.js', 'foundations.js', 'hamiltonian.js', 'movies.js', 'limiters.js', 'runge-kutta.js', 'cip.js', 'equations.js', 'coverage.js', 'numerics.js', 'favicon.svg']) fs.copyFileSync(f, `dist/${f}`);
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
    const explicit = rawTitle.match(/\s*\{#([a-zA-Z0-9_-]+)\}$/);
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
for (const file of ['references.json', 'sod.json', 'experiments.json', 'advection-reference.json', 'foundations.json', 'hamiltonian.json', 'limiters.json', 'runge-kutta.json', 'cip.json', 'equation-gallery.json', 'coverage.json']) fs.copyFileSync(`content/${file}`, `dist/${file}`);
const hosting = JSON.parse(fs.readFileSync('.openai/hosting.json', 'utf8'));
if (hosting.static?.directory !== 'dist') throw new Error('Unexpected Site configuration');
const origin = 'https://koyamahr.github.io/the-art-of-numerical-algorithms';
fs.writeFileSync('dist/robots.txt', `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
fs.writeFileSync('dist/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc></url></urlset>\n`);
console.log(`Built static web edition with ${Object.keys(documents).length} complete reading chapters.`);
