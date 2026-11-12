# Board Interface and Fabrication Contract

This contract records externally visible board connections and manufacturing package expectations. It is derived from `mini4wd-motor-driver/README.md`, `docs/hardware_spec.md`, and `specs/001-smt-gerber-board/spec.md`.

## Board Stackup and Mechanical Envelope

- Two copper layers, nominal board thickness 1.6 mm, and approximately 55 ﾃ・21 mm physical outline.
- The 1.6 mm thickness is the approved requirement for this new design and supersedes the 1.2 mm thickness recorded for the legacy hardware revision in `docs/hardware_spec.md`.
- Confirm the assembled board, mated Micro-Fit connectors, battery spacing, and chassis clearance against the vehicle before fabrication release.

## Power and Motor Connectors

Two two-position Molex Micro-Fit 3.0 SMD right-angle headers face outward from opposite board ends.

| Connector | Pin | Net | Meaning |
|---|---:|---|---|
| Battery input | 1 | B+ / M+ | Battery positive and motor positive common node |
| Battery input | 2 | B- | Battery negative |
| Motor output | 1 | B+ / M+ | Motor positive, common with battery positive |
| Motor output | 2 | M- | Motor negative, switched low-side node |

The final pin-1 marking and keying orientation must be visible on silkscreen and agree with the selected mating cable assembly. The board-side header is SMT; mating wire housing and terminals are identified in the assembly BOM.

## XIAO MG24 Sense Interface

| Module pad | Board signal | Direction/role |
|---|---|---|
| 5V | 5V_OUT | Board supplies 5 V to module |
| GND | GND | Common return |
| PC0 / D0 | VBAT_SENSE | Scaled battery-positive measurement |
| PC1 / D1 | NTC_TEMP | Board-temperature divider signal |
| PC2 / D2 | MOTOR_PWM | PWM motor-control input |
| PC3 / D3 | MID_SENSE | Scaled motor-negative measurement |
| PC4 / D4 / SDA | I2C_SDA | Optional future sensor breakout pad |
| PC5 / D5 / SCL | I2C_SCL | Optional future sensor breakout pad |

Use castellated-pad direct soldering. Do not add a pin header or socket. Verify pad order, numbering, and module orientation with Seeed's official XIAO MG24 Sense design materials before routing.

## Electrical Behavior

- Forward-only motor drive; no reverse drive or H-bridge behavior.
- N-channel MOSFET switches the M竏・low side.
- P-channel MOSFET provides short braking.
- One PWM control input.
- Intended supply: Ni-MH two-cell or Li-ion one-cell. Li-ion two-cell and 8.4 V systems are out of scope.
- Design target: 5 A continuous motor current; connector target: 5 A peak per specified interface.
- The contract describes target requirements, not a claim that the as-yet-unbuilt board has passed thermal qualification.

## Fabrication Package

The package is generated from the user-designated active EasyEDA project and includes, as applicable to the selected fabricator:

- Two copper layers: top and bottom.
- Top and bottom solder mask, with underside vias tented.
- Top and bottom silkscreen as used by the design.
- A board-outline layer for the approximately 55 ﾃ・21 mm physical contour.
- Drill outputs only for actual holes/vias; no component through holes are permitted.
- BOM and pick-and-place files for SMT assembly.
- Layer map and review images identifying the exact project revision.

The Gerber archive must be previewed as a complete layer set, with drill registration and board dimensions checked, then accepted by the chosen fabricator's file validation before release.
