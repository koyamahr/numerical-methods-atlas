# 勾配制限：minmod、Superbee、MC、van Leer、van Albada

勾配制限は、線形な高次再構成を局所勾配の非線形な選択に置き換えます。[勾配制限ノート](#/limiters)で、同じ格子・時間積分に対する5種の選択と、1次・無制限のスカラー基準例を比較できます。

## 再構成と比の規約 {#reconstruction-and-the-ratio-convention}

一様セルの後退・前進増分を、

\[
a_i=\bar u_i-\bar u_{i-1},\qquad b_i=\bar u_{i+1}-\bar u_i,
\qquad r_i=a_i/b_i,\qquad s_i=\phi(r_i)b_i.
\]

とし、セルiから再構成する2状態を、

\[
u_{i+1/2}^{L}=\bar u_i+\tfrac12s_i,\qquad
u_{i-1/2}^{R}=\bar u_i-\tfrac12s_i.
\]

とします。実装はa、bを直接使うため、平坦部の分母ゼロに数値epsilonや任意の比は不要です。符号が異なる場合、または一方がゼロなら制限勾配はゼロです。これらは増分であり、微分が必要なときだけセル幅で割ります。

## 5つの制限関数 {#five-limiter-functions}

以下はいずれもr≤0でゼロです。r>0では、

\[
\begin{aligned}
\phi_{\rm minmod}(r)&=\min(1,r),\\
\phi_{\rm Superbee}(r)&=\max\{\min(2r,1),\min(r,2)\},\\
\phi_{\rm MC}(r)&=\min\{2r,(1+r)/2,2\},\\
\phi_{\rm van\ Leer}(r)&=2r/(1+r),\\
\phi_{\rm van\ Albada}(r)&=(r^2+r)/(r^2+1).
\end{aligned}
\]

です。van Albadaは**切り詰めた対称形式**で、epsilon正則化はありません。別の形式は極値近傍で異なります。MCはmonotonized centralの略です。すべてphi(1)=1と、図示するスカラー条件0≤phi(r)≤min(2r,2)を満たします。スカラー流束制限の枠組みとRoeの圧縮的構成は[Sweby（1984）](https://doi.org/10.1137/0721062)、実装規約は[Clawpack](https://www.clawpack.org/pyclaw/evolve/limiters.html)と[MPI-AMRVAC](https://amrvac.org/md_doc_2limiter.html)を参照してください。同じ名称でも、変数、時間積分、epsilonの選択が同じとは限りません。

Minmodは同符号の小さい増分を選びます。Superbeeはより圧縮的で、滑らかな特徴を平坦部へ変える場合があります。MCとvan Leerは多くの単調領域でminmodより勾配を残します。ノートでは誤差、全変動、オーバーシュートの測定で傾向を確かめます。すべての問題で最良の制限関数はありません。

## 計算による比較 {#computed-comparisons}

スカラー方程式u_t+a u_x=0を周期区間[0,1]で解きます。全計算は保存的有限体積、風上界面流束、SSPRK(3,3)、N=200、|a|dt/dx≤0.3、終了時刻1で、最終ステップを短縮します。a=±1の両方向を計算し、[0.2,0.4]の単位矩形パルスとsin(2πx)を使います。初期値・参照値は、部分的に覆われたセルや正弦波のsinc係数を含む**厳密セル平均**です。表示L1もこれを使います。周期全変動は末尾から先頭への跳びを含み、質量はdx×総和です。最大TVは初期状態を含む全保存フルステップ診断から求めます。

1次比較は勾配ゼロです。無制限比較は同じ流束とSSPRK3で中心勾配(a+b)/2を使い、振動を生じ得ます。完全離散のLax–Wendroff法ではありません。

別のSod比較は既存の理想気体設定、gamma=1.4、N=200、t=0.2、HLLC、基本変数再構成、CFL=0.3のSSPRK3で、勾配選択だけを変えます。密度誤差は既存規約どおり**点値**であり、厳密セル平均誤差ではありません。流出境界のため、周期スカラーの質量・TV診断はこのパネルへ適用しません。

滑らかな正弦波をN=40、80、160、t=0.2で細分化し、L1誤差と次数を報告します。2次という名称は滑らかな領域の整合性であり、極値での一様な点値精度や不連続の2次誤差を意味しません。

## TVDはスカラー更新全体の性質 {#tvd-is-a-property-of-the-complete-scalar-update}

このスカラーMUSCL演算子では、示した勾配条件と|a|dt/dx≤1/2によりTVDの前進Euler構成要素が得られ、SSPRK3はその範囲で凸安定性を保ちます。ソルバーもCFLをこの範囲に制限します。テストでは両方向、周期保存、フルステップ全変動、上下限、CFL=1/2のランダムデータ前進Eulerを確認します。

同じ関数をEuler基本変数の各成分に使っても、一般の系のTVD定理、エントロピー条件、正のセル平均の保証にはなりません。特性再構成と完全離散正値性は別の拡張です。TVBの極値緩和と保存的正値スケーリングは[発展的な勾配制限](advanced-limiters.md)を参照してください。

## 再現と確認 {#reproduce-and-inspect}

```bash
python -m numart.cli run sod --method muscl --riemann hllc --limiter superbee --n 200
python scripts/build_limiters.py
python scripts/sync_web_content.py
```

```python
from numart import get_problem, solve
from numart.tvd import solve_advection

sod = solve(get_problem("sod"), limiter="mc")
pulse = solve_advection(profile="square", limiter="van-leer", speed=-1.)
```

`docs/figures/limiters.json`は全描画配列、細分化、診断、ソースハッシュを記録します。ブラウザーはPython計算曲線を選び、別のPDE実装を実行しません。既定MUSCLはminmodのままで、制限関数オプションはWENO5や2次元Euler／MHD基準例には適用しません。

![計算した勾配制限の比較](figures/limiters.png)
