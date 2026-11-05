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

# Cross-language reference cases for the browser's live advection laboratory.
import numpy as np
from numart.advection import amplification, difference_step
n = 32
x = (np.arange(n)+.5)/n
initial = np.sin(2*np.pi*x)+.001*(np.sin(2*np.pi*(n/2)*x)+np.cos(2*np.pi*(n/4)*x))
theta = np.linspace(0,np.pi,17)
cases = []
for method in ('ftcs','upwind','lax-friedrichs','lax-wendroff'):
    for courant in (-1.2,-.8,0.,.3,.8,1.2):
        values = initial.copy()
        for _ in range(12):
            values = difference_step(values,courant,method)
        growth = amplification(theta,courant,method)
        cases.append({'method':method,'courant':courant,'steps':12,
                      'expected':values.tolist(),
                      'amplification_real':growth.real.tolist(),
                      'amplification_imag':growth.imag.tolist()})
fixture = {'n':n,'initial':initial.tolist(),'theta':theta.tolist(),'cases':cases,
           'source_sha256':hashlib.sha256((ROOT/'numart/advection.py').read_bytes()).hexdigest()}
(content/'advection-reference.json').write_text(json.dumps(fixture,separators=(',',':'))+'\n')
original = json.loads((ROOT/'docs/figures/validation.json').read_text())
metrics = original['metrics']
experiments = {
    'advection_reference_sha256':fixture['source_sha256'],
    'dg':{'n':[8,16,32,64],'time':.2,'cfl':.2,
          'norm':'Quadrature-sampled RMS error',
          'series':[{'label':f'DG P{p}','degree':p,'expected_order':p+1,
                     'errors':metrics[f'dg_p{p}_errors']} for p in (0,1,2)]},
    'entropy':{'n':[40,80,160],'time':1.,'cfl':.3,'norm':'Pointwise density L1 error',
               'series':[{'label':'MUSCL','errors':metrics['entropy_muscl_density_L1'],
                          'expected_order':2},
                         {'label':'WENO5-JS','errors':metrics['entropy_weno5_density_L1'],
                          'expected_order':5}]},
    'gallery_manifest':'assets/validation.json',
    'gallery_source_sha256':original['source_sha256'],
    'scope':'Existing gallery measurements; no wall-clock or equal-cost ranking.'}
(content/'experiments.json').write_text(json.dumps(experiments,indent=2)+'\n')
print(f'Exported {len(cases)} Python advection reference cases and two convergence studies.')
