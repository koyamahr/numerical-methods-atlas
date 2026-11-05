# 二重Mach反射

2次元理想気体Euler方程式で、壁に反射するMach 10衝撃波を計算します。[Woodward・Colella（1984）](https://doi.org/10.1016/0021-9991(84)90142-6)に関連するテストで、現代の実装参照としてNASAの[LAVAチュートリアル](https://www.nas.nasa.gov/LAVA/unst_docs/tutorials/double_mach/double_mach/)があります。

![256×64格子、1次HLLとSSPRK2で計算した二重Mach反射の密度・等高線](figures/double-mach.png)

## 方程式と初期状態 {#equations-and-initial-states}

gamma=1.4、領域[0,4]×[0,1]、保存状態U=(rho,rho u,rho v,E)、E=p/(gamma−1)+rho(u²+v²)/2を使います。初期衝撃波は底壁のx=1/6で交わり、壁と60度です。

\[
x_s(y,0)=\frac16+\frac{y}{\sqrt3}.
\]

左の衝撃波後方状態は(rho,u,v,p)=(8,8.25sqrt(3)/2,−4.125,116.5)、右の未擾乱状態は(1.4,0,0,1)です。上流音速が1なので、法線伝播速度10がMach 10に対応します。

初期セル値はセル中心が衝撃波のどちら側かで決め、切断セル平均を厳密積分しません。移動する入射衝撃波線は、

\[
x_s(y,t)=\frac16+\frac{y+20t}{\sqrt3}.
\]

です。これらの状態は法線方向の移動Rankine–Hugoniot関係を満たし、テストは法線(sqrt(3)/2,−1/2)、速度10を使います。

## 境界と離散化 {#boundary-conditions-and-discretization}

左は衝撃波後方状態、右はゼロ勾配流出です。底面のx<1/6は後方状態を供給し、残りの壁では法線運動量を反射します。上面はx_s(1,t)で両状態を選び、SSPRK2の各段階では対応時刻の境界を使います。

区分一定有限体積、Davis型の最小・最大音響速度を使う2波HLL、非分割流束発散で計算し、刻みは、

\[
\Delta t=C\left[\frac{\max(|u|+c)}{\Delta x}
+\frac{\max(|v|+c)}{\Delta y}\right]^{-1}.
\]

で制限します。表示計算はNx=256、Ny=64、delta x=delta y=1/64、C=0.4、終了時刻0.2、811ステップです。最終最小密度1.4、最小圧力1.0は、この計算の実測診断であって一般的な正値性定理ではありません。

## 再現と確認 {#reproduce-and-inspect}

```bash
python -m numart.cli run double-mach --n 64 --cfl 0.4 --output outputs/double-mach
```

`--n`はNyを定め、Nx=4Nyです。`solution.npz`、`run.json`、`double-mach.png`を保存します。ギャラリーには[計算記録](figures/double-mach-run.json)と[保存状態配列](figures/double-mach.npz)があり、qの形状は(Nx,Ny,4)、x・yはセル中心です。記録には生成時のソースハッシュと作業ツリー状態を含めます。

## 図が示す範囲 {#what-the-figure-establishes}

図は計算した入射・反射波形を密度と30等高線で示します。**1次空間再構成は意図的に拡散的**で、高解像度PPMや適応計算の細い壁面ジェットと巻上がりは解像しません。厳密終了時刻解、格子収束、原論文の図の数値化比較は含みません。

テストでは同一状態流束、周期一様状態、入射波跳躍、移動上面・反射壁、粗格子の許容状態を確認します。反射模様全体の収束は示しておらず、高次再構成、細分化、独立参照コード比較が必要です。

強衝撃波不安定性は[カーバンクル](carbuncle.md)へ進んでください。このHLL図からRoe実装の安定・不安定は判断できません。

## 反射の時間発展を見る {#watch-the-reflection-evolve}

[保存状態の動画](#/movies?case=double-mach)は同じ256×64計算の密度・圧力を示します。実際の物理時刻、ステップ、固定色範囲、フレーム検査、MP4出力があります。[標本化の定義](movies.md)を参照してください。
