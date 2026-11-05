# NASA の代表的な 2D 検証ケース

公式の入口は [NPARC Verification and Validation Archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)、
[CFL3D のケース集](https://nasa.github.io/CFL3D/Cfl3dv6/cfl3dv6_testcases.html)、
[Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/) です。
TMR は NASA が維持してきた資料で、2026 年 2 月に GitHub に移転したことが
[NASA の案内](https://www.nasa.gov/nasa-turbulence-modeling-resource/) に明記されています。
以下は**カタログ化した候補**で、本リポジトリにこれらの 2D 流れの実装や再現結果はまだありません。

## Euler・解析解から始める候補

- **15° wedge、Mach 2.0**：斜め衝撃波、壁面圧、格子依存性、Roe／HLLE の比較。
  [NASA のケース](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html)。
- **15° wedge、Mach 2.5**：衝撃波角と下流状態を理論値で照合する候補。
  下の膨張コーナーと対にして、圧縮・膨張を扱います。
  個別ページは [公式アーカイブの該当項目](https://www.grc.nasa.gov/WWW/wind/valid/archive.html) から辿れます。
- **Prandtl–Meyer 15° expansion、Mach 2.5**：膨張扇、Mach 数、圧力の解析関係。
  [公式アーカイブ](https://www.grc.nasa.gov/WWW/wind/valid/archive.html)。

## 層流・非定常・圧力 Poisson に接続する候補

- **Driven cavity**：正方形内の流れ、中心線速度、主渦と隅渦。
  NASA は低 Mach 数で非圧縮近似を計算し、Ghia ほかの参照値と比較しています。
  [NASA のケース](https://www.grc.nasa.gov/WWW/wind/valid/cavity/cavity.html)。
- **Blasius laminar flat plate**：境界層速度分布、壁面摩擦、法線格子。
  [NASA のケース](https://www.grc.nasa.gov/www/wind/valid/fplam/fplam.html)。
- **Circular cylinder、層流非定常**：渦放出、抗力・揚力の履歴、時間精度。
  dual time stepping の後の候補です。
  [NASA のケース](https://www.grc.nasa.gov/WWW/wind/valid/lamcyl/lam_cyl.html)。

## 乱流モデル・剥離・翼型

- **Zero-pressure-gradient turbulent flat plate**：壁面摩擦、乱流モデルの実装検証、格子収束。
  [TMR verification](https://tmbwg.github.io/turbmodels/flatplate.html)。
- **2D bump-in-channel**：曲面圧力と摩擦、同一モデルを用いたコード間検証。
  [TMR verification](https://tmbwg.github.io/turbmodels/bump.html)。
- **Driver–Seegmiller backward-facing step**：剥離・再付着、Cp／Cf、速度分布。
  Reynolds 数の定義・訂正を含め、採用するデータの版を固定します。
  [TMR validation](https://tmbwg.github.io/turbmodels/backstep_val.html)、
  [NPARC](https://www.grc.nasa.gov/WWW/wind/valid/backstep/backstep.html)。
- **Sajben transonic diffuser**：内部衝撃波、背圧、衝撃波と境界層の相互作用。
  [NASA のケース](https://www.grc.nasa.gov/WWW/wind/valid/transdif/transdif.html)。
- **RAE 2822 transonic airfoil**：翼面 Cp、衝撃波、境界層。ケース番号、補正した Mach 数・迎角を明示して使います。
  [NASA のケース](https://www.grc.nasa.gov/WWW/wind/valid/raetaf/raetaf.html)。
- **NACA 0012**：翼面圧力、揚抗力、格子・遠方境界・乱流モデルの影響。
  [TMR validation](https://tmbwg.github.io/turbmodels/naca0012_val.html)。
- **NACA 4412 trailing-edge separation**：逆圧力勾配と後縁剥離。
  [TMR validation](https://tmbwg.github.io/turbmodels/naca4412sep_val.html)。
- **NASA wall-mounted hump**：壁面隆起による剥離・再付着。
  三次元性を含む実験と 2D 計算の適用範囲も記録します。
  [TMR validation](https://tmbwg.github.io/turbmodels/nasahump_val.html)。
- **2D mixing layer**：自由剪断層の成長、速度・乱流量。
  [TMR validation](https://tmbwg.github.io/turbmodels/delvilleshear_val.html)。
- **2D airfoil near-wake**：翼後流の速度欠損と回復。
  [TMR validation](https://tmbwg.github.io/turbmodels/airfoilwake_val.html)。

## NASA の公式ケース集とは別の古典的な 2D ベンチマーク

Double Mach Reflection、Mach 3 forward-facing step、2D Riemann configurations、
isentropic vortex、odd-even shock instability／carbuncle も、数値流束の展示に適しています。
前二者の代表文献は [Woodward–Colella (1984), 原論文](https://crd.lbl.gov/assets/pubs_presos/AMCS/ANAG/A31984.pdf)。
これらを「NASA が提案した問題」と一括りにはしません。
ONERA M6 は有名ですが 3D wing、軸対称 bump／jet も平面 2D とは異なるため、この一覧の本体に含めません。

## ケース化するときに固定する情報

出典、ケース番号、幾何、無次元化、Mach／Re／迎角、壁面・遠方・流入流出境界、格子系列、
乱流モデルの正確な変種、収束残差、時間刻み、Cp／Cf／Cl／Cd の定義を保存します。
単なる残差低下は、格子収束や実験との一致を意味しません。
NASA の入口だけを引用して原実験の引用を省くことはせず、各実装段階で元の計測論文も追加します。
