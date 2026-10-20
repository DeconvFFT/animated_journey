#!/usr/bin/env python3
"""test_lint.py: acceptance tests for scripts/public_lint.py (build plan WP-03 "public_lint" lines).

A throw-away git repository is built under the scratch folder (never in the repo). Every bad string
is assembled from fragments HERE, so this file itself stays clean (python3 -I scripts/public_lint.py --paths
tests/hygiene must pass). Each test prints   RESULT PASS|FAIL <name> :: <detail>   and the run exits 0 only
when all pass.
  python3 -I tests/hygiene/test_lint.py [--quick]     (--quick skips the 2 MB blob and the mutation test)
  python3 -I tests/hygiene/test_lint.py --force-added-only     (just the force_added_ok cases; about 15 s)
It also drives the three checks that go red on a force-added ignored file (public_lint.py, build/run_all_checks.sh repo.gitignore_coverage and
tests/integration/run_checks.py hygiene.no_ignored_file_tracked_or_staged) in scratch copies of the repository, against the exact-path force_added_ok list
of scripts/public_lint.config.json (force_added_cases below; package s1-force-added-ok).
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LINT = REPO / "scripts" / "public_lint.py"
BASE = REPO.parent / "build-scratch"
QUICK = "--quick" in sys.argv
FORCE_ONLY = "--force-added-only" in sys.argv       # only the force_added_ok cases below (run_tests.sh --quick runs just these; --all runs them inside the whole file)
FAILS = []


def result(name, ok, detail=""):
    print("RESULT %s %s :: %s" % ("PASS" if ok else "FAIL", name, detail if (detail or ok) else ""))
    if not ok:
        FAILS.append(name)


def run(root, *args, timeout=300, cwd=None):
    p = subprocess.run([sys.executable, "-I", str(LINT), "--root", str(root)] + list(args), capture_output=True, text=True, errors="replace", timeout=timeout, cwd=cwd)
    return p.returncode, p.stdout + p.stderr


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), "-c", "user.name=lint-test", "-c", "user.email=lint-test@example.invalid"] + list(args),
                          capture_output=True, text=True, errors="replace")


def tree_hash(root):
    h = hashlib.sha256()
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d != ".git")
        for f in sorted(fn):
            p = Path(dp) / f
            h.update(p.relative_to(root).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def write(root, rel, text, mode="w"):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        p.write_bytes(text)
    else:
        p.write_text(text, encoding="utf-8")
    return p


def png_bytes(total=None):
    """A valid one-pixel PNG; with TOTAL, padded with a private ancillary chunk to exactly that many bytes."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    body = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(b"\x00\x10\x20\x30"))
    end = chunk(b"IEND", b"")
    pad = b"" if total is None else chunk(b"zzZz", b"\x00" * (total - len(body) - len(end) - 12))
    return body + pad + end


def force_added_cases(T):
    """The exact-path force_added_ok list (package s1-force-added-ok). Three checks go red on a file that .gitignore ignores but git tracks or has staged (git add -f):
    scripts/public_lint.py in diff mode (ignored-staged), build/run_all_checks.sh repo.gitignore_coverage (the python heredoc is cut out of the script and run as it is) and
    tests/integration/run_checks.py hygiene.no_ignored_file_tracked_or_staged (the real driver, copied into the scratch repository and run with --only). Each runs in a
    throw-away repository under the scratch folder (never in this repo's index). The same three claims for each: a listed PNG force-added passes; an unlisted ignored file
    force-added fails; a listed path that grows to 200,000 bytes (or stops being a PNG) fails."""
    real_cfg_path = REPO / "scripts" / "public_lint.config.json"
    real_cfg = json.loads(real_cfg_path.read_text(encoding="utf-8"))
    entries = real_cfg.get("force_added_ok", [])
    card1, card2 = entries[0]["path"], entries[1]["path"]
    other = "research/craft-motion-fixtures/media/ch01_s03.png"             # same folder, same extension, NOT on the list
    sh_text = (REPO / "build" / "run_all_checks.sh").read_text(encoding="utf-8")
    m = re.search(r"cat > \"\$REPO_PY_SRC\" <<'PYEOF'\n(.*?)\nPYEOF\n", sh_text, re.S)
    result("force_added_the_repo_checks_python_can_be_cut_out_of_run_all_checks_sh", bool(m) and "def gitignore()" in m.group(1), "heredoc found" if m else "no heredoc")
    if not m:
        return
    repo_py = T / "repo_checks_cut_from_run_all_checks.py"
    repo_py.write_text(m.group(1) + "\n", encoding="utf-8")
    n = [0]

    def make_repo(cfg_text=None):
        n[0] += 1
        r = T / ("fa%d" % n[0])
        r.mkdir()
        git(r, "init", "-q")
        shutil.copy(REPO / ".gitignore", r / ".gitignore")
        (r / "scripts").mkdir()
        shutil.copy(LINT, r / "scripts" / "public_lint.py")
        (r / "scripts" / "public_lint.config.json").write_text(cfg_text if cfg_text is not None else real_cfg_path.read_text(encoding="utf-8"), encoding="utf-8")
        (r / "tests" / "integration").mkdir(parents=True)
        shutil.copy(REPO / "tests" / "integration" / "run_checks.py", r / "tests" / "integration" / "run_checks.py")
        for e in entries:                                                  # the reviews the list cites are files of the repository
            write(r, e["review"], "placeholder for the cited review\n")
        write(r, "docs/readme.md", "# A clean page\n")
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "baseline")
        return r

    def add_force(r, rel, data):
        write(r, rel, data)
        git(r, "add", "-f", "--", rel)

    def lint_rc(r, *extra):
        return run(r, *extra)

    def gi_rc(r):
        p_ = subprocess.run([sys.executable, "-I", str(repo_py), "gitignore"], cwd=str(r), capture_output=True, text=True, errors="replace", timeout=120)
        return p_.returncode, p_.stdout + p_.stderr

    def hy_line(r):
        ev = T / ("ev%d" % n[0])
        p_ = subprocess.run([sys.executable, "-I", "-B", str(r / "tests" / "integration" / "run_checks.py"), "--mode", "quick", "--only", "hygiene.no_ignored_file_tracked_or_staged",
                             "--evidence", str(ev), "--work", str(ev / "work")], cwd=str(r), capture_output=True, text=True, errors="replace", timeout=180)
        line = next((l for l in (p_.stdout + p_.stderr).splitlines() if "hygiene.no_ignored_file_tracked_or_staged" in l and l.split()[0] in ("PASS", "FAIL")), (p_.stdout + p_.stderr)[-300:])
        return p_.returncode, line

    def all_three(r, cfg=None):
        """(public_lint default mode, public_lint --staged, gitignore_coverage, hygiene.no_ignored_file_tracked_or_staged), each as (exit code, output). CFG: a config file for the lint run
        (the other two read the scripts/public_lint.config.json of the scratch repository)."""
        extra = ["--config", str(cfg)] if cfg else []
        a = lint_rc(r, *extra)
        b = lint_rc(r, "--staged", *extra)
        c = gi_rc(r)
        d = hy_line(r)
        return a, b, c, d

    # --- 0. nothing force-added: all three clean on the baseline
    r = make_repo()
    (a, b, c, d) = all_three(r)
    result("force_added_baseline_scratch_repository_is_clean_in_all_three_checks", a[0] == 0 and b[0] == 0 and c[0] == 0 and d[0] == 0, "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))

    # --- 1. a listed PNG force-added passes all three
    r = make_repo()
    add_force(r, card1, png_bytes())
    (a, b, c, d) = all_three(r)
    ls = [l for l in a[1].splitlines() if "force-added-ok" in l and card1 in l]
    result("force_added_listed_png_passes_public_lint_diff_mode_and_is_shown_as_a_NOTE", a[0] == 0 and len(ls) == 1 and "1 suppressed by the config allow list" in a[1] and "ignored-staged" not in a[1], "exit %d; %s" % (a[0], (ls[0] if ls else a[1].strip().splitlines()[-1])[:140]))
    result("force_added_listed_png_passes_public_lint_staged_mode", b[0] == 0 and "ignored-staged" not in b[1], "exit %d" % b[0])
    result("force_added_listed_png_passes_gitignore_coverage_of_run_all_checks_sh", c[0] == 0 and "gitignore_coverage: ok" in c[1] and "1 force-added and reviewed" in c[1], "exit %d: %s" % (c[0], c[1].strip().splitlines()[-1]))
    result("force_added_listed_png_passes_hygiene_no_ignored_file_tracked_or_staged", d[0] == 0 and d[1].startswith("PASS") and "1 reviewed force-add(s) on force_added_ok" in d[1], "exit %d: %s" % (d[0], d[1][:150]))
    git(r, "commit", "-q", "-m", "the card goes in")
    (a, b, c, d) = all_three(r)
    result("force_added_listed_png_still_passes_all_three_once_committed", a[0] == 0 and c[0] == 0 and d[0] == 0, "lint %d, gitignore_coverage %d, hygiene %d" % (a[0], c[0], d[0]))
    ra = lint_rc(r, "--no-allow")
    result("force_added_no_allow_ignores_the_list_and_flags_the_card_again", ra[0] == 1 and "ignored-staged" in ra[1] and card1 in ra[1], "exit %d" % ra[0])

    # --- 2. both listed cards, then an unlisted PNG in the same folder: exactly that one fails, in all three
    r = make_repo()
    add_force(r, card1, png_bytes())
    add_force(r, card2, png_bytes())
    (a, b, c, d) = all_three(r)
    result("force_added_both_listed_cards_pass_all_three", a[0] == 0 and b[0] == 0 and c[0] == 0 and d[0] == 0 and "2 suppressed by the config allow list" in a[1], "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))
    add_force(r, other, png_bytes())
    (a, b, c, d) = all_three(r)
    ls = [l for l in a[1].splitlines() if l.startswith("FINDING") and "ignored-staged" in l]
    result("force_added_unlisted_ignored_png_fails_public_lint_diff_mode_alone", a[0] == 1 and len(ls) == 1 and other in ls[0] and "does not list it" in ls[0], "exit %d; %s" % (a[0], ls[0][:150] if ls else a[1].strip().splitlines()[-1]))
    result("force_added_unlisted_ignored_png_fails_public_lint_staged_mode", b[0] == 1 and other in b[1], "exit %d" % b[0])
    tb = [l for l in c[1].splitlines() if "TRACKED BUT IGNORED" in l]
    result("force_added_unlisted_ignored_png_fails_gitignore_coverage_alone", c[0] == 1 and len(tb) == 1 and other in tb[0] and "gitignore_coverage: FAIL" in c[1] and "2 force-added and reviewed" in c[1], "exit %d; %s" % (c[0], tb[0][:120] if tb else c[1].strip().splitlines()[-1]))
    result("force_added_unlisted_ignored_png_fails_hygiene_no_ignored_file_tracked_or_staged_alone", d[0] == 1 and d[1].startswith("FAIL") and other in d[1] and card1 not in d[1] and card2 not in d[1], "exit %d: %s" % (d[0], d[1][:150]))

    # --- 3. other ignored files (a mov, a jpg under media/) force-added: not listed, so fail in all three
    r = make_repo()
    add_force(r, "clip.mov", b"mov")
    add_force(r, "media/not_a_card.jpg", b"\xff\xd8\xff\xe0" + b"x" * 64)
    (a, b, c, d) = all_three(r)
    result("force_added_unlisted_mov_and_jpg_fail_all_three", a[0] == 1 and b[0] == 1 and c[0] == 1 and d[0] == 1 and "clip.mov" in c[1] and "media/not_a_card.jpg" in d[1], "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))

    # --- 4. a listed path that grows: 199,999 bytes passes, 200,000 fails (index copy), and a working-tree-only growth fails too
    r = make_repo()
    add_force(r, card1, png_bytes(199_999))
    (a, b, c, d) = all_three(r)
    result("force_added_listed_png_of_199999_bytes_passes_all_three", a[0] == 0 and b[0] == 0 and c[0] == 0 and d[0] == 0, "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))
    add_force(r, card1, png_bytes(200_000))
    (a, b, c, d) = all_three(r)
    ls = [l for l in a[1].splitlines() if l.startswith("FINDING") and "ignored-staged" in l]
    result("force_added_listed_png_grown_to_200000_bytes_fails_public_lint_with_the_reason", a[0] == 1 and b[0] == 1 and len(ls) == 1 and "200,000 bytes" in ls[0] and "200 KB" in ls[0], "exit %d; %s" % (a[0], ls[0][:170] if ls else ""))
    result("force_added_listed_png_grown_to_200000_bytes_fails_gitignore_coverage", c[0] == 1 and "TRACKED BUT IGNORED" in c[1] and "200 KB" in c[1], "exit %d" % c[0])
    result("force_added_listed_png_grown_to_200000_bytes_fails_hygiene_no_ignored_file_tracked_or_staged", d[0] == 1 and d[1].startswith("FAIL") and "200 KB" in d[1], "exit %d: %s" % (d[0], d[1][:150]))
    r = make_repo()
    add_force(r, card1, png_bytes())
    write(r, card1, png_bytes(400_000))                                   # grown on disk, not re-added: a later `git commit -a` would carry it
    (a, b, c, d) = all_three(r)
    result("force_added_listed_png_grown_in_the_working_tree_only_fails_all_three", a[0] == 1 and c[0] == 1 and d[0] == 1 and "working-tree copy" in a[1], "lint %d, gitignore_coverage %d, hygiene %d" % (a[0], c[0], d[0]))

    r = make_repo()
    add_force(r, card1, png_bytes(300_000))
    write(r, card1, png_bytes())                                          # the working-tree copy is small again, but the index copy (what `git commit` takes) is not
    (a, b, c, d) = all_three(r)
    result("force_added_listed_png_whose_index_copy_is_over_200_kb_fails_all_three_even_if_the_file_on_disk_is_small", a[0] == 1 and b[0] == 1 and c[0] == 1 and d[0] == 1 and "index copy" in a[1], "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))

    # --- 5. a listed path that is not a PNG (text or a JPEG renamed), or a symbolic link, fails all three
    r = make_repo()
    add_force(r, card1, b"\xff\xd8\xff\xe0" + b"j" * 100)
    (a, b, c, d) = all_three(r)
    result("force_added_listed_path_holding_a_jpeg_fails_all_three", a[0] == 1 and c[0] == 1 and d[0] == 1 and "not a PNG image" in a[1], "lint %d, gitignore_coverage %d, hygiene %d" % (a[0], c[0], d[0]))
    r = make_repo()
    add_force(r, card1, b"\x89PNG\r\n\x1a\n" + b"\x00" * 40)             # the signature alone, with no IHDR chunk, is not a PNG
    (a, b, c, d) = all_three(r)
    result("force_added_listed_path_with_only_the_png_signature_fails_all_three", a[0] == 1 and c[0] == 1 and d[0] == 1, "lint %d, gitignore_coverage %d, hygiene %d" % (a[0], c[0], d[0]))

    # --- 6. the list itself: a glob, a folder, a path with no review, a review that is not in the repository. Never allowed; the lint exits 2 on any run
    def cfg_with(mut):
        c_ = json.loads(real_cfg_path.read_text(encoding="utf-8"))
        mut(c_["force_added_ok"])
        return json.dumps(c_, indent=1)
    bad_lists = (
        ("a_glob", lambda e: e[0].__setitem__("path", "research/craft-motion-fixtures/media/*.png"), "glob"),
        ("a_folder", lambda e: e[0].__setitem__("path", "research/craft-motion-fixtures/media/"), "plain repo-relative file path"),
        ("a_path_that_climbs_out", lambda e: e[0].__setitem__("path", "research/../media/ch01_s01.png"), "plain repo-relative file path"),
        ("a_non_png_path", lambda e: e[0].__setitem__("path", "research/craft-motion-fixtures/media/ch01_s01.jpg"), ".png"),
        ("an_entry_without_a_reason", lambda e: e[0].pop("reason"), "reason"),
        ("an_entry_without_a_review", lambda e: e[0].pop("review"), "review"),
        ("the_same_path_twice", lambda e: e.append(dict(e[0])), "listed twice"),
    )
    for label, mut, word in bad_lists:
        cfg_text = cfg_with(mut)
        r = make_repo(cfg_text)
        add_force(r, card1, png_bytes())
        add_force(r, card2, png_bytes())
        planted = T / ("cfg_%s.json" % label)
        planted.write_text(cfg_text, encoding="utf-8")
        rl = lint_rc(r, "--config", str(planted))
        c = gi_rc(r)
        d = hy_line(r)
        result("force_added_list_with_%s_is_refused_by_all_three" % label, rl[0] == 2 and rl[1].startswith("USAGE: the lint config's force_added_ok list is not valid") and word in rl[1] and c[0] == 1 and "FORCE_ADDED_OK INVALID" in c[1] and d[0] == 1 and d[1].startswith("FAIL"),
               "lint %d: %s; gitignore_coverage %d; hygiene %d" % (rl[0], rl[1].strip()[:110], c[0], d[0]))
    r = make_repo(cfg_with(lambda e: e[0].__setitem__("review", "reviews/build/no-such-review.md")))
    add_force(r, card1, png_bytes())
    c = gi_rc(r)
    d = hy_line(r)
    result("force_added_list_citing_a_review_that_is_not_in_the_repository_fails_gitignore_coverage_and_hygiene", c[0] == 1 and "the review it cites is not a file" in c[1] and d[0] == 1, "gitignore_coverage %d; hygiene %d" % (c[0], d[0]))
    empty_text = cfg_with(lambda e: e.clear())
    r = make_repo(empty_text)
    (T / "cfg_empty_list.json").write_text(empty_text, encoding="utf-8")
    add_force(r, card1, png_bytes())
    (a, b, c, d) = all_three(r, T / "cfg_empty_list.json")
    result("force_added_empty_list_allows_nothing_in_any_of_the_three", a[0] == 1 and b[0] == 1 and c[0] == 1 and d[0] == 1, "lint %d, staged %d, gitignore_coverage %d, hygiene %d" % (a[0], b[0], c[0], d[0]))

    # --- 7. the real list and the real cards (when they are on disk) meet the rule today
    spec = importlib.util.spec_from_file_location("lj_public_lint_for_tests", str(LINT))
    lint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint)
    probs = lint.force_added_config_problems(real_cfg, REPO)
    result("force_added_real_list_is_valid_cites_reviews_that_exist_and_holds_exactly_the_two_cards",
           not probs and [e["path"] for e in entries] == ["research/craft-motion-fixtures/media/ch01_s01.png", "research/craft-motion-fixtures/media/ch01_s02.png"], "; ".join(probs) or "2 entries")
    present = [e["path"] for e in entries if (REPO / e["path"]).is_file()]
    if present:
        verdicts = [lint.force_added_check(REPO, real_cfg, rel_) for rel_ in present]
        result("force_added_real_cards_on_disk_are_pngs_under_200_kb", all(ok_ for ok_, _ in verdicts), "; ".join("%s %d bytes -> %s" % (rel_.rsplit("/", 1)[-1], (REPO / rel_).stat().st_size, "ok" if v[0] else v[1]) for rel_, v in zip(present, verdicts)))
    else:
        print("SKIPPED force_added_real_cards_on_disk_are_pngs_under_200_kb :: the two cards are not on disk in this clone")


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    T = Path(tempfile.mkdtemp(prefix="hyg-lint.", dir=str(BASE)))
    try:
        if FORCE_ONLY:
            force_added_cases(T)
        else:
            run_all(T)
    finally:
        shutil.rmtree(T, ignore_errors=True)
    print("\nlint tests: %d failed" % len(FAILS))
    return 1 if FAILS else 0


def run_all(T):
    # ---------------------------------------------------------------- the throw-away repository
    root = T / "repo"
    root.mkdir()
    git(root, "init", "-q")
    shutil.copy(REPO / ".gitignore", root / ".gitignore")
    # The real .gitignore now carries the Q-3 backstop for raw PC reports. This throw-away repository models a clone WITHOUT it, so
    # the tests below keep proving the second belt: the lint refuses those names by path even where git would not have hidden them.
    gi_lines = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
    q3 = ("pc_report*.json", "colour_patch_pc*.json", "maker-pc*.json")
    (root / ".gitignore").write_text("\n".join(l for l in gi_lines if l.strip() not in q3) + "\n", encoding="utf-8")
    # the maker's clone must ignore the local deny list (the orchestrator adds the line, report F-6); the lint now says so when it does not (tested below)
    with open(root / ".gitignore", "a", encoding="utf-8") as fh:
        fh.write("\nscripts/public_lint.deny.local.txt\n")
    write(root, "docs/clean.md", "# A clean page\n\nNothing identifying here. Version 6.1.1 and 31.0.15." + "5222 and 192.0." + "2.1 and /home/" + "user/x.\n")
    shutil.copytree(REPO / "tests" / "win" / "fixtures", root / "tests" / "win" / "fixtures")
    write(root, "ops/GATHER.md", "# Gather\nPlain list.\n")
    write(root, "playbooks/old.md", "An existing playbook that mentions a Mughal garden (INFO only for the theme guard).\n")
    write(root, "scripts/keep.txt", "x\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "baseline")

    rc, out = run(root)
    result("clean_tree_passes_default_mode", rc == 0 and "0 identifying-data finding" in out, out.strip().splitlines()[-1] if out.strip() else "")
    rc, out = run(root, "--all")
    result("clean_tree_and_synthetic_fixtures_pass_whole_tree_audit", rc == 0, out.strip().splitlines()[-1])
    notes = [l for l in out.splitlines() if l.startswith("NOTE")]
    result("fixture_65_hex_is_a_note_not_a_failure", len(notes) >= 1 and rc == 0, "%d fixture note(s)" % len(notes))

    # ---------------------------------------------------------------- plant one file per category
    planted = {
        "docs/p_email.md": ("identifying", "email", "contact jane.doe" + "@" + "mailbox-test.io today\n", "jane.doe" + "@" + "mailbox-test.io"),
        "docs/p_ip.md": ("identifying", "ipv4", "the server is at 84.1" + "12.9.200 now\n", "84.1" + "12.9.200"),
        "docs/p_mac.md": ("identifying", "mac", "adapter 3C:52:" + "82:1A:9F:07 here\n", "3C:52:" + "82:1A:9F:07"),
        "docs/p_winpath.md": ("identifying", "profile_path_windows", "saved to C:" + "\\Users\\" + "jsample" + "\\Desktop\\x\n", "jsample"),
        "docs/p_winpath_json.md": ("identifying", "profile_path_windows", "\"p\": \"C:" + "\\\\Users\\\\" + "jsample" + "\\\\x\"\n", "jsample"),
        "docs/p_linpath.md": ("identifying", "profile_path_linux", "saved to /home/" + "jsample" + "/work\n", "jsample"),
        "docs/p_token.md": ("identifying", "token_shape", "token gh" + "p_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8 end\n", "gh" + "p_a1B2"),
        "docs/p_guid.md": ("identifying", "guid_serial", "id 3f2504e0-" + "4f89-11d3-" + "9a0c-0305e82c3301 end\n", "3f2504e0-" + "4f89"),
        "docs/p_hex65.md": ("identifying", "guid_serial", "hash " + hashlib.sha256(b"a").hexdigest() + "a end\n", hashlib.sha256(b"a").hexdigest()[:12]),
        "docs/p_handle.md": ("identifying", "handle", "follow @" + "invented_user" + " for news\n", "@" + "invented_user"),
        "data/pc_report.json": ("denylist", "raw_pc_report", "{}\n", None),
        "data/colour_patch_pc_1.json": ("denylist", "raw_pc_report", "{}\n", None),
        "deep/er/maker-pc.json": ("denylist", "raw_pc_report", "{}\n", None),
    }
    for rel, (_k, _c, text, _h) in planted.items():
        write(root, rel, text)
    write(root, "docs/p_nul.txt", b"abc\x00def\x00ghi" * 20)
    write(root, "docs/p_ok_sha256.md", "sha256 " + hashlib.sha256(b"abc").hexdigest() + " fine\n")
    write(root, "docs/p_ok_docips.md", "docs 192.0." + "2.1, 198.51." + "100.7, 203.0." + "113.9 and 127.0." + "0.1 and v 10.0.22631.4317 and 23.40.27." + "06\n")
    write(root, "docs/p_ok_placeholders.md", "paths /home/user/x and /home/user/build-scratch/y and <scratch>/z and C:\\Users\\<user>\\AppData and %USERPROFILE%\\x\n")
    write(root, "docs/p_ok_email_reserved.md", "write to someone" + "@" + "example.org\n")
    write(root, "docs/p_ok_splat.md", "In PowerShell, `Invoke-Thing @" + "params` splats, and:\n\n```powershell\nInvoke-Other @" + "args -Verbose\n```\n")
    write(root, "tool_splat.ps1", "Invoke-Thing @" + "params\n")
    write(root, "tests/win/fixtures/pc_report_synthetic.json", "{\"synthetic\": true}\n")
    write(root, "docs/p_otherhome.md", "work in /home/" + "maker2" + "/work\n")
    write(root, "docs/p_scratch_ok.md", "run in /home/user/build-scratch/pwsh\n")
    write(root, "media_clip.mov", "tiny\n")
    git(root, "add", "-f", "media_clip.mov")
    write(root, "scripts/public_lint.deny.local.txt", "# invented names for the test\nZorba" + "zan\n")
    write(root, "docs/p_deny.md", "thanks to zorba" + "zan for the help\n")
    if not QUICK:
        write(root, "docs/p_big.txt", ("x" * 99 + "\n") * (2 * 10000 + 500))

    before_hash = tree_hash(root)
    before_status = git(root, "status", "--porcelain").stdout
    rc, out = run(root)
    after_hash = tree_hash(root)
    after_status = git(root, "status", "--porcelain").stdout
    result("planted_tree_exits_2_identifying_data", rc == 2, "exit %d" % rc)
    for rel, (kind, cat, _t, hit) in planted.items():
        ls = [l for l in out.splitlines() if l.startswith("FINDING") and (" " + rel) in l]
        ok = any(kind in l and cat in l for l in ls)
        result("flags_%s_in_%s" % (cat, rel.replace("/", "_")), ok, ls[0] if ls else "no finding line for the file")
    ls = [l for l in out.splitlines() if "docs/p_nul.txt" in l]
    result("flags_NUL_byte", any("binary" in l and "nul_byte" in l for l in ls), ls[0] if ls else "")
    ls = [l for l in out.splitlines() if "media_clip.mov" in l]
    result("flags_staged_mov_that_gitignore_blocks", any("ignored-staged" in l for l in ls), ls[0] if ls else "")
    if not QUICK:
        ls = [l for l in out.splitlines() if "docs/p_big.txt" in l]
        result("flags_2MB_blob", any("size" in l and "over_1mb" in l for l in ls), ls[0] if ls else "")
    result("local_deny_file_itself_is_never_scanned_or_printed", not any("public_lint.deny.local.txt" in l for l in out.splitlines()), "")
    ls = [l for l in out.splitlines() if "docs/p_deny.md" in l]
    result("flags_local_deny_word_masked", any("local_deny" in l and "hit=Zo" in l for l in ls) or any("local_deny" in l and "hit=zo" in l for l in ls), ls[0] if ls else "")
    ls = [l for l in out.splitlines() if "docs/p_otherhome.md" in l]
    result("home_path_under_another_name_is_flagged", any("profile_path_linux" in l for l in ls), ls[0] if ls else "")
    for rel in ["docs/p_ok_sha256.md", "docs/p_ok_docips.md", "docs/p_ok_placeholders.md", "docs/p_ok_email_reserved.md", "docs/p_ok_splat.md", "tool_splat.ps1",
                "docs/p_scratch_ok.md", "tests/win/fixtures/pc_report_synthetic.json", "docs/clean.md"]:
        ls = [l for l in out.splitlines() if l.startswith("FINDING") and (" " + rel) in l]
        result("passes_%s" % rel.replace("/", "_"), not ls, ls[0] if ls else "no finding")
    # masking: no planted value is ever printed whole
    leaks = [v for (_k, _c, _t, v) in planted.values() if v and len(v) > 4 and v in out]
    leaks += [w for w in ("jane.doe", "invented_user", "jsample", "zorba" + "zan", "Zorba" + "zan") if w in out]
    result("output_is_masked_no_planted_value_printed_in_full", not leaks, "leaked: %s" % [x[:3] + "..." for x in leaks])
    result("tree_hash_and_git_status_unchanged_by_the_lint", before_hash == after_hash and before_status == after_status, "read-only")

    # --paths mode flags the same without git
    rc, out = run(root, "--paths", "docs/p_email.md", "docs/p_ok_sha256.md")
    result("paths_mode_flags_a_file_and_passes_another", rc == 2 and "docs/p_email.md" in out and "p_ok_sha256" not in out.replace("2 file(s)", ""), out.strip().splitlines()[-1])
    rc, out = run(root, "--staged")
    result("staged_mode_looks_only_at_the_index", "p_email" not in out and "media_clip.mov" in out, out.strip().splitlines()[-1])
    git(root, "add", "docs/p_email.md")
    rc, out = run(root, "--staged")
    result("staged_mode_sees_a_file_once_it_is_staged", "docs/p_email.md" in out and rc == 2, out.strip().splitlines()[-1])
    git(root, "reset", "-q", "docs/p_email.md")

    # diff mode: a changed tracked file is judged on its ADDED lines only
    old = (root / "docs" / "clean.md").read_text(encoding="utf-8")
    (root / "docs" / "clean.md").write_text(old + "an added line with ad" + "min" + "@" + "mailbox-test.io\n", encoding="utf-8")
    rc, out = run(root)
    ls = [l for l in out.splitlines() if "docs/clean.md" in l]
    result("diff_mode_reports_the_added_line_with_its_line_number", any("email" in l and "docs/clean.md:4" in l for l in ls), ls[0] if ls else "")
    (root / "docs" / "clean.md").write_text(old, encoding="utf-8")

    # the local deny list must never be tracked or staged
    git(root, "add", "-f", "scripts/public_lint.deny.local.txt")
    rc, out = run(root)
    result("tracked_or_staged_local_deny_file_is_refused", rc == 2 and any("local_deny_file" in l and "public_lint.deny.local.txt" in l for l in out.splitlines()), next((l for l in out.splitlines() if "local_deny_file" in l), "no finding")[:140])
    git(root, "reset", "-q", "scripts/public_lint.deny.local.txt")

    # ---------------------------------------------------------------- theme guard
    scene = "// scene one\nconst a = 'Mughal garden at dusk';\nconst b = 'Christmas card';\nconst c = 'crossfade to the next shot'; // across, Churchill\nconst d = 'Taj Mahal';\n"
    write(root, "pipeline/scenes/scene1.js", scene)
    write(root, "pipeline/scenes/scene_ok.js", "const t = 'crossfade'; // across the frame, a Churchill-sized title\n")
    # Rule statements are NOTEs only in prose (.md) and only when the cue (no, never, not, excluded, out of scope ...) comes
    # within 40 characters BEFORE the keyword (review r1, C-1). Bare 'out', 'no' and 'without' after or far from the keyword are animation words.
    write(root, "skills-staging/rules/scene_rules.md", "No Mughal or other Islamic motifs and no Christian motifs.\nExcluded: Mughal or Islamic, Christian items.\nOut of scope: Mughal and Islamic motifs, Christian motifs.\nA Mughal garden, not too dark.\n"
          "Fade out to a Taj Mahal silhouette.\nA church without a steeple.\nChristmas lights left out on the porch.\n"
          "No new shots today, so keep every frame bright and warm, then add a Mughal arch.\n"
          "No Mughal garden here. Later the camera pulls back across a long hall to a Mughal arch.\n")
    # scene code: every string is rendered, so animation words must never excuse a keyword (the four lines of the r1 review)
    write(root, "pipeline/scenes/scene_anim.js", "const a = 'fade out to a Taj Mahal silhouette';\nconst b = 'no fog over the Mughal garden tonight';\nconst c = 'a church without a steeple';\nconst d = 'Christmas lights left out on the porch';\n")
    # even a plain rule sentence is not demoted under pipeline/scenes/ or in the phone test strings
    write(root, "pipeline/scenes/notes.md", "No Mughal or other Islamic motifs in this scene.\n")
    write(root, "pipeline/phone/test_strings.json", '["never a Taj Mahal here", "avoid every church"]\n')
    write(root, "docs/outside_theme_paths.md", "A Mughal garden here is not in a theme-bearing path.\n")
    rc, out = run(root, "--theme")
    ls = [l for l in out.splitlines() if l.startswith("FINDING")]
    result("theme_guard_flags_Mughal_garden", any("pipeline/scenes/scene1.js:2" in l and "mughal" in l for l in ls), "; ".join(ls[:3]))
    result("theme_guard_flags_Christmas_card", any("pipeline/scenes/scene1.js:3" in l and "christmas" in l for l in ls), "")
    result("theme_guard_flags_Taj_Mahal", any("scene1.js:5" in l and "taj-mahal" in l for l in ls), "")
    result("theme_guard_does_not_flag_crossfade_across_or_Churchill", not any("scene1.js:4" in l or "scene_ok.js" in l for l in ls), "; ".join(l for l in ls if "scene1.js:4" in l or "scene_ok" in l))
    result("theme_guard_ignores_files_outside_the_theme_paths", not any("outside_theme_paths" in l for l in ls), "")
    notes_ = [l for l in out.splitlines() if l.startswith("NOTE")]
    result("theme_guard_shows_rule_statements_as_NOTE_not_findings", not any("scene_rules.md:1" in l or "scene_rules.md:2" in l or "scene_rules.md:3" in l for l in ls)
           and all(any("scene_rules.md:%d" % n in l for l in notes_) for n in (1, 2, 3)), "; ".join(l for l in out.splitlines() if "scene_rules" in l)[:200])
    result("theme_guard_still_flags_a_use_with_only_a_plain_not", any("scene_rules.md:4" in l and "mughal" in l for l in ls), "")
    # review r1, C-1: the four animation lines in scene code are FINDINGs, never NOTEs
    for n, kid in ((1, "taj-mahal"), (2, "mughal"), (3, "church"), (4, "christmas")):
        result("theme_guard_flags_animation_word_line_%d_in_scene_code" % n, any("scene_anim.js:%d" % n in l and kid in l for l in ls) and not any("scene_anim.js:%d" % n in l for l in notes_),
               "; ".join(l for l in out.splitlines() if "scene_anim.js:%d" % n in l)[:160])
    # ... and also in prose: 'out' and 'without' are no cue, and a cue AFTER the keyword never counts
    result("theme_guard_flags_fade_out_and_without_in_markdown", any("scene_rules.md:5" in l and "taj-mahal" in l for l in ls) and any("scene_rules.md:6" in l and "church" in l for l in ls), "")
    result("theme_guard_does_not_demote_a_cue_after_the_keyword_or_far_before_it", any("scene_rules.md:7" in l and "christmas" in l for l in ls) and any("scene_rules.md:8" in l and "mughal" in l for l in ls), "")
    result("theme_guard_judges_every_occurrence_on_a_line", any("scene_rules.md:9" in l and "mughal" in l for l in ls) and not any(l.startswith("NOTE") and "scene_rules.md:9" in l for l in out.splitlines()), "")
    # never demote under pipeline/scenes/ (even in a .md) or in the phone test strings
    result("theme_guard_never_demotes_under_pipeline_scenes_or_phone_test_strings",
           any("pipeline/scenes/notes.md:1" in l for l in ls) and any("test_strings.json:1" in l and "taj-mahal" in l for l in ls) and any("test_strings.json:1" in l and "church" in l for l in ls)
           and not any(l.startswith("NOTE") and ("pipeline/scenes/" in l or "test_strings" in l) for l in notes_), "")
    result("theme_guard_exits_1_and_states_its_limit", rc == 1 and "can NOT judge iconography" in out, "exit %d" % rc)
    rc, out = run(root, "--theme", "--paths", "pipeline/scenes/scene_ok.js")
    result("theme_guard_passes_crossfade_alone", rc == 0, out.strip().splitlines()[0])
    rc, out = run(root, "--theme", "--paths", "pipeline/scenes/scene_anim.js")
    # 5 findings: 'a church without a steeple' is a church (r1) and, since the review r4 keywords, a steeple too
    result("theme_guard_exits_1_on_a_scene_file_of_only_animation_word_lines", rc == 1 and len([l for l in out.splitlines() if l.startswith("FINDING")]) == 5 and any("scene_anim.js:3" in l and "steeple" in l for l in out.splitlines())
           and not any(l.startswith("NOTE") for l in out.splitlines()), "exit %d" % rc)
    rc, out = run(root, "--theme", "--paths", "docs/outside_theme_paths.md")
    result("theme_guard_with_explicit_paths_scans_what_it_is_given", rc == 1 and "mughal" in out, "")
    # a changed (not new) theme-bearing file: only its added lines count
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "second")
    with open(root / "ops" / "GATHER.md", "a", encoding="utf-8") as fh:
        fh.write("Visit the old mos" + "que.\n")
    rc, out = run(root, "--theme")
    result("theme_guard_sees_the_added_line_of_a_changed_theme_file", "ops/GATHER.md:3" in out and "mosque" in out, out.strip().splitlines()[0] if out.strip() else "")
    result("theme_guard_reports_old_playbooks_as_INFO_only_and_never_fails_them",
           "INFO only" in out and "playbooks: 1 keyword hit" in out and not any(l.startswith("FINDING") and "playbooks/old.md" in l for l in out.splitlines()),
           next((l for l in out.splitlines() if l.startswith("INFO")), "no INFO line")[:160])
    (root / "ops" / "GATHER.md").write_text("# Gather\nPlain list.\n", encoding="utf-8")

    # a staged copy of an installed skill (untracked, so every line of it is new to git) is judged on the lines its installed counterpart lacks (2026-10-20, package k2-pr4-skill-parity);
    # explicit --paths still scan the whole file
    inst_text = "# Pair\nNo Mughal motifs in this skill.\nA cited title: The Mughal Garden, a book.\nPlain line.\n"
    write(root, ".claude/skills/pairskill/SKILL.md", inst_text)
    write(root, "skills-staging/pairskill/SKILL.md", inst_text + "A new line with a Mughal arch.\n")
    write(root, "skills-staging/solo/SKILL.md", "# Solo\nA cited title: The Mughal Garden, a book.\n")
    rc, out = run(root, "--theme")
    ls = [l for l in out.splitlines() if l.startswith("FINDING")]
    result("theme_guard_judges_a_staged_skill_copy_on_the_lines_its_installed_copy_lacks",
           any("skills-staging/pairskill/SKILL.md:5" in l and "mughal" in l for l in ls) and not any("skills-staging/pairskill/SKILL.md:2" in l or "skills-staging/pairskill/SKILL.md:3" in l for l in ls)
           and not any(l.startswith("NOTE") and "skills-staging/pairskill/SKILL.md:2" in l for l in out.splitlines()), "; ".join(l for l in ls if "pairskill" in l)[:200])
    result("theme_guard_still_scans_a_staged_file_that_has_no_installed_counterpart_whole", any("skills-staging/solo/SKILL.md:2" in l and "mughal" in l for l in ls), "")
    rc, out = run(root, "--theme", "--paths", "skills-staging/pairskill/SKILL.md")
    result("theme_guard_with_explicit_paths_still_scans_a_staged_copy_whole", "pairskill/SKILL.md:3" in out and "pairskill/SKILL.md:5" in out, "")
    for rel_ in (".claude/skills/pairskill/SKILL.md", "skills-staging/pairskill/SKILL.md", "skills-staging/solo/SKILL.md"):
        (root / rel_).unlink()

    # review r4, nudge 4: playbooks/ is a theme path (new or changed lines only) and the unambiguous D-28 words Easter, Eid, steeple, jali, arabesque, muezzin are keywords
    write(root, "playbooks/x.md", "A Mughal garden opens the chapter.\nNo Mughal motifs.\nEaster egg hunt.\nEid lanterns, an arabesque border, and the muezzin calls.\nA jali screen and a church steeple.\nThe Eastern shore and Eidetic memory.\n")
    rc, out = run(root, "--theme")
    ls = [l for l in out.splitlines() if l.startswith("FINDING")]
    notes_ = [l for l in out.splitlines() if l.startswith("NOTE")]
    result("theme_guard_scans_a_new_playbook_and_flags_a_Mughal_garden", rc == 1 and any("playbooks/x.md:1" in l and "mughal" in l for l in ls), "; ".join(ls[:2]))
    result("theme_guard_shows_No_Mughal_motifs_in_a_playbook_as_a_NOTE", any("playbooks/x.md:2" in l for l in notes_) and not any("playbooks/x.md:2" in l for l in ls), "; ".join(notes_[:2]))
    result("theme_guard_flags_Easter_in_a_playbook", any("playbooks/x.md:3" in l and "easter" in l for l in ls), "")
    result("theme_guard_flags_Eid_arabesque_muezzin_jali_and_steeple",
           all(any("playbooks/x.md:%d" % n in l and kid in l for l in ls) for n, kid in ((4, "eid"), (4, "arabesque"), (4, "muezzin"), (5, "jali"), (5, "steeple"), (5, "church"))), "; ".join(l for l in ls if "x.md:4" in l or "x.md:5" in l)[:200])
    result("theme_guard_does_not_flag_Eastern_or_Eidetic", not any("playbooks/x.md:6" in l for l in ls), "; ".join(l for l in ls if "x.md:6" in l))
    result("theme_guard_still_leaves_an_unchanged_old_playbook_as_INFO", not any("playbooks/old.md" in l for l in ls) and "playbooks: 1 keyword hit" in out, "")
    (root / "playbooks" / "x.md").unlink()
    old_pb = (root / "playbooks" / "old.md").read_text(encoding="utf-8")
    (root / "playbooks" / "old.md").write_text(old_pb + "A new line with a Mughal arch.\n", encoding="utf-8")
    rc, out = run(root, "--theme")
    ls = [l for l in out.splitlines() if l.startswith("FINDING")]
    result("theme_guard_judges_only_the_added_lines_of_a_changed_playbook", rc == 1 and any("playbooks/old.md:2" in l for l in ls) and not any("playbooks/old.md:1" in l for l in ls), "; ".join(ls[:2]))
    (root / "playbooks" / "old.md").write_text(old_pb, encoding="utf-8")
    rc, out = run(root, "--theme")
    result("theme_guard_is_quiet_again_with_the_playbooks_back_at_HEAD", rc == 0, out.strip().splitlines()[0])

    # ---------------------------------------------------------------- fail closed and usage
    bad = T / "badpat.json"
    bad.write_text("{not json", encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", str(LINT), "--root", str(root), "--patterns", str(bad)], capture_output=True, text=True)
    result("invalid_pattern_file_fails_closed_exit_2", p.returncode == 2 and "nothing was checked" in p.stdout, p.stdout.strip()[:100])
    p = subprocess.run([sys.executable, "-I", str(LINT), "--root", str(root), "--patterns", str(T / "missing.json")], capture_output=True, text=True)
    result("missing_pattern_file_fails_closed_exit_2", p.returncode == 2 and "nothing was checked" in p.stdout, p.stdout.strip()[:100])
    rc, out = run(root, "--paths", "no/such/path")
    result("missing_path_is_a_usage_error_exit_2", rc == 2, out.strip()[:80])
    rc, out = run(T / "not-a-repo-xyz")
    result("missing_root_is_an_environment_error_exit_3", rc == 3, out.strip()[:80])
    plain = T / "plain"
    plain.mkdir()
    write(plain, "a.txt", "hello\n")
    rc, out = run(plain)
    result("default_mode_outside_git_exits_3_and_says_to_use_paths", rc == 3 and "--paths" in out, out.strip()[:100])
    rc, out = run(plain, "--paths", "a.txt")
    result("paths_mode_works_without_git", rc == 0, out.strip().splitlines()[-1])

    # review r4, C-1: a path outside the repository root is a usage error (exit 2, a USAGE line), never "0 file(s) scanned" and exit 0
    outside = T / "outside"
    write(outside, "leak.md", "contact outside.person" + "@" + "mailbox-test.io today\n")
    write(outside, "scene.md", "A church steeple at dusk.\ncrossfade to the Christmas card\nA jali screen in the Mughal style\n")
    cases = (("lint_folder", ("--paths", str(outside))), ("lint_file", ("--paths", str(outside / "leak.md"))),
             ("lint_one_inside_one_outside", ("--paths", "docs/p_email.md", str(outside))),
             ("theme_folder", ("--theme", "--paths", str(outside))), ("theme_file", ("--theme", "--paths", str(outside / "scene.md"))))
    for label, args_ in cases:
        rc, out = run(root, *args_)
        result("paths_outside_the_root_exit_2_with_a_USAGE_line_%s" % label,
               rc == 2 and out.startswith("USAGE: a path given to --paths is outside the repository root (--root)") and "file(s) scanned" not in out and "outside.person" not in out and str(outside) not in out,
               "exit %d: %s" % (rc, out.strip()[:110]))
    rc, out = run(root, "--paths", "../outside", cwd=str(root))
    result("a_relative_path_that_climbs_out_of_the_root_is_also_exit_2", rc == 2 and out.startswith("USAGE: ") and "outside the repository root" in out, "exit %d: %s" % (rc, out.strip()[:110]))
    # ... while an absolute path INSIDE the root is still read, and the findings are still printed
    rc, out = run(root, "--paths", str(root / "docs" / "p_email.md"))
    result("an_absolute_path_inside_the_root_is_still_scanned", rc == 2 and "FINDING" in out and "docs/p_email.md:1" in out and "USAGE" not in out and "1 file(s) scanned" in out, "exit %d: %s" % (rc, out.strip().splitlines()[-1]))
    write(root, "pipeline/scenes/scene_probe.js", "const a = 'A church steeple at dusk';\nconst b = 'crossfade to the Christmas card';\nconst c = 'A jali screen in the Mughal style';\n")
    rc, out = run(root, "--theme", "--paths", "pipeline/scenes/scene_probe.js")
    ls = [l for l in out.splitlines() if l.startswith("FINDING")]
    result("a_church_steeple_scene_under_root_is_still_a_theme_finding",
           rc == 1 and all(any("scene_probe.js:%d" % n in l and kid in l for l in ls) for n, kid in ((1, "church"), (1, "steeple"), (2, "christmas"), (3, "jali"), (3, "mughal"))), "exit %d, %d finding(s)" % (rc, len(ls)))
    rc, out = run(root, "--theme", "--paths", str(root / "pipeline" / "scenes" / "scene_probe.js"))
    result("the_same_scene_by_absolute_path_inside_the_root_is_also_a_finding", rc == 1 and "scene_probe.js:1" in out, "exit %d" % rc)

    # review r4, nudge 5: a local deny list that exists but is not git-ignored is a finding (exit 2) before `git add -A` stages the maker's real names
    dr = T / "deny_repo"
    dr.mkdir()
    git(dr, "init", "-q")
    write(dr, "a.md", "A clean page.\n")
    git(dr, "add", "-A")
    git(dr, "commit", "-q", "-m", "baseline")
    write(dr, "scripts/public_lint.deny.local.txt", "# invented names for the test\nQuillo" + "mar\n")
    for label, extra_args in (("default", ()), ("all", ("--all",))):
        rc, out = run(dr, *extra_args)
        ls = [l for l in out.splitlines() if "local_deny_file" in l]
        result("unignored_local_deny_list_is_a_finding_exit_2_%s_mode" % label, rc == 2 and len(ls) == 1 and "exists but is not git-ignored" in ls[0] and "scripts/public_lint.deny.local.txt" in ls[0] and "Quillo" not in out and "quillo" not in out,
               "exit %d: %s" % (rc, (ls[0] if ls else out.strip())[:150]))
    rc, out = run(dr, "--staged")
    result("staged_mode_does_not_flag_an_unstaged_unignored_deny_list", rc == 0 and "local_deny_file" not in out, "exit %d" % rc)
    rc, out = run(dr, "--paths", "a.md")
    result("paths_mode_does_not_look_at_the_deny_list_file", rc == 0 and "local_deny_file" not in out, "exit %d" % rc)
    for ignore_line in ("scripts/public_lint.deny.local.txt", "*.local.*"):
        write(dr, ".gitignore", ignore_line + "\n")
        rc, out = run(dr)
        result("ignored_local_deny_list_%s_is_not_a_finding" % ("exact" if "/" in ignore_line else "star_local_star"), rc == 0 and "local_deny_file" not in out and "Quillo" not in out, "exit %d: %s" % (rc, out.strip().splitlines()[-1]))
    git(dr, "add", "-f", "scripts/public_lint.deny.local.txt")
    rc, out = run(dr)
    result("a_staged_local_deny_list_is_still_refused_even_when_ignored", rc == 2 and any("local_deny_file" in l and "unstage it" in l for l in out.splitlines()), "exit %d" % rc)

    force_added_cases(T)

    # ---------------------------------------------------------------- the consumer contract and the disagreement test
    samples = T / "samples.json"
    samples.write_text(json.dumps({"samples": {"a": "x" * 3, "b": ["192.0", ".2.1"], "c": "84.1" + "12.9.200"}}), encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", str(LINT), "--pattern-self-test", str(samples)], capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
        ok = d["consumer"] == "scripts/public_lint.py" and d["results"] == {"a": [], "b": [], "c": ["ipv4"]} and "patterns_version" in d and len(p.stdout.strip().splitlines()) == 1
    except Exception:
        ok = False
    result("pattern_self_test_prints_one_json_object_in_the_consumer_contract", ok, p.stdout.strip()[:140])
    rc, out = run(REPO, "--self-test")
    result("self_test_no_disagreement_between_consumers", rc == 0 and "no disagreement between consumers" in out, "; ".join(l for l in out.splitlines() if l.startswith("consumer"))[:300])
    result("self_test_reports_a_consumer_that_has_not_landed_as_SKIPPED_not_landed", ("SKIPPED: not landed" in out) or (REPO / "win" / "kit2" / "run_checks_pc.ps1").exists(), "")
    if not (REPO / "win" / "kit2" / "run_checks_pc.ps1").exists():
        rc2, out2 = run(REPO, "--self-test", "--fail-on-skip")
        result("self_test_fail_on_skip_makes_a_skip_a_failure", rc2 == 1, "exit %d" % rc2)
    if not QUICK:
        # a deliberately wrong consumer: windows_check.py reading a pattern file without the 64-hex exemption
        t2 = T / "mut"
        (t2 / "scripts").mkdir(parents=True)
        for f in ("public_lint.py", "windows_check.py", "public_lint.config.json", "redaction_patterns.json"):
            shutil.copy(REPO / "scripts" / f, t2 / "scripts" / f)
        pats = json.loads((REPO / "scripts" / "redaction_patterns.json").read_text(encoding="utf-8"))
        pats["exemptions"] = [e for e in pats["exemptions"] if e["id"] != "sha256_64hex"]
        (t2 / "scripts" / "redaction_patterns.mutated.json").write_text(json.dumps(pats), encoding="utf-8")
        wc = (t2 / "scripts" / "windows_check.py").read_text(encoding="utf-8")
        assert 'PATTERNS_PATH = HERE / "redaction_patterns.json"' in wc
        (t2 / "scripts" / "windows_check.py").write_text(wc.replace('PATTERNS_PATH = HERE / "redaction_patterns.json"', 'PATTERNS_PATH = HERE / "redaction_patterns.mutated.json"'), encoding="utf-8")
        p = subprocess.run([sys.executable, "-I", str(t2 / "scripts" / "public_lint.py"), "--root", str(t2), "--self-test"], capture_output=True, text=True)
        out = p.stdout
        result("self_test_exits_1_and_names_the_consumer_the_sample_and_both_answers",
               p.returncode == 1 and "DISAGREEMENT scripts/windows_check.py, sample" in out and "scripts/windows_check.py says ['guid_serial']" in out and "scripts/public_lint.py says []" in out,
               next((l for l in out.splitlines() if l.startswith("DISAGREEMENT")), out[-200:])[:240])


if __name__ == "__main__":
    sys.exit(main())
