# MHD：制約輸送法と発散クリーニング

[GSPH／GSPMHDノート](gsph.md)は別の粒子法の分岐を説明します。[相対論的発展の調査](relativistic-hydrodynamics.md)は、CT、基本変数回復、動的時空を含むSRMHD・GRMHDをたどります。以下のNewton力学的な平面モデルは、どちらも実装していません。

## 問題と単位 {#problem-and-units}

モデルは周期単位正方形上の平面2次元理想MHDで、`γ=5/3`、`μ0=1`、`vz=Bz=0`です。配列添字は`[x,y,variable]`、状態は`q=(ρ,mx,my,E,Bx,By,ψ)`、`E=p/(γ-1)+ρ(vx²+vy²)/2+(Bx²+By²)/2`です。Orszag–Tangの初期条件は、

\[
\rho=\frac{25}{36\pi},\quad p=\frac5{12\pi},\quad
\mathbf v=(-\sin2\pi y,\sin2\pi x),\quad
\mathbf B=\frac1{\sqrt{4\pi}}(-\sin2\pi y,\sin4\pi x).
\]

です。広く使われる圧縮性テストの規格化で、[Orszag–Tang（1979）](https://doi.org/10.1017/S002211207900210X)の元の非圧縮MHD研究の完全な再現ではありません。[MASCLET論文](https://doi.org/10.1093/mnras/staa877)は、この圧縮性規格化の参照先のひとつです。

## CT：同じ辺電場を共有する {#ct-share-the-same-edge-electric-field}

磁場の法線成分をセル面に置き、角で共有する`Ez`によって両方向を更新します。例えば`Bx <- Bx - Δt D_y Ez`、`By <- By + Δt D_x Ez`です。対応する発散更新には`-D_xD_y Ez+D_yD_x Ez=0`が現れ、一致する離散発散を保存します。

初版は、Rusanov面流束から求めた電場を算術平均する単純なflux-CTを使います。面のリーマン問題は共通の法線磁場を使い、基本変数の圧力を保つよう界面エネルギーを調整します。更新後のセル中心磁場は面から平均します。全エネルギーを非保存的に再設定することはありません。Evans–Hawleyの全座標系の詳細やAthenaの風上CTを再現するものではありません。[Evans–Hawley（1988）](https://doi.org/10.1086/166684)、[Tóth（2000）](https://doi.org/10.1006/jcph.2000.6519)。

## GLM：発散誤差を輸送・減衰させる {#glm-transport-and-damp-divergence-errors}

セル中心磁場Bと補助変数ψを用いて、

\[
\partial_t\mathbf B+\nabla\cdot(\mathbf v\mathbf B-\mathbf B\mathbf v)+\nabla\psi=0,
\qquad
\partial_t\psi+c_h^2\nabla\cdot\mathbf B=-\alpha\psi.
\]

を解きます。誘導流束成分は`F_i(B_j)=v_i B_j-B_i v_j+δij ψ`です。初版は`ch=3`を固定し、`α=damping*ch/h`、`damping=0.18`を使います。線形ψ減衰を分離して指数的に積分し、残りを1次Rusanov流束と前進Eulerで更新します。エネルギーはψ²を含まない通常のMHDエネルギーです。この教育用Dedner型モデルはGLM／EGLM定式化の一部を扱います。[Dednerら（2002）](https://doi.org/10.1006/jcph.2001.6961)。

## ∇·Bを測る {#measuring-b}

CTは面磁場の差分、GLMはセル中心磁場の中心差分を使います。異なる離散発散の値から直接順位を付けられないため、記録には**演算子名**を含めます。固定した比較的散逸の強いGLM波速と対称なOT初期値では、中心差分発散が極めて小さいままの場合があります。OTだけではクリーニング性能の根拠として不十分です。

別の診断として`magnetic_error=0.01`で`Bx += 0.01sin(2πx)`を加え、初期気体圧力を保つようエネルギーを調整します。これは**標準OT問題ではありません**。発散波の輸送・減衰を調べ、減衰と数値粘性による誤差減少を区別します。CTは初期の離散制約を保存しますが、既存の磁気単極子誤差を自動的に取り除くものではありません。

## 検証範囲 {#verification-scope}

テストでは周期質量・全エネルギー、選定ケースの密度・圧力の正値性、CTの発散保存、GLMの注入誤差除去を確認します。参照コード比較、格子収束、Brio–Wu、磁場ループ移流、Alfvén波は今後の課題です。低解像度・1次OT図は、磁場制約の処理を学ぶ導入例です。

## 時間発展 {#time-evolution}

[動画ギャラリー](movies.md)には、64²のOrszag–Tangの[CT](#/movies?case=orszag-tang-ct)と[GLM](#/movies?case=orszag-tang-glm)の動画があります。実際の適応CFLスナップショット時刻と、それぞれの離散発散診断は異なります。再生から同一精度の順位は導きません。
