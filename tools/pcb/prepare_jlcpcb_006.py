#!/usr/bin/env python3
"""Check a 006 KiCad design and export local JLCPCB review files."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "hardware/kicad/mini4wd-course-adaptive"
SCRIPTS = ROOT / "plugins/kicad-happy/skills"
COMMON_LAYERS = ["B.Cu", "F.Mask", "B.Mask", "F.SilkS", "B.SilkS", "F.Paste", "B.Paste", "Edge.Cuts"]


def run(*args, allowed=(0,)):
    result = subprocess.run(args, check=False, timeout=180)
    if result.returncode not in allowed:
        raise SystemExit(f"Command failed ({result.returncode}): {' '.join(map(str, args))}")
    return result.returncode


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def check_references(path, field, grouped=False):
    refs = []
    for row in read_csv(path):
        value = row[field]
        refs.extend(ref.strip() for ref in (value.split(",") if grouped else [value]))
    if not refs or "" in refs or len(refs) != len(set(refs)):
        raise SystemExit(f"Empty or duplicate designators in {path}")
    return set(refs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New directory for reports and files")
    parser.add_argument("--design", default="mini4wd-course-adaptive",
                        help="KiCad basename, optionally prefixed with a 006 subdirectory")
    parser.add_argument("--layers", choices=(2, 4), type=int, required=True)
    parser.add_argument("--pcba-review", action="store_true", help="Also generate BOM and placement files for review")
    parser.add_argument("--manual", action="append", default=[], metavar="REF",
                        help="Exclude one hand-installed reference from PCBA files, keeping it in the full BOM")
    args = parser.parse_args()

    if not re.fullmatch(r"(?:[a-zA-Z0-9_-]+/)*[a-zA-Z0-9_-]+", args.design):
        parser.error("design must be a relative path without extension")
    manual = set(args.manual)
    if manual and not args.pcba_review:
        parser.error("--manual requires --pcba-review")
    stem = PROJECT / args.design
    design_dir = stem.parent
    sources = {ext: stem.with_suffix(f".kicad_{ext}") for ext in ("pro", "sch", "pcb")}
    missing = [str(p) for p in sources.values() if not p.is_file()]
    if missing:
        raise SystemExit(f"KiCad source missing: {', '.join(missing)}")
    # Include local libraries and subsheets in the revision record.
    inputs = sorted({
        *sources.values(),
        *(p for p in design_dir.rglob("*") if p.is_file() and (
            p.suffix in {".kicad_sch", ".kicad_sym", ".kicad_mod", ".kicad_dru"}
            or p.name in {"fp-lib-table", "sym-lib-table"}
        ))
    })
    source_hashes = {str(p.relative_to(PROJECT)): digest(p) for p in inputs}
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    version = subprocess.check_output(["kicad-cli", "version"], text=True).strip()
    sch, pcb = sources["sch"], sources["pcb"]
    erc = run("kicad-cli", "sch", "erc", "--severity-all", "--exit-code-violations",
              "--output", out / "erc.json", "--format", "json", sch, allowed=(0, 5))
    drc = run("kicad-cli", "pcb", "drc", "--schematic-parity", "--severity-all",
              "--exit-code-violations", "--output", out / "drc.json", "--format", "json",
              pcb, allowed=(0, 5))
    if erc or drc:
        raise SystemExit(f"ERC/DRC requires resolution. Reports: {out}")

    # Read the board and check the export layer selection against the real stack.
    actual_layers = int(subprocess.check_output(
        ["/usr/bin/python3", "-c",
         "import pcbnew, sys; print(pcbnew.LoadBoard(sys.argv[1]).GetCopperLayerCount())",
         str(pcb)], text=True).strip())
    if actual_layers != args.layers:
        raise SystemExit(f"Board has {actual_layers} layers, requested {args.layers}")

    run("kicad-cli", "sch", "export", "netlist", "--format", "kicadxml",
        "--output", out / "schematic.xml", sch)
    run("/usr/bin/python3", ROOT / "tools/pcb/audit_connectivity.py",
        pcb, out / "schematic.xml", out / "connectivity.json")
    run("kicad-cli", "sch", "export", "pdf", "--output", out / "schematic.pdf", sch)

    cam = out / "cam"
    cam.mkdir()
    layers = ["F.Cu", *[f"In{i}.Cu" for i in range(1, args.layers - 1)], *COMMON_LAYERS]
    run("kicad-cli", "pcb", "export", "gerbers", "--layers", ",".join(layers),
        "--output", str(cam) + "/", pcb)
    run("kicad-cli", "pcb", "export", "drill", "--excellon-separate-th",
        "--output", str(cam) + "/", pcb)
    run("python3", SCRIPTS / "kicad/scripts/analyze_gerbers.py", cam,
        "--output", out / "gerber-analysis.json")
    findings = json.loads((out / "gerber-analysis.json").read_text())["findings"]
    serious = [item for item in findings if item.get("severity", "").lower() == "error"]
    if serious:
        raise SystemExit(f"Gerber analyzer reported errors. Report: {out / 'gerber-analysis.json'}")

    raw_bom = out / "bom-kicad.csv"
    run("kicad-cli", "sch", "export", "bom", "--exclude-dnp", "--ref-range-delimiter", "",
        "--fields", "Reference,Value,Footprint,MPN,Manufacturer,LCSC",
        "--labels", "Reference,Value,Footprint,MPN,Manufacturer,LCSC Part #",
        "--output", raw_bom, sch)
    all_refs = check_references(raw_bom, "Reference", grouped=True)

    if args.pcba_review:
        raw_pos = out / "positions-kicad-mm.csv"
        bom, pos = out / "jlc-bom-review.csv", out / "jlc-cpl-review.csv"
        assembly_bom = raw_bom
        if manual:
            if manual - all_refs:
                raise SystemExit(f"Manual assembly reference missing from BOM: {sorted(manual - all_refs)}")
            assembly_bom = out / "bom-pcba-kicad.csv"
            original_rows = read_csv(raw_bom)
            manual_rows, assembly_rows = [], []
            for row in original_rows:
                refs = {ref.strip() for ref in row["Reference"].split(",")}
                for group, selected in ((manual_rows, refs & manual), (assembly_rows, refs - manual)):
                    if selected:
                        group.append({**row, "Reference": ",".join(sorted(selected))})
            write_csv(assembly_bom, assembly_rows, original_rows[0].keys())
            write_csv(out / "bom-manual.csv", manual_rows, original_rows[0].keys())
        run("kicad-cli", "pcb", "export", "pos", "--format", "csv", "--units", "mm",
            "--side", "both", "--exclude-dnp", "--output", raw_pos, pcb)
        translator = SCRIPTS / "bom/scripts/translate_bom_pnp.py"
        run("python3", translator, "bom", assembly_bom, "-o", bom)
        run("python3", translator, "pnp", raw_pos, "-o", pos, "--units", "mm", "--bom", bom)
        bom_refs = check_references(bom, "Designator", grouped=True)
        pos_refs = check_references(pos, "Designator")
        if bom_refs != all_refs - manual or bom_refs != pos_refs:
            raise SystemExit(f"BOM/CPL disagreement: BOM-only {sorted(bom_refs-pos_refs)}, CPL-only {sorted(pos_refs-bom_refs)}")

    if any(digest(PROJECT / name) != expected for name, expected in source_hashes.items()):
        raise SystemExit("Source changed during export")
    archive = out / "jlc-gerbers-review.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as package:
        for p in sorted(cam.iterdir()):
            if p.is_file() and p.suffix.lower() != ".gbrjob":
                package.write(p, p.name)
    artifacts = {str(p.relative_to(out)): digest(p) for p in sorted(out.rglob("*")) if p.is_file()}
    (out / "manifest.json").write_text(json.dumps({
        "design": args.design, "kicad_version": version, "copper_layers": actual_layers,
        "status": "local_review", "erc_drc_and_schematic_parity": "pass",
        "gerber_analyzer_findings": len(findings), "pcba_review": args.pcba_review,
        "manual_assembly_refs": sorted(manual),
        "source_sha256": source_hashes, "artifact_sha256": artifacts,
    }, indent=2) + "\n")
    print(f"Local review package: {archive}")


if __name__ == "__main__":
    main()
