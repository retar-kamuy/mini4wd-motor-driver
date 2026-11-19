"""1D copper centerline network sensitivity; not FEM or measured current capacity.
Actual widths/endpoints/intersections/pad contacts/vias are read from the PCB.
Pads are ideal equipotentials. Zones and edge-only trace overlaps are omitted.
No package, solder, crimp, contact or wire resistance is hidden in copper R.
"""
from pathlib import Path
import sys,math,json,hashlib,collections
import pcbnew,numpy as np
root=Path(__file__).resolve().parents[4];out=Path(__file__).parent
pcb=root/'hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb';board=pcbnew.LoadBoard(str(pcb));rho=.01724 # ohm mm^2/m at20C
fps={f.GetReference():f for f in board.GetFootprints()}
def xy(p):return (p.x/1e6,p.y/1e6)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def solve(edges,src,dst):
 adj=collections.defaultdict(set)
 for a,b,R,meta in edges:adj[a].add(b);adj[b].add(a)
 seen={src};todo=[src]
 while todo:
  for q in adj[todo.pop()]-seen:seen.add(q);todo.append(q)
 if dst not in seen:raise RuntimeError('Source/sink not centerline-connected; do not use an unverified shortcut')
 nodes=sorted(seen);idx={k:i for i,k in enumerate(nodes)};unknown=[k for k in nodes if k not in (src,dst)];ii={k:i for i,k in enumerate(unknown)};A=np.zeros((len(ii),len(ii)));rhs=np.zeros(len(ii));valid=[]
 for a,b,R,meta in edges:
  if a not in seen or a==b:continue
  g=1/R;valid.append((a,b,R,meta))
  for x,y in ((a,b),(b,a)):
   if x not in ii:continue
   A[ii[x],ii[x]]+=g
   if y in ii:A[ii[x],ii[y]]-=g
   elif y==src:rhs[ii[x]]+=g
 v=np.linalg.solve(A,rhs) if len(ii) else []
 V={src:1.,dst:0.};V.update({k:float(v[i]) for k,i in ii.items()})
 currents=[((V[a]-V[b])/R,meta,R,a,b) for a,b,R,meta in valid];I=sum((V[src]-V[b])/R if a==src else (V[src]-V[a])/R if b==src else 0 for a,b,R,meta in valid)
 loss=sum(i*i*R for i,_,R,_,_ in currents);residual=max(abs(A@v-rhs)) if len(ii) else 0
 assert I>0 and abs(loss-I)/I<1e-8
 return 1/I,[(i/I,meta,R) for i,meta,R,a,b in currents],float(residual),len(nodes)
# Independent numerical checks of series and parallel networks.
assert abs(solve([(0,1,1,{}),(1,2,2,{})],0,2)[0]-3)<1e-12
assert abs(solve([(0,1,1,{}),(0,1,2,{})],0,1)[0]-2/3)<1e-12

def network(net):
 tracks=[t for t in board.GetTracks() if t.GetNetname()==net and not isinstance(t,pcbnew.PCB_VIA)];vias=[t for t in board.GetTracks() if t.GetNetname()==net and isinstance(t,pcbnew.PCB_VIA)];pads=[(f.GetReference(),p) for f in fps.values() for p in f.Pads() if p.GetNetname()==net];nodes={};data=[];parents=[]
 def node(layer,p):
  key=(layer,round(p[0],6),round(p[1],6))
  if key not in nodes:nodes[key]=len(data);data.append(key);parents.append(len(parents))
  return nodes[key]
 def get(i):
  while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
  return i
 def union(a,b):parents[get(a)]=get(b)
 for t in tracks:
  for p in (xy(t.GetStart()),xy(t.GetEnd())):node(t.GetLayer(),p)
 for v in vias:
  for layer in (pcbnew.F_Cu,pcbnew.B_Cu):node(layer,xy(v.GetPosition()))
 for ref,p in pads:node(pcbnew.F_Cu,xy(p.GetPosition()))
 # Add all non-collinear geometric centerline crossings.
 for j,t in enumerate(tracks):
  a=xy(t.GetStart());r=sub(xy(t.GetEnd()),a)
  for u in tracks[j+1:]:
   if t.GetLayer()!=u.GetLayer():continue
   b=xy(u.GetStart());s=sub(xy(u.GetEnd()),b);den=cross(r,s)
   if abs(den)<1e-12:continue
   d=sub(b,a);x,y=cross(d,s)/den,cross(d,r)/den
   if -1e-8<=x<=1+1e-8 and -1e-8<=y<=1+1e-8:node(t.GetLayer(),(a[0]+x*r[0],a[1]+x*r[1]))
 padnodes={}
 for ref,p in pads:
  mid=node(pcbnew.F_Cu,xy(p.GetPosition()));padnodes[ref,p.GetNumber()]=mid
  for i,(layer,x,y) in enumerate(data):
   if layer==pcbnew.F_Cu and p.HitTest(pcbnew.VECTOR2I(round(x*1e6),round(y*1e6))):union(mid,i)
 # Split every segment at all existing centerline points, including collinear overlaps.
 edges={}
 for t in tracks:
  a=xy(t.GetStart());z=xy(t.GetEnd());d=sub(z,a);length=math.hypot(*d)
  if length<1e-9:continue
  points=[]
  for i,(layer,x,y) in enumerate(data):
   if layer!=t.GetLayer():continue
   q=sub((x,y),a);u=(q[0]*d[0]+q[1]*d[1])/(length*length)
   if -1e-7<=u<=1+1e-7 and abs(cross(q,d))/length<2e-6:points.append((u,i))
  points.sort()
  for (u,i),(v,j) in zip(points,points[1:]):
   m,n=get(i),get(j);L=(v-u)*length
   if m==n or L<1e-9:continue
   key=(min(m,n),max(m,n));R=rho*(L/1000)/(t.GetWidth()/1e6*.035)
   # Coincident segments describe one copper area; keep the widest, not duplicate parallel conductors.
   if key not in edges or R<edges[key][2]:edges[key]=(m,n,R,{'type':'track','uuid':t.m_Uuid.AsString(),'layer':board.GetLayerName(t.GetLayer()),'width_mm':t.GetWidth()/1e6,'length_mm':L})
 for v in vias:
  x,y=xy(v.GetPosition());m,n=get(node(pcbnew.F_Cu,(x,y))),get(node(pcbnew.B_Cu,(x,y)));d=v.GetDrillValue()/1e6;pl=.020;R=rho*.0016/(math.pi*(d+pl)*pl)
  edges[('via',v.m_Uuid.AsString())]=(m,n,R,{'type':'via','uuid':v.m_Uuid.AsString(),'xy_mm':[x,y],'drill_mm':d,'assumed_plating_mm':pl})
 return list(edges.values()),{k:get(i) for k,i in padnodes.items()}

cases=[('drive_VBAT','VBAT',[('J1','1')],[('J2','1')]),('drive_MOTOR','MOTOR_MINUS',[('J2','2')],[('Q1','5')]),('drive_GND','GND',[('Q1',str(n)) for n in (1,2,3)],[('J1','2')]),('brake_VBAT','VBAT',[('J2','1')],[('Q2',str(n)) for n in (1,2,3)]),('brake_MOTOR','MOTOR_MINUS',[('Q2',str(n)) for n in (5,6,7,8)],[('J2','2')]),('diode_VBAT','VBAT',[('D1','1')],[('J2','1')]),('diode_MOTOR','MOTOR_MINUS',[('J2','2')],[('D1','2')])];results=[]
for name,net,src,dst in cases:
 edges,pads=network(net)
 # Zero internal conductor between package terminals; retain this assumption explicitly.
 def merge_group(group):
  ids={pads[k] for k in group};first=min(ids)
  return first,{k:first for k in ids}
 S,sm=merge_group(src);T,tm=merge_group(dst);mapping=sm|tm
 edges=[(mapping.get(a,a),mapping.get(b,b),R,m) for a,b,R,m in edges];R,cc,res,n=solve(edges,S,T);R70,_,_,_=solve([(a,b,R/2 if m['type']=='track' else R,m) for a,b,R,m in edges],S,T)
 vias=[{'current_at5A_A':i*5,**m} for i,m,r in cc if m['type']=='via'];top=sorted([{'current_at5A_A':i*5,'loss_at5A_W':25*i*i*r,**m} for i,m,r in cc if m['type']=='track'],key=lambda x:x['loss_at5A_W'],reverse=True)[:12]
 entry={'case':name,'net':net,'resistance_at20C_35um_ohm':R,'copper_loss_at5A_20C_W':25*R,'resistance_with_70um_copper_via_unchanged_ohm':R70,'solver_KCL_residual_A_for1V':res,'connected_nodes':n,'via_current_distribution':vias,'largest_track_losses':top};results.append(entry);print(name,R,flush=True)
 (out/'power-path-results.json').write_text(json.dumps({'pcb_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),'status':'one_dimensional_centerline_sensitivity_not_FEM_or_current_rating','copper_resistivity_20C_ohm_mm2_per_m':rho,'assumed_copper_mm':.035,'assumed_finished_via_plating_mm':.020,'cases':results,'limitations':['Pads/package common source/drain nodes are ideal equipotential; solder and contact spreading omitted.','Zones omitted; 1D trace centerlines omit 2D current crowding and edge-only overlaps.','Actual finished copper/plating and temperature are not measured.','Via current division belongs to this approximation; equal sharing is not assumed.','Resistance alone is not a thermal or universal5A qualification.']},indent=2)+'\n')
