# Quickstart: Validate the New Board Design and Gerber Package

## Prerequisites

- EasyEDA Pro installed and available.
- Manufacturer design resources for XIAO MG24 Sense and selected components.
- Manufacturer drawings for the board-side Molex header and mating cable parts.
- A Gerber viewer and access to the selected PCB fabricator's upload/file check.

## Create and review the source design

1. Open the user-designated `mini4wd-motor-driver.eprj2` project and reconstruct rev1 from the README, `prompt.md`, and reference SVGs.
2. Build the schematic and board from the spec, project README, `prompt.md`, and reference SVGs. Do not use another `.eprj2` project as a design source.
3. Confirm the schematic pin/net table against [the interface contract](contracts/board-interface-and-fabrication.md).
4. Run the schematic/netlist checks and PCB DRC. Expected result: no unresolved connections, shorts, or unwaived DRC findings.
5. Inspect the 2D and 3D views. Expected result: approximately 55 ﾃ・21 mm outline, two outward-facing connectors at opposite ends, direct castellated MG24 placement, no underside leads, and a battery-facing underside with tented vias.
6. Review the connector drawing against the 1.6 mm nominal board thickness and confirm the complete mating cable parts. Inspect the assembled board and mated connectors against battery spacing and chassis clearance. Expected result: no unresolved collision or attachment issue in the vehicle envelope.
7. Review 5 A continuous current capability using documented electrical/thermal conditions and manufacturer ratings. Expected result: a signed-off analysis or recorded design change before manufacturing release.

## Export and inspect manufacturing files

1. Use EasyEDA Pro's **Export 竊・PCB Fabrication Files (Gerber)** flow to generate the Gerber archive and required drill outputs.
2. Export the BOM and pick-and-place data from the same saved project revision.
3. Open the complete Gerber set in a viewer. Check top/bottom copper, masks, silkscreens, outline, drill alignment, dimensions, and component clearances.
4. Upload the archive to the selected fabricator's file checker without placing an order. Expected result: board dimensions and two-layer stackup are recognized and no file/outline errors are reported.
5. Save the viewer render, file-check result, layer map, project revision, and BOM/CPL alongside the Gerber archive.

EasyEDA Pro's documented export menu and Gerber viewer review steps are summarized in [research.md](research.md#6-review-generated-gerbers-outside-the-source-editor).
