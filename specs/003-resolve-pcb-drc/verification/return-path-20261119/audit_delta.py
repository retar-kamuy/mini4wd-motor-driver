from pathlib import Path
import hashlib,json,collections
import pcbnew
r=Path(__file__).resolve().parents[4];out=Path(__file__).parent;c=r/'hardware/kicad/mini4wd-motor-driver';old=r/'.cache/return-path-20261119/canonical-before';A=pcbnew.LoadBoard(str(old/'mini4wd-motor-driver.kicad_pcb'));B=pcbnew.LoadBoard(str(c/'mini4wd-motor-driver.kicad_pcb'))
def sig(t):
 return (t.GetNetname(),t.GetLayerName(),tuple(t.GetStart()),tuple(t.GetEnd()),t.GetWidth(pcbnew.F_Cu) if isinstance(t,pcbnew.PCB_VIA) else t.GetWidth(),t.GetDrillValue() if isinstance(t,pcbnew.PCB_VIA) else None)
def tracks(b):return {t.m_Uuid.AsString():sig(t) for t in b.GetTracks()}
a,b=tracks(A),tracks(B);removed={k:v for k,v in a.items() if k not in b};added={k:v for k,v in b.items() if k not in a};changed={k:{'before':a[k],'after':b[k]} for k in a.keys()&b.keys() if a[k]!=b[k]}
fa={f.GetReference():f for f in A.GetFootprints()};fb={f.GetReference():f for f in B.GetFootprints()};placement=[]
for ref in fa.keys()&fb.keys():
 x,y=fa[ref],fb[ref]
 if tuple(x.GetPosition())!=tuple(y.GetPosition()) or x.GetOrientationDegrees()!=y.GetOrientationDegrees():placement.append({'reference':ref,'before':[v/1e6 for v in x.GetPosition()]+[x.GetOrientationDegrees()],'after':[v/1e6 for v in y.GetPosition()]+[y.GetOrientationDegrees()]})
oldpower={t.m_Uuid.AsString():sig(t) for t in A.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetWidth(pcbnew.F_Cu)==800000 and t.GetDrillValue()==400000}
newpower={t.m_Uuid.AsString():sig(t) for t in B.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetWidth(pcbnew.F_Cu)==800000 and t.GetDrillValue()==400000}
result={'before_pcb_sha256':hashlib.sha256((old/'mini4wd-motor-driver.kicad_pcb').read_bytes()).hexdigest(),'after_pcb_sha256':hashlib.sha256((c/'mini4wd-motor-driver.kicad_pcb').read_bytes()).hexdigest(),'placement_changes':placement,'added_footprints':sorted(fb.keys()-fa.keys()),'removed_tracks_by_net':dict(collections.Counter(v[0] for v in removed.values())),'added_tracks_by_net':dict(collections.Counter(v[0] for v in added.values())),'modified_existing_tracks':changed,'power_vias_33_identical_uuid_net_position_size_drill':oldpower==newpower and len(newpower)==33,'project_settings_unchanged':(old/'mini4wd-motor-driver.kicad_pro').read_bytes()==(c/'mini4wd-motor-driver.kicad_pro').read_bytes(),'root_schematic_unchanged':(old/'mini4wd-motor-driver.kicad_sch').read_bytes()==(c/'mini4wd-motor-driver.kicad_sch').read_bytes(),'J1_J2_pad_positions_nets_unchanged':all([(p.GetNumber(),tuple(p.GetPosition()),p.GetNetname()) for p in fa[f].Pads()]==[(p.GetNumber(),tuple(p.GetPosition()),p.GetNetname()) for p in fb[f].Pads()] for f in ('J1','J2')),'BOM_changes':['C105 22uF10V GRM188R61A226ME15D','R106 33ohm CRCW040233R0FKED','R107 2.2kohm CRCW04022K20FKED'],'zones':[]}
for z in B.Zones():
 bb=z.Outline().BBox();result['zones'].append({'net':z.GetNetname(),'layer':B.GetLayerName(z.GetLayer()),'outline_bbox_mm':[bb.GetX()/1e6,bb.GetY()/1e6,bb.GetRight()/1e6,bb.GetBottom()/1e6],'filled_polygon_count':z.GetFilledPolysList(z.GetLayer()).OutlineCount()})
(out/'geometry-delta.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['power_vias_33_identical_uuid_net_position_size_drill'] and result['project_settings_unchanged'] and result['J1_J2_pad_positions_nets_unchanged'];assert [p['reference'] for p in placement]==['L1']
