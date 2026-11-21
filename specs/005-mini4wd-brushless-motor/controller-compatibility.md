# MCT8316ZR適合確認 — 設計ドラフト

作成日: 2026-11-20。T008/T015の途中成果。実機適合判定は未完了。

## 判明した接続条件

[TI SLVSF18B](https://www.ti.com/lit/ds/symlink/mct8316z.pdf) §6/8.4/8.5/8.3.13を参照。DRVOFFはHighで全FETをHi-Zにし、BRAKEはHighでローサイド短絡ブレーキとなる。SPIは16 bit、MSB first、SCLK idle Low、立下り捕捉（mode 1相当）、nSCSのフレーム間Highは最低400 ns。Hall入力はAVDDを超えず、sleep時は外部センサーから入力へ給電しない構成が必要。

設計方針: SPI開始値は1 MHz、FAULHABER基準候補のPWM開始候補は100 kHz（旧20 kHz案を撤回）。これらは設計選択でありXIAOでの測定値ではない。DRVOFFにドライバ側電源を基準とする外部プルアップ、PWM/BRAKE/nSLEEPに安全な外部バイアスを用意し、MCU無給電時の逆給電も確認する。抵抗値・ゲート論理は回路設計時に確定する。停止時の力学的な停止時間は実測する。

## XIAO端子割付案

[Seeed pin map](https://wiki.seeedstudio.com/xiao_mg24_getting_started/)と既存 `firmware/mini4ai_v358/mini4ai_v358.ino` のPC0/PC1/PC2およびPD5使用箇所を参照。全端子は3.3 Vロジックで扱う設計案。

| XIAO | MCU | 機能案 | 注意 |
|---|---|---|---|
| D0 | PC00 | 電池電圧ADC | 分圧比は電源決定後 |
| D1 | PC01 | 基板NTC | 既存用途を保持 |
| D2 | PC02 | ESC PWM | timer周波数・BLE共存を実測 |
| D3 | PC03 | SPI nSCS | 003のMID_SENSE用途を廃止/置換する必要 |
| D4 | PC04 | ARM_EDGE | Wire既定バスを廃止し、IMU内部バスへ移す必要あり |
| D5 | PC05 | nFAULT | 上記と同じ。pull-upと逆給電評価が必要 |
| D6 | PC06 | BRAKE | UART0を使用しない割付 |
| D7 | PC07 | HOST_INHIBIT | 外部armラッチ/禁止回路への入力。driverのDRVOFFへ直結しない候補 |
| D8/D9/D10 | PA03/PA04/PA05 | SCLK/SDO/SDI | 標準SPI0割付 |
| D13 | PB02 | IMU内部バス専用 | U7 SDAに接続。nSLEEP案を撤回 |
| D14 | PB03 | IMU内部バス専用 | U7 SCLに接続。nFAULT案を撤回 |
| D18 | PD02 | WDI | 底面パッド。FGOUTはテスト点のみ、回転数テレメトリ保留 |
| 内部PD5 | PD5 | IMU電源 | 既存用途を保持 |

D11/D12はSAMD11との接続表示があるため割付対象から外す。D15–D17は基板内flashのSPIへ接続されており予備GPIOから除外する。この案は底面パッドの基板接続を必要とし、通常の左右ヘッダーだけでは成立しない。追加基板でのランド/接続高さ・保守性をT010/T019で評価する。

## モーター別速度スクリーニング

式: 無負荷近似rpm = KV × VM、電気周波数 = rpm × 極対数 / 60。VM=5.0 Vを仮定した算術例（許容電圧の選定ではない）:

| 候補 | KV | rpm近似 | 電気周波数（p=極対数） |
|---|---:|---:|---:|
| MZ704 | 8500 | 42500 | 708.33 × p Hz |
| MZ705 | 5600 | 28000 | 466.67 × p Hz |
| MZ706 | 4100 | 20500 | 341.67 × p Hz |

極対数、最高回転数、センサー遷移の上限、巻線R/L、連続/始動/拘束電流が未確認。計算はコントローラー適合や実回転数を保証しない。

## 解決が必要なゲート

- センサー: ピン配列、電源、出力形式、電気角と三相の対応。京商のセンサー線を一般的なHall配列と仮定しない。
- 電源: モーター許容電圧とドライバ最低4.5 Vの重なり。1S直結を選ばない。2S直結/降圧のどちらも未承認。
- 電流: 8 A peakを連続定格にしない。相電流制限、拘束時間、温度上昇を決める。
- 制御: 底面パッド利用、SPI波形とreadback、PWM周波数、FGOUTイベント量、BLE/IMU同時動作。

回路図・PCBが存在しないためERC/DRC、熱/EMC/SPICE解析は本資料の対象回路では未実施。安全な実機測定後に適合を確定する。

2026-11-21: [駆動禁止回路案](hardware-inhibit-design.md)でwatchdog出力の自動復帰と再armラッチを整理。メーカーnetlistに基づくI/O訂正は下節を参照。nSLEEPによるsleepではSPI設定がリセットされるため、wake後は禁止中に再設定する。

2026-11-20メーカー資料追跡: [manufacturer-evidence.md](manufacturer-evidence.md)に、取得した京商T05取説、KV/JAN、MZ707=80mm、元車体の単4×4本指定と、取得できなかったセンサー配列/電気定格/寸法を記録した。元車体電源をモーター単体の定格や2S直結適合に換算しない。シャーシ対象は003の範囲（FM-A/SFM等除外）を継承する。


## 2026-11-21 メーカーKiCad照合による端子割付訂正

取得した[Seeed公式KiCad ZIP](https://files.seeedstudio.com/wiki/XIAO_MG24/Getting_Start/XIAO_MG24_v1.0_KiCad_260114.zip)をkicad-cliでnetlist化した。出典ハッシュと実ノードは[evidence/xiao-internal-nets.json](evidence/xiao-internal-nets.json)。D13/PB02とD14/PB03はIMUのSDA/SCL、D15–D17は内蔵flashと直結している。これらへnSLEEP/nFAULT/watchdogを割り付ける旧案は不適切のため撤回する。

必要GPIOを確保する配線案として、D4=ARM_EDGE、D5=nFAULT、D18=WDIへ変更する。nSLEEPはGPIOから外し、ロジック電源監視に基づくハードウェアwake（driver側pull-down＋許可時のみHigh、逆給電防止）を検討する。常時awake中もDRVOFFで禁止を維持し、cold start時にSPI再設定する。FGOUTはテスト点に出し、回転数テレメトリは初期必須にしない。D4/D5の外部I2C拡張は使えなくなる。

**残る不一致**: 取得ZIPではU7 SDA=PB02/D13、SCL=PB03/D14だが、[Silicon Labs公式core pins_arduino.h](https://github.com/SiliconLabs/arduino/blob/main/variants/xiao_mg24/pins_arduino.h)ではWire1のSDA=D14、SCL=D13で逆になっている。既存firmwareのWire.begin()はD4/D5既定バスを使用する。従ってIMUドライバのバス選択・実装revisionに応じたSDA/SCL指定を確認するまで、この割付はファームウェア適合済みとしない。core/メーカー資料のどちらかを推測で正解としない。


## 2026-11-21 公開仕様モーターによる前進

[documented-motor-design.md](documented-motor-design.md)でFAULHABER 1218S006Bを詳細設計の基準にした。デジタルHall供給2.5–5.5 V/最大10 mAをAVDD給電案へ、全6状態の通電相をDIR=0へ対応付けた。線間R/L、極数、連続DC-equivalent電流、寸法を取得したため、その項目をXSPEEDの情報待ちで止める必要はない。低電流ILIM精度、100 kHz PWM波形、電源、放熱、機構/調達を引き続き評価する。
