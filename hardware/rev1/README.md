# Mini 4WD Motor Driver PCB rev1

## Revision record

- Revision: rev1 (design in progress)
- Editable source: user-designated active project `../../mini4wd-motor-driver.eprj2`
- Rev1 is reconstructed in the user-designated active project. Other `.eprj2` files are not used as design sources.
- PCB target: two copper layers, nominal thickness 1.6 mm, physical outline approximately 55 ﾃ・21 mm. Live stackup and thickness still require confirmation.
- Interfaces: two Molex Micro-Fit 3.0 SMD right-angle two-position headers and direct castellated-pad mounting for XIAO MG24 Sense.

## Source requirements

- `../../README.md` and `../../docs/hardware_spec.md`: existing board behavior, circuit blocks, signals, and legacy geometry.
- `../../../specs/001-smt-gerber-board/spec.md` at the workspace root: approved module mounting, connector family, current targets, and 1.6 mm thickness decision.
- `../../docs/pcb_front.svg`, `../../docs/pcb_back.svg`, `../../docs/pcb_front_3D.png`, and `../../docs/pcb_back_3D.png`: visual routing, placement, and printed-interface-label references. They are not a source netlist or authoritative physical outline; use the documented 55 mm × 21 mm size.
- `../../../specs/001-smt-gerber-board/`: approved feature specification, interface contract, and implementation plan.

The legacy hardware specification records the existing revision at 1.2 mm. The approved requirement for this new revision is 1.6 mm.

## Manufacturing outputs

Final Gerber, drill, BOM, pick-and-place, layer map, and review records will be stored under `manufacturing/` after the EasyEDA design and release checks are complete.

## Regeneration

Open the designated active EasyEDA project, verify that its revision matches the manufacturing package, and regenerate all exports from that saved revision. Do not use another `.eprj2` file as a design source.
