# 疎行列・非線形方程式系：真の残差を測る

**実装済み**：COOからCSRへの組立て、再始動GMRES、BiCGSTAB、Jacobi、ピボット選択なしILU(0)、密行列またはKrylov内部解法を使うArmijo減衰Newton法。内部を確認できる小規模な実数演算の例です。

## 1986〜1992年：非対称Krylov法 {#19861992-nonsymmetric-krylov-methods}

[Saad–Schultz（1986）](https://doi.org/10.1137/0907058)がGMRES、[van der Vorst（1992）](https://doi.org/10.1137/0913035)がBiCGSTABを導入します。本実装のGMRESはArnoldi再直交化と小さなHessenberg最小二乗問題を使い、指定した内部反復回数で再始動します。BiCGSTABは破綻を明示し、残差は単調に減るとは限りません。

両実装は**固定した右前処理**を適用します。

\[
A M^{-1} z=b,\qquad x=M^{-1}z,
\qquad \|b-Ax\|_2\leq\max(\mathrm{atol},\mathrm{rtol}\|b\|_2).
\]

停止判定の履歴では真の残差を再計算します。Jacobiは対角スケーリングです。ILU(0)は与えた非ゼロ構造だけを保ち、追加のフィル、ピボット選択、並べ替えを行いません。非常に小さなピボットでは明示的に失敗します。実用的な頑健な疎行列分解を置き換えるものではありません。

## Newton法と条件数 {#newton-and-conditioning}

Newton法はJ(x)δ=−F(x)を解き、残差に対するArmijo減少条件を満たすよう後退探索でステップ長を選びます。Newton–Krylovの例はJを組み立ててGMRESを使い、**行列不要方式ではありません**。Bratu方程式を2つの空間解像度で解析解と比較し、内部求解の失敗も検査します。

残差が小さくても、解誤差が小さいとは限りません。

\[
\frac{\|x-\hat x\|}{\|x\|}
\leq \kappa(A)\frac{\|b-A\hat x\|}{\|b\|}.
\]

条件数、固有値分布、非正規性は異なる性質を表します。条件数が小さいことだけで再始動GMRESの優劣は決められません。CGには引き続き対称正定値演算子と適切な対称正定値前処理が必要で、一般のILU(0)がその条件を満たすとはしていません。

![実測した真の残差と検証](figures/solver-foundations.png)

非対称の例は、ゼロDirichlet条件での1次風上移流と中心差分拡散です。1反復あたりの計算量が異なるため、図では実行時間の順位を付けません。[データとソースハッシュ](figures/solver-foundations.json)、[FEMの組立て](fem.md)、[陰的ODE段階](stiff-integration.md)も参照してください。
