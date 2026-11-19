# PCBA業者の候補比較

調査日: 2026-11-15、公開資料再確認: 2026-11-17。公開仕様に基づく候補整理で、見積取得・部品適合確認・注文前DFMは未実施。

## この基板に関係する条件

- 2026-11-19に検査した正規レイアウトは55 × 21 mm、2銅層、1.6 mm厚。部品38個は全てF.Cu側で、B.Cuには部品を置かない片面実装である。以後に設計を変更した場合は最新版を再確認する。
- したがって「2層基板」は「両面実装」を意味しない。電池に向ける面をB.Cu側とする搭載方向および車体隙間は別途確認が必要。
- 発注数は固定しない。価格比較は少なくとも2、5、10枚など複数の数量帯で行い、基板・実装・段取り・ステンシル・部品余剰/ロス・送料/税を含む到着総額で比べる。
- BOMには基板1枚当たりの使用数を示す。業者のリール/カットテープ最低購入数や実装ロス分は注文総数と分けて管理する。

## 公開条件の比較

| 業者 | 公開されている少数枚条件 | この基板との適合性 | 留意点 |
|---|---|---|---|
| Seeed Fusion | SeeedのPCBA仕様は注文数量1～8,000枚を掲載。公式PCBAページは在庫部品のOPL調達とXIAOモジュールの供給を案内。 | 一枚の試作と複数枚の両方を見積できる有力候補。XIAO MG24 Senseを含む正確な部品番号、Molex、MOSFET、コネクタの実装可否を個別に確認する。 | 公開ページの「XIAO対応」は特定型番・基板上へのモジュール実装可否を保証しない。モジュールの外形、端子面、向き、供給形態と組立設備への適合確認が必要。 |
| JLCPCB | Economy PCBAは2～50枚、標準PCBAは2～80,000枚。Economyは10 × 10 mm以上、0.8～1.6 mm厚、単面配置。 | 現設計の55 × 21 mm、1.6 mm、F.Cuのみの部品配置はEconomyの公表範囲に入る。部品を標準ライブラリから確保できれば有力な価格候補。 | 注文2枚未満ではEconomy対象外。LCSC調達の在庫・拡張部品料金、XIAOおよびMicro-Fit部品の調達/実装可否を確認。公開能力は注文可否の最終保証ではない。 |
| PCBWay | [現行PCBA能力ページ](https://www.pcbway.com/assembly-capabilities.html)は最小5枚・単板10 × 10 mmからと掲載。[別の能力ページ](https://www.pcbway.com/pcb_prototype/PCB_assembly_Capabilities.html)は50 × 100 mm未満でパネル化が必要と掲載し、[面付け案内](https://www.pcbway.com/pcb_prototype/Panel_Requirements_for_Assembly.html)の最小パネルは50 × 50 mm。 | 部品の調達/実装方法を相談する代替候補。 | 公開ページ間で寸法条件が異なり、55 × 21 mmの単板実装・面付け条件は見積時に確認する。公開する最小数量も注文画面/見積で再確認する。 |

## 現時点の判断

数量の幅とSeeed由来のXIAOを考慮すると、Seeed Fusionを最初の問い合わせ・見積候補にする。2枚以上で全品がLCSC実装可能なら、JLCPCB Economyも同一BOMで比較する。PCBWayはパネル化費用を含めて比較する代替候補とする。正規設計のBOMには全品の候補メーカー・型番を記入済みだが、在庫・調達・実装受入と見積は未確認のため、現時点で最安業者や発注先は選定できない。[BOM候補と照合結果](pcba-bom-stage/README.md)を参照。

見積依頼時は、同一の確定Gerber/BOM/CPLを用い、組立枚数（例: 2、5、10）、全品実装、XIAOモジュール実装可否、Molexコネクタの実装可否、部品不足時の代替承認、初期費用、部品余剰、パネル/ブレークアウェイ条件、検査内容、納期、配送先までの総額を同じ条件で照会する。

## 公式資料

- [JLCPCB PCBA capability](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
- [Seeed Fusion PCBA specification](https://support.seeedstudio.com/knowledgebase/articles/457797-fusion-pcba-specification)
- [Seeed Fusion PCBA product page](https://www.seeedstudio.com/pcb-assembly.html)
- [Seeed XIAO tape-and-reel announcement](https://www.seeedstudio.com/blog/2025/10/24/seeed-studio-xiao-now-available-in-tape-reel/)
- [PCBWay assembly capabilities](https://www.pcbway.com/pcb_prototype/PCB_assembly_Capabilities.html)
