"""Audit named coverage and generate one set of promotional counts.

No numerical experiments run here. The registry states its counting unit;
publication identities use DOI first, then normalized author/title/year.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'catalog/coverage.json').read_text())
bio=json.loads((ROOT/'catalog/biological-models.json').read_text())
refs=json.loads((ROOT/'catalog/references.json').read_text())

def identity(e):
    if e.get('doi'):return 'doi:'+e['doi'].strip().lower()
    normalize=lambda s:re.sub(r'\W+','',str(s).casefold())
    return 'work:'+normalize(e['author'])+':'+normalize(e['title'])+':'+str(e['year'])

unique={}
for e in refs:
    key=identity(e)
    if key in unique:raise ValueError('Duplicate publication: '+e['id']+' / '+unique[key]['id'])
    unique[key]=e
items=registry['items']+[dict(kind='equation',id='bio-'+m['id'],label=m['name'],chapter='biological-models',status='reading',group='Biological model survey',scope=m['scope']) for m in bio['models']]
assert len({(e['kind'],e['id']) for e in items})==len(items)
for e in items:
    if not (ROOT/'docs'/(e['chapter']+'.md')).is_file():raise ValueError('Missing chapter: '+e['chapter'])
    if e['status'] not in ('reading','local-example'):raise ValueError('Unrecognized status')
equations=[e for e in items if e['kind']=='equation'];methods=[e for e in items if e['kind']=='method']
types=Counter(e.get('type','article') for e in refs)
cases=json.loads((ROOT/'website/content/equation-gallery.json').read_text())['cases']
counts=dict(equations=len(equations),methods=len(methods),papers=types['article']+types['inproceedings'],references=len(unique),
    journal_articles=types['article'],conference_papers=types['inproceedings'],books=types['book'],chapters=types['incollection'],reports=types['techreport'],other_sources=types['misc'],
    local_equations=sum(e['status']=='local-example' for e in equations),reading_equations=sum(e['status']=='reading' for e in equations),
    local_methods=sum(e['status']=='local-example' for e in methods),reading_methods=sum(e['status']=='reading' for e in methods),
    biological_entries=len(bio['models']),gallery_cases=len(cases),gallery_equations=len({c['equation'] for c in cases}),
    reading_chapters=len({p.name for p in (ROOT/'website/content').glob('*.md')}|{'site-coverage.md'}))
sources=['catalog/coverage.json','catalog/biological-models.json','catalog/references.json','scripts/build_coverage.py']
data=dict(schema_version=1,edition=registry['edition'],counted_on=registry['counted_on'],policy=registry['policy'],counts=counts,items=items,
    publications=[dict(id=e['id'],type=e.get('type','article'),identity=identity(e)) for e in refs],
    source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
(ROOT/'website/content/coverage.json').write_text(text)
(ROOT/'docs/figures/site-coverage.json').write_text(text)
(ROOT/'website/public/assets/site-coverage.json').write_text(text)
lines=['# Site coverage and counting rules','',f"{data['edition']}, counted {data['counted_on']}. These are counts of catalog entries and documented examples, not a claim that every entry is a verified end-to-end solver.",'',
 f"**{counts['equations']} equation/model entries · {counts['methods']} methods and building blocks · {counts['papers']} journal/conference papers · {counts['references']} total sources.**",'',
 f"There are {counts['gallery_cases']} saved-profile equation-gallery cases across {counts['gallery_equations']} equation families, and {counts['reading_chapters']} reading chapters including this inventory.",'',
 '## Equations and models','',registry['policy']['equations'],'',
 f"{counts['local_equations']} entries have scoped local examples; {counts['reading_equations']} are reading-only, including all {counts['biological_entries']} biological survey entries. A coupled system is one entry; its individual component equations do not increase the count. Poisson/Laplace and dimensional variants share entries. Named frameworks and specialized kinetic laws can both appear, so this is not a count of mathematically disjoint families.",'']
for kind,title,entries in [('equation','Equation/model inventory',equations),('method','Numerical method inventory',methods)]:
    lines.extend(['## '+title,''])
    if kind=='method':lines.extend([registry['policy']['methods'],'',f"{counts['local_methods']} entries have scoped local examples; {counts['reading_methods']} are reading-only. Reconstruction limiters, preconditioners and coupling operators are building blocks, not complete PDE solvers. Mesh layouts, CFL conditions and theorems are not counted as numerical methods.",''])
    for group in dict.fromkeys(e['group'] for e in entries):
        lines.extend(['### '+group,''])
        for e in entries:
            if e['group'] != group:continue
            scope=' '+e['scope'] if e['scope'] else ''
            status='Local example' if e['status']=='local-example' else 'Reading only'
            lines.append(f"- [{e['label']}]({e['chapter']}.md) — {status}.{scope}")
        lines.append('')
lines.extend(['## Papers versus all sources','',registry['policy']['papers'],'',registry['policy']['references'],'',
 f"- {counts['journal_articles']} journal-article records, including reviews, translations and explicitly labeled accepted papers.\n- {counts['conference_papers']} conference papers.\n- {counts['books']} books.\n- {counts['chapters']} book chapters.\n- {counts['reports']} technical/teaching reports.\n- {counts['other_sources']} other records, including documentation and a separately identified preprint.",'',
 'A duplicate Cockburn–Shu 1989 record was merged. Burgers 1948 is classified as a book chapter. The former 146-record total included that duplicate; subsequent source additions are reflected in the current unique-work totals above. An original paper and a separately published translation remain separate works. The bibliography does not claim that every full text has been inspected; source notes preserve the inspection status.','',
 '## Reproduction','',
 'The named registry is `catalog/coverage.json`; biological entries and publication types come from their respective catalogs. `python scripts/build_coverage.py` checks unique publication identities and local reading links, then generates the counts and this inventory. The website build runs that audit before rendering. Parameter choices, time frames, repeated equations in prose and test function counts do not increase these totals.','',
 '[Download the counted inventory and source hashes](figures/site-coverage.json). Browse the [reference catalog](references.md), [equation gallery](equation-gallery.md), [biological survey](biological-models.md) or [implementation roadmap](roadmap.md).',''])
chapter='\n'.join(lines)
(ROOT/'docs/site-coverage.md').write_text(chapter)
(ROOT/'website/content/site-coverage.md').write_text(chapter)
print(json.dumps(counts,ensure_ascii=False))
