# 公開仕様に基づくセンサードモーター設計案

更新: 2026-11-21。ユーザー回答C/B/Aを反映したT008/T009/T014–T016の部分成果。完成車での性能・取付・温度は未検証。

## 基準候補

**FAULHABER 1218S006B（標準digital Hall、K1855なし）を詳細設計の基準候補**とする。XSPEEDは資料待ちの比較候補に残す。これは調達・製造の確定選定ではない。[メーカーeShop](https://eshop.faulhaber.com/en/1218S006B/1218S006B)はAvailable / Delivery time on requestと表示し、問い合わせによる供給経路があるが、日本向け価格・納期・MOQ・在庫数量は未確認。

| 候補 | 機構 | 公称電圧 | 連続電流 / トルク | 特徴・判断 |
|---|---|---:|---|---|
| 1218S006B | Ø12×18 mm、1.2 mm軸、8.3 g | 6 V | 0.663 A DC-equivalent / 0.96 mNm | 小型搭載を優先する基準候補 |
| 1226S006B | Ø12×26 mm、1.2 mm軸、13 g | 6 V | 0.932 A DC-equivalent / 2.13 mNm | トルク余裕を優先する代案、標準缶長との差を要評価 |
| 1628T012B | Ø16×28 mm、1.5 mm軸 | 12 V | 0.829 A DC-equivalent / 2.62 mNm | 電源/長さが増えるため優先度を下げる |

出典: [1218 datasheet](https://www.faulhaber.com/fileadmin/Import/Media/EN_1218_B_FMM.pdf)、[1226 datasheet](https://www.faulhaber.com/fileadmin/Import/Media/EN_1226_B_FMM.pdf)、[1628 datasheet](https://www.faulhaber.com/fileadmin/Import/Media/EN_1628_B_FMM.pdf)。各2026-07-28版。連続値は22°C、指定放熱条件であり樹脂ホルダー内の保証値ではない。

1218S006Bの線間R=3.14 Ω、線間L=35 µH、極対数1、無負荷30,500 rpm、定格18,280 rpm、最高79,000 rpm。巻線上限125°C、環境上限100°C。熱保護と負荷試験が必要。公称値からの計算例は[evidence/documented-motor-calculations.json](evidence/documented-motor-calculations.json)。メーカー値と計算値を混同しない。

## 電気接続案

[AN163](https://www.faulhaber.com/fileadmin/Import/Media/AN163_EN.pdf) Table 3（p.3）を目視確認。1218/1226標準Hallは2.5–5.5 V、最大10 mA、push-pull。Table 6（p.5）に三相とHallの対応がある。**アナログHallのK1855を注文しない。** データシートの例示型番はK1855付きなので取り違えない。

| モーター線 | 色 | MCT8316ZR案 |
|---|---|---|
| Phase A / B / C | brown / orange / yellow | OUTA / OUTB / OUTC |
| Hall A / B / C | green / blue / grey | HPA / HPB / HPC |
| Hall GND | black | AGNDを基準とするセンサー帰路 |
| Hall supply | red | AVDD由来の給電許可回路（3.3 V系） |

AVDDの3.1–3.465 V範囲はHall電源範囲内で、外部負荷30 mAに対しHall上限10 mAを配分する設計案。残り20 mAはそのまま自由に使用せず、プルアップ・安全回路の合計と温度条件を精査する。センサー出力を5 Vで直接HPxへ入れない。睡眠時の逆給電を防ぐためセンサー電源をAVDDと連動し、電源断順序・入力保護も確認する。push-pullなので外付けプルアップを標準実装しない。HNA/HNB/HNCはdigital modeに従い未接続。

FAULHABER CWの全6有効Hall状態とTI DIR=0の通電相は表の上で一致した（JSON参照）。線の色をHall波形図の描画色と混同しない。000/111、センサー断線は正常6状態に含めず、故障評価を行う。

## PWM・電流・電源

[FAULHABER AN190](https://www.faulhaber.com/fileadmin/Import/Media/AN190_EN.pdf)はslotless巻線に40 kHz以上、edge-alignedはその2倍を推奨する。従来20 kHz開始案をこの候補では撤回し、**100 kHz PWM**を評価開始値とする。MCT8316ZRは200 kHzまで対応するが、XIAOのtimer波形・最小パルス・BLE共存は未検証。

AN190の台形転流換算による相RMSの連続目安は0.663×0.82=0.544 A（指定放熱条件）。0.663 Aを相RMSまたは電池電流として設定しない。MCTのcycle-by-cycle peak limitもRMS値とは別であり、ILIM分圧・CSA精度・PWMリップル・低電圧低電流精度を含めて決める。タイヤ拘束を無期限に許容しない。

設計方向は2Sリチウム→外部降圧→VM最大6.0 V、ロジック給電は別途分岐。6.0 Vは公称モーター電圧を超えない設計目標で、buck設定値/許容差/過渡の上限を含む。1S直結は不可。2S直結も採用しない。VM最低4.5 Vを満たす余裕、出力コンデンサ、回生/電源断クランプ、ピーク電流を確定して電源ICを選ぶ。BLE通信喪失ではBRAKE Low、DRVOFF Highとしてcoastし、再armまで保持する。

## 専用ホルダーと残るゲート

1218の缶長18±0.3 mm、直径12±0.03 mm、軸実径1.190–1.193 mm、フランジ基準から先端まで4.95–5.25 mm。M5.5×0.5取付ねじ/Ø6ボスは図面参照。元の130缶と同じ軸中心を保つ二分割ホルダーと軸スリーブを設計する。樹脂だけで定格放熱を仮定せず金属放熱経路も評価する。ピニオンの穴・歯形・軸方向位置は既存ギヤ側の根拠を取得して確定し、圧入荷重をモーターへ伝えない。

残る発注条件: 日本向け見積/供給、車体負荷と連続運転時間、ホルダー/ピニオン位置、電源ICと保護定数、ILIM低電流精度、100 kHz波形、Sense IMUバス不一致、回路図/PCB/ERC/DRC/熱/EMC/実機試験。今回の調査で公開仕様不足の経路を改善したが、完成基板の適合判定ではない。

## 取得資料の同定

PDFは一時領域へ取得し寸法図と表を描画して目視した。汎用IC用の自動抽出キャッシュをモーターへ擬装せず、以下の出典ハッシュを記録する。

| 資料 | SHA-256 |
|---|---|
| EN_1218_B_FMM.pdf | f52f59f5ef1523c49110a1666c41a4401e2b016751f5ed9aa894fe11fd1035f5 |
| AN163_EN.pdf | e1852b3c2e426f5c2f389884f4a061fdf5611f10fc4c02d4cd56a4c2178184c1 |
| AN190_EN.pdf | bdc8883f387513dfe4f60e17d4cf3a004e90fef1aefa2e3e30a32e110d8ea6f1 |
