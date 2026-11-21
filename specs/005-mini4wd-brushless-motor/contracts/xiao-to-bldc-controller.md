# XIAO-to-BLDC Controller Interface Contract

**Status**: Planning contract; electrical values and protocol are intentionally unselected until a motor/controller is qualified.

## Purpose

Retain the XIAO MG24 Sense with the current BLE/WebApp as the preferred high-level control path. The XIAO supplies run/speed/stop intent. A dedicated commutation function generates three-phase motor drive. Existing brushed-motor PWM semantics must not be wired directly to phase gates.

The selected motor sensor signals are required as commutation feedback; 1218S006B standard digital Hall is now the detailed-design baseline. The provisional first choice is TI MCT8316ZR on the new PCB; its sensor/electrical/thermal and chassis compatibility is not yet qualified. Codex designs the XIAO firmware and BLE/WebApp control application around PWM speed commands and SPI configuration/diagnostics. See [ESC selection](../controller-selection.md) for alternatives and final selection gates. No BLHeli firmware or DShot dependency is required.

## Signals and behavior to define during G3

| Signal/function | Required contract |
|---|---|
| Speed command | First choice: XIAO PWM duty command to MCT8316ZR. Define frequency, valid range, ramp limits, scaling, and invalid values after motor qualification. This is a duty command; closed-loop speed regulation requires defined FGOUT feedback and host logic. |
| ESC command transport | First choice: SPI for configuration and fault diagnostics, plus PWM/DIR/BRAKE/DRVOFF controls. MCT8316ZR supports 3.3-V logic and up to 5-MHz 16-bit SPI per datasheet; select operating clock and SDO pull-up/interface settings during detailed design. Complete the XIAO pin/timer allocation before schematic freeze. |
| Enable/drive inhibit | Define active polarity, pull state, reset/boot default, and hardware path to force outputs off. Reset or disconnected XIAO must not enable torque. |
| Stop mode | Define separate meanings for coast, controlled deceleration, and electrical brake where supported. Never infer that zero speed command means a safe brake. |
| Motor sensor inputs | Identify sensor type, pinout, logic levels, pull-ups, phase relationship/commutation table, maximum edge rate, filtering, and connector. The selected commutation controller must consume these signals for rotor position feedback. |
| Fault input | Controller fault must be visible to XIAO if supported, with asserted polarity, filtering, latch/clear behavior, and user-visible status. Fault shutdown must not depend only on a software polling loop. |
| Telemetry (optional) | Define available speed/current/voltage/temperature data, freshness, scaling, and failure behavior. |
| Power and ground | Define logic supply source, voltage range, sequencing, common reference, isolation (if any), USB/battery backfeed prevention, and motor-noise return path. |

## Safety semantics

- On boot, reset, brownout, invalid command, or command timeout, drive remains disabled or enters an explicitly validated safe stop state.
- Communication recovery does not restart the motor automatically; a fresh arm/run command is required.
- Current/voltage/thermal controller faults disable drive according to the selected device’s hardware behavior and are reported to the XIAO when possible.
- Brake energy and DC-bus voltage must remain within component and battery limits, including a full or disconnected battery case.
- Command timeout, timeout action, and restart policy are selected from measured vehicle stopping behavior and documented before implementation.

## Values pending selection

XSPEED sensor pinout/supply/type/phase relationship; MCT8316ZR motor voltage/current/speed and thermal qualification; battery configuration; XIAO pin/timer budget; PWM frequency and speed mapping; SPI settings; timeout; enable/fault logic; stop/coast/brake definitions; telemetry; power rails and level shifting. Sensor signals must reach the commutation controller. Use datasheet-defined DRVOFF with a safe power-up bias and verify shutdown across resets; fault reading is not a substitute for hardware shutdown. Finalize from selected documents or measurements and test before schematic freeze.


## 2026-11-20 detailed design draft

See [controller compatibility and pin allocation](../controller-compatibility.md). The provisional design uses D0 battery ADC, D1 NTC, D2 PWM, D3 nSCS, D6 BRAKE, D7 DRVOFF, D8–D10 SPI, bottom pads D13 nSLEEP / D14 nFAULT / D18 FGOUT. D3 replaces the 003 MID_SENSE use; the existing firmware must be adapted before connection. Bottom-pad connection and timer/core/Sense-internal-resource compatibility remain qualification gates.

Proposed host policy (design values, not measured acceptance results):

| State | Drive control | Transition |
|---|---|---|
| BOOT/DISARMED | DRVOFF High, PWM zero, BRAKE Low | Initialize SPI and read back configuration with drive inhibited |
| READY | Same inhibited outputs; valid Hall interface and power required | Fresh explicit arm plus zero command |
| ARMED | BRAKE Low, release DRVOFF only after all gates pass | Fresh RUN command and bounded duty ramp |
| COAST | Assert DRVOFF; PWM zero | Fresh arm required after a timeout/fault |
| BRAKE | PWM zero; BRAKE High with drive enabled, only after brake qualification | Bound duration/current; then disable drive |
| FAULT | DRVOFF High, PWM zero; snapshot fault registers | User clear + healthy inputs + reinitialization + fresh arm |

DRVOFF and BRAKE are distinct: inhibit has priority in the host policy, so a disabled output must not be reported as active braking. An independent watchdog must force drive inhibit if the MCU stops updating. The [hardware inhibit draft](../hardware-inhibit-design.md) proposes TPS3431 plus an arm latch, power supervisor and a driver-side pull-up/sink interface. Exact parts, GPIO allocation and circuit verification remain incomplete. Internal IC protections cover their specified faults and do not prove MCU-stall shutdown.

Initial host parameters for bench qualification: 1-MHz SPI, mode 1, 16-bit MSB-first, 1-µs CS-high gap; 100-kHz PWM candidate for the FAULHABER slotless motor (supersedes the former 20-kHz draft; see AN190 in documented-motor-design.md). Proposed fresh command heartbeat 100 ms and timeout 300 ms; expiry disables drive and disarms. Tune timeout from vehicle stopping distance and BLE/IMU timing before acceptance. A repeated/stale sequence must not refresh the lease. Establish BLE-loss and independent watchdog behavior on hardware before release.

Sensor disconnect behavior must be investigated explicitly: do not assume every invalid Hall state produces a protective fault. Check all input combinations and missing transitions with the selected IC truth table, lock protection and current limits; require safe recovery without automatic restart.

2026-11-21: D7 is provisionally HOST_INHIBIT into the external latch/inhibit circuit rather than a direct DRVOFF connection. WDI and ARM_EDGE require two additional GPIOs, not yet qualified. The draft uses a 200-ms external watchdog (170–230 ms datasheet range) and 50-ms main-loop servicing. It does not guarantee inhibition within 300 ms of the last command: a 300-ms command lease followed by MCU stall can add up to 230 ms before independent inhibition. Final timeout acceptance includes circuit delay and measured stopping distance. nFAULT must not be wired directly to clear without checking DRVOFF/wake-induced Low states.


2026-11-21 pin-budget correction: manufacturer KiCad netlist proves D13/D14 are the IMU bus and D15–D17 the onboard flash SPI. Withdraw the former D13 nSLEEP / D14 nFAULT allocation. Proposed replacement is D4 ARM_EDGE, D5 nFAULT, D18 WDI, hardware-controlled nSLEEP and FGOUT as test point only. Firmware must stop using default Wire D4/D5 and qualify the IMU bus mapping; the official core and schematic disagree on SDA/SCL. See `../controller-compatibility.md` and `../evidence/xiao-internal-nets.json`. This is a proposed contract amendment, not tested firmware.


2026-11-21 clarification integration: BLE loss requires coast (BRAKE Low, assert inhibit/disarm), and communication recovery requires fresh explicit arm. PWM=0 alone is not the safe-stop proof. See [documented motor design](../documented-motor-design.md) for AVDD-referenced push-pull Hall supply, exact wire mapping and six-state commutation comparison. Existing XSPEED unknowns remain specific to that comparison; baseline qualification now tracks FAULHABER supply/cooling/current-limit and vehicle fit.
