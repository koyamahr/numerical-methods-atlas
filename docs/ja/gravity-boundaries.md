# 重力核：孤立FFTと周期スラブ

境界条件はPoissonソルバーの定義の一部です。有限の孤立質量、完全周期の密度偏差、上下が真空で水平周期の円盤は異なるGreen関数を持ち、配列のゼロ埋めだけでは適切な核を選べません。

孤立構成は[Computer Simulation Using Particles](https://doi.org/10.1201/9780367806934)のHockney–Eastwood倍領域畳み込みに従います。円盤は[Koyama・Ostriker（2009）、ApJ 693、1316–1345](https://doi.org/10.1088/0004-637X/693/2/1316)第2.3節・付録A（[著者プレプリント](https://arxiv.org/abs/0812.1846)）を参照します。水平周期、鉛直領域倍増、モード依存鏡像補正を使います。以下は独自に明示した変換規格化で核を導出・検査し、有限標本DFTと連続Fourier係数を区別します。

![孤立倍格子畳み込み、スラブ平均モード、正弦薄層と標本・連続変換の差](figures/gravity-boundaries.png)

## 孤立重力：倍格子上の線形畳み込み {#isolated-gravity-linear-convolution-on-a-doubled-grid}

G=1で3次元孤立ポテンシャルは、

\[
\phi(\boldsymbol x)=-\int\frac{\rho(\boldsymbol x')}{|\boldsymbol x-\boldsymbol x'|}\,d^3x'.
\]

です。Nx×Ny×Nzの密度を2Nx×2Ny×2Nzへゼロ埋めし、倍領域の符号付き格子差で核を作ります。密度FFTと核FFTを掛け、逆変換後に元の物理領域を取り出します。

\[
\phi_{\rm physical}=\Delta V\,
\mathcal R\,\operatorname{IFFT}\bigl[
\operatorname{FFT}(\rho_{\rm padded})\operatorname{FFT}(K_{\rm doubled})\bigr].
\]

取り出す領域内の源・標的の距離は各方向で元の領域長より小さいため、倍領域の循環畳み込みが所望の非周期離散畳み込みに一致します。周期鏡像を遠ざけるだけより強い性質です。核を通常の周期記号−4pi/k²へ置き換えると別問題になります。

特異な原点核を明示する必要があります。`isolated_potential`は`self_kernel`を既定ゼロ、それ以外を−1/rとし、有限源セルでの核積分はしません。直接格子和との丸め誤差での一致は畳み込みとゼロ埋めを検証し、高次の連続精度や唯一正しい自己セル規約を示すものではありません。孤立有限質量では無限遠でphi→0とできますが、表面密度が非ゼロのスラブでは一般にできません。

## スラブの水平Fourier変換 {#horizontal-fourier-transform-of-a-slab}

x・yを周期とし、長さLzの鉛直区間外で密度をゼロにします。水平波数k_perpに対し、規約を、

\[
\widehat\rho_{\boldsymbol k}(z)=\frac1{L_xL_y}
\int\rho(x,y,z)e^{-i(k_xx+k_yy)}\,dx\,dy,\qquad
k=\sqrt{k_x^2+k_y^2}.
\]

とします。Poisson方程式は(partial_z²−k²)phi_hat=4pi G rho_hatです。4pi Gを含む完全な重力核は、

\[
\mathcal G_k(s)=\begin{cases}
-\dfrac{2\pi G}{k}e^{-k|s|},&k>0,\\
2\pi G|s|,&k=0,
\end{cases}\qquad
\widehat\phi_{\boldsymbol k}(z)=\int\mathcal G_k(z-z')\widehat\rho_{\boldsymbol k}(z')\,dz'.
\]

です。重力係数を核に含める符号規約で、文献によっては外に出します。s=0の微分の跳びが4pi Gとなり、符号・規格化を確認できます。非ゼロ水平モードは外部で減衰し、ゼロモードは水平平均質量薄層です。外部に有限の力があり、ポテンシャルは減衰しません。

## 鉛直Fourier係数と鏡像因子 {#the-vertical-fourier-coefficient-and-the-image-factor}

必要な距離は|s|<Lzだけです。核を長さ2Lzの距離区間へ周期延長し、k_z,ell=pi ell/Lzとします。k>0の連続積分は、

\[
\widetilde{\mathcal G}_{k,\ell}
=\int_{-L_z}^{L_z}\mathcal G_k(s)e^{-ik_{z,\ell}s}\,ds
=-\frac{4\pi G}{k^2+k_{z,\ell}^2}
\left[1-(-1)^\ell e^{-kL_z}\right].
\]

です。偶関数の指数と余弦を積分して得られます。角括弧が通常の完全周期Poisson乗数との違いです。同じことは、zを倍増し、水平モード係数exp(−k Lz)の負の鏡像密度をLzずらして加え、通常の非ゼロPoisson乗数を適用しても表せます。

水平k=0モードの連続係数は、

\[
\widetilde{\mathcal G}_{0,\ell}=
\begin{cases}
2\pi G L_z^2,&\ell=0,\\
\dfrac{4\pi G[(-1)^\ell-1]}{k_{z,\ell}^2},&\ell\ne0.
\end{cases}
\]

です。この規約の全ゼロ係数は加法的なポテンシャル定数を決め、別の定数ゲージでも力は同じです。しかし**水平k=0モード全体**を落とすと、物理的な平均薄層を消してしまいます。本スラブソルバーは平均密度を引きません。

## 標本DFTは別の数値的対象 {#a-sampled-dft-is-a-different-numerical-object}

dz=Lz/Nz、s_jを2Nz個の符号付き鉛直格子差とすると、離散求積の乗数は、

\[
\widetilde{\mathcal G}^{\rm sampled}_{k,\ell}
=\Delta z\sum_{j=0}^{2N_z-1}\mathcal G_k(s_j)
 e^{-2\pi i j\ell/(2N_z)}.
\]

です。標本核DFTの厳密なdz倍で、有限Nzでは上の連続積分とは同じではありません。k>0の実数値は等比級数で、

\[
\widetilde{\mathcal G}^{\rm sampled}_{k,\ell}
=-\frac{2\pi G\Delta z}{k}
\frac{\sinh(k\Delta z)}{\cosh(k\Delta z)-\cos(\pi\ell/N_z)}
\left[1-(-1)^\ell e^{-kL_z}\right].
\]

とも評価できます。k=0には独立した分岐を使い、桁落ちとゼロ除算を避けます。sinh・cosh・cosの展開により、固定した解像モードでdz→0なら連続係数を回復し、テストで収束を測ります。連続係数を有限標本和そのものと誤表示しないための区別です。

`slab_green_transform`は`sampled`と`continuum`の両表現を公開します。`slab_potential`の既定は標本核で、FFT結果が独立した鉛直直接求積に一致します。連続オプションは解析係数を適用します。小さな独立実装の核実験室で、原論文の全数値選択や星間物質シミュレーションの再現ではありません。

## 銀河計算の前に境界の物理を確かめる {#check-the-boundary-physics-before-a-galaxy-calculation}

```python
import numpy as np
from numart.gravity_boundaries import isolated_potential, slab_potential
rho = np.ones((8,8,16))
phi_slab = slab_potential(rho)  # horizontal mean mode retained
phi_isolated = isolated_potential(rho, spacing=(1/8,1/8,1/16))
```

2配列は別の境界問題です。テストは、境界近くの源も含む孤立FFTと非周期直接和、平均平面の2次ポテンシャル・内部線形加速度、正弦薄層の指数場を確認します。表面密度Sigmaの薄層では平均ポテンシャルは2pi G Sigma |z−z0|、非ゼロモードはexp(−k|z−z0|)で減衰します。

[核の検証記録](figures/gravity-boundaries.json)にはソースハッシュと表示検査の実測誤差があります。

通常の水平周期を使い、せん断周期の再配置はしません。実用化前には質量割当て、自己セル積分、鉛直求積精度、力の微分、重力・流体結合を検査する必要があります。[粒子重力](particle-gravity.md)、[マルチグリッド](elliptic.md)、[Hamilton写像](symplectic.md)へ進んでください。
