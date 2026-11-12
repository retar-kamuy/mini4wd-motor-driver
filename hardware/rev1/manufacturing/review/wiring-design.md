# Rev1 Wiring Design Decisions

Date: 2026-10-11  
Status: Codex design proposal based on the documented source-board behavior and the approved rev1 requirements. These decisions resolve connectivity that the routing SVGs do not identify. They are not claims about the original board's hidden netlist.

## Governing constraints

- Preserve the documented forward-only N-channel low-side drive and P-channel short-brake behavior.
- One MG24 PWM signal selects drive when high and short brake when low.
- Use the selected UCC27511, TPS61023, Q1, Q2, NTC, and existing passive positions in the BOM.
- Do not increase resistor or capacitor placement counts. Do not add gate resistors or pull resistors whose source-board positions have not been verified.
- The prompt explicitly calls for flyback protection. Seeed requires a diode between an external supply and the XIAO 5V pin. These are diode functions, not resistor/capacitor additions.
- A source SVG trace establishes a connection only where geometry is continuous. The rest of the nets below are rev1 design decisions.

## Net definitions

| Net | Connect these pins / terminals | Basis |
|---|---|---|
| `GND` | J1 battery negative; Q1 source; Q2 gate-driver return; U1 pin 4; U2 pin 4; CIN/COUT1/COUT2/C_BYPASS ground terminals; lower ends of R_VBAT_LO, R_MID_LO, and TH1 temperature divider; XIAO GND | Required common return for the documented topology and device application circuits |
| `VBAT` | J1 battery positive; J2 motor `M+`; U2 VIN (pin 3) and EN (pin 2); CIN input terminal; L1 input terminal; R_VBAT_HI upper terminal; Q2 source pins 1–3; D_FLYBACK cathode | Source-board battery/M+ relationship and TPS61023 boost input design |
| `MOTOR_MINUS` | J2 motor `M-`; Q1 drain; Q2 drain pins; R_MID_HI upper terminal; D_FLYBACK anode | Source-board M- is the switched node and is the P-channel brake return |
| `GATE` | U1 OUTH (pin 2), U1 OUTL (pin 3), Q1 gate, Q2 gate | Shared drive/brake control. UCC27511 logic table explicitly supports OUTH/OUTL tied together: one output sources high while the other is high impedance; on low, OUTH is high impedance and OUTL sinks low. This yields Q1 on/Q2 off for PWM high and Q1 off/Q2 on for PWM low, given Q2 source at VBAT. |
| `PWM` | XIAO D2 / PC2 / MOTOR PWM; U1 IN+ (pin 6) | Documented signal mapping and noninverting driver configuration |
| `GND` (input disable) | U1 IN- (pin 5) | TI specifies IN- tied to GND to enable noninverting operation; do not leave floating |
| `BOOST_SW` | U2 SW (pin 5); L1 switched terminal | TPS61023 boost topology |
| `BOOST_5V` | U2 VOUT (pin 6); R_BOOST_FB_HI top; R_BOOST_FB_LO top network; COUT1/COUT2 positive terminals; U1 VDD (pin 1); D_XIAO anode | Boost output at nominal 5 V. U1 uses the un-dropped rail to retain its 4.5 V minimum operating supply. |
| `BOOST_FB` | U2 FB (pin 1); junction of R_BOOST_FB_HI and R_BOOST_FB_LO | 732 kΩ from BOOST_5V and 100 kΩ to GND sets the documented 5 V target |
| `XIAO_5V` | D_XIAO cathode; XIAO 5V pad | D_XIAO is oriented from BOOST_5V toward the XIAO 5V pin to block USB-side backfeed |
| `VBAT_SENSE` | XIAO D0 / PC0; junction R_VBAT_HI to VBAT and R_VBAT_LO to GND | User-confirmed D0 destination and specified 22 kΩ:10 kΩ divider |
| `MID_SENSE` | XIAO D3 / PC3; junction R_MID_HI to MOTOR_MINUS and R_MID_LO to GND | Documented M- measurement and 22 kΩ:10 kΩ divider |
| `NTC_TEMP` | XIAO D1 / PC1; junction R_NTC to 3V3 and TH1 to GND | Documented 10 kΩ fixed resistor + 10 kΩ NTC divider; use the XIAO 3V3 pad as excitation |
| `3V3` | XIAO 3V3 pad; upper terminal of R_NTC | Uses the XIAO regulated output for the low-current NTC divider |

For two-pin capacitors, polarity is not applicable: CIN is between VBAT and GND; COUT1 and COUT2 are between BOOST_5V and GND; C_BYPASS is directly between U1 VDD and GND. Existing library symbol pin labels 1/2 are not a substitute for checking the physical capacitor terminals during PCB assignment.

## Diode selections

- `D_XIAO`: Vishay SS14-E3/61T Schottky, 1 A / 40 V, SMA. Anode to BOOST_5V, cathode to XIAO_5V. This implements Seeed's external-supply diode direction and keeps the gate-driver rail at the undropped 5 V node.
- `D_FLYBACK`: SS54 Schottky, 5 A / 40 V, SMA. Anode to MOTOR_MINUS, cathode to VBAT/M+. This is the flyback clamp explicitly required by `specs/001-smt-gerber-board/spec.md`; it is in parallel with the P-channel brake path and does not add a resistor or capacitor position.

These selections establish nominal parts and orientation, not independent thermal/current qualification. Confirm the manufacturer's package land patterns and exact EasyEDA library devices before layout freeze.

## Important limitations of this design decision

- The source SVGs do not expose net names. Therefore the complete J1/J2, divider, boost, and MOSFET net assignments above are rev1 design decisions, except where a trace endpoint or user-confirmed label independently agrees.
- The P-channel device's gate is driven by the same 0 V/5 V gate net as Q1. This makes its static states match the documented one-PWM behavior: at low, Q2 clamps M- to M+; at high, Q2 is off while Q1 drives M- low. Switching overlap/deadtime is not independently characterized, consistent with the user's acceptance of the existing toy-board behavior; do not claim it has been validated.
- No separate gate resistor or P-channel gate pull-up is introduced. The UCC27511's complementary high-impedance output states allow its split outputs to form the shared gate net, and its active high level holds Q2 off for the supported battery rails. Keep the driver close to Q1/Q2 and C_BYPASS as the TI layout guidance requires.
- `BOOST_5V` must feed U1 directly. Only the XIAO branch passes through D_XIAO; putting that diode before U1 could reduce the driver supply below its 4.5 V operating minimum.
- The current schematic is still missing the XIAO symbol/pad, J1/J2 symbols, and both diodes. This file defines their electrical roles but does not claim they have already been placed or routed in EasyEDA.

## Sources

- Existing-board behavior and named signals: `mini4wd-motor-driver/README.md`, `docs/hardware_spec.md`, `docs/pwm_and_brake.md`, and `docs/wiring_and_usage.md`.
- Seeed, [XIAO MG24 getting started and pin map](https://wiki.seeedstudio.com/xiao_mg24_getting_started/): external 5 V input must be connected through a diode, anode at the external source and cathode at the 5V pad; D0–D3 mappings.
- TI, [UCC27511 datasheet](https://www.ti.com/lit/ds/symlink/ucc27511.pdf): pin functions, IN- grounding for noninverting mode, split-output logic table, 0.1 µF plus a few-µF recommended parallel bypass, and layout guidance.
- TI, [TPS61023 datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf): VIN/SW/VOUT/FB topology, 5 V application network, and EN behavior.
- Device datasheets and landing patterns are catalogued in `manufacturing/bom.csv`; verify supplier availability before ordering.
