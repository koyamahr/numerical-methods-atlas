# 生物モデル方程式と数値検証

個体群の増殖から確率的な遺伝子制御、流体構造連成まで、22の生物・生物由来モデルを選び、保存則CFDの外へ方程式の地図を広げます。**22項目すべてが文献調査とベンチマーク設計案です。この追加では生物ソルバーを実装しておらず、生物系のシミュレーション結果も示していません。**

以下は慣用的な簡略形・規格化形です。出典はモデルの系譜を示し、すべての係数や変数が原論文と一致するという意味ではありません。[構造化カタログ](figures/biological-models.json)に、各項目の引用、数値的な課題、検証目標、範囲を記録しています。現代数理生物学の網羅的総説ではなく、数値計算の多様性を重視した選定です。出典確認日は2026年11月6日です。

## 生物の問いと数値計算法の対応 {#which-biological-questions-exercise-which-algorithms}

- **個体群・生態：** ロジスティック増殖、捕食被食、Fisher前線、交差拡散、レプリケータ動力学は、正値性、不変集合、長時間挙動、空間侵入を調べます。
- **人口構造・感染症：** 年齢輸送と区画モデルは、更新境界、収支、区画の非負性、閾値を調べます。
- **生化学・代謝：** 酵素反応とMonod増殖は、硬いODE、保存則、縮約モデルを結びます。
- **形態形成：** Turing解析、Gierer–Meinhardt、Schnakenberg、Gray–Scottでは、物理的な不安定性と数値的な模様選択を分けます。
- **興奮：** Hodgkin–Huxley、FitzHugh–Nagumo、Aliev–Panfilovでは、硬い反応とパルス伝導、不応期、らせん波を結びます。
- **遺伝子制御・雑音：** 遅延フィードバック、トグル、リプレシレーター、化学マスター方程式には、履歴補間、分岐解析、ジャンプ過程のシミュレーションなどが必要です。
- **生体力学：** 流体と弾性構造には、流体方程式に加えて構成力と連成離散化が必要です。

既存の[拡散・楕円型解法](elliptic.md)、[有限要素法](fem.md)、[疎行列・Newton法](sparse-nonlinear.md)、[硬い系の時間積分](stiff-integration.md)、[非圧縮投影法](incompressible.md)は、その部品になります。既存のテストが、ここで追加した生物系を検証しているわけではありません。

## 歴史順のモデルカタログ {#historical-model-catalog}

年は初期の出典または選んだ発展を指し、排他的な先取権の主張ではありません。後年の空間拡張、縮約、翻訳は各項目で区別します。

### 01 · 1838 · ロジスティック個体群増殖（Logistic population growth） {#01-1838-logistic-population-growth}

**個体群・生態・文献調査のみ。** 環境収容力Kによる密度制限付き増殖です。生物系ODEの最も基本的な比較問題になります。

\[
\dot N=rN(1-N/K).
\]

**数値的な課題。** 正値性、平衡点、Kを越えるオーバーシュートを調べます。滑らかに見える曲線でも不変区間を破る場合があります。

**検証案。** N0>0でN(t)=K/[1+(K/N0−1)exp(−rt)]と比較し、時間精度と0、K付近の振る舞いを測ります。

**モデルの規約。** リンク先は後年の1847年の論文です。1838年の短報自体は未確認です。この微分方程式は離散ロジスティック写像とは異なります。

出典：[Verhulst, Pierre-François (1847)](https://doi.org/10.3406/marb.1847.3457)。

### 02 · 1913 · Michaelis–Mentenと完全酵素反応系（Michaelis–Menten and full enzyme kinetics） {#02-1913-michaelismenten-and-full-enzyme-kinetics}

**生化学反応・文献調査のみ。** 酵素の飽和反応です。質量作用則の全体系は過渡的な複合体Cを解き、縮約速度則は速い変数を消去します。

\[
E+S\mathrel{\mathop{\rightleftharpoons}^{k_1}_{k_{-1}}}C\mathrel{\mathop{\longrightarrow}^{k_2}}E+P,\qquad v=V_{\max}S/(K_M+S).
\]

**数値的な課題。** 速い初期層と硬さがあり、全体系と縮約系では適用範囲が異なります。通常の準定常近似ではKM=(k−1+k2)/k1です。

**検証案。** 閉じた反応機構でE+C、S+C+Pの保存を確認します。酵素と基質の尺度比を変え、縮約系と全体系の差を評価します。縮約を厳密解とは扱いません。

**モデルの規約。** 1913年の迅速平衡の解釈と、1925年の準定常状態による導出を区別します。

出典：[Michaelis–Menten（1913、2011年の翻訳を参照）](https://doi.org/10.1021/bi201284u), [Briggs, George E. and Haldane, J. B. S. (1925)](https://doi.org/10.1042/bj0190338), [Johnson, Kenneth A. and Goody, Roger S. (2011)](https://doi.org/10.1021/bi201284u)。

### 03 · 1920 · Lotka–Volterra捕食・被食（Lotka–Volterra predator–prey） {#03-1920-lotkavolterra-predatorprey}

**個体群・生態・文献調査のみ。** 被食者の増殖と捕食を結合したモデルで、位相平面と長時間積分のテストになります。

\[
\dot x=\alpha x-\beta xy,\qquad\dot y=\delta xy-\gamma y.
\]

**数値的な課題。** 正値性と閉軌道の人工的な減衰・増幅を調べます。この理想化モデルの周期軌道は吸引的な極限周期軌道ではありません。

**検証案。** 正のx,yについてH=δx−γ ln(x)+βy−α ln(y)を追跡し、刻みを細かくしたときの軌道ドリフトを比較します。

出典：[Lotka, Alfred J. (1920)](https://doi.org/10.1073/pnas.6.7.410), [Volterra, Vito (1926)](https://doi.org/10.1038/118558a0)。

### 04 · 1926 · McKendrick年齢構造個体群（McKendrick age-structured population） {#04-1926-mckendrick-age-structured-population}

**構造化個体群の輸送・文献調査のみ。** 個体は年齢aの方向へ単位速度で移動し、新生個体は非局所的な更新境界から入ります。

\[
\partial_t n+\partial_a n=-\mu(a)n,\qquad n(0,t)=\int_0^\infty b(a)n(a,t)\,da.
\]

**数値的な課題。** 年齢方向の風上・有限体積輸送、出生境界の求積、無限年齢区間の打ち切りを扱います。

**検証案。** コホートに沿う特性曲線上の生存率と、d∫n da/dt=出生−死亡を確認します。最高年齢からの人工的な流出も含めます。

**モデルの規約。** 古典的な年齢輸送の形です。後年のvon Foersterの系譜も認めますが、その年を初出とは扱いません。

出典：[McKendrick, A. G. (1926)](https://doi.org/10.1017/S0013091500034428)。

### 05 · 1927 · SIR・SEIR区画モデル（SIR and SEIR compartment models） {#05-1927-sir-and-seir-compartment-models}

**感染症区画・文献調査のみ。** 閉じた一様混合系における規格化人口比のモデルです。SEIRでは曝露区画と発症への遷移率を追加します。

\[
\dot s=-\beta si,\quad\dot i=\beta si-\gamma i,\quad\dot r=\gamma i,\quad s+i+r=1.
\]

**数値的な課題。** 各区画の非負性、全人口の不変性、流行ピーク時刻の解像を確認します。

**検証案。** 閉じたSIRで総和1と、β>0,s>0におけるi+s−(γ/β)ln(s)を確認します。初期増殖率βs0−γと最終規模の関係も比較します。

**モデルの規約。** 元の一般的な流行理論は、このSIRへの特殊化より広いものです。人数と人口比ではβの定義が変わります。

出典：[Kermack, W. O. and McKendrick, A. G. (1927)](https://doi.org/10.1098/rspa.1927.0118)。

### 06 · 1937 · Fisher–KPP侵入前線（Fisher–KPP invasion front） {#06-1937-fisherkpp-invasion-front}

**個体群・生態・文献調査のみ。** 侵入個体群や有利な対立遺伝子の空間的な拡大を反応拡散前線で表します。

\[
u_t=D\Delta u+ru(1-u),\qquad 0\leq u\leq1.
\]

**数値的な課題。** 前線速度の時空間誤差、先端の解像、正値性、有限領域の境界による汚染を調べます。

**検証案。** c=5√(Dr/6)のAblowitz–Zeppetella厳密前線を用います。最小速度2√(Dr)を調べる場合は、十分大きな領域と適切に急減する初期値が必要です。

**モデルの規約。** Fisher–KPPは慣用的な系統名です。独立したKPPの1937年原論文の確認は今後の課題です。ここでの特殊な厳密前線の速度は最小速度ではありません。

出典：[Fisher, R. A. (1937)](https://doi.org/10.1111/j.1469-1809.1937.tb02153.x), [Ablowitz, Mark J. and Zeppetella, Anthony (1979)](https://doi.org/10.1007/BF02462380)。

### 07 · 1949 · Monod増殖とケモスタット（Monod growth and chemostat） {#07-1949-monod-growth-and-chemostat}

**生化学反応・文献調査のみ。** 栄養制限を受ける生物量X、基質S、収率Y、希釈率dのケモスタットモデルです。d=0では閉じた回分培養になります。

\[
\mu(S)=\mu_{\max}\frac{S}{K_S+S},\quad\dot X=(\mu(S)-d)X,\quad\dot S=d(S_{in}-S)-\mu(S)X/Y.
\]

**数値的な課題。** 閾値付近のウォッシュアウト、資源と増殖の尺度差、正値性、収率と速度定数の区別に注意します。

**検証案。** d=0でS+X/Yを確認します。d>0ではd(S+X/Y)/dt=d[Sin−(S+X/Y)]を用い、ウォッシュアウト平衡も検証します。

**モデルの規約。** 飽和増殖を一定収率で拡張した一例であり、代謝全般の普遍モデルではありません。

出典：[Monod, Jacques (1949)](https://doi.org/10.1146/annurev.mi.03.100149.002103)。

### 08 · 1952 · Hodgkin–Huxley膜動態（Hodgkin–Huxley membrane dynamics） {#08-1952-hodgkinhuxley-membrane-dynamics}

**興奮系・文献調査のみ。** 膜電位とゲート変数z=m,h,nでイオン性の興奮膜を記述します。ケーブルへの拡張では軸方向の電流を追加します。

\[
C_m\dot V=I_{app}-\bar g_{Na}m^3h(V-E_{Na})-\bar g_Kn^4(V-E_K)-g_L(V-E_L),\quad\dot z=\alpha_z(V)(1-z)-\beta_z(V)z.
\]

**数値的な課題。** ゲートの硬さ、速度式の除去可能特異点、ゲートの範囲、電位・電流の符号と温度の規約を確認します。

**検証案。** 版が明示されたCellML等の規約を選び、静止平衡と電位固定時のゲート緩和を検証してから、スパイク時刻と波形の収束を調べます。

**モデルの規約。** 原論文のイカ巨大軸索モデルは、ヒト心筋に較正したモデルではありません。この調査では特定の速度パラメータ組を選定していません。

出典：[Hodgkin, A. L. and Huxley, A. F. (1952)](https://doi.org/10.1113/jphysiol.1952.sp004764)。

### 09 · 1952 · Turing反応拡散の枠組み（Turing reaction–diffusion framework） {#09-1952-turing-reactiondiffusion-framework}

**模様形成・文献調査のみ。** 一様な反応平衡のまわりで拡散駆動の模様が生じる枠組みです。f,gを一意に指定するモデルではありません。

\[
u_t=D_u\Delta u+f(u,v),\qquad v_t=D_v\Delta v+g(u,v).
\]

**数値的な課題。** 物理不安定性と数値不安定性、領域の固有モード、離散Laplacianの分散関係の誤差を区別します。

**検証案。** 反応則を指定し、J−k²diag(Du,Dv)の固有値と初期のFourierモード成長を比較します。拡散駆動不安定性を論じる前にk=0の反応平衡が安定であることを示します。

**モデルの規約。** 斑点画像や拡散係数の差だけではTuring機構の証明になりません。境界条件が許容モードを決めます。

出典：[Turing, Alan M. (1952)](https://doi.org/10.1098/rstb.1952.0012)。

### 10 · 1961 · FitzHugh–Nagumoの興奮と回復（FitzHugh–Nagumo excitation and recovery） {#10-1961-fitzhughnagumo-excitation-and-recovery}

**興奮系・文献調査のみ。** 速い興奮と遅い回復を規格化したモデルです。空間へ拡張するとパルス、不応期、らせん波を表します。

\[
v_t=D\Delta v+v-v^3/3-w+I,\qquad w_t=\epsilon(v+a-bw).
\]

**数値的な課題。** 硬い時間尺度分離、分割誤差、波速の収束、数値的な波の分裂を調べます。

**検証案。** まずODEの固定点・ヌルクラインと微小摂動の固有値を確認します。2次元らせん動画の前に1次元パルスの収束を調べます。

**モデルの規約。** 広く使われる規格化形の一例です。3次項の係数、回復項の符号、無次元化は定式化によって異なります。

出典：[FitzHugh, Richard (1961)](https://doi.org/10.1016/S0006-3495(61)86902-6), [Nagumo, Jinichi and Arimoto, Suguru and Yoshizawa, Shuji (1962)](https://doi.org/10.1109/JRPROC.1962.288235)。

### 11 · 1970 · Keller–Segel走化性（Keller–Segel chemotaxis） {#11-1970-kellersegel-chemotaxis}

**走化性・文献調査のみ。** 細胞密度nが走化性物質の勾配に沿って移動します。τc=0では化学物質の部分問題が楕円型になります。

\[
n_t=D_n\Delta n-\chi\nabla\cdot(n\nabla c),\qquad\tau_c c_t=D_c\Delta c+\alpha n-\lambda c.
\]

**数値的な課題。** 相互に結合した流束、正値性、質量保存、集中ピークを扱います。人工的な負値を物理的な凝集や爆発と取り違えないようにします。

**検証案。** 細胞の全流束が境界でゼロなら∫nを保存します。一様平衡と線形成長を調べ、特異性を論じる前にピークと領域の収束を確認します。凝集例の前に滑らかな製造解を用います。

**モデルの規約。** より詳細な元の定式化からの一般的な2変数縮約です。爆発閾値は次元、領域、境界条件、化学物質の時間発展に依存します。

出典：[Keller, Evelyn F. and Segel, Lee A. (1970)](https://doi.org/10.1016/0022-5193(70)90092-5)。

### 12 · 1972 · Gierer–Meinhardt活性化・抑制（Gierer–Meinhardt activator–inhibitor） {#12-1972-gierermeinhardt-activatorinhibitor}

**模様形成・文献調査のみ。** 短距離の活性化と長距離の抑制を組み合わせた、代表的な簡略モデルです。

\[
a_t=D_a\Delta a+\rho a^2/h-\mu a+\sigma_a,\qquad h_t=D_h\Delta h+\rho_h a^2-\nu h.
\]

**数値的な課題。** 抑制因子が分母に入るため特異化の可能性があります。hの正値性、細いピーク、反応の硬さを明示的に扱います。

**検証案。** 正の一様平衡を選び、分散関係と抑制因子の正値性を確認してから、ピーク幅と模様の波長の収束を調べます。

**モデルの規約。** 発生源密度、飽和、基礎生成はモデルの派生形で異なります。この簡略式は各原形をそのまま転記したものではありません。

出典：[Gierer, Alfred and Meinhardt, Hans (1972)](https://doi.org/10.1007/BF00289234)。

### 13 · 1972 · 流体・弾性構造と埋め込み境界（Fluid–elastic structure and immersed boundaries） {#13-1972-fluidelastic-structure-and-immersed-boundaries}

**生体力学・文献調査のみ。** 流体と変形構造の連成です。力・構成則を与えることで、弁や膜などの生物学的対象を扱えます。

\[
\rho(\boldsymbol u_t+\boldsymbol u\cdot\nabla\boldsymbol u)=-\nabla p+\mu\Delta\boldsymbol u+\boldsymbol f,\quad\nabla\cdot\boldsymbol u=0,\quad\boldsymbol X_t=\boldsymbol u(\boldsymbol X,t).
\]

**数値的な課題。** 硬い弾性力、圧力投影、Euler–Lagrange間の補間・力分配、体積の漏れが問題になります。

**検証案。** 弾性エネルギーと力をまず指定します。単純に緩和する境界で、力の受け渡し、補間と分配の随伴性、流体の発散、囲まれた体積のドリフトを確認します。

**モデルの規約。** 埋め込み境界は数値的な結合法であり、それだけで閉じた生物構成方程式になるわけではありません。既存の周期MACソルバーはこの連成を実装していません。

出典：[Peskin, Charles S. (1972)](https://doi.org/10.1016/0021-9991(72)90065-4)。

### 14 · 1977 · 化学マスター方程式とGillespie SSA（Chemical master equation and Gillespie SSA） {#14-1977-chemical-master-equation-and-gillespie-ssa}

**確率反応網・文献調査のみ。** 整数分子数、反応ジャンプνj、反応傾向関数ajを用います。SSAはこの連続時間Markovモデルの軌道を標本化します。

\[
\partial_t P(\boldsymbol n,t)=\sum_j\left[a_j(\boldsymbol n-\boldsymbol\nu_j)P(\boldsymbol n-\boldsymbol\nu_j,t)-a_j(\boldsymbol n)P(\boldsymbol n,t)\right].
\]

**数値的な課題。** 組合せを含む正しい反応傾向関数、事象順序、吸収状態、統計誤差を確認します。tau-leapingは別の近似です。

**検証案。** 一定率kの∅→Xと率γnのX→∅を用いると、定常分子数はPoisson(k/γ)です。集団平均・分散・分布を信頼区間とともに比較します。

**モデルの規約。** 1977年論文はSSAの基礎文献であり、全てのマスター方程式の起源を主張するものではありません。SSAは解法で、反応網がモデルです。乱数種は軌道を特定しますが集団検証にはなりません。

出典：[Gillespie, Daniel T. (1977)](https://doi.org/10.1021/j100540a008)。

### 15 · 1977 · Mackey–Glass遅延生理フィードバック（Mackey–Glass delayed physiological feedback） {#15-1977-mackeyglass-delayed-physiological-feedback}

**遅延・遺伝子制御・文献調査のみ。** 規格化した生理制御系の遅延フィードバックです。遅延が安定性と振動挙動を変えます。

\[
\dot x(t)=\frac{\beta x(t-\tau)}{1+x(t-\tau)^p}-\gamma x(t).
\]

**数値的な課題。** 区間[−τ,0]の履歴関数、遅延値の補間、伝播する導関数の不連続、遅延を考慮した適応刻みを扱います。

**検証案。** τ=0のODE極限、一定平衡の履歴、外力付き製造解を確認します。カオス軌道の点ごとの一致を無期限に要求せず、長時間統計を比較します。

**モデルの規約。** スカラー初期値だけでは問題が定まりません。遅延ODEと空間反応拡散モデルは別です。

出典：[Mackey, Michael C. and Glass, Leon (1977)](https://doi.org/10.1126/science.267326)。

### 16 · 1978 · レプリケータ進化ゲーム動態（Replicator evolutionary game dynamics） {#16-1978-replicator-evolutionary-game-dynamics}

**進化動力学・文献調査のみ。** 指定した行列ゲームで、各戦略の比率が相対利得に応じて増減します。

\[
\dot x_i=x_i[(A\boldsymbol x)_i-\boldsymbol x^TA\boldsymbol x],\qquad x_i\geq0,\quad\sum_i x_i=1.
\]

**数値的な課題。** 確率単体の保持、絶滅境界付近の挙動、中立周期と吸引平衡の違いを調べます。

**検証案。** 単体の総和、不変な境界面、解析的に選んだゲーム平衡を確認します。不変量やLyapunov関数はゲームに適したものを用います。

**モデルの規約。** 普遍的なLyapunov関数や、固定点と進化的安定戦略の同値性を仮定しません。

出典：[Taylor, Peter D. and Jonker, Leo B. (1978)](https://doi.org/10.1016/0025-5564(78)90077-9)。

### 17 · 1979 · Schnakenberg反応拡散（Schnakenberg reaction–diffusion） {#17-1979-schnakenberg-reactiondiffusion}

**模様形成・文献調査のみ。** 単純な自己触媒反応則を空間へ拡張したもので、再現可能なTuring不安定性の発生テストに適しています。

\[
u_t=D_u\Delta u+a-u+u^2v,\qquad v_t=D_v\Delta v+b-u^2v.
\]

**数値的な課題。** 反応の硬さ、濃度の正値性、反応系のHopf不安定性と空間的なTuring不安定性の違いを調べます。

**検証案。** u*=a+b、v*=b/(a+b)²を確認し、固定した境界条件のもとで、離散・連続の線形化作用素とモード成長率を比較します。

**モデルの規約。** 数理的な化学模様モデルです。生物の模様に似た画像ができても、組織への較正にはなりません。

出典：[Schnakenberg, Jürgen (1979)](https://doi.org/10.1016/0022-5193(79)90042-0)。

### 18 · 1979 · Shigesada–Kawasaki–Teramoto交差拡散（Shigesada–Kawasaki–Teramoto cross-diffusion） {#18-1979-shigesadakawasakiteramoto-cross-diffusion}

**個体群・生態・文献調査のみ。** 密度依存の自己・相互分散を伴う競争が、空間的な棲み分けを生みます。

\[
u_t=\Delta[(d_1+\alpha_{11}u+\alpha_{12}v)u]+u(a_1-b_1u-c_1v),\quad v_t=\Delta[(d_2+\alpha_{21}u+\alpha_{22}v)v]+v(a_2-b_2u-c_2v).
\]

**数値的な課題。** 結合した非線形拡散行列、単純なスカラー最大原理の議論が使えなくなること、正値性、エントロピーに整合した離散化を扱います。

**検証案。** 滑らかな製造解と一定平衡から始めます。反応なし・法線流束なしでは各種の質量を保存します。エントロピー則を主張する前に係数の仮定を確認します。

**モデルの規約。** 表示式は一様環境への縮約で、元の環境ポテンシャル項を省いています。独立した2本のスカラー拡散方程式とは異なります。

出典：[Shigesada, Nanako and Kawasaki, Kohkichi and Teramoto, Ei (1979)](https://doi.org/10.1016/0022-5193(79)90258-3)。

### 19 · 1983 · Gray–Scott空間自己触媒反応（Gray–Scott spatial autocatalysis） {#19-1983-grayscott-spatial-autocatalysis}

**模様形成・文献調査のみ。** 供給と減衰を含む化学反応モデルです。空間へ拡張すると多様な斑点や波を生じます。

\[
u_t=D_u\Delta u-uv^2+F(1-u),\qquad v_t=D_v\Delta v+uv^2-(F+k)v.
\]

**数値的な課題。** F,k、拡散、領域、有限振幅の初期摂動への感度があります。格子尺度の模様や丸め誤差が長時間の形態に影響する場合もあります。

**検証案。** 全パラメータと摂動の乱数種を記録します。一様状態(1,0)と初期摂動応答を検証し、定量的な観測量の格子・時間収束を調べます。

**モデルの規約。** 1983年は一様混合CSTRの出典で、空間模様はPearson 1993が出典です。斑点分裂だけでは細胞分裂や線形Turing不安定性を示しません。

出典：[Gray, Peter and Scott, Stephen K. (1983)](https://doi.org/10.1016/0009-2509(83)80132-8), [Pearson, John E. (1993)](https://doi.org/10.1126/science.261.5118.189)。

### 20 · 1996 · Aliev–Panfilov心筋興奮（Aliev–Panfilov cardiac excitation） {#20-1996-alievpanfilov-cardiac-excitation}

**興奮系・文献調査のみ。** 心筋波と回復特性を表す、現象論的に縮約した興奮・回復モデルです。

\[
u_t=D\Delta u-ku(u-a)(u-1)-uv,\quad v_t=\left(\epsilon_0+\frac{\mu_1v}{u+\mu_2}\right)[-v-ku(u-b-1)].
\]

**数値的な課題。** 回復過程の硬さ、分母の挙動、波速・回復曲線の解像度と時間分割への感度を調べます。

**検証案。** モデルの符号化版とパラメータを指定し、2次元リエントリーの前に単一細胞と1次元伝導の収束を確立します。らせん画像だけでなく回復曲線を比較します。

**モデルの規約。** 単領域・双領域の組織モデルは伝導率テンソルを追加し、双領域では細胞外の楕円型制約も加わります。この2変数モデルに自動的に含まれるものではありません。

出典：[Aliev, R. R. and Panfilov, A. V. (1996)](https://doi.org/10.1016/0960-0779(95)00089-5)。

### 21 · 2000 · Repressilator mRNA・タンパク質回路（Repressilator mRNA–protein network） {#21-2000-repressilator-mrnaprotein-network}

**遅延・遺伝子制御・文献調査のみ。** 3つの抑制遺伝子を環状に結びます。mRNAとタンパク質を両方保持すると状態変数は6つになります。

\[
\dot m_i=\frac{\alpha}{1+p_{i-1}^n}+\alpha_0-m_i,\quad\dot p_i=\beta(m_i-p_i),\qquad i=1,2,3\ \text{cyclic}.
\]

**数値的な課題。** 複数の分解尺度、振動の発生、位相誤差、決定論的周期と単一細胞の雑音を伴う挙動の差を調べます。

**検証案。** 対称平衡と線形安定性を確認します。過渡時間を明示し、その後の周期と振幅を時間刻みの細分化で比較します。

**モデルの規約。** 6変数形と3タンパク質への縮約形は異なります。振動の有無はパラメータに依存します。

出典：[Elowitz, Michael B. and Leibler, Stanislas (2000)](https://doi.org/10.1038/35002125)。

### 22 · 2000 · 遺伝子トグルスイッチ（Genetic toggle switch） {#22-2000-genetic-toggle-switch}

**遅延・遺伝子制御・文献調査のみ。** 相互抑制によって双安定スイッチが生じうる、規格化された遺伝子モデルです。

\[
\dot u=\frac{\alpha_1}{1+v^p}-u,\qquad\dot v=\frac{\alpha_2}{1+u^q}-v.
\]

**数値的な課題。** パラメータに依存する双安定性、鞍点の分離曲線、連続追跡、吸引域境界付近の摂動への感度を調べます。

**検証案。** 全ての正の平衡とJacobian固有値を求めます。十分遅いパラメータ追跡と複数初期値で履歴現象を検証します。

**モデルの規約。** 任意のHill指数や生成率で双安定性が保証されるわけではありません。誘導、mRNA動態、雑音は追加のモデル選択です。

出典：[Gardner, Timothy S. and Cantor, Charles R. and Collins, James J. (2000)](https://doi.org/10.1038/35002131)。

## 動画の前に組み立てる検証経路 {#a-verification-path-before-attractive-movies}

最初の実装順として、**ロジスティック／SIR → 酵素反応の全体系 → Fisher前線 → FitzHugh–Nagumoパルス → Schnakenbergモード → Keller–Segel凝集**を提案します。捕食被食はHamilton系ノートと並行して長時間不変量を調べ、出生死滅SSAを最初の確率的分岐にできます。Gray–Scottはその後の視覚的な化学展示に向きますが、供給率、空間尺度、初期摂動、出典を明示します。これは実装順の提案で、歴史順とは別です。

### 非線形前線の厳密解 {#an-exact-nonlinear-front}

尺度化したFisher方程式では、[Ablowitz–Zeppetella（1979）](https://doi.org/10.1007/BF02462380)の特殊な前線が、決定論的な比較基準になります。

\[
u(x,t)=\left[1+\exp\left(\sqrt{\frac r{6D}}(x-ct-x_0)\right)\right]^{-2},
\qquad c=5\sqrt{\frac{Dr}{6}}.
\]

有限区間では、厳密解に一致する時間依存境界値を与えるか、境界を十分遠ざけて打ち切りの影響を測ります。前線位置、形状のノルム、時間・空間の細分化をそれぞれ比較します。この特殊な陽表示の前線は最小速度の前線より速く進みます。両者を混同すると、解法に存在しない誤差を検出してしまいます。

### 模様の発生を定量的に調べる {#pattern-onset-is-a-quantitative-test}

選んだ2種反応系の平衡でJacobian Jを作ります。連続体では波数ベクトルkのFourierモードを、次の作用素が発展させます。

\[
L(k)=J-|k|^2\operatorname{diag}(D_u,D_v).
\]

一様な正方格子と中心差分Laplacianでは、|k|²を次で置き換えます。

\[
\kappa_h^2=\frac4{h^2}
\left[\sin^2(k_xh/2)+\sin^2(k_yh/2)\right].
\]

小振幅の固有モードをひとつ与え、初期の指数成長を測って、両方の分散関係と比較します。k=0の反応系が安定で非零モードが不安定なら、選んだ拡散駆動不安定性を診断できます。非線形段階の斑点だけでは診断できません。Schnakenbergはこの実験に単純な反応則を与えますが、Turing自身の例と黙って置き換えてはいけません。周期境界とゼロ流束境界では許されるモードが異なります。

### 解法を評価する前にモデルを固定する {#preserve-the-model-before-judging-the-method}

将来の各計算では、有次元・規格化変数、全パラメータ、初期・境界条件、単位、必要なら乱数種、モデルの版と出典を指定します。収支には境界流束と生成項を含めます。すべての生物反応拡散問題が各種の質量を保存するわけではありません。値を切り詰める正値化は総量や絶滅閾値を変える場合があります。拡散部分を陰的に解くだけでは、分割更新全体の正値性は証明できません。

確率反応網では、離散化・モデル近似と有限標本集団の統計的不確かさを分けます。非線形反応網でODE解が確率系の厳密な平均に一致するとは限りません。遅延方程式では履歴関数と補間則を記録します。生化学の縮約では、モデル縮約誤差と積分誤差を別々に測ります。

## 出典と今後の分岐 {#sources-and-further-branches}

[Murrayの第3版入門書（2002）](https://doi.org/10.1007/b98868)は、これらの分野を横断する読書経路になります。Physiomeの[Hodgkin–Huxleyワークスペース](https://models.cellml.org/workspace/hodgkin_huxley_1952)と[Aliev–Panfilovの符号化](https://models.cellml.org/workspace/241/file/1164ecbd63d818c0d6c9631ef6bd92f12e87ae6b/model.xml)は、実装パラメータを選ぶ前に確認すべきモデルの版の参照先です。独立した検証データではありません。

今後の独立した調査対象には、神経集団場、空間確率反応拡散、細胞内極性と質量保存反応網、細胞周期のサイズ構造、頂点・位相場による細胞力学、腫瘍と栄養の自由境界、遺伝的浮動を含む集団遺伝学などがあります。現在の22項目が生物モデルの全範囲を尽くすという主張ではありません。指定した方程式に対する数値検証と、生物個体や実験データに対する妥当性検証も異なります。

[方程式ギャラリー](equation-gallery.md)、[歴史アトラス](history.md)、[全参考文献](references.md)へ戻れます。
