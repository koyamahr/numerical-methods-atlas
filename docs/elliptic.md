# 拡散、楕円型、境界条件と反復

## 放物型：拡散を時間発展させる

`u_t=νu_xx` を `[0,1]`、両端 `u=0`、初期値 `sin(πx)` で解きます。
参照解は `u=exp(-νπ²t)sin(πx)`。`numart.linear.diffusion_1d` は内部節点を返します。

中心 2 次の空間差分と θ 法を使うと

\[
(I-\theta\nu\Delta t D_{xx})u^{n+1}
=(I+(1-\theta)\nu\Delta t D_{xx})u^n.
\]

- θ=0：FTCS。`r=νΔt/h²≤1/2`。
- θ=1：後退 Euler。時間 1 次、線形拡散では無条件安定。
- θ=1/2：Crank–Nicolson。時間 2 次、線形拡散では A 安定。

Fourier モードの増幅率は `G=[1-4(1-θ)r sin²(ξ/2)]/[1+4θr sin²(ξ/2)]`。
CN は大きな r で G が負になり、安定でも高周波成分が符号反転します。
安定性、正値性、単調性、時間解像度はそれぞれ確認する必要があります。
[Crank–Nicolson (1947)](https://doi.org/10.1017/S0305004100023197)。

`spectral_diffusion` は別の周期問題で、各 Fourier 係数を `exp(-νk²t)` 倍します。
Dirichlet 問題の FD 解との比較では、境界条件の違いを揃えずに精度の優劣を主張しません。

## Thomas：陰的時間積分を三重対角系につなぐ

下対角 a、対角 b、上対角 c に対して、前進消去は
`m_i=a_i/b'_{i-1}`、`b'_i=b_i-m_i c_{i-1}`、`d'_i=d_i-m_i d'_{i-1}`。
後退代入は `x_i=(d'_i-c_i x_{i+1})/b'_i`。計算量・記憶量は O(N) です。

`thomas` は入力を変更せず、小さなピボットで明示的に失敗します。
ピボット選択のない消去法で、すべての三重対角行列に安全なわけではありません。
ここでの拡散行列は厳密対角優位です。
1949 年の Thomas 原報の本文は未確認なので、歴史記載と現代的な実装の検証を区別します。

## 楕円型：Poisson 方程式

符号は `-Δu=f` とします。1D では三重対角 + Thomas、2D では 5 点差分 + matrix-free CG または multigrid を使います。
既定の製造解は 1D `sin(πx)`、2D `sin(πx)sin(πy)`。
線形系の残差と、連続解に対する離散化誤差を別々に確認します。

## Dirichlet、Neumann、Robin

Dirichlet は境界値 `u=g_D`、Neumann は外向き法線微分 `∂u/∂n=g_N`、
Robin は `αu+β∂u/∂n=g` です。左端の法線微分は `-u_x`、右端は `+u_x`。
熱伝導の外向き熱流束は `-k∂u/∂n` なので、指定する量と符号を区別します。

`Boundary.dirichlet(value)`、`Boundary.neumann(value)`、`Boundary(alpha,beta,value)` を
`poisson_boundary_1d` に渡せます。Robin／Neumann は ghost point を消去し、端点の半重みを使います。
既定の時間発展 `diffusion_1d` は両端ゼロ Dirichlet に限定しています。

純 Neumann の Poisson は任意の定数を加えても同じ解です。
発散定理から適合条件

\[
\int_\Omega f\,dV=-\int_{\partial\Omega}g_N\,dS
\]

が必要です。実装では台形則に対応した離散適合条件を確認し、指定した平均値（既定 0）で定数を固定します。
Robin も係数次第で一意性が失われるため、一般に無条件で解けるとはしません。
周期境界では、両端を結び、周期 Poisson なら同様にゼロモードの適合条件と平均値指定が必要になります。

## 反復行列のスペクトル半径

`Ax=b` に対する定常反復 `x^{k+1}=T x^k+c` の誤差は `e^{k+1}=T e^k`。
有限次元では **任意の初期誤差に対して収束する必要十分条件は `ρ(T)<1`** です。
ここで `ρ(T)=max |λ_i(T)|`。
これは級数 `Σa_n z^n` の収束半径 `R=1/limsup |a_n|^{1/n}` とは別概念です。
Newton 反復の初期値について議論する「収束域」とも区別します。

`A=D+L+U` と書くと、Jacobi は `T=-D^{-1}(L+U)`、GS は `T=-(D+L)^{-1}U`、
SOR は `T=(D+ωL)^{-1}[(1-ω)D-ωU]`。
`iteration_matrix` と `spectral_radius` が小規模な行列で可視化を支えます。
非正規行列では ρ<1 でも一時的に誤差が増えうるため、ρだけで途中経過を保証しません。
条件数 κ(A) と反復行列の ρ(T) も別です。
[Netlib Templates](https://www.netlib.org/templates/templates.html)。

## red-black GS と SOR

5 点差分の節点を `(i+j) mod 2` で色分けすると、一つの色の更新は反対色の値だけを使います。
red を更新してから black を更新します。ω=1 は GS、`0<ω<2` の更新は SOR です。
この条件だけで任意の非対称問題の収束が保証されるわけではありません。
本実装は対称正定値の Dirichlet Poisson を対象にしています。

## 幾何学的 multigrid V-cycle

1. fine grid で red-black GS を 3 sweep。
2. 残差 `r_h=f_h-A_h u_h` を計算。
3. full weighting で coarse grid に制限。
4. coarse の誤差方程式を再帰的に解く。
5. bilinear prolongation で誤差補正。
6. fine grid で 3 sweep。

内部節点数は一辺 `N=2^k-1`。粗格子は再離散化した 5 点作用素で、最粗格子は未知数 1 個を直接解きます。
補間、制限、格子幅、境界条件の整合性を自動テストします。
この初版は可変係数、異方性、曲線格子、AMG、FAS を含みません。
[Fedorenko (1961)](https://www.mathnet.ru/eng/zvmmf8014)、
[Brandt (1977)](https://doi.org/10.1090/S0025-5718-1977-0431719-X)。
