# WP-01a report: Windows kit A (PC inventory, report checker, tools, pins, schema, fixtures, maker README)

Written Mon 19 Oct 2026 by the Sonnet implementor for WP-01a. Branch `build/process-lock`. Nothing was committed or pushed. No file outside the owner paths was edited (scratch work stayed in `<scratch>` and `renders/`, which is git-ignored).

## 0. Status in one paragraph

Everything in the WP-01a deliverables list exists and passes its tests **in the container**. One start gate was not met while I worked: **WP-03's `scripts/redaction_patterns.json` and `scripts/lj_guard.sh` had not landed** (no `build/evidence/wp03/LANDED-4.13.txt`). I coded against the frozen 4.13 description and ran every pattern-dependent test against a **stand-in pattern file that I built from 4.13 and kept in `<scratch>`, not in the repo** (it is not committed and I did not create `scripts/redaction_patterns.json`, which WP-03 owns). So: the 91 tests below are real passes of my code against my reading of 4.13; they are **not yet** a pass against WP-03's file. Re-running is one command, and the evidence folder records which tree was used (`build/evidence/wp01a/environment.json`: "STAND-IN in an alternate tree"). Windows behaviour is **UNVERIFIED** until the maker's first run, as the plan requires.

Test totals (last run, `LJ_TEST_TREE=<scratch>/dev-tree bash tests/win/run_tests.sh --all`): **PASS 91, FAIL 0, UNVERIFIED 1 (the Windows-claims line), SKIPPED 1 (`public_lint.py --self-test`, not landed), BLOCKED 0.** `--quick` (43 lines) takes about 7 seconds.

## 1. What I built

| Path | What it is |
|---|---|
| `win/step0_pc_tests.ps1` | The read-only inventory (about 1,000 lines with comments). 19 numbered steps, each printed before it runs and closed with `ok`, `skipped (not Windows)` or `failed: <type> - <scrubbed text>`. Writes one BOM-less UTF-8 file, by default `%TEMP%\lj_pc_report.json` (printed unexpanded). Fail-closed pattern load, self-scan with category / field / masked hit, exit 2 on refusal, hardware-name-field collisions as `NOTE`. Test modes `-TestFixture -FakeUser -FakeComputer -FakeDomain` and `-PatternSelfTest`. |
| `scripts/windows_check.py` | Standard-library checker: reads UTF-8, UTF-8 BOM, UTF-16 (with or without BOM); fail-closed pattern load; the same scan (plus `--forbid WORD` and the git-ignored local deny list); a built-in JSON-Schema subset validator; the tier table; `--json-out`, `--tier-json-out`, `--hardware-md`, `--pattern-self-test`; `-` reads the pasted report from standard input so it never has to be saved. Exit 0/1/2 (3 only if its own data files are missing). |
| `win/README-MAKER.md` | Plain-language page, 11 parse-tested `powershell` fences, every section the plan names (see section 4, README test). |
| `win/pins.json`, `win/tiers.json` | W-22 pins (PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 with fallback 0.8.0 and 0.7.2 retired, EffectCraft 0.11.1, SoundCraft none). Thresholds, each block with a `source`; proposals marked (J). |
| `win/schema/pc_report.schema.json`, `pc_tier.schema.json` | `additionalProperties: false` at every object level (a test counts them). |
| `win/tools/fetch_pwsh.sh`, `ps_parse.sh`, `ps_lint.py` | Idempotent guarded pwsh 7.5.4 fetch with SHA-256 against the release's UTF-16 `hashes.sha256`; `Parser::ParseFile` on every `.ps1` under `win/` and every `powershell` fence in the READMEs that exist; a 5.1-compatibility and read-only lint (rules R01 to R14, `RO-*`, `W01`). |
| `tests/win/run_tests.sh` (+ `make_fixtures.py`, `acceptance_transcript.sh`, `make_evidence.sh`, `mocks/mock_windows_wrapper.ps1`, `fixtures/` with 19 synthetic reports and a README) | `--quick` and `--all`; every test writes an evidence envelope (4.2) to `build/evidence/wp01a/tests.jsonl`. |
| `build/evidence/wp01a/` | `tests_quick.txt`, `tests_all.txt`, `tests.jsonl`, `summary.json`, `acceptance_transcript.txt` (the plan's acceptance commands run verbatim), `unverified.txt`, `fetch_pwsh_run.txt`, a sample derived `tier_gpu12_pro_16gb.json` and `hardware_gpu12_pro_16gb.md` (from a synthetic fixture), `environment.json`. |

Fixtures beyond the plan's list (my own rules deserve their own tests): `report_gpu_low_4gb`, `report_amd_16gb` (non-NVIDIA cap), `report_below_blender_floor`.

## 2. How to run it

Maker (Windows, nothing to install), from the project folder:

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\step0_pc_tests.ps1
```

then read `%TEMP%\lj_pc_report.json` in Notepad and paste it in chat only. Orchestrator, in the container (the pasted text can be piped, so it never needs saving):

```
python3 -I scripts/windows_check.py -                     < pasted.txt         # table and exit code
python3 -I scripts/windows_check.py --tier-json-out build/evidence/pc/pc_tier.json --hardware-md <scratch>/hardware.md -   < pasted.txt
```

Tests and tools (repo root):

```
bash tests/win/run_tests.sh --quick          # about 7 s
bash tests/win/run_tests.sh --all            # about 35 s; needs pwsh from fetch_pwsh.sh
bash tests/win/make_evidence.sh              # regenerates build/evidence/wp01a/
bash win/tools/ps_parse.sh                   # exit 3 "PENDING: pwsh not yet fetched" if pwsh is absent
python3 -I win/tools/ps_lint.py [--allow-write] FILE.ps1|README.md
python3 -I tests/win/make_fixtures.py [--check]
bash win/tools/fetch_pwsh.sh <absolute new path>            # inside lj_with_disk 275 once the guard exists
```

While the WP-03 file is missing, add `LJ_TEST_TREE=<a tree with the same layout and a stand-in pattern file>`; the report line and `environment.json` then say so. A tree without the pattern file ends `BLOCKED` (exit 3), never a silent pass.

## 3. Acceptance tests (the plan's list, in its order)

Real transcripts: `build/evidence/wp01a/acceptance_transcript.txt` and `tests_all.txt`. "SI" below means the run used the stand-in pattern file.

| # | Test | Result | Proof |
|---|---|---|---|
| 1 | `source scripts/lj_guard.sh; lj_with_disk 275 wp01a-pwsh -- bash win/tools/fetch_pwsh.sh <scratch>/pwsh` | **BLOCKED as written; the same script PASSED run directly** | `scripts/lj_guard.sh` does not exist yet. I ran `bash win/tools/fetch_pwsh.sh <scratch>/pwsh` directly (the script applies the same rule itself: refuse unless Avail minus 275 MB stays at least 400 MB). Output: `df (before): Avail 971 MB`, `size 75396784 bytes`, `computed: 1fd7983fe56ca9e6233f126925edb24bf6b6b33e356b69996d925c4db94e2fef`, `published: ...` identical, `MATCH`, `PowerShell 7.5.4`, `df (after): Avail 786 MB`, `exit=0` (`fetch_pwsh_run.txt`). Re-run idempotent: `already installed and verified`, exit 0. Note for the orchestrator: Avail is now about 600 MB, below the 675 MB the literal command needs, so the guarded command will refuse (`DISK`) until space is freed. |
| 2 | `bash tests/win/run_tests.sh --all` | **PASS (SI)**, exit 0 | `WP-01a all: PASS=91 FAIL=0 UNVERIFIED=1 SKIPPED=1 BLOCKED=0` |
| 3 | `ps_lint.py win/step0_pc_tests.ps1 && ps_parse.sh` | **PASS** | `TOTAL: 0 error(s), 0 warning(s)`; `PARSED 12 item(s), 0 parse error(s)` (the script and 11 README fences, pwsh 7.5.4) |
| 4 | `pwsh -File win/step0_pc_tests.ps1 -Out renders/wp01a/linux_report.json`, then the checker | **PASS (SI)** | exit 0, `files written: renders/wp01a/linux_report.json`; checker: `NOT A WINDOWS REPORT: os.platform is non-windows ...` `RESULT: exit 1` |
| 5 | gpu12_pro | **PASS** | exit 0; `gpu_tier gpu-8-12 NVIDIA, 12.0 GB read from nvidia-smi`; `ram_tier 16+ ... WSL2 ok`; `pro-or-higher ... BitLocker can be offered` |
| 6 | nogpu_home | **PASS** | exit 0; `gpu_tier none`, `ram_tier 8-15`, `edition home ... BitLocker not offered`, `RESULT: exit 0 ... A low tier is information, not a failure` |
| 7 | software_gpu | **PASS** | exit 0; `gpu_tier none` |
| 8 | vram_nvidia_over_cap | **PASS** | exit 0; `gpu-16+ ... 24.0 GB read from nvidia-smi` |
| 9 | vram_capped_only | **PASS** | exit 1; `FINDING: VRAM unreadable: AdapterRAM stops near 4 GB ...` |
| 10 | ffmpeg9 | **PASS** | exit 0; `ffmpeg 9.0.2 ... run the colour-patch test on this build` |
| 11 | craft_pins_mixed | **PASS** | exit 1; `photocraft match (0.10.0); vectorcraft MISMATCH (0.12.9); lightcraft absent; filmcraft fallback pin (0.8.0); effectcraft absent; soundcraft unpinned (learning only)` |
| 12 | identifying | **PASS (SI)** | exit 2; four lines `category=email field=tools.git.notes hit=ta********`, `category=ipv4 field=notes[0] hit=10********`, `category=mac field=notes[3] hit=02********`, `category=profile_path_windows field=errors[0] hit=C:********`; the test also asserts none of the planted values appears in output |
| 13 | bom equals plain | **PASS** | same 18 table lines; UTF-16 with and without BOM (made with `iconv` at test time) give the same table, only the `encoding:` line differs |
| 14 | `--forbid exampleperson` on gpu12 | **PASS** | exit 0 |
| 15 | `--forbid zeta` collision | **PASS (SI)** | exit 0; `NOTE category=user_name field=gpus[0].name hit=ze** (a hardware-name field: reported, not refused)` (and the `vendor` field) |
| 16 | `--forbid zeta` leak | **PASS (SI)** | exit 2; `category=user_name field=tools.git.notes hit=ze**` |
| 17 | version strings shaped like IPv4 | **PASS (SI)** | exit 0 (needs the `field_exemptions` of the pattern file) |
| 18 | sha256_ok | **PASS (SI)** | exit 0 (64-hex exempt) |
| 19 | hex65_leak | **PASS (SI)** | exit 2; `category=guid_serial field=notes[0] hit=3f********` |
| 20 | `--tier-json-out` | **PASS** | exit 0; validates against `pc_tier.schema.json` with the checker's own validator |
| 21 | Tier file leaks nothing | **PASS** | a test searches the tier file for the CPU and GPU names and every token of them (4 characters or more), the driver version, OS caption/version/build, RAM, every disk size and free figure, and the tool versions: 0 found; `additionalProperties: false`; no `shared_pc_hint` (see deviation D1) |
| 22 | Self-scan, script side, identifying fixture with invented names | **PASS (SI)** | exit 2; `REDACTION CHECK FAILED, nothing was written`; nine `category=... field=... hit=...` lines including `user_name`, `computer_name`, `domain_name`; stdout contains none of the three invented names in full; `renders/wp01a/none.json` does not exist |
| 23 | Same, collision fixture | **PASS (SI)** | exit 0; two `NOTE` lines; `files written: renders/wp01a/collision.json`; the file's `redaction.name_hits_in_hardware_fields` holds the two notes |
| 24 | Same, leak fixture | **PASS (SI)** | exit 2; `category=user_name field=tools.git.notes hit=ze**`; no file |
| 25 | Fail closed | **PASS** | a copy of the kit without the pattern file: `step0` exits 2 with `REDACTION PATTERNS UNAVAILABLE, nothing was collected and nothing was written`, no output file; `windows_check.py` exits 2, no `--tier-json-out` or `--json-out` file. Also a corrupt pattern file (exit 2 both) and one lacking required categories (exit 2) |
| 26 | `public_lint.py --self-test` | **SKIPPED: not landed** | stand-in until then: `patterns.python_and_powershell_agree`: 30 samples built from the pattern file's own declared samples, `python/powershell disagreements or declared-expectation misses: 0` |
| 27 | No private identifying-data regex | **PASS** | a grep over `win/step0_pc_tests.ps1`, `win/tools/*`, `scripts/windows_check.py` for e-mail, IPv4, MAC, IPv6, GUID and profile-path regex shapes: nothing |
| 28 | README test | **PASS** | `headings found: 9/9; powershell fences: 11; pattern categories scanned: 9; problems: 0`; referenced files exist; no handle, e-mail, IP or user path |
| 29 | Planted machine-scope `Set-ExecutionPolicy` | **PASS** | `ps_lint.py` exit 1 `[R13]` for a `.ps1`, for a `.md` fence, and for the real README with a block appended; `-Scope Process` and quoted text pass |
| 30 | Directory hash before/after | **PASS (SI)** | the kit and fixtures hash identically before and after; the only new files are the three passing `-Out` files; the refusals created none |

Extra tests I added (all PASS): Windows-branch logic of the script with invented CIM / registry / `nvidia-smi` / `wsl` answers (`mock_windows.*`, 12 lines: nvidia-smi merge over a capped AdapterRAM, `qwMemorySize` as 64-bit and as bytes, the CIM account fallback, drives without network/CD/null-size entries, screen mode and scale, Craft folder scan with `FilmCraft-v0.8.0-win-x64` and `vectorcraft_0.13.1`, a failing step that continues with a scrubbed message, a real-mode user name in the CPU field as a note, in a drive field as a refusal); the local deny list in UTF-16; stdin; invalid JSON, schema-invalid and unknown-key input (the unknown key name is not echoed); a collision audit of 12 clean fixtures and the script's own note strings against nine default Windows names (this is what found D4).

## 4. UNVERIFIED (listed in `build/evidence/wp01a/unverified.txt`, 15 groups)

Every CIM/WMI query and the registry reads (EditionID, UBR, display class `qwMemorySize`, `AppliedDPI`); `Get-LocalUser` on 5.1 and on 7; `System.Windows.Forms` screen count; `winget --version`, `wsl --status` (UTF-16 output and its English wording), `py -3 --version`; the `nvidia-smi` output format; Vulkan detection (a DLL on disk is only a hint); the `%TEMP%` default on a managed PC; Windows PowerShell 5.1 behaviour of every cmdlet and of `ConvertTo-Json`; execution-policy options A and B, `Unblock-File`, Group Policy; whether version strings on the maker's PC trip a pattern; process start with time limits through `System.Diagnostics.Process` on 5.1; the (J) thresholds in `tiers.json`; the six paste-in commands (parse-tested only, `Get-CimInstance` does not exist on Linux); the File Explorer instructions. The mock tests prove the script's own logic, not what Windows answers.

## 5. Deviations from the plan, and why

- **D1. `shared_pc_hint` is not in `pc_tier.json`.** Fable's round-2 review (nudge 4) asked for it to be cut; the checker still prints it in the chat table. Plan text 4.16 lists it; the schema and file follow the nudge.
- **D2. Nudge 7 applied:** `windows_check.py` and the script read extra forbidden words from the git-ignored `scripts/public_lint.deny.local.txt` (category `local_deny`, whole word, any Notepad encoding). `--forbid` stays in the checker for container tests and is **not** in the maker README, which explains the deny file instead.
- **D3. The sixth paste-in command is `py -0`, not `py -0p`.** `py -0p` prints folder paths that normally contain the Windows user name, which would then sit in the chat. The README says why.
- **D4. `powershell.edition` is `WindowsPowerShell` / `PowerShell`, not PSEdition's `Desktop` / `Core`.** My collision audit showed that the word `Desktop` is the start of every default computer name (`DESKTOP-XXXXXXX`) and the 4.13 fragment rule would have refused the maker's first report on most PCs. Same keys as 4.4, different label; the schema enumerates the two values.
- **D5. Exit code 3** from `windows_check.py` when its own `win/*.json` files are missing (4.3: environment problem). The plan lists 0/1/2 for the tool; pattern-file problems are still exit 2.
- **D6. Acceptance line 1 (guard).** See table: the guard does not exist, so I ran the identical rule inside the script. When the guard lands and there are 675 MB free, the literal command works unchanged (the script is idempotent and does not need the guard to be sourced).
- **D7. Stand-in pattern file.** See section 0. My loader accepts the same alternatives for `exemptions` / `field_exemptions` keys as WP-02's `ops_lint.py` does (`category`, `categories`, `applies_to`, `category_id`; `fields`, `field`, `paths`, `path`), skips documented `placeholders`, and treats a hit as exempt when an exemption match covers its span (so a 64-hex run is exempt and a 65-hex run is not). If WP-03 chose different key names the loader fails closed (exit 2) or becomes stricter, never looser.
- **D8. GPU tier for non-NVIDIA cards is capped at `gpu-low`** until a test says otherwise, because `playbooks/ai-imagery.md` Decision 2 names the 8 to 12 GB tier as Nvidia and its tools assume CUDA. It is data (`non_nvidia_max_tier`, set to null to remove). Marked (J).
- **D9. Blender floor** is judged on physical cores, RAM and VRAM; "below" is information, never a failure.
- **D10. magick, inkscape and blender are found by file and never started** (version from the file's resource). The plan's `tools` list gives each `{found, version, notes}` without saying they are run; starting Blender or Inkscape was not worth the risk.
- **D11. `-Out` creates a missing parent folder** and prints `created folder:` in the files-written line, so the plan's `-Out renders/wp01a/...` commands work on a fresh checkout. Nothing else is ever created. The default path (`%TEMP%`) always exists.
- **D12. `-PatternSelfTest` prints exactly one JSON object on stdout**; its `TEST MODE` banner goes to stderr so the object can be parsed. Other test modes print the banner on stdout.
- **D13. `Next:` line precedes the final line** so that `files written: ...` is the last line printed, as 4.7 says.

## 6. Requests and findings for the orchestrator and other packages

1. **WP-03 / `public_lint.py`:** treat `tests/win/fixtures/` as a place where synthetic planted values are expected. I hid the punctuation of the planted e-mail, IPv4, MAC and profile path with `\u` escapes and I build every planted string from pieces in the Python and PowerShell sources, but `report_hex65_leak.json` has a 65-character hex run in plain text and `report_version_strings_not_ip.json` contains only escaped dots, so the hex file needs the path exemption (the path denylist exemption in 4.13 is the same folder).
2. **WP-03 / 4.13:** `vulkan.devices[]` holds GPU names (hardware names) but is not in `hardware_name_fields`; a user name that collides with a Vulkan device string would refuse. Suggest adding `vulkan.devices[]`. Also consider a fragment exemption for `tools.ffmpeg.sha256` (a 4-hex-character computer-name fragment can occur in a random 64-hex hash by chance; about 0.4 percent for a hex-only default name, and the refusal is safe but annoying).
3. **Orchestrator:** `.gitignore` needs `pc_report*.json`, `*.local.*` (the deny list), `logs/` as in round-2 nudge 8; `renders/` is already ignored. Decide C-04 (second tools root `C:\LifeJourney\tools`; one line in `win/pins.json` and one in the script) and C-11 (the ai-photo skill's `hardware.md` fields: the checker writes the bucketed draft).
4. **Disk:** the shared volume dipped to about 130 MB free for a few minutes during my work (another job) and came back to about 600 MB; two of my test runs failed on write during the dip and passed when re-run. `<scratch>/pwsh` is 185 MB and stays until `cleanup_scratch.sh`.
5. **`fable-advisor` Tuesday checklist (round-2 nudge 2):** `step0_pc_tests.ps1`, `windows_check.py` (validate, scan, tier table, `--pattern-self-test`), `README-MAKER.md`, `ps_lint.py`, `ps_parse.sh`, `pins.json`, `tiers.json`, `pc_report.schema.json`, the fail-closed test and the five redaction fixtures are all present and passing; `pc_tier.schema.json`, `--tier-json-out`, `--hardware-md`, `report_bom` and the UTF-16 test are also done, so nothing has to wait for Friday.

## 7. Known risks left open

- The first real Windows run may show a step `failed` (each is isolated and recorded in `errors[]`), a false refusal from the pattern file (the README tells the maker exactly what to paste), or a policy block (the README says to stop). The six paste-in commands are the last fallback, and the README's "if it fails" section names them.
- My name rule follows 4.13 literally (whole word plus 4-character fragments of names of 5 or more characters). Names such as `Administrator` or `DESKTOP-ABC123` are audited against the clean fixtures and the script's own strings; a user whose name shares four letters with some other report text will see a refusal with the category and field, by design.
