# Legacy PCB Layout Reference Review

Review date: 2026-10-04  
Status: reviewed as visual and connectivity-label references; not a source netlist.

## Sources reviewed

- `mini4wd-motor-driver/docs/hardware_spec.md`
- `mini4wd-motor-driver/docs/pcb_front.svg`
- `mini4wd-motor-driver/docs/pcb_back.svg`
- `mini4wd-motor-driver/docs/pcb_front_3D.png`
- `mini4wd-motor-driver/docs/pcb_back_3D.png`

## Transcribed circuit information

The hardware specification and the back-side legend establish these named nodes and interfaces:

| Signal / node | Recorded meaning |
|---|---|
| B+ / M+ | Battery positive and motor positive are common |
| B- | Battery negative |
| M- | Motor negative; switched low-side node |
| XIAO 5V | 5V_OUT |
| XIAO GND | GND |
| PC0 / D0 | VBAT_SENSE |
| PC1 / D1 | NTC_TEMP |
| PC2 / D2 | MOTOR_PWM |
| PC3 / D3 | MID_SENSE |

The back-side legend states that VBAT_SENSE and MID_SENSE use a 22 kΩ:10 kΩ divider and that the original voltage is reconstructed as ADC voltage × 3.2. The hardware specification also records a 10 kΩ fixed resistor with the 10 kΩ NTC thermistor.

The component requirements transcribed from `hardware_spec.md` are the Vishay SiSS64DN-T1-GE3 N-channel MOSFET, Vishay SI7137DP-T1-GE3 P-channel MOSFET, TI UCC27511DBVR gate driver, TI TPS61023DRLR boost converter, and TDK NTCG104BH103JT1 thermistor. The documentation does not give the boost inductor/capacitor MPNs, resistor MPNs/packages/tolerances, or reverse-current diode MPN.

## Rendered-board observations

The R/C candidate audit is recorded in `passive-position-inventory.md`. Five resistor functions/values are documented (two 22 kΩ:10 kΩ dividers and one 10 kΩ NTC fixed resistor). The two boost-feedback resistors and four capacitors in the candidate BOM derive from TI reference material, not confirmed source-board part values. The rendered source does not expose readable R/C designators or enough detail to verify a complete passive footprint count; therefore it cannot establish a one-to-one BOM map by itself.

- The front render labels the XIAO interface pads with 5V, GND, 3V3, D0:VBAT SENSE, D1:NTC TEMP, D2:MOTOR PWM, and D3:MID SENSE.
- The power/motor end is labeled B-, M-, M+, and B+. Preserve the documented common B+/M+ node and separate B-/M- roles when rebuilding the circuit.
- The back render says “XIAO MG24 Sense ONLY” and “2-cell Ni-MH / 1S Li-ion ONLY”; it warns against 2S Li-ion.
- The SVGs contain copper geometry on top and bottom layers, but their exported primitive records have no net names. They guide visual routing and placement; they do not by themselves prove the electrical netlist or component pin mapping.
- The rendered legacy board shows its original connector and physical arrangement. The rev1 board must use the separately approved SMD Micro-Fit headers and must not copy the old outline scale from the SVG viewBox.

## Design use

Use this record with the board interface contract to reconstruct the schematic. Verify each trace-to-pad connection from the labeled nodes and electrical topology, then record the resulting EasyEDA netlist in `schematic-review.md`. Any path whose endpoints cannot be distinguished in the rendered references remains unresolved until the schematic is reviewed.
