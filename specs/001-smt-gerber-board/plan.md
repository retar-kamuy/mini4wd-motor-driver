# Implementation Plan: Mini 4WD SMT Motor Driver Gerber Design

**Branch**: `001-smt-gerber-board` | **Date**: 2026-10-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-smt-gerber-board/spec.md`

## Summary

Use the user-designated active EasyEDA project as the editable implementation target and manufacturing package for the 55 × 21 mm, two-layer Mini 4WD motor driver using nominal 1.6 mm PCB thickness. Copy the existing circuit using only confirmed source-board features and apply compatible improvements explicitly listed in `prompt.md`; treat unconfirmed source features as unimplemented. Place and route the design with two opposite-facing Molex Micro-Fit connectors (candidate `43650-0214`) and direct castellated-pad XIAO MG24 Sense mounting. The source SVGs guide visual layout only. Per user decision, no vehicle-clearance assessment or independent 5 A thermal qualification is required. Do not use any other `.eprj2` project as a design source. Release Gerber data after circuit definition, electrical/PCB DRC, and Gerber-viewer checks are complete.

## Technical Context

**Language/Version**: N/A; graphical electronic design project

**Primary Dependencies**: EasyEDA Pro; Seeed Studio XIAO MG24 Sense public design materials; component manufacturer drawings and datasheets; PCB manufacturer fabrication rules

**Storage**: User-designated active EasyEDA `.eprj2` project and separately reviewable manufacturing outputs

**Testing**: Schematic electrical-rule and netlist checks; PCB design-rule check; board outline and layer review; exported Gerber inspection in a Gerber viewer; fabrication-service file check

**Target Platform**: Two-layer SMT PCB, approximately 55 ﾃ・21 mm, nominal 1.6 mm thick, mounted above Mini 4WD batteries; user-selected two-AA alkaline or NiMH supply, with 1S Li-ion support confirmed separately

**Project Type**: Electronic circuit and PCB design

**Performance Goals**: 5 A continuous motor-current design target; 5 A peak connector requirement; no unconnected electrical nets; no unresolved DRC or outline errors at manufacturing release

**Constraints**: All components SMT; no through-hole components; castellated-pad direct mounting for XIAO MG24 Sense; nominal 1.6 mm PCB thickness; underside kept flat with bottom-side vias tented; N-channel low-side motor drive and P-channel short-brake architecture; positive-only motor direction; two SMD right-angle Micro-Fit 3.0 two-position connectors; rev1 reconstructed from approved requirements in the active project

**Scale/Scope**: One complete schematic and one two-layer board, one source project, one Gerber archive, and supporting BOM, pick-and-place, layer map, and review images as supported by the selected assembly workflow

## Constitution Check

The repository constitution file still contains template placeholders and does not define ratified project principles or gates. No constitutional violation can be evaluated from those placeholders. This plan follows the feature specification and uses only its stated electrical and manufacturing release checks; vehicle clearance and separate 5 A qualification are waived by the user.

**Gate status**: Pass, with no project-specific constitution constraints declared.

## Project Structure

### Documentation (this feature)

```text
specs/001-smt-gerber-board/
笏懌楳笏 plan.md
笏懌楳笏 research.md
笏懌楳笏 data-model.md
笏懌楳笏 quickstart.md
笏懌楳笏 contracts/
笏・  笏披楳笏 board-interface-and-fabrication.md
笏披楳笏 checklists/
    笏披楳笏 requirements.md
```

### Source and design outputs

```text
mini4wd-motor-driver/
├── mini4wd-motor-driver.eprj2       # User-designated active EasyEDA source project
└── hardware/rev1/
    ├── manufacturing/
    │   ├── gerber/                   # Released Gerber and drill ZIP
    │   ├── bom.csv                   # Assembly bill of materials
    │   ├── pick-and-place.csv        # Component placement data
    │   ├── layer-map.md               # Fabrication layer mapping
    │   └── review/                    # Schematic, 2D/3D, and Gerber review renders
    └── README.md                     # Revision, assumptions, and regeneration notes
```

**Structure Decision**: Keep the manufacturing package and review records in a revision-specific hardware directory. Use the user-designated active project as editable source and leave the README and reference SVGs unchanged.

## Phase 0: Research Findings

See [research.md](research.md). Decisions include reconstructing rev1 in the user-designated active EasyEDA project, using Seeed's public XIAO MG24 Sense hardware resources for the module interface, selecting Molex 43650-0214 as the SMD right-angle two-position Micro-Fit header, and adopting its recommended nominal PCB thickness of 1.60 mm. Vehicle-clearance assessment is waived.

## Phase 1: Design and Contracts

See [data-model.md](data-model.md), [contracts/board-interface-and-fabrication.md](contracts/board-interface-and-fabrication.md), and [quickstart.md](quickstart.md).

1. Continue in the user-designated active `mini4wd-motor-driver.eprj2` project. Reconstruct the rev1 design from the README, `prompt.md`, and reference SVGs; do not use another `.eprj2` as a source.
2. Reconstruct the existing schematic from the README hardware specification and connection contract. Record each existing component value, manufacturer part number, package, and source. Preserve existing resistor/capacitor positions and quantities; do not add passive positions. Keep the README's forward-only low-side N-MOSFET drive and P-MOSFET short-brake behavior. Only apply changes explicitly listed in `prompt.md`.
3. Verify the XIAO MG24 Sense pinout and castellated pad geometry against Seeed's official hardware materials. Add only the interfaces in the contract, including 5 V, GND, VBAT sense, NTC temperature, motor PWM, and MID sense.
4. Select footprints from manufacturer drawings. Confirm the Micro-Fit mating housing and terminal family, SMT solder-tab lands, connector orientation, and recommended 1.60 mm PCB thickness before placement.
5. Place components on the top side. Keep the battery-facing bottom surface flat, tent bottom vias, and maintain the 55 ﾃ・21 mm outline and outward-facing connectors on opposite ends.
6. Route high-current power and motor nets with copper pours or appropriately sized copper paths on both layers where suitable. Keep gate-drive and sense paths away from high-current switching paths, and preserve the existing voltage-divider and NTC components and functions without adding passive positions.
7. Run schematic/netlist checks and PCB DRC; inspect the board outline, layers, and battery-facing underside for the prompt's SMT/flatness requirements.
8. Inspect 2D/3D assembly as a design record, and resolve connectivity, DRC, footprint, mask, and board-outline findings. Vehicle clearance and independent thermal qualification are waived.
9. Export Gerber and drill data, BOM, and pick-and-place data. Open every manufacturing layer together in a Gerber viewer, verify scale, registration, outline, mask, silkscreen, and drill alignment, then check the archive with the selected fabricator's upload/file validation.
10. Release the Gerber package only after circuit, DRC, and manufacturing-file review gates pass. Record the 1.6 mm nominal thickness and approximately 55 × 21 mm outline.

### Release Gates

- **Circuit gate**: Schematic connectivity agrees with the contract; no unresolved net names or pin assignments.
- **Part gate**: Each selected part has a verified manufacturer number, package/footprint source, electrical rating, and assembly suitability.
- **Copy-fidelity gate**: Existing resistor and capacitor positions and quantities match the reference board one-to-one. No passive positions are added; any exception must be an explicit `prompt.md` improvement.
- **Board-definition gate**: Record the 55 × 21 mm outline, nominal board thickness, connector orientation, and battery-facing SMT surface.
- **Current requirement**: Record the 5 A continuous motor target and 5 A peak connector target. Per user decision, independent thermal/overcurrent qualification of the inherited toy-board design is not a rev1 release gate; do not claim qualification without evidence.
- **Fabrication gate**: Two copper layers, solder masks, silkscreens, outline, and needed drill outputs are correctly mapped and viewer-checked; fabricator file validation passes.

## Complexity Tracking

No constitution gates are violated. A single PCB project and its manufacturing package are sufficient for the stated scope.
