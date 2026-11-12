# XIAO MG24 Sense Interface Review

Review date: 2026-10-04  
Status: complete for the 14 castellated edge pads; orientation is cross-checked against the user's D0 location and the legacy board render.

## Verified module information

Seeed's XIAO MG24(Sense) hardware page specifies a 21 × 17.8 mm module and publishes this pad map:

| XIAO pad | MCU pad | Use in motor-driver board |
|---|---|---|
| 5V | VBUS | 5V_OUT supplied by the board through reverse-current protection |
| GND | GND | GND |
| D0 | PC00 | VBAT_SENSE |
| D1 | PC01 | NTC_TEMP |
| D2 | PC02 | MOTOR_PWM |
| D3 | PC03 | MID_SENSE |
| D4 | PC04 / SDA | Optional future sensor SDA breakout |
| D5 | PC05 / SCL | Optional future sensor SCL breakout |

The mapping agrees with the legacy README's PC0–PC3 roles. The user prompt additionally asks for optional SDA/SCL pads, so the new board interface contract must include those two optional breakout signals.

## User-confirmed D0 connection

The user confirmed that XIAO MG24 Sense `D0` must connect to the board's `D0:VBAT SENSE` position shown in `docs/pcb_front_3D.png`. Matching that position to Seeed's pad order fixes the module rotation: viewed as `pcb_front_3D.png`, pad 1 / 5V is at the upper-left and pad 14 / D0 is at the lower-left. This is a 180-degree rotation from the cited KiCad footprint's unrotated coordinate view. Use the mapping below in EasyEDA.

## Footprint source and geometry

The official Seeed GitHub library contains `XIAO-MG24-SMD.kicad_mod` and a separate `XIAO-MG24-DIP.kicad_mod`. The SMD footprint's edge-contact array is:

- 14 numbered edge pads, seven on each long side.
- 2.54 mm pitch along each row.
- Each edge pad is 2.75 × 2.00 mm.
- Pad centers span x = -7.62 mm to +7.62 mm; row centers are y = ±8.0825 mm in the source footprint coordinates.
- The courtyard is approximately 20.95 × 17.78 mm, consistent with Seeed's published 21 × 17.8 mm module size.
- Pin-1 marker is at the positive-x end of the first row in the KiCad footprint coordinates.

The library also defines additional inner pads (15 onward). They are not part of the 14 castellated edge-contact interface shown on the module perimeter and are not used by this board interface. Do not import or connect these inner pads as castellated contacts; use only edge pads 1–14 for the module-to-board footprint.

The GitHub repository's `projects/` directory does not list a standalone MG24 board project. It does contain the complete SMD footprint. Seeed's MG24 Wiki separately links a full KiCad project ZIP, which is a different resource from the GitHub footprint library.

## Seeed sources

- Manufacturer hardware page: https://wiki.seeedstudio.com/xiao_mg24_getting_started/
- Official GitHub SMD footprint: https://github.com/Seeed-Studio/OSHW-XIAO-Series/blob/main/Seeed%20Studio%20XIAO%20Series%20Library/XIAO-MG24-SMD.kicad_mod
- Official GitHub DIP footprint: https://github.com/Seeed-Studio/OSHW-XIAO-Series/blob/main/Seeed%20Studio%20XIAO%20Series%20Library/XIAO-MG24-DIP.kicad_mod
- Official GitHub projects directory: https://github.com/Seeed-Studio/OSHW-XIAO-Series/tree/main/projects
- XIAO MG24 Sense KiCad project archive linked by Seeed: https://files.seeedstudio.com/wiki/XIAO_MG24/Getting_Start/XIAO_MG24_v1.0_KiCad_260114.zip
- XIAO Series footprint archive linked by Seeed: https://files.seeedstudio.com/wiki/XIAO-KiCad-Library/New_XIAO_Series_Footprints.zip

## Complete edge-pad map in the legacy front-render orientation

`pcb_front_3D.png` viewed as shown, with columns numbered left-to-right, gives this reconciled footprint map:

| Column | Upper row: Seeed pad / signal | Lower row: Seeed pad / signal | Board net/use |
|---:|---|---|---|
| 1 | 1 / 5V (VBUS) | 14 / D0 (PC00) | 5V_OUT / `D0:VBAT SENSE` (VBAT_SENSE) |
| 2 | 2 / GND | 13 / D1 (PC01) | GND / `D1:NTC TEMP` (NTC_TEMP) |
| 3 | 3 / 3V3 | 12 / D2 (PC02) | 3V3 / `D2:MOTOR PWM` (MOTOR_PWM) |
| 4 | 4 / D10 (PA05) | 11 / D3 (PC03) | Unused / `D3:MID SENSE` (MID_SENSE) |
| 5 | 5 / D9 (PA04) | 10 / D4 (PC04 / SDA) | Unused / optional SDA breakout |
| 6 | 6 / D8 (PA03) | 9 / D5 (PC05 / SCL) | Unused / optional SCL breakout |
| 7 | 7 / D7 (PC07) | 8 / D6 (PC06) | Unused / unused |

The upper-row 5V, GND, and 3V3 labels and lower-row D0–D3 labels match the render and Seeed pin map. Keep the prompt-requested SDA/SCL breakout on edge pads 10 and 9 respectively. All other unused edge pads remain unconnected. This closes pad-number, net, and orientation reconciliation; the live EasyEDA placement must preserve this mapping.
