"""Render the bilingual textbook reading guide from shared bibliographic IDs."""
import html
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
           '[Search the full reference library](#/references) · [All cataloged books](#/references?q=type%3Abook) · [Download BibTeX](../references.bib)',
           'Covers are supplied by [Open Library](https://openlibrary.org/dev/docs/api/covers) for the listed ISBN. Each card links to Amazon Japan and the publisher or bibliographic record. The title stays visible when a cover is unavailable.'],
    'ja': ['# 教科書案内：次に何を調べるか',
           'このアトラスから参照するための書棚です。知りたい問いから選ぶ読書案内で、順位付けではありません。以下の年は引用する版の年であり、アルゴリズムの発明年ではありません。',
           'リンク先は出版社の書誌情報や著者管理のページです。版情報と公開されている紹介・目次を確認しており、各書のすべての導出を点検したという意味ではありません。関連章はアトラスとの接点を示し、教科書全体の実装を意味しません。',
           '**最初の道筋：** CFDの枠組みにはHirsch、保存則と有限体積法の考え方にはLeVeque、RiemannソルバーにはToro、圧力・速度連成にはPatankar、疎行列の反復解法にはSaad。個々の手法の由来を追うときは原論文にも戻ってください。',
           '[参考文献庫を検索](#/references) · [登録済みの書籍のみ](#/references?q=type%3Abook) · [BibTeXをダウンロード](../references.bib)',
           '表紙は記載したISBNに対応する[Open Library](https://openlibrary.org/dev/docs/api/covers)の画像を表示します。各カードにAmazon Japanと出版社・書誌情報へのリンクがあります。表紙を取得できない場合も書名を表示します。'],
}


def amazon_url(isbn):
    if len(isbn) != 13 or not isbn.isdigit() or sum(int(c)*(1 if i % 2 == 0 else 3) for i,c in enumerate(isbn)) % 10:
        raise ValueError('Invalid ISBN-13: '+isbn)
    if not isbn.startswith('978'):
        return 'https://www.amazon.co.jp/s?k='+isbn
    digits = isbn[3:-1]
    check = (-sum(int(c)*(10-i) for i,c in enumerate(digits))) % 11
    return 'https://www.amazon.co.jp/dp/'+digits+('X' if check == 10 else str(check))


seen = set()
for group in guide['groups']:
    for item in group['books']:
        key = item['reference']
        if key in seen or refs[key].get('type') != 'book':
            raise ValueError('Duplicate or non-book guide entry: '+key)
        seen.add(key)
        amazon_url(item['isbn'])
        cover = item['cover']
        if cover['available'] and (not isinstance(cover.get('image_id'), int) or cover['image_id'] <= 0):
            raise ValueError('Available cover requires a verified image ID: '+key)
        if not cover['available'] and not cover.get('note'):
            raise ValueError('Missing-cover decision needs a reason: '+key)
        for chapter in item['chapters']:
            if not (ROOT/'docs'/f'{chapter}.md').is_file():
                raise ValueError('Unknown linked chapter: '+chapter)
for locale in ('en','ja'):
    lines = introductions[locale].copy()
    for group in guide['groups']:
        lines.append('## '+group['title'][locale]+' {#'+group['id']+'}')
        for item in group['books']:
            r = refs[item['reference']]
            isbn = item['isbn']
            record = 'https://openlibrary.org/isbn/'+isbn
            available = item['cover']['available']
            cover = f'https://covers.openlibrary.org/b/id/{item["cover"]["image_id"]}-M.jpg?default=false' if available else None
            cover_label = ('Cover of ' if locale=='en' else '表紙：')+r['title']
            source_label = ('Cover: Open Library' if locale=='en' else '表紙出典：Open Library') if available else ('Open Library record' if locale=='en' else 'Open Libraryの書誌情報')
            loading = 'Loading cover' if locale=='en' else '表紙を読み込み中'
            unavailable = 'Cover unavailable' if locale=='en' else '表紙画像なし'
            cover_image = (f'<img class="book-cover-image" src="{cover}" alt="{html.escape(cover_label,quote=True)}" '
                           'width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">\n') if available else ''
            state = 'loading' if available else 'missing'
            lines.append(f'<section class="textbook-card" aria-labelledby="{r["id"]}">\n'
                         '<div class="textbook-art">\n'
                         f'<div class="textbook-cover" data-cover-state="{state}">\n'
                         f'<a href="{record}" target="_blank" rel="noopener" aria-label="Open Library: {html.escape(r["title"],quote=True)}">\n'
                         '<span class="book-cover-placeholder" aria-hidden="true">'
                         f'<span class="book-placeholder-title" lang="en" data-original>{html.escape(r["title"])}</span>'
                         f'<span class="book-cover-loading">{loading}</span>'
                         f'<span class="book-cover-unavailable">{unavailable}</span></span>\n'
                         +cover_image+
                         '</a>\n</div>\n'
                         f'<a class="book-cover-credit" href="{record}" target="_blank" rel="noopener">{source_label}</a>\n'
                         f'<span class="book-isbn">ISBN {isbn}</span>\n</div>\n'
                         '<div class="textbook-details">')
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
            links = [f'<a class="book-purchase" href="{amazon_url(isbn)}" target="_blank" rel="noopener">Amazon Japan ↗</a>',
                     f'<a href="{html.escape(source,quote=True)}" target="_blank" rel="noopener">'+('Publisher / record ↗' if locale=='en' else '出版社・書誌情報 ↗')+'</a>']
            if r['source'] != source:
                links.append(f'<a href="{html.escape(r["source"],quote=True)}" target="_blank" rel="noopener">'+('Author / source ↗' if locale=='en' else '著者・参照資料 ↗')+'</a>')
            lines.append('<p class="book-links">'+'\n'.join(links)+f'\n<code>{r["id"]}</code></p>')
            lines.append('</div>\n</section>')
    path = ROOT/'docs'/('ja/' if locale=='ja' else '')/'textbooks.md'
    path.write_text('\n\n'.join(lines)+'\n')
print(f'Rendered {len(seen)} selected textbooks in English and Japanese.')
