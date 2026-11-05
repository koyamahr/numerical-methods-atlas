# 数値計算法の歴史アトラス

年は原著の出版年を基準とし、必要に応じて翻訳、再版、オンライン公開の年を区別します。このアトラスは代表的な出典をたどる読書の道案内であり、すべての発明や優先権を確定するものではありません。[参考文献一覧](references.md)では、未確認の事項も含め、各出典と実装の関係を記録しています。

## 古典的な基礎：方程式、差分、反復 {#classical-foundations-equations-differences-and-iteration}

前進・後退・中心差分、Euler時間積分、Fourier展開、熱伝導、Laplace・Poisson方程式から始めます。Dirichlet、Neumann、Robin条件を導入する前に、境界の値と境界を通る流束を区別します。これらの数学的な起源は、後に数値流体力学で使われるようになる時代より前にあります。

## 1928年：CFL条件と依存領域 {#1928-cfl-and-domains-of-dependence}

Courant–Friedrichs–Lewyは、連続問題の依存領域と離散ステンシルが届く範囲を比較します。線形移流で`C=a Δt/Δx`を変え、必要条件と十分条件を区別します。[CFLの原論文](https://doi.org/10.1007/BF01448839)、[導出と実験](stability.md)を参照してください。

## 1939〜1943年：運動論の漸近展開と変分的な組立て {#19391943-kinetic-asymptotics-and-variational-assembly}

Chapman–Cowlingの運動論の本は1939年に出版されました。これは書籍の出版年であり、[Chapman–Enskog展開](chapman-enskog.md)の発明年ではありません。[Courant（1943）](https://doi.org/10.1090/S0002-9904-1943-07818-4)は変分問題と区分的な表現を結び付けます。[P1 FEMの展示](fem.md)では、独立に作った疎行列Poisson問題を実装しています。

## 1947〜1950年：拡散、陰解法、線形安定性 {#19471950-diffusion-implicit-methods-and-linear-stability}

Crank–Nicolson（1947）、一般に1949年の報告へ帰されるThomasの三重対角消去、Charney–Fjørtoft–von Neumannの数値予報研究（1950）における安定性解析へ進みます。Thomas報告の原文はここでは未確認です。1950年論文は歴史的な背景として扱い、von Neumann解析がその論文だけから始まったとは主張しません。拡散数`r=ν Δt/Δx²`をA安定性、単調性、陰的な線形方程式系へ結び付けます。[拡散と線形ソルバー](elliptic.md)。

[Burgers（1948）](https://doi.org/10.1016/S0065-2156(08)70100-5)は、並行する非線形モデルの分岐を与えます。[方程式ギャラリー](equation-gallery.md)では非粘性の衝撃波・膨張波問題を使い、原著の乱流解析を再現しているわけではありません。

## 1954〜1961年：Lax、Godunov、保存形 {#19541961-lax-godunov-and-conservation-form}

Lax（1954）、Lax–Richtmyer（1956）、Godunov（1959）、Lax–Wendroff（1960）、Rusanov（1961）を通して、弱解、数値流束、衝撃波速度、数値粘性、分散へ進みます。線形問題の収束に関するLax–Richtmyer定理と、非線形保存的近似の弱極限に関するLax–Wendroff型の結果では、仮定が異なります。

本実装の`method="godunov"`は、近似リーマン流束を使うGodunov型有限体積法を意味し、原著の厳密流束アルゴリズム全体の再現ではありません。

[BGK（1954）](https://doi.org/10.1103/PhysRev.94.511)は運動論的な緩和モデルを与えます。[Lighthill–Whitham（1955）](https://doi.org/10.1098/rspa.1955.0089)と[Richards（1956）](https://doi.org/10.1287/opre.4.1.42)は、保存則を交通波へ結び付けます。これらの別々の分岐は、単一の発明年表としてではなく、明示した方程式と出典を介してギャラリーでつながります。

## 1961〜1977年：緩和、マルチグリッド、局所基底と大域基底 {#19611977-relaxation-multigrid-and-local-and-global-bases}

Fedorenko（1961）、Reed–Hill（1973）、Gottlieb–Orszag（1977）、Brandt（1977）をたどります。Poisson反復を、高周波誤差の平滑化と、滑らかな誤差の粗格子補正に分けます。DGは要素ごとの多項式を境界流束でつなぎ、スペクトル法は大域基底を使います。それ以前のGalerkin法やFourierの考え方が数学的な背景です。[Poissonとマルチグリッド](elliptic.md)、`numart.advection.dg_advection`を参照してください。

[Chorin（1968）](https://doi.org/10.1090/S0025-5718-1968-0242392-2)から[非圧縮流の射影法](incompressible.md)へ進みます。[Alexander（1977）](https://doi.org/10.1137/0714068)は[SDIRKの分岐](stiff-integration.md)を与えます。ソース項の扱いや適応誤差制御は、手法の線形安定性関数とは別の要素です。

## 1978〜1983年：共通テスト問題と高解像度流束 {#19781983-shared-benchmarks-and-high-resolution-fluxes}

Sod（1978）、van LeerのMUSCL（1979）、Orszag–Tang（1979）、Roe（1981）、Harten–Lax–van Leer（1983）へ進みます。同じSod問題で接触波と音響波の解像度を比べます。初版のMUSCLはminmodと線の方法を使い、van Leerの原型であるLagrange移動・再配置とは異なります。原著の非圧縮Orszag–Tang研究と、今日の圧縮性テストの規格化も区別します。[テスト問題の定義](benchmarks.md)、[MHD](mhd.md)。

## 1984〜1989年：TVD勾配とTVBによる極値の緩和 {#19841989-tvd-slopes-and-tvb-extrema-relaxation}

[Sweby（1984）](https://doi.org/10.1137/0721062)はスカラー流束制限の条件を整理します。[Cockburn–Shu（1989）](https://doi.org/10.1090/S0025-5718-1989-0983311-4)はTVB RKDGの枠組みを発展させます。5種類の[勾配制限](limiters.md)を比較し、別の構成要素である[TVBと正値状態スケーリング](advanced-limiters.md)を調べます。後者ではZhang–Shu（2010）の正値性の枠組みも紹介し、必要な流束、求積、CFL、SSP条件を示します。

## 1985〜1991年：3次分布と輸送する勾配 {#19851991-cubic-profiles-and-transported-gradients}

[Takewaki–Nishiguchi–Yabe（1985）](https://doi.org/10.1016/0021-9991(85)90085-3)と[Yabe–Aoki（1991）](https://doi.org/10.1016/0010-4655(91)90071-R)が、3次の値・勾配輸送であるCIPの系譜を発展させます。[CIPの章](cip.md)では定速のスカラー例を計算し、後の保存型・有理関数型の分岐と区別します。構成したHermite場のテストにより、低拡散性と質量保存の保証を分けます。

## 1987〜1989年：高次精度、前処理、磁場の制約 {#19871989-higher-order-preconditioning-and-magnetic-constraints}

HartenらのENO（1987）、Turkelの低速流前処理（1987）、Einfeldt（1988）、Evans–HawleyのCT（1988）、Shu–Osher（1988、1989）、Cockburn–ShuのRKDG（1989）へ進みます。高次補間だけでは頑健な衝撃波捕獲は保証されず、エントロピー修正と正値性は別に扱う必要があります。Shu–Osher問題は衝撃波と滑らかな密度波を組み合わせます。

## 1991〜1996年：非定常反復、低密度、HLLC、WENO {#19911996-unsteady-iteration-low-densities-hllc-and-weno}

Einfeldtら（1991）、Jameson（1991）、Toro–Spruce–Speares（1994）、Liu–Osher–Chan（1994）、Jiang–Shu（1996）をたどり、物理時間と擬似時間、低密度での破綻、接触波の回復、非線形WENO重みを学びます。1994年のWENOの起源と、初版に実装したWENO5-JS（1996）を区別します。[前処理と二重時間積分](advanced.md)。

## 2000〜2008年：多次元での頑健性と制約 {#20002008-multidimensional-robustness-and-constraints}

Tóth（2000）、Dednerら（2002）、Abgrallの残差分配法の総説（2006）、Nishikawa–Kitamura（2008）をたどります。離散CT／GLM演算子、保存的な残差分配、回転ハイブリッド流束、カーバンクル不安定性を調べます。2006年はRDの総説の年であり、残差分配法の発明年ではありません。

[Inutsuka（2002）](https://doi.org/10.1006/jcph.2002.7053)は、粒子対ごとのリーマン問題を使う畳み込みに基づいたSPH発展という、並行する粒子法の分岐を加えます。[GSPHの章](gsph.md)では1994年の先行研究、2002年の詳細な定式化、[Iwasaki–Inutsuka（2011）](https://doi.org/10.1111/j.1365-2966.2011.19588.x)によるMHD拡張を区別します。文献ノートと今後の流体ソルバーの計画であり、既存の静的なSPH再構成とは別です。

## 2001〜2009年：SSPの継承とRunge–Kuttaの追加段階 {#20012009-ssp-inheritance-and-additional-rungekutta-stages}

[Gottlieb–Shu–Tadmor（2001）](https://doi.org/10.1137/S003614450036757X)、[Spiteri–Ruuth（2002）](https://doi.org/10.1137/S0036142901389025)、[Gottlieb–Ketcheson–Shu（2009）](https://doi.org/10.1007/s10915-008-9239-z)は、スカラー線形安定性と、条件付きの非線形安定性の継承を区別します。SSPの分岐における発展であり、Runge–Kutta法そのものの起源ではありません。[RK系譜の章](runge-kutta.md)はRK2の各種公式、RK4、SSPRK(s,p)を、実際の非線形段階と細分化で比較します。

## 相対論の分岐：1972〜2026年 {#relativistic-branch-19722026}

[SRHD／GRHD／GRMHDの調査](relativistic-hydrodynamics.md)は、WilsonのKerr背景計算（1972）、厳密SRリーマン解（1994）、Valencia（1997）、局所座標系ソルバー（1998）、相対論的な磁場制約、HARM（2003）、動的時空、非線形の基本変数回復を結び付けます。後の分岐には放射、DG–FD混合法、物理状態の制約、GPU向け合体コードを含みます。[SRGSPH（2026）](https://doi.org/10.1016/j.jcp.2025.114448)はInutsukaの粒子定式化へつながります。出典と出版状況は2026年11月6日時点の確認を記録しており、相対論ソルバーの実装は追加していません。

## 現代的な検証と妥当性確認へ {#toward-modern-verification-and-validation}

[NASAの2次元テスト問題集](nasa-2d.md)では、数値的な検証（verification）と、実験に対する物理的な妥当性確認（validation）を区別します。今後の展示は原典、現在のデータ入手先、実装状況、検証根拠を結び付ける必要があります。

## 移動格子、粒子、時間モード {#moving-meshes-particles-and-temporal-modes}

固定格子の歴史には並行する分岐があります。[Hirt・Amsden・Cook（1974）](https://doi.org/10.1016/0021-9991(74)90051-5)は古典的なALEの枠組みを与え、[Gingold・Monaghan（1977）](https://doi.org/10.1093/mnras/181.3.375)と[Lucy（1977）](https://doi.org/10.1086/112164)は独立した初期SPHの出典です。[ALE](ale.md)、[粒子](particles-sph.md)、[格子](meshes.md)の各章で、幾何と運動の表現の違いをつなぎます。コードが実装するのは小さな再構成と幾何保存の例であり、原著の流体計算そのものではありません。

[時間積分の章](time-integration.md)は2ステップleapfrogの漸化式と計算モードの根を示します。時間フィルターの説明では[Williams（2009）](https://doi.org/10.1175/2009MWR2724.1)による後の改良を参照しますが、leapfrogの発明をその論文へ帰してはいません。

[二重Mach反射の展示](double-mach.md)では2次元衝撃波干渉を実際に計算します。[Quirk（1994）](https://doi.org/10.1002/fld.1650180603)と[Pandolfi・D’Ambrosio（2001）](https://doi.org/10.1006/jcph.2000.6652)から、別に用意した[カーバンクルの文献ノート](carbuncle.md)へ進みます。[Philip L. Roeを偲んで](roe-memorial.md)では大学による2026年の追悼を記録し、1981年の貢献へ立ち返ります。

## 粒子場と正準的な時間写像 {#particle-fields-and-canonical-time-maps}

[HockneyのP³Mの解説（1981）](https://www.ccp5.ac.uk/wp-content/uploads/2023/03/CCP5_Newsletter_1981_06_01.pdf)、[Barnes–Hut（1986）](https://doi.org/10.1038/324446a0)、[Greengard–Rokhlin（1987）](https://doi.org/10.1016/0021-9991(87)90140-9)は格子・木・展開に基づく場の計算をつなぎます。[Yoshida（1990）](https://doi.org/10.1016/0375-9601(90)90092-3)は高次のシンプレクティック合成への道を与えます。[重力](particle-gravity.md)と[Hamilton写像](symplectic.md)の章では役割の違いを明示します。[Koyama–Ostriker（2009）](https://doi.org/10.1088/0004-637X/693/2/1316)は、[境界核の章](gravity-boundaries.md)にある円盤ポテンシャルFFTの参照文献です。

## 滑らかな流れの構造と適切なテスト選択 {#smooth-flow-structure-and-honest-test-selection}

[Kuya・Totani・Kawai（2018）](https://doi.org/10.1016/j.jcp.2018.08.058)は、圧縮性流れの離散化KEEPの系譜を導入します。[KEEPの章](keep.md)では原型の直交座標2次形式を実装し、後のエントロピー、圧力平衡、時間方向への拡張と区別します。滑らかな渦の収束と[保存状態による動画](movies.md)は衝撃波捕獲テストとは別です。運動エネルギーの整合性も見た目の滑らかさも、一般的な安定性の保証ではありません。

## 並行するソルバーの分岐：1986〜2010年 {#parallel-solver-branches-19862010}

[GMRES（1986）](https://doi.org/10.1137/0907058)と[BiCGSTAB（1992）](https://doi.org/10.1137/0913035)は非対称[疎行列系のソルバー](sparse-nonlinear.md)を与えます。[Qianら（1992）](https://doi.org/10.1209/0295-5075/17/6/001)と[Guoら（2002）](https://doi.org/10.1103/PhysRevE.65.046308)から、[格子BGKと外力の展示](lattice-boltzmann.md)へ進みます。[Nishikawa（2007）](https://doi.org/10.1016/j.jcp.2007.07.029)は[1階の双曲型拡散系](hyperbolic-diffusion.md)を開発し、移流拡散への拡張は2010年に出版されました。解説では、原型の2次残差分配法と本実装の1次有限体積ベースラインを区別します。

## 生物と地球流体の分岐 {#biological-and-geophysical-branches}

[生物方程式の調査](biological-models.md)では、個体群増殖からLotka／Volterra、年齢構造、SIRへ進み、Fisher前線、Turing形態形成、興奮性膜、走化性、確率反応回路、合成遺伝子回路をたどります。原著、翻訳、簡約モデルにはそれぞれ出典注記があります。22項目はすべて文献調査のみです。

[Arakawa–Lamb（1977）](https://doi.org/10.1016/B978-0-12-460817-7.50009-4)は、変数配置を地球流体の波へ結び付けます。[A／B／Cの章](geophysical-grids.md)では、独立に計算したf平面の中心差分記号を比較します。水平格子の分類は、鉛直スタガード配置や非線形不変量の保存とは別の性質です。
