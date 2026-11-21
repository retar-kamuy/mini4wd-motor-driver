# Research: Mini 4WD Brushless Motor

**Date**: 2026-11-19  
**Scope**: Resolve planning questions for motor/chassis fit, commutation architecture, battery envelope, safety, and fabrication gates. This is desk research; it does not qualify a motor or prove a design.

## 1. Motor and chassis fit

**Decision**: Do not freeze the motor or motor-mount geometry from the phrase “130 size” or from the Kyosho MZ604 comparison. Select a commercial candidate only after obtaining its drawing and electrical/sensor data, then verify it against one identified stock chassis, gear, and pinion. Allow only the minimum documented chassis work; a custom chassis remains an approval-gated last resort.

**Rationale**: The official Mabuchi FA-130RA-18100 baseline is 20.1 mm diameter × 15.1 mm across flats × 25.0 mm body length, 3 V, 12,300 r/min no-load, 0.15 A no-load current, and 2.10 A stall current. These values describe a brushed comparison motor, not a BLDC candidate. Kyosho’s MZ604 page identifies an 8500KV MINI-Z brushless motor but does not provide the dimensions or electrical/sensor parameters needed to establish fit or controller compatibility.

The manufacturer-listed leads found so far are not drop-in qualified: X-TEAM XTI-2030 lists Ø20×30 mm, 2.0×11 mm shaft, 7–13 V, 4800–8600KV, 10–19 A, sensorless, and 12-slot/4-pole; its page also gives a general length range of 30–40 mm and provides no motor drawing or R/L values. Castle Creations 0808 (060-0039-00) lists Ø20×38 mm, 2×13 mm shaft, 2S LiPo, 8200KV, 4-pole sensorless, and max 100,000 rpm, but no R/L/current data. Precision Microdrives 720-400 has comparatively complete manufacturer datasheet data (Ø20×40 mm, dual shaft, digital Hall, 12 V, 1503 rpm/V, 1 pole pair, 1.30 Ω, 0.08 mH, 1.93 A nominal, 10 A stall) but its 40 mm body and 56 g mass are substantially different from the 25 mm FA-130 can. These are candidate leads only; no dimensions or performance have been matched to a physical chassis/gear set.

**Alternatives considered**: (a) assume 130 nomenclature means identical can/mount — rejected because the dimensional proof is absent; (b) immediately design a custom chassis — rejected because the user prefers stock chassis; (c) contact/seek an OEM motor — retain only as a later candidate path if commercial motors fail the fit gate, with user approval for any custom solution.

**References**: [Mabuchi FA-130RA-18100 specifications](https://product.mabuchi-motor.co.jp/detail.html?id=10), [Mabuchi dimensions and baseline values](https://product.mabuchi-motor.co.jp/result.html?t=1516059386), [Kyosho MZ604](https://rc.kyosho.com/ja/mz604.html), [X-TEAM XTI-2030](https://www.x-teamrc.com/product/x-team-xti-2030-inrunner-brushless-motor-for-mini-r-c-car/), [Castle Creations 0808](https://castlecreations.com/products/sensorless-motor-inrunner-0808-8200kv-motor-060-0039-00), and [Precision Microdrives 720-400 datasheet](https://www.precisionmicrodrives.com/datasheets/720-400%20-%20720-600%20-%20720-801%20-%20R0-V1.pdf).

## 1a. Commercial chassis leads

**Decision**: Keep Tamiya MA and MS as chassis candidates for physical inspection; do not yet select one. MA is a double-shaft midship layout with listed overall 156×97 mm, 80 mm wheelbase, 2.2 mm ground clearance. MS is a direct-drive double-shaft layout, listed 152×92 mm, 80 mm wheelbase, 4 mm clearance, and 4:1 ratio for the catalog’s stated configuration. Manufacturer public specs do not give the assembled motor bay, battery bay, or maximum PCB outline. Those must be measured with a specific kit/chassis revision and motor installed.

**Rationale**: The candidate motor leads differ in shaft count and body length, so chassis choice depends on the motor. MA and MS both require a double-shaft drivetrain. The earlier suggestion of MA for a single-shaft motor was incorrect; VZ/AR rear-motor chassis are the next candidates for inspection. Neither exterior vehicle dimensions nor an illustration establishes internal fit. Mount the XIAO with its Type-C port outward if the chassis opening allows it, then verify plug/cable insertion path; there is no assumed USB interference.

**Reference**: [Tamiya Mini 4WD chassis catalog](https://tamiya.com/english/cms/mini4wd_chassis_select.html).

## 2a. Battery candidate implications

**Decision**: Track 2S LiPo as a promising initial voltage candidate, not an approved pack. Record the VBpower VBLiPO-360mAh-7.4V (30×15×14 mm, stated 360 mAh/60C continuous) as a Mini-Z-sized lead and Spektrum SPMX3002S30 (42×19×12 mm, 300 mAh/9 A continuous) as an unavailable comparison. Confirm exact full/cutoff voltages and pack protection with the seller/manufacturer before use.

**Rationale**: A 2S LiPo full charge is approximately 8.4 V per standard 4.2 V/cell charging convention, enough to exceed the 4.5 V minimum of the TI MCF8316A/MCT8315A comparison devices and within their 35 V recommended maximum. The Spektrum 9 A pack current figure is less than the X-TEAM XTI-2030 listing’s 10–19 A range; this indicates that pack and motor candidate cannot be paired on listed limits without selecting a lower-current winding or different pack. VBpower’s stated 60C × 0.36 Ah implies 21.6 A on paper, but this calculation is not independent verification of pack capability. Chassis fit, protection, and startup current remain unknown.

**References**: [VBpower Mini-Z battery](https://www.vbpowerbattery.com/product/vbpower2s360mah60c-upgrade-lipo-battery-for-mini-z), [Spektrum SPMX3002S30](https://www.spektrumrc.com/product/spektrum-accessories-7.4v-300mah-2s-30c-lipo-battery-ph/SPMX3002S30.html), [TI MCF8316A datasheet](https://www.ti.com/lit/ds/symlink/mcf8316a.pdf), [TI MCT8315A datasheet](https://www.ti.com/lit/ds/symlink/mct8315a.pdf).

## 3a. Preliminary controller comparison against candidate leads

**Decision**: No controller selected. TI MCT8315A is the higher-electrical-speed comparison (up to 3 kHz, 4 A peak); MCF8316A is the FOC comparison (up to 1500 Hz, 8 A peak). Both are sensorless comparison devices and therefore do not meet the now-required use of XSPEED sensor signals unless a separate validated sensor-consuming commutation implementation is added. Their peak current limits are also below the XTI-2030 product page’s 10–19 A maximum-current range, so that lead cannot be assumed compatible. The 720-400’s lower nominal current may fit a small integrated driver in principle, but its 10 A stall current, 12 V nominal voltage, long 40 mm can, and Hall interface still require validation and current limiting. External ESC remains a comparison path only if it consumes the required motor sensors.

**Rationale**: At the Castle 0808’s listed 8200 KV and 2S full-charge 8.4 V, idealized no-load speed is about 68,900 rpm. Four poles mean two pole pairs, yielding about 2.30 kHz electrical frequency, below MCT8315A’s 3 kHz value but above MCF8316A’s 1.5 kHz range. This is a screening estimate, not an operating prediction; load, motor tolerances, and actual speed limit matter. The XTI page does not list max RPM or full motor R/L, so its controller compatibility is unresolved.

**Alternatives considered**: MCT8315A/MCF8316A integrated ICs may simplify a compact board but have limited phase-current headroom for some leads. A commercial external ESC may handle current/startup but must fit the chassis and expose an interface compatible with XIAO. XIAO commutation requires a separate demonstration of timer routing, complementary PWM/dead-time, and fault behavior; it is not selected by default.

## 2. XIAO control platform and BLDC commutation

**Decision**: Preserve XIAO MG24 Sense, BLE, and WebApp as the preferred high-level command/monitoring platform. Start the architecture comparison with a dedicated commutation function (integrated controller IC or separate ESC). Consider direct XIAO phase commutation only after proving accessible timer/pin routing, synchronized complementary outputs and dead-time, fault shutdown, and operation alongside BLE/IMU. The existing 003 single brushed PWM and H-bridge cannot be treated as a three-phase inverter.

**Rationale**: Repository evidence for 003 shows `analogWrite(PWM_PIN, d)` sends one brushed-motor command; the 200 Hz loop is the IMU/rules loop. Silicon Labs' Arduino core has a PWM duty-cycle API, but its generic behavior does not by itself prove six suitable phase outputs, safe dead-time, or robust commutation. The EFR32xG24 timer peripherals include dead-time facilities on applicable instances, but XIAO pad routing and resource contention must be checked. A controller with a speed-command input can retain the current high-level interaction while handling commutation separately.

**Alternatives considered**: (a) direct six-switch PWM controlled by XIAO — possible research path, but unproven timing/pin/safety integration; (b) standalone external hobby ESC — viable fallback if its physical size, signal protocol, reverse/brake behavior, and chassis integration work; (c) integrated controller IC on the new PCB — preferred first comparison for compactness, subject to motor compatibility and thermal/current proof.

**References**: [Seeed XIAO MG24 guide and pin map](https://wiki.seeedstudio.com/xiao_mg24_getting_started/), [Silicon Labs Arduino PWM implementation](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/wiring_analog.cpp), [PWM API](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/pwm.h), [EFR32xG24 TIMER reference](https://docs.silabs.com/gecko-platform/5.2.1/platform-peripheral-efr32xg24/timer). These sources establish capabilities/API context, not validation of the selected pin and timer combination.

## 3. Controller speed and motor compatibility

**Decision**: Use electrical speed and motor winding parameters as controller-selection gates; do not select by KV alone. Compute `f_e = mechanical_rpm × pole_pairs / 60` at maximum supply and the motor’s allowed speed, and compare against the controller’s recommended range. Treat advertised peak current as a transient limit, not continuous current.

**Rationale**: TI lists MCF8316A recommended operating ranges of 4.5–35 V motor voltage, 0.006–20 mH motor inductance, 0.006–20 Ω motor resistance, up to 1500 Hz motor electrical speed, and 8 A peak phase current. For illustration only, 8500KV at 8.4 V gives an idealized no-load estimate of 71,400 rpm (1190 rev/s); with two pole pairs this is about 2380 electrical Hz, above that device’s stated 1500 Hz recommended speed. Actual loaded speed, KV convention, pole pairs, and winding values must come from the candidate motor; this calculation does not qualify or reject a motor by itself.

TI also lists MCT8315A as an integrated sensorless trapezoidal driver with up to 3 kHz electrical speed, 4.5–35 V operating supply (40 V absolute maximum), and 4 A peak capability. It is a reference for electrical constraints, not a qualifying controller under the sensor-use requirement. A candidate controller must accept and use the motor's sensor signals, and its startup behavior under a Mini 4WD gear load must be tested.

**Alternatives considered**: MCF8316A FOC and MCT8315A trapezoidal control are comparison points, not selections. A discrete gate-driver plus XIAO commutation path can be considered if a qualified integrated controller cannot support the candidate motor, but requires substantially more firmware/timing validation.

**References**: [TI MCF8316A datasheet](https://www.ti.com/lit/ds/symlink/mcf8316a.pdf), [TI MCT8315A product data](https://www.ti.com/product/MCT8315A), [TI MCT8315A datasheet](https://www.ti.com/lit/ds/symlink/mct8315a.pdf). Startup/low-speed risks are discussed in [Microchip AN1160](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU16/ApplicationNotes/ApplicationNotes/AN1160-Sensorless-BLDC-Control-with-Back-EMF-Filtering-Using-a-Majority-Function-DS00001160.pdf) and [TI sensorless BLDC overview](https://www.ti.com/document-viewer/lit/html/slvaeg3).

## 4. Battery, braking, and fail-safe behavior

**Decision**: Prefer a lithium-based pack for evaluation, but defer cell count and exact voltage/current limits until motor, controller, and stock-chassis battery space are known. Define off/stop/coast/brake distinctly. Establish a safe response for command loss, brownout, motor lock, overcurrent, overtemperature, and battery protection cutoff before layout.

**Rationale**: Cell count sets the controller’s minimum/maximum supply fit and motor speed. Braking can return energy to the DC bus; a full or disconnected pack may not absorb it. The former 003 board’s 1-cell assumptions and short-brake behavior do not transfer to a three-phase controller. The logic rail for XIAO must be designed for the selected pack, and USB and battery power paths must be checked for backfeed.

**Alternatives considered**: 1S and multi-cell lithium packs remain open candidates pending controller operating voltage, motor data, runtime/current needs, dimensions, protection, and charging arrangement. Battery charging is kept external to the motor board in the initial plan.

## 5. PCB manufacturing route

**Decision**: Use JLCPCB as the first low-volume quote/DFM candidate after design evidence is complete; manufacturing parameters remain unfrozen until the board outline, stackup, and assembly package are known.

**Rationale**: Small board assembly can have panel-size and process constraints; the smallest PCB may require panelization or a different service tier. Confirm the selected tier’s minimum panel dimensions, board thickness/copper, via treatment, component sourcing, assembly side, inspection, and any substitution approval in the actual quote. This planning pass does not claim the design meets JLCPCB rules or is ready to order.

**Alternatives considered**: PCBWay or bare-board-only fabrication with separately assembled prototypes if the final parts, panel format, or assembly process are not supported by the chosen JLCPCB service.

## Remaining evidence required before schematic/layout freeze

- Candidate motor datasheet/drawing and supplier-confirmed availability; measured dimensions if the drawing omits critical fit features.
- One named stock chassis and gear/pinion dimensions, with motor and battery fit documented; minimum chassis modification list.
- Battery pack dimensions, cell chemistry/count, voltage range, continuous/transient current, protection and cutoff behavior.
- Controller datasheet compatibility review, motor sensor/startup method, firmware/command semantics, fault path and safe state.
- Power, current, temperature and braking energy budgets; test limits and stop conditions.
- Board/component arrangement and connector/antenna/USB/road-clearance envelope.

## 6. User-selected Kyosho XSPEED family and BLHeli firmware

**Decision**: Treat Kyosho XSPEED 85 (MZ704, 8500KV), XSPEED 56 (MZ705, 5600KV), and XSPEED 41 (MZ706, 4100KV) as the primary motor candidates. The user's gear-interface approach is an added shaft adapter sized to make the Mini 4WD pinion fit securely; include adapter concentricity, retention, balance/runout, and operating-speed checks. The shaft dimension and motor can/mount measurements still need manufacturer evidence or direct measurement. The BLHeli firmware family is an allowed leading ESC-firmware candidate, including BLHeli and BLHeli_S; exact branch and ESC hardware remain open.

**Evidence and implications**: Kyosho product pages identify the three models and KV ratings ([MZ704](https://rc.kyosho.com/en/mz704.html), [MZ705](https://rc.kyosho.com/en/rccar/miniz/mz705.html), [MZ706](https://rc.kyosho.com/en/mz706.html)). The [MR-04 EVO2 manual](https://www.kyosho.com/jpn/support/instructionmanual/mini-z/pdf/32890-32891-32892-MR-04EVO2.pdf) lists this XSPEED family as sensored brushless motors and identifies the sensor wire accessory; the product pages do not give sensor pinout, signal levels, motor dimensions, shaft diameter, phase R/L, or current limits. The MZ704 SKU also has a Kyosho support notice concerning some units and a replacement process; check lot/replacement status before buying ([notice](https://rc.kyosho.com/ja/blog/post/support_mr04_20250312)).

The user-linked [bitdump/BLHeli repository](https://github.com/bitdump/BLHeli/tree/master) contains BLHeli, BLHeli_S, and BLHeli_32 source trees. Its README describes the ESC code as sensorless; BLHeli and BLHeli_S target Silabs 8-bit MCUs, BLHeli_S is focused on multirotor applications (also usable for planes), and BLHeli_32 targets 32-bit MCUs and is closed source. The user requires the XSPEED motor sensor signals to be used for commutation. Therefore upstream BLHeli does not currently have evidence to satisfy this requirement. Investigate whether a compatible fork or a documented firmware modification can consume the XSPEED sensor signals, including the required MCU, firmware target, sensor electrical interface, commutation logic, and command protocol. Otherwise select a sensored ESC/controller. BLHeli firmware is ESC-side firmware, not a host-side XIAO library.

**Alternatives and remaining gate**: The shaft adapter is the planned way to resolve a smaller shaft/pinion bore mismatch; it does not establish motor-can or stock motor-mount fit. The final motor variant and ESC firmware/hardware must remain unselected until shaft/can data, motor electrical limits, sensor interface, a sensor-consuming ESC implementation, command protocol, and physical chassis fit are documented. A sensorless-only controller is not acceptable for this requirement.


## 7. ESC再選定（2026-11-19）

ユーザーは、Codexによる制御アプリ設計を前提にBLHeli以外のESCを許容した。先行節のBLHeli優先順位を更新し、製造PCBの第一候補を **MCT8316ZR** とする。完成品ESCの比較候補はHOBBYWING MINI28、電流拡張が必要な場合はDRV8306 + 外付けMOSFET。センサー信号を転流に使う要件は維持する。具体的な一次情報、仕様表、アプリの責任範囲、未確認条件は[ESC再選定](controller-selection.md)に記録した。モーター/シャーシ/電池と組み合わせた適合は未確定である。


## 2026-11-20 design preparation

The [controller compatibility draft](controller-compatibility.md) records a concrete host pin budget including XIAO bottom pads, SPI timing and drive/brake logic. The [mechanical measurement sheet](mechanical-envelope.md) corrects the MA drivetrain assumption and defines the motor/adapter/chassis measurements needed for layout. The [power budget draft](power-budget.md) separates battery voltage from motor VM and identifies current, braking and power-path inputs still needed. These are design drafts; T008/T009–T016 are not complete and the evidence gates before CAD remain open.

2026-11-20メーカー資料追跡: [manufacturer-evidence.md](manufacturer-evidence.md)に、取得した京商T05取説、KV/JAN、MZ707=80mm、元車体の単4×4本指定と、取得できなかったセンサー配列/電気定格/寸法を記録した。元車体電源をモーター単体の定格や2S直結適合に換算しない。シャーシ対象は003の範囲（FM-A/SFM等除外）を継承する。


## 2026-11-21 公開仕様の別モーターを基準とする設計

T008/T009/T014–T016部分進捗: `documented-motor-design.md` を追加し、FAULHABER 1218S006B標準digital Hallを詳細設計基準、1226S006Bを高トルク比較とした。公式寸法/電気値、AN163のセンサー電源/配列、全6状態のTI DIR=0との通電相一致を取得・算術照合。AN190の低インダクタンス巻線条件から旧20 kHz案を100 kHz候補に訂正。`evidence/documented-motor-calculations.json`に計算結果を記録。調達価格/納期、取付、ILIM精度、電源IC、実機の駆動/温度が未完了でタスク完了数は増やさない。CAD/ERC/DRC/SPICE/EMC/熱解析は今回未実施。
