# Staged update: agent-first-production-pipeline (WP-11b, Mon 19 Oct 2026)

Proposed by the WP-11b implementor at the end of build weeks 1 and 2. **Nothing under `.claude/` was edited.** The orchestrator copies `SKILL.md` over
`.claude/skills/agent-first-production-pipeline/SKILL.md` after `fable-advisor` approves it (CLAUDE.md: nothing counts as done until Fable approves).
Every `##` heading of the installed skill is kept; the staged file is the installed text plus the edits below, so `diff` shows exactly what moved.

## Why

The installed skill was reconciled with `DECISIONS.md` on 2026-10-19 but describes scripts that did not exist yet ("`render.mjs` is designed and not yet written",
"`lj.ps1 doctor` is designed, not built", "both are built in spike SP5" for two scripts SP5 did not deliver). Weeks 1 and 2 built and tested the real ones on synthetic
material. The skill now points each step at the script that does it, so an agent does not hand-type a colour chain or hunt for a validator that was never written.

## What changed, step by step

| Where | Change | Evidence |
|---|---|---|
| front matter description | adds the checks and files an agent now meets: `spec_check.py`, `colour_patch.py`, `mo8_gate.py`, `stale_check.py`, `public_lint.py`, `pc_tier.json`, `INDEX.md` | `pipeline/README.md` |
| Purpose | links `pipeline/README.md` and the P-LOCK readiness map; one paragraph says what is built and proven in the container, what is not built (`lint_template.py`, `edit_audit.py`, the manifest schema, the timeline emitters, `lj.ps1 run`) and that nothing has run on Windows | `build/evidence/P-LOCK-readiness-W2.md` |
| Step 4 | `lj.ps1 run <shot>` does not exist; for a `cloud: none` input the maker runs the printed command by hand and pastes the validator output in chat | `win/README-LJ.md` |
| Step 8 | the real `render.mjs` invocation (`--dir pipeline --mount /vendor=vendor`, shards, resume, `--max-seconds`, network off, path-traversal fix F-09, `--fail-on-pageerror`); encode with a **named chain** from `pipeline/lib/chains.json` (`--chain NAME --ffmpeg OUT`, or `--encode` for a sharded run) instead of a hand-typed `-vf`; **finding F-12** | `build/evidence/wp04/`, `build/evidence/wp05/oracle_findings.json` |
| Step 10 | `lint_template.py` and `edit_audit.py` are not built (the old text said SP5 built them) | `spikes/VERDICTS-W2.md` |
| Step 11 | names the validators and repo checks by script | `pipeline/validators/README.md` |
| Step 14 | what the Linux runs of the pinned apps showed for hand-offs: VectorCraft turns rect, circle and ellipse into paths and changes `data-*` on text; FilmCraft's XML exports hold absolute `file://` paths and lose the ease, so OTIO is the only portable hand-off; named emitters and validators in `pipeline/roundtrip/` | `build/evidence/wp10/`, `spikes/VERDICTS-W2.md` |
| Step 16 | the phone files with the real scripts (`encode_phone.sh`, `spec_check.py --profiles-file`, `phone_check.py`) and the fill-crop rule: the caption bottom must be at or above 88% of picture height because a phone set to fill crops about 10% off the top and bottom; the venue caption fails it by design. After Fable's round 1: PH2 stays at the register's 4 Mb/s cap (W-63) and the phone caption at 36 characters (W-18); the step says the register wins over `profile.json` and `PHONE-ROW.md`, that `parity.phone_profile_vs_register` checks it, and that `PHONE-ROW.md` is not pasted over the settings card while they disagree | `pipeline/phone/PHONE-ROW.md`, `build/evidence/wp08/`, `tests/integration/` |
| Validators checklist | video row = one `spec_check.py` command; colour row adds `colour_patch.py --all` and says `spec_check.py` does not replace it; new motion row (`mo8_gate.py`); new repo row (`public_lint.py`, `stale_check.py --new-only`) | `tests/integration/run_tests.sh --all` proves the MO8 pair |
| Checklists, new block | **Redaction and what may be filed**: one pattern file (`scripts/redaction_patterns.json`, build plan 4.13) read by four consumers, fail closed, masked output, `--self-test --fail-on-skip`; the **raw-versus-derived rule** (4.4, 4.16): raw PC reports and raw colour-patch files go to chat only, never into the repo; only `pc_tier.json` and `pc_chains.json` are filed, under `build/evidence/pc/` | `scripts/redaction_patterns.json`, `build/evidence/pc/README.md` |
| New section "Tools that exist today" | table of the Windows tools and the container scripts: what `lj.ps1 doctor` does, that `lj.ps1 close` is **a dry run in v0** (deletes, commits, pushes, writes and backs up nothing), that `-Apply`, `-Commit` and `-IncludeWindowsRecent` do not exist until v1 in week 4, and that the readiness map reads "v0 dry-run done; v1 not started (week 4)", never PASS | `win/lj.ps1`, `win/README-LJ.md`, `tests/win_lj/` |
| References | open gaps and corrections brought up to date: `render.mjs` is written (SP2 passed); `lj.ps1 doctor` v0 is built; SP1 T2 and T4 not run, SP3 deferred for disk, SP4 armed | `spikes/VERDICTS-W2.md` |
| Changelog | one new entry; the older entry's retired spelling of the process lock is replaced by "the process lock (P-LOCK)" so the stale-copy check (W-29) passes on the staged file | `python3 -I scripts/stale_check.py` |

## Finding F-12 in one line

The 3-patch colour test of the first research round measured H.264 and ProRes 4444 only. The ProRes 422 HQ master chain (W-15), which every delivery file is made
from, was measured for the first time by `colour_patch.py`: worst error 2/255 with ffmpeg's default decode and 0/255 with the accurate decode, on ffmpeg 6.1.1, inside
the +-3 tolerance (W-16), so `prores422hq_master` is `approved: true`. The numbers are for the container's build; the PC's ffmpeg (9.0.2) must repeat the test
(UNVERIFIED until the maker runs `win\kit2\run_checks_pc.ps1`).

## What did not change

Procedure order, gates G0 to G6, the Hindu-world and phone fields of the brief, the ethics and privacy guardrails, the quality bar, the key URLs. No rule was loosened.
No claim about Windows was upgraded: every Windows statement in the staged file still says UNVERIFIED, and the Linux results for the Craft apps are labelled as such.

## Checks run on this staged file

`python3 -I scripts/stale_check.py` (no hit in `skills-staging/`), `python3 -I scripts/public_lint.py --theme` (clean), `bash tests/integration/run_tests.sh --quick`
(`docs.staged_skill_update`: same name, every installed heading kept, the real script names present, every repo path it names exists).
