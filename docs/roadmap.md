# 実装と公開のロードマップ

## 現在：計算と資料の土台

ローカルで動く教育用計算、年代順解説、出典・BibTeX、比較図、自動テストを準備しています。
公開サイト、GitHub リモート、ライセンスの設定はこれから相談します。
NASA のカタログと rotated solver の文献整理を、流れの実装が済んだ状態とは表示しません。

## 次の数値検証

- 全展示の run manifest と出力データの対応を強化し、格子・時間収束と wall-clock を整理。
- FV のセル平均初期化・参照解積分、WENO の特性分解、正値性 limiter、より強い衝撃波試験。
- 浅水と等温の厳密参照、地形と well-balanced、乾床は独立した実装段階。
- MHD の Alfvén 波、Brio–Wu、field loop、より低散逸の upwind CT。外部参照コードとの比較。
- 非線形 Fourier と dealiasing、Euler DG と limiter、多次元 residual distribution。
- 低 Mach PDE 前処理と 2D Euler rotated-hybrid solver。エントロピー修正・正値性・carbuncle を別々に検証。
- elliptic の可変係数・異方性・line smoothing、FAS、AMG、混合境界の 2D 拡張。

## NASA ケースの導入順案

まず wedge と expansion で 2D Euler の流束・壁境界を確認。
次に cavity と Blasius で粘性と圧力・境界を整え、円柱で非定常時間精度を確認。
RANS は平板と bump でモデル実装を検証した後、翼型、step、diffuser、hump に進みます。
これは難度と依存関係による順序で、原論文の年代順アトラスと併用します。

## 公開サイトを相談する段階

姉妹サイトと同じ「文献 → 方程式 → 実行 → 図 → 検証」を展示単位にします。
数値的に検証した教育例、原図再現、試作、文献のみ、今後の計画を区別して表示します。
公開時には名前、URL、デザイン、日英の扱い、ライセンス、掲載する展示の基準を相談します。
その前に自動的な公開は行いません。
