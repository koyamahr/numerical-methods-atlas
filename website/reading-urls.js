/** Static reading URLs coexist with the atlas's interactive hash routes. */
export function readingURL(base, id, language = 'en', section = '') {
  const url = new URL(`${language === 'ja' ? 'ja' : 'en'}/read/${id ? `${encodeURIComponent(id)}/` : ''}`, base);
  if (section) url.hash = section;
  return url.href;
}

export function rewriteReadingLinks(html, base, language, translatedIDs = []) {
  const translated = new Set(translatedIDs);
  return html.replace(/href="#\/read\/([a-z0-9-]+)(?:\?([^"#]*))?"/g, (_, id, search = '') => {
    const locale = language === 'ja' && translated.has(id) ? 'ja' : 'en';
    const section = new URLSearchParams(search.replaceAll('&amp;', '&')).get('section') || '';
    return `href="${readingURL(base, id, locale, section)}"`;
  });
}
