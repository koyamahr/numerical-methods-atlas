/** Presentation-only localization. Numerical kernels and saved arrays stay shared. */
let language = 'en';
let messages = {};
let exact = new Map(), patterns = [];
const normalize = value => String(value).replace(/\s+/g, ' ').trim();
const escapePattern = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export function resolveLanguage(search = '', saved = null) {
  const requested = new URLSearchParams(search).get('lang');
  return ['en', 'ja'].includes(requested) ? requested : ['en', 'ja'].includes(saved) ? saved : 'en';
}
export function configureLocale(catalog, locale) {
  messages = catalog;
  language = locale === 'ja' ? 'ja' : 'en';
  exact = new Map(); patterns = [];
  for (const [id, entry] of Object.entries(catalog)) {
    const source = normalize(entry.en);
    if (!source.includes('{')) exact.set(source, id);
    else {
      const keys = [], chunks = source.split(/(\{\w+\})/g);
      const expression = chunks.map(chunk => /^\{\w+\}$/.test(chunk) ? (keys.push(chunk.slice(1, -1)), '(.+?)') : escapePattern(chunk)).join('');
      patterns.push({id, keys, pattern: new RegExp('^' + expression + '$')});
    }
  }
}
export const currentLanguage = () => language;
export function t(id, values = {}) {
  const entry = messages[id];
  if (!entry) throw new Error(`Unknown translation key: ${id}`);
  return (entry[language] ?? entry.en).replace(/\{(\w+)\}/g, (match, key) => values[key] === undefined ? match : String(values[key]));
}
export function searchText(value) {
  const source = normalize(value), id = exact.get(source);
  return id ? `${source} ${messages[id].ja}` : source;
}
/** Compatibility bridge for existing text nodes; never inserts translated HTML. */
export function translateText(value) {
  if (language !== 'ja' || !String(value).trim()) return value;
  const source = normalize(value), id = exact.get(source);
  let translated;
  if (id) translated = t(id);
  else for (const entry of patterns) {
    const match = source.match(entry.pattern);
    if (match) {
      translated = t(entry.id, Object.fromEntries(entry.keys.map((key, i) => [key, translateText(match[i + 1])])));
      break;
    }
  }
  if (translated === undefined) return value;
  const leading = String(value).match(/^\s*/)[0], trailing = String(value).match(/\s*$/)[0];
  return leading + translated + trailing;
}
export function languageURL(href, locale) {
  const url = new URL(href); url.searchParams.set('lang', locale === 'ja' ? 'ja' : 'en'); return url.href;
}

const excluded = 'pre,code,script,style,.katex,.prose,[data-original],[data-localize="false"]';
const attributes = ['aria-label', 'placeholder', 'alt', 'title'];
export function localizeTree(root) {
  if (language !== 'ja' || !root) return;
  const visit = node => {
    if (node.nodeType === 3) {
      if (node.parentElement?.closest(excluded)) return;
      const translated = translateText(node.nodeValue);
      if (node.nodeValue !== translated) node.nodeValue = translated;
      return;
    }
    if (node.nodeType !== 1 && node.nodeType !== 9) return;
    if (node.nodeType === 1) {
      if (node.closest(excluded)) return;
      for (const attr of attributes) if (node.hasAttribute(attr)) {
        const source = node.getAttribute(attr), translated = translateText(source);
        if (source !== translated) node.setAttribute(attr, translated);
      }
    }
    for (const child of node.childNodes) visit(child);
  };
  visit(root);
}
export function observeLocalization(root) {
  const observer = new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'childList') for (const node of record.addedNodes) localizeTree(node);
      else localizeTree(record.target);
    }
  });
  observer.observe(root, {subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: attributes});
  localizeTree(root);
  return () => observer.disconnect();
}

export function captureControls(root) {
  return [...root.querySelectorAll('input[id],select[id],textarea[id]')].map(element => ({id: element.id, value: element.value, checked: element.checked}));
}
export function restoreControls(root, state) {
  // Restore selectors before their dependent sliders; each update rebuilds derived output.
  for (const item of state) {
    const element = root.querySelector(`[id="${item.id}"]`);
    if (!element) continue;
    element.value = item.value;
    if (typeof item.checked === 'boolean') element.checked = item.checked;
    element.dispatchEvent(new Event('input', {bubbles: true}));
    element.dispatchEvent(new Event('change', {bubbles: true}));
  }
}
