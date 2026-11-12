> **2026-11-10 現状注記**: 本文には旧作業コピーへのパスと当時の設計・検証状態が含まれる。現行の正規設計は `hardware/kicad/mini4wd-motor-driver/`、検証根拠と残作業は `specs/003-resolve-pcb-drc/` を参照する。旧手順や完成の記述を現行基板の検証結果として扱わない。

# Board Interface and Fabrication Contract: KiCad Hardware Release

**Branch**: `002-port-to-kicad` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

This contract defines the physical, electrical, and manufacturing interfaces governing the native KiCad implementation of the Mini 4WD Motor Driver Expansion Board.

---

## 1. Mechanical Envelope & Stackup Contract

- **Outline Dimensions**: $55.00\ \text{mm} \times 21.00\ \text{mm}$ rectangular contour defined on KiCad's `Edge.Cuts` layer. Corner radius: $1.0\ \text{mm}$.
- **Board Thickness**: Nominal $1.60\ \text{mm} \pm 10\%$. This thickness matches the retention tab specifications of the Molex Micro-Fit 3.0 right-angle SMT headers (`43650-0214`).
- **Layer Count**: 2 copper layers (`F.Cu`, `B.Cu`), 1 oz ($35\ \mu\text{m}$) base copper weight.
- **Battery-Facing Bottom Surface**:
  - $100\%$ flat surface.
  - Zero through-hole component leads or pins.
  - Zero exposed via copper; all bottom vias MUST be tented by solder mask (`B.Mask`).

---

## 2. External Connector Interface (Molex Micro-Fit 3.0)

Two 2-position Molex Micro-Fit 3.0 right-angle SMT headers (`43650-0214`) positioned at opposite board edges, facing outward to prevent interference with battery and body clips.

### J1: Battery Power Input Connector
- **Location**: Left edge ($X \approx 2.0\ \text{mm}$), mating direction pointing left (-X).
- **Pin 1**: `VBAT` (Battery Positive, B+), rated 5A peak / continuous.
- **Pin 2**: `GND` (Battery Negative / Power Ground, B-), rated 5A peak / continuous.
- **Silkscreen Marking**: Explicit `B+` and `B-` polarity indicators on `F.SilkS`.

### J2: Motor Drive Output Connector
- **Location**: Right edge ($X \approx 53.0\ \text{mm}$), mating direction pointing right (+X).
- **Pin 1**: `MOTOR_PLUS` (Motor Positive, M+, connected to `VBAT`), rated 5A peak / continuous.
- **Pin 2**: `MOTOR_MINUS` (Motor Negative, M-, switched low-side node), rated 5A peak / continuous.
- **Silkscreen Marking**: Explicit `M+` and `M-` markings on `F.SilkS`.

---

## 3. Main Controller Interface (Seeed Studio XIAO MG24 Sense)

Mounted directly via 14 castellated edge pads. No pin headers or sockets are permitted.

| Pad | Pin Name | Net Name | Electrical Role | Connected Components |
|---|---|---|---|---|
| **1** | `5V` | `XIAO_5V` | 5.0 V Isolated Power Input | D_XIAO (SS14-E3) Cathode |
| **2** | `GND` | `GND` | Ground Reference | Common ground plane |
| **3** | `3V3` | `MCU_3V3` | 3.3 V Logic Reference Output | R_NTC (10 kΩ pull-up) |
| **4** | `D1 / A1` | `TEMP_SENSE` | Analog Input (Temperature) | R_NTC & TH1 (NTCG104BH103JT1) divider |
| **5** | `D2 / PWM` | `PWM_DRIVE` | Digital Output (Motor Drive) | U1 (UCC27511) IN+ pin |
| **6** | `D3 / A3` | `MID_SENSE` | Analog Input (Motor M- voltage) | R_MID_H (22 kΩ) & R_MID_L (10 kΩ) divider |
| **7** | `D4` | `NC` | Not Connected | Unused edge pad |
| **8** | `D5` | `NC` | Not Connected | Unused edge pad |
| **9** | `D6 / SCL` | `I2C_SCL` | I2C Clock Bus | SMD breakout pad (test point) |
| **10**| `D7 / SDA` | `I2C_SDA` | I2C Data Bus | SMD breakout pad (test point) |
| **11**| `D8` | `NC` | Not Connected | Unused edge pad |
| **12**| `D9` | `NC` | Not Connected | Unused edge pad |
| **13**| `D10` | `NC` | Not Connected | Unused edge pad |
| **14**| `D0 / A0` | `VBAT_SENSE` | Analog Input (Battery voltage) | R_VBAT_H (22 kΩ) & R_VBAT_L (10 kΩ) divider |

*Note on Rotation*: The module is rotated 180° so that Pad 14 (`D0 / VBAT_SENSE`) faces the bottom edge where the voltage divider resistors reside.

---

## 4. Drive & Protection Topology Contract

1. **Drive Mode**: Forward-only low-side switching via Vishay SiSS64DN-T1-GE3 (N-channel MOSFET, $R_{DS(on)} \le 2.86\ \text{m}\Omega$ @ 4.5V).
2. **Short Braking**: Passive/active short-circuit braking via Vishay SI7137DP-T1-GE3 (P-channel MOSFET) pulling M- to M+ (VBAT) when PWM drive is inactive.
3. **Gate Drive**: TI UCC27511DBVR operating at 5.0 V boosted supply from TPS61023DRLR, delivering up to 4A source / 8A sink for rapid gate transitions.
4. **Boost Stage (Restored)**: TPS61023 with **Coilcraft XEL4030-102ME** (1.0 µH) inductor, stepping up 1.8 V – 3.2 V battery voltage to stable 5.0 V for gate driver and MCU.
5. **Flyback Protection**: Comchip SS54-HF (5A 40V Schottky) connected directly across M- (Anode) and M+ (Cathode).
6. **Reverse USB Isolation**: Vishay SS14-E3/61T Schottky diode isolating the 5V boost converter output from external USB-C power connected to the XIAO MG24 Sense.

---

## 5. Manufacturing Package Contract (KiCad 10 / JLCPCB SMT)

All manufacturing files must be generated from native KiCad 10 project files (`.kicad_pro`, `.kicad_pcb`, `.kicad_sch`):

### 5.1 Gerber & Drill Output (`manufacturing/gerber/`)
- `*.gtl` (`F.Cu`): Component side copper.
- `*.gbl` (`B.Cu`): Battery side copper (wide pours, tented vias).
- `*.gts` (`F.Mask`): Top solder mask.
- `*.gbs` (`B.Mask`): Bottom solder mask (100% tenting over all vias).
- `*.gto` (`F.SilkS`): Top silkscreen with connector polarity and component legends.
- `*.gbo` (`B.SilkS`): Bottom silkscreen with conversion formulas.
- `*.gtp` (`F.Paste`): Top SMT solder paste stencil layer.
- `*.gm1` or `*.gko` (`Edge.Cuts`): 55.0 mm × 21.0 mm board profile.
- `*.drl`: Excellon NC drill file (PTH vias only; 0 component holes).

### 5.2 SMT Assembly Output (`manufacturing/`)
- `bom.csv`: Bill of materials structured for JLCPCB SMT format:
  `Comment, Designator, Footprint, LCSC Part Number / Manufacturer Part Number`
- `cpl.csv` (or `positions.csv`): Component placement centroid file:
  `Designator, Val, Package, Mid X, Mid Y, Rotation, Layer` (Layer: `Top` for all 24 components).
- `mini4wd-motor-driver.ipc`: IPC-D-356 electrical test netlist for bare-board verification.
