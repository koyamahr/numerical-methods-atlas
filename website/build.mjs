import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import katex from 'katex';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
fs.mkdirSync('dist', { recursive: true });
for (const f of ['index.html', 'style.css', 'app.js', 'experiments.js', 'foundations.js', 'hamiltonian.js', 'movies.js', 'limiters.js', 'numerics.js', 'favicon.svg']) fs.copyFileSync(f, `dist/${f}`);
fs.cpSync('public', 'dist', { recursive: true });
fs.mkdirSync('dist/vendor', { recursive: true });
fs.copyFileSync('node_modules/katex/dist/katex.min.css', 'dist/vendor/katex.min.css');
fs.cpSync('node_modules/katex/dist/fonts', 'dist/vendor/fonts', { recursive: true });
const slug = text => text.toLowerCase().replace(/<[^>]*>/g, '').replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s+/g, '-');
const documents = {};
for (const file of fs.readdirSync('content').filter(f => f.endsWith('.md'))) {
  let text = fs.readFileSync(`content/${file}`, 'utf8');
  text = text.replace(/\\\[([\s\S]*?)\\\]/g, (_, equation) => {
    const rendered = katex.renderToString(equation, { displayMode: true, throwOnError: true, strict: 'ignore', output: 'htmlAndMathml' });
    return `\n\n<div class="math-block">${rendered}</div>\n\n`;
  });
  let html = marked.parse(text);
  const headings = [];
  html = html.replace(/<h([23])>(.*?)<\/h\1>/g, (_, level, title) => {
    const id = slug(title);
    headings.push({ level: Number(level), id, title: title.replace(/<[^>]*>/g, '') });
    return `<h${level} id="${id}">${title}<a class="heading-anchor" href="#${id}" aria-label="Link to this section">#</a></h${level}>`;
  });
  html = html.replace(/href="([^"#:]+\.md)(#[^"]*)?"/g, (_, url, fragment = '') => {
    const name = path.basename(url, '.md');
    return `href="${name.toLowerCase() === 'readme' ? '#/' : `#/read/${name}`}${fragment ? `?section=${fragment.slice(1)}` : ''}"`;
  }).replace(/(?:src|href)="figures\//g, match => match.replace('figures/', 'assets/')).replace(/href="(?:\.\.\/)?references\.bib"/g, 'href="assets/references.bib"');
  const title = (html.match(/<h1>(.*?)<\/h1>/) || [])[1] || file;
  documents[path.basename(file, '.md')] = { title, html, headings };
}
fs.writeFileSync('dist/content.json', JSON.stringify(documents));
for (const file of ['references.json', 'sod.json', 'experiments.json', 'advection-reference.json', 'foundations.json', 'hamiltonian.json', 'limiters.json']) fs.copyFileSync(`content/${file}`, `dist/${file}`);
const hosting = JSON.parse(fs.readFileSync('.openai/hosting.json', 'utf8'));
if (hosting.static?.directory !== 'dist') throw new Error('Unexpected Site configuration');
const origin = 'https://koyamahr.github.io/the-art-of-numerical-algorithms';
fs.writeFileSync('dist/robots.txt', `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
fs.writeFileSync('dist/sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc></url></urlset>\n`);
console.log(`Built static web edition with ${Object.keys(documents).length} complete reading chapters.`);
