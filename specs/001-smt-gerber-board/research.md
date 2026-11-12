# Research: Mini 4WD SMT Motor Driver Gerber Design

**Feature**: [spec.md](spec.md)  
**Date**: 2026-10-04

## Decisions

### 1. Use the user-designated active EasyEDA project; do not use other `.eprj2` contents

- **Decision**: Reconstruct the board in the user-designated active EasyEDA project. Treat `README.md`, `specs/001-smt-gerber-board/spec.md`, and the two SVGs as the design inputs. Do not use any other `.eprj2` contents as a design source.
- **Rationale**: This follows the explicit project instruction and keeps the design traceable to the agreed written specification and visual references.
- **Alternatives considered**: Use a different `.eprj2` as a source; rejected because the user designated the active project as the implementation target.
- **Source**: [EasyEDA Pro project format reference](https://prodocs.easyeda.com/en/api/reference/pro-api.edmt_projectfileformat.html) describes EPRJ2 and EPRJ3 project formats.

### 2. Use EasyEDA Pro for the editable source and manufacturing exports

- **Decision**: Keep the editable source in a new `.eprj2` project; export a separate fabrication ZIP and reviewable assembly files.
- **Rationale**: The requested `.eprj2` output identifies the intended project format. EasyEDA Pro documents export of Gerber ZIP, drill, BOM, and pick-and-place data.
- **Alternatives considered**: KiCad or a hand-authored Gerber package; rejected for this plan because they do not satisfy the requested native project format.
- **Sources**: [EasyEDA Pro project format](https://prodocs.easyeda.com/en/api/reference/pro-api.edmt_projectfileformat.html), [EasyEDA Pro Gerber export](https://prodocs.easyeda.com/en/pcb/export-pcb-fabrication-file-gerber/index.html), [EasyEDA Pro manufacturing files quick start](https://prodocs.easyeda.com/en/quick-start.html).

### 3. Use the official XIAO MG24 Sense interface geometry

- **Decision**: Obtain the module schematic, KiCad project, and footprint library from Seeed's XIAO MG24 Sense hardware resources; verify their pad numbering and outline before creating the EasyEDA package or symbol.
- **Rationale**: These are manufacturer-maintained module references and reduce the risk of incorrect castellated-pad pitch, pad order, or module outline.
- **Alternatives considered**: Approximate the pad pattern from the rendered board SVG; rejected because a rendered view is not a dimensioned manufacturing footprint.
- **Source**: [Seeed XIAO MG24 getting started and hardware resources](https://wiki.seeedstudio.com/xiao_mg24_getting_started/).

### 4. Use a manufacturer-defined Micro-Fit 3.0 SMT right-angle header; part candidate 43650-0214

- **Decision**: Use Molex Micro-Fit 3.0, single-row, two-circuit, right-angle, SMD header with solder tabs. Candidate MPN: `43650-0214`. Verify the mating housing and crimp terminals for the vehicle-side leads in the BOM.
- **Rationale**: Molex lists this part as a two-circuit, right-angle, surface-mount header, with 3.00 mm pitch and 8.5 A maximum current per contact, exceeding the specified 5 A peak connector target.
- **Alternatives considered**: 43650-0215; rejected because it is a through-hole kinked-pin part. 43650-0209 is another surface-mount variant with press-fit metal retention clips and a different plating option; it may be considered if it better suits mechanical retention or supply requirements.
- **Board-thickness decision**: Adopt nominal 1.60 mm PCB thickness for the new design, matching Molex's recommendation for this SMT header. This is an explicit user-approved change from the legacy hardware specification's 1.2 mm; the legacy `hardware_spec.md` remains a record of the existing board revision. Confirm the new board and mated connectors fit the vehicle envelope before layout freeze.
- **Sources**: [Molex 43650-0214 part page](https://www.molex.com/en-us/products/part-detail/436500214), [Molex 43650 series chart](https://www.molex.com/en-us/products/series-chart/43650), [Molex 43650 product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/436/43650/PS-43650-001.pdf?inline=), [Molex Micro-Fit connector family](https://www.molex.com/en-us/products/connectors/wire-to-board-connectors/micro-fit-connectors).

### 5. Keep the existing board's documented circuit behavior and pin map

- **Decision**: Follow `mini4wd-motor-driver/README.md` and `docs/hardware_spec.md` for the circuit: forward-only motor operation, N-channel low-side drive, P-channel short braking, UCC27511 gate drive, TPS61023 5 V boost, battery/MID voltage sensing, and NTC temperature sensing. Use `specs/001-smt-gerber-board/spec.md` for the agreed module mounting, SMT connector family, and current targets.
- **Rationale**: The README describes the behavior of the board represented by the SVG layout references; the prompt records the newer assembly and connection decisions.
- **Alternatives considered**: H-bridge/dual-NMOS topology; not selected because it conflicts with the README's existing forward-only driver behavior.
- **Sources**: Project [README](../../mini4wd-motor-driver/README.md), [hardware specification](../../docs/hardware_spec.md), [Vishay SiSS64DN datasheet](https://www.vishay.com/docs/67294/siss64dn.pdf), [TI TPS61023 datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf), [TI UCC27511 product page](https://www.ti.com/product/UCC27511).

### 6. Review generated Gerbers outside the source editor

- **Decision**: Export the Gerber ZIP and drill output, inspect the complete layer set in a Gerber viewer, and run the chosen fabricator's upload validation before release.
- **Rationale**: EasyEDA Pro warns users to inspect the Gerber output; a source-editor DRC does not prove that exported layers, drill coordinates, outline, or masks are correct.
- **Alternatives considered**: Trust the export dialog alone; rejected because it does not visually demonstrate layer registration or the final board shape.
- **Source**: [EasyEDA Pro Gerber export and preview guidance](https://prodocs.easyeda.com/en/pcb/export-pcb-fabrication-file-gerber/index.html).

## Design assumptions and unresolved verification

- Maintain the documented approximately 55 ﾃ・21 mm outline and nominal 1.6 mm thickness. The thickness is fixed by the latest user decision; mechanical fit verification remains required.
- Place parts on the top side only; the bottom side faces the batteries and must remain flat, with vias tented.
- Design review must demonstrate the stated 5 A continuous motor-current target. Component ratings alone do not establish thermal performance for the assembled board.
- Existing prose describes the major circuit blocks and sensing ratios, but may not specify every passive value or wiring detail. Derive the full schematic from documented functionality and manufacturer reference circuits, and record any unresolved design assumption before routing.
- Confirm the mating 2-position Micro-Fit wire housing and 18窶・0 AWG crimp terminal combination against Molex's drawings before releasing the BOM.
