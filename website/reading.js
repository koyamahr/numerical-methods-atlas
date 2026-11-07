import { wireBookCovers } from './books.js';

document.querySelector('.mobile-menu')?.addEventListener('click', event => {
  const open = document.querySelector('.site-header').classList.toggle('menu-open');
  event.currentTarget.setAttribute('aria-expanded', String(open));
});
document.querySelector('.skip-link')?.addEventListener('click', event => {
  event.preventDefault(); document.querySelector('main').focus();
});
wireBookCovers(document);
for (const pre of document.querySelectorAll('.prose pre')) {
  const button = document.createElement('button');
  button.className = 'code-copy';
  const japanese = document.documentElement.lang === 'ja';
  button.textContent = japanese ? 'コピー' : 'Copy';
  button.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(pre.querySelector('code').textContent); button.textContent = japanese ? 'コピーしました' : 'Copied'; }
    catch { button.textContent = japanese ? 'コードを選択してコピー' : 'Select code to copy'; }
  });
  pre.append(button);
}
