"""Compare KiCad XML nets to every PCB pad and record CAD geometry facts.

Does not substitute for DRC, datasheet, current-capacity or manufacturing checks.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import xml.etree.ElementTree as ET
import pcbnew

ap = argparse.ArgumentParser()
ap.add_argument('board', type=Path)
ap.add_argument('netlist', type=Path)
ap.add_argument('report', type=Path)
args = ap.parse_args()
b = pcbnew.LoadBoard(str(args.board))
expected = {}
for net in ET.parse(args.netlist).findall('./nets/net'):
    for node in net.findall('node'):
        expected[node.get('ref'), node.get('pin')] = net.get('name')
mismatches, compared, seen = [], 0, set()
for f in b.GetFootprints():
    for p in f.Pads():
        key = f.GetReference(), p.GetNumber()
        if key not in expected and not p.GetNetname():
            continue
        compared += 1
        seen.add(key)
        if expected.get(key) != p.GetNetname():
            mismatches.append({'reference': key[0], 'pad': key[1],
                               'schematic_net': expected.get(key), 'pcb_net': p.GetNetname()})
for key in expected.keys() - seen:
    mismatches.append({'reference': key[0], 'pad': key[1], 'missing_from_pcb': True})
vias = [t for t in b.GetTracks() if isinstance(t, pcbnew.PCB_VIA)]
tracks = [t for t in b.GetTracks() if not isinstance(t, pcbnew.PCB_VIA)]
points = [p for g in b.GetDrawings() if g.GetLayer() == pcbnew.Edge_Cuts
          for p in (g.GetStart(), g.GetEnd())]
power = {}
for net in ['VBAT', 'GND', 'MOTOR_MINUS', 'SW_BOOST', 'GATE_N', 'GATE_P']:
    by_width = collections.defaultdict(float)
    for t in tracks:
        if t.GetNetname() == net:
            by_width[str(round(t.GetWidth()/1e6, 4))] += t.GetLength()/1e6
    power[net] = {w: round(length, 4) for w, length in by_width.items()}
report = {
    'kicad_version': pcbnew.Version(),
    'pcb_sha256': hashlib.sha256(args.board.read_bytes()).hexdigest(),
    'xml_sha256': hashlib.sha256(args.netlist.read_bytes()).hexdigest(),
    'compared_pads': compared, 'mismatches': mismatches,
    'footprint_count': len(list(b.GetFootprints())),
    'all_footprints_front': all(f.GetLayer() == pcbnew.F_Cu for f in b.GetFootprints()),
    'board_thickness_mm': b.GetDesignSettings().GetBoardThickness()/1e6,
    'copper_layer_count': b.GetCopperLayerCount(),
    'outline_centerline_extent_mm': [
        (max(p.x for p in points)-min(p.x for p in points))/1e6,
        (max(p.y for p in points)-min(p.y for p in points))/1e6],
    'via_count': len(vias),
    'back_tented_vias': sum(v.IsTented(pcbnew.B_Mask) for v in vias),
    'via_diameter_drill_counts_mm': dict(collections.Counter(
        f'{v.GetWidth(pcbnew.F_Cu)/1e6:g}/{v.GetDrillValue()/1e6:g}' for v in vias)),
    'track_count': len(tracks),
    'track_length_mm_by_net_and_width_mm': power,
}
args.report.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
raise SystemExit(bool(mismatches))
