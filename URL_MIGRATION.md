# アトラスの名称と公開URLの移行

2026年11月6日。表示名と公開先の方針は確定し、レビュー用のコードへ反映した。実際のリポジトリ作成・改名・Pagesの公開先切替はまだ行っていない。

- 英語名：**An Atlas of Numerical Methods**
- 日本語名：**数値計算法アトラス**
- 新しい公開先：`https://koyamahr.github.io/numerical-methods-atlas/`
- 新しい公開用リポジトリ：`koyamahr/numerical-methods-atlas`
- 現在の公開先：`https://koyamahr.github.io/the-art-of-numerical-algorithms/`

## 設定と生成物

`website/site.config.json`で日英名、ブランド表記、公開URL、ソースの参照先、旧URLを管理する。タイトル、ヘッダー、フッター、OG情報、canonical、サイトマップ、robotsの参照先に同じ設定を使う。数値計算ライブラリのパッケージ名`numart`と、姉妹サイトThe Art of Thermal Instabilityの名称・URLは維持する。

原稿中の同サイトへのリンクは新URLへ更新し、Web本文を生成する際は同じ画面内のルートへ変換する。日本語の閲覧中にリンクを開いても、言語指定と新しいプロジェクトのパスを保てる。初版リリースの歴史的な表題は記録として残す。

`npm --prefix website run build`は、通常の`website/dist/`に加えて、旧URL用の`outputs/legacy-redirect/`を生成する。後者には`index.html`、`404.html`、`migration.js`があり、新URLへの移動時に`?lang=ja`などのクエリと、`#/read/...?...`などの章・節・検索指定を保持する。JavaScriptが無効な場合は、日英の案内リンクから新サイトを開ける。この生成物は、新サイトの配布物には混ぜない。

## 公開時の順序

1. 新しい公開用リポジトリを用意し、レビュー済みのコミットを履歴付きで配置する。既存リポジトリをその場で改名するより、旧URLと旧ソースの履歴を保ちながら切り替えやすい。
2. 新しいリポジトリのPagesを設定し、公開候補を配置する。公開ワークフローは`GITHUB_REPOSITORY`が設定した新しい公開用リポジトリと一致することを確認する。旧リポジトリに新サイト本体を誤って公開する操作はここで止める。
3. 新URLで日本語／英語、章リンク、図、ダウンロード、モバイル表示が動くことを確認する。この確認前に旧サイトを置き換えない。
4. 旧サイトのPagesの配布物だけを、準備した旧URL用案内に切り替える。旧GitHubリポジトリの履歴、リリース、参照済みのコードは残す。旧サイトを戻すための直前の配布物とコミットも保存する。
5. 旧URLから言語・章・節が引き継がれることを確認し、READMEの「現在の公開先」と外部の紹介リンクを新URLへ揃える。Gitのリモートも、今後どちらを開発元とするかに合わせて更新する。

本体と案内ページの公開は別の操作であり、この準備ブランチからは自動的に実行しない。

## GitHubのURL転送との関係

GitHub公式では、リポジトリ改名時の自動転送からプロジェクトサイトURLが除外されている。また、改名後に旧リポジトリ名を再利用すると、GitHub側の旧リポジトリ転送も止まる。このため、今回の案では自動転送に依存せず、既存リポジトリを残し、新公開先と旧URL用案内を別々に用意する。[GitHubのリポジトリ改名の説明](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)
