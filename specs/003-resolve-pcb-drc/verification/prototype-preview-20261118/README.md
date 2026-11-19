# 正規試作版の確認用製造出力（2026-11-18）

正規対象 `hardware/kicad/mini4wd-motor-driver/`、PCB SHA-256 `e7152f915355a188716b45264bc74a34fdb6dc9e5e9074a5caea470124906ac7`。R1=75kΩ/R2=10kΩ、各0.1%/25ppmの新しい版から生成した。旧プレビューを上書きしていない。

- ERC/DRC/未接続/回路図パリティ0、Ignored checks None。37部品全F.Cu、116パッド一致。
- ZIP: 8 Gerber層とExcellon。Gerber analyzer指摘0。実Gerberからの上下銅箔/穴/外形SVGを生成して目視確認し、B.Mask描画オブジェクト0を確認した。
- BOM29行/37部品、CPL37行とIPC-D-356A。[元CADとの照合](../preorder-electrical-20261118/output-correspondence.json) は値・MPN・メーカー・位置・回転・実装面の不一致0。CPLはX=PCB X、Y=−PCB Y、回転はmod360。業者ライブラリの回転/原点補正は未確認。
- `source-sha256.txt`は主/階層回路図、PCB/pro、ローカルシンボル/ランド・lib-tableの20入力。`artifact-sha256.txt`は保存した出力。銅箔・ドリルは2026-11-17版と同じで、抵抗の値/MPNのみを変更した。

本出力は確認用であり、PCBA業者への送信・受入・発注は未実施。全37品の調達と業者実装、Q1パッド内ビアの穴埋め/キャップ・平坦性、銅厚/めっき、パネル支持/fiducial/デパネル、コネクタ張り出しとCPL向きを業者と照合する。電池面は片面実装で部品なし、75ビア裏面テントを保持する。

電源余裕・MLCC感度・Gate/VDSモデル・EMC/熱の評価範囲と未保証事項は [電気再評価](../preorder-electrical-20261118/README.md) と [最終レビュー](../final-review.md) を参照。実機が必要な波形/温度/走行測定は未実施で、試作後の初回通電から段階的に行う。
