#!/usr/bin/env bash
# run_week2_checks.sh: the week 1-2 check runner (build plan WP-11a; refs W-06, W-26, W-29, D-26, D-30).
#
#   bash scripts/run_week2_checks.sh --list              the 13 areas in order and which have landed (writes nothing)
#   bash scripts/run_week2_checks.sh --quick             every landed area's  tests/<area>/run_tests.sh --quick  (60 s each)
#   bash scripts/run_week2_checks.sh --all               every landed area's  tests/<area>/run_tests.sh --all    (900 s each)
#   options: --timeout SECONDS   per-area limit (replaces the 60 s / 900 s defaults, and any longer quick limit an area has in DEFAULT_AREAS)
#
# FIXED RUN ORDER (dependency order; sequential, never parallel; DEFAULT_AREAS below is the code form of this list):
#    1 hygiene      WP-03   redaction patterns, disk/bench guard, stale_check, public_lint
#    2 win          WP-01a  Windows kit A (PC inventory script, report checker)
#    3 ops          WP-02   ops files, hours log, settings card
#    4 validators   WP-05   ffprobe spec checker, colour patch, MO8 gate, chains
#    5 render       WP-04   render.mjs harness, test scene, test strings
#    6 roundtrip    WP-06   ORA, SVG ids, OTIO
#    7 sp1          WP-07   SP1a release sums and headless Craft tests
#    8 win_lj       WP-01b  lj.ps1 doctor and close v0 (dry-run only)
#    9 win_kit2     WP-09   Windows kit B (Ken Burns, archive, PC colour runner)
#   10 phone        WP-08   phone encode profile and legibility check
#   11 spikes       WP-10   SP1b read-backs, SP3, SP4, spike verdict table
#   12 runner       WP-11a  this runner, the INDEX writer, cleanup_scratch.sh
#   13 integration  WP-11b  parity, redaction, disk and end-to-end checks
# The same 13 names, in the same order, are the 13 schedulable entries WP-01a ... WP-11b of the build plan.
#
# RESULT PER AREA
#   PASS         tests/<area>/run_tests.sh exists and exited 0
#   FAIL         it exited non-zero (exit 3 means "environment": disk guard, lock busy, missing tool)
#   TIMEOUT      it did not finish inside the per-area limit; its whole process group was killed (also a FAIL)
#   NOT LANDED   tests/<area>/run_tests.sh does not exist yet: listed, never a failure, exit code unaffected
# Exit code of the runner (build plan 4.3): 0 no area FAILed or TIMED OUT; 1 at least one did;
#   2 bad usage, or identifying data would have been written, or the redaction scanner is unusable (fail closed);
#   3 environment (no python3, evidence folder not writable, a full disk, another runner already running, runner
#   started inside itself). A run that stops after the areas have started (exit 2 or 3) removes the older INDEX.md,
#   week2_summary.json and wave1_quick.txt so that no stale copy looks current.
#
# WHAT IT WRITES (and nothing else; it never edits another package's files)
#   build/evidence/INDEX.md            one row per entry: result, counts of PASS / FAIL / UNVERIFIED / SKIPPED / BLOCKED
#                                      taken from the lj-evidence/1 envelopes found under that entry's evidence folder
#                                      (one per package+test, the newest wins), evidence links, owner, and the LOWEST
#                                      disk.avail_mb_min seen in them (so the disk budget is visible)
#   build/evidence/week2_summary.json  the same as data (schema lj-week2-summary/1)
#   build/evidence/wave1_quick.txt     --quick only: the exact console output (the file attached to the Fri 23 Oct bundle)
#   build/evidence/wp11a/area_<area>_<mode>.txt   each area's output, masked, last 400 lines
#   build/evidence/wp11a/console_all.txt          --all only: the exact console output
# Scratch files live in a throw-away folder under the scratch folder beside the repo and are removed on exit.
#
# REDACTION (D-26: the repository is public). Everything the runner stores or prints from an area's output passes
# through a masker that reads ONLY scripts/redaction_patterns.json (via the Patterns class of scripts/public_lint.py);
# this file carries no pattern of its own. A hit is replaced by its first two characters and asterisks. If the
# pattern file or the scanner cannot be loaded, or fails its own sanity sample, the runner prints why and exits 2
# BEFORE running anything. Once public_lint.py offers  --text , the finished texts are also fed to
#   python3 -I scripts/public_lint.py --text      (assumed contract: text on stdin, exit 0 = clean)
# and any other exit code withholds INDEX.md, week2_summary.json and wave1_quick.txt (exit 2).
# Until then the line "public_lint --text: not available yet" is printed. The contract is UNVERIFIED (it does not exist).
#
# TEST HOOKS (tests/runner uses them; a normal run sets none)
#   LJ_RUNNER_AREAS_FILE    replaces the 13 areas by lines  area|entry|evidence-subfolder|wave|title[|quick-limit-seconds]  (needs the next one)
#   LJ_RUNNER_EVIDENCE_DIR  where the evidence folders and the three outputs live (default build/evidence)
#   LJ_RUNNER_TESTS_DIR     where tests/<area>/run_tests.sh are looked for (default tests)
#   LJ_RUNNER_TIMEOUT_S     per-area limit for every area (the --timeout option wins; either one also switches off an area's own longer quick limit)   LJ_RUNNER_BUDGET_S  quick budget (450; see below)
#   LJ_RUNNER_KILL_GRACE_S  seconds between TERM and KILL for a timed-out area (3)
#   LJ_RUNNER_PATTERNS, LJ_RUNNER_LINT   alternative pattern file and public_lint.py
#   LJ_RUNNER_LINT_TEXT=skip   do not call public_lint --text even if it exists (printed in the output)
#   LJ_SCRATCH              scratch folder (default build-scratch beside the repo folder)
#   LJ_DF_CMD               replaces  df -BM -P /  (as in lj_guard.sh) so the low-disk lines can be tested
#
# ONE RUN AT A TIME. A second runner for the same evidence folder prints BUSY and exits 3 (lock file in the scratch folder).
# WHAT IT NEVER TOUCHES. It deletes nothing of any package, starts no download, uses no network, needs no admin
# rights, writes no bytecode, and prints no absolute path, host name or user name. Children get stdin from /dev/null.
# Requires bash 4+, python3, setsid, df. UNVERIFIED on Windows (this is a Linux container script).
set -u

SELF="${BASH_SOURCE[0]}"
SELF_DIR="$(cd "$(dirname "$SELF")" && pwd)"
REPO="$(cd "$SELF_DIR/.." && pwd)"
TESTS_DIR="${LJ_RUNNER_TESTS_DIR:-$REPO/tests}"
EVDIR="${LJ_RUNNER_EVIDENCE_DIR:-$REPO/build/evidence}"
PATTERNS="${LJ_RUNNER_PATTERNS:-$SELF_DIR/redaction_patterns.json}"
LINT="${LJ_RUNNER_LINT:-$SELF_DIR/public_lint.py}"
SCRATCH="${LJ_SCRATCH:-$(cd "$REPO/.." && pwd)/build-scratch}"

# order|entry|evidence subfolder|wave|what it covers|quick limit in seconds (optional; only --quick, and only when neither --timeout nor LJ_RUNNER_TIMEOUT_S is given)
# A longer quick limit for one area needs a dated reason on its own line, so the limit does not drift. win_kit2: 90 s since Tue 20 Oct 2026 (gate w2, nudge 6). Its quick pass took 47 s on one host
# (39 s and 37 s on others; about 80 CPU-seconds on 4 vCPUs, six processes at once), and the hosts this session has landed on differed by 1.4x to 2x (SP3: 2x; the whole quick pass: 270 s and 374 s), so 47 s can
# become 66 to 94 s, past the common 60 s. 90 s covers a 1.9x host; a hang is still killed. The budget for the whole of Part B (450 s) is unchanged and still flags a slow run without failing it.
# validators (45 s), phone (38 s), runner (37 s) and integration (36 s) have the same exposure at a smaller margin; they stay on 60 s until a measured run says otherwise.
DEFAULT_AREAS=(
  "hygiene|WP-03|wp03|1|redaction patterns, disk and bench guard, stale_check, public_lint"
  "win|WP-01a|wp01a|1|Windows kit A: PC inventory script, report checker, tools"
  "ops|WP-02|wp02|1|ops files, hours log, settings card text"
  "validators|WP-05|wp05|1|ffprobe spec checker, colour patch, MO8 gate, chains"
  "render|WP-04|wp04|1|render.mjs harness, test scene, test strings, fonts"
  "roundtrip|WP-06|wp06|1|ORA, SVG ids, OTIO round trips"
  "sp1|WP-07|wp07|1|SP1a release sums and headless Craft tests"
  "win_lj|WP-01b|wp01b|2|lj.ps1 doctor and close v0 (dry-run only)"
  "win_kit2|WP-09|wp09|1+2|Windows kit B: Ken Burns, archive, PC colour runner|90"
  "phone|WP-08|wp08|2|phone encode profile and legibility check"
  "spikes|WP-10|wp10|2|SP1b read-backs, SP3, SP4, spike verdict table"
  "runner|WP-11a|wp11a|1|this runner, the INDEX writer, cleanup_scratch.sh"
  "integration|WP-11b|wp11b|3|parity, redaction, disk and end-to-end checks"
)

usage() {
  cat <<'EOF'
usage: bash scripts/run_week2_checks.sh --list | --quick | --all  [--timeout SECONDS]
  --list     print the areas in run order and which have landed; writes nothing
  --quick    run every landed area's run_tests.sh --quick (60 s each); writes INDEX.md, week2_summary.json, wave1_quick.txt
  --all      run every landed area's run_tests.sh --all (900 s each); writes INDEX.md, week2_summary.json
exit 0 all landed areas passed | 1 an area failed or timed out | 2 bad usage or redaction problem | 3 environment
EOF
}

die() { printf '%s\n' "$2" >&2; exit "$1"; }

# --------------------------------------------------------------------------- embedded python (stdlib only, run with -I)
IFS= read -r -d '' PYSRC <<'PYEOF'
import argparse, datetime, glob, importlib.util, json, os, platform, re, sys
sys.dont_write_bytecode = True

STATUSES = ("PASS", "FAIL", "UNVERIFIED", "SKIPPED", "BLOCKED")
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class Refuse(Exception):
    pass


def load_scanner(lint_path, pat_path):
    """Load Patterns from scripts/public_lint.py and the pattern file; prove it is live with a runtime-built sample."""
    if not os.path.isfile(pat_path):
        raise Refuse("the redaction pattern file scripts/redaction_patterns.json is missing; nothing was run")
    if not os.path.isfile(lint_path):
        raise Refuse("scripts/public_lint.py is missing; nothing was run")
    try:
        spec = importlib.util.spec_from_file_location("lj_public_lint", lint_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        pats = mod.load_patterns(pat_path)
    except Exception as e:
        why = str(e) if type(e).__name__ == "FailClosed" else "cannot load the redaction scanner (%s)" % type(e).__name__
        raise Refuse(why)
    probe = "zz.check" + "@" + "nowhere-co" + "." + "org"
    if not any(h[0] == "email" for h in pats.scan_line("x " + probe + " y")):
        raise Refuse("the redaction scanner did not flag its own e-mail-shaped sample; nothing was run")
    return pats


def clean(line):
    return CTRL.sub("", ANSI.sub("", line.replace("\r", "")))


def mask_line(pats, line):
    hits = pats.scan_line(line)
    if not hits:
        return line, 0
    spans = sorted((s, s + len(t)) for _, t, s in hits)
    merged = []
    for s, e in spans:
        if merged and s < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    out, pos = [], 0
    for s, e in merged:
        out.append(line[pos:s])
        out.append(pats.mask(line[s:e]))
        pos = e
    out.append(line[pos:])
    return "".join(out), len(merged)


def mask_text(pats, text):
    total, lines = 0, []
    for line in text.split("\n"):
        line = clean(line)
        for _ in range(3):
            line, n = mask_line(pats, line)
            total += n
            if n == 0:
                break
        if pats.scan_line(line):
            raise Refuse("a hit survived masking; nothing was written")
        lines.append(line)
    return "\n".join(lines), total


def cmd_selfcheck(a):
    load_scanner(a.lint, a.patterns)
    return 0


def cmd_mask(a):
    pats = load_scanner(a.lint, a.patterns)
    text = sys.stdin.buffer.read().decode("utf-8", "replace")
    out, total = mask_text(pats, text)
    sys.stdout.buffer.write(out.encode("utf-8"))
    sys.stdout.buffer.flush()
    if a.hits_out:
        with open(a.hits_out, "w") as f:
            f.write("%d\n" % total)
    return 0


def cmd_maskmany(a):
    pats = load_scanner(a.lint, a.patterns)
    for src, dst in a.pair:
        with open(src, "rb") as f:
            text = f.read().decode("utf-8", "replace")
        out, total = mask_text(pats, text)
        with open(dst, "wb") as f:
            f.write(out.encode("utf-8"))
        print(total)
    return 0


def read_envelopes(evroot, sub):
    base = os.path.join(evroot, sub)
    res = {"counts": dict.fromkeys(STATUSES, 0), "envelopes": 0, "avail_min": None, "unknown_status": 0, "unreadable": 0, "newest": None}
    if not os.path.isdir(base):
        return res
    latest = {}
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for f in sorted(files):
            if not (f.endswith(".json") or f.endswith(".jsonl")):
                continue
            p = os.path.join(root, f)
            try:
                if os.path.getsize(p) > 8 * 1024 * 1024:
                    res["unreadable"] += 1
                    continue
                text = open(p, encoding="utf-8", errors="replace").read()
                mtime = os.path.getmtime(p)
            except OSError:
                res["unreadable"] += 1
                continue
            objs = []
            if f.endswith(".jsonl"):
                for i, ln in enumerate(text.splitlines()):
                    if ln.strip():
                        try:
                            objs.append((i, json.loads(ln)))
                        except ValueError:
                            res["unreadable"] += 1
            else:
                try:
                    objs.append((0, json.loads(text)))
                except ValueError:
                    res["unreadable"] += 1
            rel = os.path.relpath(p, evroot)
            for i, o in objs:
                if not (isinstance(o, dict) and o.get("schema") == "lj-evidence/1"):
                    continue
                res["newest"] = mtime if res["newest"] is None else max(res["newest"], mtime)
                st = o.get("status")
                if st not in STATUSES:
                    res["unknown_status"] += 1
                    continue
                res["envelopes"] += 1
                d = o.get("disk")
                m = d.get("avail_mb_min") if isinstance(d, dict) else None
                if isinstance(m, (int, float)) and not isinstance(m, bool):
                    res["avail_min"] = m if res["avail_min"] is None else min(res["avail_min"], m)
                key = (o.get("package"), o.get("test")) if o.get("test") else (rel, i)
                sk = (str(o.get("date_utc") or ""), mtime, rel, i)
                if key not in latest or sk >= latest[key][0]:
                    latest[key] = (sk, st)
    for _, st in latest.values():
        res["counts"][st] += 1
    return res


NOTABLE = ("summary.json", "tests_quick.txt", "tests_all.txt", "tests.jsonl", "tests_quick.jsonl", "acceptance_transcript.txt")


def num(v):
    return int(v) if str(v).isdigit() else None


def cmd_collect(a):
    rows = []
    for ln in open(a.state, encoding="utf-8"):
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 10:
            rows.append(c)
    mode = a.mode
    areas, tot = [], dict.fromkeys(STATUSES, 0)
    low_entries = []
    lowest = None
    for c in rows:
        idx, area, entry, sub, wave, status, rc, secs, tlim, note = c[:10]
        env = read_envelopes(a.evdir, sub)
        links = []
        if os.path.isdir(os.path.join(a.evdir, sub)):
            links.append(sub + "/")
            links += [sub + "/" + n for n in NOTABLE if os.path.isfile(os.path.join(a.evdir, sub, n))][:3]
        logrel = "wp11a/area_%s_%s.txt" % (area, mode)
        if os.path.isfile(os.path.join(a.evdir, logrel)):
            links.append(logrel)
        for k in STATUSES:
            tot[k] += env["counts"][k]
        am = env["avail_min"]
        if am is not None:
            if lowest is None or am < lowest[0]:
                lowest = (am, entry)
            if am < a.hard_floor:
                low_entries.append(entry)
        fresh = None if env["newest"] is None else bool(env["newest"] >= a.run_start - 1)
        areas.append({
            "order": int(idx), "area": area, "entry": entry, "wave": wave, "owner": "sonnet-implementor (tests/%s/)" % area,
            "result": status, "exit_code": (int(rc) if rc.lstrip("-").isdigit() else None), "exit_text": rc, "seconds": int(secs),
            "timeout_s": int(tlim), "landed": status != "NOT LANDED", "note": note,
            "counts": env["counts"], "envelopes": env["envelopes"], "avail_mb_min": am, "envelopes_refreshed_this_run": fresh,
            "unknown_status_envelopes": env["unknown_status"], "unreadable_evidence_files": env["unreadable"],
            "evidence": links})
    n = lambda s: sum(1 for x in areas if x["result"] == s)
    totals = {"areas": len(areas), "landed": sum(1 for x in areas if x["landed"]), "pass": n("PASS"), "fail": n("FAIL"),
              "timeout": n("TIMEOUT"), "not_landed": n("NOT LANDED")}
    checks = []
    for x in areas:
        c = x["counts"]
        who = "%s (%s)" % (x["area"], x["entry"])
        if x["result"] == "PASS" and c["FAIL"]:
            checks.append("%s exited 0 but %d FAIL envelope(s) are on file (refreshed this run: %s); read the evidence, not just the exit code"
                          % (who, c["FAIL"], {None: "n/a", True: "yes", False: "no"}[x["envelopes_refreshed_this_run"]]))
        if x["result"] in ("FAIL", "TIMEOUT") and not c["FAIL"] and not c["BLOCKED"]:
            checks.append("%s did not pass but no FAIL or BLOCKED envelope is on file (the area may write none in --%s, or the evidence is older)" % (who, mode))
    over = bool(a.budget and a.elapsed > a.budget)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary = {
        "schema": "lj-week2-summary/1", "mode": mode, "generated_utc": now,
        "result": "FAIL" if (totals["fail"] or totals["timeout"]) else "PASS", "exit_code": a.exit_code,
        "per_area_timeout_s": a.timeout, "elapsed_s": a.elapsed, "budget_s": a.budget or None, "over_budget": over,
        "env": {"platform": platform.system().lower(), "nproc": os.cpu_count(), "python": platform.python_version(), "bash": a.bash},
        "disk": {"avail_mb_start": num(a.avail_start), "avail_mb_min": num(a.avail_min), "avail_mb_end": num(a.avail_end), "hard_floor_mb": a.hard_floor,
                 "lowest_envelope_avail_mb_min": (lowest[0] if lowest else None), "lowest_envelope_entry": (lowest[1] if lowest else None),
                 "entries_below_hard_floor": low_entries},
        "public_lint_text": a.lint_text, "totals": totals, "envelope_totals": tot, "checks": checks, "areas": areas,
        "notes": ["counts come from lj-evidence/1 envelopes under each entry's evidence folder (one per package+test, newest wins); "
                  "they are not the area's exit code", "a NOT LANDED entry may still show envelopes written before its run_tests.sh existed"]}
    with open(a.out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")

    def cell(x):
        return str(x).replace("|", "\\|")

    def avail_cell(v):
        if v is None:
            return "n/a"
        v = int(v) if float(v) == int(v) else v
        return "%s LOW (below %d)" % (v, a.hard_floor) if v < a.hard_floor else str(v)

    L = ["# Week 1-2 evidence index", "",
         "Generated by `scripts/run_week2_checks.sh --%s` on %s. Do not edit by hand; run the script again." % (mode, now), "",
         "- Result: **%s** (runner exit %d). Areas %d, landed %d: PASS %d, FAIL %d, TIMEOUT %d, NOT LANDED %d."
         % (summary["result"], a.exit_code, totals["areas"], totals["landed"], totals["pass"], totals["fail"], totals["timeout"], totals["not_landed"]),
         "- Elapsed %d s%s; per-area limit %d s%s." % (a.elapsed, (" against a %d s budget (%s)" % (a.budget, "OVER BUDGET" if over else "within")) if a.budget else "", a.timeout,
                                                       ("; own limit: " + ", ".join("%s %d s" % (x["area"], x["timeout_s"]) for x in areas if x["timeout_s"] != a.timeout)) if any(x["timeout_s"] != a.timeout for x in areas) else ""),
         "- Envelope totals (all entries): PASS %d, FAIL %d, UNVERIFIED %d, SKIPPED %d, BLOCKED %d."
         % tuple(tot[k] for k in STATUSES),
         "- Disk: Avail %s MB at start, %s MB lowest during the run, %s MB at end; lowest `avail_mb_min` in any envelope: %s%s; hard floor %d MB."
         % (a.avail_start, a.avail_min, a.avail_end, (str(int(lowest[0])) if lowest else "n/a"), (" (%s)" % lowest[1] if lowest else ""), a.hard_floor),
         "- public_lint --text: %s." % a.lint_text] + ["- Check: " + c for c in checks] + [""] + [
         "| # | Entry | Area | Result | Exit | s | PASS | FAIL | UNVERIFIED | SKIPPED | BLOCKED | Refreshed | Lowest avail_mb_min | Evidence | Owner |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in areas:
        ev = " ".join("[%s](%s)" % (cell(p), cell(p)) for p in x["evidence"]) or "none"
        c = x["counts"]
        rf = {None: "-", True: "yes", False: "no"}[x["envelopes_refreshed_this_run"]]
        L.append("| %d | %s | %s | **%s** | %s | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s |" % (
            x["order"], cell(x["entry"]), cell(x["area"]), x["result"], cell(x["exit_text"]), x["seconds"],
            c["PASS"], c["FAIL"], c["UNVERIFIED"], c["SKIPPED"], c["BLOCKED"], rf, avail_cell(x["avail_mb_min"]), ev, cell(x["owner"])))
    L += ["", "How to read this. Result is what the area's `run_tests.sh --%s` did: PASS (exit 0), FAIL (non-zero), TIMEOUT (killed at the limit; also a FAIL), "
          "NOT LANDED (`tests/<area>/run_tests.sh` does not exist yet; not a failure). The five count columns come from the `lj-evidence/1` envelopes "
          "found under the entry's evidence folder (build plan 4.2), one per package and test, the newest winning; a NOT LANDED entry can still show "
          "envelopes that were written before its tests existed. Refreshed says whether any of those envelopes was written during this run: "
          "`no` means the counts are older evidence (for example an area whose --%s run writes only a text log), `-` means no envelope exists. UNVERIFIED means a claim that needs the maker's Windows PC; it is never counted as PASS. "
          "`Lowest avail_mb_min` is the smallest free-disk figure any envelope of the entry recorded (MB); below the hard floor it is marked LOW. "
          "Every link above points to a file or folder that exists when this page is written." % (mode, mode), ""]
    with open(a.out_index, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("Envelopes: %d counted (PASS %d, FAIL %d, UNVERIFIED %d, SKIPPED %d, BLOCKED %d)" % ((sum(tot.values()),) + tuple(tot[k] for k in STATUSES)))
    if lowest:
        print("Lowest avail_mb_min in any envelope: %d MB (%s)%s" % (lowest[0], lowest[1],
              ("; below the %d MB hard floor: %s" % (a.hard_floor, ", ".join(low_entries))) if low_entries else "; none below the hard floor"))
    else:
        print("Lowest avail_mb_min in any envelope: n/a (no envelope carries a disk block)")
    for c in checks:
        print("Check: " + c)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name in ("selfcheck", "mask"):
        p = sp.add_parser(name)
        p.add_argument("--patterns", required=True)
        p.add_argument("--lint", required=True)
        if name == "mask":
            p.add_argument("--hits-out")
    p = sp.add_parser("maskmany")
    p.add_argument("--patterns", required=True)
    p.add_argument("--lint", required=True)
    p.add_argument("--pair", nargs=2, action="append", required=True, metavar=("IN", "OUT"))
    p = sp.add_parser("collect")
    p.add_argument("--state", required=True)
    p.add_argument("--evdir", required=True)
    p.add_argument("--mode", required=True)
    p.add_argument("--out-index", required=True)
    p.add_argument("--out-json", required=True)
    p.add_argument("--elapsed", type=int, default=0)
    p.add_argument("--run-start", type=int, default=0)
    p.add_argument("--budget", type=int, default=0)
    p.add_argument("--timeout", type=int, default=0)
    p.add_argument("--exit-code", type=int, default=0)
    p.add_argument("--avail-start", default="n/a")
    p.add_argument("--avail-min", default="n/a")
    p.add_argument("--avail-end", default="n/a")
    p.add_argument("--hard-floor", type=int, default=250)
    p.add_argument("--lint-text", default="not available yet")
    p.add_argument("--bash", default="")
    a = ap.parse_args()
    try:
        return {"selfcheck": cmd_selfcheck, "mask": cmd_mask, "maskmany": cmd_maskmany, "collect": cmd_collect}[a.cmd](a)
    except Refuse as e:
        sys.stderr.write("REDACTION: %s\n" % e)
        return 2


sys.exit(main())
PYEOF

py() { PYTHONDONTWRITEBYTECODE=1 python3 -I -c "$PYSRC" "$@"; }

# --------------------------------------------------------------------------- arguments
MODE=""
TIMEOUT_ARG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list|--quick|--all)
      [[ -n "$MODE" ]] && { usage >&2; die 2 "choose exactly one of --list, --quick, --all"; }
      MODE="${1#--}" ;;
    --timeout)
      [[ $# -ge 2 ]] || { usage >&2; die 2 "--timeout needs a number of seconds"; }
      TIMEOUT_ARG="$2"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; die 2 "unknown argument: $1" ;;
  esac
  shift
done
[[ -n "$MODE" ]] || { usage >&2; exit 2; }

# the area table
AREA_NAME=(); AREA_ENTRY=(); AREA_EVSUB=(); AREA_WAVE=(); AREA_TITLE=()
SRC_LINES=()
if [[ -n "${LJ_RUNNER_AREAS_FILE:-}" ]]; then
  [[ -f "$LJ_RUNNER_AREAS_FILE" ]] || die 2 "LJ_RUNNER_AREAS_FILE is not a file"
  [[ -n "${LJ_RUNNER_EVIDENCE_DIR:-}" ]] || die 2 "LJ_RUNNER_AREAS_FILE needs LJ_RUNNER_EVIDENCE_DIR too, so a test run can never overwrite the real INDEX.md"
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "$line" || "$line" == \#* ]] && continue
    SRC_LINES+=("$line")
  done < "$LJ_RUNNER_AREAS_FILE"
else
  SRC_LINES=("${DEFAULT_AREAS[@]}")
fi
for line in "${SRC_LINES[@]}"; do
  IFS='|' read -r a_name a_entry a_sub a_wave a_title a_qlim <<<"$line"
  [[ "$a_name" =~ ^[A-Za-z0-9_]+$ && "$a_entry" =~ ^[A-Za-z0-9._-]+$ && "$a_sub" =~ ^[A-Za-z0-9._-]+$ ]] || die 2 "bad area line (letters, digits, _ . - only): ${line:0:60}"
  [[ -z "${a_qlim:-}" || "$a_qlim" =~ ^[0-9]+$ ]] && (( ${a_qlim:-1} >= 1 )) || die 2 "bad quick limit in the area line (a whole number of seconds, 1 or more): ${line:0:60}"
  AREA_NAME+=("$a_name"); AREA_ENTRY+=("$a_entry"); AREA_EVSUB+=("$a_sub"); AREA_WAVE+=("${a_wave:-?}"); AREA_TITLE+=("${a_title:-}"); AREA_QLIM+=("${a_qlim:-}")
done
N=${#AREA_NAME[@]}
(( N > 0 )) || die 2 "no areas to run"

landed() { [[ -f "$TESTS_DIR/$1/run_tests.sh" ]]; }

# --------------------------------------------------------------------------- --list
if [[ "$MODE" == "list" ]]; then
  nl=0
  printf 'Week 1-2 check areas, in the fixed run order (each is tests/<area>/run_tests.sh):\n'
  printf '%3s  %-12s %-8s %-5s %-11s %s\n' '#' area entry wave landed 'covers'
  for ((i = 0; i < N; i++)); do
    if landed "${AREA_NAME[i]}"; then lv="yes"; nl=$((nl + 1)); else lv="NOT LANDED"; fi
    printf '%3d  %-12s %-8s %-5s %-11s %s\n' "$((i + 1))" "${AREA_NAME[i]}" "${AREA_ENTRY[i]}" "${AREA_WAVE[i]}" "$lv" "${AREA_TITLE[i]}"
  done
  printf 'Landed: %d of %d. A missing area is listed as NOT LANDED and does not fail a run. This listing wrote nothing.\n' "$nl" "$N"
  exit 0
fi

# --------------------------------------------------------------------------- run: preconditions
if [[ -n "${LJ_RUNNER_ACTIVE:-}" && -z "${LJ_RUNNER_AREAS_FILE:-}" ]]; then
  die 3 "REFUSED: the runner was started inside a running runner (an area's run_tests.sh must not call it on the real tree)"
fi
command -v python3 >/dev/null 2>&1 || die 3 "python3 is not installed; nothing was run"
command -v setsid >/dev/null 2>&1 || die 3 "setsid is not installed; nothing was run"
if [[ -n "$TIMEOUT_ARG" ]]; then LIMIT="$TIMEOUT_ARG"
elif [[ -n "${LJ_RUNNER_TIMEOUT_S:-}" ]]; then LIMIT="$LJ_RUNNER_TIMEOUT_S"
elif [[ "$MODE" == "quick" ]]; then LIMIT=60
else LIMIT=900; fi
[[ "$LIMIT" =~ ^[0-9]+$ ]] && (( LIMIT >= 1 )) || die 2 "the time limit must be a whole number of seconds, 1 or more"
# Quick budget, in seconds, for the whole of Part B (the 13 areas). It was 300 (the plan's "under 5 minutes"). Raised to 450 on Tue 20 Oct 2026 (follow-through round 1 of
# build week 2) because the same suite took 270 s on one container host and 374 s on the next one the session landed on (a 1.4x spread; SP3 saw 2x between two hosts the same night),
# and the 300 s mark sat on the faster host's figure. 450 is about 20 percent over the slower figure. The mark flags a slow run (OVER BUDGET in INDEX.md and the console), it
# never fails the exit code. Raise it again only with a dated note, and read a run of the quick pass against the host it ran on (lscpu, the per-area seconds).
if [[ "$MODE" == "quick" ]]; then BUDGET="${LJ_RUNNER_BUDGET_S:-450}"; else BUDGET=0; fi
[[ "$BUDGET" =~ ^[0-9]+$ ]] || die 2 "LJ_RUNNER_BUDGET_S must be a whole number"
GRACE="${LJ_RUNNER_KILL_GRACE_S:-3}"
[[ "$GRACE" =~ ^[0-9]+$ ]] || die 2 "LJ_RUNNER_KILL_GRACE_S must be a whole number"

# fail closed on redaction BEFORE anything runs
if ! py selfcheck --patterns "$PATTERNS" --lint "$LINT" 2>&1; then
  die 2 "The runner refuses to run without a working redaction scanner (D-26). Download the whole project folder, not single files."
fi
mkdir -p "$EVDIR/wp11a" 2>/dev/null && [[ -w "$EVDIR/wp11a" ]] || die 3 "the evidence folder is not writable; nothing was run"

mkdir -p "$SCRATCH" 2>/dev/null
# one runner per evidence folder at a time (two would overwrite each other's evidence)
LOCKFILE="$SCRATCH/week2-runner-$(printf '%s' "$EVDIR" | cksum | cut -d' ' -f1).lock"
if { exec {LOCKFD}>>"$LOCKFILE"; } 2>/dev/null; then   # (a bare "exec ... 2>/dev/null" would silence stderr for the rest of the run)
  flock -n "$LOCKFD" || die 3 "BUSY: another run_week2_checks.sh is already running for this evidence folder; nothing was run"
fi
TMP="$(mktemp -d "$SCRATCH/.wk2run.XXXXXX" 2>/dev/null || mktemp -d)" || die 3 "cannot create a scratch folder"
CON="$TMP/console.txt"; : > "$CON"
STATE="$TMP/areas.tsv"; : > "$STATE"
CUR_PID=""
cleanup() {
  if [[ -n "$CUR_PID" ]] && kill -0 -- "-$CUR_PID" 2>/dev/null; then kill -KILL -- "-$CUR_PID" 2>/dev/null; fi
  rm -rf "$TMP"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

CON_BAD=0
say() { printf '%s\n' "$*"; printf '%s\n' "$*" >> "$CON" 2>/dev/null || CON_BAD=1; }
install_file() { if cp "$1" "$2.tmp.$$" 2>/dev/null && mv -f "$2.tmp.$$" "$2" 2>/dev/null; then return 0; fi; rm -f "$2.tmp.$$"; return 1; }   # src dst: copy beside the target, then rename
abort() {  # CODE MESSAGE: nothing further is written, and the older outputs are removed so that none looks current
  rm -f "$EVDIR/INDEX.md" "$EVDIR/week2_summary.json" "$EVDIR/wave1_quick.txt" "$EVDIR/wp11a/console_all.txt"
  printf '%s\nINDEX.md, week2_summary.json and the console copy were not written (older copies were removed so none looks current).\n' "$2" >&2
  exit "$1"
}
mask_failed() {  # RC WHAT: python exit 2 is the fail-closed refusal; anything else is an environment problem (for example a full disk)
  [[ -s "$TMP/mask_err" ]] && cat "$TMP/mask_err" >&2
  if [[ "$1" == 2 ]]; then abort 2 "REFUSED: $2 could not be masked (fail closed)"; fi
  abort 3 "could not mask $2 (python exit $1; is the disk full?)"
}
avail_mb() {  # Avail of / in MB; LJ_DF_CMD (as in lj_guard.sh) replaces df in tests: df -P style output or a bare integer
  local out cmd
  if [[ -n "${LJ_DF_CMD:-}" ]]; then read -r -a cmd <<<"$LJ_DF_CMD"; out="$(LC_ALL=C "${cmd[@]}" 2>/dev/null)"; else out="$(LC_ALL=C df -BM -P / 2>/dev/null)"; fi
  if [[ "$out" =~ ^[[:space:]]*([0-9]+)[[:space:]]*$ ]]; then printf '%s\n' "${BASH_REMATCH[1]}"; return; fi
  printf '%s\n' "$out" | awk 'NR==2{v=$4; gsub(/[^0-9]/,"",v); print v}'
}
disp_ev() { if [[ "$EVDIR" == "$REPO/build/evidence" ]]; then printf 'build/evidence/%s' "$1"; else printf '<evidence dir>/%s' "$1"; fi; }

AV_START="$(avail_mb)"; AV_MIN="${AV_START:-0}"; [[ "$AV_START" =~ ^[0-9]+$ ]] || { AV_START="n/a"; AV_MIN=999999999; }
note_disk() { local v; v="$(avail_mb)"; if [[ "$v" =~ ^[0-9]+$ ]] && (( v < AV_MIN )); then AV_MIN="$v"; fi; }

T_START=$SECONDS
RUN_T0="$(date +%s)"
LONGER=""
if [[ "$MODE" == "quick" && -z "$TIMEOUT_ARG" && -z "${LJ_RUNNER_TIMEOUT_S:-}" ]]; then
  for ((i = 0; i < N; i++)); do [[ -n "${AREA_QLIM[i]:-}" ]] && LONGER="${LONGER:+$LONGER, }${AREA_NAME[i]} ${AREA_QLIM[i]} s"; done
fi
say "Life Journey week 1-2 checks: mode $MODE, $N areas in fixed order, per-area limit ${LIMIT} s${LONGER:+ (own limit: $LONGER)}$( ((BUDGET)) && printf ', budget %s s' "$BUDGET" )"
LOWNOTE=""
if [[ "$AV_START" =~ ^[0-9]+$ ]] && (( AV_START < 250 )); then LOWNOTE=" - BELOW the hard floor: area tests that write may be refused or stopped by the disk guard (exit 3)"; fi
say "Avail at start: ${AV_START} MB (hard floor 250 MB)${LOWNOTE}. Output is masked with scripts/redaction_patterns.json."

N_PASS=0; N_FAIL=0; N_TIMEOUT=0; N_NL=0; N_LANDED=0
RAWMAX=$((16 * 1024 * 1024))

for ((i = 0; i < N; i++)); do
  area="${AREA_NAME[i]}"; entry="${AREA_ENTRY[i]}"; sub="${AREA_EVSUB[i]}"
  idx=$((i + 1)); status=""; rc="-"; secs=0; note=""; alimit="$LIMIT"
  raw="$TMP/raw_$area.txt"; masked="$TMP/masked_$area.txt"
  if ! landed "$area"; then
    status="NOT LANDED"; N_NL=$((N_NL + 1)); note="tests/$area/run_tests.sh does not exist yet"
    printf 'NOT LANDED: tests/%s/run_tests.sh does not exist yet. This is not a failure; the runner exit code is unaffected.\n' "$area" > "$masked"
    say "$(printf '[%2d/%d] %-12s %-8s %-11s %s' "$idx" "$N" "$area" "$entry" "$status" "$note (not an error)")"
  else
    N_LANDED=$((N_LANDED + 1))
    alimit="$LIMIT"     # this area's own longer quick limit applies only to --quick and only when no explicit limit (--timeout, LJ_RUNNER_TIMEOUT_S) was given
    if [[ "$MODE" == "quick" && -z "$TIMEOUT_ARG" && -z "${LJ_RUNNER_TIMEOUT_S:-}" && -n "${AREA_QLIM[i]:-}" ]]; then alimit="${AREA_QLIM[i]}"; fi
    t0=$SECONDS; timed_out=0; flood=0; stray=0
    : > "$raw"
    (
      cd "$REPO" || exit 127
      [[ -n "${LOCKFD:-}" ]] && exec {LOCKFD}>&-   # the child must not hold the runner lock
      export LJ_RUNNER_ACTIVE=1 LJ_RUNNER_MODE="$MODE" LJ_RUNNER_EVIDENCE_DIR="$EVDIR"
      exec setsid bash "$TESTS_DIR/$area/run_tests.sh" "--$MODE"
    ) </dev/null >"$raw" 2>&1 &
    CUR_PID=$!
    deadline=$((t0 + alimit))
    while kill -0 "$CUR_PID" 2>/dev/null; do
      if (( SECONDS >= deadline )); then timed_out=1; break; fi
      sz="$(stat -c %s "$raw" 2>/dev/null || echo 0)"
      if (( sz > RAWMAX )); then flood=1; break; fi
      sleep 0.2
    done
    if (( timed_out || flood )); then
      kill -TERM -- "-$CUR_PID" 2>/dev/null
      tk=$SECONDS
      while kill -0 -- "-$CUR_PID" 2>/dev/null && (( SECONDS - tk < GRACE )); do sleep 0.2; done
      kill -KILL -- "-$CUR_PID" 2>/dev/null
    elif kill -0 -- "-$CUR_PID" 2>/dev/null; then
      for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do sleep 0.1; kill -0 -- "-$CUR_PID" 2>/dev/null || break; done   # ordinary exits get 1.5 s to finish
      if kill -0 -- "-$CUR_PID" 2>/dev/null; then stray=1; kill -KILL -- "-$CUR_PID" 2>/dev/null; fi
    fi
    wait "$CUR_PID" 2>/dev/null; rc=$?
    CUR_PID=""
    secs=$((SECONDS - t0))
    if (( timed_out )); then status="TIMEOUT"; N_TIMEOUT=$((N_TIMEOUT + 1)); note="no result in ${alimit} s; process group killed"; rc="killed"
    elif (( flood )); then status="FAIL"; N_FAIL=$((N_FAIL + 1)); note="output over 16 MB; process group killed"
    elif (( rc == 0 )); then status="PASS"; N_PASS=$((N_PASS + 1))
    else status="FAIL"; N_FAIL=$((N_FAIL + 1)); (( rc == 3 )) && note="exit 3 = environment (disk guard, lock, missing tool)"; fi
    (( stray )) && note="${note:+$note; }left background processes behind; killed"
    # mask the output (fail closed), keep the last 400 lines, and add a header
    py mask --patterns "$PATTERNS" --lint "$LINT" --hits-out "$TMP/hits_$area" < "$raw" > "$masked.body" 2> "$TMP/mask_err"; mrc=$?
    (( mrc == 0 )) || mask_failed "$mrc" "the output of area $area"
    hits="$(cat "$TMP/hits_$area" 2>/dev/null || echo 0)"
    {
      printf '# area=%s entry=%s mode=%s result=%s exit=%s seconds=%s masked_values=%s\n' "$area" "$entry" "$MODE" "$status" "$rc" "$secs" "$hits"
      lines="$(wc -l < "$masked.body")"
      (( lines > 400 )) && printf '# (earlier %d lines omitted; last 400 kept)\n' "$((lines - 400))"
      tail -n 400 "$masked.body"
    } > "$masked"
    say "$(printf '[%2d/%d] %-12s %-8s %-11s %4d s  exit %-6s %s' "$idx" "$N" "$area" "$entry" "$status" "$secs" "$rc" "$note")"
    (( hits > 0 )) && say "        masked $hits identifying-looking value(s) in this area's output"
    if [[ "$status" == "PASS" ]]; then
      last="$(grep -v '^[[:space:]]*$' "$masked.body" | tail -n 1 | cut -c1-170)"
      [[ -n "$last" ]] && say "        last line: $last"
    else
      grep -v '^[[:space:]]*$' "$masked.body" | tail -n 12 | cut -c1-170 | while IFS= read -r l; do say "        | $l"; done
    fi
    rm -f "$raw" "$masked.body"
  fi
  install_file "$masked" "$EVDIR/wp11a/area_${area}_${MODE}.txt" || abort 3 "cannot write the area log in the evidence folder (is the disk full?)"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$idx" "$area" "$entry" "$sub" "${AREA_WAVE[i]}" "$status" "$rc" "$secs" "${alimit:-$LIMIT}" "${note//$'\t'/ }" >> "$STATE"
  note_disk
done

# --------------------------------------------------------------------------- summary, outputs, gate
ELAPSED=$((SECONDS - T_START))
AV_END="$(avail_mb)"; [[ "$AV_END" =~ ^[0-9]+$ ]] || AV_END="n/a"
(( AV_MIN == 999999999 )) && AV_MIN="n/a"
EXIT=0; (( N_FAIL + N_TIMEOUT > 0 )) && EXIT=1

LINT_TEXT="not available yet"
LINT_ACTIVE=0
if [[ "${LJ_RUNNER_LINT_TEXT:-}" == "skip" ]]; then LINT_TEXT="skipped by LJ_RUNNER_LINT_TEXT=skip"
elif [[ -f "$LINT" ]] && python3 -I "$LINT" --help 2>&1 | grep -q -- '--text'; then LINT_TEXT="used"; LINT_ACTIVE=1; fi

say "----"
say "$(printf 'Areas: %d | landed %d | PASS %d | FAIL %d | TIMEOUT %d | NOT LANDED %d' "$N" "$N_LANDED" "$N_PASS" "$N_FAIL" "$N_TIMEOUT" "$N_NL")"
OVER="within"; if (( BUDGET > 0 && ELAPSED > BUDGET )); then OVER="OVER BUDGET"; fi
say "Elapsed ${ELAPSED} s$( ((BUDGET)) && printf ' against the %s s quick budget (%s)' "$BUDGET" "$OVER" )"
say "Disk: Avail ${AV_START} MB at start, ${AV_MIN} MB lowest between areas, ${AV_END} MB at end (hard floor 250 MB)"
if ! py collect --state "$STATE" --evdir "$EVDIR" --mode "$MODE" --out-index "$TMP/INDEX.md" --out-json "$TMP/week2_summary.json" \
     --run-start "$RUN_T0" --elapsed "$ELAPSED" --budget "$BUDGET" --timeout "$LIMIT" --exit-code "$EXIT" --avail-start "$AV_START" --avail-min "$AV_MIN" \
     --avail-end "$AV_END" --lint-text "$LINT_TEXT" --bash "${BASH_VERSION%%(*}" > "$TMP/collect.out" 2> "$TMP/collect.err"; then
  [[ -s "$TMP/collect.err" ]] && cat "$TMP/collect.err" >&2
  abort 3 "could not build INDEX.md (is the disk full?)"
fi
while IFS= read -r l; do say "$l"; done < "$TMP/collect.out"
say "public_lint --text: $LINT_TEXT$( ((LINT_ACTIVE)) || printf ' (the built-in masker above, driven by scripts/redaction_patterns.json, was applied)' )"
OUTS="$(disp_ev INDEX.md), $(disp_ev week2_summary.json)"
[[ "$MODE" == "quick" ]] && OUTS="$OUTS, $(disp_ev wave1_quick.txt)" || OUTS="$OUTS, $(disp_ev wp11a/console_all.txt)"
say "Writing: $OUTS, and $(disp_ev "wp11a/area_<area>_${MODE}.txt")"
say "RESULT: $( ((EXIT)) && echo FAIL || echo PASS ) (runner exit $EXIT)"

# belt and braces: mask the three finished texts again; the saved console copy must equal what was shown unless a value was caught
(( CON_BAD )) && abort 3 "could not keep a copy of the console output (is the disk full?)"
py maskmany --patterns "$PATTERNS" --lint "$LINT" --pair "$TMP/console.txt" "$TMP/final_console.txt" \
     --pair "$TMP/INDEX.md" "$TMP/final_INDEX.md" --pair "$TMP/week2_summary.json" "$TMP/final_week2_summary.json" > "$TMP/final_hits" 2> "$TMP/mask_err"; mrc=$?
(( mrc == 0 )) || mask_failed "$mrc" "the finished texts"
FH=0; while read -r h; do FH=$((FH + h)); done < "$TMP/final_hits"
(( FH > 0 )) && printf 'NOTE: %s more value(s) were masked in the saved copies than on screen\n' "$FH" >&2
if (( LINT_ACTIVE )); then
  if ! cat "$TMP/final_console.txt" "$TMP/final_INDEX.md" "$TMP/final_week2_summary.json" | python3 -I "$LINT" --text > "$TMP/lint_text.out" 2>&1; then
    abort 2 "WITHHELD: python3 -I scripts/public_lint.py --text refused the finished text (exit non-zero; it found identifying data, or its command line differs from the contract this runner assumes: text on stdin). Set LJ_RUNNER_LINT_TEXT=skip only after reading its message"
  fi
fi
install_file "$TMP/final_INDEX.md" "$EVDIR/INDEX.md" || abort 3 "cannot write INDEX.md (is the disk full?)"
install_file "$TMP/final_week2_summary.json" "$EVDIR/week2_summary.json" || abort 3 "cannot write week2_summary.json (is the disk full?)"
if [[ "$MODE" == "quick" ]]; then install_file "$TMP/final_console.txt" "$EVDIR/wave1_quick.txt" || abort 3 "cannot write wave1_quick.txt (is the disk full?)"
else install_file "$TMP/final_console.txt" "$EVDIR/wp11a/console_all.txt" || abort 3 "cannot write console_all.txt (is the disk full?)"; fi
exit "$EXIT"
