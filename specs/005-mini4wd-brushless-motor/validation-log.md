# Validation Log — Spec 005

Use one copy/section per hardware revision. Record only performed checks; mark unperformed items `NOT TESTED`. Attach instrument setup, photos, scope traces, logs, and source revision identifiers.

## Revision and configuration

- Design revision / source commit:
- KiCad schematic / PCB revision:
- Firmware revision:
- Motor manufacturer / MPN:
- Chassis / gear set:
- Battery / cell count:
- Controller / commutation architecture:
- Test date / operator:
- Ambient temperature:

## Inspection and mechanical fit

| Check | Setup / tool | Expected limit | Result | Evidence file | Pass / fail / not tested |
|---|---|---|---|---|---|
| Board and component visual inspection | | | | | NOT TESTED |
| Battery polarity and unpowered resistance checks | | | | | NOT TESTED |
| Pinion mesh and shaft retention | | | | | NOT TESTED |
| Chassis, cover, gears, battery, and road clearance | | | | | NOT TESTED |
| XIAO USB Type-C outward orientation and plug/cable access | | | | | NOT TESTED |
| Battery replacement and service access | | | | | NOT TESTED |

## Electrical and firmware checks

| Check | Supply / load / command | Expected limit | Measured result | Evidence file | Pass / fail / not tested |
|---|---|---|---|---|---|
| Logic-only power-up; drive disabled by default | | | | | NOT TESTED |
| No-load phase sequence and low-command rotation | | | | | NOT TESTED |
| Startup / restart under selected gear load | | | | | NOT TESTED |
| Speed changes and stop/coast/brake semantics | | | | | NOT TESTED |
| Command timeout / BLE loss / reset behavior | | | | | NOT TESTED |
| Fault shutdown and explicit recovery | | | | | NOT TESTED |
| Minimum / nominal / maximum approved battery voltage | | | | | NOT TESTED |

## Operating measurements

| Run | Battery voltage | Battery current | Motor speed | Board temperature | Motor temperature | Behavior / notes |
|---:|---:|---:|---:|---:|---:|---|
| 1 | | | | | | NOT TESTED |

## Disposition

- Acceptance criteria met:
- Failures / corrective action:
- Open risks / not-tested behavior:
- Reviewed by / date:
- Release decision: NOT RELEASED


## 2026-11-20 desk-design update

Evidence: TI MCT8316Z SLVSF18B (pin functions, DRVOFF, SPI communication, Hall comparator sections), Seeed XIAO MG24 pin map and Sense IMU example, Tamiya official chassis comparison, existing firmware pin assignments. Findings are documented in `controller-compatibility.md`, `mechanical-envelope.md`, `power-budget.md` and the interface contract.

Results: provisional I/O allocation exists using bottom pads; MA single-shaft suitability corrected; motor sensor/voltage/current, mechanical dimensions and watchdog circuit remain unresolved. No motor connection, current/temperature measurement, CAD ERC/DRC, SPICE, thermal or EMC analysis was performed. There is no BLDC schematic/PCB to analyze yet. No validation acceptance item is marked passed from desk research.

## 2026-11-20 メーカー資料調査

003の対象は単一車種でなくFM-A/SFM等を除く市販シャーシ範囲であることを確認し005へ継承。京商T05取説75ページを取得し、該当図・部品表を目視。出典・取得ハッシュ・既知/未知の区別を `manufacturer-evidence.md` に記録。CAD/ERC/DRC/実測は本作業では行っていない。

## 2026-11-21 駆動禁止回路の机上設計

`hardware-inhibit-design.md`にメーカー資料に基づく外部watchdog＋再armラッチの接続論理を作成。根拠はTI TPS3431 SNVSB66A、SN74LVC1G74 SCES794G、MCT8316Z SLVSF18B。WDOは一定時間後に解除されるため、タイムアウトだけでは再駆動を禁止し続けないこと、DRVOFF/wakeでもnFAULTがLowとなり得ること、sleepでSPI設定が消えることを設計へ反映。信号論理は設計案であり回路実測やIC組合せの検証結果ではない。全実機試験はNOT TESTED、CAD/ERC/DRC/SPICE/熱/EMC/調達在庫確認は未実施。


## 2026-11-21 メーカーKiCad接続照合・発注資料棚卸し

- Seeed公式ZIP SHA-256: `159126a47d860c280e76d52b77adacd6a31bb296a3eee2e62ed887e9772ad70a`。
- 実行: `kicad-cli sch export netlist --format kicadxml`（メーカー原図、一時領域）。終了0、字体代替の通知あり。メーカーnetlistの該当ノード抽出を `evidence/xiao-internal-nets.json` に保存。
- 結果: D13/D14はIMU、D15–D17はflashへ接続。旧制御割付を撤回。公式coreのWire1 SDA/SCLとメーカー原図が逆であり、実装revisionとFW確認を残す。
- 実行: `python3 tools/pcb/audit_spec005_release.py --output specs/005-mini4wd-brushless-motor/evidence/release-inventory.json`。終了2（不足あり）。これは成果物の有無とハッシュだけの棚卸しで、設計検証/DRC/ERC/発注承認ではない。
- 005のCAD、ERC/DRC、SPICE、EMC、熱、通電、在庫照合、業者提出は未実施。


## 2026-11-21 公開仕様の別モーターを基準とする設計

T008/T009/T014–T016部分進捗: `documented-motor-design.md` を追加し、FAULHABER 1218S006B標準digital Hallを詳細設計基準、1226S006Bを高トルク比較とした。公式寸法/電気値、AN163のセンサー電源/配列、全6状態のTI DIR=0との通電相一致を取得・算術照合。AN190の低インダクタンス巻線条件から旧20 kHz案を100 kHz候補に訂正。`evidence/documented-motor-calculations.json`に計算結果を記録。調達価格/納期、取付、ILIM精度、電源IC、実機の駆動/温度が未完了でタスク完了数は増やさない。CAD/ERC/DRC/SPICE/EMC/熱解析は今回未実施。
