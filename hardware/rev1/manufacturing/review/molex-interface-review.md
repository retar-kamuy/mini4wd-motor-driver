# Molex Micro-Fit 3.0 Interface Review

Review date: 2026-10-04  
Status: manufacturer data verified; PCB footprint still needs to be entered into the EasyEDA project and visually checked against the drawing.

## Selected connector parts

| Function | Manufacturer number | Qty | Verified data |
|---|---|---:|---|
| Board header, battery input | 43650-0214 | 1 | Micro-Fit 3.0, 2 circuits, single row, right-angle SMT with solder nails, 3.00 mm pitch, recommended PCB thickness 1.60 mm, gold mating surface / matte-tin solder tails, per-contact maximum 8.5 A |
| Board header, motor output | 43650-0214 | 1 | Same as above |
| Cable receptacle housing | 43645-0200 | 2 | 2-circuit, single-row receptacle housing; drawing identifies series 43645 as mating with header 43650 |
| Female crimp terminal for 18 AWG | 43030-0038 | 4 | Female Micro-Fit 3.0 crimp terminal, tin plating, 18 AWG / 0.75 mm² |

## Electrical rating interpretation

Molex lists 8.5 A as the header's maximum current per contact. Its series specification's 2-circuit, wire-to-board reference derating table lists 8.5 A for 18 AWG. That table is reference guidance based on a maximum 30 °C temperature rise, tinned stranded wire, tin-plated terminals, and all circuits powered. Molex also requires application-specific derating for ambient temperature, PCB copper, neighboring heat sources, wire construction, length, and crimp quality. Therefore this confirms connector headroom for the 5 A target as a component-selection basis, but does not qualify the assembled board for 5 A continuous operation.

## PCB land and placement requirements

The official `SD-43650-005` drawing (`436500414_sd.pdf`) is the series drawing whose part-number chart explicitly includes 43650-0214 in the 2-circuit, finish-C column. Use its page-1 `PCB LAYOUT: COMPONENT SIDE` as the source for the footprint, including the 3.00 mm contact pitch, 1.27 mm typical land spacing/geometry callouts, and solder-nail lands. The drawing also limits header placement relative to the board edge to avoid interference with the mating receptacle. Preserve the pin-1 indication and outward-facing orientation in both connector placements.

The land geometry is not yet entered into EasyEDA. The project must not use a visually similar through-hole 43650 footprint. Confirm pad numbering, solder mask, nail lands, connector body overhang, and mating housing clearance after the custom/verified SMD footprint is placed.

## Manufacturer sources

- Header product page: https://www.molex.com/en-us/products/part-detail/0436500214
- Header series drawing `SD-43650-005`: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/436/43650/436500414_sd.pdf
- Header product specification `PS-43650-001`: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/436/43650/PS-43650-001.pdf
- Two-circuit receptacle housing series chart: https://www.molex.com/en-us/products/series-chart/43645
- 18 AWG terminal product page: https://www.molex.com/en-us/products/part-detail/0430300038
- Terminal series chart: https://www.molex.com/en-us/products/series-chart/43030
