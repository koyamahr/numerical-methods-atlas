# NASAの2次元検証・妥当性確認問題集

公式の[NPARC Verification and Validation Archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)、[CFL3Dテスト](https://nasa.github.io/CFL3D/Cfl3dv6/cfl3dv6_testcases.html)、[Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/)から始めてください。NASAの[TMR案内](https://www.nasa.gov/nasa-turbulence-modeling-resource/)は2026年2月のGitHub移行を説明します。

以下は**候補として登録した問題**です。このリポジトリには以下のNASA問題の実装・再現結果はまだありません。別の古典的な[二重Mach反射の基準例](double-mach.md)は計算済みです。

## Eulerと解析参照解から始める {#starting-with-euler-and-analytical-references}

- **15度楔、Mach 2.0**：斜め衝撃波、壁圧、格子依存、Roe／HLLE比較。[NASA問題](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html)。
- **15度楔、Mach 2.5**：衝撃波角と下流状態を理論比較し、次の膨張角と対にする圧縮例。[公式アーカイブ](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)から該当項目へ進みます。
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

二重Mach反射、Mach 3前向きステップ、2次元リーマン配置、等エントロピー渦、奇偶衝撃波・カーバンクルも有用です。前二者の代表的出典は[Woodward–Colella（1984）](https://doi.org/10.1016/0021-9991(84)90142-6)です。[本二重Mach反射](double-mach.md)は実装済み1次HLL基準例で、ステップやこの段落の他の問題は今後の課題です。必要な安定性比較は[カーバンクルノート](carbuncle.md)を参照してください。

すべてをNASA発祥と呼んではいけません。ONERA M6は3次元翼で、軸対称バンプ・ジェットも平面2次元とは異なるため、主一覧から除きます。

## 実装ごとに固定する情報 {#information-to-fix-for-each-implementation}

原典、ケース番号、幾何、無次元化、Mach／Reynolds数、迎角、壁・遠方・流入・流出境界、格子列、正確な乱流モデル変種、収束残差、時間刻み、Cp／Cf／Cl／Cdの定義を記録します。残差減少だけでは格子収束や実験一致は示せません。実装時にはNASAの紹介ページだけでなく、元の測定論文も加えてください。
