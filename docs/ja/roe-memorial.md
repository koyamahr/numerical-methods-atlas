# Philip L. Roeを偲んで

Philip Lawrence Roeは2026年4月26日、87歳で逝去しました。Michigan大学の[Ken Powellによる追悼](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/)は、航空宇宙、数値計算法、教育、数値流体の共同体への貢献を記しています。

このアトラスは、方程式の波構造を保ちながら実用的な計算をどう実現するか、という中心的な問いを通してRoeを偲びます。

## 数値流体力学における歩み {#a-career-in-computational-fluid-dynamics}

1962〜1984年にRoyal Aircraft Establishmentで勤務し、Cranfield教授を経て1990年にMichigan大学へ移り、2021年に退職しました。大学の[公式退職記録](https://regents.umich.edu/files/meetings/09-21/2021-09-VI-Roe.pdf)はこの経歴と2015年AIAA Fluid Dynamics Awardを記します。追悼にはBram van Leer、Ken PowellとKeck CFD研究室を設立した役割もあります。

## 今も実行できる1981年の考え方 {#the-1981-idea-still-executable}

[Approximate Riemann solvers, parameter vectors, and difference schemes](https://doi.org/10.1016/0021-9991(81)90128-5)で、非線形界面問題を注意深く構成した線形化系へ置き換える方法を発展させました。定義的条件のひとつは、

\[
\widetilde A(U_L,U_R)(U_R-U_L)=F(U_R)-F(U_L).
\]

です。整合性と利用可能な特性分解によって、保存的流束差を認識できる波へつなぎます。[Sod比較](benchmarks.md)とホームの選択画面で、教育用1次元Euler実装をHLL、HLLC、Rusanovと比べられます。

本コードは音響エントロピー平滑化を使う独立した教育用実装で、Roeの元ソフトウェアではありません。彼の名が示す研究は、この展示ひとつよりはるかに広いものです。

## 敬意としての正確さ {#precision-as-a-form-of-respect}

近似ソルバーを有用にする波解像度は、エントロピー、低密度、多次元衝撃波への精密な問いを促します。[カーバンクルの章](carbuncle.md)は別々の数値課題として後の研究へつなぎます。限界を学ぶことも貢献の理解の一部です。

後の関心にはActive Fluxがあり、[Michigan MICDEの紹介](https://micde.umich.edu/member/philip-roe/)が大学の出発点になります。ここでは読書の方向で、実装済みではありません。

原典を読み、方程式を確かめ、計算を検証し続けるための招きとして、この解説のRoeノートをその記憶へ捧げます。
