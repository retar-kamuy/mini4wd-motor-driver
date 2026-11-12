# SVG Routing Source Review

Review date: 2026-10-11  
Status: Source geometry extracted; endpoint-to-component mapping is still in progress.

## Source and coordinate frame

- `docs/pcb_front.svg` displays the top copper and front silkscreen.
- `docs/pcb_back.svg` displays the bottom copper and back silkscreen.
- Both SVGs use the same board coordinate frame. The board outline spans approximately X=4020–4236.5 and Y=3169.8–3252.5 in SVG coordinates.
- The edge-pad centers visible in the SVG are X=4031, 4041, 4051, 4061, 4071, 4081, 4091; upper row Y≈3179 and lower row Y≈3242.6. The pad roles/orientation use `xiao-interface-review.md`, including the user's D0 confirmation.
- The SVG exports store copper as geometry; the copper primitives do not contain net names. A path touching a pad establishes geometric connectivity, but component identity at its far endpoint still needs to be matched to the footprint/pad drawing.

## MG24 edge-pad routes identified

The following routes were read from the copper polylines and matched to their MG24 edge pad by endpoint coordinates. “Far endpoint” is recorded as geometry only until matched to the corresponding part pad.

| MG24 pad | Signal from interface map | Copper primitive(s) | Far endpoint / observation |
|---|---|---|---|
| Upper row, column 1 (pad 1) | 5V | Top `gge66777_1` | (4122.74, 3218.00) |
| Upper row, column 2 (pad 2) | GND | Top `gge66780_1` | (4114.00, 3202.00) |
| Upper row, column 3 (pad 3) | 3V3 | Top `gge66774_1` | (4116.275, 3177.333) |
| Lower row, column 1 (pad 14) | D0 / VBAT_SENSE | Top `gge66771_1` | (4119.76, 3235.26) |
| Lower row, column 2 (pad 13) | D1 / NTC_TEMP | Top `gge51138_1` → bottom `gge50568_2` → top `gge67889_1` → top `gge66957_1` | Top/bottom transition (4043.00, 3230.50); bottom/top transition (4100.50, 3194.50); reaches pad geometry at (4122.2065, 3177.3333) |
| Lower row, column 3 (pad 12) | D2 / MOTOR_PWM | Top `gge51003_1` → bottom `gge66786_2` → top `gge66927_1` | Top/bottom transition (4052.00, 3230.50); bottom/top transition (4126.50, 3181.50); reaches pad geometry at (4161.034, 3177.00) |
| Lower row, column 4 (pad 11) | D3 / MID_SENSE | Top `gge68873_1` | (4115.50, 3248.466) |

The D0 route matches the user's explicit confirmation that MG24 D0 connects to the board's `D0:VBAT SENSE` position. The D1–D3 roles come from the legacy interface labels and the reviewed pad map; the physical trace starts agree with those edge-pad locations.

## Additional trace continuity established

- D1 continues from bottom copper at (4100.5, 3194.5), follows top trace `gge67889_1` to (4116.48, 3185.83), then top trace `gge66957_1` to pad geometry at (4122.2065, 3177.3333).
- D2 continues from bottom copper at (4126.5, 3181.5), then top trace `gge66927_1` reaches pad geometry at (4161.034, 3177.0).
- These coordinates establish copper continuity only. Destination component identities and pin numbers remain unresolved; proximity to a polygon center does not establish pad identity.
- D0's far endpoint at (4119.76, 3235.26) lies in a dense component-pad area. D3 ends at (4115.5, 3248.466), while the bottom perimeter trace ends separately at (4110, 3246). Do not join these based on proximity; no common endpoint is present in the SVG geometry.

## Other copper geometry

- The front/top copper contains multiple wide polylines around the MOSFETs and connector pads at the right side of the board. The SVG widths include 3.937 and 7.874 coordinate units in that power section. These are layout references for the high-current route; the net of each segment must be established by tracing its complete pad-to-pad path.
- The back/bottom copper includes `gge69461_2` from (4215, 3198) around the board edge to (4110, 3246), in addition to the D1 and D2 routes above. Its endpoint component pads are not yet identified.
- The component/body pads and fine traces are present in the front/top copper image, but the exported SVG has no net names or reference-designator metadata on those copper objects. Do not assign a net solely from proximity or from a generic IC reference circuit.

## EasyEDA implementation state

- The schematic component placements remain in the active EasyEDA project.
- Provisional net flags, ports, and trial routes based on guessed connectivity were removed after the user directed that the two routing SVGs be the wiring reference.
- The schematic is currently saved with no wire primitives or net flags/ports. Use the extracted path map to identify endpoints before drawing the next connections.
- An empty result from EasyEDA's net-list API is not treated as connectivity evidence; connectivity must be confirmed from actual schematic wires and the exported/visible netlist.
