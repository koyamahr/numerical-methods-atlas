# 教科書案内：次に何を調べるか

このアトラスから参照するための書棚です。知りたい問いから選ぶ読書案内で、順位付けではありません。以下の年は引用する版の年であり、アルゴリズムの発明年ではありません。

リンク先は出版社の書誌情報や著者管理のページです。版情報と公開されている紹介・目次を確認しており、各書のすべての導出を点検したという意味ではありません。関連章はアトラスとの接点を示し、教科書全体の実装を意味しません。

**最初の道筋：** CFDの枠組みにはHirsch、保存則と有限体積法の考え方にはLeVeque、RiemannソルバーにはToro、圧力・速度連成にはPatankar、疎行列の反復解法にはSaad。個々の手法の由来を追うときは原論文にも戻ってください。

[参考文献庫を検索](#/references) · [登録済みの書籍のみ](#/references?q=type%3Abook) · [BibTeXをダウンロード](../references.bib)

## CFDの基礎と非圧縮流れ {#cfd-foundations}

### Hirsch {#hirsch2007}

Hirsch, Charles. **Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics**. Butterworth-Heinemann, 2007・第2版.

支配方程式、格子の性質、整合性・安定性、離散化から解法まで、CFD全体の枠組みを調べる本です。引用する2007年版は第2版の基礎巻です。

アトラスの関連章：[差分、CFL条件、von Neumann解析、Laxの定理](stability.md) · [構造格子、非構造格子、三角形格子](meshes.md) · [時間積分とleapfrog法](time-integration.md).

[出版社・書誌情報](https://doi.org/10.1016/B978-0-7506-6594-0.X5037-1) · [著者・参照ページ](https://www.sciencedirect.com/book/monograph/9780750665940/numerical-computation-of-internal-and-external-flows) · `hirsch2007`

### Fletcher / Volume I {#fletcher1991v1}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques**. Springer, 1991・第2版.

I巻はPDEの分類、重み付き残差法、定常・拡散問題、線形・非線形移流を調べるために。II巻の流れ別の解法に進む前の共通の数値的道具を扱います。

アトラスの関連章：[差分、CFL条件、von Neumann解析、Laxの定理](stability.md) · [連続有限要素法：弱形式から疎行列の組立てへ](fem.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

[出版社・書誌情報](https://doi.org/10.1007/978-3-642-58229-5) · [著者・参照ページ](https://link.springer.com/book/10.1007/978-3-642-58229-5) · `fletcher1991v1`

### Fletcher / Volume II {#fletcher1991v2}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories**. Springer, 1991・第2版.

II巻はI巻の一般的手法を、流れの方程式の各分類とその数値解法に結びつけるために。各アルゴリズムと合わせて仮定や境界条件も確認します。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [前処理、二重時間積分、残差分配法](advanced.md) · [極・円筒座標：テンソルと粘性](coordinates-viscosity.md).

[出版社・書誌情報](https://doi.org/10.1007/978-3-642-58239-4) · [著者・参照ページ](https://link.springer.com/book/10.1007/978-3-642-58239-4) · `fletcher1991v2`

### Ferziger · Perić · Street {#ferziger2020}

Ferziger, Joel H.; Perić, Milovan; Street, Robert L. **Computational Methods for Fluid Dynamics**. Springer, 2020・第4版.

離散演算子を実際のCFD計算手順に結びつける際に。特に非圧縮流れの圧力・速度連成や境界条件を調べる入口です。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [極・円筒座標：テンソルと粘性](coordinates-viscosity.md).

[出版社・書誌情報](https://doi.org/10.1007/978-3-319-99693-6) · [著者・参照ページ](https://link.springer.com/book/10.1007/978-3-319-99693-6) · `ferziger2020`

### Patankar {#patankar1980}

Patankar, Suhas V. **Numerical Heat Transfer and Fluid Flow**. CRC Press (current publisher record), 1980.

コントロールボリュームの収支とSIMPLE型の圧力・速度連成を、物理的な考え方から理解したいときに。教科書の解説と手法の原論文は区別します。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md).

[出版社・書誌情報](https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224) · [著者・参照ページ](https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224) · `patankar1980`

## 保存則・Riemannソルバー・衝撃波 {#hyperbolic}

### LeVeque / finite volume {#leveque2002}

LeVeque, Randall J. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press, 2002.

弱解、有限体積法の考え方、波の伝播、リミター、多次元保存則を調べるときに。Clawpack関連資料から理論と実装を結びつけられます。

アトラスの関連章：[Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md) · [勾配制限：minmod、Superbee、MC、van Leer、van Albada](limiters.md) · [方程式ギャラリー：計算法の前に方程式を選ぶ](equation-gallery.md).

[出版社・書誌情報](https://doi.org/10.1017/CBO9780511791253) · [著者・参照ページ](https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9) · `leveque2002`

### Toro {#toro2009}

Toro, Eleuterio F. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer, 2009・第3版.

Euler方程式の厳密・近似Riemannソルバー、接触波、高解像度の衝撃波捕獲法を導出・比較したいときに。

アトラスの関連章：[前処理、二重時間積分、残差分配法](advanced.md) · [Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md) · [テスト計算ライブラリ](benchmarks.md).

[出版社・書誌情報](https://doi.org/10.1007/b79761) · [著者・参照ページ](https://doi.org/10.1007/b79761) · `toro2009`

## 差分法と線形代数 {#common-numerics}

### LeVeque / finite differences {#leveque2007}

LeVeque, Randall J. **Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems**. SIAM, 2007.

整合性・安定性・収束の関係、常微分方程式、境界値問題、偏微分方程式の差分法を調べるときに。

アトラスの関連章：[A安定性、L安定性、誤差ノルム](accuracy-stability.md) · [時間積分とleapfrog法](time-integration.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

[出版社・書誌情報](https://doi.org/10.1137/1.9780898717839) · [著者・参照ページ](https://staff.washington.edu/rjl/booksnotes.html) · `leveque2007`

### Golub · Van Loan {#golub2013}

Golub, Gene H.; Van Loan, Charles F. **Matrix Computations**. Johns Hopkins University Press, 2013・第4版.

手法名だけでソルバーを選ぶ前に、条件数、安定な行列分解、最小二乗、固有値問題を確認するための本です。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

[出版社・書誌情報](https://doi.org/10.1137/1.9781421407944) · [著者・参照ページ](https://epubs.siam.org/doi/book/10.1137/1.9781421407944) · `golub2013`

### Saad {#saad2003book}

Saad, Yousef. **Iterative Methods for Sparse Linear Systems**. SIAM, 2003・第2版.

Krylov部分空間、GMRES、BiCG系の手法、前処理を調べるときに。著者のページで第2版の本文と訂正情報が公開されています。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

[出版社・書誌情報](https://doi.org/10.1137/1.9780898718003) · [著者・参照ページ](https://www-users.cse.umn.edu/~saad/books.html) · `saad2003book`

### Barrett et al. / Templates {#templates1994}

Barrett, Richard; Berry, Michael; Chan, Tony F.; Demmel, James; Donato, June; Dongarra, Jack; Eijkhout, Victor; Pozo, Roldan; Romine, Charles; van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM, 1994.

行列に必要な仮定を確認しながら、反復線形解法のアルゴリズムと選び方を手短に引く公開リファレンスです。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

[出版社・書誌情報](https://www.netlib.org/templates/templates.html) · [著者・参照ページ](https://www.netlib.org/templates/templates.html) · `templates1994`

## スペクトル基底と不連続Galerkin法 {#high-order}

### Trefethen {#trefethen2000}

Trefethen, Lloyd N. **Spectral Methods in MATLAB**. SIAM, 2000.

スペクトル微分、Fourier・Chebyshevの例、短い再現用プログラムを調べるときに。重心補間の扱いは限られるため補足資料も参照します。

アトラスの関連章：[インタラクティブ実験ガイド](experiments.md) · [Orthogonal polynomials and mesh basis functions](basis-functions.md).

[出版社・書誌情報](https://doi.org/10.1137/1.9780898719598) · [著者・参照ページ](https://people.maths.ox.ac.uk/trefethen/spectral.html) · `trefethen2000`

### Hesthaven · Warburton {#hesthaven2008book}

Hesthaven, Jan S.; Warburton, Tim. **Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications**. Springer, 2008.

節点多項式基底、求積、参照要素の演算子を、DGの要素間流束やPDE計算法につなげるための本です。

アトラスの関連章：[Orthogonal polynomials and mesh basis functions](basis-functions.md) · [インタラクティブ実験ガイド](experiments.md).

[出版社・書誌情報](https://doi.org/10.1007/978-0-387-72067-8) · [著者・参照ページ](https://link.springer.com/book/10.1007/978-0-387-72067-8) · `hesthaven2008book`

## 時間積分・地球流体・粒子法 {#time-geophysics-particles}

### Hairer · Lubich · Wanner {#hairer2006book}

Hairer, Ernst; Lubich, Christian; Wanner, Gerhard. **Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations**. Springer, 2006・第2版.

シンプレクティック写像、対称合成法、分割法、後退誤差解析を調べるときに。シンプレクティック構造の保存と元のHamiltonianの厳密保存は異なります。

アトラスの関連章：[シンプレクティック積分：正準写像とエネルギーを分ける](symplectic.md) · [時間積分とleapfrog法](time-integration.md).

[出版社・書誌情報](https://doi.org/10.1007/3-540-30666-8) · [著者・参照ページ](https://link.springer.com/book/10.1007/3-540-30666-8) · `hairer2006book`

### Durran {#durran2010}

Durran, Dale R. **Numerical Methods for Fluid Dynamics: With Applications to Geophysics**. Springer, 2010・第2版.

地球流体の分散、移流、時間離散化を調べるときに。球面メッシュと変数配置の解説と合わせて参照してください。

アトラスの関連章：[球面メッシュとArakawa A・B・C格子](geophysical-grids.md) · [Runge–Kutta法：段数、次数、安定性、SSP](runge-kutta.md).

[出版社・書誌情報](https://doi.org/10.1007/978-1-4419-6412-0) · [著者・参照ページ](https://link.springer.com/book/10.1007/978-1-4419-6412-0) · `durran2010`

### Hockney · Eastwood {#hockney1981book}

Hockney, R. W.; Eastwood, J. W. **Computer Simulation Using Particles**. McGraw-Hill, 1981.

粒子・メッシュの考え方、力の割当て、Fourier変換による場の計算を調べるときに。初版は1981年で、リンク先DOIは後年の再刊です。

アトラスの関連章：[粒子重力：PM、P³M、ツリー、多重極、マルチグリッド](particle-gravity.md) · [重力核：孤立FFTと周期スラブ](gravity-boundaries.md).

[出版社・書誌情報](https://doi.org/10.1201/9780367806934) · [著者・参照ページ](https://doi.org/10.1201/9780367806934) · `hockney1981book`
