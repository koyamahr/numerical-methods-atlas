# 前処理、二重時間積分、残差分配法

## 条件数とPDE前処理 {#condition-numbers-and-pde-preconditioning}

`Ax=b`の2ノルム条件数は`κ₂(A)=σmax/σmin`です。特定の反復の収束率ではなく、摂動への感度を測ります。左前処理は`P^{-1}Ax=P^{-1}b`、右前処理は`AP^{-1}y=b, x=P^{-1}y`です。対称正定値系では、`P^{-1/2}AP^{-1/2}`によって対称性を保った比較ができます。

`conditioning_example`は`A=S B S`を構成し、Bを1次元Poisson行列、Sを対角スケーリングとします。対称Jacobiスケーリングによる条件数の変化を示すもので、Turkelの低Mach流前処理行列を実装するものではありません。

圧縮性PDEでは、低Mach数で対流と音響の特性速度が大きく異なると、別の前処理問題が生じます。`Γ(U) ∂U/∂τ + R(U)=0`のような擬似時間系は、特性速度、収束、数値散逸を変えます。Γの導出、変数変換、Mach数依存係数、境界の整合性には追加の検証が必要です。物理時間微分を無差別に置き換えると、時間依存解が変わります。[Turkel（1987）](https://doi.org/10.1016/0021-9991(87)90084-2)。

## 二重時間積分 {#dual-time-stepping}

`dU/dt+R(U)=0`に物理時間のBDF2を適用すると、

\[
\frac{3U^{n+1}-4U^n+U^{n-1}}{2\Delta t}+R(U^{n+1})=0.
\]

です。各物理ステップでQの擬似時間方程式、

\[
\frac{dQ}{d\tau}+\frac{3Q-4U^n+U^{n-1}}{2\Delta t}+R(Q)=0,
\]

を定常状態まで進めます。最初のステップは後退Eulerで開始します。物理時間の精度はΔt、空間誤差、内部の未収束に依存し、大きな物理CFL数だけでは正確な時間発展を示せません。[Jameson（1991）](https://doi.org/10.2514/6.1991-1596)。

`dual_time_advection`は最小の周期1次元例です。BDF1／BDF2の陰的風上移流を、Jacobi擬似時間反復で解きます。内部残差閾値は`tol*max(1,||b||∞)`、既定値は`tol=1e-10`です。反復上限までに収束しなければエラーにします。テストではBDF2離散方程式の独立した密行列解と比較します。Jamesonの圧縮性流体マルチグリッド全体ではなく、簡約モデルです。

## 残差分配法 {#residual-distribution-schemes}

要素残差`Φ_K=∫K ∇·F(U) dV`を節点へ配り、`Σ_{i∈K} Φ_i^K=Φ_K`を保ちます。この保存条件が連続有限要素と風上の考え方をつなぎます。[Abgrall（2006）の著者公開総説](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf)。

`rd_residual`は1次元P1スカラー移流の最小例です。`Φ_K=a(u_{i+1}-u_i)`全体を下流節点へ与え、集中質量hで割ります。この場合に1次風上差分と等価であることをテストします。2次元三角形のN／LDA、非線形混合、時間整合質量行列、Euler系は未実装です。

## Roe、エントロピー修正、Einfeldt、回転ソルバー {#roe-entropy-fixes-einfeldt-and-rotated-solvers}

Roeは`F_R-F_L=Ã(U_R-U_L)`を満たす線形化と固有系を使います。初版はsqrt(ρ)重みのu、Hと`ã²=(γ-1)(H̃-ũ²/2)`を作り、波強度と固有ベクトルによって散逸を加えます。[Roe（1981）](https://doi.org/10.1016/0021-9991(81)90128-5)。

エントロピー修正は、絶対値がδ未満の音響固有値を`(λ²+δ²)/(2δ)`で置き換えます。HLLEは、強い低密度膨張に対してEinfeldt型の左右波速を使う別の流束です。Roeのエントロピー修正、HLLEの正値性、カーバンクル処理は別の問題を扱います。[Einfeldt（1988）](https://doi.org/10.1137/0725021)、[Einfeldtら（1991）](https://doi.org/10.1016/0021-9991(91)90211-3)。

回転ハイブリッド・リーマンソルバーは面法線以外の方向も使って流束を組み合わせ、衝撃波に対する頑健性とせん断層の解像を両立させます。座標を回すだけではこの構成になりません。[方向分解HLLE/Roe合成と円柱前半部テスト](shock-expansion.md)を追加しました。明示的な2流束の実験であり、原型Rotated-RHLLの散逸式を最適化して再現したものとは区別します。[Nishikawa–Kitamura（2008）](https://doi.org/10.1016/j.jcp.2007.11.003)。


## RoeのProperty U {#roes-property-u}

[Roeの1981年論文の著者公開全文、359〜360頁](https://www.researchgate.net/publication/222453065_Approximate_Riemann_Solvers_Parameter_Vector_and_Difference_Schemes)の4条件は、(i)固定した状態対ごとに保存変数空間から流束空間への線形写像である、(ii)状態が一致する極限で物理Jacobianになる、(iii)状態ジャンプを流束ジャンプへ厳密に写す、(iv)固有ベクトルが線形独立、です。2状態への依存そのものが線形という意味ではありません。物理的な理想気体Eulerでは、以下の構成は実数の音響・接触速度も持ちます。

以下はアトラスで実装し、独立に検査する代数です。U=(ρ,ρu,E)、H=(E+p)/ρ、z=√ρ(1,u,H)とすると、

\[
 U(z)=\begin{pmatrix}z_1^2\\z_1z_2\\
 (z_1z_3+(\gamma-1)z_2^2/2)/\gamma\end{pmatrix},\qquad
 F(z)=\begin{pmatrix}z_1z_2\\
 ((\gamma+1)z_2^2/2+(\gamma-1)z_1z_3)/\gamma\\z_2z_3\end{pmatrix}.
\]

です。両方が2次式なので、中点のJacobian B=∂U/∂z、C=∂F/∂zはΔU=B(z̄)Δz、ΔF=C(z̄)Δzを厳密に満たします。したがってÃ=C(z̄)B(z̄)⁻¹はジャンプ条件を持ち、z̄の比から、

\[
 \widetilde u=\frac{\sqrt{\rho_L}u_L+\sqrt{\rho_R}u_R}{\sqrt{\rho_L}+\sqrt{\rho_R}},\quad
 \widetilde H=\frac{\sqrt{\rho_L}H_L+\sqrt{\rho_R}H_R}{\sqrt{\rho_L}+\sqrt{\rho_R}},\quad
 \widetilde c^2=(\gamma-1)(\widetilde H-\widetilde u^2/2).
\]

を得ます。同一状態では連鎖則からCB⁻¹=∂F/∂Uです。別に構成した固有系の速度はũ−c̃,ũ,ũ+c̃で、c̃>0なら3固有ベクトルが状態空間を張ります。パラメータ行列・固有基底・解析Jacobianと、決定的に生成した2000組の物理状態で照合します。

単一の非零Rankine–HugoniotジャンプΔF=sΔUならÃΔU=sΔUであり、そのジャンプは速度sの固有空間に属します。無修正Roe流束が孤立した接触面・衝撃波を認識する理由です。任意の再構成・時間離散化を施した衝撃波計算全体が厳密になる意味ではありません。|λ|の平滑化は行列恒等式を変えずに流束を変え、静止衝撃波を広げる場合があります。

膨張不連続もジャンプ関係を満たし得ます。静止垂直衝撃波の左右を逆転した対はProperty Uを満たしますが、無修正Roe流束はエントロピーを満たすリーマン参照と異なります。ジャンプ性質とエントロピー選択を同一視できない数値反例です。エントロピー修正は追加の設計で、いずれも多次元のカーバンクル保証ではありません。

![Roeの流束ジャンプ残差](figures/shock-methods/roe-property-u.png)

`python scripts/build_shock_robustness.py`で行列検査・移動／静止衝撃波・接触面・膨張反例を[診断マニフェスト](figures/shock-methods/robustness.json)に保存します。
