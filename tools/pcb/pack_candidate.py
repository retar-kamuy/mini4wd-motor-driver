"""Create an unrouted placement candidate. Does not overwrite canonical PCB.
Run with KiCad's Python and sexpdata; geometry-only, not a power/EMC approval.
"""
from pathlib import Path
import argparse,json,random,shutil,math
import pcbnew,sexpdata
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
if args.output.resolve()==args.source.resolve():raise SystemExit('Output must differ from source')
cache_root=Path(__file__).resolve().parents[2]/'.cache/routing'
if not args.output.resolve().is_relative_to(cache_root.resolve()):raise SystemExit('Trial output must be inside .cache/routing/')
args.output.mkdir(parents=True,exist_ok=True)
for p in args.source.iterdir():
 if p.is_file() and (p.suffix in {'.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_sym'} or p.name.endswith('-lib-table')):shutil.copy2(p,args.output/p.name)
for name in ['board-routed.pretty','mini4wd-motor-driver.pretty']:shutil.copytree(args.source/name,args.output/name,dirs_exist_ok=True)
p=args.output/'mini4wd-motor-driver.kicad_pcb';tree=sexpdata.loads(p.read_text());tree=[x for x in tree if not(isinstance(x,list) and x and str(x[0]) in ['segment','via','zone'])];p.write_text(sexpdata.dumps(tree));b=pcbnew.LoadBoard(str(p));fs={f.GetReference():f for f in b.GetFootprints()}
def box(f):
 bs=[g.GetBoundingBox() for g in f.GraphicalItems() if g.GetLayer()==pcbnew.F_CrtYd]
 return min(g.GetX() for g in bs)/1e6,min(g.GetY() for g in bs)/1e6,max(g.GetRight() for g in bs)/1e6,max(g.GetBottom() for g in bs)/1e6
for ref,x,y,angle in [('MCU1',19.5,10.5,0),('J1',5.55,10.5,270),('J2',49.45,10.5,90)]:
 f=fs[ref];f.SetOrientationDegrees(angle);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
items=[]
for ref,f in fs.items():
 if ref in ['MCU1','J1','J2']:continue
 f.SetOrientationDegrees(0);f.SetPosition(pcbnew.VECTOR2I(0,0));x,y,x1,y1=box(f);items.append((ref,x1-x,y1-y))
def contains(a,b):return b[0]>=a[0]-1e-8 and b[1]>=a[1]-1e-8 and b[0]+b[2]<=a[0]+a[2]+1e-8 and b[1]+b[3]<=a[1]+a[3]+1e-8
best=None;best_score=math.inf;best_seed=None
# Prefer the power stage near the motor connector and keep the boost loop
# together. This is a placement search, not electrical or thermal validation.
targets={'Q1':(43,10),'Q2':(40,6),'U104':(40,16),'L1':(33,3),'U2':(33,6),'C1':(32,6),'C2':(35,6),'C3':(35,7),'R1':(32,8),'R2':(32,9)}
neighbors={'C101':'U101','C102':'U102','C103':'U103','C104':'U104','C105':'U104','C106':'U105','R101':'U101','R104':'U104'}
power=set(targets)
for seed in range(1500):
 random.seed(seed);free=[(30.2,.5,16.55,20),(.5,.5,7.8,4.2),(.5,16.3,7.8,4.2),(47.2,.5,7.3,4.2),(47.2,16.3,7.3,4.2)];placed={}
 for ref,w,h in sorted(items,key=lambda v:v[1]*v[2]*(1+random.random()*1.5),reverse=True):
  options=[]
  for x,y,fw,fh in free:
   for rot,rw,rh in [(0,w+.15,h+.15),(90,h+.15,w+.15)]:
    if ref in power and x<30:continue
    if rw<=fw and rh<=fh:
     target=targets.get(ref)
     if ref in neighbors and neighbors[ref] in placed:target=placed[neighbors[ref]][:2]
     distance=math.hypot(x+rw/2-target[0],y+rh/2-target[1]) if target else 0
     options.append(((min(fw-rw,fh-rh)+distance*.6,max(fw-rw,fh-rh)),x,y,rw,rh,rot))
  if not options:break
  _,x,y,rw,rh,rot=min(options);placed[ref]=(x+.075,y+.075,rot);nf=[]
  for a in free:
   ax,ay,aw,ah=a
   if ax>=x+rw or ax+aw<=x or ay>=y+rh or ay+ah<=y:nf.append(a);continue
   if x>ax:nf.append((ax,ay,x-ax,ah))
   if x+rw<ax+aw:nf.append((x+rw,ay,ax+aw-x-rw,ah))
   if y>ay:nf.append((ax,ay,aw,y-ay))
   if y+rh<ay+ah:nf.append((ax,y+rh,aw,ay+ah-y-rh))
  free=[a for i,a in enumerate(nf) if not any(i!=j and contains(v,a) and (v!=a or j<i) for j,v in enumerate(nf))]
 if len(placed)==len(items):
  score=sum(math.dist(placed[r][:2],t) for r,t in targets.items())
  score+=sum(3*math.dist(placed[r][:2],placed[t][:2]) for r,t in neighbors.items())
  score+=sum(5*math.dist(placed['U2'][:2],placed[t][:2]) for t in ['L1','C1','C2','C3','R1','R2'])
  if score<best_score:best=placed;best_score=score;best_seed=seed
if best is None:raise SystemExit('No placement found')
for ref,(x,y,angle) in best.items():
 f=fs[ref];f.SetOrientationDegrees(angle);f.SetPosition(pcbnew.VECTOR2I(0,0));x0,y0,_,_=box(f);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x-x0),pcbnew.FromMM(y-y0)))
for f in b.GetFootprints():
 f.Reference().SetLayer(pcbnew.F_Fab);f.Value().SetLayer(pcbnew.F_Fab)
for g in b.GetDrawings():
 if isinstance(g,pcbnew.PCB_TEXT) and g.GetLayer()==pcbnew.F_SilkS:g.SetLayer(pcbnew.F_Fab)
labels={'B+':(7.8,9),'B-':(7.8,12),'M+':(49.45,13.8),'M-':(49.45,7.2)}
for g in b.GetDrawings():
 if isinstance(g,pcbnew.PCB_TEXT) and g.GetText() in labels:
  x,y=labels[g.GetText()];g.SetLayer(pcbnew.F_SilkS);g.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)));g.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(.8),pcbnew.FromMM(.8)));g.SetTextThickness(pcbnew.FromMM(.12));g.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER);g.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
b.BuildConnectivity();pcbnew.SaveBoard(str(p),b)
(args.output/'placement.json').write_text(json.dumps({ref:{'x':f.GetPosition().x/1e6,'y':f.GetPosition().y/1e6,'rotation':f.GetOrientationDegrees()} for ref,f in fs.items()},indent=2)+'\n')
print('Placed',len(fs),'footprints; seed',best_seed,'score',best_score,flush=True)
print('DSN export:',pcbnew.ExportSpecctraDSN(b,str(args.output/'board.dsn')),flush=True)
