// Covers are optional: a missing or blocked image must leave a readable book.
const wired = new WeakSet();

export function wireBookCovers(root) {
 for (const frame of root.querySelectorAll('.textbook-cover')) {
  if (wired.has(frame)) continue;
  wired.add(frame);
  const image=frame.querySelector('img');
  if (!image) {frame.dataset.coverState='missing';continue;}
  const update=()=>{frame.dataset.coverState=image.naturalWidth>1?'ready':'missing';};
  image.addEventListener('load',update);
  image.addEventListener('error',()=>{frame.dataset.coverState='missing';});
  // A cached response may finish before the reading chapter is inserted.
  if (image.complete) update();
 }
}
