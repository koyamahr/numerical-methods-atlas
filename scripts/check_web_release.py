"""Check a complete static release without network access or numerical reruns."""
from argparse import ArgumentParser
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, parse_qs
import json,re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'website';DIST=SITE/'dist'
parser=ArgumentParser();parser.add_argument('--output',type=Path)
args=parser.parse_args()
errors=[]

def require(condition,message):
    if not condition:errors.append(message)

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('src','href') and value:self.targets.append(value)

if not (DIST/'content.json').is_file():raise SystemExit('Build website/dist before checking the release')
documents=json.loads((DIST/'content.json').read_text())
expected={p.stem for p in (ROOT/'docs').glob('*.md')}
require(set(documents)==expected,'Built reading-room chapters do not match docs/')
require({p.stem for p in (SITE/'content').glob('*.md')}==expected,'Source reading-room chapters do not match docs/')
for name in sorted(expected):
    require((ROOT/'docs'/f'{name}.md').read_bytes()==(SITE/'content'/f'{name}.md').read_bytes(),f'Unsynced chapter: {name}')
    links=Links();links.feed(documents.get(name,{}).get('html',''))
    for url in links.targets:
        if url.startswith('#/read/'):
            path,_,query=url.partition('?');chapter=unquote(path[len('#/read/'):])
            require(chapter in documents,f'{name}: unknown reading route {url}')
            section=parse_qs(query).get('section',[])
            if section and chapter in documents:
                require(section[0] in {h['id'] for h in documents[chapter]['headings']},f'{name}: unknown section {url}')
        elif not url.startswith(('#','data:','mailto:')) and not urlsplit(url).scheme:
            path=unquote(urlsplit(url).path)
            target=(DIST/path).resolve()
            require(DIST.resolve() in target.parents and target.is_file(),f'{name}: missing or out-of-tree local asset {url}')
for entry in DIST.glob('*.js'):
    for imported in re.findall(r"(?:from\s*|import\s*)['\"](\./[^'\"]+)['\"]",entry.read_text()):
        require((entry.parent/imported).is_file(),f'{entry.name}: missing module {imported}')
refs=json.loads((ROOT/'catalog/references.json').read_text())
require(refs==json.loads((DIST/'references.json').read_text()),'Built reference catalog is stale')
require((ROOT/'references.bib').read_bytes()==(DIST/'assets/references.bib').read_bytes(),'Built BibTeX is stale')
coverage=json.loads((DIST/'coverage.json').read_text())
require(coverage==json.loads((SITE/'content/coverage.json').read_text()),'Built coverage data is stale')
require(coverage['counts']['references']==len(refs),'Coverage reference total differs from the catalog')
require(coverage['counts']['reading_chapters']==len(documents),'Coverage chapter total is stale')
inventory_labels=re.findall(r'^- \[([^\]]+)\]\(', (ROOT/'docs/site-coverage.md').read_text(), flags=re.MULTILINE)
require(sorted(inventory_labels)==sorted(item['label'] for item in coverage['items']),'Static inventory must list each counted item exactly once')
for item in coverage['items']:
    require(item['chapter'] in documents,'Counted entry has no chapter: '+item['id'])
for path,expected_hash in coverage['source_sha256'].items():
    source=ROOT/path
    require(source.is_file() and sha256(source.read_bytes()).hexdigest()==expected_hash,'Coverage source hash mismatch: '+path)
# Localization adds language artifacts, never additional logical chapters or models.
translations=json.loads((ROOT/'catalog/translations.json').read_text())
japanese=json.loads((DIST/'content.ja.json').read_text())
require(documents==json.loads((DIST/'content.en.json').read_text()),'English compatibility payload differs')
translated=set(translations['chapters'])
require(set(japanese)==translated,'Japanese chapter set differs from translation manifest')
require({p.stem for p in (ROOT/'docs/ja').glob('*.md')}==translated,'Japanese source set differs from translation manifest')
for name in sorted(translated):
    source=ROOT/'docs/ja'/f'{name}.md'
    require(source.read_bytes()==(SITE/'content/ja'/f'{name}.md').read_bytes(),f'Unsynced Japanese chapter: {name}')
    require(japanese[name]['locale']=='ja',f'Incorrect Japanese document language: {name}')
    require({h['id'] for h in japanese[name]['headings']}=={h['id'] for h in documents[name]['headings']},f'Cross-language section mismatch: {name}')
    links=Links();links.feed(japanese[name]['html'])
    for url in links.targets:
        if url.startswith('#/read/'):
            path,_,query=url.partition('?');chapter=unquote(path[len('#/read/'):])
            require(chapter in documents,f'{name} (ja): unknown chapter {url}')
            section=parse_qs(query).get('section',[])
            if section and chapter in documents:
                require(section[0] in {h['id'] for h in documents[chapter]['headings']},f'{name} (ja): unknown section {url}')
        elif not url.startswith(('#','data:','mailto:')) and not urlsplit(url).scheme:
            target=(DIST/unquote(urlsplit(url).path)).resolve()
            require(DIST.resolve() in target.parents and target.is_file(),f'{name} (ja): missing local asset {url}')
status=json.loads((DIST/'translation-status.json').read_text())
require(status['total']==len(documents) and status['translated']==len(japanese),'Translation progress count is stale')
require(set(status['chapters'])==set(documents),'Translation progress omits logical chapters')
glossary=json.loads((ROOT/'catalog/glossary.json').read_text())
require(glossary==json.loads((DIST/'glossary.json').read_text()),'Built glossary differs from its source')
messages=json.loads((SITE/'locales/messages.json').read_text())
require(messages==json.loads((DIST/'locales/messages.json').read_text()),'Built language messages are stale')
for term in glossary['terms']:
    require(messages.get('term.'+term['id'])=={key:term[key] for key in ('en','ja')},'Glossary message differs from source: '+term['id'])
site=json.loads((SITE/'site.config.json').read_text())
require(site==json.loads((DIST/'site.json').read_text()),'Built site metadata is stale')
index=(DIST/'index.html').read_text()
require(f'<title>{site["title"]["en"]}</title>' in index,'Incorrect site title')
require(f'<link rel="canonical" href="{site["publicUrl"]}">' in index,'Incorrect canonical URL')
require(f'<meta property="og:url" content="{site["publicUrl"]}">' in index,'Incorrect Open Graph URL')
require('{{SITE_' not in index and '{{BRAND_' not in index,'Unrendered site metadata')
require(site['publicUrl'] in (DIST/'sitemap.xml').read_text(),'Sitemap points to the wrong site')
require(site['publicUrl']+'sitemap.xml' in (DIST/'robots.txt').read_text(),'Robots sitemap points to the wrong site')
for name,document in documents.items():
    require('href="'+site['legacyPublicUrl']+'#/' not in document['html'],f'{name}: legacy site link remains')
    require('href="'+site['publicUrl']+'#/' not in document['html'],f'{name}: same-site link would leave the current language')
legacy=ROOT/'outputs/legacy-redirect'
for filename in ['index.html','404.html','migration.js']:
    require((legacy/filename).is_file(),'Missing legacy landing artifact: '+filename)
require((legacy/'migration.js').read_bytes()==(SITE/'migration.js').read_bytes(),'Legacy migration module is stale')
require(site['publicUrl'] in (legacy/'index.html').read_text(),'Legacy landing points to the wrong site')
if errors:raise SystemExit('\n'.join(errors))
files=sorted(p for p in DIST.rglob('*') if p.is_file())
file_hashes={p.relative_to(DIST).as_posix():sha256(p.read_bytes()).hexdigest() for p in files}
report=dict(scope='Offline static-release check; no external DOI/link verification or numerical reruns.',counts=coverage['counts'],
    localization=dict(japanese_drafts=sum(e['status']=='draft' for e in status['chapters'].values()),japanese_reviewed=status['reviewed'],untranslated=sum(e['status']=='missing' for e in status['chapters'].values()),glossary_terms=len(glossary['terms'])),
    files=len(files),bytes=sum(p.stat().st_size for p in files),
    artifact_sha256=sha256(json.dumps(file_hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest())
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
