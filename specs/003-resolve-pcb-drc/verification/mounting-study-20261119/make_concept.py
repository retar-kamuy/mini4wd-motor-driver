from pathlib import Path
p=Path(__file__).parent
# Geometrically based concept: carrier dimensions and support height are proposals.
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="760" viewBox="0 0 1500 760"><defs><marker id="a" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M7 3.5 0 0 0 7Z" fill="#374151"/></marker></defs><rect width="1500" height="760" fill="white"/><style>text{font-family:sans-serif;fill:#172033;font-size:18px}.small{font-size:15px}.dim{fill:none;stroke:#374151;stroke-width:1.5;marker-start:url(#a);marker-end:url(#a)}</style><text x="50" y="38" font-size="25">Removable open carrier: concept only; chassis fit not verified</text><text x="50" y="66" class="small">Current PCB/connector outlines. Carrier/support dimensions are proposals. Plug and cable space is additional. Plan is schematic.</text>''']
X=lambda x:220+x*17;Y=lambda y:150+y*13
# Plan shapes preserve board coordinate dimensions with separate axis scales, explicitly schematic.
def rect(x,y,w,h,fill,stroke,rx=0,dash=''):
 s.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*17:.1f}" height="{h*13:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2" {dash}/>')
rect(-1.1,-1.1,57.2,23.2,'#fff7ed','#ea580c',10)
rect(-.3,-.3,55.6,21.6,'white','#fdba74',8)
# Open ends; stop ears are at corners, not across the connector opening.
rect(-1.2,4.8,1.3,11.8,'white','white');rect(54.9,4.8,1.3,11.8,'white','white')
rect(0,0,55,21,'#f3f4f6','#374151',12)
rect(9,1.6,21,17.8,'#dbeafe','#2563eb',3)
rect(30.8,1,16.8,19,'#fce7f3','#db2777',4,dash='stroke-dasharray="6 4"')
for x in (-3.52,48.62):rect(x,5.875,9.9,9.65,'#334155','#111827',5)
for x in (12.5,23.5):
 rect(x,-1.1,3,1.4,'#fdba74','#c2410c',2);rect(x,20.7,3,1.4,'#fdba74','#c2410c',2)
s.extend([f'<text x="{X(14)}" y="{Y(8)}">XIAO</text>',f'<text x="{X(13)}" y="{Y(10.5)}">USB ←</text>',f'<text x="{X(32)}" y="{Y(10)}">Other parts</text>',f'<text x="{X(32)}" y="{Y(12)}" class="small">approximate</text>',f'<text x="{X(-1.8)}" y="{Y(11)}" style="fill:white">J1</text>',f'<text x="{X(51)}" y="{Y(11)}" style="fill:white">J2</text>',f'<path d="M{X(9)} {Y(10.5)} H{X(6.6)}" stroke="#dc2626" stroke-width="4" marker-end="url(#a)"/>',f'<path d="M{X(-3.7)} {Y(10.7)} H{X(-10)}" stroke="#64748b" stroke-width="3" marker-end="url(#a)"/>',f'<path d="M{X(58.7)} {Y(10.7)} H{X(65)}" stroke="#64748b" stroke-width="3" marker-end="url(#a)"/>',f'<path d="M{X(0)} 115 H{X(55)}" class="dim"/><text x="{X(24)}" y="105">PCB 55 mm</text>',f'<path d="M{X(-3.52)} 465 H{X(58.52)}" class="dim"/><text x="{X(16)}" y="490">Connector body projection62.04 mm</text>',f'<text x="{X(0)}" y="88" class="small">Orange: proposed carrier/lips; PCB width21 mm; carrier width about23-24 mm</text>'])
s.append('''<text x="55" y="530">Side concept: height budget is provisional</text><rect x="90" y="684" width="750" height="18" rx="5" fill="#cbd5e1"/><text x="100" y="728">Support on chassis/retainer; no adhesive on cell wrappers.</text><rect x="140" y="647" width="70" height="37" fill="#fed7aa"/><rect x="720" y="647" width="70" height="37" fill="#fed7aa"/><rect x="130" y="621" width="670" height="26" fill="#334155"/><text x="220" y="670" class="small">Insulation + gap: provisional2 mm from support to PCB underside</text><rect x="190" y="579" width="300" height="42" fill="#dbeafe" stroke="#2563eb"/><rect x="650" y="509" width="130" height="112" rx="5" fill="#475569"/><text x="860" y="575">PCB thickness1.6 mm</text><text x="860" y="608">Provisional6.98 mm connector height budget:</text><text x="860" y="637">2 + 1.6 + 6.98 + 0.5 ≈ 11.1 mm</text><text x="860" y="665" class="small">11-12 mm clearance is a planning value.</text><text x="860" y="690" class="small">Actual plug/wires and3D assembly may need more.</text></svg>''')
(p/'mounting-concept.svg').write_text(''.join(s))
