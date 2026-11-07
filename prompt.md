Create a custom Mini 4WD Motor Driver Expansion Board designed to be mounted directly above the battery. Follow all the system requirements, power architecture, safety guidelines, and PCB layout rules detailed below:

1. System Core & Components:
   - Main Controller: Seeed Studio XIAO MG24 Sense. Mount using Castellated Hole (Castellated Pad / SMD Direct Solder) footprint.
   - Motor Driver Circuit: Dual N-channel MOSFET or integrated H-bridge driver capable of handling continuous 5A drive current (with flyback diode protection for motor EMF).
   - Sensor Strategy: Primary sensing relies on the XIAO MG24 Sense's integrated 6-axis IMU (LSM6DS3TR-C) for slope (Pitch) and corner (Yaw) detection. Break out I2C pins (SDA, SCL) to SMD pads for optional future ToF sensors.

2. Connectors (100% SMD / SMT):
   - Power Input (B+ / B-): 1x Molex Micro-Fit 3.0 SMD Right-Angle 2-pin connector (handling 5A peak current).
   - Motor Output (M+ / M-): 1x Molex Micro-Fit 3.0 SMD Right-Angle 2-pin connector (handling 5A peak current).
   - Both connectors must be 100% Surface Mount (SMD) to avoid any through-hole leads protruding from the bottom.

3. Assembly & Manufacturing Requirements (PCBA):
   - ALL components (MCU, MOSFETs, Connectors, Diodes, Capacitors, Resistors) MUST be Surface Mount Devices (SMD/SMT).
   - Zero Through-Hole (THD) components allowed to ensure 100% automated SMT assembly (e.g., JLCPCB SMT Service) without manual hand-soldering fees.

4. PCB Layout & Physical Dimensions:
   - Board Outline: Standard Mini 4WD top-battery footprint (Approx. 55mm x 21mm, 2-layer PCB).
   - Board Thickness: 1.6mm nominal, selected to match the recommended PCB thickness of the Molex Micro-Fit 3.0 SMD right-angle header.
   - Bottom Layer Safety: Since the PCB rests on top of the batteries, the Bottom Layer must be 100% FLAT. No through-hole pins or exposed solder joints on the bottom side. Ensure Tenting Vias (solder mask covering all vias on the bottom).
   - Power Traces: Make B+/B- and M+/M- power traces sufficiently wide (min 1.5mm - 2.0mm width or copper pour) to safely carry up to 5A without excessive heating or voltage drop.
   - Connector Placement: Place the two Molex Micro-Fit 3.0 Right-Angle connectors at the front/rear edges facing outwards to minimize top-height interference with the Mini 4WD body.
