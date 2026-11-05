# Chapman–Enskog展開：分布から輸送へ

Chapman–Enskog（チャップマン–エンスコッグ）展開は、運動論的な緩和と、ゆっくり変化する流体場を分けます。古典的な運動論はChapman・Cowlingの『The Mathematical Theory of Non-Uniform Gases』（初版1939年、第3版1970年）で扱われています。書籍の出版年は展開の発明年ではありません。この章では、外力なし・等温・低Mach数の格子BGKについて、独立した導出を示します。

## 小さなパラメータと可解条件 {#a-small-parameter-and-solvability}

遅い変化を整理するパラメータεを導入します。

\[
f_q=f_q^{(0)}+\epsilon f_q^{(1)}+\epsilon^2 f_q^{(2)}+\cdots,
\quad \partial_t=\epsilon\partial_{t_1}+\epsilon^2\partial_{t_2},
\quad \nabla=\epsilon\nabla_1.
\]

保存モーメントは局所平衡が担うため、高次補正の質量・運動量モーメントはゼロです。

\[
\sum_q f_q^{(k)}=0,\quad
\sum_q\boldsymbol c_q f_q^{(k)}=0\quad (k\geq1).
\]

これらは展開の制約で、非平衡応力を消す指示ではありません。f^(1)の応力モーメントが粘性輸送を生みます。

## 離散時間のTaylor項を残す {#keep-the-discrete-time-taylor-term}

格子BGKの並進側をD_q=∂t+c_q·∇で展開します。格子時間単位のTaylor展開はD_q f_q + D_q² f_q/2から始まり、次数ごとに、

\[
f_q^{(0)}=f_q^{eq},\qquad
f_q^{(1)}=-\tau D_{1q} f_q^{eq},
\]

\[
\partial_{t_2} f_q^{eq}
+\left(1-\frac1{2\tau}\right)D_{1q}f_q^{(1)}
=-\frac{f_q^{(2)}}{\tau}.
\]

を得ます。1次の質量・運動量モーメントが連続の式とEuler部分を、2次の応力補正がNewton粘性部分を与えます。D2Q9平衡の等方性、低Mach近似、上の係数から、せん断動粘性係数は、

\[
\nu=c_s^2\left(\tau-\frac12\right)\Delta t.
\]

となります。ここでτは、緩和に使う**格子時間ステップ数を表す無次元量**で、物理的な緩和時間はτ_relax=τΔtです。一方、連続時間BGKでは対応する等温モデルのν=c_s²τ_relaxとなり、並進のTaylor半ステップはありません。定義を混ぜると粘性を誤ります。

## この導出が示す範囲 {#what-this-derivation-does-and-does-not-establish}

[D2Q9実験](lattice-boltzmann.md)は式へ代入するだけでなく、せん断減衰から粘性を測ります。[Qianら（1992）](https://doi.org/10.1209/0295-5075/17/6/001)が格子モデルの出典で、[BGKの原典](https://doi.org/10.1103/PhysRev.94.511)は連続運動論の緩和を扱います。[Guoら（2002）](https://doi.org/10.1103/PhysRevE.65.046308)の外力離散化は別で、上の無外力の代数ではそのソース項を導出していません。

打切った等温平衡に対して、小さな勾配と小さなMach数を仮定する、平衡近傍の形式的な漸近展開です。衝撃波近傍の安定性、任意の緩和時間、エネルギー方程式の回復、一般的な希薄気体Boltzmannソルバーとしての妥当性を保証しません。Burnett次数の輸送や熱的衝突モデルには、追加モーメントと解析が必要です。
