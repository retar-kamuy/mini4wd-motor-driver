# Implementation Plan: Mini 4WD Brushless Motor

**Branch**: `005-mini4wd-brushless-motor` | **Date**: 2026-11-19 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/005-mini4wd-brushless-motor/spec.md`

## Summary

Develop and prototype a controller for a documented sensored BLDC motor in a stock Mini 4WD chassis. Following clarification, use FAULHABER 1218S006B (standard digital Hall, no K1855) as the detailed-design baseline while XSPEED 85/56/41 remain manufacturer-data-dependent comparisons. See [documented motor design](documented-motor-design.md). Proceed allowing only documented minimum chassis modifications and avoiding a fully custom chassis. Use the motor sensor signals as commutation feedback. Where the motor shaft is smaller than the Mini 4WD pinion bore, design a retaining adapter and validate concentricity and high-speed retention. Retain the XIAO MG24 Sense, BLE, and WebApp as the preferred command platform. Use TI MCT8316ZR as the provisional first choice for the custom PCB ESC, with sensor-based commutation and XIAO PWM/SPI control. Codex designs the control application and firmware; no BLHeli dependency is required. Qualification remains conditional on selected-motor electrical/current-limit compatibility, supply availability and chassis fit; see [controller-selection.md](controller-selection.md). Before fixing the motor variant, battery, controller, firmware, or PCB outline, verify motor dimensions, shaft/sensor interface, and electrical data against a selected chassis and gear train. The existing 003 brushed-motor power stage is not a BLDC inverter.

The plan ends with a validated design package and a manufacturing quote/DFM request. PCB layout and fabrication release remain gated on motor, chassis, battery, commutation, thermal/current, and safety evidence.

## Technical Context

**Language/Version**: KiCad 10 project for the future hardware design; existing XIAO firmware is Arduino C++ and is changed only if the selected interface requires it.

**Primary Dependencies**: KiCad 10 and project hardware-analysis workflow; selected motor, battery pack, BLDC commutation/controller device, XIAO MG24 Sense, and a stock Mini 4WD chassis/gear set. No specific motor/controller has been qualified yet.

**Storage**: KiCad project files and versioned design/validation documents under `hardware/kicad/mini4wd-brushless-motor/` and `specs/005-mini4wd-brushless-motor/`.

**Testing**: Datasheet and drawing checks; schematic/PCB ERC/DRC and manufacturing checks; bench tests with current-limited supply; staged motor/chassis tests for startup, speed command, stop/brake, faults, voltage, current, and temperature. Each check is tied to the same design revision. No hardware validation is claimed at planning time.

**Target Platform**: A stock commercial Mini 4WD chassis carrying the selected BLDC motor, controller board, and a separate lithium-based battery pack. Scope follows 003: stock chassis excluding front-motor FM-A/SFM types. Use representative AR/VZ arrangements for initial fit studies; keep MA/MS/ME drive-path compatibility distinct from PCB mounting. Individual-chassis measured fit is not an inherited pre-order guarantee.

**Project Type**: Embedded hardware/firmware design and prototype manufacturing package.

**Performance Goals**: Reliable loaded startup and command response over an agreed voltage and load envelope; no unintended restart or loss of control in agreed fault cases. Numeric speed, current, and temperature limits are set only after motor, battery, and controller data are verified.

**Constraints**: Motor must fit the selected chassis and gear interface, preferably using the standard 130 motor mount. Minimum documented chassis cutting/drilling is allowed; a fully custom/3D-printed chassis is a last resort requiring user approval. Lithium chemistry is the preferred candidate; cell count and voltage/current envelope must match the motor and available chassis space. Protect battery and XIAO from phase-power faults and supply transients. Preserve safe off behavior across boot, signal loss, undervoltage, and detected faults. Do not reuse 003 brushed-motor ratings/circuit as BLDC design assumptions. PCB size, layer count, copper, and fab rules are not fixed until mechanical and thermal budgets are established.

**Scale/Scope**: Single prototype architecture and first chassis/motor combination, followed by a small pilot fabrication run. No mass-production, competition-rule, or cross-chassis compatibility guarantee.

## Constitution Check

The repository constitution file is an unfilled template and defines no ratified gates. Apply the repository `AGENTS.md` requirements and explicit user decisions: use Japanese for project communication, delegate KiCad/hardware design and validation to the PCB design workflow, use the KiCad skill for future CAD work, start with a commercial chassis, permit only minimized/documented chassis changes, and seek approval before adopting a wholly custom chassis. **Pre-research gate: PASS**; no conflict is known. Unresolved component and geometry facts are validation gates, not permission to guess.

### Post-design re-check

**PASS with gated implementation.** The planning artifacts preserve the commercial chassis constraint, do not lock unverified motor/controller/battery values, and require safety and manufacturing evidence before fabrication release. No constitution violation is introduced. KiCad creation, ERC/DRC, EMC/thermal analysis, and fabrication readiness have not been performed in this planning phase.

## Design Gates

1. **G1 — Motor and chassis fit**: Select a motor candidate with manufacturer drawing, can dimensions, shaft diameter/length, shaft side(s), mount, sensor/wire arrangement, gear/pinion compatibility, rated voltage/current, kV, pole pairs, winding resistance/inductance, and maximum electrical/mechanical speed. Evaluate representative stock-chassis arrangements within the 003 scope and document any minimum modification. Do not use a product-family name or comparison motor as dimensional proof.
2. **G2 — Battery and operating envelope**: Select a lithium pack candidate and establish cell count, chemistry, dimensions, full/nominal/cutoff voltage, continuous and transient current, protection method, and fault/recovery behavior. Confirm that motor/controller voltage and braking behavior fit this envelope and chassis volume.
3. **G3 — Commutation and command contract**: Qualify MCT8316ZR as the first custom-PCB ESC candidate using XSPEED sensor feedback. Compare DRV8306 with external MOSFETs if current/loss requires it, and HOBBYWING MINI28 as a finished ESC alternative. Codex designs XIAO firmware and BLE/WebApp for the selected command interface. Define PWM/SPI, XIAO pin budget, sensor supply/type/phase mapping, safe-off, stop/brake, timeout and fault handling. Upstream BLHeli is not the preferred path under the sensor-use requirement. See [controller-selection.md](controller-selection.md).
4. **G4 — Electrical and thermal feasibility**: Compare controller limits with motor electrical speed (`f_e = rpm × pole_pairs / 60`), phase current, winding parameters, startup/stall load, MOSFET loss, board temperature, and battery/transient limits. Distinguish peak from continuous ratings. Define fast shutdown and DC-bus energy handling during deceleration.
5. **G5 — Packaging and fabrication**: Freeze board outline/layers/material/copper only after a complete placement envelope covers motor, battery, XIAO antenna/USB, phase wiring, connector access, cover, road clearance, and service access. Run the repository KiCad review/validation flow. Prepare a revision-locked Gerber/drill, BOM, CPL, assembly notes, and inspection package; request JLCPCB DFM/quote as the primary low-volume candidate and review panelization, sourcing, substitutions, special processes, and cost before release.

No KiCad schematic or layout should be frozen before G1–G4 pass. No manufacturer order should be released before G5 evidence and explicit design approval.

## Project Structure

### Documentation (this feature)

```text
specs/005-mini4wd-brushless-motor/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── xiao-to-bldc-controller.md
└── tasks.md                 # created by speckit-tasks
```

### Hardware source

```text
hardware/kicad/mini4wd-brushless-motor/
├── mini4wd-brushless-motor.kicad_pro
├── mini4wd-brushless-motor.kicad_sch
├── mini4wd-brushless-motor.kicad_pcb
├── datasheets/
└── manufacturing/
```

These CAD paths are the intended implementation structure; this plan does not create a schematic or board before the design gates pass. Existing brushed project `hardware/kicad/mini4wd-motor-driver/` remains a separate design.

**Structure Decision**: Keep the feature specification, interface contract, candidate evidence, and validation procedure under the feature directory. Place a new KiCad project under a distinct hardware directory so BLDC electrical assumptions cannot be confused with the 003 brushed design. Firmware changes remain in their existing firmware project and are limited to the command interface/safety behavior proven necessary by the selected controller.

## Complexity Tracking

No constitution gates are violated; no exception is required.

Manufacturer evidence and inherited chassis scope: [manufacturer-evidence.md](manufacturer-evidence.md), updated 2026-11-20. Public Kyosho sources identify KV, sensor cable and original vehicle power arrangement; they do not yet establish the motor sensor electrical interface or standalone ratings.
