# アノテーション警告の解消

13個の参照番号を標準的な連番へ変更し、回路図とPCBを同期した。旧名は役割の別名として従来資料に残る。

| 旧参照 | 新参照 |
|---|---|
| CIN | C1 |
| COUT1 | C2 |
| COUT2 | C3 |
| C_BYP | C4 |
| D_FLY | D1 |
| D_XIAO | D2 |
| R_FB_H | R1 |
| R_FB_L | R2 |
| R_VBAT_H | R3 |
| R_VBAT_L | R4 |
| R_MID_H | R5 |
| R_MID_L | R6 |
| R_NTC | R7 |

KiCad CLIのネットリスト出力は警告なしで終了。旧参照を対応表で変換すると、変更前後の全ネットの部品・ピン集合は完全一致。PCB全トラック・ビアのUUID、ネット、始終点は一致。現在のPCBでネットリスト対応パッド74個も一致。

全チェック有効のERCは0件（erc-annotated.rpt）、再充填・パリティ付きDRCは違反0・未接続0・パリティ不一致0（drc-annotated.rpt）。最終再配置後に再検査する。

mini4wd-motor-driver.kicad_sch SHA-256: `04db91a2256b6802002da793885789033cbb4754fe40fdf87d0c354610696c0a`

mini4wd-motor-driver.kicad_pcb SHA-256: `298d40dbc5b9ec4fbe00e050c5c0230e8852855644f72e40ce3aaf6ef0ce1ac0`
