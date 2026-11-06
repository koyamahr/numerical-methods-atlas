# 教科書案内：次に何を調べるか

このアトラスから参照するための書棚です。知りたい問いから選ぶ読書案内で、順位付けではありません。以下の年は引用する版の年であり、アルゴリズムの発明年ではありません。

リンク先は出版社の書誌情報や著者管理のページです。版情報と公開されている紹介・目次を確認しており、各書のすべての導出を点検したという意味ではありません。関連章はアトラスとの接点を示し、教科書全体の実装を意味しません。

**最初の道筋：** CFDの枠組みにはHirsch、保存則と有限体積法の考え方にはLeVeque、RiemannソルバーにはToro、圧力・速度連成にはPatankar、疎行列の反復解法にはSaad。個々の手法の由来を追うときは原論文にも戻ってください。

[参考文献庫を検索](#/references) · [登録済みの書籍のみ](#/references?q=type%3Abook) · [BibTeXをダウンロード](../references.bib)

表紙は記載したISBNに対応する[Open Library](https://openlibrary.org/dev/docs/api/covers)の画像を表示します。各カードにAmazon Japanと出版社・書誌情報へのリンクがあります。表紙を取得できない場合も書名を表示します。

## CFDの基礎と非圧縮流れ {#cfd-foundations}

<section class="textbook-card" aria-labelledby="hirsch2007">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780750665940" target="_blank" rel="noopener" aria-label="Open Library: Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780750665940" target="_blank" rel="noopener">Open Libraryの書誌情報</a>
<span class="book-isbn">ISBN 9780750665940</span>
</div>
<div class="textbook-details">

### Hirsch {#hirsch2007}

Hirsch, Charles. **Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics**. Butterworth-Heinemann, 2007・第2版.

支配方程式、格子の性質、整合性・安定性、離散化から解法まで、CFD全体の枠組みを調べる本です。引用する2007年版は第2版の基礎巻です。

アトラスの関連章：[差分、CFL条件、von Neumann解析、Laxの定理](stability.md) · [構造格子、非構造格子、三角形格子](meshes.md) · [時間積分とleapfrog法](time-integration.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0750665947" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1016/B978-0-7506-6594-0.X5037-1" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://www.sciencedirect.com/book/monograph/9780750665940/numerical-computation-of-internal-and-external-flows" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>hirsch2007</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="fletcher1991v1">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540530589" target="_blank" rel="noopener" aria-label="Open Library: Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2225072-M.jpg?default=false" alt="表紙：Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540530589" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9783540530589</span>
</div>
<div class="textbook-details">

### Fletcher / Volume I {#fletcher1991v1}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques**. Springer, 1991・第2版.

I巻はPDEの分類、重み付き残差法、定常・拡散問題、線形・非線形移流を調べるために。II巻の流れ別の解法に進む前の共通の数値的道具を扱います。

アトラスの関連章：[差分、CFL条件、von Neumann解析、Laxの定理](stability.md) · [連続有限要素法：弱形式から疎行列の組立てへ](fem.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540530584" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-642-58229-5" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-642-58229-5" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>fletcher1991v1</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="fletcher1991v2">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9783540536017" target="_blank" rel="noopener" aria-label="Open Library: Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540536017" target="_blank" rel="noopener">Open Libraryの書誌情報</a>
<span class="book-isbn">ISBN 9783540536017</span>
</div>
<div class="textbook-details">

### Fletcher / Volume II {#fletcher1991v2}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories**. Springer, 1991・第2版.

II巻はI巻の一般的手法を、流れの方程式の各分類とその数値解法に結びつけるために。各アルゴリズムと合わせて仮定や境界条件も確認します。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [前処理、二重時間積分、残差分配法](advanced.md) · [極・円筒座標：テンソルと粘性](coordinates-viscosity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540536019" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-642-58239-4" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-642-58239-4" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>fletcher1991v2</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="ferziger2020">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783319996912" target="_blank" rel="noopener" aria-label="Open Library: Computational Methods for Fluid Dynamics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Methods for Fluid Dynamics</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/10130550-M.jpg?default=false" alt="表紙：Computational Methods for Fluid Dynamics" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783319996912" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9783319996912</span>
</div>
<div class="textbook-details">

### Ferziger · Perić · Street {#ferziger2020}

Ferziger, Joel H.; Perić, Milovan; Street, Robert L. **Computational Methods for Fluid Dynamics**. Springer, 2020・第4版.

離散演算子を実際のCFD計算手順に結びつける際に。特に非圧縮流れの圧力・速度連成や境界条件を調べる入口です。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [極・円筒座標：テンソルと粘性](coordinates-viscosity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3319996916" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-319-99693-6" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-319-99693-6" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>ferziger2020</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="patankar1980">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780891165224" target="_blank" rel="noopener" aria-label="Open Library: Numerical Heat Transfer and Fluid Flow">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Heat Transfer and Fluid Flow</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/12927123-M.jpg?default=false" alt="表紙：Numerical Heat Transfer and Fluid Flow" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780891165224" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780891165224</span>
</div>
<div class="textbook-details">

### Patankar {#patankar1980}

Patankar, Suhas V. **Numerical Heat Transfer and Fluid Flow**. CRC Press (current publisher record), 1980.

コントロールボリュームの収支とSIMPLE型の圧力・速度連成を、物理的な考え方から理解したいときに。教科書の解説と手法の原論文は区別します。

アトラスの関連章：[非圧縮流：整合する離散演算子で射影する](incompressible.md) · [Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0891165223" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<code>patankar1980</code></p>

</div>
</section>

## 保存則・Riemannソルバー・衝撃波 {#hyperbolic}

<section class="textbook-card" aria-labelledby="leveque2002">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780521009249" target="_blank" rel="noopener" aria-label="Open Library: Finite Volume Methods for Hyperbolic Problems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Finite Volume Methods for Hyperbolic Problems</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/328569-M.jpg?default=false" alt="表紙：Finite Volume Methods for Hyperbolic Problems" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780521009249" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780521009249</span>
</div>
<div class="textbook-details">

### LeVeque / finite volume {#leveque2002}

LeVeque, Randall J. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press, 2002.

弱解、有限体積法の考え方、波の伝播、リミター、多次元保存則を調べるときに。Clawpack関連資料から理論と実装を結びつけられます。

アトラスの関連章：[Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md) · [勾配制限：minmod、Superbee、MC、van Leer、van Albada](limiters.md) · [方程式ギャラリー：計算法の前に方程式を選ぶ](equation-gallery.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0521009243" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1017/CBO9780511791253" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>leveque2002</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="toro2009">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540252023" target="_blank" rel="noopener" aria-label="Open Library: Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/7368028-M.jpg?default=false" alt="表紙：Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540252023" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9783540252023</span>
</div>
<div class="textbook-details">

### Toro {#toro2009}

Toro, Eleuterio F. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer, 2009・第3版.

Euler方程式の厳密・近似Riemannソルバー、接触波、高解像度の衝撃波捕獲法を導出・比較したいときに。

アトラスの関連章：[前処理、二重時間積分、残差分配法](advanced.md) · [Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md) · [テスト計算ライブラリ](benchmarks.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540252029" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/b79761" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<code>toro2009</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="godlewski1996book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780387945293" target="_blank" rel="noopener" aria-label="Open Library: Numerical Approximation of Hyperbolic Systems of Conservation Laws">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Approximation of Hyperbolic Systems of Conservation Laws</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/245411-M.jpg?default=false" alt="表紙：Numerical Approximation of Hyperbolic Systems of Conservation Laws" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780387945293" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780387945293</span>
</div>
<div class="textbook-details">

### Godlewski · Raviart {#godlewski1996book}

Godlewski, Edwige; Raviart, Pierre-Arnaud. **Numerical Approximation of Hyperbolic Systems of Conservation Laws**. Springer, 1996・第1版.

非線形双曲型保存則系とその数値近似を数学的に学び、Riemann問題や気体力学を詳しく調べるための本です。有限体積法の考え方にはLeVeque、ソルバーの構成にはToroを併読するとつながります。この項目は1996年初版を引用し、[2021年の改訂第2版](https://link.springer.com/book/10.1007/978-1-0716-1344-3)も案内します。

アトラスの関連章：[前処理、二重時間積分、残差分配法](advanced.md) · [Euler再構成：PPM・特性変数・WENO-Z・AUSM](reconstruction.md) · [A安定性、L安定性、誤差ノルム](accuracy-stability.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0387945296" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-1-4612-0713-9" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-1-4612-0713-9" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>godlewski1996book</code></p>

</div>
</section>

## 差分法と線形代数 {#common-numerics}

<section class="textbook-card" aria-labelledby="leveque2007">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780898716290" target="_blank" rel="noopener" aria-label="Open Library: Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898716290" target="_blank" rel="noopener">Open Libraryの書誌情報</a>
<span class="book-isbn">ISBN 9780898716290</span>
</div>
<div class="textbook-details">

### LeVeque / finite differences {#leveque2007}

LeVeque, Randall J. **Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems**. SIAM, 2007.

整合性・安定性・収束の関係、常微分方程式、境界値問題、偏微分方程式の差分法を調べるときに。

アトラスの関連章：[A安定性、L安定性、誤差ノルム](accuracy-stability.md) · [時間積分とleapfrog法](time-integration.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898716292" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898717839" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://staff.washington.edu/rjl/booksnotes.html" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>leveque2007</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="golub2013">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9781421407944" target="_blank" rel="noopener" aria-label="Open Library: Matrix Computations">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Matrix Computations</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/8779096-M.jpg?default=false" alt="表紙：Matrix Computations" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9781421407944" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9781421407944</span>
</div>
<div class="textbook-details">

### Golub · Van Loan {#golub2013}

Golub, Gene H.; Van Loan, Charles F. **Matrix Computations**. Johns Hopkins University Press, 2013・第4版.

手法名だけでソルバーを選ぶ前に、条件数、安定な行列分解、最小二乗、固有値問題を確認するための本です。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/1421407949" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9781421407944" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://epubs.siam.org/doi/book/10.1137/1.9781421407944" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>golub2013</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="saad2003book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898715347" target="_blank" rel="noopener" aria-label="Open Library: Iterative Methods for Sparse Linear Systems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Iterative Methods for Sparse Linear Systems</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698819-M.jpg?default=false" alt="表紙：Iterative Methods for Sparse Linear Systems" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898715347" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780898715347</span>
</div>
<div class="textbook-details">

### Saad {#saad2003book}

Saad, Yousef. **Iterative Methods for Sparse Linear Systems**. SIAM, 2003・第2版.

Krylov部分空間、GMRES、BiCG系の手法、前処理を調べるときに。著者のページで第2版の本文と訂正情報が公開されています。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898715342" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898718003" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://www-users.cse.umn.edu/~saad/books.html" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>saad2003book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="templates1994">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898713282" target="_blank" rel="noopener" aria-label="Open Library: Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698646-M.jpg?default=false" alt="表紙：Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898713282" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780898713282</span>
</div>
<div class="textbook-details">

### Barrett et al. / Templates {#templates1994}

Barrett, Richard; Berry, Michael; Chan, Tony F.; Demmel, James; Donato, June; Dongarra, Jack; Eijkhout, Victor; Pozo, Roldan; Romine, Charles; van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM, 1994.

行列に必要な仮定を確認しながら、反復線形解法のアルゴリズムと選び方を手短に引く公開リファレンスです。

アトラスの関連章：[疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [拡散、楕円型方程式、境界条件、反復法](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898713285" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://www.netlib.org/templates/templates.html" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<code>templates1994</code></p>

</div>
</section>

## マルチグリッド：直観・解析・実装 {#multigrid}

<section class="textbook-card" aria-labelledby="briggs2000book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898714623" target="_blank" rel="noopener" aria-label="Open Library: A Multigrid Tutorial">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>A Multigrid Tutorial</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698765-M.jpg?default=false" alt="表紙：A Multigrid Tutorial" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898714623" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780898714623</span>
</div>
<div class="textbook-details">

### Briggs · Henson · McCormick / A Multigrid Tutorial {#briggs2000book}

Briggs, William L.; Henson, Van Emden; McCormick, Steve F. **A Multigrid Tutorial**. SIAM, 2000・第2版.

緩和法が振動的な誤差を減らし、粗格子が残った滑らかな誤差を扱う理由を知る入口です。モデル問題から残差補正、制限・延長、マルチグリッドサイクルの実装へ進めます。第2版では非線形問題やAMGも導入します。

アトラスの関連章：[拡散、楕円型方程式、境界条件、反復法](elliptic.md) · [疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898714621" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898719505" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://epubs.siam.org/doi/book/10.1137/1.9780898719505" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>briggs2000book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="trottenberg2001">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780127010700" target="_blank" rel="noopener" aria-label="Open Library: Multigrid">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Multigrid</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/1100584-M.jpg?default=false" alt="表紙：Multigrid" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780127010700" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780127010700</span>
</div>
<div class="textbook-details">

### Trottenberg · Oosterlee · Schüller / Multigrid {#trottenberg2001}

Trottenberg, Ulrich; Oosterlee, Cornelius W.; Schüller, Anton. **Multigrid**. Academic Press, 2001・第1版.

入門の次に引く詳しい参考書です。マルチグリッドの基礎理論、局所Fourier解析、スムーザーと粗格子の選び方、並列実装、連立系、付録のAMGを調べられます。アトラスのPoisson比較では、サイクルが収束する理由と仕事量を考えるために参照します。AMG・異方性・並列性能には個別の実装と検証が必要です。

アトラスの関連章：[拡散、楕円型方程式、境界条件、反復法](elliptic.md) · [疎行列・非線形方程式系：真の残差を測る](sparse-nonlinear.md) · [粒子重力：PM、P³M、ツリー、多重極、マルチグリッド](particle-gravity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/012701070X" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://shop.elsevier.com/books/multigrid/trottenberg/978-0-08-047956-9" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<code>trottenberg2001</code></p>

</div>
</section>

## スペクトル基底と不連続Galerkin法 {#high-order}

<section class="textbook-card" aria-labelledby="trefethen2000">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898714654" target="_blank" rel="noopener" aria-label="Open Library: Spectral Methods in MATLAB">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Spectral Methods in MATLAB</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698768-M.jpg?default=false" alt="表紙：Spectral Methods in MATLAB" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898714654" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780898714654</span>
</div>
<div class="textbook-details">

### Trefethen {#trefethen2000}

Trefethen, Lloyd N. **Spectral Methods in MATLAB**. SIAM, 2000.

スペクトル微分、Fourier・Chebyshevの例、短い再現用プログラムを調べるときに。重心補間の扱いは限られるため補足資料も参照します。

アトラスの関連章：[インタラクティブ実験ガイド](experiments.md) · [Orthogonal polynomials and mesh basis functions](basis-functions.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898714656" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898719598" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://people.maths.ox.ac.uk/trefethen/spectral.html" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>trefethen2000</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="hesthaven2008book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780387720654" target="_blank" rel="noopener" aria-label="Open Library: Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2412519-M.jpg?default=false" alt="表紙：Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780387720654" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9780387720654</span>
</div>
<div class="textbook-details">

### Hesthaven · Warburton {#hesthaven2008book}

Hesthaven, Jan S.; Warburton, Tim. **Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications**. Springer, 2008.

節点多項式基底、求積、参照要素の演算子を、DGの要素間流束やPDE計算法につなげるための本です。

アトラスの関連章：[Orthogonal polynomials and mesh basis functions](basis-functions.md) · [インタラクティブ実験ガイド](experiments.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0387720650" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-0-387-72067-8" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-0-387-72067-8" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>hesthaven2008book</code></p>

</div>
</section>

## 時間積分・地球流体・粒子法 {#time-geophysics-particles}

<section class="textbook-card" aria-labelledby="hairer2006book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540306634" target="_blank" rel="noopener" aria-label="Open Library: Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2221190-M.jpg?default=false" alt="表紙：Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540306634" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9783540306634</span>
</div>
<div class="textbook-details">

### Hairer · Lubich · Wanner {#hairer2006book}

Hairer, Ernst; Lubich, Christian; Wanner, Gerhard. **Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations**. Springer, 2006・第2版.

シンプレクティック写像、対称合成法、分割法、後退誤差解析を調べるときに。シンプレクティック構造の保存と元のHamiltonianの厳密保存は異なります。

アトラスの関連章：[シンプレクティック積分：正準写像とエネルギーを分ける](symplectic.md) · [時間積分とleapfrog法](time-integration.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540306633" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/3-540-30666-8" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/3-540-30666-8" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>hairer2006book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="durran2010">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9781441964113" target="_blank" rel="noopener" aria-label="Open Library: Numerical Methods for Fluid Dynamics: With Applications to Geophysics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Methods for Fluid Dynamics: With Applications to Geophysics</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/8701007-M.jpg?default=false" alt="表紙：Numerical Methods for Fluid Dynamics: With Applications to Geophysics" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9781441964113" target="_blank" rel="noopener">表紙出典：Open Library</a>
<span class="book-isbn">ISBN 9781441964113</span>
</div>
<div class="textbook-details">

### Durran {#durran2010}

Durran, Dale R. **Numerical Methods for Fluid Dynamics: With Applications to Geophysics**. Springer, 2010・第2版.

地球流体の分散、移流、時間離散化を調べるときに。球面メッシュと変数配置の解説と合わせて参照してください。

アトラスの関連章：[球面メッシュとArakawa A・B・C格子](geophysical-grids.md) · [Runge–Kutta法：段数、次数、安定性、SSP](runge-kutta.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/1441964118" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-1-4419-6412-0" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<a href="https://link.springer.com/book/10.1007/978-1-4419-6412-0" target="_blank" rel="noopener">著者・参照資料 ↗</a>
<code>durran2010</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="hockney1981book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780070291089" target="_blank" rel="noopener" aria-label="Open Library: Computer Simulation Using Particles">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computer Simulation Using Particles</span><span class="book-cover-loading">表紙を読み込み中</span><span class="book-cover-unavailable">表紙画像なし</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780070291089" target="_blank" rel="noopener">Open Libraryの書誌情報</a>
<span class="book-isbn">ISBN 9780070291089</span>
</div>
<div class="textbook-details">

### Hockney · Eastwood {#hockney1981book}

Hockney, R. W.; Eastwood, J. W. **Computer Simulation Using Particles**. McGraw-Hill, 1981.

粒子・メッシュの考え方、力の割当て、Fourier変換による場の計算を調べるときに。初版は1981年で、リンク先DOIは後年の再刊です。

アトラスの関連章：[粒子重力：PM、P³M、ツリー、多重極、マルチグリッド](particle-gravity.md) · [重力核：孤立FFTと周期スラブ](gravity-boundaries.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/007029108X" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1201/9780367806934" target="_blank" rel="noopener">出版社・書誌情報 ↗</a>
<code>hockney1981book</code></p>

</div>
</section>
