"""Read-only CAD dimensions for a proposed removable carrier, not a chassis fit check."""
from pathlib import Path
import json,hashlib,pcbnew
r=Path(__file__).resolve().parents[4];out=Path(__file__).parent;p=r/'hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb';b=pcbnew.LoadBoard(str(p));fs={f.GetReference():f for f in b.GetFootprints()}
def box(f,layer):
 rr=[g.GetBoundingBox() for g in f.GraphicalItems() if g.GetLayer()==layer]
 return [min(q.GetX() for q in rr)/1e6,min(q.GetY() for q in rr)/1e6,max(q.GetRight() for q in rr)/1e6,max(q.GetBottom() for q in rr)/1e6] if rr else None
rows=[]
for n in ('J1','J2','MCU1'):
 f=fs[n];rows.append({'reference':n,'position_mm':[f.GetPosition().x/1e6,f.GetPosition().y/1e6],'rotation_deg':f.GetOrientationDegrees(),'fab_graphics_bbox_with_stroke_mm':box(f,pcbnew.F_Fab),'courtyard_graphics_bbox_with_stroke_mm':box(f,pcbnew.F_CrtYd)})
# Candidate upper lips only, x14/25, 3mm wide and0.3mm inset. No claim about chassis attachment.
clips=[]
for x in (14,25):
 for y0,y1 in ((0,.3),(20.7,21)):
  roi=[x-1.5,y0,x+1.5,y1];hits=[]
  for f in fs.values():
   q=box(f,pcbnew.F_CrtYd)
   if q and roi[0]<q[2] and roi[2]>q[0] and roi[1]<q[3] and roi[3]>q[1]:hits.append(f.GetReference())
  clips.append({'proposed_lip_roi_mm':roi,'courtyard_bbox_intersections':hits})
d={'pcb_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'footprint_count':len(fs),'all_parts_front':all(f.GetLayer()==pcbnew.F_Cu for f in fs.values()),'pcb_size_mm':[55,21],'pcb_thickness_mm':b.GetDesignSettings().GetBoardThickness()/1e6,'mounting_hole_footprints':[f.GetReference() for f in fs.values() if 'MountingHole' in str(f.GetFPID())],'NPTH_pads':sum(p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH for f in fs.values() for p in f.Pads()),'components':rows,'nominal_connector_body_x_limits_excluding_graphics_stroke_mm':[-3.52,58.52],'nominal_connector_body_total_length_mm':62.04,'proposed_lips':clips,'usb_service_note':'MCU USB faces left; MCU fab left~9mm and J1 body right~6.38mm leave~2.6mm; standard plug access is an unverified3D interference concern, not solved by changing carrier alone.','scope':'No CAD mutation. Courtyard bbox checks for upper lips only do not establish strength, actual3D connector height, wire clearance or chassis fit.'}
assert all(not x['courtyard_bbox_intersections'] for x in clips)
(out/'board-mechanical-audit.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
