"""Render the single bibliographic catalog to Markdown and BibTeX (stdlib only)."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
entries=sorted(json.loads((ROOT/"catalog/references.json").read_text()),key=lambda e:(e["year"],e["id"]))
if len({e["id"] for e in entries})!=len(entries):
    raise ValueError("Duplicate citation key")
md=["# References by original publication year","",
    "Original papers and books are distinguished from sources used to check the implementations. A DOI does not imply that the full text has been inspected or its figures reproduced.",
    "Each note identifies publicly available originals, later expositions, and original sources that still need verification. NASA case resources appear in the [2D case catalog](nasa-2d.md).",
    "",
    "This file and `references.bib` are generated from `catalog/references.json` by `python scripts/build_references.py`.", ""]
bib=[]
allowed=("author","title","year","journal","volume","pages","publisher","institution","number","booktitle","edition","doi")
for e in entries:
    link="https://doi.org/"+e["doi"] if e.get("doi") else e["source"]
    md.extend([f"## {e['year']} · {e['id']}","",f"{e['author']}. **{e['title']}**. {e.get('journal',e.get('publisher',e.get('institution',e.get('booktitle',''))))}.","",f"[Original bibliographic record]({link}) · [Full text or implementation reference]({e['source']})", "",e["note"],""])
    fields=[f"  {k} = {{{e[k]}}}" for k in allowed if k in e]
    fields.extend([f"  url = {{{e['source']}}}",f"  note = {{{e['note']}}}"])
    bib.append("@"+e.get("type","article")+"{"+e["id"]+",\n"+",\n".join(fields)+"\n}")
(ROOT/"docs/references.md").write_text("\n".join(md),encoding="utf-8")
(ROOT/"references.bib").write_text("\n\n".join(bib)+"\n",encoding="utf-8")
print(f"Rendered {len(entries)} references")
