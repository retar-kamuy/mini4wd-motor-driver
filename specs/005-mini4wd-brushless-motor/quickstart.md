# Prototype Validation Quickstart

This is a future validation procedure for the selected prototype. No board, firmware, test fixture, or motor candidate is qualified yet. Fill all bracketed limits from approved motor, battery, and controller documents before powering hardware.

## Prerequisites

- Frozen revision ID for schematic, PCB, firmware, BOM, and this test record.
- Approved motor drawing/datasheet and one identified stock chassis/gear set.
- Approved battery pack data, protection behavior, current limit, and charging method.
- Completed [XIAO-to-BLDC interface contract](contracts/xiao-to-bldc-controller.md).
- Current-limited bench supply, fuse, emergency disconnect, oscilloscope/logic analyzer, current measurement, and temperature probes.
- Mechanical assembly inspected for motor pinion mesh, shaft retention, wire strain relief, road clearance, and battery restraint.

## Validation sequence

1. **Revision and visual checks**: Verify board marking/revision against the package. Inspect polarity, solder bridges, connector orientation, motor phase wiring, and mounting clearances. Confirm motor turns freely through the gear train with power disconnected.
2. **Unpowered electrical checks**: Check battery polarity, rail-to-ground resistance, phase-to-phase shorts, connector pinout, and XIAO/controller continuity against the schematic. Record results.
3. **Logic-only startup**: Power the logic rail from a current-limited source with motor power absent. Verify XIAO boot, BLE/WebApp connection, controller reset/configuration, and that all gate/drive outputs remain disabled before a valid run command.
4. **Power-stage no-load check**: Use a current-limited supply at the lowest approved motor voltage, wheels raised and guarded. Begin at minimum command. Confirm phase sequence/rotation, fault reporting, supply current, and safe stop. Stop immediately on unexpected current, reverse start, fault, or heating.
5. **Startup and command check**: Run at low command then step through the agreed command points. Repeat from stopped and restart after coast/brake. Log startup successes, time to response, speed, voltage/current, and any synchronization loss. Confirm command timeout and recovery require the documented re-arm action.
6. **Load and chassis check**: Install the drive in the selected stock chassis. Begin with wheels raised, then short controlled runs on a safe surface. Check pinion/gear mesh, chassis interference, stopping distance, current, battery sag, and motor/board/component temperatures.
7. **Operating corners and faults**: At approved low/nominal/high battery states, test startup, acceleration, stop, and controlled load. Test only faults that can be injected safely (command loss, undervoltage, motor lock/overcurrent as allowed by device documentation). Verify hardware shutdown, no unintended restart, and recovery procedure.
8. **Evidence and disposition**: Save scope traces, serial logs, temperature/current tables, fit photos, test conditions, failures, and corrective actions under the revision record. Mark each requirement pass/fail/not tested. Re-run impacted checks after any change.

## Required stop conditions

Immediately remove drive power for current above the approved limit, uncontrolled/reverse motion, controller fault without shutdown, battery protection trip, rail overvoltage, smoke/odor, loose wiring, gear binding, or temperature above any component/motor/battery limit. Do not bypass protection to complete a run.

## Expected outcome

The test record either demonstrates the specified startup/command/stop/fault behavior inside the approved envelope or identifies a reproducible failure with conditions and evidence. A successful bench run alone does not establish manufacturing readiness; ERC/DRC, design review, and manufacturer DFM/quote remain separate gates.
