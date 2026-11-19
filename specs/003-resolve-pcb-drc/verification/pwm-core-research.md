# PWMキャリアのソース調査（2026-11-19）

`firmware/mini4ai_v358/mini4ai_v358.ino` はPC2に `analogWrite(PWM_PIN, d)` を使い、ソース内でキャリア周波数を明示していない。200 Hzは制御ループでありPWMキャリアではない。

2026-11-19に参照した Silicon Labs公式Arduinoコアのmainでは、[`wiring_analog.cpp`](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/wiring_analog.cpp) の `analogWrite(PinName, int)` は `PWM.duty_cycle_mode` を呼び、[`pwm.h`](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/pwm.h) はduty-cycle modeの既定周波数を1000 Hzと定義している。このため、**そのコア実装を用いる場合**は1 kHzを代表条件として検討できる。

ただし、mainは変更され得る。本リポジトリ内のファームウェアに対して、実際に使用するボードパッケージの版・ビルド結果・キャリア波形をこの調査だけで確定できない。ファームウェアの1 kHz動作を無条件に保証せず、採用するコア版の固定とビルド確認、試作後の波形確認が必要である。PWMが高くなると切替待ち時間中のダイオード損失が増えるため、他のコア・設定での動作は別途評価する。
