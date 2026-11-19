# Solによる電流・ゲート回路の第一段階評価

記録日: 2026-11-15。正規設計は `hardware/kicad/mini4wd-motor-driver/`。業者未選定・発注数量可変、全基板部品の業者SMT実装を前提とする。本段階は設計途中であり、発注可能の判定ではない。

## 実施した変更

KiCad MCP 2.8.3の `edit_schematic_component` でQ1、Q2、U2、U101～U105の8品にMPN・Manufacturer・SelectionStatusを追記した。U103の総合ロジック資料URLをSN74LVC1G32データシートへ、U104のURLをUCC27524Aデータシートへ訂正した。候補品は選定・調達・電気評価未完了であることをSelectionStatusに記した。

同じ8品の28属性をPCBにも反映した。MCPの任意PCB属性編集APIがないため、`tools/pcb/sync_board_metadata.py` で局所変更候補を作成し、MCP `open_board` / `save_board` で正規PCBへ反映した。MPN・Manufacturer・SelectionStatus・Datasheet以外の全S式を同期前と比較して完全一致した。全パッド、I²Cを含むネット名、UUID、配線・ビア、配置・図面は変更していない。全面 `sync_schematic_to_board` は実行していない。差分と一致判定は [metadata-sync.json](sol-motor-stage/metadata-sync.json)。

MCPのSave Asが、候補にプロジェクト設定が存在しない場合に正規 `.kicad_pro` を既定値で書き換える副作用を検出した。親側のLuna Git担当がHEADの `.pro` SHA-256と同期前の変更なし状態を照合したため、同一SHA-256のキャッシュから復旧した。復旧後SHA-256は `b45ff3ffb2cd60255fbebd5003f734b688c7f039a4a8e7bfefa4b957977899f2`。上書き後設定・復旧候補・差分・復旧根拠は [記録](sol-motor-stage/pro-recovery-candidate.json) に保存した。ルールを緩和したり除外を追加したりせず、元の設定に戻した。補助スクリプトは以後、元 `.pro` を候補へコピーしSHA-256を記録する。

## 実際に確認できた数値

- 回路図解析は35品・27 BOM行。上記8品にMPNを記したが、全品のBOM選定・供給・PCBA受入は未完了。
- `tools/pcb/evaluate_motor_stage.py` をngspiceで実行した。仮定した電源1.8/2.4/3.2 V、電池抵抗0.05/0.2 Ω、モーター抵抗0.05/0.2/0.5 Ω、インダクタンス10/100 µHの36ケースで、静止ロータRLモデルの電流ピークは2.52504～28.35371 A、24ケースが5 Aを超えた。解析解との差の最大値は約0.001275%。入力値は測定値ではなく、全モーターの上限や定格を決める根拠ではない。ベンチ・ログ・JSONを `sol-motor-stage/` に保存した。
- LTC6994のNDIV=1の全温度静的精度±6.2%とRSET=499 kΩ±0.5%を組み合わせると、遅延は9.98 µs nominal、約9.314～10.652 µs。IC・ゲートの伝播遅延やジッタまで含む実スイッチのデッドタイム保証ではない。[ADI資料 Rev.C pp.3–5](https://www.analog.com/media/en/technical-documentation/data-sheets/699412fb.pdf)。NDIV=1に別DIV設定の精度を流用しない。
- 25°Cの単純な5 A導通損失は、Q1の2.86 mΩ（VGS=4.5 V）で0.0715 W、現Q2の3.9 mΩ（VGS=−2.5 V）で0.0975 W。温度上昇・実装熱抵抗・切替損失は含まない。現Q2はVGSの大きさが2.5 V未満になる条件のRDS(on)最大値が保証されていない。[Q1資料](https://www.vishay.com/docs/67294/siss64dn.pdf)、[Q2資料](https://www.vishay.com/docs/69063/si7137dp.pdf)。
- 候補DMP2008UFGの取得PDFにはVGS=−1.8 Vで13 mΩ、5 Aなら単純損失0.325 Wが記載される。ただし取得資料は2014年のAdvance Informationであり、現行供給・最新保証・異なるPowerDI3333-8ランドとの適合未確認のため置換は適用していない。

## 残件と次の設計判断

1. T017: J1/J2、Q1/Q2、D1の接続経路をメーカーの実端子・極性・ランドと最後まで照合する。両MOSFET同時ON時はモーターを通らないVBAT–GND短絡となり、D1では防止できない。
2. T018/T038: 仮定した感度解析を実モーターの負荷包絡と混同しない。電池・モーター抵抗、起動時間、PWMキャリア、実基板の銅厚・狭窄・ビア分担を確定して電流と熱を評価する。
3. T019: Q2の低電圧定格、3.3 V/5 Vの電源順序、監視器・ENABLE・ロジックの無保証電圧域、最小パルスと実ゲートの重なりを評価する。理想論理で重なり0だった既存結果だけでは閉じない。
4. T039: 既存VBAT/MID/NTC監視をモーター電流の高速保護とみなさない。実際の負荷範囲と部品の過渡定格に対し、電流検出・制限/停止、入力短絡保護などの方式と閾値・時間を決めてから回路へ反映する。未証明の保護回路を本段階で追加していない。

## 検査の状態と限界

本段階で回路図/PCB解析器と上記36ケースのngspice感度解析を実行した。属性同期・元プロジェクト設定の復旧後、KiCad 10.0.8で正規設計を再検査した。

| 検査 | 結果と根拠 |
|---|---|
| 全重大度ERC | エラー0・警告0・無効チェックなし。[erc-metadata.rpt](sol-motor-stage/erc-metadata.rpt) |
| 全重大度DRC・全配線・銅箔再充填・回路図パリティ | 違反0・未接続0・Footprint errors 0・無効チェックなし。[drc-metadata.rpt](sol-motor-stage/drc-metadata.rpt) |
| 再出力XMLと全パッドネット比較 | 113パッド一致、不一致0。[connectivity-metadata.json](sol-motor-stage/connectivity-metadata.json) |
| 形状・実装面・裏面ビア | 55×21 mm・板厚1.6 mm・2銅層・35品全てF.Cu側・65ビア全て裏面テント指定を維持。同上 |
| 正規CAD・検査成果物の版 | [hashes-metadata.json](sol-motor-stage/hashes-metadata.json)。PCB SHA-256 `9a80c9646bf08f6803e79dfa157b7b7942aab570a7cec6d3d0a79a22b7fac519` |

実行コマンドは `kicad-cli sch erc --severity-all --exit-code-violations`、`kicad-cli pcb drc --severity-all --all-track-errors --refill-zones --schematic-parity --exit-code-violations`、`kicad-cli sch export netlist --format kicadxml`、`/usr/bin/python3 tools/pcb/audit_connectivity.py`。入力は全て正規パスで、出力は本書からリンクした `sol-motor-stage/`。検査は元設定の復旧後に順次実行した。

実機測定、MOSFETメーカーSPICEモデルを使ったゲート過渡、EMC・熱の最終統合解析、Gerber/BOM/CPL、業者DFMは未実施。T017～T019、T038/T039のチェック状態を完了へ変更していない。属性・接続検査の合格は電気的安全性や発注可能性の判定ではない。

メーカーPDFは正規プロジェクトの `datasheets/` に9件保存した。ADIとMolexは取得がタイムアウトし、Comchip PDFは直アクセスがPDF以外へ転送されたため、全資料のローカル取得完了ではない。Seeed公式のXIAO KiCad資産はキャッシュへ取得済みで、正式ランド採否とアンテナ周囲の配置評価は後続とする。
