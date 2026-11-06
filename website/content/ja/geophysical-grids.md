# 球面メッシュとArakawa A・B・C格子

A／B／Cは**格子上で異なる変数を置く位置**を指定し、精度次数、セル形状、時間積分の分類ではありません。構造長方形格子はいずれの配置も使えます。従来の比較は[Arakawa–Lamb（1977）](https://doi.org/10.1016/B978-0-12-460817-7.50009-4)、機関による解説は[ECMWF数値計算法ノート](https://www.ecmwf.int/sites/default/files/elibrary/2002/16948-numerical-methods.pdf)を参照してください。

**本実装**は、球面メッシュの幾何図、線形周期f平面浅水系の配置図と検証済みFourier記号です。A／B／Cの非線形気象・海洋モデルや、新しい完全な流体計算ではありません。

## 球面には複数の座標チャートを使う {#spherical-meshes}

メッシュの幾何と変数の配置は別の選択です。cubed-sphereにもC格子配置を使え、三角形メッシュにも辺法線速度を置けます。A／B／Cという名前だけでは、球面の接続関係や計量は決まりません。

![同じ正射影で比べた緯度経度・陰陽・cubed-sphere・正二十面体格子](figures/spherical-meshes.png)

半径Rの球面で、緯度をφ、経度をλとすると、

\[
 ds^2=R^2\left(d\varphi^2+\cos^2\varphi\,d\lambda^2\right),
 \qquad \Delta s_\lambda\simeq R\cos\varphi\,\Delta\lambda.
\]

地理的な極は物理的な特異点ではありません。極では経度が定義できず、極の近くでは同じ経度刻みに対する距離が小さくなります。そのため陽的な波・移流計算のCFL制約が厳しくなり得ます。極フィルター、縮約格子、スペクトル法などの対処法もあり、メッシュの置換だけが選択肢ではありません。以下の3構成は単一の緯度経度チャートで生じる極への集中を回避しつつ、接続や計量の問題を導入します。自動的に等面積になるわけではありません。

## 陰陽格子：低緯度パッチを二つ重ねる {#yin-yang}

[Kageyama–Sato（2004）](https://arxiv.org/abs/physics/0403123)は同じ形の緯度経度パッチ二つを組み合わせます。各パッチ自身の座標では、

\[
 |\varphi|\leq\pi/4+\delta,\qquad |\lambda|\leq3\pi/4+\delta,
 \qquad
 \boldsymbol{x}^{\mathrm{Yang}}=
 \begin{pmatrix}-1&0&0\\0&0&1\\0&1&0\end{pmatrix}
 \boldsymbol{x}^{\mathrm{Yin}}.
\]

回転により各チャートの極は相手の低緯度領域に入ります。図はδ=3°で、紫は重複領域であり、第3のパッチではありません。各成分は直交した緯度経度座標と馴染みのある計量を保持します。重複領域を通した境界データの受け渡しが必要です。スカラー値の補間だけでは全体の質量保存は保証されず、重複領域の所有・重みと保存的な接続の設計が必要です。速度成分は局所接平面の基底間で回転させます。ここではその仕組みを説明し、重合格子の輸送ソルバーは実装していません。

## Cubed-sphere：六つの面を接続する {#cubed-sphere}

六面構成の代表的な文献は[Ronchi–Iacono–Paolucci（1996）](https://doi.org/10.1006/jcph.1996.0047)です。この図では**等角刻みの心射図法**を選びます。外向き法線nと接方向e₁、e₂からなる面の正規直交フレームに対し、

\[
 \boldsymbol{x}(\xi,\eta)=R\,
 \frac{\boldsymbol{n}+\tan\xi\,\boldsymbol{e}_1+\tan\eta\,\boldsymbol{e}_2}
 {\left\lVert\boldsymbol{n}+\tan\xi\,\boldsymbol{e}_1+\tan\eta\,\boldsymbol{e}_2\right\rVert},
 \qquad -\pi/4\leq\xi,\eta\leq\pi/4.
\]

図は各面8×8セルです。隣り合う面の境界は一致し、立方体の各頂点では3面が接続します。緯度経度の極は避けられますが、この写像は面内で一般に非直交で、セル面積と計量係数も変化します。別のcubed-sphere投影では性質が異なります。継ぎ目で隣接添字、ベクトル成分、数値流束を整合させる必要があり、連続に見える図だけでは演算子の検証になりません。

## 正二十面体の三角形と双対格子 {#icosahedral}

20枚の三角形から始め、辺の中点で各三角形を4分割し、新しい頂点を球面へ動径方向に投影します。細分化レベルLでは、

\[
 F=20\,4^L,\qquad E=30\,4^L,\qquad V=10\,4^L+2,
 \qquad V-E+F=2.
\]

![正二十面体から細分化した三角形格子と重心型の多角形双対格子](figures/spherical-dual.png)

レベル2は三角形320枚、辺480本、頂点162個です。12頂点だけ隣接数が5で、それ以外は6です。共有辺の中点を通して隣接する三角形の中心を結ぶと、五角形12枚と残りが六角形の双対ができます。ここでは**正規化した三角形の重心**を使うため、重心型双対であり、Voronoi／Delaunayの直交対という意味ではありません。この未最適化の例では最大三角形面積は最小の約1.275倍です。準一様と等面積は同じではありません。個数の公式はこの規則的細分化に対するもので、任意の球面非構造格子にそのまま当てはまるわけではありません。

[ICONのモデル解説](https://gmd.copernicus.org/articles/6/735/2013/gmd-6-735-2013.html)は三角形の幾何とC型配置を組み合わせる例です。この図は最適化されたICON格子やその力学コアではありません。発散・勾配・渦度・波の分散の精度は、整合した離散演算子に依存します。

## 接続・ベクトル・図で検証した範囲 {#spherical-interface-checks}

チャート間で成分が異なっても、物理的な接ベクトルは一つです。同一のCartesian座標系で正規直交した接基底を列に持つ行列をE_A、E_Bとすると、

\[
 \boldsymbol{v}=E_A\boldsymbol{u}_A=E_B\boldsymbol{u}_B,
 \qquad \boldsymbol{u}_B=E_B^{\mathsf T}E_A\boldsymbol{u}_A.
\]

この式は正規直交した物理成分用です。非直交座標の共変・反変成分には、対応する計量と双対基底が必要です。継ぎ目で成分配列を二つコピーするだけでは不十分です。有限体積法の共有面では、隣接セルの収支に同じ積分流束を逆符号で使います。重合格子では、重複部分の収支の定義も必要です。両パッチの面積を全て足すと一部を二重に数えます。

幾何テストでは単位半径、立方体面の境界節点の一致、正二十面体格子の辺の接続数と頂点の次数、Eulerの関係、球面三角形面積の合計4πを確認します。決定論的な等面積点サンプルで陰陽格子の被覆と重複も確認しますが、サンプルによる確認は被覆の数学的証明ではありません。再生成は `python scripts/build_spherical_meshes.py` で行えます。[幾何マニフェスト](figures/spherical-meshes.json)に構成、面積統計、ソース・画像のハッシュを記録しています。これらは輸送精度、継ぎ目の保存性、地球流体の波の収束を保証しません。次の検証として、滑らかなトレーサーを全ての継ぎ目を越えて回転させて全質量を測り、平衡した浅水波を格子細分化で比較するのが適切です。

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
