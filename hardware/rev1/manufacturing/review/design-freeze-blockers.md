# Rev1 Design Freeze Blockers

Review date: 2026-10-11  
Status: Circuit-definition decisions recorded; EasyEDA implementation and layout review remain unfinished.

The project copies the existing `mini4wd-motor-driver` board and applies only the improvements in `specs/001-smt-gerber-board/spec.md`. If a circuit feature or component cannot be confirmed from the available existing-board sources, treat it as unimplemented in the existing board and leave it unimplemented in rev1. Do not infer extra circuitry from generic reference designs. Resistor and capacitor positions/quantities must not increase.

## Active blockers

| ID | Blocker | Current evidence / gap | Evidence needed to close |
|---|---|---|---|
| — | No open circuit-definition blocker recorded. | `manufacturing/review/wiring-design.md` records the rev1 net decisions where SVG copper cannot establish net identity. Passive values are selected from documented functions and the cited manufacturer circuits. | Continue implementation checks: correct library part/value properties, place the XIAO, connectors, and two approved diode functions, verify footprints, route, and complete DRC/release review. |

## Removed from blocker status by user decision

| Former item | Disposition and retained rationale |
|---|---|
| Complete original schematic/netlist unavailable | **Not a blocker.** The full schematic/netlist cannot be obtained. Use confirmed README/hardware-spec/SVG/PNG evidence; features or connections not confirmed by those sources are treated as unimplemented in both the source-board model and rev1. |
| Generic motor-driver wording in `specs/001-smt-gerber-board/spec.md` conflicts with the documented source circuit | **Resolved by the source-evidence rule above.** Preserve the confirmed N-channel low-side drive and P-channel short-brake topology. Unconfirmed alternatives such as a dual-N implementation or H-bridge are treated as absent. Apply only prompt improvements that are explicit and compatible with the confirmed base circuit. |
| Independent 5 A overcurrent/thermal qualification | **Not required as a blocker.** This is a toy application, the user accepts following the existing board without qualification evidence, and the 5 A path is the specified rev1 difference. Retain the 5 A target from `specs/001-smt-gerber-board/spec.md`; do not claim that a separate thermal qualification has been performed. |
| Battery chemistry endpoint and low-voltage safety characterization | **Not required as a blocker.** User-selected alkaline/NiMH toy batteries may lose performance or stop as they discharge. Follow the existing design behavior without requiring a new endpoint qualification or added protection circuitry. |
| Footprint and assembled vehicle/battery mechanical-clearance review | **Not required as a blocker.** User explicitly accepts proceeding without this separate consideration. Retain the specified nominal 1.6 mm thickness, approximate 55 × 21 mm outline, and SMD connector requirements as design inputs; no vehicle-clearance evidence is required for design freeze. |

## Closed by completed review

| Former item | Closure evidence |
|---|---|
| XIAO MG24 Sense pad-number, signal, and orientation reconciliation | Closed in `manufacturing/review/xiao-interface-review.md`: all 14 castellated edge pads are mapped in the `pcb_front_3D.png` viewing orientation; the user's confirmed lower-left D0 position fixes the 180-degree footprint rotation; SDA/SCL use pads 10/9; unused edge pads and additional non-edge pads are left unconnected. |
| Unmapped source-board nets | Rev1 connectivity decisions are recorded per-net in `manufacturing/review/wiring-design.md`; SVG-traced connections and Codex-designed connections are explicitly distinguished there. |
| UCC27511 second bypass capacitor | Keep the existing 0.1 µF local bypass only. TI recommends a second few-µF capacitor in parallel, but user constraints prohibit adding capacitor positions and no existing second position is confirmed. Record this as a deliberate recommendation deviation, not as an added capacitor. |

## Confirmed scope and constraints

- Rev1 copies the existing board; only compatible, explicitly listed `specs/001-smt-gerber-board/spec.md` improvements may be applied.
- No resistor or capacitor positions/quantities may be added.
- Confirmed source architecture remains forward-only, N-channel low-side motor drive with P-channel short braking.
- Nominal 1.6 mm PCB, approximately 55 × 21 mm outline, two copper layers, SMT construction, direct XIAO MG24 Sense castellated mounting, and two outward-facing SMD Micro-Fit 3.0 connectors remain in scope.
- The target EasyEDA project remains an implementation task. The schematic now has BOM-selected component placements, while routing and the PCB remain unfinished. Use `manufacturing/review/svg-routing-source-review.md` for the currently extracted source-copper geometry; do not rely on trial routes that were removed.
- This document records design decisions and remaining definition blockers. Gerber export and file checks occur after the design itself is implemented.
