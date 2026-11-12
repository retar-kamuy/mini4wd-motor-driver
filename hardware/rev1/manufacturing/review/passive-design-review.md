# Datasheet-Based Passive Design Review

Review date: 2026-10-11  
Status: circuit values selected where requirements and manufacturer examples determine them; no resistor or capacitor positions are added.

## Design basis

This review selects passive values from the documented circuit functions and manufacturer design guidance. It does not claim that the selected values are verified as the values on the original board. Maintain the project rule: do not add resistor or capacitor placements beyond the source board; unconfirmed circuitry remains unimplemented. If a manufacturer-recommended circuit needs more passive positions than this rule permits, hold that circuit for resolution instead of silently adding parts.

## Values selected from documented functions and TI's TPS61023 5 V example

| Function | Value / candidate implementation | Evidence and limits |
|---|---|---|
| VBAT_SENSE divider | Rupper 22 kΩ, Rlower 10 kΩ | Explicitly documented in `docs/hardware_spec.md`; yields the stated 3.2 scaling. Candidate BOM MPNs use Vishay CRCW0603, 1%, pending footprint and exact design mapping. |
| MID_SENSE divider | Rupper 22 kΩ, Rlower 10 kΩ | Explicitly documented in `docs/hardware_spec.md`; yields the stated 3.2 scaling. Candidate BOM MPNs use Vishay CRCW0603, 1%, pending footprint and exact design mapping. |
| NTC divider | Fixed resistor 10 kΩ with TDK NTCG104BH103JT1 (10 kΩ at 25°C, B25/85 4100 K) | Resistor value and function are documented. The resistor MPN/package remain a candidate; TH1 is the documented 0402 part. |
| TPS61023 output feedback | R1 732 kΩ from VOUT to FB; R2 100 kΩ from FB to GND | TI's typical 5 V application explicitly uses these values. The existing candidate Vishay CRCW0603 MPNs match those nominal values. |
| TPS61023 inductor | Würth Elektronik 74438357010, 1 µH | TI lists this as a recommended part and the exact device/footprint is available in EasyEDA. Its TI-listed maximum DCR is 13.5 mΩ and saturation current is 9.6 A; verify peak current at the final input/load conditions. |
| TPS61023 input capacitor | 10 µF nominal, ceramic | TI's typical 5 V application uses 10 µF. Existing Murata GRM188R61A106MAALD is a candidate; confirm effective capacitance under DC bias and temperature. |
| TPS61023 output capacitance | 2 × 22 µF nominal, ceramic | TI's typical 5 V application uses two 22 µF capacitors. Existing Murata GRM188R61A226ME15D is a candidate; verify effective capacitance at 5 V, tolerance, and temperature before freezing the MPN. |

The TI example's stated operating point is 2.7–4.35 V input, 5 V output, 1.5 A output, and ±50 mV ripple. The TPS61023 can start above its 1.8 V UVLO threshold and then operate down to 0.5 V, but that alone does not prove the example's 1.5 A output capability at the project's full AA-cell range. Final power-stage approval needs the already documented 5 V load and battery operating range to be checked against the datasheet's inductor-current equations and curves.

## UCC27511 and MOSFET support components

- **VDD bypass:** TI recommends a 0.1 µF ceramic capacitor close to VDD/GND plus a larger parallel capacitor, approximately 1 µF or a few µF. The current BOM's 0.1 µF candidate is assigned to UCC27511 VDD bypass; it is not a TPS61023 requirement in TI's typical circuit. The user prohibits additional capacitor positions and no existing second position is confirmed, so rev1 intentionally uses only the existing 0.1 µF position. Record the omitted larger capacitor as a deviation from TI's recommendation; do not add a capacitor footprint.
- **N-channel gate resistance:** `mini4wd-motor-driver` documents that UCC27511 supports separate turn-on/turn-off gate resistance but specifies neither values nor switching targets. Per the user's direction, do not treat gate-resistor optimization as a design blocker or request additional switching conditions. Do not add resistor positions; any undocumented source-board gate-resistor network remains unimplemented under the project source-evidence rule.
- **P-channel brake gate network:** The hardware documents the P-channel short-brake function but does not provide a full gate-control circuit. Do not invent a pull-up/pull-down or series resistor network without confirming the topology and available passive positions.
- **Feed-forward capacitor:** Not part of TI's basic TPS61023 5 V application. TI describes it conditionally for output capacitance above 40 µF or input below 1 V. Do not add it to this design unless the final operating point requires it and an allowed existing position is identified.

## Decisions and open items

1. The sensor divider and NTC resistor values are selected from the project hardware specification.
2. The TPS61023 basic 5 V network values are selected from TI's typical application: 1 µH, 10 µF input, 2 × 22 µF output, 732 kΩ / 100 kΩ feedback.
3. Candidate MPNs and packages are not all frozen: check capacitor derating, operating range/load, and exact footprints.
4. The UCC27511 larger parallel bypass capacitor is omitted by design to preserve the no-additions constraint; the existing 0.1 µF bypass remains. Gate-resistor optimization is explicitly waived by the user.
5. No separate feed-forward capacitor is currently selected.

## Manufacturer sources

- TI, [TPS61023 datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf), Figure 8-1 and Sections 8.2.2.1–8.2.2.5.
- TI, [UCC27511/UCC27512 datasheet](https://www.ti.com/lit/ds/symlink/ucc27511.pdf), gate-resistor discussion and VDD bypass/layout guidance.
- TDK, [NTCG104BH103JT1 product information](https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG104BH103JT1).
- Murata, [GRM188R61A106MAAL product information](https://www.murata.com/products/productdetail?partno=GRM188R61A106MAAL%23).
- Murata, [SimSurfing capacitor characteristics](https://ds.murata.com/), for DC-bias/temperature checks of candidate MLCCs.

## Current inductor selection

Use Würth Elektronik WE-MAPI `74438357010` for L1. TI lists it as a recommended 1 µH TPS61023 inductor with 13.5 mΩ maximum DCR, 9.6 A saturation current, and a 4.1 × 4.1 × 3.1 mm package. The EasyEDA library contains the exact device and its `IND-SMD_L4.1-W4.1_SPM40XX` footprint. This replaces the earlier Coilcraft XEL4030 candidate and does not add a component position. The Würth datasheet lists different typical/current-rating values under its own conditions, so use the more conservative TI table values here. Check the actual land pattern against Würth's drawing and calculate the required peak current from the final 5 V load and minimum input voltage before freezing the PCB.

- TI, [TPS61023 datasheet, recommended inductor table](https://www.ti.com/lit/ds/symlink/tps61023.pdf).
- Würth Elektronik, [74438357010 datasheet](https://www.we-online.com/components/products/datasheet/74438357010.pdf).
