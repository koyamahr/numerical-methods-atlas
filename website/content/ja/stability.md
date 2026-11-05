# 差分、CFL条件、von Neumann解析、Laxの定理

[安定性実験室](#/experiments)と[実験ガイド](experiments.md)で、以下の式をブラウザー内の計算と結び付けて確かめられます。

## 空間と時間の離散化を別々に選ぶ {#choose-space-and-time-discretizations-separately}

前進差分（forward difference）、後退差分（backward difference）、中心差分（centered difference）は、それぞれ次のように定義します。

\[
D_+u_j=\frac{u_{j+1}-u_j}{h},\qquad
D_-u_j=\frac{u_j-u_{j-1}}h,\qquad
D_0u_j=\frac{u_{j+1}-u_{j-1}}{2h}.
\]

滑らかな関数に対して、前二者は1次、中心差分は2次精度です。`numart.advection.finite_difference`で比較できます。線形移流`u_t+a u_x=0`の風上差分（upwind difference）は情報の伝播方向に従い、`a>0`では後退差分、`a<0`では前進差分を使います。したがって、前進差分と風上差分は同じ意味ではありません。

時間方向の前進Euler法は`u^{n+1}=u^n+Δt L_h u^n`、後退Euler法は`u^{n+1}=u^n+Δt L_h u^{n+1}`で、後者では方程式系を解きます。空間に後退差分を使うだけで陰解法になるわけではありません。

## CFL条件と数値的な依存領域 {#cfl-can-the-stencil-reach-the-information-it-needs}

定係数・周期移流を隣接格子点までの陽的差分で解く場合、依存領域の議論から`|a|Δt/h ≤ 1`が必要です。この定数は差分、Runge–Kutta法、DGの次数、次元によって変わります。陽的拡散には`Δt=O(h²)`の制約が現れます。CFL条件は一般に安定性の必要条件であり、十分条件ではありません。[Courant–Friedrichs–Lewy（1928）](https://doi.org/10.1007/BF01448839)。

時間前進・空間中心差分（FTCS）の移流が反例です。Fourierモード`u_j^n=G^n e^{ijθ}`を代入すると、

\[
G=1-i C\sin θ,\quad |G|^2=1+C^2\sin^2 θ,
\qquad C=a\Delta t/h.
\]

となり、`|C|<1`でも増幅するモードがあります。通常のCFL数を固定した格子細分化に対して、この方式は不安定です。

## Lax–Friedrichs法とLax–Wendroff法 {#laxfriedrichs-and-laxwendroff}

古典的なLax–Friedrichs法は、

\[
u_j^{n+1}=\tfrac12(u_{j+1}^n+u_{j-1}^n)
-\tfrac C2(u_{j+1}^n-u_{j-1}^n),\qquad
G=\cos θ-iC\sin θ.
\]

です。`|G|²=1-(1-C²)sin²θ`より、この周期線形移流問題では`|C|≤1`で安定です。古典的LFの数値粘性係数は`h/Δt`です。Rusanov流束は局所最大波速を使い、本実装のWENOは大域LF流束分割を使います。これらは異なる離散構成です。[Lax（1954）](https://doi.org/10.1002/cpa.3160070112)。

Lax–Wendroff法は、

\[
u_j^{n+1}=u_j^n-\tfrac C2(u_{j+1}^n-u_{j-1}^n)
+\tfrac{C^2}{2}(u_{j+1}^n-2u_j^n+u_{j-1}^n),
\]

であり、増幅係数は、

\[
G=1-iC\sin θ+C^2(\cos θ-1),\quad
|G|^2=1-4C^2(1-C^2)\sin^4(θ/2).
\]

です。この問題での安定条件は同じく`|C|≤1`です。2次精度であること自体は、不連続近傍の振動を抑える保証にはなりません。[Lax–Wendroff（1960）](https://doi.org/10.1002/cpa.3160130205)。

テストでは`amplification`による解析的な増幅係数と、`difference_step`による実際のモード発展を比較します。図では小さなNyquist摂動を加え、`C=0.8`と`C=1.1`を比較しています。

![Fourier増幅係数と数値的な移流](figures/stability.png)

## Lax–Richtmyerの同値定理 {#the-laxrichtmyer-equivalence-theorem}

適切なBanach空間上の**適切に設定された線形初期値問題**と、**整合的な線形差分近似**を考えます。固定した有限時間区間で離散発展演算子が一様有界であることを安定性とすると、安定性と収束性は同値です。[Lax–Richtmyer（1956）の原論文](https://math.berkeley.edu/~wilken/228B.S07/LaxRichtmyer.pdf)。

誤差を`e^{n+1}=S_h e^n+Δt τ^n`と書けば、`||S_h^m||≤M_T`から`||e^n||≤M_T||e^0||+M_T T max||τ^k||`を得ます。整合性により打切り誤差の項がゼロへ向かい、安定性から収束性を導く基本的な議論になります。逆向きには一様有界性の議論が必要です。

この定理から、非線形Euler、WENO、衝撃波、任意の境界処理の正しさを直接保証することはできません。ここでのFourier条件`|G|≤1`は、周期・定係数のスカラー問題に適用しています。境界、変係数、非正規行列、多段階法には追加の解析が必要です。

## 初版で用いる時間刻み {#time-steps-in-the-first-edition}

- Euler系・バロトロピック系：`Δt=C h/max(|u|+c)`、既定値`C=0.3`。
- DG：`Δt=C h/((2p+1)|a|)`、既定値`C=0.2`。
- 2次元MHD：`Δt=C/[max(s_x)/h+max(s_y)/h]`、既定値`C=0.3`。

これらは選定した例で確認した控えめな設定です。すべての初期条件に対する厳密な非線形安定限界ではありません。

**A安定性・L安定性とL1／L2／L∞誤差ノルム**の定義と比較は、[精度と安定性の共通ガイド](accuracy-stability.md)を参照してください。
