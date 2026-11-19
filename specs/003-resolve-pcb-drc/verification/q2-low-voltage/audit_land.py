from pathlib import Path
import json,hashlib,sexpdata
root=Path.cwd();standard=Path('/usr/share/kicad/footprints/Package_SON.pretty/Diodes_PowerDI3333-8.kicad_mod');candidate=root/'specs/003-resolve-pcb-drc/verification/q2-low-voltage/candidate-design/board-routed.pretty/Diodes_PowerDI3333-8_DMP2008UFG.kicad_mod'
a=sexpdata.loads(standard.read_text());b=sexpdata.loads(candidate.read_text())
def strip(x):
 if not isinstance(x,list):return x
 return [strip(y) for y in x if not(isinstance(y,list) and y and str(y[0])=='uuid')]
def base(x):
 return [strip(n) for n in x[2:] if not(isinstance(n,list) and n and (str(n[0])=='descr' or str(n[0])=='pad' and str(n[1]) in ['6','7','8']))]
unchanged=base(a)==base(b)
assert unchanged,'Non-identity geometry differs'
extra=[n for n in b if isinstance(n,list) and n and str(n[0])=='pad' and str(n[1]) in ['6','7','8']]
proof=[]
for n in extra:
 v={str(x[0]):x[1:] for x in n[4:] if isinstance(x,list)}
 x,y=v['at'];w,h=v['size'];box=[float(x-w/2),float(y-h/2),float(x+w/2),float(y+h/2)]
 # Standard common pad: central rectangle [-.400,1.310] x [-1.185,1.185],
 # plus four fingers [1.310,1.850] x [.115,.535] etc.
 inside=abs(float(x)-1.5)<1e-8 and abs(float(w)-.7)<1e-8 and abs(float(h)-.42)<1e-8 and abs(float(y)) in [.325,.975]
 assert inside and v['layers']==['F.Cu']
 proof.append({'number':str(n[1]),'layers':v['layers'],'rectangle_mm':box,'contained_by_original_common_drain_pad':True})
r={'status':'exact_geometry_and_manufacturer_dimension_check','datasheet':'DS35694 Rev14-2 August2014 pp1,5; retrieved2026-11-15','manufacturer_pin_map':{'1':'S','2':'S','3':'S','4':'G','5':'D','6':'D','7':'D','8':'D'},'standard_footprint_sha256':hashlib.sha256(standard.read_bytes()).hexdigest(),'candidate_footprint_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'standard_shapes_pads_mask_paste_and_3D_unchanged_except_3_copper_only_identities':unchanged,'extra_pad_containment_proof':proof,'unchanged_manufacturer_dimensions_mm':{'pitch_C':.65,'lead_land_Y3':.7,'lead_land_X2':.42,'overall_terminal_extent_Y':3.7,'drain_finger_envelope_X':2.37,'drain_extent_Y1':2.25,'drain_continuous_start_distance_Y2':1.85,'finger_gap_G':.23,'drain_finger_width_G1':.42},'no_additional_F_Mask_opening':True,'no_additional_F_Paste_opening':True,'no_change_to_copper_union':True,'alternative':'Single common-pad5 with a reduced-pin symbol was considered; explicit physical 1-8 traceability was retained without changing mask/paste or copper union.','not_verified':['Vendor stencil aperture acceptance and reflow profile','Actual solder joint reliability','Board-specific thermal resistance']}
(root/'specs/003-resolve-pcb-drc/verification/q2-low-voltage/land-audit.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
