# 格子Boltzmann法：衝突、並進、流体運動の回復

**実装済み**：低Mach数・等温D2Q9–BGK、Guo体積力、周期境界、静止した中間壁バウンスバック。格子単位はΔx=Δt=ρ_ref=1、c_s²=1/3です。

## 1954年から1992年、2002年へ {#1954-1992-2002}

[Bhatnagar–Gross–Krook（1954）](https://doi.org/10.1103/PhysRev.94.511)の緩和モデルは格子BGKに先行します。[Qian–d'Humières–Lallemand（1992）](https://doi.org/10.1209/0295-5075/17/6/001)が格子BGK、[Guo–Zheng–Shi（2002）](https://doi.org/10.1103/PhysRevE.65.046308)が本実装の外力離散化の出典です。異なる発展として扱います。

D2Q9には静止分布1つ、軸方向4つ、対角方向4つがあり、それぞれの重みは4/9、1/9、1/36です。平衡分布は、

\[
f_q^{eq}=w_q\rho\left[1+3\boldsymbol c_q\cdot\boldsymbol u
+\frac92(\boldsymbol c_q\cdot\boldsymbol u)^2
-\frac32|\boldsymbol u|^2\right].
\]

です。衝突で分布を緩和し、その後に整数格子速度に沿って各分布を並進させます。

\[
f_q(\boldsymbol x+\boldsymbol c_q,t+1)
=f_q(\boldsymbol x,t)-\frac{f_q-f_q^{eq}}{\tau}+S_q.
\]

力密度Fに対し、Guo外力は、

\[
S_q=w_q\left(1-\frac1{2\tau}\right)
\left[3(\boldsymbol c_q-\boldsymbol u)
+9(\boldsymbol c_q\cdot\boldsymbol u)\boldsymbol c_q\right]\cdot\boldsymbol F,
\quad
\rho\boldsymbol u=\sum_q f_q\boldsymbol c_q+\frac{\boldsymbol F}{2}.
\]

を使います。密度は分布の総和、圧力はc_s²ρ、動粘性係数はν=c_s²(τ−1/2)です。[Chapman–Enskogの導出](chapman-enskog.md)で離散時間の半ステップ補正を説明します。τ>1/2はこの粘性を正にしますが、一般的な非線形安定性の保証ではありません。

## 独立した2つのテスト {#two-independent-tests}

![LBMのせん断減衰、壁面流れ、双曲型拡散](figures/kinetic-hyperbolic.png)

周期的な横せん断波はexp(−νk²t)で減衰し、独立に粘性を測れます。外力駆動Poiseuille流の厳密分布はu_x=F_x y(H−y)/(2ρ_refν)です。壁は最外の流体節点中心ではなく、その半格子間隔外に置きます。τ=0.8、最大速度0.01を固定し、Ny=8、16、32で壁位置と細分化を検証します。初期過渡は最も遅い粘性減衰時間の12倍まで計算し、有限時間誤差と空間誤差を区別します。

[データ記録](figures/solver-foundations.json)にはチャネル誤差、Mach数、力の設定、ステップ数があります。単体テストでは周期質量・運動量保存と平衡モーメントも確認します。BGKは単一緩和の基準例です。MRT／TRT、エントロピー型・キュムラント衝突、熱的・圧縮性LBM、移動壁、多相モデルは今後の拡張です。[射影法の流れ](incompressible.md)は別の離散系を解き、非圧縮性へのもうひとつの道を与えます。
