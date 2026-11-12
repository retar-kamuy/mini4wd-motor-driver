# Rev1 5 V power budget research

Date: 2026-10-04  
Status: Primary-source research completed; final load and low-voltage validation remain open. Per user clarification, reaching each cell chemistry's discharge endpoint is not a functional-performance requirement for this toy application.

## System interpretation

The available legacy SVG/PNG images provide named nets and visible placement/routing, but are not a complete schematic or authoritative netlist. The intended battery source is a pair of user-selected AA cells, not one fixed 2-cell NiMH model. Relevant examples include Tamiya Power Champ RX (alkaline) and Eneloop (NiMH); Tamiya explicitly identifies Power Champ RX as two AA alkaline cells. The values below therefore use the documented circuit blocks and manufacturer reference data. The assumed 5 V consumers are the XIAO MG24 Sense module and UCC27511; the motor's 5 A current is supplied from the battery/motor power path, not from the boost output.

## XIAO MG24 Sense current

Seeed's documentation identifies the XIAO 5V pin as an external power input and recommends a series diode between an external source and that pin. Seeed also links its official XIAO MG24 Sense schematic. The schematic shows the board's internal 3.3 V regulators and integrated peripherals; consequently, the SoC's 3.3 V current is not numerically identical to current drawn at the external 5 V pin.

Silicon Labs specifies the EFR32MG24 SoC at up to 156.8 mA for 19.5 dBm radio transmit, 19.1 mA at 10 dBm transmit, and 4.4 mA receive (1 Mbps GFSK). The 156.8 mA figure is a SoC rail condition and excludes XIAO board conversion loss/peripherals. As a power-equivalent estimate only, 3.3 V x 156.8 mA = 0.517 W; at 5 V and 85% conversion efficiency this is about 122 mA. Do not use this estimate as a module maximum: measure the XIAO's 5 V input current in its actual radio mode, with the IMU and firmware workload enabled.

Suggested characterization: measure average and peak current at the 5 V source using a current probe or a low-value Kelvin shunt plus oscilloscope; test idle, IMU sampling, continuous BLE advertising/connection, and maximum intended radio transmit power. Also measure the voltage directly at XIAO 5V after the proposed series diode.

## UCC27511 gate-driver current

TI specifies quiescent current below 1 mA. Its 4 A source / 8 A sink ratings describe short output pulses used to charge/discharge a MOSFET gate, not steady current drawn from the 5 V rail. Estimate the average gate-charge component as:

`I_gate(avg) ~= Qg x PWM_frequency`

For the specified Q1 gate charge of 21 nC, this is approximately 0.42 mA at 20 kHz or 2.1 mA at 100 kHz, before losses and the Q2 brake-gate switching contribution. These are illustrative estimates, not project switching-frequency requirements. Per the user's direction, do not hold design freeze for a PWM-frequency or gate-resistor optimization target that is absent from the source project. The supply still needs local bypassing because edge currents are pulsed.

## Battery minimum voltage

The battery envelope must cover both primary alkaline cells and rechargeable NiMH cells. Tamiya identifies Power Champ RX as an AA alkaline battery; Eneloop is AA NiMH. Panasonic's handbook gives a recommended 0.8 V/cell cutoff for alkaline and uses 1.0 V/cell as the NiMH discharge cutoff. These give chemistry-specific *capacity test/use endpoints* of 1.6 V per two-cell alkaline pack and 2.0 V per two-cell NiMH pack, not fixed instantaneous voltages under a motor pulse. Cell type, age, temperature, state of charge, contact resistance, and motor stall/acceleration current can cause additional loaded sag. Record the exact supported AA cells and measure pack voltage at the PCB connector during worst-case acceleration.

TPS61023 operates over 0.5-5.5 V input and has a minimum start-up input of 1.8 V. The alkaline pair's 1.6 V recommended cutoff endpoint is below the converter's specified startup minimum, so startup/restart at that endpoint is not guaranteed. Per user clarification, preserving motor performance at this endpoint is not required; reduced speed or shutdown as the cells discharge is acceptable. The electrical/thermal safety response to sag and brownout must still be checked: the converter must not cause repeated damaging transients, and the motor switching path must remain safe. The published 5 V / 1.5 A, 94% efficiency condition is at VIN=3.6 V, not at either chemistry's depleted endpoint. At 5 V / 200 mA out, a rough input estimate is `Pin/Vin = (5 V x 0.2 A)/(2.0 V x efficiency)`, or about 0.59 A at 85% efficiency; at 1.6 V it would be about 0.74 A. Validate the actual 5 V load and safe brownout response at representative loaded battery voltages; end-of-life motor performance is outside the required use case.

The legacy board labels 1S Li-ion as an allowed source. Per user decision, rev1 inherits the existing toy-board battery behavior without a new chemistry-endpoint qualification; the chemistry calculations above are background and not an additional performance requirement.

## Capacitor DC-bias characteristics

Murata identifies the proposed GRM188R61A106MAALD (10 uF, 10 V, X5R, 0603) and GRM188R61A226ME15D (22 uF, 10 V, X5R, 0603) part families and provides their DC-bias characteristic data through SimSurfing. Set the simulation to 5 V DC bias, expected operating temperature, and use the effective capacitance curve rather than the nominal label. Sum the two output capacitors' effective capacitances and compare with TI's TPS61023 minimum input/output capacitance requirements after tolerance, bias, temperature, and aging allowances.

The individual product pages' "Characteristic Data" area links to Murata SimSurfing. Exact part-number shortcuts:

- [10 uF GRM188R61A106MAALD DC-bias data](https://ds.murata.com/simsurfing/mlcc.html?oripartnumbers=%5B%22GRM188R61A106MAALD%22%5D&partnumbers=%5B%22GRM188R61A106MAAL%22%5D)
- [22 uF GRM188R61A226ME15D DC-bias data](https://ds.murata.com/simsurfing/mlcc.html?oripartnumbers=%5B%22GRM188R61A226ME15D%22%5D&partnumbers=%5B%22GRM188R61A226ME15%22%5D)

## D1 XIAO supply diode

Seeed recommends a series diode from external supply to XIAO 5V. Nexperia lists PMEG2010EA,115 as SOD323, 20 V, 1 A, with 0.48 V typical / 0.55 V maximum forward voltage at its listed test condition. Measure input current and check the XIAO pin voltage after the diode at peak current. If the resulting drop breaches the module's supply margin or current rating/thermal conditions, select a lower-drop or higher-current solution. This device is for XIAO supply isolation only, not motor flyback protection.

## Acceptance data to capture

Before design release, record (1) XIAO 5 V average and peak current for the firmware/radio test cases, (2) gate-driver 5 V supply waveform, (3) representative user battery types and loaded voltage range at the PCB, (4) Murata effective capacitance at 5 V and temperature limits, (5) 5 V rail startup/ripple/dropout and safe brownout behavior over the intended operating range, and (6) diode forward drop and temperature at measured peak load. Separately validate the battery-to-motor path, MOSFETs, and connectors at the defined 5 A duty and under foreseeable stall/blocked-rotor faults.

## Manufacturer sources

- [Seeed XIAO MG24 Sense getting-started page, 5V input guidance and official schematic links](https://wiki.seeedstudio.com/ja/xiao_mg24_getting_started/)
- [XIAO MG24 Sense official schematic PDF](https://files.seeedstudio.com/wiki/XIAO_MG24/Getting_Start/XIAO_MG24_v1_0_SCH_PDF.pdf)
- [Silicon Labs EFR32MG24 datasheet](https://www.silabs.com/documents/public/data-sheets/efr32mg24-datasheet.pdf)
- [TI UCC27511 datasheet](https://www.ti.com/lit/gpn/UCC27511)
- [TI TPS61023 datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf)
- [Panasonic Ni-MH handbook](https://eu.industrial.panasonic.com/sites/default/pidseu/files/downloads/files/id_ni-mh_1104_e.pdf)
- [Panasonic alkaline handbook (LR6/AA recommended cutoff 0.8 V/cell)](https://eu.industrial.panasonic.com/sites/default/pidseu/files/downloads/files/id_alkaline_1203_e.pdf)
- [Tamiya Power Champ RX specification (two AA alkaline cells)](https://www.tamiya.com/japan/products/55119/index.html)
- [Murata 10 uF capacitor product page](https://www.murata.com/ja-JP/products/productdetail?partno=GRM188R61A106MAAL%23)
- [Murata 22 uF capacitor product data sheet](https://www.murata.com/en-eu/api/pdfdownloadapi?cate=luCeramicCapacitorsSMD&partno=GRM188R61A226ME15D)
- [Nexperia PMEG2010EA product page](https://www.nexperia.com/products/diodes/schottky-diodes-and-rectifiers/schottky-diodes-and-rectifiers-if-1-a/PMEG2010EA.html)
