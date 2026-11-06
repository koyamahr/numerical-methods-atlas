# 実装ロードマップ

## 現在の最優先：衝撃波手法 {#current-priority-shock-methods}

相対論・新分野より、衝撃波手法の拡充を優先します。最初の公開段階として[制限付き放物線FV・特性変数・WENO-Z・AUSM基準例](reconstruction.md)、[数値反例を含むRoeのProperty U](advanced.md#roes-property-u)、[管理した平面odd–even診断](carbuncle.md)を追加しました。原型PPMの波の追跡・接触面強調・衝撃波平坦化、AUSM+／AUSM+-up、鈍頭物体カーバンクル、回転ハイブリッドが、この優先群の次の段階です。範囲を限定した実験だけで全体を完了扱いにはしません。

## 初版：実行可能な基礎 {#first-edition-executable-foundations}

v0.1.0は教育用Pythonライブラリ、歴史アトラス、英語解説、文献カタログ、比較図、自動数値検査をまとめています。リポジトリが初版配布物で、[README](../README.md)のガイドが資料をつなぎます。

NASA問題集には計算済みの15°楔の基準例と未実装候補が含まれます。回転ソルバーノートは今後の計画であり、カタログへの収録だけでは実装済みを意味しません。

## 次の検証 {#next-verification-work}

- 計算記録と保存配列を強く結び、格子・時間細分化と実行時間を併記します。
- 有限体積セル平均の初期化・積分参照、特性WENO、正値制限、強い衝撃波テストを加えます。
- 浅水・等温厳密参照を追加し、地形、静水平衡保存、乾燥床を別段階で扱います。
- 新しいHLLD標準テストを、UCT-HLLD・強磁場問題・外部参照コード比較へ広げます。
- 非線形Fourierとエイリアシング除去、制限付きEuler DG、多次元残差分配を調べます。
- 低Mach PDE前処理と2次元Euler回転ハイブリッドを実装し、エントロピー修正、正値性、カーバンクルを別々に確認します。
- 楕円解法を変係数、異方性、線緩和、FAS、AMG、2次元混合境界へ拡張します。

## NASA問題の推奨順序 {#suggested-order-for-nasa-cases}

楔・膨張で2次元Euler流束と壁境界を検証し、キャビティ・Blasiusで粘性・圧力・境界を整え、円柱で非定常精度を調べます。RANSでは平板・バンプでモデル実装を確認してから、翼型、ステップ、ディフューザー、ハンプへ進みます。依存関係と難しさに沿う順序で、出版年順の歴史を補います。

## 衝撃波ギャラリー：NASA楔と前向きステップ {#shock-gallery-nasa-wedges-and-a-forward-facing-step}

NASAの15°楔、Mach 2.0／2.5を、独立した物体適合1次HLL・SSPRK2有限体積法で計算し、2格子と斜め衝撃波の参照を追加しました。古典的Mach 3前向きステップは240 × 80の障害物セル格子でt=4まで計算し、81保存状態とMP4を追加して動画は合計5本になりました。ステップ角は通常の反射境界で、元のPPM比較のエントロピー・エンタルピー再設定は使いません。教育用の非粘性基準例であり、Wind-US出力や粘性実験の妥当性確認ではありません。[設定と限界](nasa-2d.md)を参照してください。Mach 5衝撃波・境界層干渉、Mach 7粘性ランプ、既存の遷音速ディフューザー・翼型は実装候補です。

## Web版 {#web-edition}

[Web版](https://koyamahr.github.io/numerical-methods-atlas/)は、初版を歴史アトラス、解説、計算図、文献検索に整理します。各展示が文献・方程式・実行・図・検証範囲をつなぎます。

ホームのSod比較はPython計算済みMUSCL密度4曲線を切り替えます。図と初期ギャラリー検証記録も完全なソース版とともに公開します。今後も、検証した教育例、原論文図の再現、試作、文献のみ、計画を区別します。

## 第1拡張：インタラクティブ数値ノート {#first-expansion-interactive-numerical-notebooks}

安定性実験室はブラウザーで周期FTCS・風上・古典LF・LWを計算し、両速度方向、Fourier増幅、点値誤差、データ保存を提供します。Python24参照ケースと数値カーネルを比較しています。

収束ノートは既存DG・Eulerエントロピー波の測定値、実測傾き、スカラー未知数を調べられます。新しい実行時間順位や一般的非線形安定性は主張しません。[実験ガイド](experiments.md)に定義と来歴があります。

## 第2拡張：幾何、時間、多次元衝撃波 {#second-expansion-geometry-time-and-multidimensional-shocks}

スカラーODE積分器7種と時間ノート、格子接続3例とエクスプローラー、1次元SPH再構成、1次元ALE幾何保存、円筒勾配・Newton応力・応力発散の解析検証を追加しました。[座標・粘性の章](coordinates-viscosity.md)は物理成分と座標基底を区別します。

[二重Mach反射](double-mach.md)は1次HLL・SSPRK2でMach10干渉を実際に計算します。高次再構成、完全格子収束、細い壁面ジェットは今後で、NASA楔の基準例は後に追加しましたが、カタログの粘性・乱流問題は未実装です。[平面診断を超える鈍頭物体カーバンクル比較](carbuncle.md)、完全SPH、非構造流束、完全ALE Eulerも今後です。[Roe追悼](roe-memorial.md)は大学の公式記録に基づきます。

## 第3拡張：Hamilton写像と粒子重力 {#third-expansion-hamiltonian-maps-and-particle-gravity}

調和・4次振動子の固定刻み正準写像とノート、周期3次元CIC／FFT PM、単極・全2次モーメントの孤立軟化八分木、孤立倍格子畳み込み、標本・連続スラブGreen変換を追加しました。図には専用ソース記録があります。P³M補正、結合TreePM、FMM移動、宇宙膨張、せん断周期再配置、重力結合SPH流体積分は今後の課題です。

## 第4拡張：非定常動画と滑らかなKEEP {#fourth-expansion-nonsteady-movies-and-smooth-keep}

計算刻みを変えない保存状態、フレーム検査・MP4付き4動画、原型2次直交KEEPと滑らかな渦の収束を追加しました。定常場は静止図です。KEEPは衝撃波安定化、後のPEP・再定義、高次曲線形、3次元TGV／LESを含みません。

## 第5拡張：勾配制限、RK族、CIP {#fifth-expansion-limiters-rk-families-and-cip}

MUSCL勾配の選択、TVB修正minmodと正値再構成、非線形段階検証付き9陽的RK係数表、12振動子手法、保存性反例付き原型3次Hermite CIPを追加しました。Euler時間更新全体の正値性は別の拡張です。

## 第6拡張：方程式、疎行列、運動論輸送 {#sixth-expansion-equations-sparse-systems-and-kinetic-transport}

Burgers・LWR交通流を含む7系統9ケースの保存分布を追加し、スカラー厳密セル平均、Sod点値、浅水・等温の厳密重ね描きなしを区別します。

[連続P1 FEM](fem.md)、[疎行列・非線形解法](sparse-nonlinear.md)、[硬いODE](stiff-integration.md)、[周期MAC射影](incompressible.md)、[D2Q9–BGK](lattice-boltzmann.md)、[1次双曲型拡散](hyperbolic-diffusion.md)に専用検査・図・ソースハッシュがあります。[Chapman–Enskog展開](chapman-enskog.md)は測定したせん断粘性へつなぐ形式導出です。これらの教育用実装は新しいアトラスで公開済みです。各章に実装範囲と残る検証を示しています。

## 承認済みの次の作業 {#authorized-next-work}

- **追加済み — RoeのProperty U**：原典の4条件、パラメータベクトルの導出、ジャンプ・整合性・固有基底の検査、膨張不連続の反例。[解説](advanced.md#roes-property-u)を参照。
- InutsukaのGSPH：Gaussian畳み込み、比体積再構成、向き付き粒子対リーマン状態、整合保存エネルギー更新を、可変平滑化長の前に滑らか・接触・衝撃波管で検証します。Iwasaki–InutsukaのGSPMHDは後の独立段階です。[出典と計画](gsph.md)。
- 相対論流体：SRHD回復・特性を先に検査し、SRMHD、固定計量GR、独立検証Einstein物質結合へ進みます。放射とSRGSPHは別の分岐です。[2026年11月確認の調査](relativistic-hydrodynamics.md)。
- **第1段階を追加**：制限付き放物線FV、保存特性変数、FD WENO-ZのSod・接触面・Shu–Osher比較。原型PPM全機能は今後です。[範囲](reconstruction.md)を参照。
- 共通音速・3次圧力分割のAUSM基準例を追加。AUSM+・AUSM+-upは独立した予定です。
- **Web実装済み**：HLLD、Brio–Wu、Alfvén波の格子細分化、弱い磁場ループのCT-Contact／GLM比較。[MHDテスト](#/mhd-tests)を参照。
- **予定 — 電磁場のFDTD（時間領域有限差分法）**：Yee格子の変数配置、leapfrogによるMaxwell方程式の更新、CFL制限、数値分散。真空中の波と導体空洞のテストから始め、吸収境界・PMLの反射検査へ進みます。実装と専用の検証は未完了です。
- **予定 — プラズマPIC（Particle-in-Cell法）**：静電的な粒子–Poisson連成から、電磁的な粒子–Maxwell連成へ進みます。粒子形状、格子への割当てと場の補間、Boris法、電荷保存電流割当て、Gauss則の診断を扱います。プラズマ振動、two-stream不安定性、Landau減衰を検証候補とし、エネルギー・ノイズ・格子／時間／粒子数依存性を確認します。既存の重力PM例とは適用範囲を分けます。[WarpXのPIC理論ノート](https://warpx.readthedocs.io/en/25.11/theory/pic.html)を出発点とし、プラズマPICソルバーは現時点では未実装です。
- 硬い積分：BE／BDF2／SDIRK2／IMEX Eulerを超える高次IMEX、埋込みDIRK、可変BDF、演算子分割。
- 疎行列・非線形：固定右GMRES／BiCGSTAB・ILU(0)を超える行列不要Newton–Krylov、頑健な並べ替え・フィル、可変前処理、広い非線形テスト。
- 粘性・非圧縮：周期Taylor–Greenを超える壁射影、SIMPLE／PISO、キャビティ・円柱後流の妥当性確認。
- FEM：速度・圧力混合対、inf–sup、曲線・不規則格子、自然・混合境界組立て。
- LBM：低Mach等温D2Q9–BGKを超えるMRT／TRT／キュムラント、熱的・多相モデル。
- 双曲型拡散：周期1次基準を超える完全2次RD、異方性、移流・粘性の統一系。

著者の要望によりAMRは保留で、今回の拡張に含みません。

## 生物・地球流体の調査追加 {#biological-and-geophysical-survey-additions}

[生物カタログ](biological-models.md)は22系統を文献のみで整理し、方程式、出典規約、検証案を含みます。実装順はロジスティック／SIR・酵素反応からFisher前線、FitzHugh–Nagumo、Schnakenberg、Keller–Segelへ進め、出生・死亡SSAを独立した確率分岐とします。生物ソルバーや生物の妥当性確認は追加していません。

[Arakawa A／B／C](geophysical-grids.md)は配置図と検証済み半離散f平面記号を持ちます。D／E、鉛直配置、非線形渦位、Kelvin／Rossby、海岸は追加課題で、完全な地球流体コアではありません。

## 機械学習に関連する数値計算の改訂候補 {#planned-machine-learning-numerics}

**状態：改訂候補。以下の専用解説・実装・検証はまだ追加していません。** 第1巻の共通基盤につながる安定な関数評価、自動微分、最適化を先に扱い、科学技術機械学習の応用は後続の候補とします。予定項目を実装済み手法数には加えず、公開時期も未定です。

混合精度演算・低精度GPU計算の設計は、今回のスコープから外します。通常の浮動小数点の丸め誤差と、安定な関数評価は共通基礎として扱います。

- [ ] **softmaxとlog-sum-exp**：最大値を引くシフト、log-softmax、指数関数のオーバーフローとアンダーフロー。大きな入力、定数シフトに対する不変性、確率和、微分の整合性を検証候補とします。[SciPyのsoftmax解説](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html)を参照します。
- [ ] **交差エントロピーと安定な損失評価**：確率を経由せずlogitsから計算する方法、log-sum-expとの関係、sigmoidと二値交差エントロピー。極端な入力での有限値と解析的な勾配を確認します。[PyTorchの交差エントロピー解説](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)を出発点とします。
- [ ] **自動微分・逆伝播**：前進／逆モード、連鎖律、Jacobian–vector積（JVP）、vector–Jacobian積（VJP）、Hessian–vector積。記号微分・有限差分との違い、丸め誤差、非微分点、保存する中間値とメモリの関係を扱います。[JAXの自動微分解説](https://docs.jax.dev/en/latest/301/index.html)を参照し、解析微分・方向微分との比較を計画します。
- [ ] **陰関数微分・随伴法と微分可能なソルバー**：線形求解、収束した非線形系、時間発展を通した感度計算。反復を展開して微分する方法と、方程式から微分する方法を区別し、Jacobianの可逆性、求解許容誤差、勾配検査を明記します。[陰関数微分の原論文](https://papers.neurips.cc/paper_files/paper/2022/file/228b9279ecf9bbafe582406850c57115-Paper-Conference.pdf)を調査の入口とします。
- [ ] **機械学習向け最適化**：勾配降下・SGD、momentum、Adam、L-BFGS、Gauss–Newton／Levenberg–Marquardt。既存のNewtonによる方程式求解と目的関数の最小化を区別し、尺度・条件数、学習率、勾配ノルムを比較します。すべての目的関数に対する収束保証や優劣は主張しません。
- [ ] **応用候補 — PINNsと逆問題**：PDE残差、初期・境界条件、観測データの損失を分け、通常の差分・FEMと同じ誤差指標で比較します。学習損失の低下だけをPDE解の精度保証とはしません。[PINNsの著者解説](https://maziarraissi.github.io/PINNs/)と[失敗モードの研究](https://papers.nips.cc/paper_files/paper/2021/hash/df438e5206f31600e6ae4af72f2725f1-Abstract.html)を参照します。
- [ ] **応用候補 — Neural Operator／Fourier Neural Operator**：入力関数から解関数への写像を学習する考え方を、既存のFourier基底・スペクトル法と接続します。学習分布外、格子変更、離散化・aliasing誤差を独立に確認する計画とし、格子を変更できることだけで精度を保証しません。[Neural Operator原論文](https://www.jmlr.org/papers/volume24/21-1524/21-1524.pdf)を参照します。
- [ ] **応用候補 — 記号回帰と方程式発見**：データや学習モデルから明示的な数式を探す方法。微分の自動計算と区別し、ノイズ、次元・対称性、式の複雑さ、別データでの再現性を評価します。[深層学習から記号モデルを抽出する研究](https://proceedings.neurips.cc/paper_files/paper/2020/hash/c9f2f917078bd2db12f23c3b413d9cba-Abstract.html)を調査候補とします。

## 量子化学・DFTの開発予定 {#planned-quantum-chemistry-and-dft}

**状態：予定。実装と専用の文献調査は未着手で、公開時期は未定です。** 電子状態計算を独立した分岐として、次の開発リストに記録します。予定項目を現在の実装済み手法数や方程式数には加えません。

- [ ] **Schrödinger固有値問題**：調和振動子、水素型原子の動径問題などの1電子モデルから開始。有限差分・有限要素・スペクトル離散化を比較し、境界・領域打切り・解像度の誤差を分けて記録します。
- [ ] **電子状態計算の基底**：原子軌道、Gaussian・Slater関数、平面波、実空間格子。重なり行列と一般化固有値問題を含めます。既存の[要素基底ノート](basis-functions.md)と接続し、メッシュ内の多項式基底と分子軌道用の基底集合を区別します。
- [ ] **Coulomb・Hartreeポテンシャル**：電子の電荷密度とPoisson解法を接続。静電単位系、電荷の符号、孤立・周期境界、ゼロモード、自己相互作用の規約を明記し、重力の符号や規格化をそのまま流用しません。
- [ ] **Hartree–Fock**：小さな閉殻分子を対象に、行列組立て・一般化固有値解法・自己無撞着場（SCF）反復を実装。必要な積分計算を検証してからエネルギーを提示します。
- [ ] **Kohn–Sham密度汎関数法（DFT）**：密度・有効ポテンシャル・交換相関近似を解説。使用するLDAモデルを明示して開始し、GGA以降は個別に検証します。
- [ ] **SCF反復と混合**：減衰、密度・ポテンシャル混合、Pulay／DIIS加速を比較。電子数、固有値問題とSCFの残差、エネルギー変化、未収束を報告します。
- [ ] **検証例**：1電子の参照解、小さな原子・分子を使い、基底・格子の細分化と独立した参照コードで確認。離散化誤差、SCF許容誤差、物理モデルの差を分けます。

最初の到達点は、検証済みの1電子固有値ソルバー、最小基底のHartree–Fock例、適用範囲を明示したKohn–Sham DFT例の順です。周期物質、擬ポテンシャル、スピン依存の拡張、post-Hartree–Fock相関は後続の独立課題とし、初期実装の完成範囲には含めません。この予定の追加で上記の流体計算法の優先順位は変えず、AMRも引き続き保留します。

今後の編集は、同じ方程式を複数の検証済み離散化、コスト・誤差、明示した失敗へ結び付けることを優先し、調査・試作・検証済みモデルの表示を維持します。


## 検証付きEuler・MHD比較 {#verified-euler-and-mhd-comparisons}

2次元基本変数MUSCLのminmod／MC、厳密セル平均の滑らかな解の細分化、NASA楔の2格子での1次・2次再構成比較、前向きステップの3再構成動画を追加しました。[比較ページ](#/flow-comparison)ではHLL／SSPRK2を固定し、診断値を表示します。完全な3成分のHLLD、Brio–Wu、4格子の円偏波Alfvén波、2格子の弱い磁場ループでのHLLE／HLLD × CT-Contact／GLMを追加しました。[MHDページ](#/mhd-tests)にはソース・成果物ハッシュ、保存変数配列、正値性・再試行・切替診断と日英の適用範囲があります。合意したWebの3段階を完了し、書籍は後回しです。
