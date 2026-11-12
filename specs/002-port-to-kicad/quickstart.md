> **2026-11-10 現状注記**: 本文には旧作業コピーへのパスと当時の設計・検証状態が含まれる。現行の正規設計は `hardware/kicad/mini4wd-motor-driver/`、検証根拠と残作業は `specs/003-resolve-pcb-drc/` を参照する。旧手順や完成の記述を現行基板の検証結果として扱わない。

# Quickstart Validation Guide: Mini 4WD Motor Driver KiCad Port

**Branch**: `002-port-to-kicad` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

This guide provides end-to-end runnable scenarios to validate the native KiCad 10 project, schematic connectivity, PCB layout design rules, and manufacturing deliverables.

---

## Prerequisites

1. **KiCad 10.0** installed on Windows (`C:\Program Files\KiCad\10.0\bin`).
2. **KiCad MCP Server** configured and running or accessible via Node.js (`C:\Users\hoshi\Repositories\KiCAD-MCP-Server\dist\index.js`).
3. Python environment configured with `kicad-cli` or `pcbnew` Python module.

---

## Validation Scenario 1: Schematic Electrical Rules Check (ERC)

Validate that the ported schematic contains all 24 components, correct net labels, and zero electrical conflicts.

### Test Action via KiCad MCP Server
Invoke the `run_erc` tool on the active project:
```json
{
  "project_path": "c:/Users/hoshi/Repositories/mini4wd-motor-driver/hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro"
}
```

### Alternative CLI Validation
Execute `kicad-cli` from PowerShell:
```powershell
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" sch erc `
  --severity-all `
  --exit-code-violations `
  "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch"
```

### Expected Outcome
- ERC Exit Code: `0`
- Unconnected pins: `0`
- Floating labels: `0`
- Net conflicts: `0`
- Inductor L1 mapped to `Coilcraft_XEL4030` footprint.

---

## Validation Scenario 2: PCB Layout Design Rules Check (DRC) & 5A Routing

Validate that the physical board conforms to the 55.0 mm × 21.0 mm outline, adheres to the 1.6 mm stackup, passes clearance rules, and meets high-current trace width minimums.

### Test Action via KiCad MCP Server
Invoke the `run_drc` tool:
```json
{
  "project_path": "c:/Users/hoshi/Repositories/mini4wd-motor-driver/hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro"
}
```

### Alternative CLI Validation
```powershell
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb drc `
  --severity-all `
  --exit-code-violations `
  --output "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/manufacturing/drc-report.txt" `
  "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb"
```

### Expected Outcome
- DRC Violations: `0 errors`, `0 warnings`.
- Unconnected Nets: `0`.
- Clearance violations: `0` (min track/space $\ge 0.127\ \text{mm}$).
- High-current net widths (`VBAT`, `GND`, `MOTOR_PLUS`, `MOTOR_MINUS`): all $\ge 1.5\ \text{mm}$ or wide copper polygon zones.

---

## Validation Scenario 3: Battery Underside Flatness and Via Tenting Check

Verify that the battery-facing underside has zero through-hole pads and 100% tented vias.

### Test Action
1. Inspect the bottom copper layer (`B.Cu`):
   - Confirm all 24 components are placed on `F.Cu` (Top layer).
   - Confirm no through-hole component pins penetrate to the bottom side.
2. Inspect the bottom solder mask layer (`B.Mask`):
   - Confirm `B.Mask` contains zero openings for via holes (all vias are fully covered/tented by solder mask).

### Expected Outcome
- Through-hole pads: `0`.
- Exposed via copper on bottom: `0`.

---

## Validation Scenario 4: Manufacturing Output Package & PCBA Centroid Check

Verify that production-ready Gerber archives, Excellon drill files, and JLCPCB SMT files are cleanly generated.

### Test Action via KiCad MCP Server
Invoke:
1. `export_gerbers` -> outputs to `manufacturing/gerber/`
2. `export_drill` -> outputs to `manufacturing/gerber/`
3. `export_pos` -> outputs `cpl.csv`
4. `export_bom` -> outputs `bom.csv`

### Alternative CLI Validation
```powershell
$outDir = "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/manufacturing/gerber"
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export gerbers `
  --output $outDir `
  "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb"

& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export drill `
  --output $outDir `
  "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb"

& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export pos `
  --output "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/manufacturing/cpl.csv" `
  --format csv --units mm --side top `
  "hardware/archive/kicad-before-consolidation/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb"
```

### Expected Outcome
- Gerber layer files present: `F.Cu`, `B.Cu`, `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS`, `F.Paste`, `Edge.Cuts`.
- Drill file present: `.drl` (PTH vias only, 0 component holes).
- Centroid file `cpl.csv`: exactly 24 entries, all with `Layer = Top`.
- BOM file `bom.csv`: includes L1 as `Coilcraft XEL4030-102ME`, U1 as `UCC27511DBVR`, Q1 as `SiSS64DN-T1-GE3`, Q2 as `SI7137DP-T1-GE3`, U2 as `TPS61023DRLR`, and Molex `43650-0214`.
