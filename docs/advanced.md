# 前処理、dual time stepping、残差分配

## 条件数と PDE 前処理

線形系 `Ax=b` の 2-ノルム条件数は `κ₂(A)=σmax/σmin`。
摂動への感度を示す量で、特定の反復法の収束率そのものではありません。
左前処理は `P^{-1}Ax=P^{-1}b`、右前処理は `AP^{-1}y=b, x=P^{-1}y`。
対称正定値なら `P^{-1/2}AP^{-1/2}` で対称性を保つ比較もできます。

`conditioning_example` は `A=S B S`、B=1D Poisson、S=対角スケーリングの人工例です。
Jacobi の対称スケーリングで条件数がどう変わるかを示します。
これは低 Mach 流体用の Turkel 前処理行列そのものではありません。

圧縮性 PDE では対流と音響の特性速度が大きく異なる低 Mach 領域に、別の前処理の問題があります。
擬似時間系を `Γ(U) ∂U/∂τ + R(U)=0` のように変更し、特性速度や収束・数値散逸を調整します。
Γ の導出、変数変換、Mach 数に応じた係数、境界の整合性は別途検証が必要です。
物理時間微分を安易に置換すると時間依存解が変わります。
[Turkel (1987)](https://doi.org/10.1016/0021-9991(87)90084-2)。

## dual time stepping

半離散問題 `dU/dt+R(U)=0` を BDF2 で物理時間に離散化すると

\[
\frac{3U^{n+1}-4U^n+U^{n-1}}{2\Delta t}+R(U^{n+1})=0.
\]

各物理ステップで、未知数 Q に対する擬似時間方程式

\[
\frac{dQ}{d\tau}+\frac{3Q-4U^n+U^{n-1}}{2\Delta t}+R(Q)=0
\]

を定常まで解きます。初段は後退 Euler で開始します。
物理時間の精度は Δt と空間誤差、内側反復の未収束に依存します。
物理 CFL が大きいことだけでは正しい時間発展を保証できません。
[Jameson (1991)](https://doi.org/10.2514/6.1991-1596)。

`dual_time_advection` は周期 1D 移流の陰的風上 + BDF1/BDF2 を、Jacobi の擬似時間反復で解く最小例です。
内側の相対残差は `tol*max(1,||b||∞)`、既定 tol=1e-10。
最大反復数までに収束しなければ失敗します。
独立の dense solve と比較して BDF2 の離散式を満たすことを検証します。
Jameson の multigrid による圧縮性流れのアルゴリズム全体を再現したものではありません。

## residual distribution scheme

要素 K の積分残差 `Φ_K=∫K ∇·F(U) dV` を節点に分配し、
`Σ_{i∈K} Φ_i^K=Φ_K` を保つことで保存性を構成します。
連続有限要素と upwind の考え方が接続する手法群です。
[Abgrall (2006), 著者公開版](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf)。

`rd_residual` は 1D P1 scalar advection の最小例です。
`Φ_K=a(u_{i+1}-u_i)` を流下側の節点にすべて配り、lumped mass h で割ります。
この場合は 1 次風上差分と一致することを確認できます。
2D 三角形の N／LDA／非線形ブレンド、時間整合質量行列、Euler 系は未実装です。

## Roe、entropy fix、Einfeldt、rotated solver

Roe は `F_R-F_L=Ã(U_R-U_L)` を満たす線形化と固有分解を使います。
初版は sqrt(ρ) 重みの u、H を使い、`ã²=(γ-1)(H̃-ũ²/2)`。
波の強さと固有ベクトルによる散逸を数値流束に加えます。
[Roe (1981)](https://doi.org/10.1016/0021-9991(81)90128-5)。

音響固有値の絶対値を δ 未満で `(λ²+δ²)/(2δ)` に置き換えるのが初版の entropy fix。
HLLE は別の流束で、Einfeldt 型の左右波速を使い、低密度の強膨張問題を対象にします。
Roe の entropy fix、HLLE の正値性、衝撃波に対する carbuncle 対策は相互に置き換えられません。
[Einfeldt (1988)](https://doi.org/10.1137/0725021)、
[Einfeldt ほか (1991)](https://doi.org/10.1016/0021-9991(91)90211-3)。

rotated-hybrid Riemann solver は、界面法線以外の方向も利用して複数の流束を組み合わせ、
衝撃波安定性と剪断層の解像度を両立させる方向です。
単純な座標回転だけを実装して、この手法を再現したとはしません。
初版は文献・再現対象の整理までで、2D Euler、幾何、方向選択、carbuncle 試験が次段階です。
[Nishikawa–Kitamura (2008)](https://doi.org/10.1016/j.jcp.2007.11.003)。
