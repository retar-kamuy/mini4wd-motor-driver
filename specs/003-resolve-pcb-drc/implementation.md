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
