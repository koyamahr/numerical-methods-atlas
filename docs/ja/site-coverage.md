# 収録範囲と数え方

公開Web版、集計日2026-11-06。数えるのはカタログ項目と記載した実験例です。すべての項目が検証済みの完全なソルバーであるという意味ではありません。

**方程式・モデル42項目・計算法と構成要素90項目・学術誌／会議論文136件・全参考資料158件。**

保存済み計算を用いる方程式ギャラリーは7系統・9例、読書章はこの一覧を含め44章です。

## 方程式とモデル {#equations-and-models}

名前付きの方程式・モデルを数えます。スカラー成分や数学的に互いに独立な系統の数ではありません。枠組みや補助定式化を含み、通常は派生形を一つにまとめます。ただし個別に説明するSR／GRの流体系3種類は分けます。生物モデルは専用カタログから一度だけ取り込みます。

ローカル実験のある項目は15、文献解説のみは27で、後者には生物調査22項目すべてを含みます。連成系は一項目とし、成分方程式では増やしません。Poisson／Laplaceや次元の違いもまとめます。枠組みと個別反応則が並ぶため、数学的に独立した系統数ではありません。

一覧の詳細な範囲注記は原文（英語）を保持します。各章の日本語本文も併せて参照できます。

## 方程式・モデルの一覧 {#equationmodel-inventory}

### 物理・数学モデル {#physics-amp-mathematical-models}

- [線形移流（Linear advection）](stability.md) — ローカル実験あり。
- [熱・拡散（Heat / diffusion）](elliptic.md) — ローカル実験あり。
- [Poisson／Laplace方程式（Poisson / Laplace）](elliptic.md) — ローカル実験あり。
- [非粘性Burgers方程式（Inviscid Burgers）](equation-gallery.md) — ローカル実験あり。
- [LWR交通流（LWR traffic flow）](equation-gallery.md) — ローカル実験あり。
- [圧縮性Euler方程式（Compressible Euler）](benchmarks.md) — ローカル実験あり。
- [浅水方程式（線形回転モデルを含む）（Shallow water, including the rotating linear model）](geophysical-grids.md) — ローカル実験あり。 <span lang="en" data-original>Wet 1D flow and linear rotating Fourier symbols; no full geophysical dynamical core.</span>
- [等温Euler方程式（Isothermal Euler）](benchmarks.md) — ローカル実験あり。
- [理想MHD（Ideal MHD）](mhd.md) — ローカル実験あり。
- [非圧縮Navier–Stokes方程式（Incompressible Navier–Stokes）](incompressible.md) — ローカル実験あり。
- [等温格子BGK（Isothermal lattice BGK）](lattice-boltzmann.md) — ローカル実験あり。
- [Hamilton振動子（Hamiltonian oscillators）](symplectic.md) — ローカル実験あり。
- [重力粒子モデル（Gravitational particle model）](particle-gravity.md) — ローカル実験あり。 <span lang="en" data-original>Static force evaluations and boundary kernels; no coupled self-gravitating fluid evolution.</span>
- [Bratu非線形境界値問題（Bratu nonlinear boundary-value problem）](sparse-nonlinear.md) — ローカル実験あり。
- [補助変数による双曲型拡散系（Auxiliary hyperbolic diffusion system）](hyperbolic-diffusion.md) — ローカル実験あり。 <span lang="en" data-original>Periodic first-order steady-solution baseline, not physical-time heat diffusion.</span>

### 相対論モデル {#relativistic-models}

- [特殊相対論的流体力学（Special-relativistic hydrodynamics）](relativistic-hydrodynamics.md) — 文献解説のみ。 <span lang="en" data-original>Literature review; no local relativistic solver.</span>
- [一般相対論的流体力学（General-relativistic hydrodynamics）](relativistic-hydrodynamics.md) — 文献解説のみ。 <span lang="en" data-original>Literature review; no local relativistic solver.</span>
- [一般相対論的MHD（General-relativistic MHD）](relativistic-hydrodynamics.md) — 文献解説のみ。 <span lang="en" data-original>Literature review; no local relativistic solver.</span>
- [相対論的放射モーメント／M1（Relativistic radiation moments / M1）](relativistic-hydrodynamics.md) — 文献解説のみ。 <span lang="en" data-original>Literature review; no local relativistic solver.</span>
- [因果的な相対論的粘性流体（Causal relativistic viscous fluid）](relativistic-hydrodynamics.md) — 文献解説のみ。 <span lang="en" data-original>Literature review; no local relativistic solver.</span>

### 生物モデル調査 {#biological-model-survey}

- [ロジスティック個体群増殖（Logistic population growth）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The linked original is the later 1847 memoir; the 1838 note itself was not audited. The differential equation is not the discrete logistic map.</span>
- [Michaelis–Mentenと完全酵素反応系（Michaelis–Menten and full enzyme kinetics）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The 1913 rapid-equilibrium interpretation and the 1925 quasi-steady-state derivation must remain distinct.</span>
- [Lotka–Volterra捕食・被食（Lotka–Volterra predator–prey）](biological-models.md) — 文献解説のみ。
- [McKendrick年齢構造個体群（McKendrick age-structured population）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>This is the classical age-transport form; the later von Foerster lineage is acknowledged without treating its date as the first appearance.</span>
- [SIR・SEIR区画モデル（SIR and SEIR compartment models）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The original general epidemic framework is broader than this SIR specialization. Population-count and fraction conventions give different β definitions.</span>
- [Fisher–KPP侵入前線（Fisher–KPP invasion front）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>Fisher–KPP is a conventional family name; the independent KPP 1937 original remains an archival follow-up. The exact special speed is not the minimal speed.</span>
- [Monod増殖とケモスタット（Monod growth and chemostat）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>This writes one constant-yield extension of saturation growth, not a universal metabolic model.</span>
- [Hodgkin–Huxley膜動態（Hodgkin–Huxley membrane dynamics）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The original squid-axon model is not a calibrated human cardiac model. No single rate parameter set is selected by this survey.</span>
- [Turing反応拡散の枠組み（Turing reaction–diffusion framework）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>A spot image or unequal diffusion coefficients alone do not establish a Turing mechanism. Boundary conditions determine the available modes.</span>
- [FitzHugh–Nagumoの興奮と回復（FitzHugh–Nagumo excitation and recovery）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>This is a common normalized variant; cubic coefficients, recovery signs and nondimensionalization differ between formulations.</span>
- [Keller–Segel走化性（Keller–Segel chemotaxis）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>This is a common two-field reduction of a more detailed original formulation. Blowup thresholds depend on dimension, domain, boundary and chemical dynamics.</span>
- [Gierer–Meinhardt活性化・抑制（Gierer–Meinhardt activator–inhibitor）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>Source densities, saturation and baseline production vary across the model family. This simplified formula is not a verbatim transcription of every original variant.</span>
- [流体・弾性構造と埋め込み境界（Fluid–elastic structure and immersed boundaries）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>Immersed boundary is a numerical coupling method, not itself a closed biological constitutive equation. The existing periodic MAC solver does not implement this coupling.</span>
- [化学マスター方程式とGillespie SSA（Chemical master equation and Gillespie SSA）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The 1977 paper is a foundational SSA reference, not a priority claim for all master equations. SSA is a solver; the reaction network is the model. A seed documents a trajectory, not an ensemble validation.</span>
- [Mackey–Glass遅延生理フィードバック（Mackey–Glass delayed physiological feedback）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>A scalar initial value alone is insufficient. The delayed ODE is distinct from a spatial reaction–diffusion model.</span>
- [レプリケータ進化ゲーム動態（Replicator evolutionary game dynamics）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>No universal Lyapunov function or equivalence of fixed point and evolutionarily stable strategy is assumed.</span>
- [Schnakenberg反応拡散（Schnakenberg reaction–diffusion）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>A mathematical chemical pattern model; matching a visual biological pattern does not calibrate it to a tissue.</span>
- [Shigesada–Kawasaki–Teramoto交差拡散（Shigesada–Kawasaki–Teramoto cross-diffusion）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The displayed homogeneous-environment reduction omits the original environmental-potential terms. It is not equivalent to two independent scalar diffusion equations.</span>
- [Gray–Scott空間自己触媒反応（Gray–Scott spatial autocatalysis）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>1983 is the well-mixed CSTR source; Pearson 1993 is the spatial pattern reference. Spot division does not by itself demonstrate cell division or a linear Turing instability.</span>
- [Aliev–Panfilov心筋興奮（Aliev–Panfilov cardiac excitation）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>Monodomain/bidomain tissue models add conductivity tensors and, for bidomain, an extracellular elliptic constraint. They are not automatically included by this two-variable model.</span>
- [Repressilator mRNA・タンパク質回路（Repressilator mRNA–protein network）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>The six-variable form is distinct from a reduced three-protein oscillator; oscillations are parameter-dependent.</span>
- [遺伝子トグルスイッチ（Genetic toggle switch）](biological-models.md) — 文献解説のみ。 <span lang="en" data-original>Bistability is not guaranteed for arbitrary Hill exponents or production rates. Induction, mRNA dynamics and noise are additional model choices.</span>

## 計算法の一覧 {#numerical-method-inventory}

名前付きの離散化法、積分法、線形・非線形解法、連成演算子を数えます。パラメータの違いでは増やしません。

ローカル実験のある項目は84、文献解説のみは6です。再構成の制限関数、前処理、連成演算子は構成要素であり、完全なPDEソルバーではありません。格子配置、CFL条件、定理は計算法の数に含めません。

### 空間離散化 {#spatial-discretization}

- [空間前進差分（Forward spatial difference）](stability.md) — ローカル実験あり。
- [空間後退差分（Backward spatial difference）](stability.md) — ローカル実験あり。
- [空間中心差分（Centered spatial difference）](stability.md) — ローカル実験あり。
- [風上差分（upwind）（Upwind finite differences）](stability.md) — ローカル実験あり。
- [Lax–Friedrichs法（Lax–Friedrichs）](stability.md) — ローカル実験あり。
- [Lax–Wendroff法（Lax–Wendroff）](stability.md) — ローカル実験あり。
- [Godunov型有限体積法（Godunov-type finite volumes）](benchmarks.md) — ローカル実験あり。
- [MUSCL再構成（MUSCL reconstruction）](benchmarks.md) — ローカル実験あり。
- [WENO5-JS（WENO5-JS）](benchmarks.md) — ローカル実験あり。
- [不連続Galerkin法／Legendre（Discontinuous Galerkin / Legendre）](benchmarks.md) — ローカル実験あり。
- [Fourier微分と時間発展（Fourier differentiation and evolution）](benchmarks.md) — ローカル実験あり。
- [3次Hermite CIP（Cubic-Hermite CIP）](cip.md) — ローカル実験あり。
- [連続P1 Galerkin有限要素法（Continuous P1 Galerkin FEM）](fem.md) — ローカル実験あり。
- [制限付きPPM再構成（Limited PPM reconstruction）](reconstruction.md) — ローカル実験あり。 <span lang="en" data-original>Method-of-lines parabolic FV only; no original wave tracing, contact steepening, flattening or remap.</span>
- [Eulerの特性変数再構成（Euler characteristic reconstruction）](reconstruction.md) — ローカル実験あり。 <span lang="en" data-original>Local conservative FV basis or face-frozen Roe FD basis; controlled component/characteristic comparisons.</span>
- [有限差分WENO5-Z（FD WENO5-Z）](reconstruction.md) — ローカル実験あり。 <span lang="en" data-original>Global LF splitting, exponent 2, fixed epsilon 1e-6; point values, not FV state interpolation.</span>

### リーマン流束と修正 {#riemann-fluxes-amp-corrections}

- [Rusanov／局所Lax–Friedrichs流束（Rusanov / local Lax–Friedrichs flux）](benchmarks.md) — ローカル実験あり。
- [HLL（HLL）](benchmarks.md) — ローカル実験あり。
- [HLLC（HLLC）](benchmarks.md) — ローカル実験あり。
- [Roe法（Roe）](benchmarks.md) — ローカル実験あり。
- [HLLE／Einfeldt波速（HLLE / Einfeldt wave speeds）](benchmarks.md) — ローカル実験あり。
- [Roe音響波のエントロピー修正（Acoustic Roe entropy correction）](advanced.md) — ローカル実験あり。
- [回転ハイブリッド・リーマンソルバー（Rotated-hybrid Riemann solver）](advanced.md) — 文献解説のみ。
- [HLLDのMHDリーマン解法（HLLD MHD Riemann solver）](mhd.md) — ローカル実験あり。 <span lang="en" data-original>Full-vector adiabatic HLLD/HLLE with Brio-Wu, circular Alfven refinement and weak field-loop tests. CT-Contact and GLM, not UCT-HLLD.</span>
- [AUSM系列の流束分割（AUSM-family flux splitting）](reconstruction.md) — ローカル実験あり。 <span lang="en" data-original>Common arithmetic sound speed and cubic pressure baseline, with 1D/2D tests. AUSM+ and AUSM+-up remain planned.</span>

### 勾配制限と許容状態 {#limiters-amp-admissibility}

- [Minmod（Minmod）](limiters.md) — ローカル実験あり。
- [Superbee（Superbee）](limiters.md) — ローカル実験あり。
- [単調中心勾配制限／MC（Monotonized central / MC）](limiters.md) — ローカル実験あり。
- [Van Leer勾配制限（Van Leer limiter）](limiters.md) — ローカル実験あり。
- [切り詰めたVan Albada勾配制限（Clipped Van Albada limiter）](limiters.md) — ローカル実験あり。
- [TVB修正minmod（TVB modified minmod）](advanced-limiters.md) — ローカル実験あり。
- [平均を保つ正値状態スケーリング（Mean-preserving positive-state scaling）](advanced-limiters.md) — ローカル実験あり。 <span lang="en" data-original>Reconstruction building block; no full Euler-update positivity guarantee.</span>

### 時間積分 {#time-integration}

- [前進Euler法（Forward Euler）](time-integration.md) — ローカル実験あり。
- [後退Euler法（Backward Euler）](time-integration.md) — ローカル実験あり。
- [Heun法／SSPRK(2,2)（Heun / SSPRK(2,2)）](time-integration.md) — ローカル実験あり。
- [陽的中点RK2（Explicit midpoint RK2）](time-integration.md) — ローカル実験あり。
- [Ralston RK2（Ralston RK2）](time-integration.md) — ローカル実験あり。
- [Kutta RK3（Kutta RK3）](time-integration.md) — ローカル実験あり。
- [SSPRK(3,3)（SSPRK(3,3)）](time-integration.md) — ローカル実験あり。
- [SSPRK(4,3)（SSPRK(4,3)）](time-integration.md) — ローカル実験あり。
- [古典的RK4（Classical RK4）](time-integration.md) — ローカル実験あり。
- [SSPRK(5,4)（SSPRK(5,4)）](time-integration.md) — ローカル実験あり。
- [陰的中点則（Implicit midpoint）](time-integration.md) — ローカル実験あり。
- [2ステップleapfrog法（Two-step leapfrog）](time-integration.md) — ローカル実験あり。
- [Crank–Nicolson法（Crank–Nicolson）](elliptic.md) — ローカル実験あり。
- [BDF2（BDF2）](stiff-integration.md) — ローカル実験あり。
- [L安定なSDIRK2（L-stable SDIRK2）](stiff-integration.md) — ローカル実験あり。
- [IMEX Euler（IMEX Euler）](stiff-integration.md) — ローカル実験あり。
- [適応SDIRK2／ステップ倍分割（Adaptive SDIRK2 / step doubling）](stiff-integration.md) — ローカル実験あり。
- [シンプレクティックEuler法（Symplectic Euler）](symplectic.md) — ローカル実験あり。
- [速度Verlet／粒子leapfrog法（Velocity Verlet / particle leapfrog）](symplectic.md) — ローカル実験あり。
- [吉田の4次合成法（Yoshida fourth-order composition）](symplectic.md) — ローカル実験あり。

### 線形・非線形ソルバー {#linear-amp-nonlinear-solvers}

- [Thomas法／三重対角消去（Thomas tridiagonal elimination）](elliptic.md) — ローカル実験あり。
- [Jacobi反復（Jacobi iteration）](elliptic.md) — ローカル実験あり。
- [Gauss–Seidel反復（Gauss–Seidel iteration）](elliptic.md) — ローカル実験あり。
- [逐次過緩和法／SOR（Successive over-relaxation / SOR）](elliptic.md) — ローカル実験あり。
- [共役勾配法（Conjugate gradients）](elliptic.md) — ローカル実験あり。
- [赤黒Gauss–Seidel法（Red-black Gauss–Seidel）](elliptic.md) — ローカル実験あり。
- [幾何マルチグリッドVサイクル（Geometric multigrid V-cycle）](elliptic.md) — ローカル実験あり。
- [再始動GMRES（Restarted GMRES）](sparse-nonlinear.md) — ローカル実験あり。
- [BiCGSTAB（BiCGSTAB）](sparse-nonlinear.md) — ローカル実験あり。
- [Jacobi／対角前処理（Jacobi / diagonal preconditioning）](sparse-nonlinear.md) — ローカル実験あり。
- [ピボット選択なしILU(0)（Unpivoted ILU(0)）](sparse-nonlinear.md) — ローカル実験あり。
- [Armijo減衰Newton法（Armijo-damped Newton）](sparse-nonlinear.md) — ローカル実験あり。
- [組み立てたJacobianによるNewton–Krylov法（Newton–Krylov with assembled Jacobian）](sparse-nonlinear.md) — ローカル実験あり。

### 結合・制約・粒子 {#coupling-constraints-amp-particles}

- [二重時間積分（Dual time stepping）](advanced.md) — ローカル実験あり。
- [スカラー残差分配法（Scalar residual distribution）](advanced.md) — ローカル実験あり。 <span lang="en" data-original>1D P1 upwind equivalent, not multidimensional Euler RD.</span>
- [低Mach数のPDE前処理（Low-Mach PDE preconditioning）](advanced.md) — 文献解説のみ。
- [制約輸送法／CT（Constrained transport / CT）](mhd.md) — ローカル実験あり。 <span lang="en" data-original>Original arithmetic flux-CT OT baseline plus contact-upwinded CT loop tests. Native face divergence; not UCT-HLLD.</span>
- [GLM発散クリーニング（GLM divergence cleaning）](mhd.md) — ローカル実験あり。 <span lang="en" data-original>Original Rusanov OT baseline plus HLLD/HLLE loop tests with an exact longitudinal cleaning solve and split damping. Native cell-centered divergence.</span>
- [MAC圧力射影法（MAC pressure projection）](incompressible.md) — ローカル実験あり。
- [D2Q9–BGK衝突・並進（D2Q9–BGK collision and streaming）](lattice-boltzmann.md) — ローカル実験あり。
- [Guo外力（Guo forcing）](lattice-boltzmann.md) — ローカル実験あり。
- [中間壁バウンスバック（Half-way bounce-back）](lattice-boltzmann.md) — ローカル実験あり。
- [1次の双曲型拡散ベースライン（First-order hyperbolic diffusion baseline）](hyperbolic-diffusion.md) — ローカル実験あり。
- [SPHカーネル再構成（SPH kernel reconstruction）](particles-sph.md) — ローカル実験あり。
- [ALE一様状態・幾何保存モデル（ALE uniform-state / geometric-conservation model）](ale.md) — ローカル実験あり。 <span lang="en" data-original>Moving-volume scalar check; no complete ALE Euler solver.</span>
- [Godunov SPH／GSPH（Godunov SPH / GSPH）](gsph.md) — 文献解説のみ。

### 粒子場と重力 {#particle-fields-amp-gravity}

- [Cloud-in-cellの割当てと補間（Cloud-in-cell assignment and interpolation）](particle-gravity.md) — ローカル実験あり。
- [FFT粒子格子力（FFT particle–mesh forces）](particle-gravity.md) — ローカル実験あり。
- [Barnes–Hut八分木（Barnes–Hut octree）](particle-gravity.md) — ローカル実験あり。
- [単極と2次モーメント展開（Monopole and second-moment expansion）](particle-gravity.md) — ローカル実験あり。
- [孤立境界の倍格子FFT畳み込み（Isolated doubled-grid FFT convolution）](gravity-boundaries.md) — ローカル実験あり。
- [水平周期スラブGreen関数FFT（Horizontal-periodic slab Green-function FFT）](gravity-boundaries.md) — ローカル実験あり。
- [P³M短距離補正（P³M short-range correction）](particle-gravity.md) — 文献解説のみ。
- [TreePM力分割（TreePM force splitting）](particle-gravity.md) — 文献解説のみ。
- [高速多重極法の移動演算（Fast multipole translations）](particle-gravity.md) — 文献解説のみ。

### 追加の定式化 {#additional-formulations}

- [直交座標の原KEEP分割流束（Original Cartesian KEEP split flux）](keep.md) — ローカル実験あり。

### 要素基底・関数近似 {#element-bases-amp-approximation}

- [Legendreモード基底・正規直交化（Legendre modal basis / orthonormal scaling）](basis-functions.md) — ローカル実験あり。 <span lang="en" data-original>Reference-element tabulation, derivatives, projection and affine mass/stiffness matrices.</span>
- [Lagrange節点基底・GLL選点法（Lagrange nodal basis / GLL collocation）](basis-functions.md) — ローカル実験あり。 <span lang="en" data-original>Interval cardinal functions, modal transforms, exact versus quadrature mass, and P1/P2 triangle shapes.</span>

## 論文数と全資料数の区別 {#papers-versus-all-sources}

論文数は学術誌論文と会議論文です。総説、翻訳、採録済みであることを明記した論文も含みます。全参考資料は、それに書籍、章、技術資料、文書、個別に識別したプレプリント等を加えた、重複を除く出版物の数です。

- 133件：学術誌論文（総説・翻訳・採録済み論文を含む）
- 3件：会議論文
- 7件：書籍
- 2件：書籍の章
- 3件：技術・教育レポート
- 10件：その他の資料・文書・プレプリント

Cockburn–Shu 1989の重複書誌を統合し、Burgers 1948を書籍の章に分類しました。以前の146レコードには重複があり、その後の出典追加も現在の重複を除く総数に反映しています。原著と別途出版された翻訳は異なる出版物です。すべての全文を確認済みとは主張せず、確認状態を各出典注記に残します。

## 再現方法 {#reproduction}

名前付き登録簿は`catalog/coverage.json`です。生物項目と出版物の種別は各専用カタログを参照します。`python scripts/build_coverage.py`が出版物の同一性とローカル章リンクを検査し、数と一覧を生成します。Webビルドもこの検査を実行します。パラメータ、保存フレーム、本文での方程式の繰り返し、テスト関数の数では増やしません。翻訳ファイルも章の総数を増やしません。

[集計一覧と出典ハッシュをダウンロード](figures/site-coverage.json)。[参考文献](references.md)、[方程式ギャラリー](equation-gallery.md)、[生物モデル](biological-models.md)、[実装ロードマップ](roadmap.md)も参照できます。
