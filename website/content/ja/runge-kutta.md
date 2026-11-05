# Runge–Kutta法：段数、次数、安定性、SSP

RK2・RK4は次数、SSPは安定性の継承を表し、異なる問いに答えます。[RK系譜ノート](#/runge-kutta)では、9つの陽解法の全段階係数、非線形予測値、線形安定領域、実測収束次数を比べます。

## 1ステップと複数の右辺評価 {#one-step-several-right-hand-side-evaluations}

y′=f(t,y)の陽的s段RK法は、

\[
Y_i=y_n+h\sum_{j<i}a_{ij}k_j,\qquad
k_i=f(t_n+c_i h,Y_i),\qquad
y_{n+1}=y_n+h\sum_{i=1}^s b_i k_i,
\qquad c_i=\sum_{j<i}a_{ij}.
\]

です。Butcher表はc、A、bを係数図にまとめます。段数sは本実装の右辺評価回数です。次数pは、必要な滑らかさ・安定性・固定区間の仮定で大域誤差O(h^p)を意味します。段階予測値Y_iは一般に途中時刻の高精度解ではありません。段階時刻は逆戻りする場合があり、SSPRK(4,3)はc=(0,1/2,1,1/2)で評価します。時間依存外力・境界値には、次の時刻順の割合ではなく正しいc_iを使います。

## RK2はひとつの族 {#rk2-is-a-family}

2段・2次の族を、

\[
k_1=f(t_n,y_n),\quad
k_2=f(t_n+\alpha h,y_n+\alpha h k_1),\quad
y_{n+1}=y_n+h\left[\left(1-\frac1{2\alpha}\right)k_1+
\frac1{2\alpha}k_2\right].
\]

と書けます。Heun／陽的台形則はalpha=1、陽的中点は1/2、Ralstonは2/3です。HeunはSSPRK(2,2)でもあります。ここでの完全な非線形法のSSP係数は、それぞれ1、0、1/2で、全Butcher表の絶対単調性不等式から確認します。

3法ともスカラー線形安定性多項式は、

\[
R(z)=1+z+\tfrac12 z^2,\qquad z=h\lambda.
\]

です。そのため、厳密算術ではy′=lambda yの軌道は同じですが、非線形段階や誤差は一致するとは限りません。ノートでは厳密解1/(1+t)を持つy′=−y²、y(0)=1も計算し、振動子だけでは見分けられない違いを示します。ひとつの問題から普遍的に最良のRK2は決められません。

## RK3、古典的RK4、SSPの段数 {#rk3-classical-rk4-and-ssp-stage-counts}

実装した3次群は、Kuttaの古典的3段、SSPRK(3,3)、SSPRK(4,3)です。前二者はR(z)=1+z+z²/2+z³/6を共有しますが、非線形SSP係数は0と1です。SSPRK(4,3)は4回目の右辺評価を使い、C=2、追加項z⁴/48を持ちます。4段だから4次になるわけではありません。

古典的4段RK4の重みは(1/6,1/3,1/3,1/6)です。安定性多項式はz⁴/24を加え、4次精度です。一般の非線形SSP係数はゼロです。すべてのRK4計算が振動するのではなく、一般的な前進EulerからのSSP継承保証が使えないという意味です。[NumipediaのRK4記録](https://ketch.github.io/numipedia/methods/RK44.html)に係数表とスカラー安定性があります。

比較用にSpiteri–Ruuthの5段4次SSP法SSPRK(5,4)も実装します。全係数は[Gottlieb–Ketcheson–Shu総説](https://www.davidketcheson.info/assets/papers/sspreview.pdf)第3.1節です。小数Shu–Osher形式をButcher表へ変換し、y_nからの増分で表現することで丸めたアフィン重みのずれを避けます。厳密有理係数とはせず、控えめな丸め限界C=1.508を使い、与えた精度で次数条件と非線形収束を検査します。

一般の非線形SSP係数が正の標準陽的RK法では次数は最大4です。4段4次の陽解法はC>0を持てないため、4次SSPには追加段が必要です。SSPRK(5,4)は一例で、すべての5段4次法がSSPなのではありません。[Spiteri–Ruuth（2002）](https://doi.org/10.1137/S0036142901389025)、[Gottlieb–Ketcheson–Shu（2009）](https://doi.org/10.1007/s10915-008-9239-z)。

## SSPが保存するもの {#what-ssp-preserves}

特定の半離散空間演算子Lが、h≤h_FEで前進Eulerに対して凸安定性を満たすとします。係数CのSSP法は、

\[
h\le C h_{\rm FE}.
\]

でそれを継承します。前提は全変動、ノルム、許容凸集合などですが、実際の演算子と段階処理が条件を満たす必要があります。SSPはTVD空間離散化を生み出したり、不適切な境界を直したり、欠けたEuler正値状態を補ったりはしません。[Gottlieb–Shu–Tadmor（2001）の総説](https://www.math.umd.edu/~tadmor/pub/linear-stability/Gottlieb-Shu-Tadmor.SIREV-01.pdf)がこの視点を説明します。[勾配制限](limiters.md)と[正値再構成](advanced-limiters.md)の別の要件と比較してください。

表記は**SSPRK(s,p)**で、先が段数、後が次数です。初版ではHeun／SSPRK(2,2)はC=1、SSPRK(3,3)は1、SSPRK(4,3)は2、SSPRK(5,4)は丸め限界1.508です。右辺評価あたりのSSP刻み限界C/sは参考になりますが、実行時間の順位ではありません。メモリー転送、記憶量、空間精度、他の安定制約が実際のコストを左右します。

## 線形安定性は別の図 {#linear-stability-is-a-separate-picture}

y′=lambda yでは、1ステップの倍率は、

\[
R(z)=1+z\,b^T(I-zA)^{-1}{\bf1}.
\]

です。|R(z)|≤1がスカラー絶対安定領域です。Re(z)∈[−6,2]、Im(z)∈[−4,4]の401×401格子で境界を標本化し、曲線は近似等高線であって厳密な境界位置ではありません。正規な線形空間演算子なら固有値からRの評価位置を考えられますが、非正規演算子の一時的増大は固有値だけでは見落とします。

無減衰振動子でRK2には虚軸上のゼロでない安定区間がなく、SSPRK(3,3)と古典的RK4にはあります。これはスカラー線形問題の性質で、前進Euler自身もこの振動子でゼロでない安定刻みを持たないため、HeunのSSP性とは矛盾しません。

## 時間積分の他の分岐 {#other-branches-of-the-time-integration-family}

Dormand–Prince 5(4)などの埋込みRK対は、2つの次数で誤差と刻みを推定します。この括弧は埋込み次数で、SSPRK(s,p)の段数・次数とは違います。初版では埋込み誤差推定、適応制御、連続出力、FSAL最適化は実行しません。

低記憶RKは段階計算を組み替えて配列を減らしますが、自動的にSSPにはなりません。陰的RKには中点、Gauss／Radau／SDIRKなどがあり、非線形求解と独自の安定性を持ちます。IMEX対は陽的・陰的演算子を分けます。既存の**スカラー線形**後退Euler・陰的中点の実演を除き、ここでは読書の背景です。下の汎用`rk_step`は9つの陽的Butcher表だけに対応します。leapfrogは多段階漸化式、力学Verletと[シンプレクティック写像](symplectic.md)はさらに別の分岐です。

## 再現と検証 {#reproduction-and-verification}

```python
from numart.runge_kutta import rk_step, nonlinear_trajectory

value, stages = rk_step(lambda t, y: -y*y, 0., 1., 0.5,
                        method="ssprk43", return_stages=True)
t, y = nonlinear_trajectory("ssprk54", steps=40)
```

```bash
python scripts/build_runge_kutta.py
python scripts/sync_web_content.py
```

JSONには全係数表、等高線、27個の1ステップ段階例（h=0.25、0.5、1）、9つの細分化（N=10、20、40、80、T=1）、ソースハッシュを記録します。誤差は厳密な非線形解を使い、段階は実際の右辺評価です。テストでは4次までの全次数条件、非線形製造時間依存方程式、複素線形安定係数、指定Cでの全係数表SSP不等式、継承した刻み制約でのスカラーMUSCL保存／TVDを確認します。既存Euler／WENOがRK選択可能や完全正値性保存になるわけではありません。

![計算したRK系譜の比較](figures/runge-kutta.png)
