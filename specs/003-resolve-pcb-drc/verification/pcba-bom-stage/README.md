# PCBA BOM・実装ランドの更新候補（2026-11-16）

正規設計は `hardware/kicad/mini4wd-motor-driver`。候補コピーは `.cache/pcba-bom-stage/candidate`。このコピーを設計対象や発注元として扱わない。候補を検証した後、正規プロジェクトへKiCad MCPで反映済み。

## 実行したこと

- KiCad MCP `edit_schematic_component` で未記入19 BOM行/27部品の `MPN`、`Manufacturer`、`Datasheet`、`SelectionStatus` を候補へ追加。
- KiCad CLIでXMLを新規出力、`sync_board_metadata.py`でPCB候補へ108属性同期。`metadata-sync.json` は属性以外の全S式一致を記録する（この時点のメタデータだけの候補）。
- 正規 `.pro` を候補へ複製済み。正規MCP Save As前後に設定ハッシュを再確認した。候補での後続ランド/配置変更はこの108属性差分とは別であり、全S式一致の証拠を流用しない。
- Molexメーカー推奨ランドと現行フットプリントの不一致、XIAO公式ランドとの差を発見。根拠と修正座標は [mechanical-findings.md](mechanical-findings.md)。DRC/ERC/全パッド対応を合格させ、正規に適用して再検査した。

## 選択した未記入部品の候補

| 参照 | メーカー / 発注候補 | 照合条件と残り |
|---|---|---|
| C1 | Murata GRM188R61A106MAALD | 10µF/10V、0603。DCバイアス/温度による実効容量は別途評価 |
| C2,C3 | Murata GRM188R61A226ME15D | 22µF/10V、0603。TPS61023の実効出力容量4µF以上、44µF公称値だけで合格させない |
| C101,C102,C103,C104,C106 | Murata GRM155R61A104KA01D | 100nF/10V、0402。各電源5V以下 |
| C105 | Murata GRM188R61C225KE15D | 2.2µF/16V、0603。UVLO余裕の実測は組立後、部品実効容量評価は組立前 |
| D1 | Comchip SS54-HF | SMA、5A/40V。5Aはメーカー指定温度条件による定格で本基板の連続5A保証ではない |
| D2 | Vishay SS14-E3/61T | SMA、1A/40V、Cathode=1の対応を確認する |
| J1,J2 | Molex43650-0214 | 30µin金メッキ、SMT固定タブ。カスタムランド不一致を修正済み |
| L1 | Coilcraft XEL4030-102MEC | 1µH、XEL4030、末尾Cを含む完全発注型番へ統一。従来のWürth候補と混用しない |
| MCU1 | Seeed Studio102010610 | XIAO MG24 Sense、ヘッダ未装着。castellated業者実装の受入確認が必要 |
| R1 | Vishay CRCW0603732KFKEA | 732kΩ/1%、0603 |
| R2 | Vishay CRCW0603100KFKEA | 100kΩ/1%、0603 |
| R3,R5 | Vishay CRCW060322K0FKEA | 22kΩ/1%、0603 |
| R4,R6,R7 | Vishay CRCW060310K0FKEA | 10kΩ/1%、0603 |
| R101 | Yageo RT0603BRD07499KL | 499kΩ/0.1%、0603、0.1W/25ppm/K。仕様の0.5%以下を満たす精度候補。型番登録とメーカーRT系列資料を照合 |
| R102 | Vishay CRCW0402100KFKED | 100kΩ/1%、0402 |
| R103 | Vishay CRCW04020000Z0ED | 0Ω、0402。CRCWの0Ω用Zコード |
| R104 | Vishay CRCW04022K20FKED | 2.2kΩ/1%、0402 |
| TH1 | TDK NTCG104BH103JT1 | 10kΩ/5%、0402、B定数は既存FW温度換算と照合 |

機械読み取り用の型番とメーカーURLは [selected-candidates.json](selected-candidates.json)。定格の資料元はMurata各型番PDF、[Vishay CRCW](https://www.vishay.com/docs/20035/dcrcwe3.pdf)、[Yageo RT](https://www.yageogroup.com/content/datasheet/asset/file/pyu-rt_1-to-0-01_rohs_l)、[Comchip SS54-HF](https://www.comchiptech.com/admin/files/product/20190806165140.pdf)、[Vishay SS14](https://www.vishay.com/docs/88746/ss12.pdf)、[Coilcraft XEL4030](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xel/xel4030/xel4030-102/)。

## 既存選定済み10行の供給識別メモ

- U101はLTC6994IS6-2#TRMPBF、LCSC C581055。-1は機能が異なるので代替不可。同一-2のTRPBFはリール包装違いだが無断代替しない。
- U104はTexas Instruments UCC27524ADR、JLC C185857。UMW類似品をTI品として扱わない。
- R105/R106はCRCW04024R70FKED/CRCW040222R0FKED。Q1/Q2/U2/U102/U103/U105を含む既存10行は今回の27部品追加で変更しない。
- ここでの登録確認は発注可能在庫、数量、PCBA受入の確認とは別。供給不足は業者調達/同等品承認の手順で閉じ、ユーザーの手はんだへ転嫁しない。

## 正規での最終検査

- `final-erc.rpt` / `final-drc.rpt`: 全チェックERC0、DRC0、未接続0、回路図パリティ0、Ignored checks None。
- `final-connectivity.json`: 新規XMLに対して116パッド一致、不一致0、37部品すべてF.Cu、55×21 mm、1.6 mm、2層。
- `bom-analysis.json` / `bom-candidates.csv`: 29行/37部品、MPN・Datasheet全29行、欠落0。これは調達/実装の業者受入を意味しない。
- `final-cpl.csv`: 全37個の実装座標。部品データベースに対する回転補正は業者プレビューで確認する。
- 新しい版の製造プレビュー、ハッシュと差分レビューは `../final-review.md` に記録する。
