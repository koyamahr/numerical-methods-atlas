"""Render the bilingual textbook reading guide from shared bibliographic IDs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
refs = {r['id']: r for r in json.loads((ROOT/'catalog/references.json').read_text())}
guide = json.loads((ROOT/'catalog/textbooks.json').read_text())
introductions = {
    'en': ['# Textbooks: where to look next',
           'A working bookshelf for this atlas. Choose a book by the question you need to answer; this is a reading guide, not a ranking. Bibliographic years below identify the cited editions, not the invention dates of algorithms.',
           'The links lead to publisher records or author-maintained pages. We checked edition metadata and available descriptions or contents, not every derivation in every book. Chapter suggestions describe the atlas connection; they do not claim that all of a textbook has been implemented.',
           '**A short starting path:** Hirsch for the CFD framework; LeVeque for conservation laws and finite-volume reasoning; Toro for Riemann solvers; Patankar for pressure–velocity coupling; Saad for sparse iterative solves. Return to original papers when tracing a particular algorithm.',
           '[Search the full reference library](#/references) · [All cataloged books](#/references?q=type%3Abook) · [Download BibTeX](../references.bib)'],
    'ja': ['# 教科書案内：次に何を調べるか',
           'このアトラスから参照するための書棚です。知りたい問いから選ぶ読書案内で、順位付けではありません。以下の年は引用する版の年であり、アルゴリズムの発明年ではありません。',
           'リンク先は出版社の書誌情報や著者管理のページです。版情報と公開されている紹介・目次を確認しており、各書のすべての導出を点検したという意味ではありません。関連章はアトラスとの接点を示し、教科書全体の実装を意味しません。',
           '**最初の道筋：** CFDの枠組みにはHirsch、保存則と有限体積法の考え方にはLeVeque、RiemannソルバーにはToro、圧力・速度連成にはPatankar、疎行列の反復解法にはSaad。個々の手法の由来を追うときは原論文にも戻ってください。',
           '[参考文献庫を検索](#/references) · [登録済みの書籍のみ](#/references?q=type%3Abook) · [BibTeXをダウンロード](../references.bib)'],
}
seen = set()
for group in guide['groups']:
    for item in group['books']:
        key = item['reference']
        if key in seen or refs[key].get('type') != 'book':
            raise ValueError('Duplicate or non-book guide entry: '+key)
        seen.add(key)
        for chapter in item['chapters']:
            if not (ROOT/'docs'/f'{chapter}.md').is_file():
                raise ValueError('Unknown linked chapter: '+chapter)
for locale in ('en','ja'):
    lines = introductions[locale].copy()
    for group in guide['groups']:
        lines.append('## '+group['title'][locale]+' {#'+group['id']+'}')
        for item in group['books']:
            r = refs[item['reference']]
            lines.append('### '+item['label']+' {#'+r['id']+'}')
            edition = (f" · edition {r['edition']}" if locale=='en' else f"・第{r['edition']}版") if r.get('edition') else ''
            author = r['author'].replace(' and ', '; ').rstrip('.')
            lines.append(f"{author}. **{r['title']}**. {r['publisher']}, {r['year']}{edition}.")
            lines.append(item['purpose'][locale])
            links = []
            for chapter in item['chapters']:
                chapter_path = ROOT/'docs'/('ja/' if locale=='ja' else '')/f'{chapter}.md'
                if not chapter_path.is_file():
                    chapter_path = ROOT/'docs'/f'{chapter}.md'
                title = chapter_path.read_text().splitlines()[0].removeprefix('# ')
                links.append(f'[{title}]({chapter}.md)')
            links = ' · '.join(links)
            lines.append(('Atlas connections: ' if locale=='en' else 'アトラスの関連章：')+links+'.')
            source = 'https://doi.org/'+r['doi'] if r.get('doi') else r['source']
            lines.append(f"[{'Publisher / bibliographic record' if locale=='en' else '出版社・書誌情報'}]({source}) · [{'Author / source page' if locale=='en' else '著者・参照ページ'}]({r['source']}) · `{r['id']}`")
    path = ROOT/'docs'/('ja/' if locale=='ja' else '')/'textbooks.md'
    path.write_text('\n\n'.join(lines)+'\n')
print(f'Rendered {len(seen)} selected textbooks in English and Japanese.')
