/** Preserve locale, chapter, section and search when moving the Pages project. */
export function migrationURL(previousHref, destination) {
  const previous = new URL(previousHref), next = new URL(destination);
  if (next.protocol !== 'https:') throw new Error('The migration destination must use HTTPS');
  next.search = previous.search;
  next.hash = previous.hash;
  return next.href;
}
