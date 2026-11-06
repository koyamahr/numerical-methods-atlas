"""Prepare publishing inputs without rerunning numerical experiments.

Catalogs and docs are authoritative. Numerical profiles/figures are copied
from saved artifacts; their builders remain explicit research commands.
"""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'website'


def generate(script):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)


def copy_changed(source,target):
    if not source.is_file():raise FileNotFoundError(source)
    target.parent.mkdir(parents=True,exist_ok=True)
    data=source.read_bytes()
    if not target.is_file() or target.read_bytes()!=data:
        target.write_bytes(data)


generate('build_references.py')
generate('build_biology_survey.py')
for source in sorted((ROOT/'docs').glob('*.md')):
    copy_changed(source,SITE/'content'/source.name)
copy_changed(ROOT/'catalog/references.json',SITE/'content/references.json')
copy_changed(ROOT/'references.bib',SITE/'public/assets/references.bib')
for source in sorted((ROOT/'docs/figures').glob('*.png')):
    copy_changed(source,SITE/'public/assets'/source.name)
for name in ('limiters.json','runge-kutta.json','cip.json','basis.json','hamiltonian.json','equation-gallery.json'):
    copy_changed(ROOT/'docs/figures'/name,SITE/'content'/name)
for name in ('validation.json','double-mach-run.json','double-mach.npz',
             'hamiltonian.json','particle-gravity.json','gravity-boundaries.json',
             'keep-vortex.json','equation-gallery.json','solver-foundations.json',
             'biological-models.json','geophysical-grids.json'):
    copy_changed(ROOT/'docs/figures'/name,SITE/'public/assets'/name)
generate('build_coverage.py')
generate('build_japanese_catalogs.py')
for source in sorted((ROOT/'docs/ja').glob('*.md')):
    copy_changed(source,SITE/'content/ja'/source.name)
expected={p.name for p in (ROOT/'docs').glob('*.md')}
actual={p.name for p in (SITE/'content').glob('*.md')}
if expected!=actual:
    raise ValueError('Reading-room chapter mismatch: '+repr(expected^actual))
print('Prepared source chapters, catalog and saved artifacts; no numerical runs executed.')
