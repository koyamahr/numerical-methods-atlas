# v0.1.0 初版

初版**The Art of Numerical Algorithms**は、歴史的な論文を、方程式、実行可能な教育用実装、テスト図、数値検証へ結び付けました。

## 収録内容 {#included}

- 保存則、安定性、拡散、境界、反復、DG、スペクトル、MHDを扱う英語の歴史アトラスと計算法ノート。
- Euler、浅水、等温、線形移流、拡散、Poisson、平面理想MHDのPythonライブラリとCLI。
- Godunov型・MUSCL有限体積、Rusanov／HLL／HLLE／HLLC／Roe、差分WENO5-JS、モードDG、Fourier伝播。
- Thomas消去、行列不要の共役勾配、赤黒緩和、幾何マルチグリッド。
- 最小の二重時間、行列スケーリング、スカラー残差分配の例。
- 発散診断を区別したCT・GLMの磁場制約実演。
- 英語出典注記付き39項目の文献、生成Markdown・BibTeX、今後のNASA2次元問題集。
- Python3.9・3.12の自動数値検査とギャラリー生成。

## インストールと実行 {#install-and-run}

Python3.9以降が必要です。リポジトリのルートで実行します。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install '.[test]'
python -m pytest -q
python -m numart.cli gallery --output outputs/gallery
```

[読書ガイド](../README.md#reading-guide)と[テスト問題の定義](benchmarks.md)から始めてください。

## 初版の範囲 {#scope-of-this-edition}

独立した教育用モデルで、図は原論文図の再現を主張しません。選定した設定の検証であり、一般的な非線形安定性や正値性を証明するものではありません。有限体積・差分の誤差は点値比較と明示し、CT／GLMは発散演算子名を示します。

NASA流れ、多次元Euler回転ハイブリッド、低Mach PDE前処理、Euler／MHD DG、多次元残差分配は今後の課題です。[ロードマップ](roadmap.md)と、原典の未確認事項を記した[参考文献](references.md)を参照してください。
