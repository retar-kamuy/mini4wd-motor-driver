# rev1 Design Inputs and Assumptions

## Source hierarchy

1. `specs/001-smt-gerber-board/spec.md` is authoritative for XIAO MG24 Sense mounting, the Molex Micro-Fit SMD connector family, current targets, and the new board thickness.
2. `mini4wd-motor-driver/README.md` and `mini4wd-motor-driver/docs/hardware_spec.md` define the existing circuit behavior, signals, and physical outline. Their 1.2 mm thickness is legacy information for the existing board revision and is superseded by the approved 1.6 mm requirement for rev1.
3. `mini4wd-motor-driver/docs/pcb_front.svg`, `pcb_back.svg`, `pcb_front_3D.png`, and `pcb_back_3D.png` provide visual routing, placement, and silkscreen-label references. Do not scale their rendered bounds as the physical outline or treat copper appearance alone as an authoritative netlist.
4. Manufacturer datasheets and land-pattern drawings govern component ratings, footprints, and mating parts.
5. The user-designated active `.eprj2` is the implementation container; do not use any other `.eprj2` contents as a design source.

## Approved constraints

- Two copper layers; all components SMT; no component through holes or battery-facing protruding leads.
- Nominal PCB thickness: 1.6 mm.
- Physical outline: approximately 55 ﾃ・21 mm.
- Two opposite-facing, outward-oriented Molex Micro-Fit 3.0 two-position SMD right-angle headers; `43650-0214` is the selected header candidate.
- XIAO MG24 Sense mounted directly by castellated pads.
- Forward-only low-side N-channel motor drive, P-channel short braking, and the signals documented for the existing board.
- Toy-grade battery use follows the existing board: user-selected AA alkaline (including Tamiya Power Champ RX), AA NiMH (including Eneloop), and the legacy-marked 1S Li-ion option. No separate low-voltage qualification is required; performance may decline or stop as cells discharge.
- The atypical electrical requirement is the 5 A motor-drive target in `specs/001-smt-gerber-board/spec.md`. Follow the existing toy-board design without a separate overcurrent/thermal qualification; do not claim independent qualification evidence.
- Rev1 is a copy of the existing board. Preserve the existing resistor and capacitor positions and quantities; do not add passive footprints or parts. Populate/replace values and manufacturer parts only for positions identified on the reference board. The only additions/changes allowed are explicit rev1 improvements in `specs/001-smt-gerber-board/spec.md`.

## Items to resolve before layout freeze

See `manufacturing/review/design-freeze-blockers.md` for the consolidated blocker list and required closure evidence.

- XIAO MG24 Sense pin numbering, signal mapping, and footprint orientation are reconciled in `manufacturing/review/xiao-interface-review.md`. Preserve the documented 180-degree placement and use only the 14 castellated edge pads; leave unused edge pads and non-edge pads 15 onward unconnected.
- Import the verified XIAO MG24 Sense castellated footprint into the live EasyEDA project using the documented pad map.
- `docs/hardware_spec.md` provides the core IC/MOSFET/NTC part numbers and nominal divider values. Datasheet-based passive values are recorded in `manufacturing/review/passive-design-review.md`; the earlier image-based inventory is retained only as a record of source limitations. The no-additions rule for resistor/capacitor positions remains in force. The XIAO supply isolation diode candidate remains on hold pending reconciliation with the existing circuit implementation.
- Use `manufacturing/review/power-budget-research.md` as background only. Per user decision, inherit the existing toy-board power behavior without requiring new low-voltage endpoint or independent thermal qualification evidence. Unknown source circuit features remain unimplemented; do not add protection or passive parts based only on a reference design.
- For complete rev1 net assignments where the copper SVGs do not carry net names, follow `manufacturing/review/wiring-design.md`. It records the Codex-designed boost, sensing, MOSFET, connector, and XIAO power nets, and separates those decisions from connections directly established by SVG geometry.
- See `manufacturing/review/design-freeze-blockers.md` for the remaining definition blocker. Vehicle/battery mechanical-clearance evidence and separate 5 A thermal/current qualification are explicitly not required for design freeze per user decision.

## Live EasyEDA implementation checkpoint (2026-10-04)

- The user designated the currently opened EasyEDA project `mini4wd-motor-driver` as the implementation target. This supersedes the earlier clean-project-only target for live editing.
- The opened project contains an empty `PCB1` and an empty `schematic1` page. No existing design primitives were present in `PCB1` when inspected.
- A closed 55 mm ﾃ・21 mm rectangular board outline was created on the Board Outline layer and saved to the active EasyEDA project. This is only the initial outline; stackup thickness, parts, schematic, routing, review, and Gerbers remain incomplete.
- The EasyEDA API reports two active copper layers and the existing closed board outline measures 55.00 × 21.00 mm. PCB thickness is not confirmed yet.

## Live EasyEDA implementation update (2026-10-11)

- The user-connected `mini4wd-motor-driver` project is the active implementation target. Its schematic page now contains the BOM-selected ICs, MOSFETs, NTC, resistor/capacitor positions, and L1. The schematic was saved through the EasyEDA API.
- L1 uses Würth Elektronik WE-MAPI `74438357010`, replacing the earlier Coilcraft candidate. The exact EasyEDA library part is available with footprint `IND-SMD_L4.1-W4.1_SPM40XX`. This is a TI-listed 1 µH TPS61023 recommendation; the actual copper land pattern still needs to be checked against the manufacturer drawing.
- The user specified `docs/pcb_front.svg` and `docs/pcb_back.svg` as the routing references. The provisional net flags, ports, and trial wires were removed; the schematic currently has the placed components but no wires or net labels. `manufacturing/review/svg-routing-source-review.md` records the copper-layer geometry identified in those two SVGs and the remaining endpoint mapping work.
- EasyEDA's net-list API returned no nets during the trial wiring session. Do not use that empty result as evidence of correct connectivity; route the confirmed source paths and verify the resulting nets through the actual schematic/PCB views before release.
- MG24/connector symbols, PCB synchronization and placement, routing, DRC, and Gerber export remain incomplete. This component placement checkpoint is not a design freeze.
