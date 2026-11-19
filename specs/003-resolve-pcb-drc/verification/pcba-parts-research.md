# 試作前PCBA部品候補の資料調査

**2026-11-18更新:** R1/R2はYageo RT0603BRD0775KL / RT0603BRD0710KL（75kΩ/10kΩ、各0.1%/25ppm）へ改版。[現BOM](preorder-electrical-20261118/bom-candidates.csv) と [電気評価・未保証事項](preorder-electrical-20261118/README.md) を参照。以下は先行の部品調査で、在庫/実装受入の回答ではない。

2026-11-15。調査中の正規回路・基板は同時に変更され得るため、この一覧は発注用BOMではない。型番、端子、基板形状、設計時の電流・電圧・温度、および業者の供給・実装をすべて満たして初めて採用する。

| 対象 | メーカー資料で確認できた候補 | 根拠 | 未完了 |
|---|---|---|---|
| MCU1 | Seeed Studio XIAO MG24 **Sense**、SKU 102010610 | [Seeed製品ページ](https://jp.seeedstudio.com/Seeed-XIAO-MG24-Sense-p-6248.html) | PCBA用供給形態、アンテナ・底面・パッドと実装可否。SKU 102010590は非Senseのため混同しない |
| L1 | Coilcraft XEL4030-102MEC、1 µH | [メーカー仕様](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xel/xel4030/xel4030-102/)、[JLCPCB登録C5441341](https://jlcpcb.com/partdetail/Coilcraft-XEL4030102MEC/C5441341) | 基板ランド、昇圧条件での飽和・電流・熱、在庫・実装可否。旧BOMのWürth品との違いを記録する |
| D1 | Comchip SS54-HF、DO-214AC SMA | [メーカー資料](https://www.comchiptech.com/admin/files/product/20190806165140.pdf)、[JLCPCB C3757794](https://jlcpcb.com/partdetail/Comchip-SS54HF/C3757794) | 正規ランド・向き、ブレーキ/還流パルスと温度、必要数の在庫。SS54C-HF等の別パッケージと混同しない |
| D2 | Vishay SS14-E3/61T、SMA | [Vishay資料](https://www.vishay.com/docs/88746/ss12.pdf)、[LCSC C47460](https://www.lcsc.com/product-detail/Schottky-Barrier-Diodes-SBD_VISHAY_SS14-E3-61T_SS14-E3-61T_C47460.html) | 電源回路の逆流・順方向損失・ランド・実装可否 |
| C2/C3 | Murata GRM188R61A226ME15#、22 µF・10 V・0603・X5R | [メーカー資料](https://www.murata.com/en-global/api/pdfdownloadapi?cate=luCeramicCapacitorsSMD&partno=GRM188R61A226ME15%23) | 完全発注コード、DCバイアスによる実効容量とTPS61023の安定性、供給・実装可否 |
| Q2 | Diodes DMP2008UFG-7、PowerDI3333-8 | [試作版反映記録](prototype-design-release.md)、[調達記録](q2-sourcing.md) | 電源順序、ブレーキ熱の実機測定、実装先受入 |
| U101 | Analog Devices LTC6994IS6-2#TRMPBF、TSOT-23-6 | [LCSC C581055](https://www.lcsc.com/product-detail/C581055.html)、[ADI資料](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6994-1-6994-2.pdf) | 在庫・業者の調達/実装条件。末尾のTRPBFはリール包装違いで、回路動作が異なる `-1` と混同しない |
| U104 | Texas Instruments UCC27524ADR、SOIC-8 | [JLCPCB C185857](https://jlcpcb.com/partdetail/TexasInstruments-UCC27524ADR/C185857) | 供給数量・工程可否・5 V起動余裕。同名を含む他社製品とメーカーを混同しない |

数値、在庫、業者への部品持込条件は見積時に再確認する。資料ページに掲載された部品番号だけでは業者による実装受入を意味しない。

## C2/C3のDCバイアス調査

[TI TPS61023資料](https://www.ti.com/lit/ds/symlink/tps61023.pdf)の推奨動作条件では、出力コンデンサの実効容量は4～1000 µF。公称22 µFをそのまま使わず、印加電圧・温度・公差を考慮する。資料p.14には実効出力容量40 µFを超える場合のフィードフォワード容量の推奨もある。

[TI技術者の説明](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1258565/tps61022-output-voltage-drops-below-input-voltage)は、GRM188R61A226ME15の5 Vにおける例として約74.7%低下、1個あたり約5.5 µFを示している。2個なら同条件の単純和は約11 µFである。これは典型的な参考であり、メーカーが保証する最小値や、温度・経年・個体差を含む本基板での保証値ではない。Murataの該当品の曲線・実装後の安定性を確認するまで確定しない。
