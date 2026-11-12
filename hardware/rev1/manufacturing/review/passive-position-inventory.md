# Legacy Passive Position Inventory

Review date: 2026-10-11  
Status: partial inventory complete; no breadboard or physical prototype is needed for this document review.

**Superseded approach:** Following the user's 2026-10-11 direction, passive selection now proceeds from component datasheets and documented circuit functions; it does not try to infer the original BOM from SVG/3D images. See `passive-design-review.md`. This audit remains as the record of why the original passive footprint count cannot be proven from those renders.

## Source limits

Reviewed `docs/hardware_spec.md`, `docs/pcb_front.svg`, `docs/pcb_back.svg`, and both 3D renders. The SVG exports show board artwork and copper geometry but do not expose component reference designators or net names. The 3D renders show mounted packages but do not label individual R/C references or values. Consequently, the source files support identification of documented circuit functions and a visual placement comparison, but they do not currently support a reliable, complete count of individual resistor and capacitor footprints or a unique one-to-one location map.

Do not infer a part value from package size or from a TI example circuit. A footprint visible in a render is not enough to identify whether it is a resistor or capacitor when there is no readable reference/value marking.

## BOM candidate review

| Candidate BOM references | Candidate quantity | What the project source confirms | What remains unconfirmed | Disposition for rev1 |
|---|---:|---|---|---|
| R_VBAT_HI, R_VBAT_LO | 2 | `hardware_spec.md` documents a 22 kΩ:10 kΩ divider for VBAT_SENSE. | Exact two footprint locations, package, tolerance, and MPN. | Values/functions may be retained as requirements; do not claim the candidate 0603 MPNs or placements are source-verified. |
| R_MID_HI, R_MID_LO | 2 | `hardware_spec.md` documents a 22 kΩ:10 kΩ divider for MID_SENSE. | Exact two footprint locations, package, tolerance, and MPN. | Values/functions may be retained as requirements; do not claim the candidate 0603 MPNs or placements are source-verified. |
| R_NTC | 1 | `hardware_spec.md` documents a 10 kΩ fixed resistor with the 10 kΩ NTC. | Exact footprint location, package, tolerance, and MPN. | Value/function may be retained as a requirement; do not claim the candidate 0603 MPN or placement is source-verified. |
| R_BOOST_FB_HI, R_BOOST_FB_LO | 2 | TPS61023 5 V converter is listed in the hardware specification; TI's typical 5 V design specifies 732 kΩ/100 kΩ. | Whether the original board has the same exact positions and values. | Values are adopted for the datasheet-based design in `passive-design-review.md`; they are not evidence of original-board placement. |
| CIN | 1 | A 5 V boost converter is documented; TI's typical design specifies 10 µF. | Whether the original board has the same exact position, value, package, and MPN. | 10 µF is adopted for the datasheet-based design; it is not evidence of original-board placement. |
| COUT1, COUT2 | 2 | A 5 V boost converter is documented; TI's typical design specifies 2 × 22 µF. | Whether the original board has two positions and whether the candidate parts retain sufficient effective capacitance. | 2 × 22 µF is adopted as the initial datasheet-based design; confirm effective capacitance and do not claim original-board placement. |
| C_BYPASS | 1 | TI recommends 0.1 µF close to UCC27511 VDD/GND. | Whether an existing allowed capacitor position can serve this function; the UCC datasheet also recommends a larger parallel capacitor. | Reassigned to UCC27511 local bypass in the datasheet-based design; a second capacitor is held pending the no-additions constraint. |

The BOM therefore contains **7 resistor candidates** (5 tied to documented sensor/divider functions and 2 reference-derived boost-feedback candidates) and **4 capacitor candidates** (all reference-derived). These are candidate quantities, not a verified count of the source board's footprints.

## Conclusion and closure rule

This is a historical layout audit, not the current component-selection method. Datasheet-derived values are now recorded in `passive-design-review.md`. The exact original-board footprint count remains unknown, so preserve the no-additions constraint and do not claim the selected component count is an exact copy of the source.
