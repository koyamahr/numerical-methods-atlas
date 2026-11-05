# 極・円筒座標：テンソルと粘性

以下は円筒座標(r,phi,z)、phiはラジアン、r>0として、**正規直交基底(e_r,e_phi,e_z)の物理成分**を使います。平面極座標場はu_z=0、全z微分をゼロにします。座標基底のテンソル成分には別の計量因子があり、規約を混ぜると粘性力を誤ります。

円筒流体方程式の導出は[Richard Fitzpatrickの講義](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html)を参照してください。この章は一般の体積粘性の規約を明示し、解析的な場で検査します。

## 速度勾配：基底も微分する {#velocity-gradient-differentiate-the-basis-too}

L_ij=e_i·((e_j·grad)u)とします。行は速度成分、列は微分方向です。

\[
L=\begin{pmatrix}
\partial_r u_r & (\partial_\phi u_r-u_\phi)/r & \partial_z u_r\\
\partial_r u_\phi & (\partial_\phi u_\phi+u_r)/r & \partial_z u_\phi\\
\partial_r u_z & (\partial_\phi u_z)/r & \partial_z u_z
\end{pmatrix}.
\]

−u_phi/rと+u_r/rは基底の回転から生じます。D=(L+L^T)/2、theta=tr(L)を定義すると、

\[
\theta=\nabla\cdot u=\partial_r u_r+\frac{u_r}{r}
+\frac{\partial_\phi u_\phi}{r}+\partial_z u_z.
\]

です。`numart.coordinates`の入力`partials[...,i,j]`は、物理速度成分iを座標j=(r,phi,z)で普通に微分した値です。phi微分そのものを渡し、既にrで割った値を渡さないでください。

## Newton応力：独立な6成分すべて {#newtonian-stress-all-six-independent-components}

全応力sigma=−p I+tau、せん断粘性mu、体積粘性zetaとして、**3次元**構成則は、

\[
\tau=2\mu D+\lambda\theta I,\qquad
\lambda=\zeta-\frac23\mu.
\]

です。Stokes仮説はzeta=0という物質の仮定で、非圧縮条件theta=0とは異なります。mu>0、zeta≥0なら粘性散逸は非負です。

\[
\begin{aligned}
\tau_{rr}&=2\mu\,\partial_r u_r+\lambda\theta,\\
\tau_{\phi\phi}&=\frac{2\mu}{r}(u_r+\partial_\phi u_\phi)+\lambda\theta,\\
\tau_{zz}&=2\mu\,\partial_z u_z+\lambda\theta,\\
\tau_{r\phi}&=\mu\left(\partial_r u_\phi-\frac{u_\phi}{r}
+\frac{\partial_\phi u_r}{r}\right),\\
\tau_{rz}&=\mu(\partial_z u_r+\partial_r u_z),\\
\tau_{\phi z}&=\mu\left(\partial_z u_\phi+\frac{\partial_\phi u_z}{r}\right).
\end{aligned}
\]

下付き添字は共変座標基底ではなく**物理成分**を表します。工学的な非対角せん断速度は対応するDの2倍ですが、上の式へさらに2を掛けてはいけません。

## 応力の発散：単位体積あたりの粘性力 {#stress-divergence-the-viscous-force-per-volume}

対称な物理応力テンソルのf=div(tau)は、

\[
\begin{aligned}
f_r&=\partial_r\tau_{rr}+\frac1r\partial_\phi\tau_{r\phi}
+\partial_z\tau_{rz}+\frac{\tau_{rr}-\tau_{\phi\phi}}r,\\
f_\phi&=\partial_r\tau_{r\phi}+\frac1r\partial_\phi\tau_{\phi\phi}
+\partial_z\tau_{\phi z}+\frac{2\tau_{r\phi}}r,\\
f_z&=\partial_r\tau_{rz}+\frac1r\partial_\phi\tau_{\phi z}
+\partial_z\tau_{zz}+\frac{\tau_{rz}}r.
\end{aligned}
\]

です。加速度への寄与はf/rho、圧力の−grad(p)は別です。応力微分に係数変化を含めれば、空間変化するmu・zetaにも使えます。Pythonの`partials[...,i,j,k]`は物理応力成分(i,j)の座標k微分です。

## 一定粘性とベクトルLaplacian {#constant-viscosity-and-the-vector-laplacian}

mu・lambdaが一定の場合に限り、力を、

\[
f=\mu\nabla^2 u+(\mu+\lambda)\nabla\theta.
\]

と簡略化できます。スカラーgについて、

\[
\Delta_s g=\frac1r\partial_r(r\partial_r g)
+\frac1{r^2}\partial_\phi^2g+\partial_z^2g.
\]

と置くと、**ベクトル**Laplacianの物理成分は、

\[
\begin{aligned}
(\nabla^2u)_r&=\Delta_su_r-\frac{u_r}{r^2}
-\frac2{r^2}\partial_\phi u_\phi,\\
(\nabla^2u)_\phi&=\Delta_su_\phi-\frac{u_\phi}{r^2}
+\frac2{r^2}\partial_\phi u_r,\\
(\nabla^2u)_z&=\Delta_su_z.
\end{aligned}
\]

です。非圧縮・一定粘性でも、thetaが消えるだけで径・方位方向の計量項は残ります。変係数でmuを微分の外へ出すと2D·grad(mu)、theta grad(lambda)を落とすため、応力発散全体を評価します。

## 軸対称、極座標断面、物質加速度 {#axisymmetry-polar-slices-and-material-acceleration}

軸対称はphi微分を消しますが、u_r/r、−u_phi/r、応力発散の計量項を**消しません**。旋回もあり得ます。3次元Newton流体の平面極座標断面では2mu/3補正とtau_zz=lambda thetaを残します。真の2次元構成モデルでは偏差のトレース減算が異なるため、別に宣言します。

スカラー移流微分はD_s/Dt=partial_t+u_r partial_r+(u_phi/r)partial_phi+u_z partial_zです。ベクトル物質加速度には径・方位方向の追加項があります。

\[
a_r=\frac{D_su_r}{Dt}-\frac{u_\phi^2}{r},\qquad
a_\phi=\frac{D_su_\phi}{Dt}+\frac{u_ru_\phi}{r},\qquad
a_z=\frac{D_su_z}{Dt}.
\]

これらの慣性項は粘性の計量項とは別です。

## 座標基底テンソルと変換 {#coordinate-basis-tensors-and-transformations}

円筒座標基底は(partial_r,partial_phi,partial_z)=(e_r,r e_phi,e_z)、計量はdiag(1,r²,1)です。物理u_phi=r u^phi、物理tau_phi,phi=r² tau^{phi,phi}=tau_{phi,phi}^{coordinate}/r²となります。共変・反変・物理成分の配列は、この因子なしには交換できません。

非ゼロChristoffel記号にはGamma^r_phi,phi=−r、Gamma^phi_r,phi=Gamma^phi_phi,r=1/rがあります。共変微分は上で明示した基底変化を取り込みます。列をe_r、e_phi、e_zとする直交行列Qで、L_cart=Q L_cyl Q^T、tau_cart=Q tau_cyl Q^Tと直交座標へ変換します。

## 解析的検査と軸 {#analytic-checks-and-the-axis}

- **剛体回転**：u_phi=Omega rではLが反対称、D=0、粘性応力ゼロです。partial_r u_phiだけでは偽のせん断を生みます。
- **円管Poiseuille流**：u_z=Umax(1−r²/R²)でtau_rz=−2mu Umax r/R²、f_z=−4mu Umax/R²です。定常軸運動量にはdp/dz=f_zが必要です。
- **円形Couette流**：u_phi=A r+B/rでtau_rphi=−2mu B/r²となり、境界外の方位粘性力発散はゼロです。
- **直交座標のアフィン場**：ランダムな一定直交速度勾配を円筒へ変換し戻します。一定直交応力も角方向の基底微分を含めれば発散ゼロです。

散逸恒等式も検査します。

\[
\tau:D=2\mu D_{\rm dev}:D_{\rm dev}+\zeta\theta^2\ge0.
\]

関数はr>0を要求します。軸ではrを任意の小数に置き換えず、正則性と解析極限を使います。滑らかな軸対称場はu_r・u_phi=O(r)、u_z=u_z(0)+O(r²)で、軸方向成分のスカラー径Laplacianは2partial_r²u_zへ向かいます。非軸対称の正則直交場は異なる成分極限を持ち、一様な直交平行移動でもu_r=O(r)とは限りません。

```python
import numpy as np
from numart.coordinates import cylindrical_velocity_gradient, newtonian_stress
r, omega = 0.7, 2.0
u = np.array([0., omega*r, 0.])
du = np.zeros((3,3)); du[1,0] = omega
L = cylindrical_velocity_gradient(r, u, du)
assert np.allclose(newtonian_stress(L), 0.)
```

コードは指定点のテンソル恒等式を検査します。円筒Navier–StokesのPDEソルバー、軸境界方式、球座標実装は今後の課題です。
