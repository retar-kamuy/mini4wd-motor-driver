"""Prepare a quote-only PCBA handoff from a hash-matched preview and PCB.

Does not approve procurement, CAM rotation, DFM, or electrical performance.
Run with the Python that provides pcbnew. Never edits the design source.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import html
import json
import shutil
import zipfile
import pcbnew

ap = argparse.ArgumentParser()
ap.add_argument("preview", type=Path)
ap.add_argument("output", type=Path)
args = ap.parse_args()
root = Path(__file__).resolve().parents[2]
project = root / "hardware/kicad/mini4wd-motor-driver"
preview, out = args.preview.resolve(), args.output.resolve()
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source_rows = [line.split("  ", 1) for line in (preview / "source-sha256.txt").read_text().splitlines()]
for expected, name in source_rows:
    if digest(project / name) != expected:
        raise SystemExit(f"Source differs from preview: {name}")
for expected, name in [line.split("  ", 1) for line in (preview / "artifact-sha256.txt").read_text().splitlines()]:
    if digest(preview / name) != expected:
        raise SystemExit(f"Preview artifact differs: {name}")
b = pcbnew.LoadBoard(str(project / "mini4wd-motor-driver.kicad_pcb"))
fps = {f.GetReference(): f for f in b.GetFootprints()}
with (preview / "bom-candidates.csv").open(newline="") as stream:
    bom = list(csv.DictReader(stream))
with (preview / "cpl-front.csv").open(newline="") as stream:
    cpl = list(csv.DictReader(stream))
bomrefs = [ref for r in bom for ref in r["Reference"].split(",")]
cplrefs = [r["Ref"] for r in cpl]
assert len(bomrefs) == len(set(bomrefs)) == len(fps) == 38
assert len(cplrefs) == len(set(cplrefs)) == 38
assert set(bomrefs) == set(cplrefs) == set(fps)
for row in bom:
    assert int(row["Qty"]) == len(row["Reference"].split(","))
    assert row["MPN"] and row["Manufacturer"] and row["Datasheet"]
    for ref in row["Reference"].split(","):
        f = fps[ref]
        assert row["Value"] == f.GetValue()
        assert row["MPN"] == f.GetFieldText("MPN")
        assert row["Manufacturer"] == f.GetFieldText("Manufacturer")
for row in cpl:
    f = fps[row["Ref"]]
    assert abs(float(row["PosX"]) - f.GetPosition().x / 1e6) < 1e-6
    assert abs(float(row["PosY"]) + f.GetPosition().y / 1e6) < 1e-6
    d = (float(row["Rot"]) - f.GetOrientationDegrees()) % 360
    assert min(d, 360 - d) < 1e-6
    assert row["Side"] == "top" and f.GetLayer() == pcbnew.F_Cu
out.mkdir(parents=True, exist_ok=True)
(out / "assembly").mkdir(exist_ok=True)
(out / "checks").mkdir(exist_ok=True)
for name in ["gerber-preview.zip", "mini4wd-motor-driver.ipc", "schematic.pdf", "source-sha256.txt"]:
    shutil.copyfile(preview / name, out / name)
shutil.copyfile(preview / "bom-candidates.csv", out / "bom-per-board.csv")
shutil.copyfile(preview / "cpl-front.csv", out / "cpl-kicad-mm.csv")
shutil.copyfile(preview / "artifact-sha256.txt", out / "checks/preview-artifact-sha256.txt")

def write_csv(name, header, rows):
    with (out / name).open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)

write_csv("bom-turnkey.csv", ["Line#", "Qty", "Designator", "MPN", "Manufacturer", "Description", "Package", "Type", "Datasheet", "Notes"],
          [[i, r["Qty"], r["Reference"], r["MPN"], r["Manufacturer"], r["Value"], r["Footprint"], "SMD", r["Datasheet"], r["Notes"]]
           for i, r in enumerate(bom, 1)])
write_csv("cpl-top-mm.csv", ["Designator", "Mid X", "Mid Y", "Layer", "Rotation"],
          [[r["Ref"], r["PosX"], r["PosY"], "Top", f'{float(r["Rot"]) % 360:.6f}'] for r in cpl])
write_csv("procurement-response.csv", ["Designator", "MPN", "Manufacturer", "Qty/board", "Qty/2boards", "Qty/5boards", "Qty/10boards", "Supplier source", "Available qty", "MOQ", "Assembly loss qty", "Unit price/currency", "Lead time", "Assembly accepted", "Proposed substitute (approval required)", "Notes"],
          [[r["Reference"], r["MPN"], r["Manufacturer"], r["Qty"], *[int(r["Qty"]) * n for n in (2, 5, 10)], *[""] * 9] for r in bom])
padrows = []
for ref, f in sorted(fps.items()):
    for p in sorted(f.Pads(), key=lambda p: p.GetNumber()):
        padrows.append([ref, p.GetNumber(), p.GetNetname(), f'{p.GetPosition().x/1e6:.6f}', f'{-p.GetPosition().y/1e6:.6f}', "Top"])
write_csv("assembly/pads-mm.csv", ["Designator", "Pad", "Net", "X mm", "Y mm (same as CPL)", "Layer"], padrows)

# Independent cards preserve the global top view and make every pad readable.
# They draw actual PCB pad center/size/rotation, not manufacturer body geometry.
esc = html.escape
cards = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2960" viewBox="0 0 1600 2960">', '<rect width="1600" height="2960" fill="white"/>', '<g font-family="sans-serif" fill="#182333">', '<text x="20" y="28" font-size="20">PCBA pad orientation reference — global Top view, NOT a vendor rotation approval</text>', '<text x="20" y="51" font-size="13">Cards normalized in size. Pad numbers follow the PCB; see pads-mm.csv for exact X/Y/net. CPL Y = minus PCB Y.</text>']
for idx, (ref, f) in enumerate(sorted(fps.items())):
    x0, y0 = (idx % 4) * 400 + 10, (idx // 4) * 287 + 75
    cards.append(f'<rect x="{x0}" y="{y0}" width="380" height="273" rx="5" fill="#f5f8fa" stroke="#b8c4d0"/>')
    cards.append(f'<text x="{x0+10}" y="{y0+22}" font-size="18" font-weight="bold">{esc(ref)}  {f.GetOrientationDegrees()%360:g}°</text>')
    cards.append(f'<text x="{x0+10}" y="{y0+42}" font-size="12">{esc(f.GetFieldText("MPN"))}</text>')
    pads = list(f.Pads())
    coords = [(p, p.GetPosition().x / 1e6, p.GetPosition().y / 1e6, p.GetSize().x / 1e6, p.GetSize().y / 1e6) for p in pads]
    xmin = min(x-max(w,h)/2 for p,x,y,w,h in coords); xmax = max(x+max(w,h)/2 for p,x,y,w,h in coords)
    ymin = min(y-max(w,h)/2 for p,x,y,w,h in coords); ymax = max(y+max(w,h)/2 for p,x,y,w,h in coords)
    scale = min(325 / max(xmax-xmin, 0.1), 165 / max(ymax-ymin, 0.1), 50)
    for p,x,y,w,h in coords:
        px = x0+190+(x-(xmin+xmax)/2)*scale; py=y0+149+(y-(ymin+ymax)/2)*scale
        a = p.GetOrientationDegrees()
        color = '#f9c56c' if p.GetNumber()=='1' else '#c8d6e3'
        cards.append(f'<rect x="{px-w*scale/2:.3f}" y="{py-h*scale/2:.3f}" width="{w*scale:.3f}" height="{h*scale:.3f}" transform="rotate({-a:.3f} {px:.3f} {py:.3f})" fill="{color}" stroke="#456" stroke-width="1"/>')
        cards.append(f'<text x="{px:.3f}" y="{py+4:.3f}" text-anchor="middle" font-size="12">{esc(p.GetNumber())}</text>')
    cards.append(f'<text x="{x0+10}" y="{y0+258}" font-size="12">X={f.GetPosition().x/1e6:g} mm, CPL Y={-f.GetPosition().y/1e6:g} mm</text>')
cards.append('</g></svg>')
(out / "assembly/pad-orientation.svg").write_text('\n'.join(cards), encoding="utf-8")
q1 = fps['Q1']; q1vias=[]
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA) and any(p.GetNetname() == 'MOTOR_MINUS' and p.HitTest(t.GetPosition(), t.GetWidth(pcbnew.F_Cu)//2) for p in q1.Pads()):
        q1vias.append([t.GetPosition().x/1e6, -t.GetPosition().y/1e6, t.GetNetname(), t.GetWidth(pcbnew.F_Cu)/1e6, t.GetDrillValue()/1e6])
write_csv("assembly/q1-pad-vias-mm.csv", ['X mm','Y mm (same as CPL)','Net','Diameter mm','Drill mm'], q1vias)
assert len(q1vias) == 6
result = {"pcb_sha256": digest(project / 'mini4wd-motor-driver.kicad_pcb'), "source_files_checked":len(source_rows), "source_mismatches":0, "preview_artifacts_hash_checked":True, "bom_rows":len(bom), "bom_components":len(bomrefs), "cpl_components":len(cpl), "bom_cpl_pcb_references_equal":True, "bom_value_mpn_manufacturer_pcb_mismatches":0, "cpl_position_rotation_side_pcb_mismatches":0, "pad_rows":len(padrows), "q1_pad_vias":len(q1vias), "procurement_and_vendor_rotation":"UNCONFIRMED", "scope":"Quote package assembly and CAD consistency only; no new electrical/thermal approval"}
(out / 'checks/package-validation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
