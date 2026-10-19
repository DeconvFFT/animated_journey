# ops/: the working files of the project

Text only; IDs only, never names (the repository is public, D-26). Owner of these files: WP-02.

| File | What it is | Who edits it |
|---|---|---|
| `hours.csv` | The hours log. Header only until the maker logs a block of work. How to fill it in: `HOURS-HOWTO.md`. | the maker types; the orchestrator commits |
| `HOURS-HOWTO.md` | One page: what counts, the columns, the activity words, "no names in note". | the orchestrator |
| `decisions.csv` | A flat mirror of `DECISIONS.md` (one row per D-, W-, O- and S- ID). Generated, never hand-typed: `python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv`; check with `--check`. Only the two columns `maker_answer` and `last_changed` are typed by the orchestrator and survive regeneration. | the register is the source; the orchestrator regenerates |
| `gate_log.csv` | The gate-decision log (header only) in the schema the planning skill reads: `research/production-scale-fixtures/decisions.csv` is the template. | the orchestrator, at each gate |
| `GATHER.md` | What to collect and when: Part A before P-LOCK (own material and five stand-in scans), Part B from Sun 15 Nov after P-LOCK. | the orchestrator; the maker ticks and dates it |
| `SETTINGS-CARD.md` | The settings card TD-1 to TD-4 (plus colour, sound and the phone row) for the maker to sign on Sun 1 Nov. It stays `signed: no` until the maker says so. | the orchestrator; never an agent's signature |

Checks (all read-only): `python3 -I scripts/ops_lint.py` for these files, `python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19` for the hours, `bash tests/ops/run_tests.sh --all` for the tests. `ops_lint.py` reads every identifying-data pattern from `scripts/redaction_patterns.json` and, on the maker's machine only, a private deny list `scripts/public_lint.deny.local.txt` (it must stay git-ignored; never commit it).
