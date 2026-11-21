#!/usr/bin/env python3
"""Read-only Spec 005 release evidence inventory; never grants manufacturing approval."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / 'hardware/kicad/mini4wd-brushless-motor'
SPEC = ROOT / 'specs/005-mini4wd-brushless-motor'


def record(path):
    if not path.is_file():
        return {'path': str(path.relative_to(ROOT)), 'status': 'missing'}
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'status': 'present' if data else 'empty',
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    required = [BOARD / ('mini4wd-brushless-motor' + ext) for ext in ('.kicad_sch', '.kicad_pcb', '.kicad_pro')]
    required += [SPEC / f for f in ('manufacturer-evidence.md', 'controller-compatibility.md',
                                    'mechanical-envelope.md', 'power-budget.md', 'validation-log.md')]
    required += [BOARD / 'design-review.md']
    checks = ['erc', 'drc', 'schematic-pcb-parity', 'connectivity', 'datasheet-pin-pad',
              'spice', 'emc', 'thermal', 'mechanical-fit', 'prototype-test', 'supplier-dfm']
    inventory = [record(p) for p in required]
    evidence = {name: [record(p) for p in sorted((BOARD / 'validation').glob(name + '*')) if p.is_file()]
                for name in checks}
    packages = [record(p) for p in sorted((BOARD / 'manufacturing').glob('rev-*/*')) if p.is_file()]
    result = {'scope': 'artifact inventory only; presence/hash does not validate contents',
              'manufacturing_approval': 'NOT_GRANTED_BY_THIS_TOOL', 'artifacts': inventory,
              'check_evidence': evidence, 'revision_package_files': packages,
              'missing_artifact_count': sum(r['status'] != 'present' for r in inventory),
              'checks_without_evidence': [name for name, files in evidence.items() if not files],
              'open_design_inputs': ['XSPEED sensor pinout/type/levels', 'motor voltage/current/R-L/pole pairs',
                                     'motor geometry', 'selected supply topology and ratings',
                                     'XIAO Sense schematic/core IMU bus mismatch'],
              'release_rule': 'All native reports and raw source/datasheet checks must be reviewed for the same revision; user approval and supplier DFM remain separate.'}
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    else:
        print(output, end='')
    return 2 if result['missing_artifact_count'] or result['checks_without_evidence'] or not packages else 0


if __name__ == '__main__':
    raise SystemExit(main())
