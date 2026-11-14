"""Trial power backbone for the explicitly checked placement, never canonical.

This establishes routing geometry, not a 5 A or thermal qualification.
"""
from pathlib import Path
import argparse
import re
import pcbnew

ap = argparse.ArgumentParser()
ap.add_argument('board', type=Path)
args = ap.parse_args()
if '.cache/routing/' not in str(args.board):
    raise SystemExit('This experiment accepts only .cache/routing/ boards')
b = pcbnew.LoadBoard(str(args.board))
fs = {f.GetReference(): f for f in b.GetFootprints()}
for ref, xy in {'Q1': (49.48, 18.18), 'Q2': (33.85, 3.349999),
                'J1': (5.55, 10.5), 'J2': (49.45, 10.5),
                'U104': (41.3, 3.3), 'U2': (35.23, 7.35),
                'U102': (44.9, 8.25), 'U101': (32, 16.85),
                'L1': (40.3, 8.5), 'C101': (31.21, 19.56)}.items():
    p = fs[ref].GetPosition()
    if abs(p.x / 1e6 - xy[0]) > .001 or abs(p.y / 1e6 - xy[1]) > .001:
        raise SystemExit(f'Unexpected placement: {ref}')
if list(b.GetTracks()):
    raise SystemExit('Expected an unrouted candidate')

def vec(p):
    return pcbnew.VECTOR2I(pcbnew.FromMM(p[0]), pcbnew.FromMM(p[1]))

def path(net, layer, width, points):
    for a, z in zip(points, points[1:]):
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(vec(a)); t.SetEnd(vec(z)); t.SetLayer(layer)
        t.SetWidth(pcbnew.FromMM(width)); t.SetNetCode(b.FindNet(net).GetNetCode())
        b.Add(t)

def vias(net, points, diameter=.8, drill=.4):
    for p in points:
        v = pcbnew.PCB_VIA(b)
        v.SetPosition(vec(p)); v.SetWidth(pcbnew.FromMM(diameter))
        v.SetDrill(pcbnew.FromMM(drill)); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        v.SetNetCode(b.FindNet(net).GetNetCode())
        v.SetBackTentingMode(pcbnew.TENTING_MODE_TENTED)
        v.SetFrontTentingMode(pcbnew.TENTING_MODE_TENTED)
        b.Add(v)

# These swaps are relative to pack_candidate.py's selected placement.
def swap(a, z):
    f, g = fs[a], fs[z]
    p, angle = f.GetPosition(), f.GetOrientationDegrees()
    f.SetOrientationDegrees(g.GetOrientationDegrees()); f.SetPosition(g.GetPosition())
    g.SetOrientationDegrees(angle); g.SetPosition(p)

if fs['D1'].GetPosition().x < pcbnew.FromMM(10):
    swap('D1', 'D2')
if fs['C104'].GetPosition().x < pcbnew.FromMM(44):
    swap('C104', 'C102')
fs['C105'].SetOrientationDegrees(90)
fs['C105'].SetPosition(vec((46.0,4.2)))
fs['R104'].SetOrientationDegrees(0)
fs['R104'].SetPosition(vec((34.94,12.65)))
F, B = pcbnew.F_Cu, pcbnew.B_Cu
# Battery positive: connector to connector; branch to Q2 sources.
for p in [[(5.55,9),(6.5,9),(7.4,9)], [(48.5,12),(49.45,12),(50.35,12)]]:
    vias('VBAT', p); path('VBAT', F, 1.5, p); path('VBAT', B, 1.5, p)
path('VBAT', B, 2, [(6.5,9),(10.5,9),(13.5,12),(49.45,12)])
vias('VBAT', [(30.7,1.5),(30.7,2.7),(30.7,3.9)])
path('VBAT', B, 1.5, [(30.7,1.5),(30.7,12)])
path('VBAT', F, .6, [(31.18,1.445),(31.18,3.985)])
for y in [1.5,2.7,3.9]:path('VBAT', F, .6, [(30.7,y),(31.18,y)])
# Low-side return stays on bottom copper until the connector and FET pads.
vias('GND', [(46.5,17.3),(46.5,18.2),(46.5,19.1),
             (5.55,12),(6.5,12),(7.4,12)])
path('GND', F, .6, [(48.045,17.19),(48.045,18.51)])
for y in [17.3,18.2]:path('GND', F, .8, [(46.5,y),(48.045,y)])
path('GND', F, 1.2, [(46.5,17.3),(46.5,19.1)])
path('GND', F, 1.5, [(5.55,12),(7.4,12)])
path('GND', B, 2, [(5.55,12),(7,13.45),(7,17),(9.1,19.1),(46.5,19.1)])
path('GND', B, 1.5, [(46.5,17.3),(46.5,19.1)])
# Motor return and brake drains.
vias('MOTOR_MINUS', [(50.2,17.7),(51.1,17.7),(50.2,18.6),(51.1,18.6),
                     (48.55,9),(49.45,9),(50.35,9),
                     (37,2.7),(37,3.7),(37,4.7)])
path('MOTOR_MINUS', F, 1.5, [(50.2,17.7),(51.1,17.7),(51.1,18.6),(50.2,18.6),(50.2,17.7)])
path('MOTOR_MINUS', B, 2, [(51.1,18.6),(52.3,18.6),(52.3,9),(49.45,9),(48.55,9)])
path('MOTOR_MINUS', F, 1.5, [(48.55,9),(50.35,9)])
path('MOTOR_MINUS', F, .6, [(36.645,1.445),(36.645,5.255)])
for y in [2.7,3.7,4.7]:path('MOTOR_MINUS', F, .6, [(36.645,y),(37,y)])
path('MOTOR_MINUS', B, 1.5, [(37,2.7),(37,4.7)])
path('MOTOR_MINUS', B, 2, [(37,3.7),(44.15,3.7),(49.45,9)])
# Complete the two connections the constrained trial router left open. This
# gate route is a connectivity experiment; its loop/return still needs review.
path('GND', F, .2, [(31.69,19.56),(31.69,18.2975),(32,17.9875)])
path('GATE_N', F, .2, [(43.775,2.665),(45.0,2.665),(45.0,.8),(44.95,.6)])
vias('GATE_N', [(44.95,.6),(47,4.5),(47.3,15.8),(48.045,20.2)], .6, .3)
path('GATE_N', B, .2, [(44.95,.6),(47,.6),(47,4.5)])
path('GATE_N', F, .2, [(47,4.5),(47.3,4.8),(47.3,15.8)])
path('GATE_N', B, .2, [(47.3,15.8),(48.045,16.545),(48.045,20.2)])
path('GATE_N', F, .2, [(48.045,20.2),(48.045,19.17)])
# Signal supplies cross the power buses on the opposite layer.
path('GND', F, .2, [(38.825,3.935),(40.1,3.935),(40.2,4.035),(40.2,6)])
vias('GND', [(40.2,6),(39.9,10.45),(39.9,15.2),(46.4,9.8)], .6, .3)
path('GND', B, .2, [(40.2,6),(40.2,10.45),(39.9,10.45)])
path('GND', F, .2, [(39.9,10.45),(39.9,15.2)])
path('GND', B, .2, [(39.9,15.2),(39.9,19.1)])
path('GND', F, .2, [(45.85,9.3875),(46.4,9.8)])
path('GND', B, .2, [(46.4,9.8),(46.4,10.4),(40.2,10.4)])
vias('MCU_3V3', [(43.775,.75),(42,2.1),(42,6),(43.3,6.5)], .6, .3)
path('MCU_3V3', F, .2, [(43.775,1.395),(43.775,.75)])
path('MCU_3V3', B, .2, [(43.775,.75),(42,2.1)])
path('MCU_3V3', F, .2, [(42,2.1),(42,6)])
path('MCU_3V3', B, .2, [(42,6),(43.3,6.5)])
path('MCU_3V3', F, .2, [(43.3,6.5),(43.95,7.1125)])
b.BuildConnectivity()
for track in b.GetTracks():
    track.SetLocked(True)
pcbnew.SaveBoard(str(args.board), b)
dsn = args.board.parent/'board.dsn'
print('DSN export:', pcbnew.ExportSpecctraDSN(b, str(dsn)))
# KiCad exports net clearance, but the router needs an additional margin to
# reproduce the separate 0.25 mm board-edge rule. Inset only its virtual border.
def inset(match):
    numbers = [float(n) for n in match.group(1).split()]
    adjusted = []
    for x, y in zip(numbers[::2], numbers[1::2]):
        adjusted.extend([150+x*54700/55000, -150+y*20700/21000])
    return '(boundary (path pcb 0 '+ ' '.join(f'{n:.5f}' for n in adjusted)+'))'
text = re.sub(r'\(boundary\s+\(path pcb 0\s+([^)]*)\)\s*\)', inset, dsn.read_text())
dsn.write_text(text)
