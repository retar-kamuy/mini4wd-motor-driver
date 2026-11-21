# Mini 4WD Brushless Motor Controller — Hardware Project

This directory is reserved for the separate Spec 005 BLDC hardware design. It is intentionally separate from `hardware/kicad/mini4wd-motor-driver/`, which is the existing brushed-motor board.

## Naming and revision convention

- KiCad project base name: `mini4wd-brushless-motor`
- Project files use the same base name (`.kicad_pro`, `.kicad_sch`, `.kicad_pcb`).
- Use KiCad-managed project revision and a matching release identifier for manufacturing outputs.
- Store design reviews and validation under `validation/`; store each immutable manufacturing export under `manufacturing/rev-<revision>/`.
- Do not create/freeze schematic or PCB content until motor/chassis fit, battery envelope, commutation architecture, and safety gates are supported by evidence.

## Current status

No BLDC schematic, PCB, BOM, or manufacturing output has been created. Candidate motor, chassis, battery, and controller remain unselected. This directory contains project guidance only.
