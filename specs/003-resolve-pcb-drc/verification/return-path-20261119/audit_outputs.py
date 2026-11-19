#!/usr/bin/env python3
from pathlib import Path
import csv,json,hashlib,math
import pcbnew
root=Path(__file__).resolve().parents[4];analysis=Path(__file__).resolve().parent
preview=analysis.parent/'prototype-preview-20261119'
pcb=root/'hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb'
b=pcbnew.LoadBoard(str(pcb));fps={f.GetReference():f for f in b.GetFootprints()}
cpl=list(csv.DictReader((preview/'cpl-front.csv').open()));bm=list(csv.DictReader((preview/'bom-candidates.csv').open()))
cm=[];bmismatch=[];seen=set();bomrefs=set()
for row in cpl:
 ref=row['Ref'];seen.add(ref);f=fps.get(ref)
 if f is None:cm.append({'ref':ref,'error':'missing PCB footprint'});continue
 xy=f.GetPosition();delta=(float(row['Rot'])-f.GetOrientationDegrees())%360
 checks={'x':abs(float(row['PosX'])-xy.x/1e6)<1e-6,'y':abs(float(row['PosY'])+xy.y/1e6)<1e-6,'rotation':min(delta,360-delta)<1e-6,'side':row['Side']=='top' and f.GetLayer()==pcbnew.F_Cu,'value':row['Val']==f.GetValue(),'package':row['Package']==str(f.GetFPID().GetLibItemName())}
 if not all(checks.values()):cm.append({'ref':ref,'checks':checks})
for row in bm:
 refs=row['Reference'].split(',')
 if int(row['Qty'])!=len(refs):bmismatch.append({'row':row['Reference'],'error':'quantity differs'})
 for ref in refs:
  bomrefs.add(ref);f=fps.get(ref)
  if f is None:bmismatch.append({'ref':ref,'error':'missing PCB footprint'});continue
  for key in ('MPN','Manufacturer'):
   actual=f.GetFieldText(key)
   if actual!=row[key]:bmismatch.append({'ref':ref,'field':key,'bom':row[key],'pcb':actual})
  if row['Value']!=f.GetValue():bmismatch.append({'ref':ref,'field':'Value'})
result={'pcb_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),'cpl_rows':len(cpl),'bom_rows':len(bm),'bom_components':sum(int(r['Qty']) for r in bm),'cpl_missing_references':sorted(set(fps)-seen),'bom_missing_references':sorted(set(fps)-bomrefs),'cpl_pcb_mismatches':cm,'bom_pcb_mismatches':bmismatch,'transform':'CPL X=PCB X, CPL Y=-PCB Y; rotation equivalent modulo360; all top/F.Cu','vendor_library_rotation_and_procurement':'unconfirmed'}
(analysis/'output-correspondence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
assert not(cm or bmismatch or set(fps)-seen or set(fps)-bomrefs)
