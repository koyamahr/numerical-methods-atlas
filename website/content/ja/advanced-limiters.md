# 発展的な勾配制限：TVBと正値性保存

[勾配制限ノート](#/limiters)は、TVBスカラー実験と、別の保存的Euler状態スケーリングを含みます。滑らかな極値の精度低下と、許容できない熱力学状態という異なる失敗を扱います。

## TVB修正minmod {#tvb-modified-minmod}

候補増分vと隣接増分a、bに対して、

\[
\widetilde m(v,a,b)=
\begin{cases}
v,&|v|\le M\Delta x^2,\\
m(v,a,b),&\text{otherwise},
\end{cases}
\]

と定義します。mは一般化minmodで、共通符号なら最小絶対値、符号不一致ならゼロです。スカラー例ではv=(a+b)/2を選びます。M=0ではTVD実験の2増分minmodに一致します。M>0なら、隣の勾配が逆符号でも十分小さな増分を残し、滑らかなピークの曲率を保てます。

dx²閾値は、RKDGで滑らかな極値の面偏差が持つ尺度に対応します。係数の単位は解の単位／長さ²で、普遍的な無次元定数ではありません。従属変数や座標を尺度変換するならMを再検討し、増分と微分でも閾値を変える必要があります。

[Cockburn・Shu（1989）](https://doi.org/10.1090/S0025-5718-1989-0983311-4)はTVB RKDGの枠組みを発展させます。初版が実装するのは**スカラー有限体積の修正minmodという構成要素**で、完全なRKDGやその定理ではありません。ノートは正弦波・矩形波でM=0、10、50を計算します。小さな極値を認めるとTVは各ステップで減るとは限らず、大きなMでは不連続の近くに小さな振動も許します。Mの変更だけで任意の方式の一様TVB限界は証明できません。Euler系のTVB拡張は未実装です。

## 密度の正値性と圧力の正値性は別の制約 {#positive-density-and-pressure-are-different-constraints}

理想気体の保存変数U=(rho,m,E)について、

\[
p(U)=(\gamma-1)\left(E-\frac{|m|^2}{2\rho}\right),\qquad
\mathcal G=\{U:\rho>0,\ p(U)>0\}.
\]

です。正の密度だけでは正の内部エネルギーは保証されません。TVD、TVB、エントロピー修正、目に見える振動がないことから、Euler状態が許容されるとは限りません。rhoとEが正でも、運動エネルギーが過大なら負圧になり得ます。

## 平均を保つスケーリング {#a-mean-preserving-scaling-building-block}

許容される保存セル平均Ubarから始め、与えた全再構成点へ同じ係数を使います。

\[
\widehat U_\alpha=\bar U+\theta(U_\alpha-\bar U),\qquad 0\le\theta\le1.
\]

元の点の求積平均がUbarなら、変換後も保たれます。この構成では全成分・全点に共通のthetaを使うことが重要です。rho、圧力、全エネルギーを独立に切り詰めても、この保存性はありません。

まず最小再構成密度からthetaを制限します。

\[
\theta_\rho=\min\left(1,
\frac{\bar\rho-\epsilon_\rho}{\bar\rho-\rho_{\min}}\right)
\quad\text{if }\rho_{\min}<\epsilon_\rho;
\qquad\theta_\rho=1\text{ otherwise}.
\]

その後、すべての点がp(Uhat)≥epsilon_pを満たすまで[0,theta_rho]でthetaを縮めます。理想気体圧力は正密度で凹関数なので、線分の許容部分は平均を含み、二分法で探せます。実装は64反復と丸めを避ける小さな後退を使います。密度・圧力下限は入力パラメータで、質量やエネルギーを挿入するものではありません。悪い平均はエラーにします。この方法で不正な平均を中心に縮めても、保存性と正値性を同時に修復できません。

[Zhang・Shu（2010）](https://doi.org/10.1016/j.jcp.2010.08.016)の凸スケーリングの考え方を、単純な共通状態スケーリングと数値的圧力探索で使います。原著の2段階の密度多項式・状態制限を逐語的に再現するものではありません。対象は与えた点だけで、その間の任意の多項式値まで自動的に制限しません。

## 実演が実際に検証するもの {#what-the-demonstration-actually-verifies}

3節点セルはxi=−1、0、1、正のGauss–Lobatto重み(1/6,2/3,1/6)、gamma=1.4、Ubar=(1,0,2.5)です。生の状態をUbar+xi×deltaとし、密度違反にはdelta=(1.2,0,0)、圧力違反には(0,3,0)、両方の違反には(1.2,3,1)を選びます。実数演算で重み付き平均はUbarです。図は3節点だけを標本化し、epsilon_rho=epsilon_p=1e-8で、theta、制限後最小密度・圧力、保存平均の欠損を報告します。構成した再構成テストで、爆風や膨張波の時間積分ではありません。

```python
import numpy as np
from numart.limiters import positive_reconstruction

mean = np.array([1., 0., 2.5])
raw = mean + np.array([-1., 0., 1.])[:, None] * [0., 3., 0.]
limited, theta = positive_reconstruction(mean, raw)
```

テストでは、既に許容される再構成が不変であること、不正平均の拒否、3失敗例での両下限と保存的求積平均を確認します。

## 再構成から完全離散の保証へ {#from-reconstruction-to-a-fully-discrete-guarantee}

完全な正値性保存Euler法には、整合する正値性保存流束、界面状態を含む正の求積分解、対応する波速／CFL制約、必要な全段階での制限も必要です。SSP時間積分が前進Eulerの正値性を伝えるのは、その性質と刻み制約が既に成り立つ場合だけです。ソース項と境界処理にも独自の検証が必要です。

この補助関数は**既存のEuler MUSCL、差分WENO、CT／GLM、KEEPの時間更新へ接続していません**。既存の限界はそのままです。今後は各段階の許容性・保存性、真空近傍の二重膨張波、強い爆風を確認してから、時間全体の正値性を主張すべきです。多次元・非理想状態方程式にも追加解析が必要です。
