# Candidate Register — Spec 005

This register tracks evidence for selecting a motor, chassis/gear set, battery, and commutation controller. A blank or `unknown` critical field blocks selection and design freeze. Prefer manufacturer documents and measurements; identify source revision/date and confidence for every critical value.

## Decision status

- Detailed-design baseline: **FAULHABER 1218S006B, standard digital Hall**; sourcing/vehicle qualification pending. XSPEED remains a comparison pending missing manufacturer data. See [documented-motor-design.md](documented-motor-design.md).
- Chassis scope: **same as 003** — stock chassis excluding front-motor FM-A/SFM types; representative AR/VZ arrangements first, with MA/MS/ME drive compatibility tracked separately. Exact gear/pinion remains unqualified.
- Selected lithium pack: **not selected**
- Provisional first-choice custom-PCB ESC: **TI MCT8316ZR**, sensor commutation + XIAO PWM/SPI; final qualification pending sensor/electrical/mechanical evidence. See [controller-selection.md](controller-selection.md).
- PCB size/outline: **not selected**; measure the usable chassis envelope after placing the selected motor, pack, XIAO, and wiring.

## Motor candidates

| Manufacturer / MPN | Availability/source | Can and mount dimensions | Shaft / pinion | Sensors / wiring | Voltage | KV / max RPM | Pole pairs | Phase R / L | Current limits | Source / confidence | Status |
|---|---|---|---|---|---|---|---:|---|---|---|---|
| Mabuchi FA-130RA-18100 (brushed reference only) | Manufacturer product catalog | Ø20.1 × 15.1 × 25.0 mm | Verify for comparison | Brushed; 2 terminals | 3 V nominal | 12,300 r/min no-load | N/A | N/A | 0.15 A no-load; 2.10 A stall | [Mabuchi](https://product.mabuchi-motor.co.jp/result.html?t=1516059386), high confidence for listed values | Reference only; not a BLDC candidate |
| Kyosho MZ704 XSPEED 85 | [Kyosho product page](https://rc.kyosho.com/en/mz704.html) | Drawing/can dimensions and mount details not published on product page | Shaft diameter/projection unknown; user expects a fitted gear adapter if the shaft is smaller than the Mini 4WD pinion bore | Sensored brushless family per [MR-04 EVO2 manual](https://www.kyosho.com/jpn/support/instructionmanual/mini-z/pdf/32890-32891-32892-MR-04EVO2.pdf); sensor pinout/levels unknown | Unknown | 8500 KV | Unknown | Unknown | Unknown | Manufacturer confirms model/KV; electrical/mechanical detail incomplete | Primary candidate; MZ704 lot/replacement status must be checked against [Kyosho support notice](https://rc.kyosho.com/ja/blog/post/support_mr04_20250312) |
| Kyosho MZ705 XSPEED 56 | [Kyosho product page](https://rc.kyosho.com/en/rccar/miniz/mz705.html) | Drawing/can dimensions and mount details not published on product page | Shaft diameter/projection unknown; user expects a fitted gear adapter if the shaft is smaller than the Mini 4WD pinion bore | Sensored brushless family per [MR-04 EVO2 manual](https://www.kyosho.com/jpn/support/instructionmanual/mini-z/pdf/32890-32891-32892-MR-04EVO2.pdf); sensor pinout/levels unknown | Unknown | 5600 KV | Unknown | Unknown | Unknown | Manufacturer confirms model/KV; electrical/mechanical detail incomplete | Primary candidate |
| Kyosho MZ706 XSPEED 41 | [Kyosho product page](https://rc.kyosho.com/en/mz706.html) | Drawing/can dimensions and mount details not published on product page | Shaft diameter/projection unknown; user expects a fitted gear adapter if the shaft is smaller than the Mini 4WD pinion bore | Sensored brushless family per [MR-04 EVO2 manual](https://www.kyosho.com/jpn/support/instructionmanual/mini-z/pdf/32890-32891-32892-MR-04EVO2.pdf); sensor pinout/levels unknown | Unknown | 4100 KV | Unknown | Unknown | Unknown | Manufacturer confirms model/KV; electrical/mechanical detail incomplete | Primary candidate |
| X-TEAM XTI-2030 (lead) | Manufacturer product page; contact for details | Listed Ø20 × 30 mm, but same page also says length 30–40 mm | Ø2.0 × 11 mm listed; page also says shaft Ø2.0–2.3 mm | Sensorless; winding delta/star offered | 7–13 V listed | 4800–8600 KV range; max RPM not specified | 2 (12-slot/4-pole description) | Unknown | “Max current” 10–19 A range; conditions not specified | [X-TEAM](https://www.x-teamrc.com/product/x-team-xti-2030-inrunner-brushless-motor-for-mini-r-c-car/), manufacturer source but internal inconsistencies and missing drawing/datasheet | Closest short-can lead so far; not qualified |
| Castle Creations 0808 8200KV (060-0039-00) | Manufacturer product page; listed for sale | Ø20 × 38 mm | Ø2 × 13 mm | Sensorless, 4-pole | 2S LiPo | 8200 KV; max 100,000 rpm | 2 | Unknown | Not listed on product page | [Castle Creations](https://castlecreations.com/products/sensorless-motor-inrunner-0808-8200kv-motor-060-0039-00), manufacturer product data | Too long for a same-size assumption; R/L/current missing |
| Precision Microdrives 720-400 (lead) | Manufacturer datasheet; stocked design | Ø20 × 40 mm | Dual shafts; drawing needed for pinion details | Digital Hall; 8-pin JST PHR-8 | 12 V nominal | 1503 rpm/V; 17,630 rpm no-load | 1 | 1.30 Ω / 0.08 mH | 1.93 A nominal; 10 A stall | [720-400 datasheet](https://www.precisionmicrodrives.com/datasheets/720-400%20-%20720-600%20-%20720-801%20-%20R0-V1.pdf), manufacturer data | Electrical data relatively complete, but long and heavy (56 g); not qualified |

### Documented sensored alternatives — 2026-11-21

1218S006B (Ø12×18 mm, 6 V) is the compact detailed-design baseline; 1226S006B (Ø12×26 mm, 6 V) is the higher-torque fallback. Their standard Hall interface, phase/wire colors, R/L, pole count and mechanical drawings are public. Manufacturer supply route is inquiry-based; actual price, delivery and Japanese availability are not confirmed. Use standard digital Hall, without analog-Hall option K1855. See [evidence and design](documented-motor-design.md).

### Motor screening checklist

- [ ] Manufacturer drawing or measured can/mount geometry; shaft diameter, projection, side(s), and pinion fit
- [ ] Sensor type, sensor pinout, lead exit, and controller compatibility
- [ ] Rated voltage, KV/back-EMF, pole pairs, allowed mechanical/electrical speed
- [ ] Phase resistance/inductance and continuous/peak phase current with test conditions
- [ ] Supplier availability and source document version/date
- [ ] Fit verified against the selected stock chassis without assuming a product-family name means 130 compatibility

## Chassis and gear candidates

| Manufacturer / chassis model / revision | Stock motor layout / gears | Battery bay | Usable PCB envelope / height | USB and service access | Public dimensions / source | Status |
|---|---|---|---|---|---|---|
| Tamiya MA (revision/model to choose) | Midship single-piece chassis; double-shaft motor layout; gear/pinion details need exact kit/manual confirmation | Internal dimensions not published in source reviewed | Unknown; measure assembled chassis | Unknown | 156 × 97 mm overall, 80 mm wheelbase, 2.2 mm ground clearance; [Tamiya chassis catalog](https://tamiya.com/english/cms/mini4wd_chassis_select.html) | Double-shaft comparison only; previous single-shaft suitability statement withdrawn |
| Tamiya MS (revision/model to choose) | Midship direct-drive double-shaft motor; catalog lists 4:1 gear ratio for stated setup | Internal dimensions not published in source reviewed | Unknown; measure assembled chassis | Unknown | 152 × 92 mm overall, 80 mm wheelbase, 4 mm ground clearance; [Tamiya chassis catalog](https://tamiya.com/english/cms/mini4wd_chassis_select.html) | Candidate if a double-shaft motor is selected; not selected |

**2026-11-20 correction**: The [Tamiya catalog](https://tamiya.com/english/cms/mini4wd_chassis_select.html) places both MA and MS in the midship double-shaft category. Investigate VZ/AR rear-motor chassis first for a single-shaft XSPEED; final kit, stock gear interface and fit remain unselected. See [mechanical measurement sheet](mechanical-envelope.md).

Record the fully assembled chassis envelope, not just the exposed chassis tray. Orient the XIAO USB Type-C port outward where possible and check plug/cable access in that orientation; the presence of the port does not itself imply interference. Record only actual blocked or usable clearances. Document any proposed chassis cutting/drilling and why selection/layout cannot avoid it.

## Lithium battery candidates

| Manufacturer / model | Chemistry / cells | Dimensions | Nominal / full / cutoff voltage | Continuous / transient current | Protection and recovery | Connector | Source / status |
|---|---|---|---|---|---|---|---|
| VBpower VBLiPO-360mAh-7.4V | LiPo, 2S | 30 × 15 × 14 mm; 15 g | 7.4 V nominal; full/cutoff not stated on product page | 360 mAh, 60C continuous claim (21.6 A by C-rate calculation); transient limit not stated | Protection/over-discharge recovery not stated; external balance charging | PH 2.0 discharge, JST-XH balance | [VBpower product page](https://www.vbpowerbattery.com/product/vbpower2s360mah60c-upgrade-lipo-battery-for-mini-z); candidate lead only; verify details and fit |
| Spektrum SPMX3002S30 (reference) | LiPo, 2S | 42 × 19 × 12 mm; 17 g | 7.4 V nominal; full/cutoff not listed | 300 mAh; 9 A continuous / 30C | Protection/cutoff not listed; product currently marked unavailable on official page | PH | [Spektrum product page](https://www.spektrumrc.com/product/spektrum-accessories-7.4v-300mah-2s-30c-lipo-battery-ph/SPMX3002S30.html); reference only, unavailable |

**Battery evaluation note**: These are 2S leads, not an approved selection. A 2S LiPo reaches 8.4 V at full charge by standard LiPo cell voltage; verify exact pack limit with its manufacturer before use. Compare both against the motor/controller voltage/current envelope, full chassis battery bay, charger, and protection method. Do not infer that a high C-rate claim supplies an integrated protection circuit.

## Commutation controller candidates

Current priority and final-choice gates are in [controller-selection.md](controller-selection.md). Earlier sensorless rows below are reference comparisons only and do not meet the sensor-use requirement.

| Device / architecture | Supply range | Electrical speed | Motor R/L | Phase-current evidence | Sensing/startup | Stop/brake and faults | Source / status |
|---|---|---|---|---|---|---|---|
| TI MCT8316ZR (current first choice) | 4.5–35 V | Hall timing/speed qualification pending | Motor compatibility pending | 8 A peak; continuous capability requires thermal design | Analog/digital Hall-based 120° commutation; XSPEED sensor pinout/type/phase mapping unknown | PWM + SPI configuration/diagnostics, DRVOFF and nFAULT; system semantics pending | [TI datasheet](https://www.ti.com/lit/ds/symlink/mct8316z.pdf), 7×5 mm IC; provisional first choice, not qualified |
| BLHeli family (legacy BLHeli / BLHeli_S; investigation candidate) | Depends on ESC hardware | Depends on firmware target and ESC hardware | Firmware target/hardware dependent | Power stage dependent | XSPEED sensor signals are required for commutation. Upstream repository describes sensorless ESC firmware; only qualifies if a compatible sensor-input fork/modification is found and validated. | Define from exact ESC firmware target, command protocol and power stage | [bitdump/BLHeli repository](https://github.com/bitdump/BLHeli/tree/master) contains BLHeli, BLHeli_S, and BLHeli_32 code; README describes sensorless ESC code. Candidate status is conditional; no sensor-capable target identified yet |
| BLHeli_32 (separate family branch) | Depends on ESC hardware | Depends on firmware target and ESC hardware | Firmware target/hardware dependent | Power stage dependent | XSPEED sensor signals are required; no support established from cited upstream source | Verify exact target | Same repository; README describes 32-bit MCU firmware and closed-source status. Included for evaluation only if sensor input support is demonstrated |
| TI MCF8316A (comparison only) | 4.5–35 V recommended | Up to 1500 Hz recommended | 0.006–20 Ω; 0.006–20 mH | 8 A peak | Sensorless FOC; motor tune/start validation required | Check full datasheet for bus/brake/fault response | [TI datasheet](https://www.ti.com/lit/ds/symlink/mcf8316a.pdf); not selected |
| TI MCT8315A (comparison only) | 4.5–35 V operating | Up to 3 kHz electrical | Verify detailed datasheet range | 4 A peak, not continuous | Sensorless trapezoidal; startup/load validation required | Has configured stop/fault features; check system behavior | [TI datasheet](https://www.ti.com/lit/ds/symlink/mct8315a.pdf); not selected |
| XIAO-generated commutation | Board logic supply | Must be demonstrated for selected motor | Motor dependent | Requires separate power stage | Verify timer/pin routes, synchronized PWM/dead-time, fault shutdown and BLE/IMU concurrency | Firmware and hardware fail-safe require proof | Not selected |
| Sensored external ESC/controller | Device dependent | Device dependent | Device dependent | Device dependent | Must accept and use XSPEED position sensor signals for commutation and fit the chassis | Verify signal, reverse, brake, and failsafe behavior | Required fallback if BLHeli cannot consume sensors; specific hardware not selected |

## Change log

| Date | Change | Evidence / decision |
|---|---|---|
| 2026-11-19 | Initial register | Planning research; no motor, chassis, pack, or controller selected |

メーカー資料追跡（2026-11-20）: [manufacturer-evidence.md](manufacturer-evidence.md)。MZ704/705/706のKV/JANとMZ707=80mmを確認。元車体の単4×4本指定はモーター単体定格の代用にしない。
