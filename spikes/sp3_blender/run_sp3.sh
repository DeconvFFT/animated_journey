#!/usr/bin/env bash
# run_sp3.sh: SP3, Blender (the bpy module) for hero shots: timing a NEUTRAL stand-in scene (build plan WP-10 item 2). Prepared 19 Oct 2026; FIRST REAL RUN Tue 20 Oct 2026:
#   all four timings within 2x the table (0.81x to 0.86x), see build/reports/w2-sp3.md. That run found the cleanup defect fixed in run_inner (test: spikes/sp3_blender/test_cleanup.sh).
#
#   bash spikes/sp3_blender/run_sp3.sh --check     the entry conditions and the numbers: df, the bpy wheel size (PyPI), the Blender tarball size (HEAD request), Python, the reused
#                                                   research scripts (py_compile). Prints "NOT RUN: needs >= 3.5 GB free" and exits 3 on a volume with less than 3,500 MB free;
#                                                   prints READY and exits 0 when the entry condition holds. Downloads nothing; writes nothing.
#   bash spikes/sp3_blender/run_sp3.sh --run       only when --check says READY: ONE disk stage (lj_with_disk 3100) that makes a venv, installs bpy==5.2.2 (a 402 MB wheel),
#                                                   times the stand-in kitchen scene at a few sample counts under lj_bench, writes the RESULT lines to build/evidence/wp10/sp3_results.txt
#                                                   and deletes the venv. SP3_DRYRUN=1 prints what it would do and does none of it.
#   bash spikes/sp3_blender/run_sp3.sh --help
# WHY IT WAS NOT RUN ON 19 OCT (historical; disk was freed on 20 Oct and the real peak was 1,408 MB, not 3,100). The container had about 700 MB free (it is shared and shrinking); the wheel is 402 MB, the venv about 1 GB, and the plan wants Avail minus planned at least 400 MB.
# The entry figure is 3,500 MB = planned 3,100 MB (wheel, pip's temporary copy of it, the venv, a margin for the first Cycles kernel build and the outputs) + the 400 MB floor.
# SP3 runs in week 3 either on the maker's PC (playbooks/toolchain.md Exercise 5, Blender parallax timed with the Claude app closed) or here after at least 3.5 GB is free, and only on a
# NEUTRAL stand-in scene with no photograph (S3's own rule). The pass mark, one real hero frame within 2x the table, cannot be judged before the real kitchen exists (G1).
# REUSED, NOT COPIED: research/production-scale-fixtures/followup2-s3-kitchen-standin.py (the scene: primitives only, no photographs, no family imagery) and, as the record of the sweep, followup2-s3-run-sweep.sh,
# whose first lines hold a path of an earlier session and which is therefore NOT executed; this script runs the same configurations itself. Its earlier numbers are in followup2-s3-container-results.txt.
# EXIT CODES (build plan 4.3)  0 READY (--check) or the run finished   1 a measurement step failed   2 bad usage   3 NOT RUN: the entry condition does not hold, or an environment problem
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
SELF="${BASH_SOURCE[0]}"
SP="$(cd "$(dirname "$SELF")" && pwd)"
ROOT="$(cd "$SP/../.." && pwd)"
SCENE="$ROOT/research/production-scale-fixtures/followup2-s3-kitchen-standin.py"
SWEEP="$ROOT/research/production-scale-fixtures/followup2-s3-run-sweep.sh"
RESULTS="$ROOT/research/production-scale-fixtures/followup2-s3-container-results.txt"
EVID="${LJ_SP3_EVIDENCE:-$ROOT/build/evidence/wp10}"
ENTRY_MB="${SP3_ENTRY_MB:-3500}"; PLANNED_MB=3100
WHEEL_RECORDED=401697653; BLENDER_RECORDED=383295504   # PyPI bpy 5.2.2 cp313 manylinux_2_28 x86_64 and blender-5.2.2-linux-x64.tar.xz (playbooks/toolchain.md [102][103]), 18 Oct 2026
# shellcheck disable=SC1091
. "$ROOT/scripts/lj_guard.sh"
say() { printf '%s\n' "$*"; }
die() { printf 'run_sp3: %s\n' "$*" >&2; exit "${2:-2}"; }
commas() { printf '%s\n' "$1" | sed -e ':a' -e 's/\([0-9]\)\([0-9]\{3\}\)\($\|,\)/\1,\2\3/' -e 'ta'; }

wheel_size() {  # prints "BYTES|source"
  local j n
  j="$(curl -sS --max-time 20 https://pypi.org/pypi/bpy/5.2.2/json 2>/dev/null)" || j=""
  n="$(printf '%s' "$j" | python3 -I -c "
import json, sys
try:
    d = json.load(sys.stdin)
    for u in d['urls']:
        if u['filename'].endswith('cp313-cp313-manylinux_2_28_x86_64.whl'):
            print(u['size']); break
except Exception:
    pass" 2>/dev/null)"
  if [[ "$n" =~ ^[0-9]+$ ]]; then echo "$n|read from PyPI just now"; else echo "$WHEEL_RECORDED|recorded 18 Oct 2026 (PyPI was not reachable)"; fi
}
blender_size() {  # HEAD request
  local n
  n="$(curl -sS -I -L --max-time 20 https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz 2>/dev/null | tr -d '\r' | awk 'tolower($1)=="content-length:"{v=$2} END{print v}')"
  if [[ "$n" =~ ^[0-9]+$ ]]; then echo "$n|read by HEAD request just now"; else echo "$BLENDER_RECORDED|recorded 18 Oct 2026 (the HEAD request failed)"; fi
}

do_check() {
  local avail w b wb bb py pyv ok_scene="MISSING" ok_sweep="MISSING" cf
  avail="$(lj_df_avail_mb)"; [[ "$avail" =~ ^[0-9]+$ ]] || { say "cannot read free disk space (df gave no number)"; return 3; }
  w="$(wheel_size)"; b="$(blender_size)"; wb="${w%%|*}"; bb="${b%%|*}"
  py="$(command -v python3)"; pyv="$(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null)"
  mkdir -p "${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}"
  cf="$(mktemp "${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}/sp3-cfile.XXXXXX")"
  [[ -f "$SCENE" ]] && python3 -c "import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)" "$SCENE" "$cf" 2>/dev/null && ok_scene="py_compile ok"
  [[ -f "$SWEEP" ]] && bash -n "$SWEEP" 2>/dev/null && ok_sweep="bash -n ok (referenced, not executed: it holds a path of an earlier session)"
  rm -f "$cf"
  say "run_sp3.sh --check    (SP3: Blender hero-shot timing on a neutral stand-in scene; prepared, NOT run; nothing is downloaded or written)"
  say ""
  say "Entry conditions"
  say "  free disk          Avail ${avail} MB now; needed at least ${ENTRY_MB} MB (planned ${PLANNED_MB} MB + the 400 MB floor of scripts/lj_guard.sh)"
  say "  bpy wheel          $(commas "$wb") bytes ($((wb / 1048576)) MiB), cp313 manylinux_2_28 x86_64, ${w#*|}; the venv it makes is about 1 GB on disk (R9/M14)"
  say "  Blender tarball    $(commas "$bb") bytes ($((bb / 1048576)) MiB), blender-5.2.2-linux-x64.tar.xz, ${b#*|}; NOT used by this script (bpy is the route); listed for the PC route"
  say "  python             ${pyv:-none} at ${py:-none} (the wheel is cp313 only, so 3.13 is required)"
  say "  reused scene       research/production-scale-fixtures/followup2-s3-kitchen-standin.py: ${ok_scene}; primitives only, no photograph, no family imagery"
  say "  reused sweep       research/production-scale-fixtures/followup2-s3-run-sweep.sh: ${ok_sweep}"
  say "  earlier numbers    followup2-s3-container-results.txt (stand-in, 1080p, Cycles CPU, 4 vCPU): 64 samples with denoise 110-115 s, 128 without 192-232 s, 24 with denoise 51-59 s"
  say "  pass mark          one real hero frame within 2x the table: cannot be judged before the real kitchen exists (G1); this run times the stand-in only"
  say ""
  if (( avail >= ENTRY_MB )) && [[ "$ok_scene" == "py_compile ok" ]] && [[ "$pyv" == 3.13.* ]]; then
    say "READY: Avail ${avail} MB is at least ${ENTRY_MB} MB. Start it with: bash spikes/sp3_blender/run_sp3.sh --run"
    return 0
  fi
  if (( avail < ENTRY_MB )); then
    say "NOT RUN: needs >= 3.5 GB free (Avail ${avail} MB; short by $((ENTRY_MB - avail)) MB). Justified deferral: SP3 runs in week 3 on the maker's PC (toolchain Exercise 5) or here once 3.5 GB is free."
  else
    say "NOT RUN: an entry condition other than disk fails (python 3.13 or the reused scene); see the lines above."
  fi
  return 3
}

run_inner() {
  local PYV="" cfg out="$ROOT/build/evidence/wp10/sp3_results.txt"
  # S is deliberately NOT local: an EXIT trap runs after this function has returned, when a local S is gone and, under set -u,
  # "S: unbound variable" stopped the first real run (20 Oct 2026) from deleting the venv. The trap text also carries the value itself.
  S="${LJ_SCRATCH:-$(dirname "$ROOT")/build-scratch}/sp3"
  trap 'rm -rf -- "${S:-/nonexistent-sp3-scratch}"' EXIT
  rm -rf -- "$S"; mkdir -p "$S" "$EVID" || die "cannot create the scratch folder" 3
  say "[1/5] python3 -m venv <scratch>/sp3/venv"
  python3 -m venv "$S/venv" || die "venv failed" 3
  say "[2/5] pip install --no-cache-dir bpy==5.2.2   (a 402 MB wheel; no pip cache is written)"
  "$S/venv/bin/python" -m pip install --no-cache-dir --disable-pip-version-check -q bpy==5.2.2 || die "pip install bpy failed" 3
  PYV="$("$S/venv/bin/python" -c 'import bpy; print(bpy.app.version_string)' 2>/dev/null)"
  say "[3/5] bpy imports: Blender ${PYV:-unknown}"
  [[ "$PYV" == 5.2.* ]] || die "bpy did not import as Blender 5.2.x" 1
  say "[4/5] the stand-in kitchen at 1920x1080 (fresh process per line, each under lj_bench; samples denoise adaptive)"
  { echo "SP3 run, neutral stand-in scene (primitives only), Blender ${PYV}, Cycles CPU, $(nproc) vCPU, no GPU; $(date -u +%Y-%m-%d)"; } > "$out"
  for cfg in "8 0 0" "64 0 0" "64 1 0" "128 1 0"; do
    # shellcheck disable=SC2086
    set -- $cfg
    lj_bench "$S/venv/bin/python" "$SCENE" -- "$S/out" 1920 1080 "$1" "$2" "$3" 2>/dev/null | grep RESULT | tee -a "$out"
  done
  say "[5/5] cleanup: the venv and the renders are deleted; results are in ${out#"$ROOT"/}"
}

do_run() {
  do_check; local rc=$?
  (( rc != 0 )) && { say "Nothing was started and nothing was forced."; return 3; }
  if [[ "${SP3_DRYRUN:-}" == 1 ]]; then
    say "SP3_DRYRUN=1: would run  lj_with_disk ${PLANNED_MB} sp3-blender -- bash spikes/sp3_blender/run_sp3.sh --run-inner"
    say "  python3 -m venv <scratch>/sp3/venv ; <venv>/bin/python -m pip install --no-cache-dir bpy==5.2.2"
    say "  for \"8 0 0\" \"64 0 0\" \"64 1 0\" \"128 1 0\": lj_bench <venv>/bin/python followup2-s3-kitchen-standin.py -- <scratch>/sp3/out 1920 1080 SAMPLES DENOISE ADAPTIVE"
    say "  rm -rf <scratch>/sp3"
    return 0
  fi
  lj_with_disk "$PLANNED_MB" "sp3-blender" -- bash "$SELF" --run-inner
}

case "${1:-}" in
  --check) do_check; exit $?;;
  --run) do_run; exit $?;;
  --run-inner) run_inner; exit $?;;
  -h|--help) awk 'NR > 1 && /^#/ { print; next } NR > 1 { exit }' "$SELF"; exit 0;;
  "") die "give --check or --run (try --help)";;
  *) die "unknown argument: $1 (try --help)";;
esac
