# 厳密解・参照解ライブラリ

検証用ライブラリでは「正解」が何を意味するかを明示します。[参照解エクスプローラー](https://koyamahr.github.io/numerical-methods-atlas/#/exact-solutions)には、式、仮定、出典、点値、1次元ではセル平均を備えた**18ケース**を収録しています。参照解を評価する機能であり、数値的なPDEの時間発展は行いません。

## 4種類の参照解 {#four-different-reference-categories}

- **解析解（analytic）**：スカラーのエントロピー波、正弦波の移流・減衰、乾床・真空への膨張波、チャネル流、Taylor–Green流などの陽な式です。浮動小数点評価の丸め誤差は残ります。
- **半解析解（semi-analytic）**：Euler、水深が正の浅水流、等温流のRiemann解です。波の曲線は解析的ですが、中間状態の接続にはスカラー方程式の数値的な求根が必要です。
- **製造解（manufactured）**：滑らかな場を先に与え、外力と境界条件を導きます。Poissonの正弦波ケースは、その場に合わせて選んだ強制問題を検証します。
- **数値参照解（numerical reference）**：細かい格子などで計算した数値解です。離散化・境界・時間積分の誤差が残ります。既存アトラスの高解像度比較は、該当する場合にこの区分を明示します。本ライブラリの解析解ケースとしては追加していません。

参照解との一致は、特定の設定についての実装検証です。実験との比較による物理モデルの妥当性確認や、任意の境界処理の保証とは異なります。

## 収録する場と仮定 {#included-fields-and-assumptions}

スカラーには周期正弦波の移流と熱減衰、Burgersの衝撃波・膨張波、2次交通流モデルの衝撃波・膨張波があります。EulerにはSod、Lax、二重膨張波、生成される真空を収録し、比熱比1.4の理想気体を使います。浅水流には水深が正のダム崩壊、乾床への膨張、中央の乾燥領域を収録し、平坦な底面と重力1を使います。等温Eulerは一定音速1、初期密度は厳密に正とし、エネルギー方程式や有限の真空状態を持ちません。

粘性流は単位幅の平面チャネルにおける定常Couette・Poiseuille速度分布と、周期的な2次元Taylor–Green渦です。チャネルの出力は速度であり、圧縮流の保存変数ではありません。Taylor–Greenは速度と平均ゼロに固定した圧力を返します。Poisson製造解は場と外力の両方を提供します。

いずれも標準的な無次元設定です。参照解の乾床・真空への対応は、既存の正値状態を要求する有限体積ソルバーに、その機能を追加するものではありません。地形、粘性Riemann問題、一般の状態方程式、多次元衝撃波相互作用は初回の対象外です。

![6ケースの点値参照解と保存変数・スカラーのセル平均](figures/reference-solutions.png)

## 点値と有限体積セル平均 {#point-values-and-finite-volume-means}

保存変数を有限体積法で比較するときは、次のセル平均を使います。

\[
\overline{\boldsymbol U}_i(t)=\frac{1}{x_{i+1/2}-x_{i-1/2}}
\int_{x_{i-1/2}}^{x_{i+1/2}}\boldsymbol U(x,t)\,dx.
\]

Eulerでは密度・運動量・全エネルギー、浅水・等温流では水深または密度と運動量を積分します。保存変数の平均を基本変数に変換したものは、一般に基本変数自体の平均とは異なります。衝撃波がセルを横切るとき、セル中心の点値で代用すると特に誤解を招きます。

既知の衝撃波・接触面・膨張波の両端で積分区間を滑らかな部分に分け、各部分に24点と48点のGauss–Legendre積分を適用します。保存する平均は48点の結果です。両次数の最大差は収束の目安であり、**厳密な誤差上限ではありません**。この規則は解析解にも適用し、保存セル平均は記号積分ではなく有限次数の求積で計算します。

非一様格子での誤差ノルムは全領域長で規格化します。

\[
L_1=\frac{\sum_i\Delta x_i|e_i|}{\sum_i\Delta x_i},\qquad
L_2=\left(\frac{\sum_i\Delta x_i e_i^2}{\sum_i\Delta x_i}\right)^{1/2},\qquad
L_\infty=\max_i|e_i|.
\]

成分ごとに報告します。[方程式ギャラリー](equation-gallery.md)のEuler・浅水・等温流にも、これらの保存変数セル平均を接続しました。保存時刻の数値解は引き続き、最終時刻を変えて独立に実行した計算です。

## Riemann解の構成と許容誤差 {#riemann-construction-and-tolerances}

自己相似変数xi=(x−x0)/tを使います。接続する未知量はEulerでは圧力、浅水では水深、等温流では密度です。正の未知量の対数に対して単調な波接続残差を挟み込み、二分法を適用します。対数区間幅の目標は2e−13、二分法は最大160回、最終残差は特性速度スケールの2e−10倍以内であることを検査します。残差が厳密にゼロなら、それ以前に停止できます。反復回数、最終区間幅、残差をケースごとに保存します。

Eulerや浅水の膨張波が離れると、中央に真空・乾燥領域が生じる場合があります。その場合は正状態の求根を省略します。保存変数はすべてゼロです。真空中の速度は物理的に未定義ですが、低レベルの変換では表示上の規約としてゼロとします。等温流では有限の真空の代わりに、非常に小さい正の密度になります。float64の対応範囲を超える状態は、黙って切り詰めずエラーにします。

[ClawpackのEulerの章](https://www.clawpack.org/riemann_book/html/Euler.html)と[浅水の章](https://www.clawpack.org/riemann_book/html/Shallow_water.html)は、波の構成と乾床・真空を説明しています。[Bhat・Fetecauの著者原稿](https://www.sfu.ca/~van/papers/Riemann-inv.pdf)のRiemann問題の議論には、元の等温Euler系の波曲線があります。本ライブラリは、その元の系を使い、論文の正則化モデルは使いません。

## 粘性流と製造解の式 {#viscous-and-manufactured-formulas}

単位幅・単位密度・動粘性係数nuの平面チャネルでは、定常分布は次式です。

\[
u_{\rm Couette}(y)=y,\qquad
u_{\rm Poiseuille}(y)=\frac{G}{2\nu}y(1-y),\qquad G=1,\quad\nu=0.1.
\]

Couetteでは壁速度が0と1、圧力勾配はゼロです。Poiseuilleでは両壁が静止したno-slip条件で、Gは密度で割った負の圧力勾配、または等価な体積力加速度です。十分に発達した平面流であり、円管流ではありません。

周期正方形[0,2pi]²のTaylor–Green解は、nu=0.1、単位密度で次のとおりです。

\[
u=\sin x\cos y\,e^{-2\nu t},\qquad
v=-\cos x\sin y\,e^{-2\nu t},\qquad
p=\frac{\cos(2x)+\cos(2y)}4e^{-4\nu t}.
\]

Webではy=pi/4のx方向断面を表示し、**2次元セル面積平均ではありません**。Pythonは2次元座標と滑らかな長方形セルの平均に対応します。関連する方法は[粘性流の章](incompressible.md)を参照してください。

製造解はu=sin(pi x)を与え、−u_xx=f=pi² sin(pi x)、両端は同次Dirichlet条件とします。同じオブジェクトから外力を取得できます。任意の外力に対するPoissonソルバーではありません。

## 再利用と再現 {#reuse-and-reproduce}

```python
import numpy as np
from numart.reference_solutions import get_reference, riemann_reference

ref = get_reference('euler-sod')
edges = np.array([0., .15, .42, .51, .7, 1.])
points = ref.point((edges[:-1] + edges[1:]) / 2, t=.2)
report = ref.cell_average_report(edges, t=.2)
means = report['values']  # columns: rho, rho*u, E
# With actual numerical conserved means q of the same shape:
# errors = ref.compare_means(q, edges, t=.2)
custom = riemann_reference('shallow-water', (2., 0.), (1., 0.),
                           parameter=9.81)
tg = get_reference('taylor-green')
box_mean = tg.box_average([0., 0.], [.2, .3], t=.5)
```

保存分布と図は`MPLCONFIGDIR=.mplconfig python scripts/build_reference_solutions.py`で再生成できます。[データと数値実装のソースハッシュをダウンロード](figures/reference-solutions.json)。Pythonでは、既存の独立なEuler実装との比較、Rankine–Hugoniot条件とLax不等式、膨張波のPDE残差と不変量、全領域の収支、既知の積分、製造解の外力、Taylor–Greenの運動量・発散残差を検証します。Webのビルドでは保存データの形式、波の位置、ソースハッシュ、平均値の規約を検査します。

Blasius、Sedov、Nohや追加の多次元参照解は今後の拡張です。[LANL ExactPack](https://github.com/lanl/ExactPack)はそれらを追加する際に参照できる独立した資料集です。現時点の依存ライブラリではなく、上のケースをExactPackと相互検証したという意味でもありません。
