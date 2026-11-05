# MHD：CT と divergence cleaning

## 問題と単位

2D planar ideal MHD、γ=5/3、μ0=1、vz=Bz=0、周期単位正方形を対象とします。
`q=(ρ,mx,my,E,Bx,By,ψ)`、配列順は `[x,y,variable]`。
Orszag–Tang は

\[
\rho=\frac{25}{36\pi},\quad p=\frac5{12\pi},\quad
\mathbf v=(-\sin2\pi y,\sin2\pi x),\quad
\mathbf B=\frac1{\sqrt{4\pi}}(-\sin2\pi y,\sin4\pi x).
\]

これは広く使われる圧縮性テストの正規化です。
元の [Orszag–Tang (1979)](https://doi.org/10.1017/S002211207900210X) の非圧縮 MHD の計算条件を完全再現したものではありません。
正規化の実装例は [MASCLET の論文](https://doi.org/10.1093/mnras/staa877) などでも確認できます。

## CT：同じ辺の電場を共有する

磁場の法線成分をセル面に置き、角の同じ `Ez` で両方向の磁場を更新します。
たとえば `Bx <- Bx - Δt D_y Ez`、`By <- By + Δt D_x Ez`。
発散の更新に `-D_xD_y Ez+D_yD_x Ez=0` が現れ、対応する離散発散が保存されます。

初版は Rusanov 面流束から電場を算術平均する単純な flux-CT 型です。
面 Riemann 問題には単一の法線磁場を与え、primitive 圧力を保つよう界面エネルギーを調整します。
更新後は面磁場からセル磁場を平均し直します。総エネルギーの非保存的リセットは行いません。
Evans–Hawley 原著の座標系や Athena の upwind CT をそのまま実装したものではありません。
[Evans–Hawley (1988)](https://doi.org/10.1086/166684)、
[Tóth (2000)](https://doi.org/10.1006/jcph.2000.6519)。

## GLM：発散誤差を波として運び、減衰させる

セル中心 B と補助変数 ψ を使い

\[
\partial_t\mathbf B+\nabla\cdot(\mathbf v\mathbf B-\mathbf B\mathbf v)+\nabla\psi=0,
\qquad
\partial_t\psi+c_h^2\nabla\cdot\mathbf B=-\alpha\psi
\]

を解きます（誘導流束の成分は `F_i(B_j)=v_i B_j-B_i v_j+δij ψ`）。
初版は固定 ch=3、`α=damping*ch/h`、damping=0.18。
ψ の線形減衰は指数関数で演算子分割し、その他は 1 次 Rusanov + forward Euler。
エネルギー変数は通常の MHD エネルギーで ψ² の項は含みません。
これは Dedner 型の教育実装で、すべての GLM／EGLM 変種を含むものではありません。
[Dedner ほか (2002)](https://doi.org/10.1006/jcph.2001.6961)。

## ∇·B の測り方

CT では面磁場の差、GLM ではセル中心 B の中心差分を使います。
どちらも**演算子名を付けて**記録し、異なる離散発散の値をそのままランキングにしません。
今回の GLM は固定で大きめの散逸波速を使い、対称な OT 初期値では中心差分発散が非常に小さくなることがあります。
OT の結果だけでは cleaning の能力を十分に検証できません。

そのため `magnetic_error=0.01` で `Bx += 0.01sin(2πx)` を与える別の診断を用意します。
初期のガス圧を保つようエネルギーを変更します。
この試験は**標準 OT そのものではありません**。
発散波の伝播と減衰を調べ、減衰だけでなく数値粘性も誤差を減らすことを区別します。
CT は既存の磁気単極子誤差を自動的に消す方法ではなく、初期の離散制約を保存する構造です。

## 検証範囲

周期領域の質量・総エネルギー、選定例の密度・圧力の正値性、CT の離散発散保存、GLM の誤差注入を自動確認します。
参照コードとの解の一致、格子収束、Brio–Wu、field-loop advection、Alfvén 波は今後の検証です。
低解像度・1次精度の OT 図は、磁場制約の仕組みを見るための初期例です。
