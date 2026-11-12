# Feature Specification: Mini 4WD SMT Motor Driver Gerber Design

**Feature Branch**: `001-smt-gerber-board`
**Created**: 2026-10-04
**Status**: Draft
**Input**: User description: Create a specification and develop Gerber manufacturing data for a new Mini 4WD motor driver PCB using `docs/pcb_back.svg` and `pcb_front.svg` as layout references. Use the connector and MG24 connection decisions recorded in this feature specification, based on the conversation in `繝溘ル蝗幃ｧ・Δ繝ｼ繧ｿ繝ｼ繝峨Λ繧､繝舌・蝓ｺ譚ｿ縺ｮ閾ｪ菴懷庄閭ｽ諤ｧ.pdf`.

## User Scenarios & Testing

### User Story 1 - Produce a manufacturable SMT motor driver board (Priority: P1)

The board designer needs a board design based on the existing front and back layout references, with the agreed MG24 and connector mounting, so that a fabrication house can manufacture the PCB and a PCBA service can assemble it without manual through-hole work.

**Why this priority**: The primary outcome is a manufacturable replacement board that addresses difficult hand soldering and permits detachable power and motor wiring.

**Independent Test**: Review the completed fabrication package against the approved dimensions, connection map, component mounting constraints, and fabrication-service checks; confirm the board house accepts the Gerber package without missing layers or outline errors.

**Acceptance Scenarios**:

1. **Given** the final approved board requirements, **When** the design is reviewed, **Then** the board outline and component arrangement are traceable to the approved reference and dimensions.
2. **Given** an assembly review, **When** every component and board interface is inspected, **Then** the XIAO MG24 Sense uses castellated-pad direct soldering, the power and motor connections use the agreed two SMD right-angle connectors, and there are no through-hole component leads or protrusions on the battery-facing side.
3. **Given** the manufacturing package, **When** it is opened by a PCB fabrication service, **Then** it contains the required copper, mask, silkscreen, and board-outline data for a two-layer board and passes the service's file and design-rule checks.

### User Story 2 - Verify the battery-facing SMT surface (Priority: P2)

The builder needs an all-SMT board with a flat battery-facing side and no protruding through-hole component leads.

**Why this priority**: The prompt requires a flat underside without through-hole leads or exposed via barrels on the battery-facing side.

**Independent Test**: Inspect the underside manufacturing layers for through-hole component pads/leads and confirm all underside vias are tented.

**Acceptance Scenarios**:

1. **Given** the assembled board, **When** its battery-facing surface is inspected, **Then** no through-hole leads or exposed solder features protrude toward the batteries.

### Edge Cases

- The reference SVGs are rendered 窶弃hoto View窶・images rather than editable PCB design files; their displayed size is about 60.07 ﾃ・26.09 mm, while the README specifies a physical board size of about 55 ﾃ・21 mm. The displayed SVG bounds must not be mistaken for the physical board outline.
- The README does not establish an independent qualification for the 5 A continuous motor-current target; per user decision, inheriting the existing toy-board design is accepted.
- A fabrication or PCBA service reports a layer, footprint, solder-mask, clearance, or assembly issue.

## Requirements

### Functional Requirements

- **FR-001**: The design MUST follow the XIAO MG24 Sense and motor/power connector mounting decisions defined in this specification.
- **FR-002**: The XIAO MG24 Sense MUST be mounted by castellated pads directly to the board, without a pin header or socket.
- **FR-003**: The board MUST provide one two-position Molex Micro-Fit 3.0 SMD right-angle connector for battery power and one for motor output, with both connectors oriented outward at opposite board edges as specified by the approved layout.
- **FR-004**: All components MUST be surface mount; the design MUST contain no through-hole components or battery-facing protruding leads, and all underside vias MUST be covered by solder mask.
- **FR-005**: The design MUST provide a two-layer PCB and complete, correctly registered fabrication data for copper, solder mask, silkscreen, and board outline.
- **FR-006**: The board MUST use the approximately 55 ﾃ・21 mm physical outline specified in `mini4wd-motor-driver/README.md`; the SVGs MUST be used as front/back visual layout references, not as authoritative page dimensions.
- **FR-012**: The board MUST use a nominal 1.6 mm thickness to match the recommended PCB thickness for the selected Molex Micro-Fit 3.0 SMD right-angle header.
- **FR-007**: The board MUST preserve the README-defined positive-drive, M竏・low-side control architecture: N-channel MOSFET motor drive, P-channel MOSFET short braking, one PWM control signal, and the documented XIAO MG24 Sense pin assignments.
- **FR-008**: The manufacturing package MUST include the native editable board design and a concise layer/file map so the design can be reviewed and regenerated.
- **FR-009**: The motor drive MUST target 5 A continuous current as stated in this specification; each power/motor connector MUST meet the stated 5 A peak requirement. Per user decision, rev1 follows the existing toy-board design without a separate 5 A overcurrent/thermal qualification gate; do not report unperformed qualification as completed.
- **FR-013**: The board is intended for user-selected two-AA alkaline or NiMH toy batteries. Maintaining motor performance to each battery's discharge endpoint and separately characterizing low-voltage/brownout safety are not rev1 requirements; follow the confirmed existing design behavior.
- **FR-014**: Rev1 MUST copy the existing `mini4wd-motor-driver` board's resistor and capacitor positions and quantities. It MUST NOT add resistor or capacitor positions/components. Passive MPN/value substitutions are allowed only for existing positions. Additional design changes are limited to improvements explicitly listed in this specification.
- **FR-010**: The completed package MUST pass electrical connectivity, design-rule, board-outline, and fabrication-output checks for the selected manufacturer.
- **FR-011**: The rev1 board MUST be reconstructed from the README, this specification, and SVG layout references in the user-designated active EasyEDA project. Other `.eprj2` project contents MUST NOT be used, imported, or copied as design input.

### Key Entities

- **Board design**: The editable two-layer design, its physical outline, component placement, connectivity, and mounting orientation.
- **Fabrication package**: The generated manufacturing layer files and their documented mapping to board-fabrication inputs.
- **Board interface**: The connector pins, MG24 pads, power nets, motor nets, and sensor/control signals required to connect the board to the vehicle.
- **Layout reference**: The front/back SVG renderings and accompanying hardware notes used to reconstruct and verify placement.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The approved board has zero through-hole components and zero component leads protruding from the battery-facing side.
- **SC-002**: The XIAO MG24 Sense and both two-position power/motor connectors match the mounting type and connector family recorded in this specification.
- **SC-003**: The released design has two copper layers and a complete fabrication layer set accepted by the selected PCB manufacturer窶冱 file check.
- **SC-004**: The released fabrication package has zero unresolved connectivity errors, board-outline errors, or manufacturer design-rule violations.
- **SC-005**: The board outline is approximately 55 ﾃ・21 mm, and connector orientations are explicitly recorded.
- **SC-006**: The 5 A continuous motor-current target and 5 A peak connector requirement are recorded as design targets; no independent thermal qualification is required for rev1 per user decision.
- **SC-007**: The board thickness is nominally 1.6 mm and the outline is approximately 55 × 21 mm; separate vehicle/battery clearance evidence is not required per user decision.

## Source prompt disposition

The former root `prompt.md` has been merged into this specification and removed. Its settled mechanical, mounting, connector, all-SMT, underside-insulation, and current-target requirements are captured above. The original prompt's alternative dual-N-channel/H-bridge wording is not a design decision: the confirmed existing-board topology in this specification (N-channel low-side drive with P-channel short braking) governs. Requirements in this specification are the maintained source of truth for this feature.

## Assumptions

- `this specification` records the final user-approved decisions for the MG24 mounting and power/motor connectors; older alternatives in the PDF do not override those decisions.
- The PDF is background discussion. It contains earlier alternatives and advice, so only decisions repeated in this specification are treated as settled.
- The SVGs are visual layout references, not sufficient manufacturing source files; an editable PCB design must be created or recovered before Gerber data can be generated reliably.
- `mini4wd-motor-driver/README.md` is authoritative for the existing board窶冱 approximately 55 ﾃ・21 mm outline, electrical topology, and XIAO signal assignments. For this new design, the user-approved 1.6 mm thickness in this specification supersedes the legacy 1.2 mm thickness recorded in `docs/hardware_spec.md`.
- The user-designated active EasyEDA project is the editable rev1 target. Other `.eprj2` project contents are excluded as design references.
- The board follows the existing toy-board battery behavior, including user-selected AA alkaline (such as Tamiya Power Champ RX), AA NiMH (such as Eneloop), and the legacy-marked 1S Li-ion option. Loss of performance or shutdown as cells discharge is acceptable; no separate low-voltage qualification is required for rev1.
- The rev1 design is a copy of the existing board, with only the improvements explicitly listed in this specification. Existing resistor/capacitor placements and counts are preserved; TI evaluation-board circuits may be used as component-selection references but not as authority to add parts.
- The larger SVG viewBox describes the rendered view; the physical PCB outline follows the README窶冱 approximately 55 ﾃ・21 mm board specification.
- PCBA-ready files such as a bill of materials and component placement data may be produced as supporting outputs when needed by the selected assembly service.
