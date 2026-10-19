# tests/runner (WP-11a)

Tests for `scripts/run_week2_checks.sh` (the check runner and its `INDEX.md` writer) and `scripts/cleanup_scratch.sh`.

```bash
bash tests/runner/run_tests.sh --quick    # about 40 s: fake-area tests, cleanup tests, lint of the owned files
bash tests/runner/run_tests.sh --all      # quick + a rerun check and a real-tree dry run of the cleanup script
```

Output: `RESULT PASS|FAIL name :: detail` lines, the log in `build/evidence/wp11a/tests_<mode>.txt`, envelopes in
`build/evidence/wp11a/tests_<mode>.jsonl` (build plan 4.2), `summary_<mode>.json` (`summary.json` for `--all`) and `unverified.txt`.

## The fake areas (`fake_tests/`, listed in `fake_areas.txt`)

| area | what it does | what the runner must do |
|---|---|---|
| `fk_pass` | writes 4 envelopes, plus an older failing duplicate of one test | PASS; count 3 PASS and 1 UNVERIFIED (the newer envelope wins); lowest `avail_mb_min` 123 shown as LOW |
| `fk_fail` | exits 1 with a FAIL, a BLOCKED and a SKIPPED envelope | FAIL, runner exit 1 |
| `fk_missing` | has no folder at all | NOT LANDED, exit unaffected |
| `fk_hang` | ignores TERM, starts a background child, sleeps 300 s | TIMEOUT; the whole process group killed |
| `fk_email` | prints a planted e-mail-shaped string and a planted home path (built from fragments at run time) | both masked everywhere; raw text never stored or printed |
| `fk_edge` | picked by `FK_EDGE`: stray background process, exit 3, 450 lines, colour codes and NUL, malformed evidence | handled without a crash |

Every run uses the runner's test hooks (`LJ_RUNNER_AREAS_FILE`, `LJ_RUNNER_EVIDENCE_DIR`, `LJ_RUNNER_TESTS_DIR`, ...; see the
header of the runner), so the real `build/evidence/INDEX.md` is never touched by these tests. `lint_stub.py` stands in for
`public_lint.py` to exercise the future `--text` call. Cleanup tests build fake home, scratch and repo folders under the real
scratch folder's own temp area and remove them again. Linux only: nothing here is a Windows script.
