# 非圧縮流：整合する離散演算子で射影する

**実装済み**：単位密度・周期2次元Navier–StokesをMAC格子で扱い、対流・粘性を中心差分、時間を射影付きSSPRK2、Poissonを離散FFT逆演算で解きます。

## 1968年：射影法の分岐 {#1968-the-projection-branch}

[Chorin（1968）](https://doi.org/10.1090/S0025-5718-1968-0242392-2)が射影法の原典です。本実装の周期RKモデルは原理を示し、原著の境界処理や時間刻みを再現するものではありません。

速度成分は異なる面、圧力はセル中心に置きます。周期格子の内積でD=−Gᵀとなるよう発散Dと勾配Gを選ぶと、

\[
DG\phi=D\boldsymbol u^*,\qquad
\boldsymbol u=\boldsymbol u^*-G\phi,\qquad D\boldsymbol u=0.
\]

です。FFTが逆にするのは連続の−|k|²ではなく、**DG**の記号です。

\[
\lambda_h=-\frac4{h^2}
\left[\sin^2(k_xh/2)+\sin^2(k_yh/2)\right].
\]

圧力定数は未定なので平均をゼロにし、周期適合性のためPoissonソースから平均を引きます。テストでは随伴恒等式、射影の冪等性、エネルギーの非増加、発散除去を確認します。

## Taylor–Greenによる検証 {#taylorgreen-verification}

[0,2π)²、粘性νで、

\[
u=\sin x\cos y\,e^{-2\nu t},\qquad
v=-\cos x\sin y\,e^{-2\nu t}.
\]

を使います。T=0.5、ν=0.1、N=16、32、64で速度誤差が2次収束します。平均運動エネルギーはe^(−4νt)/4です。段階の射影乗数を黙って物理圧力と呼ぶことはせず、最後の圧力推定を運動量右辺から再構成します。圧力次数の検証は主張していません。

![射影の収束とエネルギー](figures/solver-foundations.png)

[再現可能な測定値](figures/solver-foundations.json)には離散発散の絶対値の最大を含めます。陽的時間刻みには移流・粘性の両制約が残ります。粘着壁キャビティ、SIMPLE／PISO、円柱後流、混合FEM、乱流モデル、実験に対する妥当性確認は、この周期テストでは実装していません。別の低Mach数[LBMモデル](lattice-boltzmann.md)と比較してください。

[Arakawa A／B／C比較](geophysical-grids.md)ではMAC配置を地球流体の文脈に置きます。面位置が一致しても、Coriolisや渦位のアルゴリズムが自動的に備わるわけではありません。
