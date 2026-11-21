---
description: "Ordered implementation tasks for the Mini 4WD brushless motor feature"
---

# Tasks: Mini 4WD Brushless Motor

**Input**: Design documents from `/specs/005-mini4wd-brushless-motor/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Task rules**: Do not commit a motor, battery, controller, or PCB outline to design until its evidence is recorded. Use the repository KiCad skill and PCB design review workflow for CAD and hardware validation. Do not claim hardware tests, ERC/DRC, or manufacturing readiness until run and recorded. Chassis cutting/drilling must be minimized and documented; a fully custom chassis requires user approval.

## Phase 1: Setup

**Purpose**: Prepare traceable records and a separate workspace for this BLDC design.

- [X] T001 [P] Create the motor, chassis, battery, and controller candidate record with source links and unresolved fields in `specs/005-mini4wd-brushless-motor/candidate-register.md`
- [X] T002 [P] Create the design revision and validation evidence log template in `specs/005-mini4wd-brushless-motor/validation-log.md`
- [X] T003 Create the isolated hardware project directory and record the approved project naming/revision convention in `hardware/kicad/mini4wd-brushless-motor/README.md`

---

## Phase 2: Foundational Research and Decision Gates

**Purpose**: Establish evidence needed before independent implementation of mechanical fit, motor control, and fabrication stories.

- [X] T004 Record the primary Kyosho XSPEED 85/56/41 candidates using published manufacturer data; list missing drawing/electrical/sensor evidence and the planned shaft-adapter fit checks in `specs/005-mini4wd-brushless-motor/candidate-register.md`; do not treat an incomplete candidate as qualified
- [X] T005 Record commercially available chassis candidates, published dimensions/drive layouts/gear data, and explicitly mark undocumented battery-bay and internal-envelope dimensions for physical measurement in `specs/005-mini4wd-brushless-motor/candidate-register.md`
- [X] T006 Record lithium battery candidates with dimensions, cell count, full/nominal/cutoff voltage, current capability, and protection behavior in `specs/005-mini4wd-brushless-motor/candidate-register.md`
- [X] T007 Compare integrated BLDC controller, external ESC (including MCT8316ZR, DRV8306, HOBBYWING MINI28 and the BLHeli firmware family), and XIAO commutation options against candidate motor voltage, electrical speed, winding R/L, phase current, sensors, startup, and stop behavior in `specs/005-mini4wd-brushless-motor/research.md`
- [ ] T008 Qualify the provisional MCT8316ZR ESC against XSPEED sensor signals and electrical limits, then finalize XIAO PWM/SPI timing, I/O budget, safe-off, timeout, fault and stop/brake semantics in `specs/005-mini4wd-brushless-motor/contracts/xiao-to-bldc-controller.md`; use alternatives in `controller-selection.md` if a gate fails

**Checkpoint**: Proceed to the user story phases only when motor, chassis, battery, and controller candidates have enough evidence to test against their acceptance criteria. Unknown critical dimensions or ratings remain blockers; do not fill them by assumption.

---

## Phase 3: User Story 2 — Fit the motor and board in a commercial chassis (Priority: P1)

**Goal**: Install the selected motor, battery, controller board, and required wiring in one stock commercial chassis, using its standard features where possible and only minimum documented chassis changes.

**Independent Test**: Assemble the selected motor and gear set in the chassis, place the PCB and battery in the available envelope, verify pinion mesh and clearances through full chassis assembly, and record all interferences and any minimum chassis modification.

- [ ] T009 [US2] Evaluate XSPEED candidates and representative stock chassis/gear arrangements within the 003 scope (front-motor FM-A/SFM excluded), using manufacturer dimensions, shaft/pinion compatibility, and mounting evidence; record the decision and rejected alternatives in `specs/005-mini4wd-brushless-motor/candidate-register.md`
- [ ] T010 [US2] Measure or derive the maximum usable PCB outline and height inside the fully assembled chassis, including motor, battery, gears, cover, road clearance, XIAO antenna, USB Type-C plug/cable access, connectors, and service access; record dimensions and reference photos in `specs/005-mini4wd-brushless-motor/mechanical-envelope.md` (check the USB insertion path in the outward-facing orientation; do not assume interference)
- [ ] T011 [US2] Create a dimensioned placement drawing for motor, battery, XIAO, power stage, phase wiring, and connectors within the measured chassis envelope in `specs/005-mini4wd-brushless-motor/mechanical-envelope.md`
- [ ] T012 [US2] Identify the minimum required chassis modifications, state why part selection or board placement cannot avoid each one, and document a stock-chassis alternative before proposing custom chassis work in `specs/005-mini4wd-brushless-motor/mechanical-envelope.md`
- [ ] T013 [US2] Verify the mechanical assembly for pinion mesh, shaft retention, gear rotation, battery replacement, cover fit, wiring strain relief, and zero unintended chassis/road interference in `specs/005-mini4wd-brushless-motor/validation-log.md`

**Checkpoint**: Mechanical fit passes only when the board stays inside the measured chassis envelope and required modifications are minimal and recorded. Obtain user approval before any fully custom chassis solution.

---

## Phase 4: User Story 1 — Drive the Mini 4WD with a brushless motor (Priority: P1)

**Goal**: Deliver controlled startup, speed change, stop/brake behavior, and safe fault handling using the selected motor, lithium pack, controller, and XIAO/BLE/WebApp platform.

**Independent Test**: With current-limited bench power and the selected motor, verify disabled outputs at boot, loaded startup, command changes, stop modes, command-loss/fault shutdown, no unintended restart, and agreed voltage/current/temperature limits; then repeat in the selected chassis.

- [ ] T014 [US1] Select the lithium pack configuration and define operating voltage, continuous/transient current, cutoff, protection trip/recovery, and brake-energy conditions in `specs/005-mini4wd-brushless-motor/power-budget.md`
- [ ] T015 [US1] Calculate maximum motor electrical speed as `f_e = rpm × pole_pairs / 60` and compare motor voltage, R/L, speed, current, sensor interface, and startup requirements against the selected sensored controller datasheet in `specs/005-mini4wd-brushless-motor/controller-compatibility.md`
- [ ] T016 [US1] Define power-stage current limits, battery/XIAO logic rails, transient suppression, reverse-current paths, thermal budget, and hardware fault shutdown in `specs/005-mini4wd-brushless-motor/power-budget.md`
- [ ] T017 [US1] Create the new KiCad project, symbols, footprints, schematic sheets, and project rules for the selected design in `hardware/kicad/mini4wd-brushless-motor/`
- [ ] T018 [US1] Implement the battery input, protected logic supply, BLDC controller/power stage, sensing, connectors, and hardware-safe enable/fault paths in `hardware/kicad/mini4wd-brushless-motor/mini4wd-brushless-motor.kicad_sch`
- [ ] T019 [US1] Implement the PCB placement, phase/DC-link switching loops, current sensing, thermal paths, ground return, XIAO antenna/USB clearance, and chassis mounting within the measured outline in `hardware/kicad/mini4wd-brushless-motor/mini4wd-brushless-motor.kicad_pcb`
- [ ] T020 [US1] Update XIAO firmware only as needed to implement the selected command, arming, timeout, stop, fault, and recovery contract in `firmware/mini4ai_v358/mini4ai_v358.ino`
- [ ] T021 [US1] Verify motor/controller pinout, component ratings, power sequencing, and datasheet-derived configuration against manufacturer documents in `hardware/kicad/mini4wd-brushless-motor/design-review.md`
- [ ] T022 [US1] Run and record schematic ERC, PCB DRC, schematic-to-PCB parity, unconnected-pad, and manufacturing-rule checks for the same KiCad revision in `hardware/kicad/mini4wd-brushless-motor/validation/`
- [ ] T023 [US1] Review switching-current loops, return paths, decoupling, RF coexistence, and emissions risks; record findings and mitigations in `hardware/kicad/mini4wd-brushless-motor/validation/emc-review.md`
- [ ] T024 [US1] Review power loss, component derating, copper/via thermal paths, and expected board/motor temperatures; record assumptions and limits in `hardware/kicad/mini4wd-brushless-motor/validation/thermal-review.md`
- [ ] T025 [US1] Build a prototype and perform current-limited logic-only and no-load bring-up, recording supply current, phase behavior, fault status, and unexpected heating in `specs/005-mini4wd-brushless-motor/validation-log.md`
- [ ] T026 [US1] Execute staged startup, speed, stop/coast/brake, low/nominal/high voltage, load, command-loss, and safe fault tests using `specs/005-mini4wd-brushless-motor/quickstart.md`; record results and failures in `specs/005-mini4wd-brushless-motor/validation-log.md`
- [ ] T027 [US1] Repeat the approved drive tests in the assembled stock chassis and record current, voltage sag, temperatures, stopping behavior, mechanical interference, and any motor synchronization loss in `specs/005-mini4wd-brushless-motor/validation-log.md`

**Checkpoint**: The drive story passes only when all agreed operation and fault criteria are demonstrated within the selected motor, battery, and controller limits. Unverified behavior remains explicitly marked not tested.

---

## Phase 5: User Story 3 — Prepare and request prototype fabrication (Priority: P2)

**Goal**: Prepare a revision-locked fabrication and assembly package that JLCPCB or an alternative provider can quote and review without unapproved substitutions.

**Independent Test**: A manufacturer can identify the board revision, stackup, holes, component MPNs, assembly side/orientation, special processes, inspection needs, and open DFM questions, then return a quote and DFM response.

- [ ] T028 [US3] Freeze and identify the reviewed design revision; export Gerber and drill files from the matching KiCad schematic/PCB into `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/`
- [ ] T029 [US3] Generate and cross-check the revision-matched BOM and CPL, including approved MPNs, sourcing status, side, rotation, origin, and pin-1 orientation in `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/`
- [ ] T030 [US3] Write fabrication stackup, board finish, thickness/copper, via treatment, panelization, assembly, inspection, and test requirements in `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/fabrication-notes.md`
- [ ] T031 [US3] Submit the revision package to JLCPCB for a quote and DFM review; record panelization, part availability, assembly capability, special processes, cost, lead time, and open questions in `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/dfm-response.md`
- [ ] T032 [US3] Resolve DFM blockers or compare an alternative manufacturer without accepting component substitutions or design changes that lack user approval in `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/dfm-response.md`
- [ ] T033 [US3] Obtain explicit design/revision approval and record the agreed quantity, inspection criteria, price, and remaining prototype-only risks in `hardware/kicad/mini4wd-brushless-motor/manufacturing/rev-<revision>/release-record.md`

**Checkpoint**: Fabrication release is permitted only after matching design checks, manufacturer DFM/quote review, and explicit approval. Do not order before this checkpoint.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Keep design evidence, implementation records, and handoff documentation consistent.

- [ ] T034 [P] Update `specs/005-mini4wd-brushless-motor/quickstart.md` with the selected hardware identifiers and approved operating limits
- [ ] T035 [P] Update `specs/005-mini4wd-brushless-motor/data-model.md` with final selected motor, chassis, battery, controller, PCB, and manufacturing package values
- [ ] T036 Reconcile acceptance criteria, design exceptions, remaining risks, and test evidence across `specs/005-mini4wd-brushless-motor/spec.md`, `specs/005-mini4wd-brushless-motor/validation-log.md`, and `hardware/kicad/mini4wd-brushless-motor/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes evidence and project records.
- **Foundational (Phase 2)**: Depends on setup; candidate and interface evidence must exist before design decisions.
- **User Story 2 (Phase 3)**: Depends on foundational motor/chassis candidate data; its measured envelope constrains the board and battery placement.
- **User Story 1 (Phase 4)**: Depends on the selected motor/chassis fit from US2 and foundational battery/controller data. Power-stage design and validation are hardware dependent.
- **User Story 3 (Phase 5)**: Depends on US1 design checks and prototype validation, plus US2 fit evidence.
- **Polish (Phase 6)**: Depends on the selected implementation and current validation records.

### User Story Dependencies

- **US2 (P1)**: Starts after Phase 2. Establishes the physical fit gate and usable PCB envelope.
- **US1 (P1)**: Starts after Phase 2 and requires US2's selected motor/chassis and measured PCB envelope. This dependency is deliberate because motor, battery, and board fit jointly determine feasibility.
- **US3 (P2)**: Requires completed and revision-locked US1/US2 artifacts; manufacturing handoff cannot be independent of the hardware design.

### Parallel Opportunities

- T001 and T002 can be done in parallel.
- T004, T005, and T006 can be researched in parallel, then reconciled in T007/T008.
- After the motor/chassis choice, T010 measurement and T014 battery evaluation can proceed in parallel; PCB outline remains provisional until the combined placement drawing is reviewed.
- Within US1, controller compatibility and power budget documents can be developed in parallel after candidate selection; schematic/layout tasks must follow the approved architecture and fit envelope.
- Within US3, BOM/CPL generation and fabrication notes can be prepared in parallel from the same frozen revision.

## Parallel Example: Candidate Research

```text
Task: T004 — Research commercial BLDC motor candidates and primary-source data
Task: T005 — Research stock chassis dimensions, battery bays, and gear interfaces
Task: T006 — Research lithium pack candidates and protection data
```

## Implementation Strategy

### MVP First

1. Complete setup and candidate research.
2. Pass the stock chassis fit gate (US2), including a measured maximum PCB outline.
3. Validate the selected motor, battery, and controller envelope before schematic freeze.
4. Implement and validate the drive function (US1) on the bench, then in the chassis.
5. Prepare a revision-locked manufacturing package and obtain DFM/quote feedback (US3).

### Incremental Delivery

Resolve motor/chassis/battery feasibility first; implement the smallest safe controller architecture that meets the drive story; validate in increasingly realistic conditions; then package for fabrication. A failure at a gate returns the work to candidate/architecture selection instead of silently relaxing the chassis, battery, or safety requirements.

## Notes

- The tasks describe future work; no CAD, ERC/DRC, hardware test, sourcing order, or manufacturer request was performed by task generation.
- Do not reuse the existing 003 brushed board’s footprint, current targets, connector, or power assumptions without fresh evidence.
- [P] tasks operate on separate files or research records and do not depend on incomplete implementation tasks.


## Implementation progress — 2026-11-20

- T008 partial: host signal allocation, control states, SPI/PWM timing candidates, safe bias and watchdog requirement recorded in `controller-compatibility.md` and the interface contract. Sensor compatibility and bench timing remain unqualified.
- T009–T013 preparation: `mechanical-envelope.md` defines measurement references and shaft-adapter checks; MA/MS double-shaft classification corrected. Exact motor, kit and placement remain open.
- T014–T016 partial: `power-budget.md` records topology options and inputs required for current/thermal/braking calculations; no operating limits selected.
- T017–T019 cannot be frozen before motor voltage/current/sensor data and chassis measurements are available. No CAD files or manufactured-ready claim introduced by this update.

- 2026-11-20: 003と同じシャーシ対象範囲を継承し、メーカー資料調査を `manufacturer-evidence.md` へ記録。京商最新版T05取説を取得・該当図/部品表を確認。センサー配列・信号電圧・モーター単体定格・缶/軸寸法は今回の公開資料で未取得。T008/T009/T014–T016の適合ゲートは未完了。

- 2026-11-21: T008/T016 partial: `hardware-inhibit-design.md` にTPS3431候補の独立watchdog、外部再armラッチ、電源監視、DRVOFF駆動論理、起動復帰手順、故障注入条件を記録。WDOの自動解除だけで再駆動を許可しない構成とした。300-ms lease＋230-ms watchdogの時間積算を明示。追加GPIO2本・部品値・電源監視閾値・最悪条件の回路検証が未完了であり、完了マークは増やしていない。T017–T019のCAD着手ゲートは維持。


## 2026-11-21 製造準備の部分進捗

- T008: 公式Seeed KiCadをnetlist化しSense内部配線を照合。旧D13/D14制御信号案を撤回し、D4 ARM_EDGE / D5 nFAULT / D18 WDI / hardware wakeを提案。メーカーKiCadと公式coreのIMU SDA/SCL不一致は未解決。
- T028–T033: `hardware/kicad/mini4wd-brushless-motor/manufacturing/README.md` に003相当の成果物と停止条件を具体化。`tools/pcb/audit_spec005_release.py` で現状インベントリを生成。回路/PCB/検査/発注パッケージ未作成のためタスク完了にはしない。


## 2026-11-21 公開仕様の別モーターを基準とする設計

T008/T009/T014–T016部分進捗: `documented-motor-design.md` を追加し、FAULHABER 1218S006B標準digital Hallを詳細設計基準、1226S006Bを高トルク比較とした。公式寸法/電気値、AN163のセンサー電源/配列、全6状態のTI DIR=0との通電相一致を取得・算術照合。AN190の低インダクタンス巻線条件から旧20 kHz案を100 kHz候補に訂正。`evidence/documented-motor-calculations.json`に計算結果を記録。調達価格/納期、取付、ILIM精度、電源IC、実機の駆動/温度が未完了でタスク完了数は増やさない。CAD/ERC/DRC/SPICE/EMC/熱解析は今回未実施。
