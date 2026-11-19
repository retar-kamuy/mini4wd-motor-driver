# Research: Mini 4WD Brushless Motor

**Date**: 2026-11-19  
**Scope**: Resolve planning questions for motor/chassis fit, commutation architecture, battery envelope, safety, and fabrication gates. This is desk research; it does not qualify a motor or prove a design.

## 1. Motor and chassis fit

**Decision**: Do not freeze the motor or motor-mount geometry from the phrase “130 size” or from the Kyosho MZ604 comparison. Select a commercial candidate only after obtaining its drawing and electrical/sensor data, then verify it against one identified stock chassis, gear, and pinion. Allow only the minimum documented chassis work; a custom chassis remains an approval-gated last resort.

**Rationale**: The official Mabuchi FA-130RA-18100 baseline is 20.1 mm diameter × 15.1 mm across flats × 25.0 mm body length, 3 V, 12,300 r/min no-load, 0.15 A no-load current, and 2.10 A stall current. These values describe a brushed comparison motor, not a BLDC candidate. Kyosho’s MZ604 page identifies an 8500KV MINI-Z brushless motor but does not provide the dimensions or electrical/sensor parameters needed to establish fit or controller compatibility. No manufacturer-primary-source drawing in this research proved a commercially available BLDC is a drop-in 130 replacement.

**Alternatives considered**: (a) assume 130 nomenclature means identical can/mount — rejected because the dimensional proof is absent; (b) immediately design a custom chassis — rejected because the user prefers stock chassis; (c) contact/seek an OEM motor — retain only as a later candidate path if commercial motors fail the fit gate, with user approval for any custom solution.

**References**: [Mabuchi FA-130RA-18100 specifications](https://product.mabuchi-motor.co.jp/detail.html?id=10), [Mabuchi dimensions and baseline values](https://product.mabuchi-motor.co.jp/result.html?t=1516059386), [Kyosho MZ604](https://rc.kyosho.com/ja/mz604.html). The [X-Team XTI-2030 product listing](https://www.x-teamrc.com/product/x-team-xti-2030-inrunner-brushless-motor-for-mini-r-c-car/) may be tracked as an investigation lead only; it is not established as a 130-fit candidate or electrically qualified.

## 2. XIAO control platform and BLDC commutation

**Decision**: Preserve XIAO MG24 Sense, BLE, and WebApp as the preferred high-level command/monitoring platform. Start the architecture comparison with a dedicated commutation function (integrated controller IC or separate ESC). Consider direct XIAO phase commutation only after proving accessible timer/pin routing, synchronized complementary outputs and dead-time, fault shutdown, and operation alongside BLE/IMU. The existing 003 single brushed PWM and H-bridge cannot be treated as a three-phase inverter.

**Rationale**: Repository evidence for 003 shows `analogWrite(PWM_PIN, d)` sends one brushed-motor command; the 200 Hz loop is the IMU/rules loop. Silicon Labs' Arduino core has a PWM duty-cycle API, but its generic behavior does not by itself prove six suitable phase outputs, safe dead-time, or robust commutation. The EFR32xG24 timer peripherals include dead-time facilities on applicable instances, but XIAO pad routing and resource contention must be checked. A controller with a speed-command input can retain the current high-level interaction while handling commutation separately.

**Alternatives considered**: (a) direct six-switch PWM controlled by XIAO — possible research path, but unproven timing/pin/safety integration; (b) standalone external hobby ESC — viable fallback if its physical size, signal protocol, reverse/brake behavior, and chassis integration work; (c) integrated controller IC on the new PCB — preferred first comparison for compactness, subject to motor compatibility and thermal/current proof.

**References**: [Seeed XIAO MG24 guide and pin map](https://wiki.seeedstudio.com/xiao_mg24_getting_started/), [Silicon Labs Arduino PWM implementation](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/wiring_analog.cpp), [PWM API](https://github.com/SiliconLabsSoftware/arduino/blob/main/cores/gecko/pwm.h), [EFR32xG24 TIMER reference](https://docs.silabs.com/gecko-platform/5.2.1/platform-peripheral-efr32xg24/timer). These sources establish capabilities/API context, not validation of the selected pin and timer combination.

## 3. Controller speed and motor compatibility

**Decision**: Use electrical speed and motor winding parameters as controller-selection gates; do not select by KV alone. Compute `f_e = mechanical_rpm × pole_pairs / 60` at maximum supply and the motor’s allowed speed, and compare against the controller’s recommended range. Treat advertised peak current as a transient limit, not continuous current.

**Rationale**: TI lists MCF8316A recommended operating ranges of 4.5–35 V motor voltage, 0.006–20 mH motor inductance, 0.006–20 Ω motor resistance, up to 1500 Hz motor electrical speed, and 8 A peak phase current. For illustration only, 8500KV at 8.4 V gives an idealized no-load estimate of 71,400 rpm (1190 rev/s); with two pole pairs this is about 2380 electrical Hz, above that device’s stated 1500 Hz recommended speed. Actual loaded speed, KV convention, pole pairs, and winding values must come from the candidate motor; this calculation does not qualify or reject a motor by itself.

TI also lists MCT8315A as an integrated sensorless trapezoidal driver with up to 3 kHz electrical speed, 4.5–35 V operating supply (40 V absolute maximum), and 4 A peak capability. This makes it an architecture candidate only; its voltage range may not support a low-voltage single-cell pack, and current/thermal/startup fit remains unknown. Sensorless startup behavior under a Mini 4WD gear load must be tested. A sensored motor may improve standstill position knowledge but requires compatible sensors and wiring.

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
