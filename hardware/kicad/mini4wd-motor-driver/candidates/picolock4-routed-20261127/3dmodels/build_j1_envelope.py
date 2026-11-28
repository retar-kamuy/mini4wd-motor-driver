#!/usr/bin/env python3
"""Create a conservative XEL4030-102 envelope, not a vendor detailed model."""
from pathlib import Path
from math import sqrt

rows=[]
def entity(value):
    rows.append(value)
    return f'#{len(rows)}'
def point(v):return entity("CARTESIAN_POINT('',("+','.join(f'{x:.8g}' for x in v)+'))')
def direction(v):return entity("DIRECTION('',("+','.join(f'{x:.8g}' for x in v)+'))')
def sub(a,b):return [a[i]-b[i] for i in range(3)]
def norm(v):
    n=sqrt(sum(x*x for x in v));return [x/n for x in v]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
app=entity("APPLICATION_CONTEXT('automotive design')")
entity(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,{app})")
pc=entity(f"PRODUCT_CONTEXT('',{app},'mechanical')")
product=entity(f"PRODUCT('J1_PICOLOCK_ENVELOPE_APPROX','J1_PICOLOCK_ENVELOPE_APPROX','11.95x7.60x2.60 mm provisional envelope; not a vendor 3D model',({pc}))")
formation=entity(f"PRODUCT_DEFINITION_FORMATION('','',{product})")
pdc=entity(f"PRODUCT_DEFINITION_CONTEXT('part definition',{app},'design')")
pd=entity(f"PRODUCT_DEFINITION('design','',{formation},{pdc})")
pds=entity(f"PRODUCT_DEFINITION_SHAPE('','',{pd})")
origin=point([0,0,0]);zdir=direction([0,0,1]);xdir=direction([1,0,0]);axis=entity(f"AXIS2_PLACEMENT_3D('',{origin},{zdir},{xdir})")
mm=entity('(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))')
radian=entity('(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))')
steradian=entity('(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())')
uncertainty=entity(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-7),{mm},'distance_accuracy_value','')")
context=entity(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT(({uncertainty})) GLOBAL_UNIT_ASSIGNED_CONTEXT(({mm},{radian},{steradian})) REPRESENTATION_CONTEXT('',''))")
verts=[[-5.975,-3.435,0],[5.975,-3.435,0],[5.975,4.165,0],[-5.975,4.165,0],[-5.975,-3.435,2.6],[5.975,-3.435,2.6],[5.975,4.165,2.6],[-5.975,4.165,2.6]]
points=[point(v) for v in verts];vp=[entity(f"VERTEX_POINT('',{p})") for p in points]
faces=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
edges={};faceids=[]
for ids in faces:
    oriented=[]
    for a,b in zip(ids,ids[1:]+ids[:1]):
        key=tuple(sorted((a,b)))
        if key not in edges:
            vec=entity(f"VECTOR('',{direction(norm(sub(verts[b],verts[a])))},1.)")
            line=entity(f"LINE('',{points[a]},{vec})")
            edges[key]=(a,b,entity(f"EDGE_CURVE('',{vp[a]},{vp[b]},{line},.T.)"))
        start,end,edge=edges[key]
        oriented.append(entity(f"ORIENTED_EDGE('',*,*,{edge},{'.T.' if (a,b)==(start,end) else '.F.'})"))
    loop=entity("EDGE_LOOP('',("+','.join(oriented)+'))')
    bound=entity(f"FACE_OUTER_BOUND('',{loop},.T.)")
    a,b,c=[verts[i] for i in ids[:3]]
    placement=entity(f"AXIS2_PLACEMENT_3D('',{points[ids[0]]},{direction(norm(cross(sub(b,a),sub(c,b))))},{direction(norm(sub(b,a)))})")
    plane=entity(f"PLANE('',{placement})")
    faceids.append(entity(f"ADVANCED_FACE('',({bound}),{plane},.T.)"))
shell=entity("CLOSED_SHELL('',("+','.join(faceids)+'))')
solid=entity(f"MANIFOLD_SOLID_BREP('J1 approximate envelope',{shell})")
rep=entity(f"ADVANCED_BREP_SHAPE_REPRESENTATION('',({axis},{solid}),{context})")
entity(f"SHAPE_DEFINITION_REPRESENTATION({pds},{rep})")
color=entity("COLOUR_RGB('J1 approximate envelope black',0.18,0.18,0.18)")
fillcolor=entity(f"FILL_AREA_STYLE_COLOUR('',{color})")
fill=entity(f"FILL_AREA_STYLE('',({fillcolor}))")
ssfill=entity(f"SURFACE_STYLE_FILL_AREA({fill})")
side=entity(f"SURFACE_SIDE_STYLE('',({ssfill}))")
usage=entity(f"SURFACE_STYLE_USAGE(.BOTH.,{side})")
psa=entity(f"PRESENTATION_STYLE_ASSIGNMENT(({usage}))")
styled=entity(f"STYLED_ITEM('',({psa}),{solid})")
entity(f"MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('',({styled}),{context})")
header="""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('J1 approximate envelope only: Molex 205338-0004 simplified envelope; not a manufacturer detailed 3D model'),'2;1');
FILE_NAME('J1_PICOLOCK_ENVELOPE_APPROX.step','2026-11-26T00:00:00',('mini4wd project'),('mini4wd project'),'manual STEP generator','manual STEP generator','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));
ENDSEC;
DATA;
"""
output=Path(__file__).with_name('J1_PICOLOCK_ENVELOPE_APPROX.step')
output.write_text(header+''.join(f'#{i} = {v};\n' for i,v in enumerate(rows,1))+'ENDSEC;\nEND-ISO-10303-21;\n')
print(output)
