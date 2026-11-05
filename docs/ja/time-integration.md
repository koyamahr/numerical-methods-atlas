# 時間積分とleapfrog法

空間再構成と時間積分は独立した選択です。空間離散化後、PDEはODE系dU/dt = L(U)になります。精度、安定性、単調性、散逸、計算量は両者に依存します。[時間積分ノート](#/time-integration)ではy′=i y、y(0)=1を使い、時間積分の選択を切り分けます。

## ひとつの振動子と12手法 {#twelve-methods-on-one-oscillator}

厳密解exp(i t)は単位円をたどります。前進Eulerと後退Eulerは1次精度で、この無減衰振動子に対して前者は増幅、後者は減衰します。陽的RK2にはHeun／SSPRK(2,2)、陽的中点、Ralstonがあります。Kutta RK3、SSPRK(3,3)、SSPRK(4,3)は3次、古典的RK4とSSPRK(5,4)は4次です。陰的中点則は2次で、この線形振動子の振幅を保存しますが、位相には誤差があります。[RK系譜の章](runge-kutta.md)と[系譜ノート](#/runge-kutta)で段数・次数・SSP、非線形テストを比較できます。

y′=lambda yに対してz=lambda delta tと置くと、1ステップ増幅係数の例は、

\[
R_{\rm FE}=1+z,\quad R_{\rm BE}=\frac1{1-z},\quad
R_{\rm midpoint}=\frac{1+z/2}{1-z/2}.
\]

です。このスカラー線形方程式では、3種のRK2、Kutta RK3／SSPRK(3,3)、古典的RK4のRK係数は、それぞれ2次、3次、4次までの指数関数のTaylor多項式になります。SSPRK(4,3)には4次項z⁴/48、SSPRK(5,4)には5次項もあります。同じスカラー増幅係数でも、非線形RK段階が同じとは限りません。SSP性は空間演算子の前進Euler限界に依存し、無条件安定ではありません。

## leapfrog法には2つの根が必要 {#leapfrog-needs-two-roots}

1階の方程式系を中心差分で進める2ステップ漸化式は、

\[
y^{n+1}=y^{n-1}+2z y^n,\qquad
\xi_\pm=z\pm\sqrt{1+z^2}.
\]

です。zがゼロへ向かうと+1へ近づく根が物理モード、−1へ近づく根がステップごとに交互に変わる計算モードを担います。両方の根と重複度が重要です。z=i sigmaでは、|sigma|<1なら異なる2根の絶対値は1です。|sigma|=1では重根によって線形増大する解があり得るため、一般的な有界性の主張に端点を含めてはいけません。その上では一方の根が等比的に増幅します。

y(0)に加えて開始値が必要です。本実装ではRK4で1ステップ進め、必要に応じてy(1)へ実摂動epsilonを加えます。lambda=0なら、偶数番目の標本は1、奇数番目は1+epsilonとなり、計算モードを直接示せます。ノートの振動子では物理モードも同時に変化します。

Robert–Asselin系などの時間フィルターは、減衰と精度のトレードオフを伴って挙動を変えます。[Williams（2009）](https://doi.org/10.1175/2009MWR2724.1)を参照してください。初版にはフィルターを適用していません。

## 粒子leapfrogは別の定式化 {#particle-leapfrog-is-a-different-formulation}

位置と速度をずらして更新するkick–drift法や、2階の力学系に対する速度Verletも、leapfrogと呼ばれることがあります。変数が異なる時刻位置にあり、シンプレクティックな解釈にはその構造を使います。上のスカラー漸化式は、完全なSPH粒子積分器の実演でも、一般の力学系の長時間エネルギー保存の証明でもありません。

## ノートを再現して読む {#reproduce-and-read-the-notebook}

```python
from numart.time_integration import linear_trajectory, leapfrog_roots
t, y = linear_trajectory(rate=1j, dt=0.1, steps=200, method='leapfrog')
print(leapfrog_roots(0.1j))
```

ブラウザーでは、終了時刻20でPython計算した軌道から、12手法、7刻み幅、leapfrog開始摂動3種を選べます。不安定な標本では軸範囲が広がります。陰的求解とRK段数が異なるため、同じ時間区間でも同じ計算量とは限りません。テストでは時間収束次数、leapfrogの根、交互モード、中点則の振幅を確認します。

これらの振動子軌道はスカラー安定性係数を評価し、この線形テスト方程式ではRK段階と代数的に等価です。別の系譜ノートでは完全な非線形段階を評価します。[空間安定性実験室](experiments.md)、[SPH](particles-sph.md)、[ALE](ale.md)へ進んでください。

## 正準的な力学写像 {#canonical-mechanical-maps}

[シンプレクティック積分の章](symplectic.md)では、調和・4次Hamilton系に対して、力学的なkick–drift–kick Verlet、吉田の4次合成、シンプレクティックEuler、陰的中点則を実装します。[写像ノート](#/hamiltonian)ではRK4と比較し、正準構造と厳密なエネルギー保存を分けます。
