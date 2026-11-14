"""Import a nonempty SES into a trial while retaining every locked backbone item."""
from pathlib import Path
import argparse
import collections
import json
import pcbnew

ap = argparse.ArgumentParser()
ap.add_argument('board', type=Path)
ap.add_argument('session', type=Path)
args = ap.parse_args()
if '.cache/routing/' not in str(args.board):
    raise SystemExit('Trial importer accepts only .cache/routing/ boards')
if not args.session.exists() or args.session.stat().st_size == 0:
    raise SystemExit('Missing or empty SES; board was not modified')
original = pcbnew.LoadBoard(str(args.board))
b = pcbnew.LoadBoard(str(args.board))
if not pcbnew.ImportSpecctraSES(b, str(args.session)):
    raise SystemExit('SES import failed; board was not modified')

def key(t):
    if isinstance(t, pcbnew.PCB_VIA):
        return ('via', t.GetNetname(), t.GetPosition().x, t.GetPosition().y,
                t.GetWidth(pcbnew.F_Cu), t.GetDrillValue())
    ends = sorted([(t.GetStart().x, t.GetStart().y), (t.GetEnd().x, t.GetEnd().y)])
    return ('track', t.GetNetname(), t.GetLayer(), t.GetWidth(), *ends)

present = {key(t) for t in b.GetTracks()}
retained = 0
for t in original.GetTracks():
    if t.IsLocked() and key(t) not in present:
        item = t.Duplicate()
        item.SetNetCode(b.FindNet(t.GetNetname()).GetNetCode())
        b.Add(item)
        retained += 1
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA):
        t.SetBackTentingMode(pcbnew.TENTING_MODE_TENTED)
b.BuildConnectivity()
pcbnew.SaveBoard(str(args.board), b)
present = {key(t) for t in b.GetTracks()}
report = {
    'restored_locked_items': retained,
    'locked_items': sum(t.IsLocked() for t in b.GetTracks()),
    'track_width_counts_mm': dict(collections.Counter(
        str(round(t.GetWidth()/1e6, 4)) for t in b.GetTracks()
        if not isinstance(t, pcbnew.PCB_VIA))),
    'via_count': sum(isinstance(t, pcbnew.PCB_VIA) for t in b.GetTracks()),
    'all_backbone_geometry_present': all(
        key(t) in present
        for t in original.GetTracks() if t.IsLocked()),
}
(args.board.parent/'route-import.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
