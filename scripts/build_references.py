"""Render the single bibliographic catalog to Markdown and BibTeX (stdlib only)."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
entries=sorted(json.loads((ROOT/"catalog/references.json").read_text()),key=lambda e:(e["year"],e["id"]))
if len({e["id"] for e in entries})!=len(entries):
    raise ValueError("Duplicate citation key")
md=["# 参考文献（原著の刊行年順）","",
    "原論文・書籍の書誌と、実装の照合に使う資料を区別します。DOIが付いていても本文全体の精読・原図再現が完了したという意味ではありません。",
    "公開本文の有無、後年の解説を使った項目、原報未確認は各項目の注記に残します。NASAのケース資料は [別一覧](nasa-2d.md) にまとめています。",
    "",
    "このファイルと `references.bib` は `python scripts/build_references.py` で `catalog/references.json` から生成します。", ""]
bib=[]
allowed=("author","title","year","journal","volume","pages","publisher","institution","number","booktitle","edition","doi")
for e in entries:
    link="https://doi.org/"+e["doi"] if e.get("doi") else e["source"]
    md.extend([f"## {e['year']} · {e['id']}","",f"{e['author']}. **{e['title']}**. {e.get('journal',e.get('publisher',e.get('institution',e.get('booktitle',''))))}.","",f"[原著の書誌]({link}) · [本文または実装参照資料]({e['source']})", "",e["note"],""])
    fields=[f"  {k} = {{{e[k]}}}" for k in allowed if k in e]
    fields.extend([f"  url = {{{e['source']}}}",f"  note = {{{e['note']}}}"])
    bib.append("@"+e.get("type","article")+"{"+e["id"]+",\n"+",\n".join(fields)+"\n}")
(ROOT/"docs/references.md").write_text("\n".join(md),encoding="utf-8")
(ROOT/"references.bib").write_text("\n\n".join(bib)+"\n",encoding="utf-8")
print(f"Rendered {len(entries)} references")
