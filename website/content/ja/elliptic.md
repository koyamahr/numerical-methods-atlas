# 拡散、楕円型方程式、境界条件、反復法

## 放物型問題：拡散を時間発展させる {#parabolic-problems-evolving-diffusion}

区間`[0,1]`でゼロDirichlet境界と初期値`sin(πx)`を与え、`u_t=νu_xx`を解きます。参照解は`u=exp(-νπ²t)sin(πx)`です。`numart.linear.diffusion_1d`は内部節点の値を返します。

空間2次中心差分とθ法を組み合わせると、

\[
(I-\theta\nu\Delta t D_{xx})u^{n+1}
=(I+(1-\theta)\nu\Delta t D_{xx})u^n.
\]

となります。

- θ=0：FTCS。`r=νΔt/h²≤1/2`が必要です。
- θ=1：後退Euler法。時間1次精度で、線形拡散に対して無条件安定です。
- θ=1/2：Crank–Nicolson法。時間2次精度で、線形拡散に対してA安定です。

Fourier増幅係数は`G=[1-4(1-θ)r sin²(ξ/2)]/[1+4θr sin²(ξ/2)]`です。rが大きいとCrank–NicolsonではGが負になり、高周波モードは安定なまま符号を交互に変えます。安定性、正値性、単調性、時間解像度は別々に確認します。[Crank–Nicolson（1947）](https://doi.org/10.1017/S0305004100023197)。

`spectral_diffusion`は別の周期問題を解き、各Fourier係数に`exp(-νk²t)`を掛けます。Dirichlet差分問題と精度を比べる際は、境界条件の違いを考慮します。

## Thomas消去：陰的時間積分から三重対角系へ {#thomas-elimination-from-implicit-steps-to-tridiagonal-systems}

下側対角をa、対角をb、上側対角をcとすると、前進消去は`m_i=a_i/b'_{i-1}`、`b'_i=b_i-m_i c_{i-1}`、`d'_i=d_i-m_i d'_{i-1}`です。後退代入は`x_i=(d'_i-c_i x_{i+1})/b'_i`です。計算量と記憶量はともにO(N)です。

`thomas`は入力を変更せず、小さなピボットでエラーにします。ピボット選択を行わないため、任意の三重対角行列に安全に使えるわけではありません。ここでの拡散行列は狭義対角優位です。1949年のThomas報告の原文は未確認で、歴史的な引用と現代の実装の検証は別の主張です。

## 楕円型問題：Poisson方程式 {#elliptic-problems-the-poisson-equation}

符号規約は`-Δu=f`です。1次元では三重対角系とThomas消去、2次元では5点差分と行列を陽に作らない共役勾配法またはマルチグリッドを使います。既定の製造解は1次元の`sin(πx)`と2次元の`sin(πx)sin(πy)`です。線形方程式の残差と、連続解に対する離散化誤差を分けて確認します。

## Dirichlet・Neumann・Robin境界条件 {#dirichlet-neumann-and-robin-boundaries}

Dirichlet条件は値`u=g_D`、Neumann条件は外向き法線微分`∂u/∂n=g_N`、Robin条件は`αu+β∂u/∂n=g`を指定します。法線微分は左端で`-u_x`、右端で`+u_x`です。外向きの伝導熱流束は`-k∂u/∂n`なので、何を指定したかと符号の両方が重要です。

`poisson_boundary_1d`に`Boundary.dirichlet(value)`、`Boundary.neumann(value)`、または`Boundary(alpha,beta,value)`を渡します。Robin・Neumann条件では仮想点を消去し、端点の重みを半分にします。時間依存の`diffusion_1d`は、現在ゼロDirichlet境界に対応しています。

純NeumannのPoisson解は、加法定数を除いてしか決まりません。発散定理から、

\[
\int_\Omega f\,dV=-\int_{\partial\Omega}g_N\,dS.
\]

が必要です。実装は台形求積に対応する離散適合条件を確認し、指定した平均で定数を固定します。既定平均はゼロです。Robin係数によっても一意性が失われる場合があります。周期Poisson問題も、端点を同一視したうえでゼロモードの適合条件と平均の制約が必要です。

## 反復行列のスペクトル半径 {#spectral-radius-of-the-iteration-matrix}

`Ax=b`を解く定常反復`x^{k+1}=T x^k+c`では、誤差は`e^{k+1}=T e^k`に従います。有限次元では、**すべての初期誤差について収束することと`ρ(T)<1`は同値**です。ここで`ρ(T)=max |λ_i(T)|`をスペクトル半径（spectral radius）と呼びます。べき級数の収束半径`R=1/limsup |a_n|^{1/n}`や、Newton反復の収束域とは異なります。

`A=D+L+U`とすると、Jacobiは`T=-D^{-1}(L+U)`、Gauss–Seidelは`T=-(D+L)^{-1}U`、SORは`T=(D+ωL)^{-1}[(1-ω)D-ωU]`です。`iteration_matrix`と`spectral_radius`で小行列の例を調べられます。非正規行列は`ρ<1`でも一時的に誤差が増える場合があります。系の条件数`κ(A)`と反復行列のスペクトル半径`ρ(T)`は異なる性質を測ります。[Netlib Templates](https://www.netlib.org/templates/templates.html)。

## 赤黒Gauss–Seidel法とSOR {#red-black-gaussseidel-and-sor}

5点差分格子を`(i+j) mod 2`で2色に分けます。一方の色の更新は他方の色だけに依存するため、赤、黒の順に更新します。`ω=1`がGauss–Seidelで、SOR緩和には`0<ω<2`を使います。ただし、この範囲だけで任意の非対称系の収束を保証することはできません。実装対象は、対称正定値のDirichlet Poisson問題です。

## 幾何マルチグリッドのVサイクル {#geometric-multigrid-v-cycle}

1. 細格子で赤黒Gauss–Seidelを3回スイープします。
2. `r_h=f_h-A_h u_h`を計算します。
3. 全重み付け（full weighting）で残差を粗格子へ制限します。
4. 粗格子の誤差方程式を再帰的に解きます。
5. 双線形補間で補正を細格子へ延長します。
6. 細格子でさらに3回スイープします。

各辺の内部節点数は`N=2^k-1`です。粗格子では5点演算子を再離散化し、未知数が1つの最粗格子は直接解きます。テストでは補間、制限、格子間隔、境界の整合性を確認します。変係数、異方性、曲線格子、代数マルチグリッド（AMG）、完全近似方式（FAS）は初版の範囲外です。[Fedorenko（1961）](https://www.mathnet.ru/eng/zvmmf8014)、[Brandt（1977）](https://doi.org/10.1090/S0025-5718-1977-0431719-X)。

## 粒子と円盤の重力 {#particle-and-disk-gravity}

[粒子重力の章](particle-gravity.md)はPM、P³M、ツリー、多重極、マルチグリッドをつなぎます。[重力境界核](gravity-boundaries.md)はHockney–Eastwoodの孤立畳み込みとKoyama–OstrikerのスラブFourier核を加えます。既存のマルチグリッド例は2次元ゼロDirichlet演算子を維持し、3次元開放境界の重力ソルバーではありません。

## 拡散・楕円型問題への別の道 {#further-routes-to-diffusion-and-elliptic-problems}

弱形式の組立ては[連続P1 FEM](fem.md)、非対称系は[GMRES／ILUと非線形解法](sparse-nonlinear.md)、補助勾配による擬似時間反復は[西川の双曲型拡散法](hyperbolic-diffusion.md)を参照してください。[方程式ギャラリー](equation-gallery.md)では物理時間での熱拡散を別に示します。

**A安定性・L安定性とL1／L2／L∞誤差ノルム**の定義と比較は、[精度と安定性の共通ガイド](accuracy-stability.md)を参照してください。
