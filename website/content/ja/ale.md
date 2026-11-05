# 任意Lagrange–Euler法

Euler型セルは固定され、流体が面を横切ります。Lagrange型セルは流体とともに動きます。ALEでは格子速度wを流速uとは独立に選べます。[Hirt・Amsden・Cook（1974）](https://doi.org/10.1016/0021-9991(74)90051-5)は古典的な全速度ALE定式化を与えます。

## 流束は動く面に対する相対量 {#the-flux-is-relative-to-the-moving-face}

移動する検査体積K(t)にReynolds輸送定理を適用すると、

\[
\frac{d}{dt}\int_{K(t)}U\,dV
+\int_{\partial K(t)}\left[F(U)\cdot n-(w\cdot n)U\right]dS=0.
\]

です。w=0がEuler型です。格子の法線速度を流体の法線速度に合わせるとLagrange質量流束の極限になります。ただし物質面を通じても圧力は運動量・エネルギーを伝えるため、質量流束をゼロにしても全Euler流束がゼロになるわけではありません。

## 幾何も保存則に従う {#geometry-must-obey-a-conservation-law-too}

一様状態を一様に保つには、セル体積の変化と面運動を整合させます。

\[
\frac{d|K|}{dt}=\int_{\partial K}w\cdot n\,dS.
\]

離散的な対応が幾何保存則（geometric conservation law, GCL）です。格子移動と流体更新で掃引体積が一致しないと、個別には正確そうでも定数データから偽の流れを生じる場合があります。

## 再現可能な1ステップの検査 {#a-reproducible-one-step-check}

`numart.geometry.moving_volume_uniform_test`は、端点を固定して[0,1]の面を滑らかな正弦変位で変形します。面速度は実際の変位をdelta tで割った値です。定数スカラーqの示量量Vqを相対流束(a−w)qで更新し、新体積で割ります。両方に同じ変位を使います。

```python
import numpy as np
from numart.geometry import moving_volume_uniform_test
old_faces, new_faces, q = moving_volume_uniform_test(phase=0.8)
print(np.max(np.abs(q - 1)))
```

複数の変形位相で、一様状態が丸め誤差の範囲で保たれることを確認します。振幅制約は正のセル幅を保証します。**1次元移動体積の恒等式検査**であり、ALE Eulerソルバーや非一様データの精度検証ではありません。

## 格子移動、再配置、歪み {#mesh-motion-remapping-and-distortion}

完全なALE法は、頂点を動かし、Lagrangeまたは相対流束ステップを解き、より良い格子へ再配置する場合があります。保存的再配置、格子の絡まり、境界移動、時間整合性には追加の検証が必要です。総質量を保つ再配置でも、正値性や定数状態の保存に失敗する場合があります。

[格子の章](meshes.md)で位相と運動を分け、[座標の章](coordinates-viscosity.md)で移動検査体積とテンソル基底の変更を区別してください。xをrへ置き換えたり、描画頂点を動かしたりするだけでALE法になるわけではありません。
