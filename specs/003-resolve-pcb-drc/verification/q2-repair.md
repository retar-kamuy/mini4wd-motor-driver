# Q2端子とPCBの修正記録

正規設計: `hardware/kicad/mini4wd-motor-driver/`。2026-11-12の修正時点。

## 資料と接続

[Vishay Si7137DP 資料](https://www.vishay.com/docs/69063/si7137dp.pdf) p.1による端子は1–3=S、4=G、5–8=D。回路図のネットリストとPCBを照合し、1–3=VBAT、4=GATE_DRIVE、5–8=MOTOR_MINUS、および重複する中央Drainパッド=MOTOR_MINUSであることを確認した。74個のネットリスト対応パッド（重複パッドを含む）は全て一致。機械パッドおよび意図的な未接続パッドは別扱い。

## 修正と検査

- 前回の回路図シンボル修正に続き、作業開始時にはPCB pad 5は既にMOTOR_MINUSで、旧VBATへの接続線は取り除かれていた。
- MCP `open_board`、`delete_trace`、`save_board` で、旧接続に残ったVBATの孤立ビア（47,13 mm）と行き止まり配線2本を削除した。既存の並行するVBAT配線は残した。
- MCP `sync_schematic_to_board` を一時データで確認すると、MCU1 pad 4/5の `/I2C_SDA`・`/I2C_SCL` の先頭スラッシュが欠落した。この同期処理を正規設計へ再適用せず、pcbnewでそれぞれのネット名とQ1/U1のPCB側Datasheet属性を回路図に合わせた。他のパッド接続との差は前記照合で0件。
- `kicad-cli pcb drc --severity-all --all-track-errors --refill-zones --save-board --schematic-parity` の結果は [drc-q2-repair.rpt](drc-q2-repair.rpt): 違反0、未接続0、パリティ不一致0、無効チェックなし。
- `kicad-cli sch erc --severity-all` の結果は [erc-q2-repair.rpt](erc-q2-repair.rpt): エラー0、警告0。ネットリスト出力時のアノテーション警告は別途未解決。
- 検査時のPCB SHA-256: `c6a4986c8ed964493ffa553796c3ffb24a09a53b488ef7e7627080b6e3c0da67`。回路図 SHA-256: `c13f2ae6fa5c6d7490a3a1e792b804807dabae6453733b53c4523c6119e66d39`。

これらはQ2修正時点の結果であり、5 A電流容量、EMC、部品のランド、機構および製造データの妥当性を保証しない。後続の配置・配線変更後に再検査する。Q2シンボルの見やすさは別途確認する。
