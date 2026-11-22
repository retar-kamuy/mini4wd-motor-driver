# 006 車載初版のJLCPCB提出資料

提出対象は `mini4wd-course-adaptive` の車載ブラシレス基板。初版は趣味用で、同じ基板で通電・停止・低速走行を評価し、必要に応じて改版する。構成と未確定情報は[駆動回路レビュー](../design-review.md)と[検証課題](../../../../specs/006-course-adaptive-mini4wd/verification.json)を参照する。

## 製造データの再生成

リポジトリルートから実行する。初版の配置候補は4層。最終版の層数が変わった場合は `--layers` を実際の値に合わせる。出力先には新規ディレクトリを指定し、回路図・PCB・プロジェクトの版をそろえる。

```sh
python3 tools/pcb/prepare_jlcpcb_006.py --layers 4 --pcba-review out/006-vehicle-r1
```

Gerberとドリルを `jlc-gerbers-review.zip` にまとめる。ERC・DRC、回路図とPCBの照合、CAM解析、BOM、設計と出力のハッシュも保存する。PCBA用に手実装部品を分ける場合は、実際の部品番号を `--manual REF` で指定する。該当部品は `bom-manual.csv` に出力し、JLCPCB用BOMとCPLから除外する。XIAOやモーター・電池のハーネスは部品照合と取付方式を見て扱いを決める。

JLCPCBのプレビューで基板外形、銅層、穴と、PCBA対象の部品・ピン1を照合する。基板厚、銅箔、仕上げは同じ版のPCBと駆動回路の設計値を見積条件に使う。基板の発注条件に実走結果は含めない。[JLCPCB基板製造仕様](https://jlcpcb.com/capabilities/pcb-capabilities/)・[JLCPCB PCBA部品照合](https://jlcpcb.com/help/article/component-matching-guidelines-for-pcba-orders)

## 初回通電と改版

実装後に短絡・極性・駆動禁止の初期状態を確認する。モーター接続前にHallの電源・信号・相順、電池接続前に許容電流を確認する。初回のモーター試験は電流制限付き電源を使い、回転・停止・異常時の温度を記録する。通信喪失時の自然減速と、明示開始まで停止を保持する動作を確認してから走行へ進む。
