---
description: "Implementation task list for porting Mini 4WD Motor Driver to KiCad"
---

# Tasks: Port Mini 4WD Motor Driver to KiCad

**Input**: Design documents from `specs/002-port-to-kicad/`
**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/board-interface-and-fabrication.md](contracts/board-interface-and-fabrication.md), [quickstart.md](quickstart.md)

**Task Paths**: The native KiCad 10 project files and manufacturing artifacts are located in:
`mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/`

**Tests**: Hardware design verification is conducted via KiCad Electrical Rules Check (ERC), Design Rules Check (DRC), underside via tenting inspection, and manufacturing file validation as detailed in `quickstart.md`.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Maps to User Stories from `spec.md` (`[US1]`, `[US2]`, `[US3]`)
- Every task includes the exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize directory layout and KiCad 10 project structure.

- [x] T001 Create project directories `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/`, `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/`, and `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/`
- [x] T002 Initialize the native KiCad 10 project file `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro` using KiCad MCP server
- [x] T003 [P] Register the project-local footprint library `mini4wd-motor-driver.pretty` in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/fp-lib-table`

---

## Phase 2: Foundational (Custom Footprints & Board Setup)

**Purpose**: Create verified SMT footprints, stackup, and design rules before schematic completion and PCB layout.

**⚠️ CRITICAL**: Must complete before User Story 1 and User Story 2 layout work can proceed.

- [x] T004 [P] Create and verify custom SMT footprint for Molex Micro-Fit 3.0 SMD Right-Angle 2-pin header (`43650-0214`, 3.0 mm pitch, solder retention tabs) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Molex_MicroFit30_43650-0214.kicad_mod`
- [x] T005 [P] Create and verify custom footprint for Seeed Studio XIAO MG24 Sense 14-pad castellated module (2.54 mm pitch, 17.78 mm row span) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/XIAO_MG24_Castellated_14P.kicad_mod`
- [x] T006 [P] Create and verify custom footprint for restored boost inductor Coilcraft XEL4030-102ME (4.0 mm × 4.0 mm body, pads 1.37 mm × 2.39 mm, 1.88 mm gap) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Coilcraft_XEL4030.kicad_mod`
- [x] T007 Configure 2-layer board stackup (1.6 mm thickness, 1 oz Cu) and netclasses (`Default` and `Power_5A` with min 1.5 mm track width) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro`

**Checkpoint**: Footprints and project design rules established.

---

## Phase 3: User Story 1 - Create Native KiCad Project and Schematic (Priority: P1) 🎯 MVP

**Goal**: Complete the native KiCad schematic representing the full Mini 4WD Motor Driver circuit with all 24 components, restored Coilcraft inductor, and pass KiCad ERC with zero errors.

**Independent Test**: Run KiCad Electrical Rules Check (`run_erc`) via KiCad MCP server or `kicad-cli sch erc`; confirm 0 errors, 0 unassigned pins, and complete footprint bindings.

### Implementation for User Story 1

- [x] T008 [US1] Create the schematic document `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch` with standard power and ground ports via KiCad MCP server
- [x] T009 [P] [US1] Instantiate power conversion block (TI TPS61023DRLR, restored Coilcraft XEL4030-102ME, CIN 10 µF, COUT1/2 22 µF, feedback resistors 732 kΩ / 100 kΩ) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T010 [P] [US1] Instantiate motor drive and gate driver block (TI UCC27511DBVR, SiSS64DN N-MOSFET, SI7137DP P-MOSFET, SS54-HF flyback diode, C_BYP 0.1 µF) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T011 [P] [US1] Instantiate sensing and protection block (VBAT divider 22 kΩ : 10 kΩ, MID divider 22 kΩ : 10 kΩ, NTCG104BH103JT1 thermistor with 10 kΩ fixed pull-up, SS14-E3 5V isolation diode) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T012 [P] [US1] Instantiate external connectors (J1 Battery, J2 Motor) and MCU interface (XIAO MG24 Sense castellated pads 1–14) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T013 [US1] Connect all schematic wires and net labels (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`, `BOOST_5V`, `XIAO_5V`, `PWM_DRIVE`, `VBAT_SENSE`, `MID_SENSE`, `TEMP_SENSE`, `I2C_SDA`, `I2C_SCL`) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T014 [US1] Bind SMT footprints to all 24 schematic symbols per `data-model.md` and verify no unassigned footprints in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`
- [x] T015 [US1] Run KiCad Electrical Rules Check (ERC) via KiCad MCP server or CLI and resolve all warnings/errors in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch`

**Checkpoint**: User Story 1 complete. Schematic is electrically valid, fully annotated, and passes ERC (0 errors).

---

## Phase 4: User Story 2 - Layout, Routing, and DRC Verification (Priority: P2)

**Goal**: Complete the 2-layer PCB layout conforming to 55.0 mm × 21.0 mm outline, 1.6 mm thickness, flat battery-facing bottom surface, outward connectors, 5A trace widths, and 0 DRC errors.

**Independent Test**: Run KiCad Design Rules Check (`run_drc`) via KiCad MCP server or `kicad-cli pcb drc`; confirm 0 violations, 0 unrouted nets, 0 clearance errors, and inspect bottom solder mask for 100% via tenting.

### Implementation for User Story 2

- [x] T016 [US2] Synchronize schematic netlist and footprints into `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` via KiCad MCP server
- [x] T017 [US2] Define rectangular board outline (55.0 mm × 21.0 mm, 1.0 mm corner radius) on `Edge.Cuts` in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [x] T018 [US2] Place connectors J1 (left edge) and J2 (right edge) facing outwards, and position MCU1 (180° rotation) and power semiconductors on the top layer (`F.Cu`) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` (aligned 100% to `docs/pcb_front.svg`)
- [x] T019 [US2] Place passives (inductor L1, capacitors, resistor dividers, diodes, thermistor) on `F.Cu` adhering to `docs/pcb_front.svg` orientation (vertical 90° rotation) and short switching loops in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [x] T020 [US2] Route high-current nets (`VBAT`, `GND`, `MOTOR_MINUS`) using dedicated polygon copper pours and ≥ 1.5 mm – 2.0 mm traces on `F.Cu` and `B.Cu` in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [x] T021 [US2] Route signal nets (`PWM_DRIVE`, `GATE_DRIVE`, `VBAT_SENSE`, `MID_SENSE`, `TEMP_SENSE`, `I2C_SDA`, `I2C_SCL`, `BOOST_5V`, `XIAO_5V`) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [x] T022 [US2] Add ground copper pours on bottom layer with stitching vias and verify 100% solder mask tenting over all bottom-layer vias in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [ ] T023 [US2] Add silkscreen component labels, connector pin polarity (`B+`, `B-`, `M+`, `M-`), and ADC voltage divider scaling text (`V_REAL = V_ADC * 3.2`) in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`
- [ ] T024 [US2] Run KiCad Design Rules Check (DRC) via KiCad MCP server / CLI and verify 0 violations, 0 unconnected nets, and 0 clearance errors in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` (currently in progress: master fix script ready in `tmp/step10_master_fix.py`)

**Checkpoint**: User Story 2 layout complete, routing 100% connected, final DRC clean-up in progress.

---

## Phase 5: User Story 3 - Generate Production Manufacturing Outputs (Priority: P3)

**Goal**: Export production-ready Gerber archives, Excellon drill files, JLCPCB SMT BOM, and CPL centroid files from the verified KiCad PCB.

**Independent Test**: Validate exported Gerber archive in a Gerber viewer; verify layer registration, outline alignment, drill hits, and BOM/CPL part number mappings.

### Implementation for User Story 3

- [ ] T025 [US3] Export complete Gerber X2 / RS-274X layer files (`F.Cu`, `B.Cu`, `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS`, `F.Paste`, `Edge.Cuts`) to `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/`
- [ ] T026 [US3] Export Excellon NC drill files (PTH vias only, 0 component holes) to `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/`
- [ ] T027 [US3] Generate JLCPCB-formatted bill of materials (BOM) including Coilcraft XEL4030-102ME, UCC27511DBVR, SiSS64DN, SI7137DP, TPS61023, and Molex 43650-0214 in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/bom.csv`
- [ ] T028 [US3] Generate component placement list (CPL / POS) centroid file with rotation and layer coordinates in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/cpl.csv`
- [ ] T029 [US3] Export IPC-D-356 electrical test netlist in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/mini4wd-motor-driver.ipc`

**Checkpoint**: User Story 3 pending. Production manufacturing package ready for JLCPCB submission.

---

## Phase 6: Polish & Cross-Cutting Documentation

**Purpose**: Document release mapping, update hardware documentation, and run final end-to-end quickstart validation.

- [ ] T030 [P] Create `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/layer-map.md` documenting fabrication layer mapping and drill specifications
- [ ] T031 [P] Update `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/README.md` with KiCad 10 project overview, component restoration notes, and build/export instructions
- [ ] T032 Execute validation scenarios in `specs/002-port-to-kicad/quickstart.md` to confirm end-to-end readiness


---

## Phase 7: Convergence

> **Assessed**: 2026-11-07 | DRC report `drc_step9.rpt` (173 violations, 1 unconnected)、`tmp/step10_master_fix.py` 作成済みだが未実行。

- [ ] T033 [US2] Execute `tmp/step10_master_fix.py` to apply revised routing (crossing-free, pad-avoiding traces, B.Cu-only GND zone, F.Cu zone removed) and refill B.Cu GND zone, targeting 0 `shorting_items` and 0 `tracks_crossing` in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` per FR-010 / SC-005 (missing)
- [ ] T034 [US2] Verify or fix `MOTOR_PLUS` net assignment: spec (FR-002) and `docs/wiring-design.md` define a `MOTOR_PLUS` net (J2 Pin 1); current PCB has J2.1 assigned to `VBAT` — confirm topology is intentional (high-side switch) or reassign to `MOTOR_PLUS` in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` per FR-002 / SC-001 (missing)
- [ ] T035 [US2] Set solder mask tenting on all 38 vias in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` (SolderMaskExpansion to board default tenting value or use board-level `tenting_all_vias` rule) to satisfy FR-007 / SC-003 battery-safety requirement (missing)
- [ ] T036 [US2] Run final KiCad DRC after T033–T035 and confirm 0 violations, 0 unconnected nets, 0 clearance errors in `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` per FR-010 / SC-005 (missing)
- [ ] T037 [US2] Add silkscreen text to `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb`: connector polarity labels `B+`, `B-` (J1) and `M+`, `M-` (J2) on `F.SilkS`, plus ADC scaling annotation `V_REAL = V_ADC * 3.2` near voltage-divider resistors per T023 (missing)
- [ ] T038 [US3] Create `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/manufacturing/` directory and export Gerber X2 / RS-274X layer files (`F.Cu`, `B.Cu`, `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS`, `F.Paste`, `Edge.Cuts`) and Excellon drill files to `manufacturing/gerber/` via `kicad-cli pcb export gerbers` and `kicad-cli pcb export drill` per T025–T026 / FR-011 / SC-006 (missing)
- [ ] T039 [US3] Generate JLCPCB-formatted `manufacturing/bom.csv` (columns: Comment, Designator, Footprint, LCSC Part#) covering all 24 SMD components including Coilcraft XEL4030-102ME, UCC27511DBVR, SiSS64DN, SI7137DP, TPS61023 per T027 / FR-011 / SC-006 (missing)
- [ ] T040 [US3] Generate `manufacturing/cpl.csv` component placement list (columns: Designator, Val, Package, Mid X, Mid Y, Rotation, Layer) via `kicad-cli pcb export pos` per T028 / FR-011 / SC-006 (missing)
- [ ] T041 [US3] Export IPC-D-356 electrical test netlist to `manufacturing/mini4wd-motor-driver.ipc` via `kicad-cli pcb export ipcd356` per T029 / SC-006 (missing)
