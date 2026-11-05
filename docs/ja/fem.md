# 連続有限要素法：弱形式から疎行列の組立てへ

**実装済み**：区間とアフィン三角形上の連続P1要素、Dirichlet条件付きPoisson問題、整合質量行列、求積による誤差ノルム。アトラスの不連続Galerkin移流の例とは別です。

## 1943年：変分法による道 {#1943-a-variational-route}

[Courant（1943）](https://doi.org/10.1090/S0002-9904-1943-07818-4)は変分的な考え方の基礎文献です。この章の小さな実装は独立した現代的なP1の例で、原著の例の再現ではありません。

−Δu=fに対し、境界でu=gを指定します。境界でゼロになる試験関数を掛け、部分積分すると、

\[
\int_\Omega \nabla u_h\cdot\nabla v_h\,d\Omega
=\int_\Omega f v_h\,d\Omega.
\]

となります。u_hを節点係数と連続区分線形基底関数の積の和で表します。三角形Kの形状関数の勾配は一定なので、

\[
K^K_{ij}=|K|\nabla\phi_i\cdot\nabla\phi_j,
\qquad M^K_{ij}=\frac{|K|}{12}(1+\delta_{ij}).
\]

です。共有節点では要素からの寄与をCSR形式へ集めます。ゼロでないDirichlet値を右辺へ移してから、行と列を対称に消去します。行だけを処理すると、CGで重要な対称性が壊れます。この例は[ILU前処理付きGMRES](sparse-nonlinear.md)を使います。

## 検証結果を読む {#inspect-the-evidence}

![FEM、疎行列、硬い方程式、射影法の検証](figures/solver-foundations.png)

製造解は単位正方形上のsin(πx)sin(πy)です。L2とH1半ノルム誤差は節点だけで測らず、**要素内部**で積分します。滑らかな解に対する期待次数は2と1です。テストではアフィンパッチ、ゼロでない境界値、境界消去前の定数零空間、整合質量の総量も確認します。

```python
from numart.fem import poisson_2d
result = poisson_2d(16)
print(result.residual, result.u.shape)
```

`python scripts/build_equation_gallery.py`で再現します。専用の[計算記録](figures/solver-foundations.json)に誤差とソースハッシュを残します。速度・圧力の混合要素、inf–sup条件、曲線格子、一般のNeumann／Robin条件の組立て、適応細分化は今後の課題です。現在の[射影法の例](incompressible.md)はスタガード差分格子を使います。

**A安定性・L安定性とL1／L2／L∞誤差ノルム**は、[精度と安定性の共通ガイド](accuracy-stability.md)を参照してください。
