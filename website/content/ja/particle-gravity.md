# 粒子重力：PM、P³M、ツリー、多重極、マルチグリッド

Poissonソルバーと粒子力アルゴリズムは、関係する問いに異なる表現で答えます。Green関数、境界、質量割当て、軟化、力演算子を先に固定します。周期PMと孤立直接和は別の問題なので、差をそのまま力精度とはできません。

![孤立ツリーの開口角誤差・作業数、周期PM密度割当て、製造Poisson解](figures/particle-gravity.png)

## 粒子格子法：質量からポテンシャル、力へ {#particlemesh-mass-to-potential-to-force}

3次元周期立方体では、

\[
\nabla^2\phi=4\pi G(\rho-\overline\rho),\qquad
\widehat\phi(\boldsymbol k)=-\frac{4\pi G}{|\boldsymbol k|^2}\widehat\rho(\boldsymbol k)
\quad(\boldsymbol k\ne0),\qquad \widehat\phi(0)=0.
\]

です。平均を引くことで周期適合条件を満たし、ポテンシャルのゼロモードでゲージを固定します。水平平均が実際の鉛直力を生む孤立薄層とは異なります。

PMは質量を格子へ割り当て、Poissonを解き、ポテンシャルを微分して粒子へ加速度を補間します。例は3次元の8近傍節点へのcloud-in-cell（CIC）、連続Fourier Laplacian記号、スペクトル力微分を使います。偶数格子微分では対を持たないNyquistモードをゼロにします。整合したCIC割当て・補間と奇対称力演算子により、選定した周期例で内部力の総和が丸め誤差までゼロになります。

割当て・補間は力を平滑化します。格子Green関数、離散微分、エイリアシング、格子異方性、デコンボリューションが実効相互作用へ影響します。製造した格子モードを正確に解いても、近接対の力精度は示せません。

## P³M：近距離を二重計上せず補正する {#p³m-correct-the-near-field-without-counting-it-twice}

粒子・粒子／粒子・格子法は格子力に短距離補正を加えます。

\[
\boldsymbol a_i=\boldsymbol a_i^{\rm PM}
+\sum_{j\in\mathcal N_i}\left(\boldsymbol a_{ij}^{\rm target}
-\boldsymbol a_{ij}^{\rm mesh,near}\right).
\]

引く項は、選んだPM割当て・力演算子、または整合設計の力分割に対応する必要があります。完全なPMへ未修正Newton対力を加えると一部を二重計上します。近傍リストと集積が短距離の計算量を決めます。[HockneyのP³Mコード原解説](https://www.ccp5.ac.uk/wp-content/uploads/2023/03/CCP5_Newsletter_1981_06_01.pdf)を参照してください。

実用P³M、対応する補正表、適応細分化は**未実装**です。

## Barnes–Hutツリー：近いセルを開く {#barneshut-tree-open-the-nearby-cells}

[Barnes・Hut（1986）](https://doi.org/10.1038/324446a0)は粒子を八分木にまとめます。遠方セルは質量分布のモーメントで近似し、近方セルは再帰的に開きます。本実装の幾何受理条件はs/d<thetaで、sはセル辺長、dは重心までの距離です。標的を含むノードは常に開き、直接葉では自己相互作用を除きます。

孤立参照はG=1とPlummer軟化です。

\[
\boldsymbol a_i=-\sum_{j\ne i}m_j
\frac{\boldsymbol x_i-\boldsymbol x_j}
{(|\boldsymbol x_i-\boldsymbol x_j|^2+\epsilon^2)^{3/2}}.
\]

ツリーと直接和は粒子、質量、epsilonを同じにします。小thetaは通常、相互作用数を増やして誤差を減らしますが、個別粒子誤差は単調とは限りません。O(N log N)は適切な分布での代表的な尺度で、このPython例の時間測定や最悪計算量の保証ではありません。

## 多重極：単極と2次モーメント {#multipole-expansion-monopole-and-second-moments}

セル重心から標的へのR、源のずれdelta_a、総質量M、S=sum m_a delta_a delta_a^Tとします。重心の双極は消えます。s²=R²+epsilon²として、同じ軟化核のTaylor展開は、

\[
\phi(\boldsymbol R)\approx-G\left[
\frac{M}{s}+\frac{3\boldsymbol R^T S\boldsymbol R}{2s^5}
-\frac{\operatorname{tr}S}{2s^3}\right].
\]

です。コードはこのポテンシャルを解析微分します。トレースを含む全2次モーメントを残し、非軟化・トレースなし四重極式へ黙って置換すると近似が変わります。図は単極・2次モーメントを同じ直接力和と比較します。

高速多重極法（FMM）は局所展開も作って移動し、セル間相互作用を再利用します。Barnes–Hutへ四重極を加えるだけではありません。[Greengard・Rokhlin（1987）](https://doi.org/10.1016/0021-9991(87)90140-9)が原典で、展開移動は未実装です。

## TreePM：別の近距離評価 {#treepm-a-different-near-field-evaluator}

TreePMは格子長距離場とツリー短距離場を結びます。代表的なGaussianポテンシャル分割は、

\[
\widehat\phi_{\rm long}=\widehat\phi\,e^{-k^2r_s^2},\qquad
\phi_{\rm short}(r)=-\frac{Gm}{r}\operatorname{erfc}\left(\frac{r}{2r_s}\right).
\]

です。短距離力はこのポテンシャルの微分であり、Newton力にerfcを掛けるだけではありません。打切り、周期性、軟化も分割に整合させます。[SpringelのGADGET-2論文](https://arxiv.org/abs/astro-ph/0505010)が一次例です。ここでの独立したPMとツリーの2例は、TreePM実装を**構成しません**。

## マルチグリッドの位置付け {#where-multigrid-belongs}

マルチグリッドは対力の直接和ではなく、離散楕円型方程式を解きます。平滑化で振動誤差を減らし、制限・粗格子解・延長・補正で滑らかな成分を扱います。演算子・境界・粒子結合を指定すれば、粒子格子のPoisson解法を置き換えられます。

[既存実装](elliptic.md)は**2次元5点負Laplacian、ゼロDirichlet境界**で、孤立3次元粒子重力ではありません。有限孤立格子の境界値には多重極や開放境界構成が使え、近い箱面でphi=0とするだけでは一般に無限遠phi→0を再現しません。

## 静的な検査を再現する {#reproduce-the-static-checks}

```bash
python scripts/build_particle_gravity.py
```

図と[測定記録](figures/particle-gravity.json)を作ります。ツリー例は等質量192粒子、seed17、epsilon=0.03、開口角5種、モーメント次数2種です。誤差は||a_tree−a_direct||₂/||a_direct||₂です。受理ノード数と直接対数を報告しますが、操作コストが異なるため和を時間比較には使いません。

PMは24³周期格子です。別の密度1+0.2cos(2pi x)はG=1でポテンシャル−0.2cos(2pi x)/piを持ちます。テストはCIC質量保存、周期折返し、定数補間、自己力、総力、製造モード、theta=0の厳密開放、選定した力誤差収束を扱います。標的ごとの近似ツリーは対運動量を厳密には保たない場合があるため、記録に総力診断を含めます。

[孤立FFTとスラブGreen関数](gravity-boundaries.md)、力と時間積分の追加要件を扱う[シンプレクティック写像](symplectic.md)へ進んでください。
