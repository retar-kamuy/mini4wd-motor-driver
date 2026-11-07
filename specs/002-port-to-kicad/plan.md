# Implementation Plan: Port Mini 4WD Motor Driver to KiCad

**Branch**: `002-port-to-kicad` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-port-to-kicad/spec.md`

## Summary

Port the Mini 4WD Motor Driver Expansion Board from EasyEDA to a native KiCad 10 project using the KiCad MCP server. Construct the schematic, assign verified SMT footprints, layout and route the 55.0 mm × 21.0 mm 2-layer PCB with a nominal 1.6 mm thickness, maintain a flat battery-facing bottom side with tented vias, and route high-current paths for 5A capacity. In accordance with user direction, restore the boost inductor L1 to the originally intended **Coilcraft XEL4030-102ME** (1.0 µH), lifting the EasyEDA library constraint that had necessitated the temporary substitution of Würth 74438357010. Release complete production-ready manufacturing data (Gerbers, Excellon drill, BOM, and CPL centroid files) tailored for JLCPCB SMT automated assembly.

## Technical Context

**Language/Version**: KiCad 10.0 project format (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`), Python 3.12 (`pcbnew` scripting interface), Node.js MCP bridge.

**Primary Dependencies**: KiCad 10.0; KiCad MCP Server (`C:\Users\hoshi\Repositories\KiCAD-MCP-Server\dist\index.js`); Seeed Studio XIAO MG24 Sense hardware assets; Molex Micro-Fit 3.0 connector drawings; Coilcraft / TI component datasheets; JLCPCB 2-layer manufacturing design rules.

**Storage**: Project repository directory at `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/` and its `manufacturing/` release directory.

**Testing**: KiCad Electrical Rules Check (ERC); KiCad Design Rules Check (DRC); Bottom-side via tenting and planar clearance inspection; Gerber, drill, and centroid inspection; JLCPCB automated SMT pre-order check.

**Target Platform**: 2-layer FR-4 SMT PCB, 55.0 mm × 21.0 mm, nominal 1.6 mm thickness, mounted directly above Mini 4WD battery compartment; powered by 2×AA Ni-MH (2.4 V), 2×AA Alkaline (3.0 V), or 1S Li-ion (3.7 V).

**Project Type**: Electronic hardware CAD design (Schematic, PCB Layout, and PCBA Manufacturing Data).

**Performance Goals**: 5A continuous motor drive current; 5A peak connector handling; 0 unconnected nets; 0 ERC violations; 0 DRC violations; 100% via tenting on bottom layer.

**Constraints**:
- 100% Surface Mount Technology (SMD/SMT); zero through-hole pins or battery-facing lead protrusions.
- Nominal PCB thickness: 1.6 mm to ensure retention tab engagement on Molex Micro-Fit 3.0 SMT right-angle headers (`43650-0214`).
- Main controller: Seeed Studio XIAO MG24 Sense soldered directly via 14 castellated edge pads.
- High-current traces/pours: Minimum 1.5 mm – 2.0 mm width for 5A capacity.
- Boost Inductor L1: Restored to Coilcraft XEL4030-102ME (1.0 µH).

**Scale/Scope**: 1 complete KiCad project (schematic + PCB layout + custom footprint library), 24 surface-mount components, 1 full manufacturing archive (Gerbers, drill, BOM, CPL).

## Constitution Check

The repository constitution (`.specify/memory/constitution.md`) currently contains standard template placeholders without ratified restrictive gates. Antigravity language rules (`GEMINI.md` and `.agents/rules/language.md`) require reports and documentation summaries in Japanese. This plan fully adheres to all specified electrical, mechanical, and safety requirements.

**Gate Status**: Pass.

## Project Structure

### Documentation (this feature)

```text
specs/002-port-to-kicad/
├── plan.md              # This implementation plan
├── research.md          # Phase 0 research & technology decisions
├── data-model.md        # Phase 1 data entities, BOM, and netlist
├── quickstart.md        # Phase 1 verification and test procedures
├── contracts/
│   └── board-interface-and-fabrication.md  # Interface & manufacturing contract
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code and Hardware Deliverables

```text
mini4wd-motor-driver/
├── GEMINI.md                                    # Antigravity Japanese language rules
├── hardware/
│   ├── rev1/                                    # Legacy EasyEDA rev1 artifacts (preserved as reference)
│   └── kicad/
│       └── mini4wd-motor-driver/                # Native KiCad 10 project root
│           ├── mini4wd-motor-driver.kicad_pro   # KiCad project file
│           ├── mini4wd-motor-driver.kicad_sch   # KiCad schematic file
│           ├── mini4wd-motor-driver.kicad_pcb   # KiCad PCB layout file
│           ├── mini4wd-motor-driver.pretty/     # Custom footprint library
│           │   ├── Molex_MicroFit30_43650-0214.kicad_mod
│           │   ├── XIAO_MG24_Castellated_14P.kicad_mod
│           │   └── Coilcraft_XEL4030.kicad_mod
│           └── manufacturing/                   # Released fabrication data
│               ├── gerber/                      # Gerber X2 / RS-274X + NC drill files
│               ├── bom.csv                      # JLCPCB SMT bill of materials
│               ├── cpl.csv                      # JLCPCB SMT pick-and-place centroid file
│               └── review/                      # 2D/3D renders and DRC/ERC reports
```

**Structure Decision**: Place the new KiCad project in `hardware/kicad/mini4wd-motor-driver/` to maintain a pristine, modern KiCad 10 project tree while preserving the legacy EasyEDA files in `hardware/rev1/` as historical reference.

## Phase 0: Research Findings

See [research.md](research.md). Key resolutions:
1. Reconstruct natively in KiCad 10 via the KiCad MCP server to eliminate proprietary EasyEDA database corruption risks.
2. Revert boost inductor L1 to **Coilcraft XEL4030-102ME** (1.0 µH) with a custom/verified 4.0 × 4.0 mm land pattern.
3. Establish custom project footprints in `mini4wd-motor-driver.pretty` for Molex Micro-Fit 3.0, XIAO MG24 Sense castellated pads, and Coilcraft XEL4030.
4. Route 5A power loops (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`) using wide polygonal copper pours and 2.0 mm tracks.
5. Enforce 100% via tenting on the bottom solder mask to guarantee complete battery surface insulation.

## Phase 1: Design and Contracts

See [data-model.md](data-model.md), [contracts/board-interface-and-fabrication.md](contracts/board-interface-and-fabrication.md), and [quickstart.md](quickstart.md).

### Release Gates

- **Circuit Gate**: KiCad schematic contains all 24 components; netlist connectivity strictly agrees with `data-model.md`; KiCad ERC passes with 0 errors and 0 unassigned pins.
- **Part Gate**: Every component maps to a verified SMT manufacturer part number and package; L1 is assigned to Coilcraft XEL4030-102ME.
- **Board Definition Gate**: Board outline on `Edge.Cuts` measures exactly 55.0 mm × 21.0 mm; stackup configured to 1.6 mm thickness; connectors J1/J2 oriented outward at opposite ends; bottom side contains zero through-hole pads.
- **5A Current Gate**: Power nets (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`) maintain $\ge 1.5\ \text{mm}$ trace width or dedicated polygon copper pours.
- **Safety Gate**: Bottom-layer vias are 100% tented with solder mask; zero exposed via annular rings on the battery side.
- **DRC Gate**: KiCad DRC passes with 0 violations against JLCPCB 2-layer fabrication rules.
- **Fabrication Gate**: Complete Gerber archive, drill file, JLCPCB SMT BOM, and CPL centroid files are generated and pass automated pre-flight file checks.

## Complexity Tracking

No constitutional violations exist. Native KiCad 10 project generation provides simpler maintenance, standalone Git version control, and superior design-rule verification compared to legacy EasyEDA proprietary formats.
