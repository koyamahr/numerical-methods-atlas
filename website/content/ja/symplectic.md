# シンプレクティック積分：正準写像とエネルギーを分ける

シンプレクティック積分器は正準2形式を保ちながらHamilton系を進めます。多くの軌道・粒子積分の良い長時間挙動を支える写像の性質ですが、元のHamiltonianを一般に厳密保存するわけでは**ありません**。[Hamilton写像ノート](#/hamiltonian)は2つの問いを計算例で分けます。

![調和・4次振動子の固定刻みエネルギーと位相空間比較](figures/hamiltonian.png)

## 写像が保存するもの {#what-the-map-preserves}

状態z=(q,p)に対し、Hamilton方程式とシンプレクティック条件は、

\[
\dot z=J\nabla H(z),\qquad J=\begin{pmatrix}0&I\\-I&0\end{pmatrix},
\qquad D\Phi_h(z)^T J D\Phi_h(z)=J.
\]

です。最後の恒等式は各数値ステップが正準変換であることを示します。1自由度ではdet(D Phi)=1と同値で、向き付き位相面積を保ちます。高次元で総体積だけを保つ条件は、それより弱いものです。

2形式の保存、Hの保存、時間対称性Phi_(−h)=Phi_h^(−1)を別々に検査します。シンプレクティックEulerはその違いの例で、一般に厳密エネルギー保存でも時間対称でもありません。

## Hamiltonianを分けて厳密な部分流を合成する {#split-the-hamiltonian-compose-exact-subflows}

単位質量の可分系H(q,p)=p²/2+V(q)では、2つの部分流はドリフトとキックです。

\[
D_h(q,p)=(q+hp,p),\qquad K_h(q,p)=(q,p-h\nabla V(q)).
\]

それぞれがシンプレクティックで、合成もそうなります。ノートにはkick–driftのシンプレクティックEulerと、対称2次のStörmer–Verlet、

\[
p_{n+1/2}=p_n-\frac h2\nabla V(q_n),\quad
q_{n+1}=q_n+h p_{n+1/2},\quad
p_{n+1}=p_{n+1/2}-\frac h2\nabla V(q_{n+1}).
\]

があります。これは力学のleapfrog／速度Verletで、[時間積分ノート](time-integration.md)の2ステップスカラー漸化式とは異なります。

## 合成で4次へ {#fourth-order-by-composition}

VerletステップをS2(h)とすると、4次合成の一例は、

\[
S_4(h)=S_2(a h)\,S_2(b h)\,S_2(a h),\qquad
a=\frac1{2-2^{1/3}},\quad b=-\frac{2^{1/3}}{2-2^{1/3}}.
\]

です。[Yoshida（1990）](https://doi.org/10.1016/0375-9601(90)90092-3)は高次シンプレクティック合成を発展させます。bが負なので内部部分ステップは時間を逆行します。ここでの滑らかな保存系には適しますが、不可逆な拡散、衝撃波、衝突処理へ単に適用することは正当化されません。高次でも無条件安定や同一コストの優位性は示せません。

## エネルギーと修正Hamiltonian {#energy-and-a-modified-hamiltonian}

後退誤差解析は近傍の、一般には形式的な修正Hamiltonianを記述します。滑らかさ、有界軌道、小刻みなどの仮定で、小さな長時間エネルギー誤差を説明できます。すべての軌道・刻みで元のHが厳密不変とはしません。[Hairer・Lubich・Wanner（2003）](https://doi.org/10.1017/S0962492902000144)が幾何学的な視点と仮定を論じます。

特別な振動子H=(p²+q²)/2では、kick–drift–kick Verletは、

\[
I_h=\frac12p^2+\frac12\left(1-\frac{h^2}{4}\right)q^2
\]

を丸め誤差まで保存し、H自体は振動します。この不変量から、係数を変えていないHamiltonian流が厳密に数値の時間h写像だとは言えません。|h|<2では有界ですが、それを超えるとシンプレクティックなまま**不安定**になり得ます。

## 陰的中点則とRK4の比較 {#implicit-midpoint-and-rk4-as-comparisons}

陰的中点則は端点方程式を正確に解くとシンプレクティックかつ時間対称です。この2次振動子ではHを丸め誤差まで保存しますが、非2次Hを厳密保存するとは限りません。古典的RK4は4次ですが、一般にはシンプレクティックでも時間対称でもありません。短時間精度の良さだけでは写像の幾何は保証されません。

第2問題はH=p²/2+q²/2+q⁴/4という滑らかな非線形振動子です。中点則の特別な2次エネルギー保存と一般的主張の違いが見えるようになります。

## 再現可能なノートと検査 {#reproducible-notebook-and-checks}

```python
from numart.hamiltonian import trajectory, energy, canonical_step, J
t, z = trajectory(h=0.2, steps=1000, method='yoshida4', system='quartic')
print(max(abs((energy(z, 'quartic')-energy(z[0], 'quartic'))/energy(z[0], 'quartic'))))
_, M = canonical_step([0.7, 0.4], 0.2, 'yoshida4', 'quartic', True)
print(M.T @ J @ M - J)
```

[計算データとソース記録](figures/hamiltonian.json)は、5手法、2つのHamiltonian、h=0.1、0.2、0.4の30軌道を、(q,p)=(1,0.2)からT=200まで供給します。描画軌道は最大1001標本ですが、最大エネルギー誤差は**全積分ステップ**を使います。位相パッチは(0.7,0.4)中心の正方形へ1ステップ作用させます。標本多角形は図示で、局所欠損は中心の解析的な写像Jacobianを使います。

テストは厳密振動子に対する収束、解析Jacobianと独立差分、両ポテンシャルの正準恒等式、対称法の時間反転、Verletの2次不変量、中点則の2次・非2次エネルギーの違いを確認します。教育用固定刻み例であり、軌道精度や時間コストの順位ではありません。

## 粒子重力へつなぐ {#connecting-to-particle-gravity}

固定刻みと、整合した位置依存ポテンシャルの勾配である力が分割合成の議論を支えます。一般の近似ツリー力、変化する開口判定、場当たり的な格子補間、状態依存の刻み選択が、その証明を自動的に保つわけではありません。力近似と時間積分を合同で検査する必要があります。[粒子重力とPoisson解法](particle-gravity.md)、[重力境界核](gravity-boundaries.md)へ進んでください。
