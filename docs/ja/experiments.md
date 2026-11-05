# インタラクティブ実験ガイド

Web版には[安定性実験室](#/experiments)と[収束実験ノート](#/convergence)があります。実験室はブラウザーで計算し、収束ノートは初期ギャラリーの記録にある測定値を表示します。根拠となるデータの出所は異なります。

## ブラウザー内の周期移流 {#periodic-advection-in-the-browser}

モデルは次の周期移流方程式です。

\[
u_t+a u_x=0,\qquad x\in[0,1],\qquad u(x+1,t)=u(x,t).
\]

セル中心に置いた64個の標本点、`h=1/64`、速度`a=+1`または`a=-1`、`Δt=|C|h`を使います。符号付きCourant数は`C=aΔt/h`です。画面では`0.05≤|C|≤1.5`と0〜100時間ステップを選べます。厳密な比較値は、連続的に移動した分布`u(x-at,0)`を同じ格子点で標本化します。

初期値は正弦波、`[0.25,0.65)`で1、それ以外で0の矩形パルス、または小さな高周波摂動を加えた正弦波から選べます。

\[
u(x,0)=\sin(2\pi x)+10^{-3}
\left[\sin(2\pi(N/2)x)+\cos(2\pi(N/4)x)\right].
\]

摂動にはNyquistモードと、それより短波数の格子スケールのモードを含めます。丸め誤差だけに頼らず不安定な増幅を見えるようにしています。矩形パルスは拡散や分散振動を示すためのもので、滑らかな解の収束テストではありません。

## 4つの離散更新 {#four-discrete-updates}

`numart.advection.difference_step`とブラウザーは、FTCS、風上、古典的Lax–Friedrichs、Lax–Wendroffを実装しています。風上法は速度の符号で差分の向きを切り替えます。背景は[安定性の章](stability.md)を参照してください。FTCSでは、

\[
u_j^{n+1}=u_j^n-\frac C2(u_{j+1}^n-u_{j-1}^n),\qquad
G(\theta)=1-iC\sin\theta.
\]

となります。増幅係数の2乗は`1+C²sin²θ`です。依存領域から必要な`|C|≤1`を満たしても、ゼロでないCでは増幅するモードが存在します。風上、LF、LWは、この周期・定係数問題に対して`|C|≤1`でFourier安定条件を満たします。

解のグラフと`|G(θ)|`を同時に更新します。最大値は64点格子の実データに対応する、異なるすべての離散Fourier波数で評価します。破線は`|G|=1`を示します。解が増幅すると縦軸の範囲を広げ、計算値を切り捨てません。点値L1誤差、最大振幅、算術平均の変化は別々に報告します。

これらの性質は、この線形周期モデルについてのものです。非線形系、別の境界、別の時間積分へ自動的に引き継ぐことはできません。不安定な増大では、桁落ちや浮動小数点丸めによって平均値の測定も損なわれる場合があります。

## 再現性と出力 {#reproducibility-and-export}

ブラウザーの計算カーネルを、Python実装で作った24の参照ケースと比較しています。4手法、符号付きCourant数6通り、各ケース12回更新です。テストでは標本配列全体と複素Fourier増幅係数を比較します。別のテストで、CFL=1での厳密な1セル移動、方向反転、周期折返し、収束次数の算術を確認します。参照データは`numart/advection.py`のSHA-256を記録し、ソースが変わると参照データを更新するまでブラウザー数値テストは失敗します。

実験データのダウンロードには、設定、格子座標、初期・計算・厳密標本、診断量、Python参照ハッシュを含めます。記録するのはJavaScriptによる計算です。ブラウザー内でPythonを実行しているという意味ではありません。

Pythonで同じ差分を適用する例です。

```python
import numpy as np
from numart.advection import difference_step

n, courant, steps = 64, 0.8, 40
x = (np.arange(n) + 0.5) / n
q = np.sin(2 * np.pi * x)
for _ in range(steps):
    q = difference_step(q, courant, "lax-wendroff")
exact = np.sin(2 * np.pi * (x - courant * steps / n))
print("pointwise L1 error:", np.mean(abs(q - exact)))
```

## 格子細分化の結果を読む {#reading-a-refinement-study}

ノートには初版の`docs/figures/validation.json`の測定値を使います。ソースハッシュと実行環境のバージョンを含む元の記録をダウンロードできます。これらはブラウザー実験室より前のデータであり、新しい実行時間の測定ではありません。

隣り合う格子間の実測次数は、

\[
p_{\mathrm{obs}}=
\frac{\log(E_{\mathrm{coarse}}/E_{\mathrm{fine}})}
{\log(N_{\mathrm{fine}}/N_{\mathrm{coarse}})}.
\]

です。

**DG移流**：周期スカラー輸送、終了時刻0.2、CFL 0.2、`N=8,16,32,64`、モード型Legendre P0／P1／P2とSSPRK3を使います。誤差は実装の求積点で標本化したRMSであり、別途積分したL2ノルムではありません。Ppでは`N(p+1)`個のスカラー未知数を持ちます。横軸を要素数と未知数で切り替えても、データは変わりません。滑らかな解の空間次数1、2、3と、SSPRK3の時間3次精度が期待される挙動を説明します。

**Eulerエントロピー波**：終了時刻1、CFL 0.3、`N=40,80,160`で、基本変数minmod MUSCLまたは成分別の差分WENO5-JSとSSPRK3を使います。誤差は密度点値のL1です。WENOの空間5次再構成が時間3次誤差を消すわけではなく、この有限系列の傾きから完全離散化の漸近5次収束を保証することはできません。Eulerでは点またはセルごとに3つのスカラー状態成分を持ちます。同じ未知数でも、計算量や近似空間が同じとは限りません。

誤差の減少、観測した傾き、正値性、小さな発散、性能比較は異なる問いに答えます。ノートではこれらを区別します。残る検証項目は[テスト問題の定義](benchmarks.md)と[実装ロードマップ](roadmap.md)を参照してください。

## 時間軌道と格子の接続 {#temporal-trajectories-and-mesh-connectivity}

[時間積分ノート](#/time-integration)は、12手法についてPythonで計算したy′=i yの軌道を選択表示します。終了時刻は20で固定し、刻み幅、leapfrog初期化摂動、2つの特性根、標本誤差、振幅を示します。これは事前計算したODEの結果であり、空間安定性実験室のブラウザー内計算とは異なります。[時間積分の定義](time-integration.md)を参照してください。

[格子エクスプローラー](#/meshes)は、頂点とセルを明示した3つのデータセットを表示します。セルを選ぶと面を共有する隣接セルが強調されます。ドロップダウンとキーボード操作可能な多角形で同じ選択ができます。幾何は固定され、流体計算は行いません。[格子の定義](meshes.md)、[ALE](ale.md)、[SPH](particles-sph.md)を参照してください。

どちらも`scripts/sync_web_content.py`で生成する`foundations.json`を公開し、時間積分・幾何モジュールのSHA-256を含めています。Pythonのテストでは収束次数、leapfrogモード、中点則の振幅、カーネル規格化、格子位相、移動体積での一様状態保存を確認します。

## Hamilton写像 {#hamiltonian-maps}

[Hamilton系ノート](#/hamiltonian)は、Pythonで計算した30ケースを必要時に読み込みます。同じ固定刻みでエネルギー誤差を比較し、各写像の位相軌道や正方形境界の像を調べます。解析的な局所Jacobianの診断によって、シンプレクティック構造とエネルギー保存を区別します。[定義](symplectic.md)を参照してください。データと図は`python scripts/build_hamiltonian.py`で再生成します。

## 非定常動画とKEEP {#nonsteady-movie-and-keep-exhibits}

[動画ギャラリー](movies.md)は、実際に保存した計算状態と物理時刻を、固定した色範囲とMP4出力で示します。[KEEP](keep.md)は、厳密解のある滑らかな渦で評価し、空間・時間細分化とエントロピー診断を分けています。この滑らかな流れの計算から、衝撃波捕獲の性質は主張しません。

## 勾配制限と発展的な再構成 {#slope-limiters-and-advanced-reconstruction}

[勾配制限ノート](#/limiters)はPythonで計算した45曲線と、滑らかな解の収束6例、Euler再構成の構成的な失敗3例を読み込みます。minmod、Superbee、MC、van Leer、切り詰めたvan Albadaを選び、スカラー周期問題の全変動と質量、同じHLLC流束によるSodを比較します。スカラー誤差は厳密セル平均を使い、Sodでは点値の規約を維持します。1次法と勾配無制限の比較例はスカラー移流だけに適用します。

発展操作ではTVBのM=0、10、50を選び、保存的な正値状態スケーリングを示します。[勾配の定義](limiters.md)と[追加の仮定](advanced-limiters.md)を参照してください。`python scripts/build_limiters.py`がソースハッシュ付きの`docs/figures/limiters.json`を作り、標準の同期処理がWeb版へコピーします。スカラーTVBの例や正値再構成の補助関数だけでは、完全離散Euler法の正値性は保証されません。

## Runge–Kutta法の系譜 {#rungekutta-family-notebook}

[RK法ノート](#/runge-kutta)では固定刻みの陽的RK公式9種を比較します。3つのRK2法は線形安定性多項式を共有しますが、非線形y′=−y²では異なります。1ステップの幅を選び、実際の右辺評価に使う段階予測値を見て、標本化した安定領域と終了時刻の収束を比較します。形式次数、段数、非線形SSP係数、右辺評価回数を分けて表示します。[RKの章](runge-kutta.md)で定義と条件付きSSPの仮定を説明します。`python scripts/build_runge_kutta.py`が図示データとソース記録を作ります。振動子ノートには時間積分法が12種あり、陰的手法はスカラー線形モデルに限ります。

## CIPによる値と勾配の輸送 {#cip-value-and-gradient-transport}

[CIPノート](#/cip)は、一様周期格子のスカラー移流で、原型の3次Hermite CIPと線形の点補間を比較します。独立に輸送する勾配、初期勾配の選択、滑らかな解の収束、矩形パルスのオーバーシュート、解析的な保存性の反例を示します。[定義](cip.md)を参照してください。点値と有限体積平均は交換できません。同期前に`python scripts/build_cip.py`で再生成します。

**A安定性・L安定性とL1／L2／L∞誤差ノルム**は、[精度と安定性の共通ガイド](accuracy-stability.md)を参照してください。
