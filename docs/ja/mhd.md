# MHD：制約輸送法と発散クリーニング

[GSPH／GSPMHDノート](gsph.md)は別の粒子法の分岐を説明します。[相対論的発展の調査](relativistic-hydrodynamics.md)は、CT、基本変数回復、動的時空を含むSRMHD・GRMHDをたどります。以下のNewton力学的な平面モデルは、どちらも実装していません。

## 問題と単位 {#problem-and-units}

従来のOrszag–Tang基準例は周期単位正方形上の平面2次元理想MHDで、`γ=5/3`、`μ0=1`、`vz=Bz=0`です。配列添字は`[x,y,variable]`、状態は`q=(ρ,mx,my,E,Bx,By,ψ)`、`E=p/(γ-1)+ρ(vx²+vy²)/2+(Bx²+By²)/2`です。Orszag–Tangの初期条件は、

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

テストでは周期質量・全エネルギー、選定ケースの密度・圧力の正値性、CTの発散保存、GLMの注入誤差除去を確認します。後述のHLLD節にBrio–Wu、Alfvén波の格子細分化、磁場ループを追加しました。外部参照コードとの比較は今後の課題です。低解像度・1次OT図は、磁場制約の処理を学ぶ導入例です。

## 時間発展 {#time-evolution}

[動画ギャラリー](movies.md)には、64²のOrszag–Tangの[CT](#/movies?case=orszag-tang-ct)と[GLM](#/movies?case=orszag-tang-glm)の動画があります。実際の適応CFLスナップショット時刻と、それぞれの離散発散診断は異なります。再生から同一精度の順位は導きません。


## HLLDと標準波動テスト {#hlld-and-standard-wave-tests}

[HLLDの比較を開く](#/mhd-tests)。新しい理想MHD計算は、上の平面Orszag–Tang基準例と異なり、速度・磁場の3成分をすべて保持します。μ0=1、q=(ρ,ρvx,ρvy,ρvz,E,Bx,By,Bz)、E=p/(γ−1)+ρ|v|²/2+|B|²/2です。HLLDは外側の高速波の間で接触波と2つの回転波を解像します。中間のstar／double-star状態では共通の法線磁場を使い、不正な状態ではHLLEに切り替え、面ごとの回数を記録します。原典の書誌は[Miyoshi–Kusano（2005）](https://doi.org/10.1016/j.jcp.2005.02.017)、式の照合には公開された[Athena++ HLLD実装](https://github.com/PrincetonUniversity/athena-public-version/blob/master/src/hydro/rsolvers/mhd/hlld.cpp)を使いました。独立した教育実装であり、Athena++の実行や原論文全体の再現ではありません。

3テストとも基本変数のMC勾配・SSPRK2・面の正値性のための縮小を使い、時間刻み再試行・HLLE切替を記録します。保存平均値はクリップしません。選定ケースの正値性は一般的な頑健性の証明ではありません。

- **Brio–Wu**：γ=2、[0,1]のx=0.5で、左(ρ,p,By)=(1,1,1)、右(0.125,0.1,−1)、Bx=0.75、速度とBzは0。開放端、t=0.1、CFL 0.35です。400セルのHLLE／HLLDと800セルのHLLDを比較します。厳密解の重ね描きや普遍的な一意性の主張ではなく、数値格子比較です。[Brio–Wu（1988）](https://doi.org/10.1016/0021-9991(88)90120-9)。
- **円偏波Alfvén波**：γ=5/3、ρ=1、p=0.1、Bx=1、(By,Bz)=0.1(cos(2πx),sin(2πx))、(vy,vz)=−(By,Bz)、vx=0。周期単位区間で1周期t=1、CFL 0.35です。厳密な保存変数セル平均には、sincで平均した横磁場と一定の全エネルギーを使います。平均磁場の二乗からエネルギーを作り直しません。HLLEとHLLDの32・64・128・256セルで、横磁場の平均絶対誤差の最細格子の観測次数は両方とも約1.98です。
- **弱い磁場ループ**：γ=5/3、ρ=p=1、v=(2,1,0)、Az=10⁻³max(0.3−r,0)。周期2 × 1領域、t=1、CFL 0.3、64 × 32と128 × 64セルです。CT／GLMそれぞれでHLLE・HLLDを比較します。有限磁場の平行移動は診断用の参照であり、厳密解ではありません。磁気力は小さいものの0ではありません。

![Brio–Wuの数値分布](figures/mhd-tests/brio-wu.png)
![円偏波Alfvén波の格子細分化](figures/mhd-tests/alfven.png)
![弱い磁場ループの比較](figures/mhd-tests/field-loop.png)

## ループ問題のCT-ContactとGLMの範囲 {#ct-contact-and-glm-scope-in-the-loop-test}

CTは角のポテンシャルの離散回転から面磁場を初期化します。角のEMFの横方向微分には面の質量流束の符号による接触波の風上化を使います（[Mignone–Del Zanna（2021）の式20〜22](https://arxiv.org/html/2004.10542v1)のCT-Contact）。格子に沿う1次元極限で面の誘導流束に一致します。UCT-HLLDではありません。SSPRKの各段階で共有回転により面発散を保存し、セル磁場を面から平均します。全エネルギーは再設定しません。

GLMはセルAzの中心差分回転からセル磁場を初期化し、面で縦方向部分系を先に解きます。

\[
 B_n^*=\frac{B_{n,L}+B_{n,R}}2-\frac{\psi_R-\psi_L}{2c_h},\qquad
 \psi^*=\frac{\psi_L+\psi_R}2-\frac{c_h(B_{n,R}-B_{n,L})}2.
\]

HLLD／HLLEへ共通のBn*を渡し、面の基本変数圧力を保ちます。Bn・ψの流束はψ*・ch²Bn*です。ch=4、減衰率0.18ch/hでSSPRK2の前後にψを半刻みずつ指数減衰させます。Eにはψのエネルギーを含めません。[Mignone–Tzeferacos（2010）](https://arxiv.org/abs/0911.3410)の縦方向解法を参考にした保存的GLMモデルであり、同論文のCTU積分やEGLM変種ではありません。固定クリーニング速度は時間刻み数にも影響します。

初期磁場の離散化と離散発散演算子が異なり、磁気エネルギー比は各計算自身の初期セル磁場エネルギーで規格化します。同一精度・同一計算費用でのCT／GLMの順位は導けません。128 × 64ではCTの最大面発散は4 × 10⁻¹⁶未満、GLMの最大中心差分発散は約3.7 × 10⁻⁴です。これらは演算子に依存するB/長さの次元の数値です。公開ループ計算のHLLE切替・再試行はすべて0でした。外部コードとの比較、強磁場ループ、UCT-HLLDは今後の課題です。

再現は`python scripts/build_mhd_tests.py`です。[設定・診断・ハッシュ](figures/mhd-tests/mhd-tests.json)と[計算済み保存変数配列](figures/mhd-tests/fields.npz)を取得できます。
