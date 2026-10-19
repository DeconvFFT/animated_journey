#!/usr/bin/env bash
# svg_roundtrip.sh: do the ids and data-* attributes of a rig survive a touching tool? (WP-06, VectorCraft hand-off stand-in)
#
#   bash pipeline/roundtrip/svg_roundtrip.sh [--out DIR] [--inkscape CMD] [--json FILE] [--finding FILE]
#
# WHAT IT DOES (it prints each step before it runs it)
#   1  generates the synthetic rig (svg_rig.py gen)                                  -> DIR/rig.svg
#   2  pushes it through Inkscape's plain-SVG export, the stand-in "touching tool"      -> DIR/rig.plain.svg
#      (the documented fallback in playbooks/craft-visual.md; VectorCraft itself is WP-10)
#   3  runs the reused research/craft-visual-fixtures/check_ids.py on rig versus plain  -> the clean pass-through: gate exit 0
#   4  plants three defects in a copy of the Inkscape output and checks each one:        -> gate exit 1 each, with a named reason
#        ids_stripped    ids removed the way default svgo cleanupIds removes them        reason ids_lost
#        kind_changed    circle disc-a turned into an ellipse (same id, same data-*)     reason element_kind_changed
#        pivot_dropped   data-pivot removed everywhere                                   reason data_attr_changed
#   5  two real touch-ups through Inkscape (a child moved, a group moved) and Inkscape's own SVG format: gate exit 0 expected
#   6  writes the finding: what Inkscape did to every data-* attribute, id, viewBox and namespace  -> FILE (default DIR/inkscape_finding.json)
#
# THE GATE. check_ids.py is run unchanged (python3 -I). It exits 1 for lost ids or changed data-*, but it only PRINTS "element kind changed"
# (the exit code ignores it), so a pure kind change has raw_exit 0 there. svg_rig.py gate reads that line and exits 1 for it too; both numbers are
# printed (raw_exit, gate_exit). This is a finding about check_ids.py, recorded in the WP-06 report.
#
# Needs: bash, python3, inkscape (1.2.2 here). Inkscape runs with a throw-away profile folder inside DIR, removed at the end, so nothing is written
# to your Inkscape settings. Its harmless GtkRecentManager warning is hidden (research/craft-visual.md R5). It touches no network and no file outside DIR
# and the --json/--finding files. On Windows the same commands run with inkscape.com (playbooks/craft-visual.md); this script is Linux-only, UNVERIFIED on Windows.
#
# EXIT CODES (build plan 4.3)  0 every expectation held   1 an expectation failed   2 bad usage   3 a tool is missing (inkscape, python3, check_ids.py)
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HERE="$ROOT/pipeline/roundtrip"
CHECK_IDS="$ROOT/research/craft-visual-fixtures/check_ids.py"
OUT="$ROOT/renders/wp06/svg"; INK="inkscape"; JSON=""; FINDING=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift;;
    --inkscape) INK="$2"; shift;;
    --json) JSON="$2"; shift;;
    --finding) FINDING="$2"; shift;;
    *) echo "usage: svg_roundtrip.sh [--out DIR] [--inkscape CMD] [--json FILE] [--finding FILE]" >&2; exit 2;;
  esac
  shift
done
[ -n "$FINDING" ] || FINDING="$OUT/inkscape_finding.json"
command -v python3 >/dev/null 2>&1 || { echo "svg_roundtrip: python3 not found" >&2; exit 3; }
command -v "$INK" >/dev/null 2>&1 || { echo "svg_roundtrip: Inkscape not found (command: $INK)" >&2; exit 3; }
[ -f "$CHECK_IDS" ] || { echo "svg_roundtrip: research/craft-visual-fixtures/check_ids.py not found" >&2; exit 3; }
PY=(python3 -I -B)
mkdir -p "$OUT" || exit 3
export INKSCAPE_PROFILE_DIR="$OUT/_inkscape_profile"
mkdir -p "$INKSCAPE_PROFILE_DIR"
trap 'rm -rf "$INKSCAPE_PROFILE_DIR"' EXIT
LOG="$OUT/gate_lines.txt"; : > "$LOG"
INKVER="$("$INK" --version 2>/dev/null | head -n 1)"
REL="$OUT"; case "$OUT" in "$ROOT"/*) REL="${OUT#"$ROOT"/}";; esac
echo "svg_roundtrip: output folder $REL, touching tool: $INKVER"

ink() {   # Inkscape with its harmless GtkRecentManager warning hidden; every other message is passed on
  local rc
  "$INK" "$@" 2> "$OUT/_inkscape.err"; rc=$?
  grep -v -e GtkRecentManager -e '^[[:space:]]*$' "$OUT/_inkscape.err" >&2; rm -f "$OUT/_inkscape.err"
  return $rc
}

echo "[1/6] generating the synthetic rig (svg_rig.py gen) ..."
"${PY[@]}" "$HERE/svg_rig.py" gen "$OUT/rig.svg" || exit 1
echo "[2/6] Inkscape plain-SVG export, the stand-in touching tool ..."
ink "$OUT/rig.svg" --export-plain-svg --export-filename="$OUT/rig.plain.svg" || { echo "svg_roundtrip: Inkscape export failed" >&2; exit 3; }
[ -s "$OUT/rig.plain.svg" ] || { echo "svg_roundtrip: Inkscape wrote no file" >&2; exit 3; }
echo "      ok ($(wc -c < "$OUT/rig.plain.svg") bytes)"

FAILS=0
expect() {   # label want_exit rig touched
  local label="$1" want="$2" line rc
  line="$("${PY[@]}" "$HERE/svg_rig.py" gate "$3" "$4" --check-ids "$CHECK_IDS" --label "$label")"; rc=$?
  printf '%s\n' "$line" >> "$LOG"
  if [ "$rc" = 3 ]; then echo "svg_roundtrip: check_ids.py could not be used ($line)" >&2; exit 3; fi
  if [ "$rc" = "$want" ]; then echo "PASS svg.$label  gate_exit=$rc (wanted $want)  ${line#*reasons=}"
  else echo "FAIL svg.$label  gate_exit=$rc (wanted $want)  $line"; FAILS=$((FAILS + 1)); fi
}

echo "[3/6] check_ids.py (reused unchanged): clean pass-through, rig versus Inkscape plain-SVG ..."
expect clean_passthrough 0 "$OUT/rig.svg" "$OUT/rig.plain.svg"
echo "[4/6] planting three defects in a copy of the Inkscape output ..."
for kind in ids_stripped kind_changed pivot_dropped; do
  "${PY[@]}" "$HERE/svg_rig.py" plant "$kind" "$OUT/rig.plain.svg" "$OUT/rig.plain.$kind.svg" | sed 's/^/      /' || exit 1
  expect "planted_$kind" 1 "$OUT/rig.svg" "$OUT/rig.plain.$kind.svg"
done
echo "[5/6] two real touch-ups through Inkscape (move a child, move a group) and Inkscape's own SVG format ..."
ink "$OUT/rig.svg" --actions="select-by-id:disc-b;transform-translate:12,7;export-filename:$OUT/rig.touch_child.svg;export-plain-svg;export-do"
ink "$OUT/rig.svg" --actions="select-by-id:orbit;transform-translate:12,7;export-filename:$OUT/rig.touch_group.svg;export-plain-svg;export-do"
ink "$OUT/rig.svg" --export-type=svg --export-filename="$OUT/rig.inkscape.svg"
for f in touch_child touch_group inkscape; do [ -s "$OUT/rig.$f.svg" ] || { echo "svg_roundtrip: Inkscape wrote no rig.$f.svg" >&2; exit 3; }; done
expect touch_child_moved 0 "$OUT/rig.svg" "$OUT/rig.touch_child.svg"
expect touch_group_moved 0 "$OUT/rig.svg" "$OUT/rig.touch_group.svg"
expect inkscape_svg_format 0 "$OUT/rig.svg" "$OUT/rig.inkscape.svg"
echo "[6/6] writing the Inkscape finding (data-* attributes, ids, viewBox, namespaces) ..."
"${PY[@]}" "$HERE/svg_rig.py" finding "$OUT/rig.svg" "$OUT/rig.plain.svg" --extra "inkscape_svg_format=$OUT/rig.inkscape.svg" \
  --extra "touch_child_moved=$OUT/rig.touch_child.svg" --extra "touch_group_moved=$OUT/rig.touch_group.svg" \
  --inkscape-version "$INKVER" --json "$FINDING" | sed 's/^/      /'
if [ -n "$JSON" ]; then
  "${PY[@]}" - "$LOG" "$JSON" "$FAILS" <<'PY'
import json, re, sys
rows = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.search(r"GATE (\S+): raw_exit=(\d+) gate_exit=(\d+) authored=(\d+) lost=(\S+) kind_changed=(\S+) data_changed=(\S+) reasons=(\S+)", line)
    if m:
        rows.append({"label": m.group(1), "raw_exit": int(m.group(2)), "gate_exit": int(m.group(3)), "authored": int(m.group(4)),
                     "lost": m.group(5), "kind_changed": m.group(6), "data_changed": m.group(7), "reasons": m.group(8)})
json.dump({"schema": "lj-svg-roundtrip/1", "results": rows, "failures": int(sys.argv[3])}, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
fi
echo "files written: the .svg files and gate_lines.txt in the output folder, the finding JSON${JSON:+, and the --json file}; the throw-away Inkscape profile is removed"
if [ "$FAILS" = 0 ]; then echo "RESULT svg_roundtrip: all expectations held (clean pass-through 0; three planted defects 1 each; touch-ups 0)"; exit 0
else echo "RESULT svg_roundtrip: $FAILS expectation(s) failed"; exit 1; fi
