#!/usr/bin/env python3
"""Create a metadata-only PCB candidate; never overwrite the source board.

Use KiCad's Python interpreter and sexpdata on PYTHONPATH. A caller must inspect
the report and apply the candidate via KiCad MCP before final ERC/DRC checks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

import pcbnew
import sexpdata

FIELDS = {"MPN", "Manufacturer", "SelectionStatus", "Datasheet"}


def stripped(node):
    if not isinstance(node, list):
        return node
    return [stripped(x) for x in node if not (
        isinstance(x, list) and len(x) >= 2 and str(x[0]) == "property"
        and str(x[1]) in FIELDS)]


def invariant(path):
    return stripped(sexpdata.loads(path.read_text()))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("netlist", type=Path)
    p.add_argument("candidate", type=Path)
    p.add_argument("report", type=Path)
    p.add_argument("--references", nargs="+", required=True)
    a = p.parse_args()
    if a.source.resolve() == a.candidate.resolve():
        raise SystemExit("Refusing to overwrite the canonical source board")
    if ".cache" not in a.candidate.resolve().parts:
        raise SystemExit("Candidate output must be inside .cache")
    initial = invariant(a.source)
    before_hash = hashlib.sha256(a.source.read_bytes()).hexdigest()
    root = ET.parse(a.netlist).getroot()
    components = {c.attrib["ref"]: c for c in root.findall("./components/comp")}
    board = pcbnew.LoadBoard(str(a.source.resolve()))
    footprints = {f.GetReference(): f for f in board.GetFootprints()}
    changes = []
    for ref in a.references:
        if ref not in components or ref not in footprints:
            raise SystemExit(f"Reference {ref} missing from board or netlist")
        comp, fp = components[ref], footprints[ref]
        fields = {f.attrib["name"]: f.text or "" for f in comp.findall("./fields/field")}
        fields["Datasheet"] = comp.findtext("datasheet", "")
        if not fields.get("MPN"):
            raise SystemExit(f"Reference {ref} has no MPN in exported netlist")
        for name in sorted(FIELDS):
            if name not in fields:
                continue
            old = fp.GetFieldText(name) if fp.HasField(name) else ""
            new = fields[name]
            if old != new:
                fp.SetField(name, new)
                fp.GetField(name).SetVisible(False)
                changes.append({"reference": ref, "field": name, "old": old, "new": new})
    a.candidate.parent.mkdir(parents=True, exist_ok=True)
    # MCP save_board also persists project settings. A candidate without the
    # original .kicad_pro could cause MCP to write default rules at Save As.
    source_project = a.source.with_suffix(".kicad_pro")
    candidate_project = a.candidate.with_suffix(".kicad_pro")
    if not source_project.is_file():
        raise SystemExit("Source project settings are required; refusing an unguarded Save As")
    shutil.copy2(source_project, candidate_project)
    pcbnew.SaveBoard(str(a.candidate.resolve()), board)
    # Compare every S-expression outside the four named properties, including
    # pad/net names, item UUIDs, routes, vias, drawings and all placement data.
    same = initial == invariant(a.candidate)
    report = {"source": str(a.source), "source_sha256": before_hash,
              "candidate": str(a.candidate),
              "candidate_sha256": hashlib.sha256(a.candidate.read_bytes()).hexdigest(),
              "source_project_sha256": hashlib.sha256(source_project.read_bytes()).hexdigest(),
              "candidate_project_sha256": hashlib.sha256(candidate_project.read_bytes()).hexdigest(),
              "changed_fields": changes, "all_non_metadata_sexpressions_equal": same,
              "scope": "metadata candidate only; ERC/DRC and canonical MCP save remain required"}
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"changed_fields": len(changes),
                      "all_non_metadata_sexpressions_equal": same,
                      "report": str(a.report)}, ensure_ascii=False))
    if not same:
        raise SystemExit("Candidate changed non-metadata data; do not apply")


if __name__ == "__main__":
    main()
