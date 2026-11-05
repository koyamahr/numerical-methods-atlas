# 粒子法と平滑化粒子流体力学

Lagrange粒子は流れとともに移動しながら量を運びます。SPHは場の値や微分を、局所カーネルで重み付けした粒子和で近似します。独立した初期論文[Gingold・Monaghan（1977）](https://doi.org/10.1093/mnras/181.3.375)と[Lucy（1977）](https://doi.org/10.1086/112164)が歴史的な出発点です。以下の静的再構成は、原著の恒星計算を再現するものではありません。

## 積分から粒子へ {#from-an-integral-to-particles}

平滑化した場を、

\[
f_h(x)=\int f(x')W(x-x',h)\,dx'
\approx\sum_b \frac{m_b}{\rho_b} f_b W(x-x_b,h).
\]

で近似します。体積重みm_b/rho_bが重要です。平滑化長hはカーネルの尺度で、必ずしも粒子間隔ではありません。コンパクトな台が近傍探索を定めますが、固定格子の接続を課すわけではありません。

1次元例では、q=|x|/hとして規格化した3次スプラインを使います。

\[
W(x,h)=\frac{2}{3h}\begin{cases}
1-\frac32q^2+\frac34q^3,&0\le q<1,\\
\frac14(2-q)^3,&1\le q<2,\\
0,&q\ge2.
\end{cases}
\]

この係数は**1次元**のものです。2・3次元では別の規格化定数が必要です。

## 1の分割と補正 {#partition-of-unity-and-correction}

離散粒子集合では、粒子体積とWの積の総和は1とは限りません。Shepard規格化補間は、その総和で割ります。分母がゼロでなければ定数を再現しますが、この補間補正だけで保存的な運動、線形整合性、安定な圧力力が保証されるわけではありません。

```python
import numpy as np
from numart.geometry import sph_reconstruct
p = (np.arange(64) + 0.5) / 64
x = np.linspace(0, 1, 201)
f, partition = sph_reconstruct(x, p, np.sin(2*np.pi*p), h=0.04)
f_corrected, _ = sph_reconstruct(x, p, np.sin(2*np.pi*p), h=0.04, normalize=True)
```

この関数は[0,1]の周期最小像距離と、等しい体積重み1/Nを使います。台が最小像の規約に収まるよう、0<h<1/4が必要です。任意の不等間隔粒子から物理密度を推定するものではありません。

## 流体ソルバーに追加で必要なもの {#what-a-fluid-solver-would-additionally-need}

密度推定または連続の式の更新、整合する圧力力、運動量・エネルギー発展、境界粒子、時間積分、近傍探索更新、衝撃波や引張り・ペアリング不安定性の扱いは、追加のモデル選択です。衝撃波捕獲SPHの人工粘性は、物理的なNewton流体の[粘性応力テンソル](coordinates-viscosity.md)と区別します。

テストでは連続カーネルの規格化と、補正後の離散定数再現を確認します。初版は**カーネル再構成のみ**で、SPH流体ソルバーではありません。[時間積分](time-integration.md)では、粒子kick–drift leapfrogと1階ODEの2ステップleapfrogを混同しない理由を説明します。

## 粒子重力は別の演算子 {#particle-gravity-is-a-separate-operator}

PM、P³M、ツリー、多重極は重力場を計算し、SPHカーネルは流体量と微分を再構成します。[粒子重力](particle-gravity.md)、[孤立・スラブ境界核](gravity-boundaries.md)、[シンプレクティック時間積分](symplectic.md)で、自己重力粒子モデルの異なる構成要素を結び付けてください。

## Godunov SPH：リーマンソルバーへの分岐 {#godunov-sph-the-riemann-solver-branch}

[InutsukaのGSPH](gsph.md)は粒子流体と粒子対のリーマン問題を結び付けます。2002年の畳み込みによる導出、1994年の先行研究、Iwasaki・Inutsukaの2011年MHD拡張をたどる文献ノートと実装計画です。上のカーネル再構成はGSPH流体計算ではありません。
