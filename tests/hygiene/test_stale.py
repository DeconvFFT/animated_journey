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
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "scripts" / "stale_check.py"
PATTERNS = REPO / "scripts" / "stale_patterns.json"
ALLOW = REPO / "scripts" / "stale_allowlist.json"
REGISTER = REPO / "DECISIONS.md"
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


def run_cp1252(root, *args):
    """The tool as a Windows PowerShell capture or pipe sees it: no -I (so PYTHONIOENCODING counts) and a cp1252 stdout. Bytes in, text out."""
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    p = subprocess.run([sys.executable, str(TOOL), "--root", str(root)] + list(args), capture_output=True, env=env, timeout=300)
    return p.returncode, p.stdout.decode("cp1252", "replace") + p.stderr.decode("cp1252", "replace")


def table4_ids(register):
    """The | S-nn | ids of Table 4, read from the register itself (nothing here is a hard-coded range)."""
    ids = []
    for line in Path(register).read_text(encoding="utf-8-sig").split("\n"):
        m = re.match(r"^\| (S-[0-9]+) \|", line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


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
    scoped = sorted(set(e["file"] for e in adoc["entries"] if "*" not in e["file"]))
    leaked = [h for h in hits if "allowed" in h["file"] or h["file"] in scoped]
    result("same_strings_in_the_allowlisted_contexts_are_not_live_hits", not leaked, "live hits in allowlisted files: %s" % [(h["file"], h["pattern"]) for h in leaked][:4])
    # every entry's positive sample is planted: each entry shows up in the counts, except one that is structural AND whose sample the patterns do not hit at all (AL-4)
    seen = set(report["allowlisted_by_entry"])
    ids = set(e["id"] for e in adoc["entries"])
    missing = ids - seen
    result("allowlisted_hits_are_counted_per_entry", seen <= ids and all(e.get("structural") for e in adoc["entries"] if e["id"] in missing) and ids - missing >= set(e["id"] for e in adoc["entries"] if not e.get("structural")),
           "entries seen: %s; not seen: %s" % (sorted(seen), sorted(missing)))
    result("every_structural_entry_gives_its_reason_and_the_count_comes_from_the_file",
           all(e.get("structural_reason") for e in adoc["entries"] if e.get("structural")) and len(ids) == len(adoc["entries"]),
           "%d entries, %d structural" % (len(adoc["entries"]), sum(1 for e in adoc["entries"] if e.get("structural"))))
    # the expected rows come from the register's Table 4 (not from a range), plus W-29, in the pattern file's order
    reg_ids = table4_ids(REGISTER)
    pat_ids = [r["row_id"] for r in doc["rows"]]
    rep_ids = [r["row_id"] for r in report["rows"]]
    result("report_lists_every_table_4_row_of_the_register_and_W29", rep_ids == pat_ids and set(reg_ids) | {"W-29"} == set(rep_ids) and len(reg_ids) >= 65,
           "%d rows in the report, %d Table 4 ids in the register, missing from the report: %s" % (len(rep_ids), len(reg_ids), sorted((set(reg_ids) | {"W-29"}) - set(rep_ids))))
    md = mdp.read_text(encoding="utf-8")
    result("markdown_report_has_the_required_sections",
           all(x in md for x in ["## Every Table 4 row", "## REGRESSIONS", "## WORK ORDERS", "## Not machine-checkable (prose)", "## INFO: candidate new Table 4 rows"]), "")
    outstanding = {r["row_id"] for r in doc["rows"] if r["status"] == "outstanding"}
    result("outstanding_rows_become_work_orders_and_applied_rows_regressions",
           {w["row_id"] for w in report["work_orders"]} == outstanding and {"S-01", "S-38", "S-42", "S-61", "S-65"} <= outstanding and any(h["row_id"] == "S-05" for h in report["regressions"]),
           "%d outstanding rows" % len(outstanding))

    # INFO candidates are counted but never fail the check. Register v3 made Minecraft and the rest FAIL patterns, so the mechanism is tested with a synthetic info entry.
    result("no_info_candidates_remain_and_the_report_says_so", doc["info"] == [] and report["info_candidates"] == [] and "None today" in md, "info entries: %d" % len(doc["info"]))
    info_tree = T / "info"
    write(info_tree, "playbooks/i.md", "A candidate-only phrase: zzqx-candidate appears here.\n")
    info_pat = json.loads(PATTERNS.read_text(encoding="utf-8"))
    info_pat["info"] = [{"id": "INFO.synthetic", "suggested_row": "none", "flags": "i", "regex": "zzqx-candidate", "description": "a synthetic candidate", "positive_samples": ["zzqx-candidate"], "negative_samples": ["zzqx"]}]
    ip = T / "info_patterns.json"
    ip.write_text(json.dumps(info_pat), encoding="utf-8")
    rc, out = run(info_tree, "--patterns", str(ip), "--json", str(T / "info.json"))
    ij = json.loads((T / "info.json").read_text(encoding="utf-8"))
    tot = {i["id"]: i["total"] for i in ij["info_candidates"]}
    result("INFO_candidates_are_counted_and_do_not_fail_the_run", rc == 0 and tot.get("INFO.synthetic") == 1 and ij["summary"]["fail"] == 0, "exit %d %s" % (rc, tot))
    # the D-29 terms and the placeholder observances are FAIL now: the same text that used to be INFO fails the run and is filed under a Table 4 row
    d29_tree = T / "d29"
    write(d29_tree, "playbooks/i.md", "A Minecraft tour, an original voxel asset, Mojang textures, MagicaVoxel, Blockbench, MapartCraft and a Hanukkah slot.\n")
    rc, out = run(d29_tree, "--json", str(T / "d29.json"))
    dj = json.loads((T / "d29.json").read_text(encoding="utf-8"))
    by_pat = {}
    for h in dj["hits"]:
        by_pat[h["pattern"]] = h["row_id"]
    result("D29_terms_and_placeholder_observances_are_FAIL_not_INFO", rc == 1 and dj["info_candidates"] == [] and len(by_pat) == 7 and all(h["severity"] == "FAIL" for h in dj["hits"]),
           "exit %d, patterns %s" % (rc, sorted(by_pat)))

    # strict
    rc, out = run(snapshot, "--strict")
    result("strict_mode_exits_1_and_prints_only_FAIL_lines", rc == 1 and all(l.startswith("FAIL ") or l.startswith("strict:") for l in out.strip().splitlines()), out.strip().splitlines()[-1])
    clean = T / "clean"
    write(clean, "playbooks/ok.md", "A perfectly current page about P-LOCK and SP1 at 24 fps.\n")
    rc, out = run(clean, "--strict")
    result("strict_mode_exits_0_on_a_clean_tree", rc == 0, out.strip().splitlines()[-1])
    rc, out = run(clean)
    result("report_mode_exits_0_on_a_clean_tree", rc == 0, out.strip().splitlines()[0])

    # review r4: a Windows pipe (cp1252) must not turn the verdict into a traceback when a stale excerpt holds an arrow
    arrow = T / "arrow"
    arrow_sample = doc["patterns"][[p["id"] for p in doc["patterns"]].index("S-28.minus-1.5-dbtp")]["positive_samples"][0]
    write(arrow, "playbooks/arrow.md", "Step 4 \u2192 %s\n" % arrow_sample)
    rc, out = run_cp1252(arrow, "--strict")
    result("cp1252_pipe_strict_prints_the_FAIL_line_and_exits_1_with_no_traceback",
           rc == 1 and "FAIL S-28 playbooks/arrow.md:1" in out and "Step 4 ? " in out and "Traceback" not in out and "UnicodeEncodeError" not in out, "exit %d: %s" % (rc, out.strip().splitlines()[0] if out.strip() else "no output"))
    arrow_base = T / "arrow_base.json"
    write(T / "arrow_clean", "playbooks/ok.md", "A current page.\n")
    rc0, _o = run(T / "arrow_clean", "--baseline", "--baseline-file", str(arrow_base))
    rc, out = run_cp1252(arrow, "--new-only", "--baseline-file", str(arrow_base))
    result("cp1252_pipe_new_only_prints_the_NEW_FAIL_line_and_exits_1_with_no_traceback",
           rc0 == 0 and rc == 1 and "NEW FAIL" in out and "playbooks/arrow.md:1" in out and "Traceback" not in out and "UnicodeEncodeError" not in out, "exit %d: %s" % (rc, out.strip().splitlines()[0] if out.strip() else "no output"))
    rc, out = run_cp1252(arrow)
    result("cp1252_pipe_report_mode_exits_1_with_no_traceback", rc == 1 and "Traceback" not in out and "UnicodeEncodeError" not in out, "exit %d" % rc)

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

    # review r1: a structural entry is 'unused by design', not dead; one without a reason is invalid input (r2: the entry count is the file's own, there are three such entries)
    structural = [e["id"] for e in adoc["entries"] if e.get("structural")]
    nent = len(adoc["entries"])
    rc, out = run(REPO, "--audit-allowlist")
    by_design = [l for l in out.splitlines() if l.endswith("unused by design (structural)")]
    tagged = [l.split()[0] for l in by_design]
    # a structural entry is printed as unused by design while it suppresses nothing; one that suppresses a hit today is printed as a normal entry
    result("audit_allowlist_prints_unused_structural_entries_as_unused_by_design_and_exits_0",
           rc == 0 and "DEAD" not in out and set(tagged) <= set(structural) and "AL-4-gathering-14" in tagged
           and ("no dead entries (%d entries, %d unused by design)" % (nent, len(tagged))) in out, out.strip().splitlines()[-1])
    nor = json.loads(ALLOW.read_text(encoding="utf-8"))
    for e in nor["entries"]:
        if e.get("structural"):
            del e["structural_reason"]
    norp = T / "allow_structural_no_reason.json"
    norp.write_text(json.dumps(nor), encoding="utf-8")
    rc, out = run(REPO, "--audit-allowlist", "--allowlist", str(norp))
    result("structural_entry_without_a_reason_is_invalid_input_exit_2", rc == 2 and "structural_reason" in out, out.strip()[:100])
    unmarked = json.loads(ALLOW.read_text(encoding="utf-8"))
    for e in unmarked["entries"]:
        e.pop("structural", None)
    unp = T / "allow_unmarked.json"
    unp.write_text(json.dumps(unmarked), encoding="utf-8")
    rc, out = run(REPO, "--audit-allowlist", "--allowlist", str(unp))
    result("without_the_structural_mark_every_unused_entry_would_be_dead", rc == 1 and all(i in out for i in structural) and out.count("DEAD") >= len(structural), out.strip().splitlines()[-1])

    # review r2 (C-1): the self-test reads Table 4 from the register, so the check cannot fall behind it unnoticed
    rc, out = run(REPO, "--self-test")
    result("self_test_reads_the_register_and_passes_on_the_real_pair", rc == 0 and "register check: %d Table 4 ids" % len(table4_ids(REGISTER)) in out and "0 problems" in out, out.strip().splitlines()[-1])
    short = json.loads(PATTERNS.read_text(encoding="utf-8"))
    last_id = table4_ids(REGISTER)[-1]
    short["rows"] = [r for r in short["rows"] if r["row_id"] != last_id]
    shp = T / "patterns_missing_last_row.json"
    shp.write_text(json.dumps(short), encoding="utf-8")
    rc, out = run(REPO, "--self-test", "--patterns", str(shp))
    result("self_test_fails_when_a_table_4_id_has_no_row", rc == 1 and ("Table 4 row %s is missing" % last_id) in out, "removed %s: %s" % (last_id, out.strip().splitlines()[-1]))
    grown = REGISTER.read_text(encoding="utf-8-sig") + "\n| S-%d | a new stale value | the canonical value | somewhere | **outstanding**: Haiku |\n" % (int(last_id[2:]) + 1)
    grp = T / "register_grown.md"
    grp.write_text(grown, encoding="utf-8")
    rc, out = run(REPO, "--self-test", "--register", str(grp))
    result("self_test_fails_when_the_register_grows_a_row_the_pattern_file_lacks", rc == 1 and ("Table 4 row S-%d is missing" % (int(last_id[2:]) + 1)) in out, out.strip().splitlines()[-1])
    drift = REGISTER.read_text(encoding="utf-8-sig").replace("| S-42 |", "| S-42 |", 1)
    lines = drift.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("| S-42 |"):
            lines[i] = l.rsplit("|", 2)[0] + "| applied |"
    drp = T / "register_status_drift.md"
    drp.write_text("\n".join(lines), encoding="utf-8")
    rc, out = run(REPO, "--self-test", "--register", str(drp))
    result("self_test_fails_when_a_row_status_disagrees_with_the_register", rc == 1 and "row S-42 has status 'outstanding' but Table 4 says 'applied'" in out, out.strip().splitlines()[-1])
    orow = REGISTER.read_text(encoding="utf-8-sig") + "\n| O-85 | Sun 1 Nov | a new open question | maker | open |\n"
    orp = T / "register_o_row.md"
    orp.write_text(orow, encoding="utf-8")
    rc, out = run(REPO, "--self-test", "--register", str(orp))
    result("self_test_fails_when_the_register_grows_an_O_row_past_the_O_row_pattern", rc == 1 and "stops at O-84 but the register's last O- row is O-85" in out, out.strip().splitlines()[-1])
    rc, out = run(snapshot_for_skip := (T / "clean"), "--self-test")
    result("self_test_says_so_when_there_is_no_register_to_read", rc == 0 and "register check: SKIPPED" in out, out.strip().splitlines()[0])

    # review r2: the spellings W-29 now names fail in a playbook-like file, and their allowed negations do not
    plant = T / "w29"
    cm = "Christ" + "mas"
    lines29 = [
        "Build a Minecraft tour of her town.", "Use original voxel assets from MagicaVoxel.", "Export with Blockbench or MapartCraft; no Mojang textures.",
        "Apply the T2 rule here.", "P1, the phone master, goes by cable.", "P2, the small copy for relatives.", "Phone deliverable: P1 by cable.",
        "Week 10: Lunar New Year slot and Chhath as a constraint.", "US Thanksgiving week and Thanksgiving week rules.", "Ramadan, Ash Wednesday, Pongal and Hanukkah rows.",
        "%s and New Year as household rows." % cm, "H-1 to H-7 cover the hum cases.", "The sound note's S1/S2 source classes.",
        "The maker's own photograph of a three-dimensional murti on her shelf.", "Black; one room sound.", "Black; one true room sound.",
        "Decision 11 means moving footage.", "The her-turn conversation is on Sat 6 Mar.", "See O-85 for the answer.",
    ]
    write(plant, "playbooks/planted.md", "# planted\n\n" + "\n\n".join(lines29) + "\n")
    rc, out = run(plant, "--json", str(T / "w29.json"))
    wj = json.loads((T / "w29.json").read_text(encoding="utf-8"))
    live_lines = {h["line"] for h in wj["hits"] if h["severity"] == "FAIL"}
    silent = [l for i, l in enumerate(lines29) if (3 + 2 * i) not in live_lines]
    result("every_spelling_W29_names_fails_in_a_playbook_like_file", rc == 1 and not silent, "silent lines: %s" % silent)
    ok_tree = T / "w29ok"
    write(ok_tree, "playbooks/ok.md", "# ok\n\nThe old question about owning a game is closed: Minecraft is dropped (D-29).\n\nMinecraft was only an example of the playful feel.\n\n"
          "Chhath is not hers, so it is no constraint on the window.\n\nThe her-turn conversation is Sun 7 Mar after about 14:00; the morning of Sat 6 Mar only if she does not fast.\n\n"
          "Decision 11 is 'hindu_idiom' and decision 12 is moving footage.\n\nPH1, the phone master, goes by cable; the three-places rule holds.\n\nO-84 is the register's last row.\n")
    rc, out = run(ok_tree, "--json", str(T / "w29ok.json"))
    oj = json.loads((T / "w29ok.json").read_text(encoding="utf-8"))
    result("the_allowed_negations_and_the_patched_wordings_do_not_fail", rc == 0 and not oj["hits"] and oj["summary"]["allowlisted"] >= 3, "exit %d, live hits %s, allowlisted %d" % (rc, [(h["pattern"], h["line"]) for h in oj["hits"]], oj["summary"]["allowlisted"]))
    scoped_ok = T / "w29pclass"
    write(scoped_ok, "playbooks/pushtimarg-world.md", "R1 defines P3 as her own shelf photograph of a three-dimensional murti, and P4 as a commissioned painting.\n")
    write(scoped_ok, "playbooks/other.md", "R1 defines P3 as her own shelf photograph of a three-dimensional murti, and P4 as a commissioned painting.\n")
    rc, out = run(scoped_ok, "--json", str(T / "pclass.json"))
    pj = json.loads((T / "pclass.json").read_text(encoding="utf-8"))
    result("the_P_class_allowlist_entry_is_scoped_to_pushtimarg_world_md", rc == 1 and [h["file"] for h in pj["hits"]] == ["playbooks/other.md"], "live hits in %s" % [h["file"] for h in pj["hits"]])
    # D-29 hits are filed under the Table 4 row whose scribe owns the file
    att = T / "att"
    for rel, text in [("playbooks/format.md", "A Minecraft tour."), (".claude/skills/meaningful-game-mechanics/SKILL.md", "Minecraft assets."), ("playbooks/music-sound.md", "Minecraft's audio."),
                      ("playbooks/theatrical-delivery.md", "no Mojang assets."), ("playbooks/cinematic-quality.md", "Original voxel assets only and never the marker.\nnever a voxel marker."),
                      ("skills-staging/x-skill/SKILL.md", "A voxel asset."), ("playbooks/surprise-ops.md", "The Ramadan row."), ("playbooks/production-scale.md", "The Ramadan row."),
                      ("playbooks/film-story.md", "Black; one true room sound."), ("playbooks/gujarati-devotional-sound.md", "Black; one true room sound.")]:
        write(att, rel, text + "\n")
    rc, out = run(att, "--json", str(T / "att.json"))
    aj = json.loads((T / "att.json").read_text(encoding="utf-8"))
    got = sorted((h["file"], h["line"], h["row_id"]) for h in aj["hits"])
    want_rows = [(".claude/skills/meaningful-game-mechanics/SKILL.md", 1, "S-45"), ("playbooks/cinematic-quality.md", 1, "S-54"), ("playbooks/cinematic-quality.md", 2, "S-42"), ("playbooks/film-story.md", 1, "S-51"),
                 ("playbooks/format.md", 1, "S-44"), ("playbooks/gujarati-devotional-sound.md", 1, "S-63"), ("playbooks/music-sound.md", 1, "S-49"), ("playbooks/production-scale.md", 1, "S-61"),
                 ("playbooks/surprise-ops.md", 1, "S-56"), ("playbooks/theatrical-delivery.md", 1, "S-48"), ("skills-staging/x-skill/SKILL.md", 1, "S-50")]
    result("hits_are_filed_under_the_table_4_row_that_owns_the_file", got == sorted(want_rows), "got %s" % [g for g in got if g not in want_rows])

    # review r1: S-05.ring-1 no longer fires on ordinary words that contain 'ring 1'
    noise = T / "noise"
    write(noise, "playbooks/words.md", 'The method "originated in Persia during 13th century".\nBhavnagar spring 11.6 m at the top of the tide.\nStory 12 hours, gathering 14 hours, reserve 15.\n')
    write(noise, "playbooks/production-scale.md", "Story takes 12 hours, gathering 14, the risk reserve 15\n")
    rc, out = run(noise, "--json", str(T / "noise.json"))
    nj = json.loads((T / "noise.json").read_text(encoding="utf-8"))
    result("S05_ring_1_does_not_fire_on_during_13th_spring_11_6_or_gathering_14", rc == 0 and not [h for h in nj["hits"] if h["pattern"] == "S-05.ring-1"], "exit %d, %d hit(s)" % (rc, len(nj["hits"])))
    write(noise, "playbooks/rings.md", "Set the rings: Ring 1 is the co-keeper.\n")
    rc, out = run(noise, "--json", str(T / "noise2.json"))
    nj = json.loads((T / "noise2.json").read_text(encoding="utf-8"))
    result("S05_ring_1_still_fires_on_the_capitalised_label", [h["file"] for h in nj["hits"] if h["pattern"] == "S-05.ring-1"] == ["playbooks/rings.md"], "")


if __name__ == "__main__":
    sys.exit(main())
