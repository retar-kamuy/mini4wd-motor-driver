# 2026-11-17 正規試作版の製造プレビュー

正規設計 `hardware/kicad/mini4wd-motor-driver/`、PCB `514754f50fb7f77a5c9a6e01ddd9abdfa236c773fb83a3be6b39d33ad1f26724` から生成した。同版でERC/DRC/未接続/パリティ0、116パッド一致、BOM29行/37部品、CPL37個。

- `mini4wd-prototype-20261117-preview.zip`: Gerber8層とExcellon。
- `bom-candidates.csv` / `cpl-front.csv`: 全実装品。メーカーMPN29/29。業者ライブラリの回転・調達受入は未確認。
- `source-sha256.txt`: 階層回路図・ローカルライブラリを含む入力20ファイル。
- `artifact-sha256.txt`: このプレビューの成果物ハッシュ。
- `copper-drill-top.svg` / `copper-drill-bottom.svg`: 実Gerberと穴の描画。画面方向は同じ基板座標であり、底面からの鏡像組立図ではない。
- `gerber-top.svg` / `gerber-bottom.svg`: マスク等を含む描画。裏面マスクの描画オブジェクトは0で開口なし。SVG filter対応ビューアで表示する。
- `gerber-analysis.json`: analyzerの指摘0。業者CAM/DFM承認の代替ではない。
- `mini4wd-prototype.ipc`: 同じPCBからのIPC-D-356A出力。

[最終検査と未完了条件](../final-review.md)を参照。全品の業者実装、パッド内ビア処理、パネル枠/支持、必要枚数の調達・見積は未確認。**このプレビューを承認済み発注データとして扱わない。** 2026-11-15の旧プレビューをこの版の製造に使わない。
