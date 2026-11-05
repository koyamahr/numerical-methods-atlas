# 地球流体のArakawa A・B・C格子

A／B／Cは**格子上で異なる変数を置く位置**を指定し、精度次数、セル形状、時間積分の分類ではありません。構造長方形格子はいずれの配置も使えます。従来の比較は[Arakawa–Lamb（1977）](https://doi.org/10.1016/B978-0-12-460817-7.50009-4)、機関による解説は[ECMWF数値計算法ノート](https://www.ecmwf.int/sites/default/files/elibrary/2002/16948-numerical-methods.pdf)を参照してください。

**本実装**は、線形周期f平面浅水系の配置図と検証済みFourier記号です。A／B／Cの非線形気象・海洋モデルや、新しい完全な流体計算ではありません。

## A・B・Cは相対配置を表す {#a-b-and-c-specify-relative-placement}

正方形セル幅Δで、自由表面摂動ηをスカラー中心(i+1/2,j+1/2)に置きます。uはx速度、vはy速度です。

- **A格子**：η、u、vを同じ中心に置きます。
- **B格子**：ηは中心、u・vは両方とも頂点(i,j)です。
- **C格子**：ηは中心、uはx法線面(i,j+1/2)、vはy法線面(i+1/2,j)です。

原点を中心から頂点に移すと図の規約が逆に見える場合がありますが、相対配置は変わりません。モデル間の添字を比べる前に、位置と成分方向を描いてください。

![A／B／C配置と4つの線形分散比較](figures/geophysical-grids.png)

C格子では面法線速度から自然にセル発散が得られ、スカラーの中心間差から面圧力勾配が得られます。既存の[周期MAC射影](incompressible.md)もこの配置です。ただし一致するのは空間位置で、MACと海洋C格子コアのCoriolis・移流・境界・時間方式まで同じとは限りません。[MITgcm公式のスタガード配置](https://mitgcm.readthedocs.io/en/latest/algorithm/c-grid.html)は、この面法線配置を3次元で示します。

## 回転と重力波で違いを見る {#rotation-and-gravity-waves-make-the-difference-visible}

一定平均水深H、一定Coriolis係数fでは、

\[
u_t-fv=-g\eta_x,\qquad v_t+fu=-g\eta_y,
\qquad\eta_t+H(u_x+v_y)=0.
\]

です。連続系にはゼロ周波数の地衡流分岐と、重力波分岐、

\[
\omega^2=f^2+c^2(k^2+\ell^2),\qquad c=\sqrt{gH},\qquad L_D=c/|f|.
\]

があります。離散分散関係は位置**と**演算子に依存します。各格子に中心2次の圧力・発散演算子を使い、C格子のCoriolisにはu・v位置間の対称4点補間を使います。物理配置の位相を除いた実効波数は、

\[
\begin{aligned}
A:\quad &\widetilde k=\sin(k\Delta)/\Delta,
&\widetilde\ell=\sin(\ell\Delta)/\Delta,&\quad f_h=f,\\
B:\quad &\widetilde k=2\sin(k\Delta/2)\cos(\ell\Delta/2)/\Delta,
&\widetilde\ell=2\cos(k\Delta/2)\sin(\ell\Delta/2)/\Delta,&\quad f_h=f,\\
C:\quad &\widetilde k=2\sin(k\Delta/2)/\Delta,
&\widetilde\ell=2\sin(\ell\Delta/2)/\Delta,&\quad f_h=f\cos(k\Delta/2)\cos(\ell\Delta/2).
\end{aligned}
\]

です。計算する基準系はω_h²=f_h²+c²(k̃²+ℓ̃²)です。エネルギー尺度化状態(u,v,cη/H)の3×3 Fourier生成行列は歪Hermiteで、固有値は0、±iω_hです。**半離散**の結果であり、空間が線形エネルギーを保存しても、時間積分は位相誤差・減衰・不安定性を加え得ます。

## チェッカーボードと未解像の変形半径 {#checkerboards-and-an-unresolved-deformation-radius}

中心A格子の圧力勾配は、座標方向に最短の交互高さモードを見ません。B格子基準系は軸方向だけの零モードを除きますが、対角高さチェッカーボードを残します。C格子の勾配・発散はそのモードを結合しますが、単純Coriolis平均は一部の最短波で消えます。異なる演算子効果であり、単一の普遍的チェッカーボード診断ではありません。

図はL_D/Δ=0.25、2で軸・対角波を比較します。この正方格子演算子では対角方向のA・Bは重なり、軸方向は異なります。変形半径が未解像だと、Coriolis平均はC格子の慣性周波数近傍の分岐を強く歪め得ます。「Cが常に最良」とは結論できません。解像された重力波、粗格子の地衡流調節、方向誤差は別のテストです。C配置を変えずにCoriolis離散化だけで比較は変わります。

## D・E、鉛直スタガード、磁場格子 {#d-and-e-vertical-staggering-and-magnetic-grids}

**D格子**はCに対してu・vの面位置を交換し、uをy法線面、vをx法線面に置きます。矢印は依然として物理x・y成分なので、Cの速度配列を改名するだけではDの図になりません。**E格子**は一般にBを45度回転した配置と見なされ、添字と解像可能な波数集合を整合して扱う必要があります。説明のみで記号は未実装です。

水平Arakawa配置と、**Lorenz対Charney–Phillipsの鉛直配置**は別です。同様に[MHDのCT](mhd.md)は面・辺で磁場発散恒等式を保ちますが、Arakawa C浅水法と同義ではありません。それぞれ整合する離散演算子が必要です。

## 根拠と次の地球流体テスト {#evidence-and-the-next-geophysical-benchmarks}

`numart.geophysical_grids`がA／B／C記号を供給します。独立に物理格子差分をFourier波へ作用させて比較し、歪Hermiteエネルギー構造、地衡流ゼロ分岐、長波の2次収束、異なる短波零モードを検査します。`python scripts/build_geophysical_grids.py`で図を再現し、[記録](figures/geophysical-grids.json)に仮定・標本周波数・ソースハッシュを残します。

今後は地衡流調節、慣性重力波、沿岸Kelvin波、β平面Rossby波、続いて渦位と非線形エネルギー・エンストロフィー収支が適切です。現行の一定f記号は、β平面Rossby伝播、海岸、球面計量、地形、濡れ・乾きを検証しません。非線形Arakawa Jacobianやエネルギー・エンストロフィー保存浅水流束は別のアルゴリズムで、A／B／Cを選ぶだけでは不変量は得られません。
