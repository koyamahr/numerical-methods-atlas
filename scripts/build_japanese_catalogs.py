"""Render three Japanese catalog chapters from the shared, counted sources.

Model equations, bibliographic metadata and coverage identities have one source.
Japanese prose is a draft overlay; this script never updates review/source hashes.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
load = lambda name: json.loads((ROOT / name).read_text())
references = sorted(load('catalog/references.json'), key=lambda e: (e['year'], e['id']))
refs = {entry['id']: entry for entry in references}
models = load('catalog/biological-models.json')['models']
overlay = load('catalog/locales/ja/biological-models.json')
messages = load('website/locales/messages.json')
words = {entry['en']: entry['ja'] for entry in messages.values()}
terms = {entry['en']: entry['ja'] for entry in load('catalog/glossary.json')['terms']}

def slug(heading):
    # Match the web renderer's English IDs, including entities in marked headings.
    rendered = html.escape(heading).replace('&#x27;', '&#39;').lower()
    rendered = ''.join(c for c in rendered if c.isalnum() or c.isspace() or c == '-')
    return re.sub(r'\s+', '-', rendered.strip())

def write_chapter(name, text):
    source = (ROOT / 'docs' / (name + '.md')).read_text()
    headings = re.findall(r'^#{2,3} (.+)$', source, re.M)
    translated = re.findall(r'^#{2,3} (.+)$', text, re.M)
    if len(headings) != len(translated):
        raise ValueError('Generated Japanese section mismatch: ' + name)
    ids = iter(slug(heading) for heading in headings)
    text = re.sub(r'^(#{2,3} .+)$', lambda m: m[1] + ' {#' + next(ids) + '}', text, flags=re.M)
    path = ROOT / 'docs/ja' / (name + '.md')
    if not path.is_file() or path.read_text() != text:
        path.write_text(text)

families = {
    'Population and ecology': '個体群・生態', 'Biochemical reactions': '生化学反応',
    'Structured population transport': '構造化個体群の輸送', 'Epidemic compartments': '感染症区画',
    'Excitable systems': '興奮系', 'Pattern formation': '模様形成', 'Chemotaxis': '走化性',
    'Biomechanics': '生体力学', 'Stochastic reaction networks': '確率反応網',
    'Delay and gene regulation': '遅延・遺伝子制御', 'Evolutionary dynamics': '進化動力学',
}
if set(overlay) != {model['id'] for model in models}:
    raise ValueError('Japanese biological overlay must match every model ID')
parts = [(ROOT / 'scripts/templates/ja/biology-intro.md').read_text().strip()]
for index, model in enumerate(models, 1):
    ja = overlay[model['id']]
    citations = []
    for key in model['citations']:
        entry = refs[key]
        url = 'https://doi.org/' + entry['doi'] if entry.get('doi') else entry['source']
        label = 'Michaelis–Menten（1913、2011年の翻訳を参照）' if key == 'michaelis1913' else f"{entry['author']} ({entry['year']})"
        citations.append(f'[{label}]({url})')
    parts += [f"### {index:02d} · {model['year']} · {terms[model['name']]}（{model['name']}）",
              f"**{families[model['family']]}・文献調査のみ。** {ja['meaning']}",
              '\\[\n' + model['equation'] + '\n\\]',
              '**数値的な課題。** ' + ja['numerics'],
              '**検証案。** ' + ja['verification']]
    if model['scope']:
        if not ja['scope']: raise ValueError('Missing model-convention translation: ' + model['id'])
        parts.append('**モデルの規約。** ' + ja['scope'])
    parts.append('出典：' + ', '.join(citations) + '。')
outro = (ROOT / 'scripts/templates/ja/biology-outro.md').read_text().strip()
math = re.findall(r'\\\[[\s\S]*?\\\]', (ROOT / 'docs/biological-models.md').read_text())
for key, value in zip(('front_math', 'linear_math', 'laplacian_math'), math[-3:]):
    outro = outro.replace('{{' + key + '}}', value)
parts.append(outro)
write_chapter('biological-models', '\n\n'.join(parts) + '\n')

parts = ['# 原著の出版年順に並べた参考文献',
         '原著論文・書籍と、実装を確認するために用いた資料を区別します。DOIの存在は、全文の閲覧や図の再現を意味しません。各出典注記に、公開原著、後年の解説、未確認の原資料を記しています。NASAの資料は[2次元問題カタログ](nasa-2d.md)にもあります。',
         '著者名・原題・誌名・出典注記は、英語版と共通の原表記を保持しています。見出しや案内は日本語です。',
         'この章と`references.bib`は、`catalog/references.json`から生成します。書誌データの正本は共通であり、翻訳によって文献数は増えません。']
for entry in references:
    url = 'https://doi.org/' + entry['doi'] if entry.get('doi') else entry['source']
    venue = entry.get('journal', entry.get('publisher', entry.get('institution', entry.get('booktitle', ''))))
    parts += [f"## {entry['year']} · {entry['id']}",
              f"<div lang=\"en\" data-original>\n\n{entry['author']}. **{entry['title']}**. {venue}.\n\n</div>",
              f"[原著の書誌情報]({url}) · [全文または実装の参照資料]({entry['source']})",
              f"<div lang=\"en\" data-original>\n\n{entry['note']}\n\n</div>"]
write_chapter('references', '\n\n'.join(parts) + '\n')

coverage = load('website/content/coverage.json')
c = coverage['counts']
parts = ['# 収録範囲と数え方',
         f"公開Web版、集計日{coverage['counted_on']}。数えるのはカタログ項目と記載した実験例です。すべての項目が検証済みの完全なソルバーであるという意味ではありません。",
         f"**方程式・モデル{c['equations']}項目・計算法と構成要素{c['methods']}項目・学術誌／会議論文{c['papers']}件・全参考資料{c['references']}件。**",
         f"保存済み計算を用いる方程式ギャラリーは{c['gallery_equations']}系統・{c['gallery_cases']}例、読書章はこの一覧を含め{c['reading_chapters']}章です。",
         '## 方程式とモデル',
         '名前付きの方程式・モデルを数えます。スカラー成分や数学的に互いに独立な系統の数ではありません。枠組みや補助定式化を含み、通常は派生形を一つにまとめます。ただし個別に説明するSR／GRの流体系3種類は分けます。生物モデルは専用カタログから一度だけ取り込みます。',
         f"ローカル実験のある項目は{c['local_equations']}、文献解説のみは{c['reading_equations']}で、後者には生物調査{c['biological_entries']}項目すべてを含みます。連成系は一項目とし、成分方程式では増やしません。Poisson／Laplaceや次元の違いもまとめます。枠組みと個別反応則が並ぶため、数学的に独立した系統数ではありません。",
         '一覧の詳細な範囲注記は原文（英語）を保持します。各章の日本語本文も併せて参照できます。']
for kind, title in [('equation', '方程式・モデルの一覧'), ('method', '計算法の一覧')]:
    parts.append('## ' + title)
    if kind == 'method':
        parts += ['名前付きの離散化法、積分法、線形・非線形解法、連成演算子を数えます。パラメータの違いでは増やしません。',
                  f"ローカル実験のある項目は{c['local_methods']}、文献解説のみは{c['reading_methods']}です。再構成の制限関数、前処理、連成演算子は構成要素であり、完全なPDEソルバーではありません。格子配置、CFL条件、定理は計算法の数に含めません。"]
    entries = [entry for entry in coverage['items'] if entry['kind'] == kind]
    for group in dict.fromkeys(entry['group'] for entry in entries):
        parts.append('### ' + words[group])
        lines = []
        for entry in entries:
            if entry['group'] != group: continue
            label = terms[entry['label']]
            status = 'ローカル実験あり' if entry['status'] == 'local-example' else '文献解説のみ'
            scope = f' <span lang="en" data-original>{html.escape(entry["scope"])}</span>' if entry['scope'] else ''
            lines.append(f"- [{label}（{entry['label']}）]({entry['chapter']}.md) — {status}。{scope}")
        parts.append('\n'.join(lines))
parts += ['## 論文数と全資料数の区別',
          '論文数は学術誌論文と会議論文です。総説、翻訳、採録済みであることを明記した論文も含みます。全参考資料は、それに書籍、章、技術資料、文書、個別に識別したプレプリント等を加えた、重複を除く出版物の数です。',
          '\n'.join(f'- {c[key]}件：{label}' for key, label in [('journal_articles', '学術誌論文（総説・翻訳・採録済み論文を含む）'), ('conference_papers', '会議論文'), ('books', '書籍'), ('chapters', '書籍の章'), ('reports', '技術・教育レポート'), ('other_sources', 'その他の資料・文書・プレプリント')]),
          'Cockburn–Shu 1989の重複書誌を統合し、Burgers 1948を書籍の章に分類しました。以前の146レコードには重複があり、その後の出典追加も現在の重複を除く総数に反映しています。原著と別途出版された翻訳は異なる出版物です。すべての全文を確認済みとは主張せず、確認状態を各出典注記に残します。',
          '## 再現方法',
          '名前付き登録簿は`catalog/coverage.json`です。生物項目と出版物の種別は各専用カタログを参照します。`python scripts/build_coverage.py`が出版物の同一性とローカル章リンクを検査し、数と一覧を生成します。Webビルドもこの検査を実行します。パラメータ、保存フレーム、本文での方程式の繰り返し、テスト関数の数では増やしません。翻訳ファイルも章の総数を増やしません。',
          '[集計一覧と出典ハッシュをダウンロード](figures/site-coverage.json)。[参考文献](references.md)、[方程式ギャラリー](equation-gallery.md)、[生物モデル](biological-models.md)、[実装ロードマップ](roadmap.md)も参照できます。']
write_chapter('site-coverage', '\n\n'.join(parts) + '\n')
print('Rendered three Japanese catalog chapters from shared model/publication identities.')
