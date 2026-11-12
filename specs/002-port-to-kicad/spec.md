> **2026-11-10 現状注記**: 本文には旧作業コピーへのパスと当時の設計・検証状態が含まれる。現行の正規設計は `hardware/kicad/mini4wd-motor-driver/`、検証根拠と残作業は `specs/003-resolve-pcb-drc/` を参照する。旧手順や完成の記述を現行基板の検証結果として扱わない。

# Feature Specification: Port Mini 4WD Motor Driver to KiCad

**Feature Branch**: `002-port-to-kicad`
**Created**: 2026-10-25
**Status**: Draft
**Input**: User description: "本プロジェクトはEasyEDA用になっていますが、Kicadへ移植して。KiCADのMCPサーバを利用してください。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Native KiCad Project and Schematic via KiCad MCP Server (Priority: P1)

A hardware engineer needs the Mini 4WD Motor Driver circuit ported from the EasyEDA design into a native, standalone KiCad project (`.kicad_pro`, `.kicad_sch`) using the KiCad MCP server, so that the schematic is fully defined, version-controllable, and verified by Electrical Rules Check (ERC) with correct component symbols, values, and footprint bindings.

**Why this priority**: Establishing a valid schematic with accurate net connectivity and component definitions is the required foundation for all subsequent layout, simulation, and manufacturing work.

**Independent Test**: Execute KiCad Electrical Rules Check (ERC) via KiCad MCP server; confirm zero unconnected power pins, zero unassigned nets, zero floating inputs, and complete symbol-to-footprint assignments matching the approved bill of materials (`bom.csv`).

**Acceptance Scenarios**:

1. **Given** the approved BOM (`hardware/rev1/manufacturing/bom.csv`) and wiring architecture (`wiring-design.md`), **When** the KiCad project and schematic are generated via KiCad MCP server, **Then** all 24 components (XIAO MG24 Sense, UCC27511 gate driver, SiSS64DN N-MOSFET, SI7137DP P-MOSFET, TPS61023 boost converter, Molex Micro-Fit connectors, sense dividers, NTC thermistor, diodes, inductor, and passives) are instantiated with verified symbols, footprints, and designators.
2. **Given** the generated schematic, **When** KiCad ERC is executed, **Then** it produces zero critical errors and zero invalid net conflicts.
3. **Given** the verified schematic, **When** netlist export or schematic-to-board synchronization is performed, **Then** all nets and footprint associations synchronize into the KiCad PCB document without missing footprints or undefined pins.

---

### User Story 2 - Layout, Routing, and DRC Verification in KiCad (Priority: P2)

A PCB layout designer needs a two-layer KiCad board (`.kicad_pcb`) created via the KiCad MCP server that adheres to the 55.0 mm × 21.0 mm physical outline, 1.6 mm board thickness, all-SMD mounting constraint, completely flat battery-facing bottom surface with tented vias, and high-current (5A) power routing.

**Why this priority**: The PCB is mounted directly above the Mini 4WD battery compartment. Any protruding through-hole pin or exposed bottom via risks electrical shorting or mechanical interference with the vehicle chassis and cells.

**Independent Test**: Run KiCad Design Rules Check (DRC) via KiCad MCP server against standard 2-layer manufacturing design rules; inspect copper layers to confirm high-current traces/pours measure ≥ 1.5 mm and inspect the bottom solder mask to confirm 100% via tenting and zero exposed bottom pins.

**Acceptance Scenarios**:

1. **Given** the physical constraints from `specs/001-smt-gerber-board/spec.md` and `docs/hardware_spec.md`, **When** the PCB outline is generated in KiCad, **Then** the board outline on `Edge.Cuts` is 55.0 mm × 21.0 mm and stackup thickness is configured to 1.6 mm.
2. **Given** the placement requirements, **When** components are placed, **Then** the Molex Micro-Fit 3.0 power (J1) and motor (J2) connectors are positioned at opposite board edges facing outward, and the XIAO MG24 Sense is placed with its 14 castellated edge pads oriented according to the reference layout.
3. **Given** the 5A continuous motor drive target, **When** the power nets (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`) are routed, **Then** traces are sized to at least 1.5 mm – 2.0 mm width or implemented as dedicated polygon copper pours.
4. **Given** the battery-mounting safety requirements, **When** the bottom layer (`B.Cu` / `B.Mask`) is inspected, **Then** there are zero through-hole pads, zero exposed component leads, and all bottom vias are covered by solder mask (tented vias).
5. **Given** the routed board, **When** KiCad DRC is executed, **Then** it completes with 0 errors and 0 unrouted nets.

---

### User Story 3 - Generate Automated Manufacturing and Assembly Outputs (Priority: P3)

A manufacturing engineer needs production-ready fabrication data (Gerber X2 / RS-274X, Excellon drill files, BOM, and CPL/pick-and-place centroid files) exported directly from KiCad for automated SMT assembly (e.g. JLCPCB SMT service) without requiring hand soldering or manual CAD post-processing.

**Why this priority**: The final goal of the migration is an automated, repeatable hardware release package ready for fabrication and PCBA ordering.

**Independent Test**: Load exported Gerber and drill archives into a standard Gerber viewer / manufacturing pre-flight check; verify file completeness, layer registration, zero THD drill hits, and verify that BOM and CPL files match JLCPCB SMT submission formats.

**Acceptance Scenarios**:

1. **Given** the DRC-clean KiCad PCB, **When** manufacturing exports are executed, **Then** Gerber layers (`F.Cu`, `B.Cu`, `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS`, `F.Paste`, `Edge.Cuts`) and Excellon drill files (`.drl`) are produced and cleanly formatted.
2. **Given** the exported component placement file (CPL / POS), **When** inspected against footprint centroids, **Then** all 100% SMD parts have valid X/Y coordinates, layer assignments (`Top`), and correct component rotation angles.
3. **Given** the exported bill of materials (BOM), **When** reviewed, **Then** all parts include manufacturer part numbers (MPNs), descriptions, designators, and package designations corresponding to the approved `bom.csv`.

---

### Edge Cases

- **Custom Footprints Availability**: The Molex Micro-Fit 3.0 SMT right-angle header (`43650-0214`) and Seeed Studio XIAO MG24 Sense castellated footprint might not exist in standard default KiCad footprint libraries. Custom footprints or project-local `.pretty` footprint libraries must be generated or registered using KiCad MCP server tools (`register_footprint_library`, `create_footprint`).
- **Bottom Layer Solder Mask Tenting**: Standard CAD exporters sometimes default to untented vias. KiCad board design rules and plot settings must explicitly specify solder mask tenting for all vias on the bottom layer to ensure battery contact insulation.
- **Trace Necking at Small SMT Pads**: 5A power traces (≥ 1.5 mm) connecting to small SMT pads (e.g. SOT-23-6 or PowerPAK pads) must taper/neck down cleanly to pad widths without triggering DRC clearance or minimum-width violations.
- **KiCad MCP Server Compatibility**: The development environment is WSL/Linux with KiCad 10.0 and the installed Python/pcbnew. MCP calls and programmatic generation must adhere to the installed KiCad schema and scripting interfaces; PowerShell is not required.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST establish a native KiCad project structure (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`) located under `hardware/kicad/mini4wd-motor-driver/` (canonical target established 2026-11-10).
- **FR-002**: The KiCad schematic MUST implement the complete circuit defined in `docs/hardware_spec.md`, `hardware/rev1/manufacturing/bom.csv`, and `hardware/rev1/manufacturing/review/wiring-design.md`, containing:
  - Main Controller: Seeed Studio XIAO MG24 Sense (14 castellated edge pads)
  - Gate Driver: TI UCC27511DBVR (SOT-23-6) with 5V drive supply
  - Motor Drive N-ch MOSFET: Vishay SiSS64DN-T1-GE3 (PowerPAK 1212-8S)
  - Short-Brake P-ch MOSFET: Vishay SI7137DP-T1-GE3 (PowerPAK SO-8)
  - Boost Converter: TI TPS61023DRLR (SOT-5X3 DRL-6) with Coilcraft XEL4030-102ME 1.0 µH inductor (reverted from EasyEDA-substituted Würth 74438357010)
  - Power & Motor Connectors: 2x Molex Micro-Fit 3.0 right-angle SMT headers (J1 for B+/B-, J2 for M+/M-)
  - Voltage Sensing Dividers: VBAT_SENSE (22 kΩ : 10 kΩ) and MID_SENSE (22 kΩ : 10 kΩ)
  - Temperature Sensing: NTC thermistor (10 kΩ @ 25°C, NTCG104BH103JT1) with 10 kΩ fixed pull-up
  - Protection & Decoupling: SS54-HF 5A Schottky motor flyback diode, SS14-E3 MCU 5V isolation diode, and ceramic bypass/filter capacitors.
- **FR-003**: All schematic components MUST use 100% Surface Mount Technology (SMD/SMT). The design MUST contain zero through-hole components.
- **FR-004**: The schematic MUST pass KiCad Electrical Rules Check (ERC) with zero unresolved errors.
- **FR-005**: The PCB outline MUST be a 55.0 mm × 21.0 mm rectangle on the `Edge.Cuts` layer.
- **FR-006**: The PCB MUST be a 2-layer board with nominal 1.6 mm thickness to match the Molex Micro-Fit 3.0 right-angle SMT header retention specifications.
- **FR-007**: The bottom PCB layer (`B.Cu` / `B.Mask`) MUST be completely flat with zero through-hole leads and all vias tented with solder mask to guarantee insulation against the top of the battery cells.
- **FR-008**: Power traces and copper pours for high-current loops (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`) MUST have a width of at least 1.5 mm to 2.0 mm (or polygon copper pours) capable of carrying 5A continuous/peak current.
- **FR-009**: The connectors J1 (Battery Power) and J2 (Motor Output) MUST be placed at opposite board edges facing outward to prevent top-height and cable interference with the vehicle body.
- **FR-010**: The PCB layout MUST pass KiCad Design Rules Check (DRC) against standard 2-layer PCBA fabrication rules (JLCPCB 2-layer: min trace/space 0.127 mm, min via drill 0.3 mm, min annular ring 0.13 mm) with zero violations.
- **FR-011**: The KiCad project MUST generate complete production fabrication files under `hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/manufacturing/`, including:
  - Gerber files (RS-274X / Gerber X2)
  - Excellon NC drill files
  - BOM in JLCPCB SMT format
  - Centroid / Component Placement List (CPL / POS)
- **FR-012**: The porting and validation process MUST utilize the KiCad MCP server tools for project creation, component placement, net connectivity, and design verification.

### Key Entities

- **KiCad Project (`.kicad_pro`)**: The top-level project container governing board stackup, design rules, and library associations.
- **KiCad Schematic (`.kicad_sch`)**: The schematic document defining component symbols, electrical nets, pin connections, and schematic annotations.
- **KiCad PCB (`.kicad_pcb`)**: The physical board document defining physical dimensions (55×21 mm), copper layers (`F.Cu`, `B.Cu`), component footprints, trace routing, copper zones, and silkscreen markings.
- **Footprint Library (`.pretty`)**: Project-specific footprint library containing custom footprints for the Molex Micro-Fit 3.0 SMT header and XIAO MG24 Sense castellated module.
- **Fabrication Package**: The exported Gerbers, drill files, BOM, and CPL centroid files for JLCPCB manufacturing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of circuit components (24 parts) and functional nets from the EasyEDA design are successfully recreated in KiCad with 0 schematic ERC errors.
- **SC-002**: KiCad PCB layout adheres strictly to the 55.0 mm × 21.0 mm physical outline with nominal 1.6 mm thickness.
- **SC-003**: 100% of components are surface-mount devices (0 through-hole pins), and 100% of bottom-side vias are tented by solder mask.
- **SC-004**: High-current paths (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`) maintain ≥ 1.5 mm trace width or polygon copper pours throughout their runs.
- **SC-005**: KiCad Design Rules Check (DRC) completes with 0 errors and 0 unrouted nets.
- **SC-006**: Complete manufacturing export package (Gerbers, drill, BOM, CPL) is generated and verified with 0 syntax or layer mapping errors.

## Assumptions

- **Target CAD Environment**: KiCad 10.0 on WSL/Linux, using the KiCad MCP server when available and Linux KiCad CLI/Python utilities. PowerShell is not required.
- **Project Location**: KiCad design files are placed in `hardware/kicad/mini4wd-motor-driver/`; the nested legacy copy is historical. See `specs/003-resolve-pcb-drc/plan.md`.
- **BOM & Circuit Topology Authority**: `hardware/rev1/manufacturing/bom.csv`, `docs/hardware_spec.md`, and `hardware/rev1/manufacturing/review/wiring-design.md` serve as the authoritative sources for component selection, pinouts, and network connectivity. The boost inductor L1 is restored to the originally intended Coilcraft XEL4030-102ME (1.0 µH), lifting the EasyEDA library restriction that necessitated substituting Würth 74438357010.
- **Thermal & Current Qualification**: The 5A continuous motor drive and 5A connector ratings are design targets achieved through trace geometry and copper pours. No separate physical bench burn-in qualification is required during this CAD porting phase.
- **Manufacturing Target**: JLCPCB 2-layer PCBA process is the reference target for design rules, layer naming, and SMT assembly output formats.
