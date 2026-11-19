# XIAO-to-BLDC Controller Interface Contract

**Status**: Planning contract; electrical values and protocol are intentionally unselected until a motor/controller is qualified.

## Purpose

Retain the XIAO MG24 Sense with the current BLE/WebApp as the preferred high-level control path. The XIAO supplies run/speed/stop intent. A dedicated commutation function generates three-phase motor drive. Existing brushed-motor PWM semantics must not be wired directly to phase gates.

## Signals and behavior to define during G3

| Signal/function | Required contract |
|---|---|
| Speed command | Select PWM, analog, serial/I²C, or ESC protocol from the chosen controller datasheet. Record voltage levels, frequency/baud, valid range, scaling, and invalid values. |
| Enable/drive inhibit | Define active polarity, pull state, reset/boot default, and hardware path to force outputs off. Reset or disconnected XIAO must not enable torque. |
| Stop mode | Define separate meanings for coast, controlled deceleration, and electrical brake where supported. Never infer that zero speed command means a safe brake. |
| Fault input | Controller fault must be visible to XIAO if supported, with asserted polarity, filtering, latch/clear behavior, and user-visible status. Fault shutdown must not depend only on a software polling loop. |
| Telemetry (optional) | Define available speed/current/voltage/temperature data, freshness, scaling, and failure behavior. |
| Power and ground | Define logic supply source, voltage range, sequencing, common reference, isolation (if any), USB/battery backfeed prevention, and motor-noise return path. |

## Safety semantics

- On boot, reset, brownout, invalid command, or command timeout, drive remains disabled or enters an explicitly validated safe stop state.
- Communication recovery does not restart the motor automatically; a fresh arm/run command is required.
- Current/voltage/thermal controller faults disable drive according to the selected device’s hardware behavior and are reported to the XIAO when possible.
- Brake energy and DC-bus voltage must remain within component and battery limits, including a full or disconnected battery case.
- Command timeout, timeout action, and restart policy are selected from measured vehicle stopping behavior and documented before implementation.

## Values pending selection

Controller MPN; command protocol; logic level; PWM/serial timing; speed mapping; timeout; enable/fault polarity; stop/coast/brake definitions; telemetry; and any isolation or level-shifting. Populate the contract from the selected controller datasheet and verify on the bench before schematic freeze.
