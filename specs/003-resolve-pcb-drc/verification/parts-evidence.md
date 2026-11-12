# 部品資料の照合（調査途中）

対象: `hardware/kicad/mini4wd-motor-driver/`。値欄は候補を表し、メーカーと発注型番の確定・フットプリント認定を意味しない。基準ハッシュは [design-baseline.md](design-baseline.md)。

## 部品数

元の `hardware/rev1/manufacturing/bom.csv` は 23 行、数量合計 27。内訳は基板実装 21、ケーブルハウジング 2、圧着端子 4。元 BOM の基板実装行に XIAO モジュールは存在しないが、回路図には MCU1 があるため、現行は 21 + 1 = 22 個。旧仕様の 24 個はこの BOM から導けず、根拠未確認の数値である。これだけで元設計との差分が全て解消したとは言えない。ケーブル部品は PCB の部品数に混ぜない。

## 調査済み項目と残り

| 対象 | 現在の候補・資料 | 結果と残作業 |
|---|---|---|
| Q1 | Vishay SiSS64DN-T1-GE3、[資料 67294](https://www.vishay.com/docs/67294/siss64dn.pdf) p.1 | 30 V N MOSFET、PowerPAK 1212-8S。回路図内 Datasheet が別の SiS454DN を指す不一致を確認。回路図とPCB側の資料URLは訂正済み。端子とランド照合が必要。 |
| Q2 | Vishay SI7137DP-T1-GE3、[資料 69063](https://www.vishay.com/docs/69063/si7137dp.pdf) | 端子・ランドと動作時のゲート電圧、損失は要照合。 |
| J1/J2 | Molex 43650-0214、[製品図](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/436/43650/436500414_sd.pdf) | 図面の表に 43650-0214 を明記。43645 と嵌合時は基板端から 10.16 mm 以内、金属タブ近傍に露出配線・ビア禁止。実寸と基板の照合は未了。 |
| MCU1 | Seeed [XIAO MG24 Sense](https://wiki.seeedstudio.com/xiao_mg24_getting_started/) | 外形 21 × 17.8 mm。外部電源から 5V 端子へはダイオードが必要。ランドと端子の照合は未了。 |
| U1 | TI UCC27511DBVR、[UCC27511資料](https://www.ti.com/lit/ds/symlink/ucc27511.pdf) | 4.5–18 V動作。回路図とPCB側の資料URLはUCC27511資料へ訂正済み。出力・ピン・デカップリングの詳細要照合。 |
| U2 | TI TPS61023DRLR、[TPS61023資料](https://www.ti.com/lit/ds/symlink/tps61023.pdf) | 起動最低電圧は 1.8 V、動作入力 0.5–5.5 V。全電池条件と負荷、ピンとレイアウトは未検証。 |
| L1 | 現回路図 XEL4030-102ME、元 BOM Würth 74438357010 | 異なる候補である。[Coilcraft製品表](https://www.coilcraft.com/en-us/products/power/high-voltage-inductors/xel/xel4030/) に XEL4030-102MEC、1 µH、Isat 9 A、Irms 8.4 A（20°C上昇）の掲載。回路図の文字列だけでは発注型番末尾を確定できない。現ランドと発注型番を照合すること。 |
| D_FLY | Comchip SS54-HF、[資料](https://www.comchiptech.com/admin/files/product/SP-JB023%20SS54-HF%20Thru.%20SS520-HF%20RevA.pdf) pp.1,4 | 40 V、平均整流 5 A、SMA。5 A の条件付き定格は本基板での連続許容を意味しない。ランド・パルス損失を照合する。 |
| 抵抗・コンデンサ・TH1・D_XIAO | 元 BOM に候補型番あり | 値とフットプリントの照合、許容差、DC バイアス、供給と実装可否は未了。 |

全 22 個の回路図の MPN・Manufacturer 属性が空。出典の候補を確認せずに製造用 BOM に転記しない。

## アノテーション警告

KiCad 10.0.8 の `kicad-cli sch export netlist` は「schematic has annotation errors」を出すがネットリストは生成された。ERC 0 とは別の警告であり、原因の断定や参照番号の一括変更はしていない。参照番号の形式、シートインスタンス、回路図と基板の対応を調査する。

## 重大: Q2 5番パッドの誤接続

[Si7137DP データシート](https://www.vishay.com/docs/69063/si7137dp.pdf) p.1 は 1–3 = Source、4 = Gate、5–8 および放熱部 = Drain と定義する。基準PCBを pcbnew で列挙すると、Q2 pad 1–3 は VBAT、4 は GATE_DRIVE、**5 は VBAT**、6–8 および中央パッドは MOTOR_MINUS。物理部品の Drain 5 番と 6–8 番は内部で同一であり、実装すると VBAT と MOTOR_MINUS の意図しない短絡経路を作る。一般的なDRCと回路図パリティ0件では、このメーカー端子との不整合を検出できない。

対応には回路図側の Q2 の端子定義、PCBの pad 5 接続および関連配線を一体で修正し、実部品端子・ネット・パッドを再照合する必要がある。Q2の回路図・PCB側の修正および検査結果は [q2-repair.md](q2-repair.md) を参照。旧版のGerberプレビューは製造・実装に使用しない。
