#!/usr/bin/env python3
"""test_stale.py: acceptance tests for scripts/stale_check.py (build plan WP-03 "planted-tree" and "read-only proof").

A throw-away tree shaped like the repository is built under the scratch folder. Every stale string
planted comes from scripts/stale_patterns.json (the positive samples), so this file quotes none itself.
Each test prints   RESULT PASS|FAIL <name> :: <detail>.   Exit 0 only when all pass.
  python3 -I tests/hygiene/test_stale.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "scripts" / "stale_check.py"
PATTERNS = REPO / "scripts" / "stale_patterns.json"
ALLOW = REPO / "scripts" / "stale_allowlist.json"
BASE = REPO.parent / "build-scratch"
FAILS = []


def result(name, ok, detail=""):
    print("RESULT %s %s :: %s" % ("PASS" if ok else "FAIL", name, detail if (detail or ok) else ""))
    if not ok:
        FAILS.append(name)


def run(root, *args):
    p = subprocess.run([sys.executable, "-I", str(TOOL), "--root", str(root)] + list(args), capture_output=True, text=True, errors="replace", timeout=300)
    return p.returncode, p.stdout + p.stderr


def tree_hash(root):
    h = hashlib.sha256()
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d != ".git")
        for f in sorted(fn):
            p = Path(dp) / f
            h.update(p.relative_to(root).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), "-c", "user.name=stale-test", "-c", "user.email=stale-test@example.invalid"] + list(args), capture_output=True, text=True)


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    T = Path(tempfile.mkdtemp(prefix="hyg-stale.", dir=str(BASE)))
    try:
        run_all(T)
    finally:
        shutil.rmtree(T, ignore_errors=True)
    print("\nstale tests: %d failed" % len(FAILS))
    return 1 if FAILS else 0


def run_all(T):
    doc = json.loads(PATTERNS.read_text(encoding="utf-8"))
    adoc = json.loads(ALLOW.read_text(encoding="utf-8"))
    fail_pats = [p for p in doc["patterns"] if p["severity"] == "FAIL"]
    warn_pats = [p for p in doc["patterns"] if p["severity"] == "WARN"]

    # ---------------------------------------------------------------- a tree shaped like the repository
    tree = T / "tree"
    planted_lines = []
    for p in fail_pats:
        planted_lines.append("- %s" % p["positive_samples"][0])
    # no planted FAIL sample may sit next to an allowlist context; keep them one per line, separated by prose
    body = "# planted\n\n" + "\n\nProse between the lines.\n\n".join(planted_lines) + "\n"
    write(tree, "playbooks/planted.md", body)
    write(tree, ".claude/skills/x/SKILL.md", "Skill text.\n\n" + "\n".join("Note: " + p["positive_samples"][0] for p in fail_pats[:5]) + "\n")
    write(tree, "research/q-fixtures/fix.py", "# fixture\nprint('" + fail_pats[0]["positive_samples"][0].replace("'", "") + "')\n")
    write(tree, "win/w.ps1", "Write-Host '" + fail_pats[1]["positive_samples"][0].replace("'", "") + "'\n")
    # the same strings where they must be ignored
    for rel in ["research/notes.md", "reviews/r.md", "DECISIONS.md", "ROADMAP.md", "PLAN-ON-A-PAGE.md", "CHARTER.md", "CLAUDE.md", "build/b.md",
                "scripts/stale_patterns.json", "scripts/stale_allowlist.json", "scripts/stale_baseline.json", "ops/decisions.csv", "tests/hygiene/t.md"]:
        write(tree, rel, body)
    # the allowlisted contexts, one per allowlist entry, using the entry's own positive samples
    for e in adoc["entries"]:
        rel = e["file"] if "*" not in e["file"] else "playbooks/allowed_%s.md" % e["id"]
        for k, s in enumerate(e["positive_samples"]):
            r = rel if k == 0 else rel.replace(".md", "_%d.md" % k)
            write(tree, r, "# allowed context\n" + s + "\n")

    snapshot = T / "snapshot"
    shutil.copytree(tree, snapshot)
    git(snapshot, "init", "-q")
    git(snapshot, "add", "-A")
    git(snapshot, "commit", "-q", "-m", "snapshot")
    h0, s0 = tree_hash(snapshot), git(snapshot, "status", "--porcelain").stdout

    rep = T / "report.json"
    mdp = T / "report.md"
    rc, out = run(snapshot, "--json", str(rep), "--md", str(mdp))
    result("report_mode_on_the_planted_tree_exits_1", rc == 1, "exit %d" % rc)
    report = json.loads(rep.read_text(encoding="utf-8"))
    hits = report["hits"]
    live_by_pattern = {}
    for h in hits:
        live_by_pattern.setdefault(h["pattern"], set()).add(h["file"])
    miss = [p["id"] for p in fail_pats if "playbooks/planted.md" not in live_by_pattern.get(p["id"], set())]
    result("every_FAIL_pattern_is_found_in_a_playbook_like_file", not miss, "not found: %s" % miss)
    ignored = ["research/notes.md", "reviews/r.md", "DECISIONS.md", "ROADMAP.md", "PLAN-ON-A-PAGE.md", "CHARTER.md", "CLAUDE.md", "build/b.md",
               "scripts/stale_patterns.json", "scripts/stale_allowlist.json", "scripts/stale_baseline.json", "ops/decisions.csv", "tests/hygiene/t.md"]
    bad = sorted(set(h["file"] for h in hits) & set(ignored))
    result("same_strings_in_research_md_reviews_register_build_and_own_files_are_ignored", not bad, "scanned by mistake: %s" % bad)
    result("hits_are_also_found_in_skills_fixtures_and_win_scripts",
           {".claude/skills/x/SKILL.md", "research/q-fixtures/fix.py", "win/w.ps1"} <= set(h["file"] for h in hits), "")
    allowed_files = [("playbooks/music-sound.md" if e["file"] != "*" and e["file"].endswith("music-sound.md") else None) for e in adoc["entries"]]
    leaked = [h for h in hits if "allowed" in h["file"] or h["file"] in ("playbooks/music-sound.md", "playbooks/production-scale.md")]
    result("same_strings_in_the_allowlisted_contexts_are_not_live_hits", not leaked, "live hits in allowlisted files: %s" % [(h["file"], h["pattern"]) for h in leaked][:4])
    result("allowlisted_hits_are_counted_per_entry", set(report["allowlisted_by_entry"]) == set(e["id"] for e in adoc["entries"]),
           "entries seen: %s" % sorted(report["allowlisted_by_entry"]))
    result("report_lists_every_table_4_row_S01_to_S41_and_W29", [r["row_id"] for r in report["rows"]] == ["S-%02d" % n for n in range(1, 42)] + ["W-29"], "%d rows" % len(report["rows"]))
    md = mdp.read_text(encoding="utf-8")
    result("markdown_report_has_the_required_sections",
           all(x in md for x in ["## Every Table 4 row", "## REGRESSIONS", "## WORK ORDERS", "## Not machine-checkable (prose)", "## INFO: candidate new Table 4 rows"]), "")
    result("outstanding_rows_become_work_orders_and_applied_rows_regressions",
           {w["row_id"] for w in report["work_orders"]} == {"S-01", "S-38", "S-39", "S-40"} and any(h["row_id"] == "S-05" for h in report["regressions"]), "")

    # INFO candidates are counted but never fail the check
    info_tree = T / "info"
    write(info_tree, "playbooks/i.md", "A Minecraft tour, an original voxel asset, Mojang textures, and a Christmas slot.\n")
    rc, out = run(info_tree, "--json", str(T / "info.json"))
    ij = json.loads((T / "info.json").read_text(encoding="utf-8"))
    tot = {i["id"]: i["total"] for i in ij["info_candidates"]}
    result("INFO_candidates_are_counted_and_do_not_fail_the_run", rc == 0 and tot.get("INFO.minecraft") == 1 and tot.get("INFO.voxel") == 1 and tot.get("INFO.mojang") == 1 and tot.get("INFO.holiday-placeholders") == 1, "exit %d %s" % (rc, tot))

    # strict
    rc, out = run(snapshot, "--strict")
    result("strict_mode_exits_1_and_prints_only_FAIL_lines", rc == 1 and all(l.startswith("FAIL ") or l.startswith("strict:") for l in out.strip().splitlines()), out.strip().splitlines()[-1])
    clean = T / "clean"
    write(clean, "playbooks/ok.md", "A perfectly current page about P-LOCK and SP1 at 24 fps.\n")
    rc, out = run(clean, "--strict")
    result("strict_mode_exits_0_on_a_clean_tree", rc == 0, out.strip().splitlines()[-1])
    rc, out = run(clean)
    result("report_mode_exits_0_on_a_clean_tree", rc == 0, out.strip().splitlines()[0])

    # baseline and new-only
    base = T / "base.json"
    rc, out = run(snapshot, "--baseline", "--baseline-file", str(base))
    result("baseline_writes_counts_and_locations", rc == 0 and base.exists() and json.loads(base.read_text())["counts"]["FAIL"] == report["summary"]["fail"], out.strip())
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(base))
    result("new_only_exits_0_straight_after_the_baseline", rc == 0, out.strip().splitlines()[-1])
    pl = snapshot / "playbooks" / "planted.md"
    pl.write_text("A new first line.\n" + pl.read_text(encoding="utf-8"), encoding="utf-8")
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(base))
    result("new_only_ignores_old_hits_when_line_numbers_shift", rc == 0, out.strip().splitlines()[-1])
    new_line = doc["patterns"][[p["id"] for p in doc["patterns"]].index("S-28.minus-1.5-dbtp")]["positive_samples"][0]
    with open(pl, "a", encoding="utf-8") as fh:
        fh.write("\nOne NEW stale line: %s\n" % new_line)
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(base))
    result("one_new_stale_line_makes_new_only_exit_1_and_names_only_that_line", rc == 1 and out.count("NEW FAIL") == 1 and "S-28" in out, out.strip().splitlines()[-1])
    pl2 = snapshot / "playbooks" / "newfile.md"
    pl2.write_text("Another new file: %s\n" % new_line, encoding="utf-8")
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(base))
    result("a_new_file_with_a_stale_line_is_new_too", rc == 1 and out.count("NEW FAIL") == 2, out.strip().splitlines()[-1])
    pl2.unlink()
    git(snapshot, "checkout", "-q", "--", ".")
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(base))
    result("new_only_exits_0_again_once_the_new_line_is_gone", rc == 0, out.strip().splitlines()[-1])
    rc, out = run(snapshot, "--new-only", "--baseline-file", str(T / "no-such-baseline.json"))
    result("new_only_without_a_baseline_is_a_usage_error_exit_2", rc == 2 and "--baseline" in out, out.strip()[:90])

    # read-only proof (on the snapshot: nothing else writes there)
    git(snapshot, "checkout", "-q", "--", ".")
    git(snapshot, "clean", "-fdq")
    h1, s1 = tree_hash(snapshot), git(snapshot, "status", "--porcelain").stdout
    for args in ([], ["--strict"], ["--audit-allowlist"], ["--self-test"], ["--new-only", "--baseline-file", str(base)], ["--json", str(T / "ro.json")]):
        run(snapshot, *args)
    h2, s2 = tree_hash(snapshot), git(snapshot, "status", "--porcelain").stdout
    result("read_only_git_status_and_tree_hash_unchanged_by_every_mode", h1 == h2 and s1 == s2 == "" and h0 == h1, "hash %s, status %r" % (h2[:12], s2))

    # exit 2 / 3
    badp = T / "bad_patterns.json"
    badp.write_text("{not json", encoding="utf-8")
    rc, out = run(clean, "--patterns", str(badp))
    result("invalid_pattern_file_exits_2", rc == 2, out.strip()[:90])
    rc, out = run(T / "no-such-tree")
    result("missing_tree_exits_3", rc == 3, out.strip()[:90])

    # the audit finds a dead entry
    dead = json.loads(ALLOW.read_text(encoding="utf-8"))
    dead["entries"].append({"id": "AL-dead", "register_row": "W-29", "file": "*", "rows": ["S-05"], "context_regex": "this text appears nowhere zzz", "reason": "test",
                            "positive_samples": ["x"], "negative_samples": ["y"], "window": {"before": 0, "after": 0}})
    deadp = T / "allow_dead.json"
    deadp.write_text(json.dumps(dead), encoding="utf-8")
    rc, out = run(REPO, "--audit-allowlist", "--allowlist", str(deadp))
    result("audit_allowlist_fails_on_a_dead_entry_and_names_it", rc == 1 and "AL-dead" in out and "DEAD" in out, out.strip().splitlines()[-1])


if __name__ == "__main__":
    sys.exit(main())
