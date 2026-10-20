#!/usr/bin/env bash
# build/run_all_checks.sh: run every container-runnable acceptance test of the week 1-2 build and exit non-zero on any
# failure (build plan WP-11b integration; refs W-06, W-26, W-29, D-26, D-27, D-30, D-32).
#
#   bash build/run_all_checks.sh                run everything (the 13 package areas with  --all , plus the global checks)
#   bash build/run_all_checks.sh --quick        the same with each area's  --quick  (about 5 minutes instead of about 40)
#   bash build/run_all_checks.sh --global-only  only the global checks of Part A (about 2 minutes); no package area
#   bash build/run_all_checks.sh --list         print what would run, write nothing
#   options: --timeout SECONDS   per-area limit, passed to scripts/run_week2_checks.sh (default 900 for --all, 60 for --quick; win_kit2 has its own 90 s in --quick unless this option is given)
#
# WHAT RUNS (in this order; sequential, never parallel, because the render, timing and disk stages share one CPU budget)
#   Part A, global checks (each one command, expected exit 0; the same commands the build plan names in its acceptance lines)
#     public_lint --self-test --fail-on-skip   the redaction patterns agree in every consumer (PowerShell 7 included)
#     public_lint (diff mode)                  nothing identifying, no binary, no tracked-but-ignored file in the change set
#     public_lint --paths <build folders>      the same over every folder the build wrote
#     public_lint --theme                      the Hindu-only theme guard (D-28)
#     stale_check --self-test, --new-only      the W-29 stale-copy check, new hits only. --new-only runs ONCE per invocation: here only with
#                                              --global-only; with the package areas it is the integration area's hygiene.stale_check_new_only
#                                              (the same command, build plan WP-11b item 5), so Part A skips its copy (gate review r2, nudge 5)
#     ops_lint, decisions_to_csv --check,      the ops files, the CSV mirror of the register, the hours report
#       hours_report
#     ps_parse, ps_lint (two runs)             every Windows script and README fence parses on PowerShell 7 and obeys the 5.1 and read-only rules
#     cleanup_scratch (dry run)                what the end-of-fortnight cleanup would free (it deletes nothing)
#     repo.size_and_binary                     no file in the tree (tracked or not ignored) over 1 MB or with a NUL byte,
#                                              other than the reviewed fixtures named in scripts/public_lint.config.json
#     repo.gitignore_coverage                  every scratch, vendor, render and raw-report name the packages use is ignored,
#                                              and nothing that .gitignore ignores is tracked
#   Part B, the 13 package areas, through  scripts/run_week2_checks.sh  (hygiene, win, ops, validators, render, roundtrip,
#     sp1, win_lj, win_kit2, phone, spikes, runner, integration). That runner masks identifying data, enforces the per-area
#     timeout and the disk floor, and writes build/evidence/INDEX.md and week2_summary.json.
#
# RESULT WORDS    PASS (exit 0) | FAIL (any other exit; also a timed-out area) | BLOCKED (exit 3: the environment, for example no
#                 pwsh, a full disk, or another runner already running; never counted as PASS)
#                 UNVERIFIED is not a result of this script: it is the count of claims that need the maker's Windows PC, read from
#                 the evidence envelopes and printed at the end. They are never counted as PASS.
# EXIT CODE       0 every check and every landed area passed | 1 at least one FAIL | 2 bad usage, or the saved copy of the output
#                 looked like identifying data (it is then withheld) | 3 environment only (BLOCKED, no FAIL)
#
# WHAT IT WRITES  build/evidence/run_all_checks_<mode>.txt   the console output, with the repo and home folders replaced by
#                                                              <repo> and ~, and scanned by public_lint before it is kept
#                 plus whatever scripts/run_week2_checks.sh writes (build/evidence/INDEX.md, week2_summary.json, wp*/ evidence).
#                 Scratch files live in <scratch>/ra.XXXXXX (the scratch folder beside the repo) and are removed on exit.
# WHAT IT NEVER DOES  deletes anything of a package, uses the network, needs administrator rights, commits or pushes, reads or
#                 prints a user name, host name, address or home folder. Children get stdin from /dev/null.
# Requires bash 4+, python3, git, df, timeout. node, ffmpeg and Chromium are needed by the areas themselves. UNVERIFIED on Windows
# (a Linux container script).
set -u

SELF="${BASH_SOURCE[0]}"
SELF_DIR="$(cd "$(dirname "$SELF")" && pwd)"
REPO="$(cd "$SELF_DIR/.." && pwd)"
SCRATCH_BASE="${LJ_SCRATCH:-$(cd "$REPO/.." && pwd)/build-scratch}"
HARD_FLOOR_MB=250
SOFT_FLOOR_MB=400
CHECK_TIMEOUT_S=300
EV_REL="build/evidence"

MODE="all"; LIST=0; AREAS=1; AREA_TIMEOUT=""
usage() {
  cat <<'EOF'
usage: bash build/run_all_checks.sh [--all | --quick | --global-only] [--timeout SECONDS] | --list
  (default)      the global checks, then the 13 package areas with --all (about 40 minutes)
  --quick        the same, each area with --quick (about 5 minutes)
  --global-only  only the global checks (about 2 minutes)
  --list         print what would run and write nothing
exit 0 all passed | 1 a check or area failed | 2 bad usage or withheld output | 3 environment only
EOF
}
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) MODE="all" ;;
    --quick) MODE="quick" ;;
    --global-only) MODE="global"; AREAS=0 ;;
    --list) LIST=1 ;;
    --timeout) shift; AREA_TIMEOUT="${1:-}"; [[ "$AREA_TIMEOUT" =~ ^[0-9]+$ ]] || { echo "usage: --timeout needs whole seconds" >&2; exit 2; } ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

cd "$REPO" || { echo "cannot enter the repository folder" >&2; exit 3; }
[[ -f scripts/run_week2_checks.sh && -f scripts/public_lint.py ]] || { echo "this does not look like the project folder (scripts/ is incomplete)" >&2; exit 3; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is not installed; nothing was run" >&2; exit 3; }
command -v git >/dev/null 2>&1 || { echo "git is not installed; nothing was run" >&2; exit 3; }

avail_mb() { LC_ALL=C ${LJ_DF_CMD:-df -BM -P /} 2>/dev/null | awk 'NR==2{gsub(/M/,"",$4);print $4}'; }

# The checks of Part A: name|command (run through bash -c from the repository root)
GLOBAL_CHECKS=(
  "lint.self_test|python3 -I scripts/public_lint.py --self-test --fail-on-skip"
  "lint.diff_mode|python3 -I scripts/public_lint.py"
  "lint.build_folders|python3 -I scripts/public_lint.py --paths win scripts pipeline ops spikes tests build \$(test -d skills-staging && echo skills-staging) reviews/build"  # skills-staging/ is linted only while it exists (2026-10-20: the install removed it)
  "lint.theme_guard|python3 -I scripts/public_lint.py --theme"
  "stale.self_test|python3 -I scripts/stale_check.py --self-test"
  "stale.new_only|python3 -I scripts/stale_check.py --new-only"   # dropped below when the areas run: the integration area runs the same command
  "ops.lint|python3 -I scripts/ops_lint.py"
  "ops.decisions_mirror|python3 -I scripts/decisions_to_csv.py --check ops/decisions.csv"
  "ops.hours_report|python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19"
  "win.ps_parse|bash win/tools/ps_parse.sh"
  "win.ps_lint_read_only|python3 -I win/tools/ps_lint.py win/step0_pc_tests.ps1 win/lj.ps1 win/kit2/*.ps1 win/README-MAKER.md win/README-LJ.md"
  "win.ps_lint_writers|python3 -I win/tools/ps_lint.py --allow-write win/kit2/README-KIT2.md spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md"
  "scratch.cleanup_dry_run|bash scripts/cleanup_scratch.sh --dry-run"
  "repo.size_and_binary|REPO_PY size_binary"
  "repo.gitignore_coverage|REPO_PY gitignore"
)

# stale_check --new-only is the one check that Part A and the integration area (hygiene.stale_check_new_only) both ran, 10 to 16 s each time. With the
# package areas it stays in the integration area (the build plan's WP-11b hygiene acceptance) and leaves Part A; --global-only has no integration area, so it keeps it.
PART_A_NOTE=""
if [[ "$AREAS" == 1 ]]; then
  _kept=()
  for c in "${GLOBAL_CHECKS[@]}"; do
    [[ "${c%%|*}" == "stale.new_only" ]] && continue
    _kept+=("$c")
  done
  GLOBAL_CHECKS=("${_kept[@]}")
  PART_A_NOTE="stale.new_only is not repeated here: Part B's integration area runs the same command (hygiene.stale_check_new_only); --global-only runs it here."
fi

if [[ "$LIST" == 1 ]]; then
  echo "Part A, global checks (exit 0 expected from each):"
  for c in "${GLOBAL_CHECKS[@]}"; do printf '  %-26s %s\n' "${c%%|*}" "${c#*|}"; done
  [[ -n "$PART_A_NOTE" ]] && echo "  ($PART_A_NOTE)"
  if [[ "$AREAS" == 1 ]]; then
    echo "Part B, package areas through scripts/run_week2_checks.sh --$MODE:"
    bash scripts/run_week2_checks.sh --list | sed -n '2,$p'
  else
    echo "Part B skipped (--global-only). This listing wrote nothing."
  fi
  exit 0
fi

# ------------------------------------------------------------------ scratch, capture, masking
mkdir -p "$SCRATCH_BASE" 2>/dev/null || { echo "the scratch folder beside the repository cannot be created" >&2; exit 3; }
WORK="$(mktemp -d "$SCRATCH_BASE/ra.XXXXXX" 2>/dev/null)" || { echo "cannot create a scratch folder" >&2; exit 3; }
trap 'rm -rf "$WORK"' EXIT
RAW="$WORK/console.txt"
RESULTS="$WORK/results.tsv"; : > "$RESULTS"
HOME_MASK="${HOME:-}"; [[ ${#HOME_MASK} -lt 4 ]] && HOME_MASK="/nonexistent-home-folder"

# the two repo checks of Part A, in python (stdlib only, run with -I)
REPO_PY_SRC="$WORK/repo_checks.py"
cat > "$REPO_PY_SRC" <<'PYEOF'
import fnmatch, json, os, subprocess, sys
sys.dont_write_bytecode = True
MAX_BYTES = 1_000_000

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout

def tree_files():
    raw = git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")
    return sorted({p.decode() for p in raw if p and os.path.isfile(p.decode())})

def size_binary():
    allow = []
    try:
        with open("scripts/public_lint.config.json", encoding="utf-8") as fh:
            allow = json.load(fh).get("allow_binary", [])
    except (OSError, ValueError):
        print("cannot read scripts/public_lint.config.json: failing closed")
        return 1
    big, binary, allowed = [], [], []
    files = tree_files()
    for p in files:
        size = os.path.getsize(p)
        if size > MAX_BYTES:
            big.append((p, size))
        with open(p, "rb") as fh:
            head = fh.read(8000)
        if b"\0" in head:
            if any(fnmatch.fnmatch(p, g) for g in allow):
                allowed.append(p)
            else:
                binary.append((p, size))
    # ignored folders are listed for information only: they can never be committed by accident
    ign_big = []
    for root in ("renders", "vendor", "exports", "media"):
        for d, _, fs in os.walk(root):
            for f in fs:
                q = os.path.join(d, f)
                if os.path.isfile(q) and os.path.getsize(q) > MAX_BYTES:
                    ign_big.append((q, os.path.getsize(q)))
    print("%d files scanned (tracked, or untracked and not ignored)" % len(files))
    for p, s in big:
        print("  OVER 1 MB  %9d  %s" % (s, p))
    for p, s in binary:
        print("  BINARY     %9d  %s" % (s, p))
    for p in allowed:
        print("  allowed    reviewed fixture named in scripts/public_lint.config.json: %s" % p)
    for q, s in ign_big:
        print("  info       %9d  %s (git-ignored, cannot be committed by accident)" % (s, q))
    bad = len(big) + len(binary)
    print("size_and_binary: %s (%d over 1 MB, %d binary, %d allowed fixture(s))" % ("FAIL" if bad else "ok", len(big), len(binary), len(allowed)))
    return 1 if bad else 0

# Names the packages create or the plan (Q-3) says must never be committed. Each must be ignored by .gitignore.
MUST_IGNORE = [
    "renders/wp04/a/frame_000001.png", "renders/wp08/phone.mp4", "renders/wp09/standin/01_masters/LJ-ST-0001-F.tif",
    "exports/final.mov", "media/scan.jpg", "vendor/js/gsap.min.js", "vendor/fonts/x.woff2", "vendor/craft/_keep/a.zip",
    "scripts/__pycache__/x.cpython-313.pyc", "research/sources/__pycache__/x.pyc", "pipeline/phone/__pycache__/x.pyc",
    "pc_report.json", "pc_report_2026-10-20.json", "win/pc_report_x.json", "colour_patch_pc.json", "colour_patch_pc_ffmpeg9.json",
    "maker-pc.json", "maker-pc-tier.json", "scripts/public_lint.deny.local.txt", "win/lj.config.local.json",
    "logs/run.log", "tests/win/logs/x.log", "spikes/sp3_blender/work/scene.blend", "spikes/sp4_idle/work/gaps.json",
    "srv.pid", "node_modules/x/index.js", "build-scratch/pwsh/pwsh", "build/evidence/wp07/x.partial", "renders/wp04/a.mp4.tmp",
]
# Names that must stay VISIBLE to git (a stray pattern could hide real work)
MUST_TRACK = [
    "build/run_all_checks.sh", "build/BUILD-STATUS.md", "build/evidence/INDEX.md", "scripts/redaction_patterns.json",
    "win/lj.ps1", "win/lj.config.example.json", "win/pins.json", "pipeline/bin/render.mjs", "pipeline/lib/libs.lock.json",
    "pipeline/phone/test_strings.json", "tests/win/fixtures/report_hex65_leak.json", "tests/ops/run_tests.sh",
    "spikes/VERDICTS-W2.md", "ops/hours.csv", "research/craft-visual-fixtures/at-layers.ora",
]

def check_ignored(path):
    return subprocess.run(["git", "check-ignore", "-q", "--no-index", path], capture_output=True).returncode == 0

def gitignore():
    missing = [p for p in MUST_IGNORE if not check_ignored(p)]
    hidden = [p for p in MUST_TRACK if check_ignored(p)]
    tracked_ignored = [p.decode() for p in git("ls-files", "-ci", "--exclude-standard", "-z").split(b"\0") if p]
    stray = []
    for p in tree_files():
        low = p.lower()
        if low.endswith((".pyc", ".pid", ".lock", ".tmp", ".partial", ".swp")) or "/__pycache__/" in low or low.startswith("node_modules/"):
            stray.append(p)
    print("%d names that must be ignored, %d names that must stay visible" % (len(MUST_IGNORE), len(MUST_TRACK)))
    for p in missing:
        print("  NOT IGNORED   %s   (append a line to .gitignore)" % p)
    for p in hidden:
        print("  WRONGLY HIDDEN %s   (a .gitignore pattern is too broad)" % p)
    for p in tracked_ignored:
        print("  TRACKED BUT IGNORED  %s   (git rm --cached; the orchestrator commits)" % p)
    for p in stray:
        if p not in tracked_ignored:
            print("  SCRATCH-LIKE FILE in the tree  %s" % p)
    bad = len(missing) + len(hidden) + len(tracked_ignored) + len([p for p in stray if p not in tracked_ignored])
    print("gitignore_coverage: %s (%d not ignored, %d hidden, %d tracked-but-ignored)" % ("FAIL" if bad else "ok", len(missing), len(hidden), len(tracked_ignored)))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit({"size_binary": size_binary, "gitignore": gitignore}[sys.argv[1]]())
PYEOF

record() { printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> "$RESULTS"; }  # name, result, exit, seconds

show_tail() {  # file, max lines
  local f="$1" n="$2"
  sed -e 's/\x1b\[[0-9;]*[A-Za-z]//g' "$f" | tail -n "$n" | sed 's/^/    | /'
}

run_check() {  # name, command
  local name="$1" cmd="$2" out="$WORK/out.$$.txt" t0 t1 rc res last
  if [[ "$cmd" == REPO_PY\ * ]]; then cmd="python3 -I '$REPO_PY_SRC' ${cmd#REPO_PY }"; fi
  t0=$(date +%s)
  timeout -k 5 "$CHECK_TIMEOUT_S" bash -c "$cmd" < /dev/null > "$out" 2>&1
  rc=$?
  t1=$(date +%s)
  case "$rc" in
    0) res=PASS ;;
    3) res=BLOCKED ;;
    124|137) res=FAIL ;;
    *) res=FAIL ;;
  esac
  last="$(sed -e 's/\x1b\[[0-9;]*[A-Za-z]//g' "$out" | grep -v '^[[:space:]]*$' | tail -n 1 | cut -c1-170)"
  printf '[%-7s] %-26s exit %-3s %4ss  %s\n' "$res" "$name" "$rc" "$((t1 - t0))" "$last"
  if [[ "$res" != PASS ]]; then show_tail "$out" 14; fi
  record "$name" "$res" "$rc" "$((t1 - t0))"
  rm -f "$out"
}

main() {
  local a0 amin a start now
  start=$(date +%s)
  a0="$(avail_mb)"; amin="$a0"
  echo "run_all_checks: mode $MODE, started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "tools: $(python3 --version 2>&1), node $(node --version 2>/dev/null || echo missing), $(ffmpeg -version 2>/dev/null | head -n 1 | cut -d' ' -f1-3 || echo 'ffmpeg missing'), pwsh $(for c in "${PWSH:-}" "$SCRATCH_BASE/pwsh/pwsh" "$(command -v pwsh 2>/dev/null)"; do [[ -n "$c" && -x "$c" ]] && { "$c" -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' 2>/dev/null; break; }; done)"
  echo "branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null), head $(git rev-parse --short HEAD 2>/dev/null), $(git status --porcelain 2>/dev/null | wc -l) changed or untracked path(s)"
  if [[ ! "$a0" =~ ^[0-9]+$ ]]; then echo "disk: cannot read free space; nothing was run"; return 3; fi
  echo "disk: Avail ${a0} MB (plan floors: ${SOFT_FLOOR_MB} soft, ${HARD_FLOOR_MB} hard)"
  if (( a0 < HARD_FLOOR_MB )); then
    echo "BLOCKED: free disk is under the ${HARD_FLOOR_MB} MB hard floor; nothing was run. 'bash scripts/cleanup_scratch.sh' (dry run) shows what could be freed."
    return 3
  fi
  (( a0 < SOFT_FLOOR_MB )) && echo "note: under the ${SOFT_FLOOR_MB} MB soft floor; the guarded stages of the areas may report BLOCKED"

  echo
  echo "== Part A: global checks (${#GLOBAL_CHECKS[@]}) =="
  [[ -n "$PART_A_NOTE" ]] && echo "note: $PART_A_NOTE"
  local c
  for c in "${GLOBAL_CHECKS[@]}"; do
    run_check "${c%%|*}" "${c#*|}"
    a="$(avail_mb)"; [[ "$a" =~ ^[0-9]+$ ]] && (( a < amin )) && amin="$a"
  done

  if [[ "$AREAS" == 1 ]]; then
    echo
    echo "== Part B: the 13 package areas, scripts/run_week2_checks.sh --$MODE =="
    local rargs=("--$MODE")
    [[ -n "$AREA_TIMEOUT" ]] && rargs+=("--timeout" "$AREA_TIMEOUT")
    local out="$WORK/runner.txt" t0 t1 rc
    t0=$(date +%s)
    bash scripts/run_week2_checks.sh "${rargs[@]}" < /dev/null > "$out" 2>&1
    rc=$?
    t1=$(date +%s)
    # the runner already masks identifying data; print its console output as it is
    sed -e 's/\x1b\[[0-9;]*[A-Za-z]//g' "$out"
    case "$rc" in 0) record "areas.runner" PASS "$rc" "$((t1 - t0))" ;; 1) record "areas.runner" FAIL "$rc" "$((t1 - t0))" ;; 3) record "areas.runner" BLOCKED "$rc" "$((t1 - t0))" ;; *) record "areas.runner" FAIL "$rc" "$((t1 - t0))" ;; esac
    a="$(avail_mb)"; [[ "$a" =~ ^[0-9]+$ ]] && (( a < amin )) && amin="$a"
  else
    echo
    echo "== Part B skipped (--global-only) =="
  fi

  echo
  echo "== Summary =="
  python3 -I - "$RESULTS" "$EV_REL/week2_summary.json" "$AREAS" "$MODE" <<'PYEOF'
import json, os, sys
sys.dont_write_bytecode = True
res_path, sum_path, areas, mode = sys.argv[1], sys.argv[2], sys.argv[3] == "1", sys.argv[4]
rows = [l.rstrip("\n").split("\t") for l in open(res_path, encoding="utf-8") if l.strip()]
glob = [r for r in rows if not r[0].startswith("areas.")]
count = lambda rs, w: sum(1 for r in rs if r[1] == w)
print("Part A global checks: %d PASS, %d FAIL, %d BLOCKED of %d" % (count(glob, "PASS"), count(glob, "FAIL"), count(glob, "BLOCKED"), len(glob)))
for r in glob:
    if r[1] != "PASS":
        print("  %-8s %s (exit %s)" % (r[1], r[0], r[2]))
if areas:
    try:
        d = json.load(open(sum_path, encoding="utf-8"))
    except (OSError, ValueError):
        d = None
    if d is None or d.get("mode") != mode:
        print("Part B: no fresh week2_summary.json for mode %s (the runner stopped before writing it)" % mode)
    else:
        print("Part B package areas (generated %s, runner result %s, %ss):" % (d.get("generated_utc"), d.get("result"), d.get("elapsed_s")))
        print("  %-3s %-12s %-8s %-8s %5s %5s %5s %5s" % ("#", "area", "entry", "result", "PASS", "FAIL", "UNVER", "BLOCK"))
        for a in d.get("areas", []):
            c = a.get("counts", {})
            print("  %-3s %-12s %-8s %-8s %5s %5s %5s %5s" % (a.get("order"), a.get("area"), a.get("entry"), a.get("result"),
                  c.get("PASS", 0), c.get("FAIL", 0), c.get("UNVERIFIED", 0), c.get("BLOCKED", 0)))
        t = d.get("envelope_totals", {})
        print("  envelope totals: PASS %s, FAIL %s, UNVERIFIED %s, SKIPPED %s, BLOCKED %s (UNVERIFIED needs the maker's Windows PC; never counted as PASS)" % (
              t.get("PASS"), t.get("FAIL"), t.get("UNVERIFIED"), t.get("SKIPPED"), t.get("BLOCKED")))
        dk = d.get("disk", {})
        if dk:
            print("  runner disk: %s" % json.dumps(dk, sort_keys=True)[:200])
PYEOF
  now=$(date +%s)
  echo "disk: Avail ${a0} MB at start, lowest seen between stages ${amin} MB, $(avail_mb) MB at end"
  echo "elapsed: $((now - start)) s"

  # overall exit code
  local nfail nblock
  nfail=$(awk -F'\t' '$2=="FAIL"{n++} END{print n+0}' "$RESULTS")
  nblock=$(awk -F'\t' '$2=="BLOCKED"{n++} END{print n+0}' "$RESULTS")
  if (( nfail > 0 )); then echo "RESULT: FAIL ($nfail failing item(s), $nblock blocked). Exit 1."; return 1; fi
  if (( nblock > 0 )); then echo "RESULT: BLOCKED ($nblock item(s) could not run here; no failure). Exit 3."; return 3; fi
  echo "RESULT: PASS (every global check and every landed area passed). Exit 0."
  return 0
}

main 2>&1 | sed -u -e "s#$REPO#<repo>#g" -e "s#$SCRATCH_BASE#<scratch>#g" -e "s#$HOME_MASK#~#g" | tee "$RAW"
RC="${PIPESTATUS[0]}"

# keep a copy only if the public-repo lint finds nothing identifying in it
DEST_REL="$EV_REL/run_all_checks_${MODE}.txt"
if [[ -s "$RAW" && "$RC" != 2 ]]; then
  mkdir -p "$EV_REL" 2>/dev/null
  cp "$RAW" "$DEST_REL" 2>/dev/null
  if python3 -I scripts/public_lint.py --paths "$DEST_REL" > "$WORK/lint.txt" 2>&1; then
    echo "saved: $DEST_REL"
  else
    rm -f "$DEST_REL"
    echo "WITHHELD: the saved copy of this output failed scripts/public_lint.py, so it was deleted. Kinds only:"
    grep -E '^(FINDING|public_lint:)' "$WORK/lint.txt" | cut -c1-120 | head -n 8
    exit 2
  fi
fi
exit "$RC"
