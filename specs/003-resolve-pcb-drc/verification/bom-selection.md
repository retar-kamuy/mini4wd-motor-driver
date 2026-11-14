# 部品候補台帳（照合途中）

回路図の22実装品を元BOM候補と対応させた一覧。型番・定格・ランド・実装可否・供給の確認前であり、発注用BOMではない。回路図のMPNとManufacturer属性も未反映。

| 参照 | 回路図の値 | メーカー候補 | MPN候補 | 出典 | 状態 |
|---|---|---|---|---|---|
| C1（旧CIN） | 10uF 10V | Murata | GRM188R61A106MAALD | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |
| C2（旧COUT1） | 22uF 10V | Murata | GRM188R61A226ME15D | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |
| C3（旧COUT2） | 22uF 10V | Murata | GRM188R61A226ME15D | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |
| C4（旧C_BYP） | 0.1uF 10V | Murata | GRM155R61A104KA01D | https://www.ti.com/lit/ds/symlink/ucc27511.pdf | 候補。定格・ランド・供給未照合 |
| D1（旧D_FLY） | SS54-HF | Comchip | SS54-HF | https://www.comchiptech.com/admin/files/product/SP-JB023%20SS54-HF%20Thru.%20SS520-HF%20RevA.pdf | 候補。定格・ランド・供給未照合 |
| D2（旧D_XIAO） | SS14-E3 | Vishay | SS14-E3/61T | https://www.vishay.com/doc?88746= | 候補。定格・ランド・供給未照合 |
| J1 | Micro-Fit 3.0 B+/B- | Molex | 43650-0214 | https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/436/43650/436500414_sd.pdf | 候補。定格・ランド・供給未照合 |
| J2 | Micro-Fit 3.0 M+/M- | Molex | 43650-0214 | https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/436/43650/436500414_sd.pdf | 候補。定格・ランド・供給未照合 |
| L1 | 1.0uH 9A (XEL4030-102ME) | Coilcraft / Würth | XEL4030-102ME（回路図、末尾未確定） / 74438357010（旧BOM） | https://www.ti.com/lit/ds/symlink/tps61023.pdf; https://www.we-online.com/components/products/datasheet/74438357010.pdf | 候補が異なる。フットプリント・発注型番未確定 |
| MCU1 | XIAO MG24 Sense | Seeed Studio | XIAO MG24 Sense（発注型番未確認） | https://wiki.seeedstudio.com/xiao_mg24_getting_started/ | 候補。定格・ランド・供給未照合 |
| Q1 | SiSS64DN-T1-GE3 | Vishay | SiSS64DN-T1-GE3 | https://www.vishay.com/docs/67294/siss64dn.pdf | 候補。定格・ランド・供給未照合 |
| Q2 | SI7137DP-T1-GE3 | Vishay | SI7137DP-T1-GE3 | https://www.vishay.com/doc/?69063= | 候補。定格・ランド・供給未照合 |
| R1（旧R_FB_H） | 732k 1% | Vishay | CRCW0603732KFKEA | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |
| R2（旧R_FB_L） | 100k 1% | Vishay | CRCW0603100KFKEA | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |
| R5（旧R_MID_H） | 22k 1% | Vishay | CRCW060322K0FKEA | https://www.vishay.com/docs/20035/crcw0306e3.pdf | 候補。定格・ランド・供給未照合 |
| R6（旧R_MID_L） | 10k 1% | Vishay | CRCW060310K0FKEA | https://www.vishay.com/docs/20035/crcw0306e3.pdf | 候補。定格・ランド・供給未照合 |
| R7（旧R_NTC） | 10k 1% | Vishay | CRCW060310K0FKEA | https://www.vishay.com/docs/20035/crcw0306e3.pdf | 候補。定格・ランド・供給未照合 |
| R3（旧R_VBAT_H） | 22k 1% | Vishay | CRCW060322K0FKEA | https://www.vishay.com/docs/20035/crcw0306e3.pdf | 候補。定格・ランド・供給未照合 |
| R4（旧R_VBAT_L） | 10k 1% | Vishay | CRCW060310K0FKEA | https://www.vishay.com/docs/20035/crcw0306e3.pdf | 候補。定格・ランド・供給未照合 |
| TH1 | NTCG104BH103JT1 | TDK | NTCG104BH103JT1 | https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG104BH103JT1 | 候補。定格・ランド・供給未照合 |
| U1 | UCC27511DBVR | Texas Instruments | UCC27511DBVR | https://www.ti.com/product/UCC27511/part-details/UCC27511DBVR | 候補。定格・ランド・供給未照合 |
| U2 | TPS61023DRLR | Texas Instruments | TPS61023DRLR | https://www.ti.com/lit/ds/symlink/tps61023.pdf | 候補。定格・ランド・供給未照合 |

## 個別の根拠と残り

- Q1/Q2、U1/U2、D_FLY、J1/J2、L1およびMCU1は [parts-evidence.md](parts-evidence.md) に資料と一部の定格を記載。全端子・ランド・動作条件の照合は未了。
- 各コンデンサは電圧、容量、DCバイアス、温度と実装寸法の確認が必要。抵抗は値、公差、電力、寸法とメーカー型番を確認する。
- J1/J2のケーブルハウジングと端子は基板実装22個の対象外。別の部材として元BOMに残す。
- 在庫、発注可能数とJLCPCBでの組立可否は確認していない。

## 2026-11-14 現版との差分

上表は旧U1を含む選定途中の記録。現版は35部品・27 BOM行で、旧U1とC4は削除済み。分離ゲート回路のU101～U105、R101～R104、C101～C106を使用する。C105は2.2 µF・16 Vの候補に変更し、C104の100 nFと組み合わせる。DCバイアスによる実効容量・型番・ランド・供給は未確定。

[bom-layout-status.json](bom-layout-status.json) は現版回路図を再帰解析した記録。MPN専用欄は全27行で未設定のため、製造用BOMとは扱わない。旧製造BOM/CPLは更新していない。削除・容量変更の理由と現版の検査は [layout-decisions.md](layout-decisions.md)。
