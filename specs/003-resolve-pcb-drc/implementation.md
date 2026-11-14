# 実装と検証

## 設計対象

正規の `hardware/kicad/mini4wd-motor-driver/` を唯一の作業対象とする。開始時、この場所の回路図は空のひな形で、追跡対象の基板は削除されていた。現存していた設計一式から回路図、基板、プロジェクト設定および必要なシンボルを正規の場所に集約した。既存のローカルフットプリントファイルは保持した。

## 変更内容

- COUT1、CIN、L1、J1、J2の位置を調整し、Courtyard干渉を解消した。
- MOTOR_MINUSの検出分岐、GATE_DRIVE、VBAT_SENSE、BOOST_5V、VBATおよびGNDを引き直し、交差とクリアランス不足を解消した。VBATの対象経路は既存と同じ1.2 mm幅で引き直した。BOOST_5VとU2のGND分岐では、パッド間のクリアランスを確保するため0.35 mmから0.30 mmへ幅を変更した。
- 基板側のフットプリントIDと属性を回路図に合わせた。基板内で使用されていたカスタムフットプリントは `board-routed.pretty` に抽出し、回路図と基板の双方から参照する。抽出は形状の出典を明確にする操作であり、製造元の寸法に対する照合を意味しない。
- 基板のGND銅箔を再充填して保存した。

## 検証結果

以下のコマンドはKiCad 10.0.8で終了コード0を返した。

```sh
kicad-cli pcb drc --exit-code-violations --severity-all --all-track-errors --refill-zones --save-board --schematic-parity --output specs/003-resolve-pcb-drc/drc-report.rpt hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
```

レポートは違反0件、未接続0件、回路図との不一致0件。回路図から出力したネットリストと基板を別途照合し、接続済み73ピンのネット名がすべて一致した。

追加検証で従来無効だった5種類のDRCチェックをすべて有効にし、検出した端点・フィルタの警告を解消した。ERCの無効項目も有効にし、シンボルの同期とI2Cローカルラベルの更新を行った。全チェック有効時の最新結果は `verification/drc-all.rpt` および `verification/erc.rpt` を参照。

DRCは電流容量、熱、EMC、部品の実寸、製造適合性を保証しない。既存仕様の高電流経路幅1.5 mm以上に対して、この設計には1.2 mmのVBAT配線などが残るため、電流容量の設計確認が別途必要である。追加検証では全項目有効のERCとEMCリスク解析を実施した。電流容量、フットプリントのメーカー寸法、EMCの実機適合性は未検証であり、結果と残作業は `verification/remaining-work.md` を参照。

## 2026-11-10 Gerber確認用出力

全チェック有効のDRC、未接続、回路図パリティはいずれも0件。正規基板から `hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/` にGerber 8層とExcellonを出力し、`gerber-preview.zip` を生成した。再生成方法は `hardware/kicad/mini4wd-motor-driver/manufacturing/README.md`。構文解析結果は `verification/gerber-current.json`。製造承認・5 A評価・部品実寸と機構の照合は未完了。

## 2026-11-12: Q2修正と整合性の回復

正規プロジェクトで、Q2 pad 5のMOTOR_MINUS接続、残ったVBATの孤立ビア・行き止まり配線の除去、およびI²Cネット名・Q1/U1資料URLの回路図とPCBの整合を確認した。MCP操作とpcbnewを使用した。銅箔再充填後の全チェック有効DRC、ERCとパリティは0件、ネットリストに対応する74パッドは一致。詳細とハッシュは [verification/q2-repair.md](verification/q2-repair.md)。

これは途中版であり、5 A電流経路、ゲート駆動、部品資料とランド、コネクタの反対端配置、昇圧ループ、EMC、製造データの最終照合は未完了。旧Gerberプレビューは使用しない。

## アノテーション警告の修正

主回路とPCBの参照番号13件を揃えて更新した。ネット集合と配線・ビアの接続は不変で、最新ERC/DRC/パリティ0件。警告なしでネットリスト出力できる。対応表とハッシュは [verification/annotation-repair.md](verification/annotation-repair.md)。

## 分離ゲート回路を正規設計へ反映

主回路にGateControlシート（gate-control.kicad_sch）を追加し、旧U1を削除。Q1 gateはGATE_N、Q2 gateはGATE_Pに分離した。検査用J101と電源フラグは子シートから除いた。gate-studyライブラリを正規プロジェクトへ登録し、MCPでPCBへ15部品を追加。PCBは36部品、115パッドのネット照合に不一致なし。旧GATE_DRIVEのトラック・ビアは除去済み。

追加15部品は基板外の配置待ち領域に仮置き。配置・配線は未完了。ERC 0、DRC 4、未接続41、パリティ不一致0（verification/erc-after-gate-integration.rpt、verification/drc-after-gate-integration.rpt）。以前のDRC 0件を現行PCBの結果として使わない。製造出力の再生成はレイアウト完了後。

## 2026-11-14 正規設計の再配置・再配線

上の仮置き状態から再配置・再配線し、KiCad MCPで正規PCBへ反映した。旧C4を削除し、ゲートドライバのバイパスをC104とC105へ整理。C105は2.2 µF・16 Vの候補に更新した。35部品・113パッドのネット照合一致、正規ファイルのERC・DRC・未接続・パリティ不一致は全て0件。主電流経路には1.5～2.0 mm幅と複数ビアを使用した。板厚1.6 mm、外形55 × 21 mm、2銅層、全65ビアの裏面テント指定を確認した。

検査結果、設計対象、ハッシュ、方法と残件は [verification/layout-decisions.md](verification/layout-decisions.md)。5 Aの電流容量・熱、起動停止、部品・ランド、昇圧とゲートの帰路・EMC、製造適合性の確認は未完了。DRC合格を製造承認とは扱わず、旧製造データも更新していない。
