# 参考文献（原著の刊行年順）

原論文・書籍の書誌と、実装の照合に使う資料を区別します。DOIが付いていても本文全体の精読・原図再現が完了したという意味ではありません。
公開本文の有無、後年の解説を使った項目、原報未確認は各項目の注記に残します。NASAのケース資料は [別一覧](nasa-2d.md) にまとめています。

このファイルと `references.bib` は `python scripts/build_references.py` で `catalog/references.json` から生成します。

## 1928 · cfl1928

Courant, Richard and Friedrichs, Kurt and Lewy, Hans. **Über die partiellen Differenzengleichungen der mathematischen Physik**. Mathematische Annalen.

[原著の書誌](https://doi.org/10.1007/BF01448839) · [本文または実装参照資料](https://www.stat.uchicago.edu/~lekheng/courses/302/classics/courant-friedrichs-lewy.pdf)

原著1928。sourceは後年の英訳。依存領域とCFLの背景。

## 1947 · crank1947

Crank, John and Nicolson, Phyllis. **A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type**. Proceedings of the Cambridge Philosophical Society.

[原著の書誌](https://doi.org/10.1017/S0305004100023197) · [本文または実装参照資料](https://doi.org/10.1007/BF02127704)

原著1947。sourceは1996年の再録版。初版は線形拡散のtheta法で、原著の非線形問題の再現ではない。

## 1949 · thomas1949

Thomas, Llewellyn Hilleth. **Elliptic problems in linear difference equations over a network**. Watson Scientific Computing Laboratory, Columbia University.

[原著の書誌](https://www.netlib.org/na-digest-html/96/v96n09.html) · [本文または実装参照資料](https://www.netlib.org/na-digest-html/96/v96n09.html)

原報本文・所蔵URLは未確認。Netlibの歴史的記載に現れる書誌を仮登録。原著の直接確認済みとはしない。

## 1950 · charney1950

Charney, Jule G. and Fjørtoft, Ragnar and von Neumann, John. **Numerical Integration of the Barotropic Vorticity Equation**. Tellus.

[原著の書誌](https://doi.org/10.1111/j.2153-3490.1950.tb00336.x) · [本文または実装参照資料](https://maths.ucd.ie/~plynch/eniac/CFvN-1950.pdf)

原著公開版。安定性解析の歴史的文脈。数値予報の再現は未実装。

## 1954 · lax1954

Lax, Peter D.. **Weak solutions of nonlinear hyperbolic equations and their numerical computation**. Communications on Pure and Applied Mathematics.

[原著の書誌](https://doi.org/10.1002/cpa.3160070112) · [本文または実装参照資料](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160070112)

出版社の書誌・概要。弱解、Lax型差分の背景。Lax shock tubeのパラメータの原表照合は未実施。

## 1956 · lax1956

Lax, Peter D. and Richtmyer, Robert D.. **Survey of the stability of linear finite difference equations**. Communications on Pure and Applied Mathematics.

[原著の書誌](https://doi.org/10.1002/cpa.3160090206) · [本文または実装参照資料](https://math.berkeley.edu/~wilken/228B.S07/LaxRichtmyer.pdf)

原著公開版。線形・整合・適切な初期値問題という仮定付きの同値定理。

## 1959 · godunov1959

Godunov, Sergei K.. **A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics**. Matematicheskii Sbornik.

[原著の書誌](https://www.mathnet.ru/eng/sm4873) · [本文または実装参照資料](https://www.mathnet.ru/eng/sm4873)

原著1959、受理1956。初版のgodunovは近似流束を使うGodunov型有限体積法。

## 1960 · lax1960

Lax, Peter D. and Wendroff, Burton. **Systems of conservation laws**. Communications on Pure and Applied Mathematics.

[原著の書誌](https://doi.org/10.1002/cpa.3160130205) · [本文または実装参照資料](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160130205)

出版社の書誌。線形移流のLax–Wendroff実装と保存則の背景。

## 1961 · fedorenko1961

Fedorenko, Radii P.. **A relaxation method for solving elliptic difference equations**. Zhurnal Vychislitelnoi Matematiki i Matematicheskoi Fiziki.

[原著の書誌](https://www.mathnet.ru/eng/zvmmf8014) · [本文または実装参照資料](https://www.mathnet.ru/eng/zvmmf8014)

原著1961、英訳1962。multigridの歴史的入口。

## 1961 · rusanov1961

Rusanov, Vladimir V.. **The calculation of the interaction of non-stationary shock waves with barriers**. Zhurnal Vychislitelnoi Matematiki i Matematicheskoi Fiziki.

[原著の書誌](https://www.mathnet.ru/eng/zvmmf7987) · [本文または実装参照資料](https://www.mathnet.ru/eng/zvmmf7987)

ロシア語原著1961、英訳1962。初版は現代的な局所Lax–Friedrichs/Rusanov流束。

## 1973 · reed1973

Reed, W. H. and Hill, T. R.. **Triangular mesh methods for the neutron transport equation**. Los Alamos Scientific Laboratory.

[原著の書誌](https://digital.library.unt.edu/ark:/67531/metadc1036080/) · [本文または実装参照資料](https://digital.library.unt.edu/ark:/67531/metadc1036080/)

政府報告書の公開資料。初版は1D線形移流のmodal DGで、原著の中性子輸送三角形格子ではない。

## 1977 · brandt1977

Brandt, Achi. **Multi-level adaptive solutions to boundary-value problems**. Mathematics of Computation.

[原著の書誌](https://doi.org/10.1090/S0025-5718-1977-0431719-X) · [本文または実装参照資料](https://www.ams.org/mcom/1977-31-138/S0025-5718-1977-0431719-X/S0025-5718-1977-0431719-X.pdf)

AMS原著の公開先。初版は固定格子の幾何学的V-cycle、原著の適応法全体ではない。

## 1977 · spectral1977

Gottlieb, David and Orszag, Steven A.. **Numerical Analysis of Spectral Methods: Theory and Applications**. SIAM.

[原著の書誌](https://doi.org/10.1137/1.9781611970425) · [本文または実装参照資料](https://epubs.siam.org/doi/abs/10.1137/1.9781611970425.ch2)

出版社の章情報。スペクトル法の代表的体系書。初版は周期Fourier線形問題に限定。

## 1978 · sod1978

Sod, Gary A.. **A survey of several finite difference methods for systems of nonlinear hyperbolic conservation laws**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(78)90023-2) · [本文または実装参照資料](https://faculty.washington.edu/rjl/riemann_book/Euler_equations.html)

DOIは原著。sourceは標準Sodと厳密解の実装資料。原著の全手法・全図の再現ではない。

## 1979 · orszag1979

Orszag, Steven A. and Tang, Cha-Mei. **Small-scale structure of two-dimensional magnetohydrodynamic turbulence**. Journal of Fluid Mechanics.

[原著の書誌](https://doi.org/10.1017/S002211207900210X) · [本文または実装参照資料](https://doi.org/10.1017/S002211207900210X)

原著は非圧縮MHD。現在の圧縮性OTテストの正規化と区別する。

## 1979 · vanleer1979

van Leer, Bram. **Towards the ultimate conservative difference scheme. V. A second-order sequel to Godunov's method**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(79)90145-1) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999179901451)

出版社の書誌・概要。初版はminmod MUSCL+SSPRK3で、原著のLagrange/remapを再現しない。

## 1981 · roe1981

Roe, Philip L.. **Approximate Riemann solvers, parameter vectors, and difference schemes**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(81)90128-5) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999181901285)

出版社書誌・概要、著者公開本文も検索可能。初版は1D Euler+音響固有値の二次entropy smoothing。

## 1983 · hll1983

Harten, Amiram and Lax, Peter D. and van Leer, Bram. **On Upstream Differencing and Godunov-Type Schemes for Hyperbolic Conservation Laws**. SIAM Review.

[原著の書誌](https://doi.org/10.1137/1025002) · [本文または実装参照資料](https://www.ece.uvic.ca/~bctill/papers/numacoust/Harten_etal_1983.pdf)

原著公開版。HLLの背景。初版のhllはDavis型最小最大音響速度を使用。

## 1984 · woodward1984

Woodward, Paul and Colella, Phillip. **The numerical simulation of two-dimensional fluid flow with strong shocks**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(84)90142-6) · [本文または実装参照資料](https://crd.lbl.gov/assets/pubs_presos/AMCS/ANAG/A31984.pdf)

原著公開版。Double Mach Reflection、stepなどの2D展示候補。未実装。

## 1987 · eno1987

Harten, Amiram and Engquist, Bjorn and Osher, Stanley and Chakravarthy, Sukumar R.. **Uniformly high order accurate essentially non-oscillatory schemes, III**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(87)90031-3) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999187900313)

原著1987。1997年再録と区別。ENO単独実装は計画、初版はWENO5-JS。

## 1987 · turkel1987

Turkel, Eli. **Preconditioned methods for solving the incompressible and low speed compressible equations**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(87)90084-2) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999187900842)

出版社書誌・概要。PDE低速前処理は解説・計画で、Jacobi行列スケーリング例と区別。

## 1988 · einfeldt1988

Einfeldt, Bernd. **On Godunov-Type Methods for Gas Dynamics**. SIAM Journal on Numerical Analysis.

[原著の書誌](https://doi.org/10.1137/0725021) · [本文または実装参照資料](https://epubs.siam.org/doi/abs/10.1137/0725021)

出版社の原著書誌・概要。Euler HLLEのEinfeldt型波速。

## 1988 · evans1988

Evans, Charles R. and Hawley, John F.. **Simulation of magnetohydrodynamic flows: A constrained transport method**. The Astrophysical Journal.

[原著の書誌](https://doi.org/10.1086/166684) · [本文または実装参照資料](https://adsabs.harvard.edu/pdf/1988ApJ...332..659E)

原著公開版。初版はCartesian flux-CT型で原著の全構成の再現ではない。

## 1988 · shu1988

Shu, Chi-Wang and Osher, Stanley. **Efficient implementation of essentially non-oscillatory shock-capturing schemes**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(88)90177-5) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999188901775)

出版社の書誌・概要。TVD Runge–Kuttaと流束ベースの構成の背景。

## 1989 · cockburn1989

Cockburn, Bernardo and Shu, Chi-Wang. **TVB Runge-Kutta local projection discontinuous Galerkin finite element method for conservation laws. II. General framework**. Mathematics of Computation.

[原著の書誌](https://doi.org/10.1090/S0025-5718-1989-0983311-4) · [本文または実装参照資料](https://www-users.cse.umn.edu/~cockburn/lecture_notes/DG-4.pdf)

DOIは原著。sourceは著者の後年の講義資料。初版は滑らかな移流DG、TVB limiter未実装。

## 1989 · shu1989

Shu, Chi-Wang and Osher, Stanley. **Efficient implementation of essentially non-oscillatory shock-capturing schemes, II**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(89)90222-2) · [本文または実装参照資料](https://academic.oup.com/mnras/article/512/1/1430/6530656)

DOIは原著。初期条件の実装照合は後続のQuokka論文を使用。原図のデジタイズ比較は未実施。

## 1991 · einfeldt1991

Einfeldt, Bernd and Munz, Claus-Dieter and Roe, Philip L. and Sjögreen, Björn. **On Godunov-type methods near low densities**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/0021-9991(91)90211-3) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/0021999191902113)

出版社の書誌・概要。低密度の正値性の背景。初版の1–2–3設定はToroの標準形。

## 1991 · jameson1991

Jameson, Antony. **Time dependent calculations using multigrid, with applications to unsteady flows past airfoils and wings**. 10th AIAA Computational Fluid Dynamics Conference.

[原著の書誌](https://doi.org/10.2514/6.1991-1596) · [本文または実装参照資料](https://cfd.ku.edu/JRV/Martinelli.pdf)

DOIは原著。sourceは共著者による後年の解説。初版dual timeは線形移流の最小モデル。

## 1994 · hllc1994

Toro, E. F. and Spruce, M. and Speares, W.. **Restoration of the contact surface in the HLL-Riemann solver**. Shock Waves.

[原著の書誌](https://doi.org/10.1007/BF01414629) · [本文または実装参照資料](https://doi.org/10.1007/BF01414629)

出版社書誌・概要。初版HLLCはDavis型波速で原著の全波速推定・WAFではない。

## 1994 · templates1994

Barrett, Richard and Berry, Michael and Chan, Tony F. and Demmel, James and Donato, June and Dongarra, Jack and Eijkhout, Victor and Pozo, Roldan and Romine, Charles and van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM.

[原著の書誌](https://www.netlib.org/templates/templates.html) · [本文または実装参照資料](https://www.netlib.org/templates/templates.html)

著者側公開資料。Jacobi、GS、前処理、multigridの実装資料。

## 1994 · weno1994

Liu, Xu-Dong and Osher, Stanley and Chan, Tony. **Weighted Essentially Non-oscillatory Schemes**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1006/jcph.1994.1187) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/pii/S0021999184711879)

出版社書誌・概要。歴史的WENOの入口。初版の重みはJiang–Shu 1996。

## 1996 · jiang1996

Jiang, Guang-Shan and Shu, Chi-Wang. **Efficient Implementation of Weighted ENO Schemes**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1006/jcph.1996.0130) · [本文または実装参照資料](https://www.ece.uvic.ca/~bctill/papers/numacoust/Jiang_Shu_1996.pdf)

原著公開版。WENO5-JSの流束、smoothness indicator、非線形重みの参照。

## 2000 · toth2000

Tóth, Gábor. **The ∇·B = 0 Constraint in Shock-Capturing Magnetohydrodynamics Codes**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1006/jcph.2000.6519) · [本文または実装参照資料](https://public.websites.umich.edu/~gtoth/Papers/Toth2000_divb.pdf)

著者公開版。CT各種、離散発散の違いの参照。

## 2002 · dedner2002

Dedner, Andreas and Kemm, Friedemann and Kröner, Dietmar and Munz, Claus-Dieter and Schnitzer, Thomas and Wesenberg, Matthias. **Hyperbolic Divergence Cleaning for the MHD Equations**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1006/jcph.2001.6961) · [本文または実装参照資料](https://www.tp4.ruhr-uni-bochum.de/~sw/papers/JCP2002.6961.pdf)

原著公開版。刊行2002とDOI内の2001を区別。初版は固定chのGLM簡略モデル。

## 2002 · leveque2002

LeVeque, Randall J.. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press.

[原著の書誌](https://doi.org/10.1017/CBO9780511791253) · [本文または実装参照資料](https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9)

出版社書誌・概要。保存則・浅水などの実装背景。

## 2006 · abgrall2006

Abgrall, Rémi. **Residual distribution schemes: Current status and future trends**. Computers & Fluids.

[原著の書誌](https://doi.org/10.1016/j.compfluid.2005.01.007) · [本文または実装参照資料](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf)

著者公開版のレビュー。2006は起源年ではない。初版は1D scalar RDのみ。

## 2008 · nishikawa2008

Nishikawa, Hiroaki and Kitamura, Keiichi. **Very simple, carbuncle-free, boundary-layer-resolving, rotated-hybrid Riemann solvers**. Journal of Computational Physics.

[原著の書誌](https://doi.org/10.1016/j.jcp.2007.11.003) · [本文または実装参照資料](https://www.sciencedirect.com/science/article/abs/pii/S0021999107004822)

出版社書誌・概要。2D rotated solverとcarbuncle試験は計画。

## 2009 · toro2009

Toro, Eleuterio F.. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer.

[原著の書誌](https://doi.org/10.1007/b79761) · [本文または実装参照資料](https://doi.org/10.1007/b79761)

出版社書誌。厳密リーマン解と標準double-rarefaction設定の背景。

## 2022 · quokka2022

Wibking, Benjamin D. and Krumholz, Mark R.. **quokka: a code for two-moment AMR radiation hydrodynamics on GPUs**. Monthly Notices of the Royal Astronomical Society.

[原著の書誌](https://doi.org/10.1093/mnras/stac439) · [本文または実装参照資料](https://academic.oup.com/mnras/article/512/1/1430/6530656)

原著の公開ページ§3.1.5でShu–Osherの採用パラメータを照合。quokka本体の再現ではない。
