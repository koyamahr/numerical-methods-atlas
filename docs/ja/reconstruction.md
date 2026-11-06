# Euler再構成：PPM・特性変数・WENO-Z・AUSM

[計算済み比較を開く](#/reconstruction)。1次元で再構成と数値流束を区別して調べます。従来の[成分ごとのMUSCL／WENO基準例](benchmarks.md)を残して拡張します。

## 比較するもの {#what-is-compared}

再構成表示では、保存変数成分／特性変数でのMUSCL・MC、制限付き放物線有限体積、有限差分WENO5-JS／Zを比較します。FVはHLLC、FDは大域Lax–Friedrichs流束分離を使い、ともにSSPRK3、公称CFL 0.3、同じ格子点数です。表現・流束・誤差ノルムが異なり、再構成だけの比較や同じ計算費用での順位ではありません。各手法内で基底だけを変える比較は条件を揃えています。

別の流束表示は保存特性変数MUSCL・MCとSSPRK3を固定し、HLLC、音響エントロピー修正付きRoe、Einfeldt型HLLE、後述のAUSM基準例を切り替えます。

## 制限付き放物線有限体積 {#limited-parabolic-finite-volumes}

[Colella–Woodward（1984）](https://doi.org/10.1016/0021-9991(84)90143-8)の再構成の考え方に沿い、セル平均と両端値から放物線を作ります。確認した公開資料は[1982年の著者プレプリント](https://escholarship.org/uc/item/5sr307f1)で、最終学術誌版とは異なります。本実装は端値補間・単調性制約を含み、method of linesでSSPRK3と結合します。原型PPMの波の追跡、接触面強調、衝撃波平坦化、Lagrange発展・再配置は今後の課題です。

セル平均Q、端値L,R、ξ∈[0,1]として、

\[
 q(\xi)=L+\xi[R-L+q_6(1-\xi)],\qquad q_6=6Q-3(L+R).
\]

とすれば、積分平均は厳密にQです。隣接平均の範囲で端値を制限し、極値を平坦化して曲率制約を適用します。セル内で固定した保存変数の特性基底へ偏差を射影し、制限して戻します。「成分」は基本変数ではなく保存変数です。必要なら左端・中点・右端にQまわりの共通の正値縮小を施し、Simpson平均Qを保ちます。保存平均をクリップせず、不正なRK段階では時間刻みを半分にして再試行します。完全離散正値性の一般的証明ではありません。

## 特性変数の有限差分WENO-Z {#characteristic-finite-difference-weno-z}

各面でRoe平均の保存変数特性基底を固定します。正負の大域LF分離流束を射影し、特性成分ごとに再構成して面流束へ戻します。FDは点値を進める方式で、FVの状態再構成とは異なります。周期格子では共有流束差分により離散和を保存します。

Z変種はJSの滑らかさ指標を使い、

\[
 \tau_5=|\beta_0-\beta_2|,\quad
 \alpha_k^Z=d_k\left[1+\left(\frac{\tau_5}{\beta_k+\epsilon}\right)^2\right],
 \quad\omega_k^Z=\frac{\alpha_k^Z}{\sum_l\alpha_l^Z},
 \quad(d_0,d_1,d_2)=(0.1,0.6,0.3).
\]

とします。ε=10⁻⁶、Zの指数2を固定します。正則化と特性基底の規格化は重みに影響するため、比較条件に含めます。原典の書誌は[Borges・Carmona・Costa・Don（2008）](https://doi.org/10.1016/j.jcp.2007.11.038)です。出版社メタデータと[以前の3著者の草稿](https://citeseerx.ist.psu.edu/document?doi=84e17864257f4a33bd045df500e93cbad44e8f49&repid=rep1&type=pdf)を確認しましたが、草稿は重みの規約が異なります。上の式・指数と実行検証が本版の変種を定義し、最終論文の図は再現していません。

## AUSMは変種を明示する {#ausm-keep-the-variant-explicit}

AUSMの原典は[Liou–Steffen（1993）](https://doi.org/10.1006/jcph.1993.1122)です。本基準例は共通面音速a=(aL+aR)/2、亜音速のMach分割M±=±(M±1)²/4、3次圧力分割P±=(M±1)²(2∓M)/4を使います。超音速側は符号に従う風上分割です。式は[FEST-3Dの公式AUSMソース](https://fest3d.github.io/sourcefile/ausm.f90.html)と照合しました。定義を明示した独立のAUSM系列実装であり、FEST-3Dの計算結果や1993年の全音速・圧力選択肢の再現ではありません。

Mf=M+(uL/a)+M−(uR/a)を使い、(ρ,ρu,ρv,ρH)を左のa max(Mf,0)と右のa min(Mf,0)で輸送します。pL P+(uL/a)+pR P−(uR/a)を法線運動量だけに加え、エネルギーには全エンタルピーを輸送します。一様場、両向き超音速、Mach ±1の分岐、静止・移動接触面、Euler問題を検証します。

[AUSM+（1996）](https://doi.org/10.1006/jcph.1996.0256)、[AUSM+-up（2006）](https://doi.org/10.1016/j.jcp.2005.09.020)は独立した拡張予定です。現基準例に全速度補正や低Mach検証はありません。名称だけで普遍的な衝撃波安定性は導けません。[odd–even比較](#/shock-robustness)も参照してください。

## 問題・参照・精度 {#problems-references-and-accuracy}

- **Sod**：N=200、[0,1]、t=0.2、標準状態、外挿端。
- **移動接触面**：N=200、周期[0,1]、u=p=1、前半の密度1・後半2、1周t=1。
- **Shu–Osher**：N=240、[−5,5]、t=1.8、固定端。x=−4の左は(ρ,u,p)=(3.857143,2.629369,10.33333)、右は密度1+0.2sin(5x)、u=0,p=1。破線は本実装の特性FD WENO-Z・N=960で、厳密解や外部コード検証ではありません。

FVの初期値は保存量を積分します。Sodの最終密度誤差は解析リーマン解の128点Gauss求積を使い、64／128点の差で不連続を跨ぐ求積感度を記録します。FD誤差は点値です。FV基本変数曲線は保存平均からの変換で、基本変数そのものの厳密平均ではありません。Shu–Osherの厳密誤差は報告しません。

別の滑らかな周期エントロピー波をN=32,64,128、t=0.2、CFL=0.25(32/N)^(2/3)で計算します。dt∝dx^(5/3)によりSSPRK3の時間誤差をO(dx⁵)へ抑えます。この問題のWENO観測次数は約5、極値制限のある放物線FVは約2です。衝撃波や任意の臨界点での5次精度保証ではありません。

![再構成の計算比較](figures/reconstruction/reconstruction.png)

再現は`python scripts/build_reconstruction.py`です。[分布・診断・ソースハッシュ](figures/reconstruction/reconstruction.json)と[保存変数配列](figures/reconstruction/fields.npz)を取得できます。正値性・再試行回数は、ここで示したテストの範囲です。
