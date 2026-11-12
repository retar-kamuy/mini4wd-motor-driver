> **2026-11-10 現状注記**: 本文には旧作業コピーへのパスと当時の設計・検証状態が含まれる。現行の正規設計は `hardware/kicad/mini4wd-motor-driver/`、検証根拠と残作業は `specs/003-resolve-pcb-drc/` を参照する。旧手順や完成の記述を現行基板の検証結果として扱わない。

# Phase 0 Research: Porting Mini 4WD Motor Driver to KiCad

**Branch**: `002-port-to-kicad` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

This document consolidates technical investigations and architectural decisions for migrating the Mini 4WD Motor Driver Expansion Board from EasyEDA to KiCad 10 using the KiCad MCP server.

---

## 1. CAD Tool Migration Strategy: Native KiCad Construction vs. Translation

### Investigation
EasyEDA Pro projects are stored in `.eprj2` files, which are SQLite/JSON hybrid database containers specific to the EasyEDA engine. There is no official or lossless converter from EasyEDA Pro `.eprj2` to KiCad schematic (`.kicad_sch`) or PCB (`.kicad_pcb`). Third-party converters frequently corrupt net labels, pad assignments, and polygon fills. Conversely, the repository already contains complete, verified hardware specifications, electrical net mappings (`manufacturing/review/wiring-design.md`), a finalized BOM (`manufacturing/review/bom.csv`), and reference layout drawings (`docs/pcb_front.svg` and `pcb_back.svg`). Furthermore, the KiCad MCP server provides programmatic APIs to create projects, construct schematics, place components, route tracks, and run DRC.

### Decision
Reconstruct the hardware natively in KiCad 10 using the KiCad MCP server and verified source requirements, rather than attempting automated file translation from `.eprj2`.

### Rationale
- Guarantees 100% clean, native KiCad 10 syntax (`kicad_sch` v2024+, `kicad_pcb` v2024+).
- Ensures correct symbol pin electrical types, enabling reliable Electrical Rules Check (ERC).
- Eliminates legacy EasyEDA vendor locks, allowing standalone Git version control and native KiCad editing.

### Alternatives Considered
- *Third-party file converters (e.g. easyeda2kicad / gerber import)*: Rejected because they do not reliably import EasyEDA Pro schematic connectivity or produce editable native netlists.
- *Gerber-only import into KiCad PCB*: Rejected because imported Gerbers consist of raw copper tracks and lack schematic net associations, making ERC and design updates impossible.

---

## 2. Restoring the Original Coilcraft Boost Inductor (L1)

### Investigation
During the earlier EasyEDA phase, Coilcraft XEL4030-102ME was the intended inductor for the TI TPS61023 boost converter (as recommended in the TI TPS61023 datasheet and EVM-052 evaluation module). However, because EasyEDA Pro's component library lacked the Coilcraft part, the design temporarily substituted Würth Elektronik WE-MAPI 74438357010 (`IND-SMD_L4.1-W4.1_SPM40XX`). The user explicitly requested identifying this substitution and reverting to the original part in KiCad.

KiCad supports custom footprint creation and standard SMD inductor libraries:
- Coilcraft XEL4030-102ME footprint dimensions: Body 4.0 mm × 4.0 mm × 3.1 mm height.
- Manufacturer recommended land pattern: Pad width 2.39 mm, pad length 1.37 mm, inner pad separation 1.88 mm (overall footprint span 4.62 mm × 2.39 mm).
- Electrical ratings: $L = 1.0\ \mu\text{H}$, $DCR = 8.9\ \text{m}\Omega\ \text{typ}\ (9.79\ \text{m}\Omega\ \text{max})$, $I_{sat} = 9.0\ \text{A}$ (30% drop), $I_{rms} = 6.9\ \text{A}$ (40°C rise).

### Decision
Revert L1 to **Coilcraft XEL4030-102ME** (1.0 µH) and register its land pattern in the project-local footprint library (`mini4wd-motor-driver.pretty`).

### Rationale
- Restores the primary reference design component for the TI TPS61023 boost converter.
- Coilcraft XEL4030 offers superior DCR (8.9 mΩ typ vs. Würth's 13.5 mΩ max), reducing conduction losses and improving boost efficiency when stepping up from low battery voltages (1.8 V – 3.0 V).
- Eliminates the workaround necessitated by EasyEDA's library limitations.

### Alternatives Considered
- *Retaining Würth Elektronik 74438357010*: Rejected per user request.

---

## 3. Component Footprint Strategy in KiCad

### Investigation
The Mini 4WD Motor Driver requires 24 surface-mount components, some of which require specialized footprints:
1. **Molex Micro-Fit 3.0 SMD Right-Angle 2-Pin (43650-0214)**:
   - SMT header with solderable retention tabs / nails.
   - Recommended PCB thickness: 1.6 mm.
   - Pin pitch: 3.0 mm.
2. **Seeed Studio XIAO MG24 Sense**:
   - 14 castellated edge pads at 2.54 mm pitch (two rows of 7 pads, spaced 17.78 mm / 700 mil apart).
   - Module rotation: 180° so that pad 14 (`D0` / `VBAT_SENSE`) is positioned at the lower edge adjacent to the voltage divider.
3. **Power MOSFETs**:
   - SiSS64DN: PowerPAK 1212-8S (single N-ch, low RDS(on) 2.86 mΩ).
   - SI7137DP: PowerPAK SO-8 (single P-ch short brake).
4. **Boost Converter IC (TPS61023DRLR)**:
   - SOT-5X3 (DRL-6, 1.6 mm × 1.6 mm body, 0.5 mm pitch).
5. **Gate Driver IC (UCC27511DBVR)**:
   - SOT-23-6 (DBV-6).
6. **Passives & Diodes**:
   - Resistors: 0603 (1608 metric).
   - Capacitors: 0402 (1005 metric) for bypass, 0603 (1608 metric) for boost in/out.
   - Diodes: DO-214AC (SMA) for SS54-HF and SS14-E3.

### Decision
Create and register a project-specific footprint library:
`hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.pretty/`
containing:
- `Molex_Micro-Fit_3.0_43650-0214_SMD_RA.kicad_mod`
- `XIAO_MG24_Castellated_14P.kicad_mod`
- `Coilcraft_XEL4030.kicad_mod`
Standard package footprints (SOT-23-6, SOT-5X3, PowerPAK SO-8, 0603, 0402, SMA) will map to standard KiCad library footprints (`Package_TO_SOT_SMD`, `Package_SO`, `Resistor_SMD`, `Capacitor_SMD`, `Diode_SMD`).

---

## 4. 5A High-Current Trace Design and PCB Stackup

### Investigation
The board must safely conduct 5A continuous motor current across two battery-to-driver and driver-to-motor circuits.
According to IPC-2152 for 1oz copper (35 µm thickness) with an allowable temperature rise $\Delta T \le 15^\circ\text{C}$:
- Minimum external trace width for 5A continuous is approximately 1.5 mm – 1.8 mm.
- For high-current nodes (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`), using polygon copper pours (fills) or wide traces (2.0 mm) on both top (`F.Cu`) and bottom (`B.Cu`) layers connected by multiple stitching vias minimizes voltage drop and thermal impedance.

### Decision
- Stackup: 2-layer FR-4, 1.6 mm nominal thickness, 1 oz copper (35 µm).
- Power nets: Defined under a dedicated KiCad Netclass `Power_5A` with:
  - Minimum track width: 1.5 mm
  - Nominal track width: 2.0 mm
  - Dedicated polygonal copper pours on high-current loops.
- Signal nets: Netclass `Default` with 0.25 mm track width and 0.2 mm clearance.

---

## 5. Battery Underside Flatness and Via Tenting

### Investigation
Because the PCB is mounted directly above the Mini 4WD battery compartment, exposed component pins or vias can contact the steel battery casing, causing short circuits or puncture damage.

### Decision
- 100% surface-mount components; zero through-hole pins.
- Configure KiCad board design rules and Gerber plot settings to enforce **100% solder mask tenting** on all bottom-layer (`B.Mask`) vias (`solder_mask_min_width` and zero via expansion over solder mask).
- DRC rule check verifying zero exposed copper annular rings on the bottom side.

---

## 6. Manufacturing Package and PCBA Compatibility (JLCPCB)

### Investigation
The project targets automated SMT assembly (e.g. JLCPCB SMT Service).
Requirements:
1. Standard RS-274X or Gerber X2 layer files:
   - `F.Cu`, `B.Cu` (Copper)
   - `F.Mask`, `B.Mask` (Solder Mask)
   - `F.SilkS`, `B.SilkS` (Silkscreen)
   - `F.Paste` (Solder Paste for SMT stencil)
   - `Edge.Cuts` (Board Outline)
2. Excellon drill file (`.drl`) with unified drill origin matching Gerber auxiliary origin.
3. BOM (Bill of Materials) CSV containing:
   - `Comment/Value`, `Designator`, `Footprint`, `LCSC Part Number / MPN`
4. CPL (Component Placement List / Centroid) CSV containing:
   - `Designator`, `Mid X`, `Mid Y`, `Layer`, `Rotation`

### Decision
Export all fabrication artifacts directly from KiCad using the KiCad MCP server export tools (`export_gerbers`, `export_drill`, `export_pos`, `export_bom`) into:
`hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/manufacturing/`
with JLCPCB-compatible file naming and coordinate standards.
