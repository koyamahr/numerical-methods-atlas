# NASAの2次元検証・妥当性確認問題集

公式の[NPARC Verification and Validation Archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)、[CFL3Dテスト](https://nasa.github.io/CFL3D/Cfl3dv6/cfl3dv6_testcases.html)、[Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/)から始めてください。NASAの[TMR案内](https://www.nasa.gov/nasa-turbulence-modeling-resource/)は2026年2月のGitHub移行を説明します。

**15°楔の2ケースは、教育用Euler基準計算を追加しました。** それ以外のNASA項目は候補です。独立した実装による計算で、Wind-USの出力、実験による妥当性確認、NASAのソルバー・格子比較全体の再現ではありません。古典的なMach 3前向きステップと[二重Mach反射](double-mach.md)も併せて示します。

## 計算した衝撃波テスト {#computed-shock-tests}

[ギャラリーで衝撃波を伴う場を見る](#/gallery)。両楔は比熱比1.4、流入密度1・音速1の一様流から開始します。独立した物体適合格子はx=−0.5〜1、下壁y=max(x,0)tan(15°)、上端y=1.2です。Mach 2の弱い衝撃波が出口で上端へ届かない高さを使い、NASAのMach 2.5領域の高さ1とは異なります。流入・上端は一様流固定、流出は外挿、下壁は法線運動量を反射します。実際の四角形から面積・法線を求め、共有する面流束を逆符号で組み込んでセル総量を保存します。

- **NASA楔、Mach 2.0**：240 × 80セル、t=3のMach数・圧力分布と、理論上の弱い斜め衝撃波の線。120 × 40セルでも計算しています。[NASA設定](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html)。
- **NASA楔、Mach 2.5**：同じ独立格子と終了時刻。参照の衝撃波角は約36.94490°、圧力比2.467500、下流Mach数1.873526です。θ–β–M関係の求根と垂直衝撃波の関係から参照状態を求め、Rankine–Hugoniot関係も数値検査します。[NASA解析比較](https://www.grc.nasa.gov/WWW/wind/valid/wedge/wedge.html)。
- **古典的Mach 3前向きステップ**：長さ3・高さ1の流路、x=0.6から高さ0.2の段差。密度1.4・圧力1・速度3の一様流入、反射壁、外挿流出です。240 × 80セルでt=4まで計算し、81保存状態とMP4を公開します。[衝撃波反射の動画](#/movies?case=forward-step)。NASA発祥の実験ではなく、Emery／Woodward–Colellaの古典的テストです。[Woodward–Colella §VI.b](https://www.researchgate.net/publication/222459521_The_numerical_simulation_of_two-dimensional_fluid_flow_with_strong_shocks)の補正付きPPM比較とは異なり、今回の基準計算は通常の反射境界だけを使い、角近傍のエントロピー・エンタルピー再設定を行いません。角からの数値的な影響や、ぼやけた滑り線が残り得ます。

手法は**1次HLL有限体積法・SSPRK2、CFL 0.4**です。楔の初期値へ解析的な衝撃波を埋め込んではいません。密度の規格化L1誤差は、衝撃波直線でセルを厳密に切り分けた参照セル平均と比較します。壁圧は0.5<x<0.9の最初の流体セル列の中央値、衝撃波角は0.35<x<0.85の密度勾配から推定します。同じ有限終了時刻の2格子だけでは、一般的な漸近次数や完全な定常収束は保証しません。ステップには厳密解の重ね描きがなく、公開格子は1つです。t=4は非定常のスナップショットです。

![NASA Mach 2楔](figures/nasa-wedge-m20.png)
![NASA Mach 2.5楔](figures/nasa-wedge-m25.png)
![Mach 3前向きステップ](figures/forward-step.png)

`python scripts/build_shock_gallery.py`で再現し、`--reuse`でソースを照合した保存軌道を再描画できます。[計算条件・診断量・ハッシュ](figures/shock-gallery.json)、[最終数値場](figures/shock-gallery.npz)、[ステップ動画の記録](https://koyamahr.github.io/numerical-methods-atlas/assets/movies/shock-catalog.json)を公開します。

## 衝撃波を含むNASA問題の未実装項目 {#shock-containing-nasa-cases-still-to-implement}

[Mach 5衝撃波・境界層干渉](https://www.grc.nasa.gov/WWW/wind/valid/m5swbli/m5swbli.html)、[Mach 7層流ランプ](https://www.grc.nasa.gov/WWW/wind/valid/hypramp/hypramp.html)、Sajbenディフューザー、RAE 2822は後続候補です。各問題に必要な粘性・乱流・気体モデルも検証の一部であり、非粘性楔の図では代用できません。これらの計算展示はまだありません。

## Eulerと解析参照解から始める {#starting-with-euler-and-analytical-references}

- **15度楔、Mach 2.0 — 基準計算済み**：2格子の斜め衝撃波と壁圧。Roe／HLLEの手法比較は今後です。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html)。
- **15度楔、Mach 2.5 — 基準計算済み**：衝撃波角・下流状態の理論比較。次の膨張角の予定と対にする圧縮例。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/wedge/wedge.html)。
- **Prandtl–Meyerの15度膨張、Mach 2.5**：膨張扇と解析Mach・圧力関係。[公式アーカイブ](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)。

## 層流、非定常性、圧力Poisson {#laminar-flow-unsteadiness-and-pressure-poisson-problems}

- **駆動キャビティ**：正方形内の中心線速度、主渦、隅渦。NASAは低Mach計算で非圧縮流を近似し、Ghiaらと比較します。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/cavity/cavity.html)。
- **Blasius層流平板**：境界層分布、壁面摩擦、壁法線格子解像度。[NASA問題](https://www.grc.nasa.gov/www/wind/valid/fplam/fplam.html)。
- **非定常層流円柱**：渦放出、抗力・揚力履歴、時間精度。二重時間積分の後の候補です。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/lamcyl/lam_cyl.html)。

## 乱流モデル、剥離、翼型 {#turbulence-models-separation-and-airfoils}

- **ゼロ圧力勾配の乱流平板**：壁面摩擦、乱流モデル実装、格子収束。[TMR検証](https://tmbwg.github.io/turbmodels/flatplate.html)。
- **2次元流路内バンプ**：曲壁の圧力・摩擦を同じ乱流モデルのコード間で比較。[TMR検証](https://tmbwg.github.io/turbmodels/bump.html)。
- **Driver–Seegmiller後向きステップ**：剥離・再付着、Cp／Cf、速度分布。Reynolds数の定義や補正を含むデータ版を固定します。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/backstep_val.html)、[NPARC](https://www.grc.nasa.gov/WWW/wind/valid/backstep/backstep.html)。
- **Sajben遷音速ディフューザー**：内部衝撃波、背圧、衝撃波・境界層干渉。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/transdif/transdif.html)。
- **RAE 2822遷音速翼型**：表面Cp、衝撃波、境界層。ケース番号、補正Mach数・迎角を明示します。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/raetaf/raetaf.html)。
- **NACA 0012**：表面圧力、揚抗力、格子・遠方境界・乱流モデルの感度。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/naca0012_val.html)。
- **NACA 4412後縁剥離**：逆圧力勾配と後縁剥離。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/naca4412sep_val.html)。
- **NASA壁面ハンプ**：壁誘起の剥離・再付着。3次元効果を含む実験へ2次元計算が適用できる範囲を記録します。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/nasahump_val.html)。
- **2次元混合層**：自由せん断層の成長、速度、乱流量。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/delvilleshear_val.html)。
- **2次元翼型近傍後流**：速度欠損と回復。[TMR妥当性確認](https://tmbwg.github.io/turbmodels/airfoilwake_val.html)。

## 他の古典的2次元問題 {#other-classical-2d-benchmarks}

二重Mach反射、Mach 3前向きステップ、2次元リーマン配置、等エントロピー渦、奇偶衝撃波・カーバンクルも有用です。前二者の代表的出典は[Woodward–Colella（1984）](https://doi.org/10.1016/0021-9991(84)90142-6)です。[本二重Mach反射](double-mach.md)と上記ステップは実装済み1次HLL基準例で、滑らかなKEEP渦も計算済みです。リーマン配置と管理した奇偶衝撃波・カーバンクル比較は今後です。[カーバンクルノート](carbuncle.md)を参照してください。

すべてをNASA発祥と呼んではいけません。ONERA M6は3次元翼で、軸対称バンプ・ジェットも平面2次元とは異なるため、主一覧から除きます。

## 実装ごとに固定する情報 {#information-to-fix-for-each-implementation}

原典、ケース番号、幾何、無次元化、Mach／Reynolds数、迎角、壁・遠方・流入・流出境界、格子列、正確な乱流モデル変種、収束残差、時間刻み、Cp／Cf／Cl／Cdの定義を記録します。残差減少だけでは格子収束や実験一致は示せません。実装時にはNASAの紹介ページだけでなく、元の測定論文も加えてください。


Mach 2のMC計算はt=3でも局所的な時間変動が残り、最大保存変数更新率は約6.08です。定常収束解ではありません。密度誤差の改善と併せて更新率も公開します。

## MUSCL再構成の比較 {#muscl-reconstruction-comparisons}

[1次・minmod・MCを比較する](#/flow-comparison?case=wedge-m2.5&method=mc)。新しい計算は音響HLL、SSPRK2、公称CFL 0.4を共通にしています。四角形の面積重心で基本変数の物理勾配を求め、面の中点へ再構成します。物体適合格子では、x方向の割線に伴う物理的なyの変位も補正します。共有面流束を両隣のセルへ加えます。制限関数はminmod(a,b)とMC(a,b)=minmod(2a,(a+b)/2,2b)です。[制限関数の定義](limiters.md)も参照してください。境界再構成では固体近傍を除き、流体側の状態を反射します。面の密度・圧力が非正になる場合は、セルごとに共通の係数で再構成偏差を縮めます。SSPRK2の段階が失敗したら時間刻みを半分にして再試行し、回数を記録します。保存平均値はクリップしません。これは検証した保護処理であり、このソルバー全体の正値性の一般的証明ではありません。

両NASA楔について、120 × 40と240 × 80の格子で3再構成をt=3まで計算しました。壁圧・衝撃波角・積分密度誤差は前述の定義です。別の周期エントロピー波では速度(0.7,0.3)、圧力1、密度1+0.2sin(2πx)sin(2πy)を用い、初期化・比較とも厳密なセル平均値で行います。16²、32²、64²、128²でt=0.5まで計算し、比較ページに観測次数を表示します。この滑らかな問題ではMCが2次精度に近づきます。極値での制限関数の作動はminmodの観測次数に影響します。衝撃波誤差の収束領域は異なり、滑らかな解の2次精度の根拠にはなりません。

![滑らかな2次元波の格子細分化](figures/comparisons/smooth-refinement.png)

[前向きステップの比較](#/flow-comparison?case=forward-step&method=mc)には、同じ240 × 80格子でのminmod・MCの静止画と81状態の動画を加えました。3動画は密度・圧力の色範囲と要求出力時刻を共通にしますが、実際の途中時刻は適応時間刻み1段分ずれる場合があります。公称CFL・格子が同じでも計算費用は等しくありません。同一の物理問題を3再構成で比較しており、従来の1次動画も引き続き閲覧できます。角の処理は同じで、t=4は非定常流れです。

再現は`python scripts/build_euler_comparison.py`です。[比較の設定・診断・ハッシュ](figures/comparisons/euler-comparison.json)と[最終保存変数配列](figures/comparisons/final-fields.npz)を取得できます。全軌道はローカルの`outputs/euler-comparison`へ保存します。
