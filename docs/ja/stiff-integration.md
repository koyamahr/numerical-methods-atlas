# 硬い方程式の積分：段階を解き、時間誤差を制御する

**実装済み**：後退Euler法、その初期化を使う固定刻みBDF2、2段階SDIRK2、1次IMEX Euler、ステップ倍分割による適応SDIRK2。すべての非線形段階に減衰Newton法を使い、失敗を明示します。

## 陰的段階と安定性 {#implicit-stages-and-stability}

後退Euler法はy_new−y_old−h f(t_new,y_new)=0を解きます。BDF2は、

\[
\frac{3y_{n+1}-4y_n+y_{n-1}}{2h}=f(t_{n+1},y_{n+1}).
\]

を解きます。ここで使うL安定、2段階、2次精度の単一対角陰的公式の出典は[Alexander（1977）](https://doi.org/10.1137/0714068)です。

\[
\gamma=1-1/\sqrt2,\qquad
A=\begin{pmatrix}\gamma&0\\1-\gamma&\gamma\end{pmatrix},
\quad b=(1-\gamma,\gamma),\quad c=(\gamma,1).
\]

各対角段階は別々の非線形求解です。陰解法では陽解法の安定限界を超える刻みを使える場合がありますが、実用的な刻み幅は精度でも制限されます。収束したNewton残差が測るのは段階方程式であり、時間離散化誤差ではありません。

## 適応刻みと陽陰分割 {#adaptive-and-split-steps}

適応実装はSDIRK2の1全ステップと2半ステップを比べます。局所誤差推定は(y_half−y_full)/3で、atol+rtol max(|y_old|,|y_half|)で尺度化します。Richardson外挿はせず、2半ステップの値を採用し、指数−1/3でhを調整します。棄却試行と受理ステップを数え、試行上限に達するとエラーにします。

IMEX Eulerは一方を陽的、他方を陰的に評価します。この最小の1次分割は、[Ascher–Ruuth–Spiteri（1997）](https://doi.org/10.1016/S0168-9274(97)00056-1)の高次IMEX RK構成ではありません。陽的部分には独自の安定制約が残ります。可変刻みBDF、埋込みDIRK対、演算子分割は今後の拡張です。

![硬い外力付きODEと他のソルバーの検証](figures/solver-foundations.png)

硬いテストy′=−1000(y−cos t)−sin tは、y(0)=1のとき厳密解cos tを持ちます。[計算記録](figures/solver-foundations.json)は、実際の積分節点での最大誤差と適応ステップ数を残します。別のテストで、非線形・非自律ODEの次数と、硬い減衰モードの強い減衰を確認します。

外力付きの硬い問題の粗い刻み列は、一様な2次収束の範囲にはありません。BDF2の開始処理と硬い系の次数低下が、節点全体の最大誤差へ影響します。形式的な時間次数は、非線形・非硬性の次数テストで別に確認します。

**A安定性・L安定性とL1／L2／L∞誤差ノルム**は、[精度と安定性の共通ガイド](accuracy-stability.md)を参照してください。
