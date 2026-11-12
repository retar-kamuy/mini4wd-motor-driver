#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(dirname -- "$script_dir")
board="$project_dir/mini4wd-motor-driver.kicad_pcb"
output_dir=${1:-"$script_dir/gerber"}
archive="${output_dir%/}-preview.zip"

if [ -e "$archive" ]; then
    printf 'Archive already exists: %s\nChoose a different output directory.\n' "$archive" >&2
    exit 1
fi
mkdir -p "$output_dir"
if [ -n "$(find "$output_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
    printf 'Output directory is not empty: %s\nChoose an empty output directory.\n' "$output_dir" >&2
    exit 1
fi

report="$output_dir/drc-report.rpt"
LC_ALL=C kicad-cli pcb drc --exit-code-violations --severity-all \
    --all-track-errors --refill-zones --schematic-parity \
    --output "$report" "$board"
if ! grep -A 1 '^\*\* Ignored checks \*\*' "$report" | grep -q '    - None'; then
    printf 'DRC checks are disabled; see %s\n' "$report" >&2
    exit 1
fi

LC_ALL=C kicad-cli pcb export gerbers --check-zones \
    --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,Edge.Cuts \
    --output "$output_dir/" "$board"
LC_ALL=C kicad-cli pcb export drill --format excellon --excellon-units mm \
    --drill-origin absolute --output "$output_dir/" "$board"

python3 - "$output_dir" "$archive" <<'PY'
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile

directory, archive = map(Path, sys.argv[1:])
suffixes = {'.gtl', '.gbl', '.gts', '.gbs', '.gto', '.gbo', '.gtp', '.gm1', '.drl'}
files = sorted(p for p in directory.iterdir() if p.suffix.lower() in suffixes)
found = {p.suffix.lower() for p in files}
if found != suffixes:
    raise SystemExit(f'Missing expected output types: {sorted(suffixes - found)}')
with ZipFile(archive, 'x', ZIP_DEFLATED) as bundle:
    for path in files:
        bundle.write(path, path.name)
PY

(cd "$project_dir" && sha256sum mini4wd-motor-driver.kicad_pcb \
    mini4wd-motor-driver.kicad_sch mini4wd-motor-driver.kicad_pro) \
    > "$output_dir/source-sha256.txt"
printf 'Generated preview: %s\n' "$archive"
