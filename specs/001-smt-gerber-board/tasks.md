---
description: "Implementation task list for the Mini 4WD SMT motor driver board and Gerber package"
---

# Tasks: Mini 4WD SMT Motor Driver Gerber Design

**Input**: Design documents from `specs/001-smt-gerber-board/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Task paths**: Manufacturing artifacts are under `mini4wd-motor-driver/hardware/rev1/`. The editable source is the user-designated active `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`; this supersedes the fresh-project-only instruction. Do not use any other `.eprj2` project as a design source.

**Tests**: No standalone software test tasks are included. The specification requires electrical, DRC, mechanical, Gerber-viewer, and fabricator-file checks; these are included as design review and release tasks.

## Phase 1: Setup

**Purpose**: Confirm the designated active EasyEDA project and establish manufacturing artifact locations.

- [x] T001 Create `mini4wd-motor-driver/hardware/rev1/` with `manufacturing/gerber/` and `manufacturing/review/` subdirectories.
- [x] T002 Confirm the user-designated `mini4wd-motor-driver/mini4wd-motor-driver.eprj2` project is the active EasyEDA implementation target; do not use any other `.eprj2` project as a design source.
- [x] T003 Create `mini4wd-motor-driver/hardware/rev1/README.md` recording revision, source requirements, nominal 1.6 mm board thickness, approximately 55 ﾃ・21 mm outline, and project regeneration notes.

---

## Phase 2: Foundational Design Inputs

**Purpose**: Establish verified electrical and component inputs before schematic and layout work begins.

- [x] T004 [P] Create `mini4wd-motor-driver/hardware/rev1/design-inputs.md` with the README/prompt/SVG source hierarchy, approved 1.6 mm thickness, no-existing-EPRJ2 rule, and unresolved assumptions to be closed before release.
- [x] T005 [P] Verify XIAO MG24 Sense castellated pad numbering, pitch, outline, and orientation against Seeed source files; preserve the user-confirmed `D0 -> D0:VBAT SENSE` assignment and record the complete edge-pad map in `mini4wd-motor-driver/hardware/rev1/manufacturing/review/xiao-interface-review.md`.
- [x] T006 [P] Verify the Molex Micro-Fit 3.0 two-circuit SMD right-angle header drawing, 43650-0214 footprint/land data, 1.60 mm recommended PCB thickness, maximum contact rating, and mating housing/terminal pair; record exact manufacturer numbers and source links in `mini4wd-motor-driver/hardware/rev1/manufacturing/bom.csv`.
- [X] T007 Select manufacturer parts and packages for every circuit block in the README hardware specification; record values, ratings, footprints, and source documents in `mini4wd-motor-driver/hardware/rev1/manufacturing/bom.csv` and unresolved design assumptions in `mini4wd-motor-driver/hardware/rev1/design-inputs.md`.
- [X] T027 Complete datasheet-based passive design for the documented circuit functions; record selected values, candidate MPNs, and any recommendations that conflict with the no-additions constraint in `mini4wd-motor-driver/hardware/rev1/manufacturing/review/passive-design-review.md`. Do not add resistor/capacitor placements.
- [X] T008 Create the complete schematic and net assignments in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`, preserving the documented N-channel low-side drive, P-channel short brake, power sensing, temperature sensing, and XIAO signal mapping.
- [X] T009 Review the schematic connectivity and component ratings against `specs/001-smt-gerber-board/contracts/board-interface-and-fabrication.md`; record the reviewed netlist and any closed assumptions in `mini4wd-motor-driver/hardware/rev1/manufacturing/review/schematic-review.md`.

**Checkpoint**: The source project and verified circuit inputs are ready for PCB layout.

---

## Phase 3: User Story 1 - Produce a Manufacturable SMT Motor Driver Board (Priority: P1) 識 MVP

**Goal**: Complete a two-layer, all-SMT board design and reviewable fabrication package for the 5 A motor-driver target.

**Independent Test**: Review the saved design against the interface contract; confirm zero through-hole components, correct net connectivity, 1.6 mm nominal thickness, approximately 55 ﾃ・21 mm outline, no unresolved DRC findings, and correctly aligned Gerber layers accepted by the selected fabricator's file checker.

### Implementation for User Story 1

- [X] T010 [US1] Add verified component footprints, including XIAO MG24 Sense castellated pads and both Molex 43650-0214 headers, to `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`.
- [X] T011 [US1] Confirm the two-copper-layer stackup, set nominal 1.6 mm thickness, and verify the approximately 55 ﾃ・21 mm physical board outline in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`.
- [X] T012 [US1] Place the two Micro-Fit headers at opposite board ends facing outward and place all other components on the top side in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`.
- [X] T013 [US1] Route B+, B竏・ M竏・ and other high-current paths with documented copper geometry, and route gate-drive, PWM, sensing, and 5 V nets in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`.
- [X] T014 [US1] Complete schematic/netlist checks and PCB DRC; resolve connectivity, short, clearance, footprint, mask, and outline findings in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`.
- [x] T015 [US1] Record the user's decision to inherit the existing toy-board current/thermal design without a separate 5 A qualification gate; do not claim independent qualification evidence.
- [X] T016 [US1] Export the complete two-layer Gerber and required drill files from the saved project to `mini4wd-motor-driver/hardware/rev1/manufacturing/gerber/`.
- [X] T017 [US1] Export matching assembly BOM and pick-and-place files to `mini4wd-motor-driver/hardware/rev1/manufacturing/bom.csv` and `mini4wd-motor-driver/hardware/rev1/manufacturing/pick-and-place.csv`.
- [X] T018 [US1] Inspect every exported layer together in a Gerber viewer and record scale, registration, board outline, masks, silkscreen, and drill review in `mini4wd-motor-driver/hardware/rev1/manufacturing/review/gerber-review.md`.

**Checkpoint**: The editable board and fabrication outputs are internally reviewed and ready for vehicle-envelope validation.

---

## Phase 4: User Story 2 - Verify the Battery-Facing SMT Surface (Priority: P2)

**Goal**: Confirm the battery-facing underside follows the all-SMT and flat-surface requirements.

**Independent Test**: Inspect the underside manufacturing layers for through-hole component leads and untented vias.

### Implementation for User Story 2

- [X] T019 [US2] Inspect the battery-facing copper, solder mask, vias, and component pads in `mini4wd-motor-driver/mini4wd-motor-driver.eprj2`; tent all underside vias and ensure no through-hole lead or exposed solder feature protrudes toward the batteries.
- [x] T020 [US2] Waived per user decision: no separate assembled-board/mated-connector vehicle clearance review is required.
- [x] T021 [US2] Waived per user decision: no vehicle installation-envelope measurement or fit evidence is required.
- [x] T022 [US2] Waived per user decision: no layout change or repeat review is required for unassessed vehicle-clearance findings.

**Checkpoint**: The board has a verified battery-facing surface and documented physical fit.

---

## Phase 5: Polish & Release

**Purpose**: Freeze one reviewed project revision and validate the complete manufacturing package.

- [X] T023 Create `mini4wd-motor-driver/hardware/rev1/manufacturing/layer-map.md` mapping every exported file to the selected fabricator's layer input.
- [X] T024 Re-export Gerber, drill, BOM, and pick-and-place files from the final saved project revision to `mini4wd-motor-driver/hardware/rev1/manufacturing/` after all electrical or mechanical revisions.
- [X] T025 Upload the Gerber archive for the final revision to the selected fabricator's file checker and save the result and final review renders in `mini4wd-motor-driver/hardware/rev1/manufacturing/review/`.
- [X] T026 Update `mini4wd-motor-driver/hardware/rev1/README.md` with final revision identifiers, source requirements, manufacturing outputs, passed release gates, and regeneration instructions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; creates the output project and artifact locations.
- **Foundational (Phase 2)**: Depends on setup. Schematic work follows source and part verification; it blocks both user stories.
- **User Story 1 (Phase 3)**: Depends on the completed schematic and verified footprints from Phase 2.
- **User Story 2 (Phase 4)**: Depends on the reviewed board and exported preview from User Story 1; any mechanical revision requires affected electrical and fabrication checks to be repeated.
- **Polish & Release (Phase 5)**: Depends on User Story 1 and User Story 2 review gates passing.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; delivers the editable board and reviewed fabrication outputs as the MVP.
- **US2 (P2)**: Uses the US1 board placement and connector models; it begins after US1's board and preliminary exports are ready, and release requires its fit findings to be resolved.

### Parallel Opportunities

- T004, T005, and T006 can be prepared in parallel after T001窶典003 because they verify different inputs and artifacts.
- Within US1, no parallel CAD edits are assumed because schematic, footprints, placement, and routing share the same EasyEDA project file.
- Within US2, the underside inspection and mated-connector fit inspection can be performed in parallel after the same board revision is available.

## Parallel Example: Foundational Input Verification

```text
Task: T004 Record authoritative requirements and unresolved assumptions in mini4wd-motor-driver/hardware/rev1/design-inputs.md
Task: T005 Verify the XIAO MG24 Sense pad geometry and mapping in mini4wd-motor-driver/hardware/rev1/manufacturing/review/xiao-interface-review.md
Task: T006 Verify Molex Micro-Fit part, footprint, rating, and mating parts in mini4wd-motor-driver/hardware/rev1/manufacturing/bom.csv
```

## Implementation Strategy

### MVP First (User Story 1)

1. Complete setup and foundational source/component verification.
2. Complete the new schematic and two-layer EasyEDA board.
3. Complete circuit/DRC review, Gerber export, and Gerber-viewer inspection. Independent thermal qualification is waived.
4. Validate the board independently against the US1 criteria before proceeding to final release.

### Incremental Delivery

1. Establish the clean project and verified circuit inputs.
2. Deliver the US1 editable board and preliminary fabrication package.
3. Complete US2 underside and vehicle-fit review; revise and recheck the board if needed.
4. Re-export the final revision and pass the fabricator file checker.

## Notes

- Every task has a checkbox, unique sequential ID, and a concrete artifact path.
- `[P]` marks only independent input-verification work on separate artifacts.
- T006 manufacturer data is recorded in `mini4wd-motor-driver/hardware/rev1/manufacturing/bom.csv` and `manufacturing/review/molex-interface-review.md`. EasyEDA footprint placement and visual fit are part of T010 and later mechanical review.
- T027 is a datasheet-design and scope gate: passive values must follow documented functions and manufacturer guidance, while the explicit no-additions constraint on resistor/capacitor placements remains in force. See `passive-design-review.md` for resolved values and remaining conflicts.
- The active project was confirmed through the EasyEDA bridge. Only this user-designated target is in scope; other `.eprj2` files remain excluded.
- The legacy `mini4wd-motor-driver/docs/hardware_spec.md` remains an input record for the existing board; new revision thickness is 1.6 mm as recorded in `prompt.md` and `spec.md`.
- Do not release Gerbers until circuit/netlist, DRC, viewer, and fabricator checks are recorded. Mechanical vehicle clearance and independent thermal qualification are waived per user decision.
