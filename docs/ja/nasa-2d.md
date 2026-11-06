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
