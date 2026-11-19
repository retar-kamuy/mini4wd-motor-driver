# RFQ / DFM review — Mini 4WD motor driver prototype

Status: draft for quotation and DFM review only. Please do not start procurement or production without a separate order approval.

Please quote **2, 5 and 10 fully assembled boards**, with all 38 components on the Top side. Please state any bare-PCB minimum order and surplus separately. Delivery country/postcode: **[requester to complete before sending]**.

The attached package refers to PCB SHA-256 `a7aaab20cce23e1311411c16d31d7868e5d10233389f3a2941676cce5c175094`. Use `gerber-preview.zip`, `bom-turnkey.csv`, `cpl-top-mm.csv`, the pad orientation reference and pad coordinate CSVs. The BOM quantities are per board; please add and itemize your sourcing minimums and assembly losses. No substitutions or design edits without prior approval.

Quotation baseline: 55×21mm, two copper layers, FR-4, 1.6mm thickness, minimum finished copper 35µm on both layers, minimum via wall copper 20µm, ENIG, green solder mask, white silkscreen and lead-free assembly. Please confirm the achievable tolerances and process. A 70µm copper option may be quoted separately, subject to DFM review of the existing 0.127mm routing and spacing.

Please return `dfm-response.csv` and `procurement-response.csv`, covering these items:

1. Procure and assemble all parts, including the exact **Seeed Studio102010610 XIAO MG24 Sense without headers** as a castellated module, both Molex43650-0214 connectors, Analog Devices LTC6994IS6-2#TRMPBF and TI UCC27524ADR. Confirm module handling, secondary reflow compatibility, microphone/camera precautions, packaging and any factory manual operations. End-user soldering is not an acceptable completion method.
2. Fill, cap and planarize the six vias overlapping the Q1 drain land, listed in `assembly/q1-pad-vias-mm.csv`, using a process suitable for reliable SMT solder joints. Confirm the process, planarity and inspection. Bottom tenting alone is not via filling.
3. Keep the Bottom side free of components, with all 82 vias tented on the Bottom. Confirm CAM shows no Bottom mask openings. Preserve module-area tenting on both sides where specified.
4. Propose panel rails/carriers, panel fiducials, clamping/support and depanelization. There are no on-board fiducials/tooling holes. The outward-facing connectors extend beyond both board ends; their total projected body length is approximately 62.04mm. Protect near-edge components during handling and separation.
5. Confirm every placement origin, rotation, pin1, diode cathode, module pin function and connector polarity using your part libraries. CPL coordinates are in mm: X=KiCad absolute X, Y=minus KiCad absolute Y; rotation is KiCad modulo360. Return a placement preview and any revised CPL for approval. The coordinates identify footprint origins and do not guarantee pickup centers.
6. State PCB electrical inspection, AOI/polarity/bridge/joint inspection and X-ray availability/cost for hidden solder joints. No firmware programming or motor power testing is requested without an agreed test procedure.

Please itemize PCB fabrication, parts including MOQ/losses/surplus, setup, stencil, panel/carrier, via fill/cap, assembly/manual operations, inspection, shipping and taxes. Include lead time, quotation expiry, unavailable parts, consignment requirements and surplus return terms.

This is an initial engineering prototype. The package passed CAD ERC/DRC and connectivity checks, but continuous 5A, full temperature/power sequencing behavior and EMC compliance have not been qualified. Functional and temperature measurements will be performed after assembly under current limitation. Please identify any manufacturing changes you require before a production order.
