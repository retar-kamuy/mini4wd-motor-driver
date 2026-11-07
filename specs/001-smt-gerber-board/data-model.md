# Design Data Model

## Board Project

Represents the editable rev1 board in the user-designated active EasyEDA project. It owns one schematic, one two-layer PCB, project configuration, and locally defined components/footprints as needed, reconstructed from the approved written requirements and visual references.

**Validation rules**:

- Project revision and source requirements are recorded.
- The schematic and PCB belong to the same project revision.
- All locally created symbols and footprints have source references and revision notes.

## Schematic Component

Represents an electrical part or interface instance: designator, value, manufacturer part number, schematic symbol, footprint, electrical role, and source reference.

**Validation rules**:

- Every placed component has a known value and electrical pin mapping.
- Every assembly component has a verified SMD footprint and manufacturer drawing.
- No through-hole component is allowed.
- XIAO MG24 Sense is a module-level assembly component mounted through its castellated pads.

## Net and Board Interface

Represents a named electrical connection and its pins, including supply/motor connectors and the MG24 interface.

**Validation rules**:

- Pin numbers and net names match [the interface contract](contracts/board-interface-and-fabrication.md).
- Battery positive and motor positive are one common electrical net as described by the README.
- Battery negative and motor negative remain distinct nets.
- PWM, VBAT sense, MID sense, NTC, 5 V, and GND are explicitly represented.
- No unconnected or shorted nets remain at release.

## PCB Stackup and Outline

Represents the two copper layers, masks, silkscreens, nominal 1.6 mm board thickness, approximately 55 ﾃ・21 mm outline, via treatment, and component-side orientation.

**Validation rules**:

- Board outline is a single closed physical contour with specified dimensions.
- All underside vias are tented and no through-hole pads or leads protrude on the battery-facing surface.
- Component placement and connector mating volumes fit the vehicle envelope.
- The selected Molex footprint uses the manufacturer-recommended 1.6 mm board thickness.

## Manufacturing Package

Represents a generated revision of Gerber layers, drill data, BOM, pick-and-place coordinates, layer map, and review renders.

**Validation rules**:

- All files come from the same saved design revision.
- Gerber units, drill coordinate format, layer identity, and board outline are documented.
- Gerber layers align in a viewer and meet the selected fabricator's import checks.
- The archive has no unresolved connectivity, DRC, thermal, or mechanical release findings.

## Design Review Record

Represents the release evidence for electrical behavior, 5 A current/thermal review, connector fit, bottom-side safety, DRC, Gerber preview, and fabrication-service validation.

**State progression**: Draft 竊・Schematic Reviewed 竊・Layout Reviewed 竊・Manufacturing Preview Reviewed 竊・Released.

**Validation rules**:

- A state can advance only when the relevant gate in `plan.md` passes.
- A source change after export invalidates the prior manufacturing preview and requires re-export and review.
