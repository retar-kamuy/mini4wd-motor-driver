# Phase 1 Data Model: Mini 4WD Motor Driver KiCad Architecture

**Branch**: `002-port-to-kicad` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

This document formalizes the entities, properties, data structures, and relationships comprising the native KiCad hardware project.

---

## 1. Entity: KiCadProject

Represents the top-level project container governing the schematic, PCB layout, and design rule definitions.

- **Project File**: `mini4wd-motor-driver.kicad_pro`
- **Location**: `mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver/`
- **KiCad Version**: 10.0 (Windows)
- **Stackup Specification**:
  - Layers: 2 copper layers (`F.Cu`, `B.Cu`)
  - Substrate: FR-4, $1.60\ \text{mm}\ \pm 10\%$
  - Copper Weight: 1 oz ($35\ \mu\text{m}$) on outer layers
  - Finish: Lead-Free HASL or ENIG (electroless nickel immersion gold)
  - Solder Mask: Blue or Matte Black, both sides
  - Silkscreen: White, both sides
- **Netclasses**:
  - `Default`: Trace width 0.25 mm, clearance 0.20 mm, via diameter 0.6 mm, via drill 0.3 mm.
  - `Power_5A`: Trace width 1.50 mm (nominal 2.0 mm), clearance 0.30 mm, via diameter 0.8 mm, via drill 0.4 mm.
    - Assigned Nets: `VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`, `BOOST_5V`.

---

## 2. Entity: SchematicComponent

Represents a logical circuit symbol on the schematic page (`mini4wd-motor-driver.kicad_sch`), mapped to an authoritative manufacturer part and SMT footprint.

| RefDes | Quantity | Value / Device | Manufacturer | Manufacturer Part Number (MPN) | Package / Footprint | Function |
|---|---|---|---|---|---|---|
| **U1** | 1 | UCC27511DBVR | Texas Instruments | `UCC27511DBVR` | SOT-23-6 (`Package_TO_SOT_SMD:SOT-23-6`) | 4A/8A Low-Side Gate Driver (5V gate drive) |
| **Q1** | 1 | SiSS64DN-T1-GE3 | Vishay Siliconix | `SiSS64DN-T1-GE3` | PowerPAK 1212-8S | Low-side Motor Drive N-ch MOSFET (2.86 mΩ) |
| **Q2** | 1 | SI7137DP-T1-GE3 | Vishay Siliconix | `SI7137DP-T1-GE3` | PowerPAK SO-8 | High-side Short-Brake P-ch MOSFET |
| **U2** | 1 | TPS61023DRLR | Texas Instruments | `TPS61023DRLR` | SOT-5X3 (DRL-6) | 5V Boost Converter |
| **L1** | 1 | 1.0 µH | Coilcraft | `XEL4030-102ME` | 4.0 × 4.0 mm SMD (`mini4wd-motor-driver:Coilcraft_XEL4030`) | TPS61023 Boost Inductor (Restored from Würth) |
| **J1** | 1 | Micro-Fit 3.0 RA | Molex | `43650-0214` | 2-pin SMD RA (`mini4wd-motor-driver:Molex_MicroFit30_43650-0214`) | Battery Power Input (B+ / B-) |
| **J2** | 1 | Micro-Fit 3.0 RA | Molex | `43650-0214` | 2-pin SMD RA (`mini4wd-motor-driver:Molex_MicroFit30_43650-0214`) | Motor Drive Output (M+ / M-) |
| **MCU1** | 1 | XIAO MG24 Sense | Seeed Studio | `102010620` | 14-pin Castellated (`mini4wd-motor-driver:XIAO_MG24_Castellated_14P`) | Main Controller & 6-Axis IMU |
| **TH1** | 1 | 10 kΩ NTC | TDK | `NTCG104BH103JT1` | 0402 (`Resistor_SMD:R_0402_1005Metric`) | Board Temperature Sensing NTC |
| **D_FLY** | 1 | SS54-HF | Comchip | `SS54-HF` | DO-214AC SMA (`Diode_SMD:D_SMA`) | 5A 40V Schottky Motor Flyback Protection |
| **D_XIAO**| 1 | SS14-E3/61T | Vishay | `SS14-E3/61T` | DO-214AC SMA (`Diode_SMD:D_SMA`) | 5V Isolation Diode (prevents USB backfeed) |
| **CIN** | 1 | 10 µF 10V | Murata | `GRM188R61A106MAALD`| 0603 (`Capacitor_SMD:C_0603_1608Metric`)| Boost Input Bypass Capacitor |
| **COUT1** | 1 | 22 µF 10V | Murata | `GRM188R61A226ME15D`| 0603 (`Capacitor_SMD:C_0603_1608Metric`)| Boost Output Filter Capacitor 1 |
| **COUT2** | 1 | 22 µF 10V | Murata | `GRM188R61A226ME15D`| 0603 (`Capacitor_SMD:C_0603_1608Metric`)| Boost Output Filter Capacitor 2 |
| **C_BYP** | 1 | 0.1 µF 10V | Murata | `GRM155R61A104KA01D`| 0402 (`Capacitor_SMD:C_0402_1005Metric`)| Gate Driver VDD Local Bypass |
| **R_VBAT_H**| 1 | 22 kΩ 1% | Vishay | `CRCW060322K0FKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| VBAT Sense Upper Resistor |
| **R_VBAT_L**| 1 | 10 kΩ 1% | Vishay | `CRCW060310K0FKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| VBAT Sense Lower Resistor |
| **R_MID_H** | 1 | 22 kΩ 1% | Vishay | `CRCW060322K0FKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| MID (M-) Sense Upper Resistor |
| **R_MID_L** | 1 | 10 kΩ 1% | Vishay | `CRCW060310K0FKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| MID (M-) Sense Lower Resistor |
| **R_NTC** | 1 | 10 kΩ 1% | Vishay | `CRCW060310K0FKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| NTC Sense Fixed Pull-up Resistor |
| **R_FB_H** | 1 | 732 kΩ 1% | Vishay | `CRCW0603732KFKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| TPS61023 5V Feedback Upper Resistor |
| **R_FB_L** | 1 | 100 kΩ 1% | Vishay | `CRCW0603100KFKEA` | 0603 (`Resistor_SMD:R_0603_1608Metric`)| TPS61023 5V Feedback Lower Resistor |

---

## 3. Entity: ElectricalNet

Represents the logical interconnection between component pins.

| Net Name | NetClass | Voltage / Signal Type | Source / Driver | Sinks / Destinations |
|---|---|---|---|---|
| `VBAT` | `Power_5A` | 1.8 V – 3.2 V Power | J1 Pin 1 (B+) | U2 VIN/EN, L1 Pin 1, Q2 Source, R_VBAT_H, D_FLY Cathode, J2 Pin 1 (M+) |
| `GND` | `Power_5A` | 0 V Reference | J1 Pin 2 (B-) | MCU1 Pad 2, U1 GND, U2 GND, Q1 Source, CIN, COUT1/2, C_BYP, Dividers |
| `MOTOR_PLUS` | `Power_5A` | Battery Potential | Common `VBAT` node | J2 Pin 1 (M+), D_FLY Cathode |
| `MOTOR_MINUS`| `Power_5A` | Switched Low-Side Node| Q1 Drain / Q2 Drain | J2 Pin 2 (M-), D_FLY Anode, R_MID_H |
| `BOOST_5V` | `Power_5A` | 5.0 V Boost Output | U2 VOUT | U1 VDD, C_BYP, COUT1/2, R_FB_H, D_XIAO Anode |
| `XIAO_5V` | `Default` | 5.0 V Isolated MCU Power| D_XIAO Cathode | MCU1 Pad 1 (5V input) |
| `MCU_3V3` | `Default` | 3.3 V Logic Power | MCU1 Pad 3 (3V3 out) | R_NTC Pull-up |
| `PWM_DRIVE` | `Default` | 3.3 V PWM Signal | MCU1 Pad 5 (D2 / PWM)| U1 IN+ (Gate Driver input) |
| `GATE_DRIVE`| `Default` | 0 V / 5 V Gate Signal | U1 OUT / OUT_SPLIT | Q1 Gate (N-MOSFET), Q2 Gate (P-MOSFET invert/brake) |
| `VBAT_SENSE`| `Default` | 0 V – 3.3 V Analog Sense | R_VBAT_H / R_VBAT_L | MCU1 Pad 14 (D0 / A0) |
| `MID_SENSE` | `Default` | 0 V – 3.3 V Analog Sense | R_MID_H / R_MID_L | MCU1 Pad 6 (D3 / A3) |
| `TEMP_SENSE`| `Default` | 0 V – 3.3 V Analog Sense | R_NTC / TH1 | MCU1 Pad 4 (D1 / A1) |
| `I2C_SDA` | `Default` | 3.3 V Open-Drain Bus | MCU1 Pad 10 (SDA) | Auxiliary SMD Test Pad |
| `I2C_SCL` | `Default` | 3.3 V Open-Drain Bus | MCU1 Pad 9 (SCL) | Auxiliary SMD Test Pad |
| `SW_BOOST` | `Power_5A` | Boost Switching Node | L1 Pin 2 | U2 SW (Switching pin) |
| `FB_BOOST` | `Default` | 0.8 V Feedback Node | R_FB_H / R_FB_L | U2 FB (Feedback pin) |

---

## 4. Entity: PcbLayout

Represents the geometric implementation on the physical printed circuit board.

- **Board Boundary (`Edge.Cuts`)**:
  - Shape: Rectangle
  - Dimensions: $55.00\ \text{mm}\ (\text{Width}) \times 21.00\ \text{mm}\ (\text{Height})$
  - Corner radius: $1.0\ \text{mm}$ (chassis fit)
- **Top Layer Placement (`F.Cu`, `F.SilkS`)**:
  - Connectors J1 and J2 mounted at left ($X \approx 2\ \text{mm}$) and right ($X \approx 53\ \text{mm}$) edges facing outwards.
  - MCU1 placed centrally with USB-C connector extending towards board edge or top clear area.
  - Power switching loop (U2, L1, CIN, COUT) tightly grouped near J1 to minimize loop inductance.
  - MOSFETs Q1 and Q2 placed between boost/driver section and J2 motor connector.
- **Bottom Layer Flatness (`B.Cu`, `B.Mask`)**:
  - Zero through-hole component pads.
  - Zero through-hole component leads protruding.
  - All vias configured as tented with solder mask covering $100\%$ of via annular rings.

---

## 5. Entity: CustomFootprint

Defines custom footprints stored in `mini4wd-motor-driver.pretty/`:

1. **`Molex_MicroFit30_43650-0214_SMD_RA`**:
   - Pins: 2 electrical pins, pitch 3.0 mm, pad size $1.27\ \text{mm} \times 2.92\ \text{mm}$.
   - Mechanical: 2 solder retention nails/tabs, pad size $2.16\ \text{mm} \times 2.54\ \text{mm}$.
2. **`XIAO_MG24_Castellated_14P`**:
   - Pins: 14 castellated edge pads (2 rows of 7 pads).
   - Pitch: 2.54 mm (100 mil) along row; row-to-row spacing 17.78 mm (700 mil).
   - Pad Dimensions: $1.60\ \text{mm} \times 1.00\ \text{mm}$ rectangular SMD pad with semi-circle edge.
3. **`Coilcraft_XEL4030`**:
   - Pins: 2 pads.
   - Body: 4.0 mm × 4.0 mm.
   - Pad Dimensions: $1.37\ \text{mm}\ (\text{length}) \times 2.39\ \text{mm}\ (\text{width})$, gap between pads $1.88\ \text{mm}$.
