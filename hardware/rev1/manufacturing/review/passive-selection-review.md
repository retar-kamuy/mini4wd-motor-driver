# Rev1 passive component selection review

Date: 2026-10-11  
Status: Use `passive-design-review.md` as the current datasheet-based value selection. No new resistor or capacitor positions may be added. This file is retained as an earlier candidate review; its source-layout mapping method is superseded.

## Resistors

For the current values, use Vishay CRCW0603 0603 (1608 metric), 1%, 0.1 W as candidates for the documented 22 kOhm / 10 kOhm VBAT and MID dividers, 10 kOhm NTC divider, and TI typical TPS61023 732 kOhm / 100 kOhm feedback pair. Per the user's direction, do not pursue gate-resistor optimization where the source project specifies no value or switching target. Do not add resistor placements.

## TPS61023 boost stage

TI's TPS61023 typical 5 V design values are adopted for the boost stage: 1 uH, 10 uF input, 2 x 22 uF output, and 732 kOhm / 100 kOhm feedback. L1 is Würth Elektronik 74438357010, a TI-recommended 1 uH part with an exact EasyEDA library device and footprint; verify peak current and the manufacturer land pattern before PCB freeze. The capacitor MPNs remain subject to DC-bias and footprint checks. The 0.1 uF bypass belongs to UCC27511, not the TPS61023 typical circuit. UCC27511 also recommends a larger parallel VDD bypass capacitor; see `passive-design-review.md` for the no-additions conflict.

TI's typical application is a starting design, not proof that this board meets its load or battery envelope. Verify converter operation over the intended battery range, 5 V load, loop stability, and effective ceramic capacitance after DC-bias derating before layout freeze.

## XIAO 5 V isolation diode

The previously considered Nexperia PMEG2010EA,115 supply-isolation diode is on hold. It is not an explicit `specs/001-smt-gerber-board/spec.md` improvement, and must not become a new footprint unless the existing source layout confirms an equivalent diode position. It is distinct from the motor flyback protection mentioned in `specs/001-smt-gerber-board/spec.md` and is not permission to add a passive position.

## References

- [TI TPS61023 datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf)
- [TI TPS61023EVM-052 user's guide and BOM](https://www.ti.com/lit/ug/slvubp5/slvubp5.pdf)
- [Coilcraft XEL4030 datasheet](https://www.coilcraft.com/getmedia/8245f050-f190-4295-8c41-7c03d662ee3d/xel4030.pdf)
- [Würth Elektronik 74438357010 datasheet](https://www.we-online.com/components/products/datasheet/74438357010.pdf)
- [Murata 10 uF capacitor](https://www.murata.com/products/productdetail?partno=GRM188R61A106MAAL%23)
- [Murata 22 uF capacitor](https://www.murata.com/products/productdetail?partno=GRM188R61A226ME15D)
- [Nexperia PMEG2010EA](https://www.nexperia.com/products/diodes/schottky-diodes-and-rectifiers/schottky-diodes-and-rectifiers-if-1-a/PMEG2010EA.html)
- [Vishay CRCW resistor series datasheet](https://www.vishay.com/docs/20035/crcw0306e3.pdf)
