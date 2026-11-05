# 年代順のアトラス

年は原著の刊行年です。オンライン公開年、翻訳年、再録年を区別します。
これは代表文献をたどる読書順であり、すべての手法の発明者・優先権を決める年表ではありません。
原論文との対応・未確認事項は [参考文献](references.md) に記載します。

## 古典的な準備：方程式、差分、反復

前進差分・後退差分・中心差分、Euler の時間積分、Fourier 展開、熱伝導、Laplace／Poisson 方程式を準備します。
境界値と境界フラックスを区別してから、Dirichlet・Neumann・Robin を扱います。
これらの数学的起源と、後世の CFD 実装の成立年を同一視しません。

## 1928：CFL と依存領域

Courant–Friedrichs–Lewy。連続問題の依存領域と離散ステンシルの到達範囲を比べます。
線形移流で `C=a Δt/Δx` を変え、必要条件と十分条件を分けて考えます。
[CFL 原論文](https://doi.org/10.1007/BF01448839)、[実験と導出](stability.md)。

## 1947–1950：拡散、陰解法、線形安定性

Crank–Nicolson (1947)、Thomas の三重対角消去（1949 年報告として引用されるが原報は未確認）、
Charney–Fjørtoft–von Neumann (1950) の数値予報における安定性解析。
von Neumann 解析の成立を 1950 年の一論文だけに帰する趣旨ではありません。
拡散数 `r=ν Δt/Δx²`、A 安定性、単調性、陰的線形系を接続します。
[拡散・線形系](elliptic.md)。

## 1954–1961：Lax、Godunov、保存形

Lax (1954) の弱解と差分、Lax–Richtmyer (1956) の同値定理、Godunov (1959)、
Lax–Wendroff (1960)、Rusanov (1961)。
保存形、数値流束、衝撃波速度、数値粘性、分散を学びます。
Lax–Richtmyer の線形収束定理と、非線形保存則の Lax–Wendroff 型の弱解に関する結果は別です。
`method="godunov"` は本実装では近似リーマン流束を使う Godunov 型で、原著の厳密流束の完全再現ではありません。

## 1961–1977：緩和から multigrid、局所多項式と大域基底

Fedorenko (1961)、Reed–Hill (1973)、Gottlieb–Orszag (1977)、Brandt (1977)。
Poisson の反復を「高周波誤差の平滑化」と「低周波誤差の粗格子補正」に分けます。
一方、DG は要素ごとの多項式と境界流束、スペクトル法は大域的な基底を使います。
DG・スペクトル法の解説では、この 1970 年代以前の Galerkin 法や Fourier 法の由来も背景として位置づけます。
[Poisson と multigrid](elliptic.md)、`numart.advection.dg_advection`。

## 1978–1983：共通テストと高解像度流束

Sod (1978)、van Leer (1979) の MUSCL、Orszag–Tang (1979)、Roe (1981)、Harten–Lax–van Leer (1983)。
同じ Sod 問題で、接触面と音響波の解像度を比較します。
MUSCL の初版は minmod + method of lines であり、van Leer の原論文の Lagrange/remap 実装とは異なります。
Orszag–Tang も原著の非圧縮 MHD の研究と、現在の圧縮性テストの正規化を区別します。
[テスト定義](benchmarks.md)、[MHD](mhd.md)。

## 1987–1989：高次化、前処理、磁場制約

Harten ほか (1987) の ENO、Turkel (1987) の低速前処理、Einfeldt (1988)、
Evans–Hawley (1988) の CT、Shu–Osher (1988, 1989)、Cockburn–Shu (1989) の RKDG。
高次補間だけで衝撃波の安定性は保証されません。エントロピー修正と正値性も別の課題です。
Shu–Osher は衝撃波と滑らかな密度波を同時に解くテストとして使います。

## 1991–1996：非定常の反復、低密度、HLLC と WENO

Einfeldt ほか (1991)、Jameson (1991)、Toro–Spruce–Speares (1994)、Liu–Osher–Chan (1994)、Jiang–Shu (1996)。
物理時間と擬似時間、低密度での破綻、接触波の復元、WENO の非線形重みへ進みます。
WENO の始まり (1994) と、初版に実装した WENO5-JS (1996) は分けて表示します。
[前処理と dual time](advanced.md)。

## 2000–2008：多次元の頑健性と制約

Tóth (2000)、Dedner ほか (2002)、Abgrall (2006) の residual distribution の整理、Nishikawa–Kitamura (2008)。
CT／GLM の離散演算子、残差の分配による保存性、rotated-hybrid 流束と carbuncle を扱います。
RD の 2006 年はレビューの刊行年であり、手法の発明年ではありません。

## 現代の検証へ

[NASA の 2D 検証ケース](nasa-2d.md) は、純粋な数値検証と実験との物理検証を分けるための入口です。
歴史アトラスには原論文、現在のデータ入口、実装・検証状態を別々に紐付けます。
