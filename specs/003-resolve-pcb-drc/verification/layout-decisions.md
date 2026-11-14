# 2026-11-14 配置・配線の正規設計への反映

設計対象は `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と同ディレクトリの主回路図・`gate-control.kicad_sch`。KiCad MCP 2.8.3の `open_board` / `save_board`（既存正本を上書きするSave As）で検証結果を正本へ反映し、その正本で再検査した。設計正本は存在しており、`.cache/routing/` は検証・復旧専用である。

**現版の接続検査は合格。製造承認は未完了。** 部品・電流容量・駆動条件・EMCなどの残件は `tasks.md` の未完了項目を引き続き適用する。旧Gerberプレビューは使用しない。

## 検査結果と変更差分

| 項目 | 現版の結果 |
|---|---|
| 正規PCBの全チェックDRC | 違反0、未接続0、回路図パリティ不一致0。銅箔再充填・保存を指定して実行 |
| 正規回路図の全チェックERC | 違反0 |
| 無効化したERC/DRCルール | なし。両レポートのIgnored checksもNone |
| 回路図XMLとPCBのネット照合 | 113パッド一致、不一致0 |
| 実装部品 | 35個、全てF.Cu側 |
| 外形中心線の寸法 | 55.0 × 21.0 mm |
| 板厚・銅層数 | 1.6 mm、2層 |
| ビア | 65個、全65個の裏面テント指定を確認 |
| ビア径／穴径 | 0.8/0.4 mmが25個、0.6/0.3 mmが40個 |

根拠は [drc-layout.rpt](drc-layout.rpt)、[erc-layout.rpt](erc-layout.rpt)、[layout-audit.json](layout-audit.json)、[layout-netlist.xml](layout-netlist.xml)、[layout-hashes.json](layout-hashes.json)。パッドの照合は電気ネットの一致を意味し、メーカー端子番号・ランド寸法の確認完了を意味しない。

変更前は36部品のうち追加15部品が基板外、DRC4件・未接続41件だった（PCB SHA-256 `aa62637dd855d570e9222f3cdd1a64f21809354251ec14df9e9078ea15cd79a9`）。今回、追加部品の基板外仮置きを解消して再配置・再配線した。C4を整理したため35部品・113パッドとなった。以前の36部品・115パッドの記録は当時の版に対する検査記録である。

## 配置と配線

- J1は左端 `(5.55, 10.5)` mm・270°、J2は右端 `(49.45, 10.5)` mm・90°。嵌合方向を外側へ向けた配置。メーカー図面による嵌合・保持タブ・禁止領域の確認はT025/T026に残る。
- XIAOの中心は `(19.5, 10.5)` mm。Q1/Q2、ドライバ、昇圧回路を右側へ配置した。部品数追加による外形の拡大はない。
- VBAT・GND・MOTOR_MINUSの主経路は1.5～2.0 mm幅で先に配線し、25個の0.8/0.4 mmビアを使用する形状を固定して信号を配線した。FETの端子付近には0.6～1.2 mm幅の短い接続がある。ネット内の0.2 mm配線には検出・電源分岐も含まれるため、ネット名だけで5 A経路と判定しない。
- 全セグメント・ビアの現版の位置と幅は [layout-power-routing.csv](layout-power-routing.csv)。並列ビアの実際の電流分担、局所狭窄、製造銅厚・めっき・温度を含む5 A評価はT018に残る。
- 最初の全ネット0.2 mmの自動配線結果は接続検査専用とし、正本には採用しなかった。主電流経路を固定した結果を採用した。
- [Freerouting v2.0.1](https://github.com/freerouting/freerouting/releases/tag/v2.0.1)をJava 21で実行。`--gui.enabled=false --api_server.enabled=false --usage_and_diagnostic_data.disable_analytics=true` を指定し、サンドボックス外実行は利用者の明示許可に基づく。配線ファイルは処理終了・非空を確認して取り込み、固定経路が残ることを照合した。
- 実行JARのSHA-256は `d7fd0f63f52e6d74b0fad6715f87ca9f0ffd7109d66b2a584638000270592ecf`。このハッシュ記録は署名検証を意味しない。
- 最後の低電流信号は局所探索で補完し、RESET_OKを引き直した。RESET_OKには0.127 mm、DRIVE_ENABLEには0.15 mmの区間がある。DRC規則の最小幅0.127 mmは変更していない。これらをモーター主経路には使用していない。
- 参照番号・値はF.Fabへ移し、両コネクタの極性表示は新しい位置へ合わせてF.Silkscreenへ配置した。部品の印刷外形は残した。

## 旧バイパス部品の整理

旧U1の撤去後も残っていたC4（100 nF、BOOST_5V–GND）を削除し、追加回路のC104（100 nF）とC105へ役割をまとめた。C105は1 µFから **2.2 µF・16 Vの候補**へ更新した。回路図はMCP `delete_schematic_component`（C4の付属ラベル2個も削除）と `edit_schematic_component`、PCBはMCP `delete_component` / `edit_component` で一致させた。C4へ至る不要なGND枝線2本も除去した。

[TI UCC27524A Rev. C p.24 §8](https://www.ti.com/lit/ds/symlink/ucc27524a.pdf)は100 nFと数µFの並列バイパスを推奨している。これは今回の役割整理と候補容量の根拠であり、C105の型番、DCバイアスによる実効容量、ESR、ドライバまでの往復経路を合格とする根拠ではない。T006/T020/T022で確認する。

[BOMスナップショット](bom-layout-status.json)では35部品・27行。MPN専用プロパティは全27行で未設定。Valueに型番を含む部品もあるが、発注用BOMの完成とは扱わない。過去の製造用BOM/CPLは更新していない。

## 残る設計・検証事項

1. Q2の低電圧NiMH条件、監視器・ドライバの起動停止および3.3 V喪失時の安全状態、実際のゲート切替条件（T019）。NiMH・アルカリ対応は設計対象であり、全電圧条件での動作保証は未完了。
2. ゲート往復経路と昇圧ループの短縮・帰路・連続GND領域。現版の配線総長はGATE_N 26.409 mm、GATE_P 22.3136 mm、SW_BOOST 12.6396 mm。接続検査が0件でも、TIの短いループ・近接配置の推奨を満たしたと判定しない（T020/T022/T023）。
3. 部品MPN・ランド・定格・調達、1 oz仮定の電流／熱評価、コネクタの機械条件。パッド内に置いた電力ビアの充填・はんだ吸い込み・マスクの扱いも製造先との照合が必要。裏面テント指定だけでは解決しない。
4. 今回は回路図／PCBアナライザ、相互解析、EMC、熱、SPICE、Gerber解析、ライフサイクル確認を再実行していない。過去の結果をこの版へ流用しない。最終版の統合検証と製造データ生成はT031～T035に残る。

## 再検査

リポジトリルートからWSL/Linuxのshで実行する。保存後にCADが変わった場合は、ハッシュと全結果を更新する。

```sh
kicad-cli pcb drc --exit-code-violations --severity-all --all-track-errors \
  --refill-zones --save-board --schematic-parity \
  --output specs/003-resolve-pcb-drc/verification/drc-layout.rpt \
  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
kicad-cli sch erc --severity-all --exit-code-violations \
  --output specs/003-resolve-pcb-drc/verification/erc-layout.rpt \
  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch
/usr/bin/python3 tools/pcb/audit_connectivity.py \
  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb \
  specs/003-resolve-pcb-drc/verification/layout-netlist.xml \
  specs/003-resolve-pcb-drc/verification/layout-audit.json
```

回路図を変更した場合は、照合前に `kicad-cli sch export netlist --format kicadxml` でXMLも作り直す。
