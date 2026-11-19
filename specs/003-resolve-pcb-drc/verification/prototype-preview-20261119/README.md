# 正規試作版の確認用製造出力（2026-11-19）

正規対象は `hardware/kicad/mini4wd-motor-driver/`。PCB SHA-256 **a7aaab20cce23e1311411c16d31d7868e5d10233389f3a2941676cce5c175094**。C105=22µF/10V、R106=33Ω、R107=2.2kΩを反映し、L1向き・昇圧SW/小電流枝・局所GND帰路を改めた。同じ現版の[検査・解析と未保証事項](../return-path-20261119/README.md)を参照する。

- 全チェックERC/DRC/未接続/パリティ0、Ignored checks None。118パッド一致、38部品全F.Cu、82ビア全裏面テント。電力ビア33個0.8/0.4mmは維持。
- [Gerber ZIP](gerber-preview.zip) は8層とExcellon。実ファイル群に対するGerber analyzerは指摘0。上下銅箔・穴・外形を実GerberからSVG/PNGへ描画し目視、B.Mask描画オブジェクト0を確認した。PNGは銅箔と穴・外形だけの表示で、部品実装図ではない。
- [BOM](bom-candidates.csv)28行/38個、[CPL](cpl-front.csv)38行、[IPC](mini4wd-motor-driver.ipc)、[回路図PDF](schematic.pdf)。[CADとの照合](../return-path-20261119/output-correspondence.json)は値・MPN・メーカー・座標・回転・実装面の不一致0。CPLはX=PCB X、Y=−PCB Y、回転はmod360。業者ライブラリの原点/回転補正は未確認。
- `source-sha256.txt`は主/階層回路図、PCB/pro、ローカルsymbol/footprintとlib-tableの20入力。`artifact-sha256.txt`は本ディレクトリの出力。本版の電気接続不変のR107表示位置修正後に回路図PDFと入力ハッシュを更新した。

これは確認用出力であり、PCBA業者への送信・供給/実装受入・発注は未実施。全38品を業者実装する。XIAOヘッダなしcastellated module、Q1ドレイン6個のパッド内ビアの穴埋め/キャップ・平坦性、銅厚/めっき、パネル/fiducial/支持・デパネル、コネクタ張り出しとCPL向きを業者と確認する。裏面テントをビア穴埋め済みと解釈しない。

5A連続・全モーター・全温度・実電源の動作認定ではない。C105実効最小、TPS安定性/起動/負荷過渡、論理電源低下中の動作、Gate/VDS/熱/EMC/無線の未評価範囲を明記し、実機を必要とする測定は試作後の電流制限付き段階評価へ分ける。
