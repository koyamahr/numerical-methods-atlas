"""Export the English edition and computed Sod curves to the static website."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart import get_problem, solve

site = ROOT / 'website'
content = site / 'content'
assets = site / 'public' / 'assets'
content.mkdir(parents=True, exist_ok=True)
assets.mkdir(parents=True, exist_ok=True)
for source in (ROOT / 'docs').glob('*.md'):
    shutil.copyfile(source, content / source.name)
shutil.copyfile(ROOT / 'catalog/references.json', content / 'references.json')
shutil.copyfile(ROOT / 'references.bib', assets / 'references.bib')
for source in (ROOT / 'docs/figures').glob('*.png'):
    shutil.copyfile(source, assets / source.name)
shutil.copyfile(ROOT / 'docs/figures/validation.json', assets / 'validation.json')
problem = get_problem('sod')
curves = {}
for flux in ('roe', 'hllc', 'hll', 'rusanov'):
    result = solve(problem, n=200, method='muscl', riemann=flux)
    curves[flux] = result.q[:, 0].tolist()
reference = problem.reference(result.x, result.time)
data = {'x': result.x.tolist(), 'exact': reference[:, 0].tolist(), 'curves': curves,
        'n': 200, 'time': result.time, 'method': 'primitive minmod MUSCL + SSPRK3',
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (ROOT / 'numart').glob('*.py')}}
(content / 'sod.json').write_text(json.dumps(data, separators=(',', ':'))+'\n')
print('Synced English documents, 39 references, figures, and four computed Sod curves.')
