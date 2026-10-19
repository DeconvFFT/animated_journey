# WP-01a report: Windows kit A (PC inventory, report checker, tools, pins, schema, fixtures, maker README)

Written Mon 19 Oct 2026 by the Sonnet implementor for WP-01a, branch `build/process-lock`. Nothing was committed or pushed by me (the orchestrator's WIP checkpoint commit `e1072f5` happened to include some of my files while I was still working; the files on disk are the final ones). No file outside the owner paths was edited. Scratch work stayed in `<scratch>` and in `renders/` (git-ignored).

## 0. Status

All WP-01a deliverables exist. **Every automated test passes against WP-03's real `scripts/redaction_patterns.json` (version 1, sha256 starting `1b10d10f21a4`) and the real `scripts/lj_guard.sh`.**

- `bash tests/win/run_tests.sh --all`: **PASS 93, FAIL 0, UNVERIFIED 1, SKIPPED 1, BLOCKED 0**, exit 0, about 37 s. `--quick`: PASS 44, FAIL 0, about 7 s.
- The one SKIPPED line is `python3 -I scripts/public_lint.py --self-test`: `public_lint.py` has not landed. Until it does, `patterns.python_and_powershell_agree` stands in for it: 100 samples (the pattern file's own `samples[]` plus every category's positive and negative fragments) give the same answer in `windows_check.py` and in `step0_pc_tests.ps1`, and both match the file's declared expectation.
- The one UNVERIFIED line lists the 15 groups of Windows-only claims (section 4). **Nothing about how real Windows answers has been verified**; that waits for the maker's first run, as the plan says.

## 1. What I built

| Path | What it is |
|---|---|
| `win/step0_pc_tests.ps1` | The read-only inventory (about 1,000 lines with comments). 19 numbered steps, each printed before it runs and closed with `ok`, `skipped (not Windows)` or `failed: <type> - <scrubbed text>`. Writes one BOM-less UTF-8 file, by default `%TEMP%\lj_pc_report.json` (printed unexpanded). Fail-closed pattern load, self-scan with category / field / masked hit, exit 2 on refusal, hardware-name-field collisions as `NOTE`, the git-ignored local deny list. Test modes `-TestFixture -FakeUser -FakeComputer -FakeDomain` and `-PatternSelfTest`. |
| `scripts/windows_check.py` | Standard-library checker: reads UTF-8, UTF-8 BOM, UTF-16 (with or without BOM) from a file or from standard input (`-`, so a pasted report never has to be saved); fail-closed pattern load; the same scan plus `--forbid WORD` and the local deny list; a JSON-Schema subset validator; the tier table; `--json-out`, `--tier-json-out`, `--hardware-md`, `--pattern-self-test`. Exit 0/1/2 (3 only if its own `win/*.json` files are missing). |
| `win/README-MAKER.md` | Plain-language page with 11 parse-tested `powershell` fences and every section the plan names. |
| `win/pins.json`, `win/tiers.json` | W-22 pins (PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 with fallback 0.8.0 and 0.7.2 retired, EffectCraft 0.11.1, SoundCraft none). Thresholds, each block with a `source`; proposals marked (J). |
| `win/schema/pc_report.schema.json`, `pc_tier.schema.json` | `additionalProperties: false` at every object level (a test checks all 28 objects). |
| `win/tools/fetch_pwsh.sh`, `ps_parse.sh`, `ps_lint.py` | Idempotent guarded pwsh 7.5.4 fetch (SHA-256 against the release's UTF-16 `hashes.sha256`; uses the guard's own `lj_df_avail_mb` when the guard exists); `Parser::ParseFile` on every `.ps1` under `win/` and every `powershell` fence in the READMEs that exist; a 5.1-compatibility and read-only lint (rules R01 to R14, `RO-*`, `W01`; default is read-only, `--allow-write` for scripts whose name says they write). |
| `tests/win/run_tests.sh` (+ `make_fixtures.py`, `acceptance_transcript.sh`, `make_evidence.sh`, `mocks/mock_windows_wrapper.ps1`, `fixtures/`: 19 synthetic reports and a README) | `--quick` and `--all`; every test writes an evidence envelope (4.2) to `build/evidence/wp01a/tests.jsonl`. |
| `build/evidence/wp01a/` | `tests_quick.txt`, `tests_all.txt`, `tests.jsonl`, `summary.json`, `acceptance_transcript.txt` (the plan's acceptance commands run verbatim), `unverified.txt`, `fetch_pwsh_run.txt`, `fetch_pwsh_guard_refusal.txt`, `fetch_pwsh_guarded_run.txt`, `fetch_pwsh_guarded.json`, a sample derived `tier_gpu12_pro_16gb.json` and `hardware_gpu12_pro_16gb.md` (from a synthetic fixture), `environment.json`. |

Fixtures beyond the plan's list: `report_gpu_low_4gb`, `report_amd_16gb` (non-NVIDIA cap), `report_below_blender_floor`. I also added a Windows-branch mock (`mocks/mock_windows_wrapper.ps1`): it runs the script with `$env:OS` set to Windows and invented CIM / registry / nvidia-smi / wsl answers, so the script's own Windows logic is exercised on Linux (not what Windows really answers).

## 2. How to run it

Maker (Windows, nothing to install), from the project folder:

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\win\step0_pc_tests.ps1
```

then read `%TEMP%\lj_pc_report.json` in Notepad and paste it in chat only. Orchestrator, in the container (the pasted text can be piped, so it never needs saving):

```
python3 -I scripts/windows_check.py -  < pasted.txt                        # table and exit code
python3 -I scripts/windows_check.py --tier-json-out build/evidence/pc/pc_tier.json --hardware-md <scratch>/hardware.md -  < pasted.txt
```

Tests and tools (repo root):

```
bash tests/win/run_tests.sh --quick          # about 7 s
bash tests/win/run_tests.sh --all            # about 37 s; needs pwsh from fetch_pwsh.sh
bash tests/win/make_evidence.sh              # regenerates build/evidence/wp01a/
bash win/tools/ps_parse.sh                   # exit 3 "PENDING: pwsh not yet fetched" if pwsh is absent
python3 -I win/tools/ps_lint.py [--allow-write] FILE.ps1|README.md
python3 -I tests/win/make_fixtures.py [--check]
source scripts/lj_guard.sh; lj_with_disk 275 wp01a-pwsh -- bash win/tools/fetch_pwsh.sh /home/user/build-scratch/pwsh
```

A tree without the pattern file ends `BLOCKED` (exit 3), never a silent pass.

## 3. Acceptance tests (the plan's list, in its order)

Real transcripts: `build/evidence/wp01a/acceptance_transcript.txt`, `tests_all.txt`, `fetch_pwsh_*`.

| # | Test | Result | Proof |
|---|---|---|---|
| 1 | `source scripts/lj_guard.sh; lj_with_disk 275 wp01a-pwsh -- bash win/tools/fetch_pwsh.sh <scratch>/pwsh` | **PASS** | exit 0. `lj_guard: wp01a-pwsh: planned 275 MB, Avail 778 MB, floor 400 MB, hard floor 250 MB`; `df (before): Avail 778 MB`; `size 75396784 bytes`; `computed: 1fd7983f...94e2fef`, `published:` identical, `MATCH`; `PowerShell 7.5.4`; `df (after): Avail 593 MB`; `lj_guard: ... finished with exit 0; Avail start 778 MB, min 553 MB, end 593 MB`. How I got there: the guard did not exist at first, so my first install used the script's own identical rule (`fetch_pwsh_run.txt`). When the guard landed, the literal command was **REFUSED** (`Avail 593 MB minus planned 275 MB leaves 318 MB, below the 400 MB floor`, `fetch_pwsh_guard_refusal.txt`), so I deleted my own 185 MB scratch install and ran the literal command again; it passed. Re-running on an installed tree is a no-op (`already installed and verified`, exit 0). |
| 2 | `bash tests/win/run_tests.sh --all` | **PASS**, exit 0 | `WP-01a all: PASS=93 FAIL=0 UNVERIFIED=1 SKIPPED=1 BLOCKED=0` |
| 3 | `ps_lint.py win/step0_pc_tests.ps1 && ps_parse.sh` | **PASS** | `TOTAL: 0 error(s), 0 warning(s)`; `PARSED 12 item(s), 0 parse error(s)` (the script and 11 README fences, pwsh 7.5.4) |
| 4 | `pwsh -File win/step0_pc_tests.ps1 -Out renders/wp01a/linux_report.json`, then the checker | **PASS** | exit 0, `files written: renders/wp01a/linux_report.json`, `os.platform` non-windows; checker: `NOT A WINDOWS REPORT: os.platform is non-windows ...`, `RESULT: exit 1` |
| 5 | gpu12_pro | **PASS** | exit 0; `gpu_tier gpu-8-12 NVIDIA, 12.0 GB read from nvidia-smi`; `ram_tier 16+ ... WSL2 ok`; `pro-or-higher ... BitLocker can be offered` |
| 6 | nogpu_home | **PASS** | exit 0; `gpu_tier none`, `ram_tier 8-15`, `edition home ... BitLocker not offered`, `RESULT: exit 0 ... A low tier is information, not a failure` |
| 7 | software_gpu | **PASS** | exit 0; `gpu_tier none` |
| 8 | vram_nvidia_over_cap | **PASS** | exit 0; `gpu-16+ ... 24.0 GB read from nvidia-smi` |
| 9 | vram_capped_only | **PASS** | exit 1; `FINDING: VRAM unreadable: AdapterRAM stops near 4 GB ...` |
| 10 | ffmpeg9 | **PASS** | exit 0; `ffmpeg 9.0.2 ... run the colour-patch test on this build` |
| 11 | craft_pins_mixed | **PASS** | exit 1; `photocraft match (0.10.0); vectorcraft MISMATCH (0.12.9); lightcraft absent; filmcraft fallback pin (0.8.0); effectcraft absent; soundcraft unpinned (learning only)` |
| 12 | identifying | **PASS** | exit 2; `category=email field=tools.git.notes hit=ta********`, `category=ipv4 field=notes[0] hit=10********`, `category=mac field=notes[3] hit=02********`, `category=profile_path_windows field=errors[0] hit=C:********`; the test asserts no planted value appears in the output, and that the documentation IPv4 and the reserved `.invalid` address are **not** hits |
| 13 | bom equals plain | **PASS** | same 18 table lines; UTF-16 with and without BOM (made with `iconv` at test time) give the same table, only the `encoding:` line differs |
| 14 | `--forbid exampleperson` on gpu12 | **PASS** | exit 0 |
| 15 | `--forbid zeta`, collision | **PASS** | exit 0; `NOTE category=user_name field=gpus[0].name hit=ze** (a hardware-name field: reported, not refused)` (and the `vendor` field) |
| 16 | `--forbid zeta`, leak | **PASS** | exit 2; `category=user_name field=tools.git.notes hit=ze**` |
| 17 | version strings shaped like IPv4 | **PASS** | exit 0 (needs the `field_exemptions` of the pattern file; the fixture has 4-part versions that are valid IPv4 shapes in `powershell.version`-class fields) |
| 18 | sha256_ok | **PASS** | exit 0 (64-hex exempt, in free text too) |
| 19 | hex65_leak | **PASS** | exit 2; `category=guid_serial field=notes[0] hit=3f********` |
| 20 | `--tier-json-out` | **PASS** | exit 0; validates against `pc_tier.schema.json` with the checker's own validator |
| 21 | Tier file leaks nothing | **PASS** | the test searches the tier file for the CPU and GPU names and every token of them of 4 characters or more, the driver version, OS caption/version/build, RAM, every disk size and free figure, and the tool versions: 0 found; `additionalProperties: false`; no `shared_pc_hint` (deviation D1) |
| 22 | Self-scan, script side, identifying fixture with invented names | **PASS** | exit 2; `REDACTION CHECK FAILED, nothing was written`; twelve `category=... field=... hit=...` lines including `user_name`, `computer_name`, `domain_name`; stdout contains none of the three invented names in full; `renders/wp01a/none.json` does not exist |
| 23 | Same, collision fixture | **PASS** | exit 0; two `NOTE` lines; `files written: renders/wp01a/collision.json`; the file's `redaction.name_hits_in_hardware_fields` holds the two notes |
| 24 | Same, leak fixture | **PASS** | exit 2; `category=user_name field=tools.git.notes hit=ze**`; no file |
| 25 | Fail closed | **PASS** | a copy of the kit without the pattern file: `step0` exits 2 with `REDACTION PATTERNS UNAVAILABLE, nothing was collected and nothing was written`, no output file; `windows_check.py` exits 2 and writes no `--tier-json-out` or `--json-out` file. Also a corrupt pattern file (exit 2 from both) and one lacking required categories (exit 2) |
| 26 | `public_lint.py --self-test` | **SKIPPED: `public_lint.py` not landed** | stand-in until then: the 100-sample Python / PowerShell agreement test above (0 disagreements) |
| 27 | No private identifying-data regex | **PASS** | a grep over `win/step0_pc_tests.ps1`, `win/tools/*`, `scripts/windows_check.py` for e-mail, IPv4, MAC, IPv6, GUID and profile-path regex shapes finds nothing. I also scanned every file I own with the real categories as a stand-in for `public_lint.py`: the only hits are the 65-hex fixture (expected) and `@PSBoundParameters` in a `.ps1` (code is not scanned for the `handle` category) |
| 28 | README test | **PASS** | `headings found: 9/9; powershell fences: 11; pattern categories scanned: 9; problems: 0`; referenced files exist; no handle, e-mail, IP or user path |
| 29 | Planted machine-scope `Set-ExecutionPolicy` | **PASS** | `ps_lint.py` exit 1 `[R13]` for a `.ps1`, for a `.md` fence, and for the real README with a block appended; `-Scope Process`, comments and quoted text pass |
| 30 | Directory hash before/after | **PASS** | the kit and fixtures hash identically before and after; the only new files are the three passing `-Out` files; the refusals created none |

Extra tests I added (all PASS): the Windows branches with mocks (`mock_windows.*`, 12 lines: nvidia-smi merge over a capped AdapterRAM, `qwMemorySize` read as a 64-bit number and as bytes, the CIM account fallback, drives without network / CD / null-size entries, screen mode and scale, a Craft scan with `FilmCraft-v0.8.0-win-x64` and `vectorcraft_0.13.1`, a failing step that continues with a scrubbed message, a real-mode user name in the CPU field as a note and in a drive field as a refusal); the local deny list in UTF-16 (checker and script); stdin; invalid JSON, schema-invalid and unknown-key input (the unknown key's name is not echoed); every nullable field set to null (48 cases, no crash); every fixture through the script's own scan (19 runs); a collision audit of 12 clean fixtures and the script's own note strings against ten default Windows names (this found D4); `fetch_pwsh.sh` refusals (relative path, unverified existing folder, disk rule with a fake `df`).

## 4. UNVERIFIED (also `build/evidence/wp01a/unverified.txt`, 15 groups)

Every CIM/WMI query and the registry reads (EditionID, UBR, display class `qwMemorySize`, `AppliedDPI`); `Get-LocalUser` on 5.1 and on 7; `System.Windows.Forms` screen count; `winget --version`, `wsl --status` (UTF-16 output and its English wording), `py -3 --version`; the `nvidia-smi` output format; Vulkan detection (a DLL on disk is only a hint); the `%TEMP%` default on a managed PC; Windows PowerShell 5.1 behaviour of every cmdlet and of `ConvertTo-Json`; execution-policy options A and B, `Unblock-File`, Group Policy; whether version strings on the maker's PC trip a pattern; process start with time limits through `System.Diagnostics.Process` on 5.1; the (J) thresholds in `tiers.json`; the six paste-in commands (parse-tested only, `Get-CimInstance` does not exist on Linux); the File Explorer instructions. The mock tests prove the script's own logic, not what Windows answers. Nothing could be run on Windows PowerShell 5.1 here; `ps_lint.py` and the parser on 7.5.4 are the available evidence.

## 5. Deviations from the plan, and why

- **D1. `shared_pc_hint` is not in `pc_tier.json`.** Fable's round-2 review (nudge 4) asked for it to be cut; the checker still prints it in the chat table. Plan text 4.16 lists it; the schema and file follow the nudge.
- **D2. Nudge 7 applied:** `windows_check.py` and the script read extra forbidden words from the git-ignored `scripts/public_lint.deny.local.txt` (category `local_deny`, whole word, any Notepad encoding in the checker). `--forbid` stays in the checker for container tests and is **not** in the maker README, which explains the deny file instead.
- **D3. The sixth paste-in command is `py -0`, not `py -0p`.** `py -0p` prints folder paths that normally contain the Windows user name, which would then sit in the chat. The README says why.
- **D4. `powershell.edition` is `WindowsPowerShell` / `PowerShell`, not PSEdition's `Desktop` / `Core`.** My collision audit showed that the word `Desktop` is the start of every default computer name (`DESKTOP-XXXXXXX`) and the 4.13 fragment rule would have refused the maker's first report on most PCs. Same key as 4.4, different label; the schema enumerates the two values.
- **D5. Exit code 3** from `windows_check.py` when its own `win/*.json` files are missing (4.3: environment problem). Pattern-file problems are still exit 2.
- **D6. The identifying fixture has a non-reserved invented address as its e-mail hit.** The plan asks for a `.invalid` address; WP-03's file (rightly) exempts the reserved documentation domains (`reserved_example_email_domains`), so a `.invalid` address is no hit. The fixture now carries one invented address on an unassigned domain (a hit) and one `.invalid` address (must not be a hit). Both are built from pieces so no source file contains an address.
- **D7. GPU tier for non-NVIDIA cards is capped at `gpu-low`** until a test says otherwise, because `playbooks/ai-imagery.md` Decision 2 names the 8 to 12 GB tier as Nvidia and its tools assume CUDA. It is data (`non_nvidia_max_tier`, null to remove). Marked (J).
- **D8. Blender floor** is judged on physical cores, RAM and VRAM; "below" is information, never a failure.
- **D9. magick, inkscape and blender are found by file and never started** (version from the file's resource). The plan's `tools` list gives each `{found, version, notes}` without saying they are run; starting Blender or Inkscape was not worth the risk.
- **D10. `-Out` creates a missing parent folder** and prints `created folder:` in the files-written line, so the plan's `-Out renders/wp01a/...` commands work on a fresh checkout. The default path (`%TEMP%`) always exists. Nothing else is ever created.
- **D11. `-PatternSelfTest` prints exactly one JSON object on stdout**; its `TEST MODE` banner goes to stderr so the object can be parsed. Other test modes print the banner on stdout.
- **D12. `files written:` is the last line printed**, as 4.7 says; the "Next:" advice comes just before it.
- **D13. Loader choices for the pattern file** (the file did not exist when I wrote the loaders; I wrote them from 4.13 and WP-02's reader, then ran them against the real file): accepted alternatives for the exemption keys, `placeholders` skipped, `mask.cap`, `name_checks.fragment_min_name_len` and the top-level `samples[]` with `parts` are all read. If a future version changes a key name, the loader fails closed or becomes stricter, never looser.

## 6. Requests and findings for the orchestrator and other packages

1. **WP-03 / `public_lint.py`:** `report_hex65_leak.json` contains a 65-character hex run in plain text (JSON cannot hide it) and must be treated as an expected hit. `path_denylist_exempt_dirs` already names `tests/win/fixtures/`; please confirm the text scan treats that folder the same way. Every other planted value in my fixtures is hidden with `\u` escapes, and every planted value in my sources is built from pieces.
2. **WP-03 / 4.13 and 4.4:** `field_exemptions` names `vulkan.devices[].driver_version`, but in 4.4 (and in my schema) `vulkan.devices[]` is a list of device-name strings, so that exemption never applies. Either 4.4 should say `devices[]` are objects or the exemption should go. Separately, `vulkan.devices[]` holds GPU names but is not in `hardware_name_fields`: a user name that collides with a Vulkan device string would refuse. Suggest adding it.
3. **Orchestrator:** `.gitignore` needs `pc_report*.json`, `*.local.*` (the deny list) and `logs/` (round-2 nudge 8); `renders/` is already ignored. Decide C-04 (second tools root `C:\LifeJourney\tools`: one line in `win/pins.json`, one in the script's fallback) and C-11 (the ai-photo skill's `hardware.md` fields: the checker writes the bucketed draft).
4. **Disk:** the shared volume dipped to about 130 MB free for a few minutes during my work (another job) and came back to about 600 MB; two of my test runs failed on write during the dip and passed when re-run. `<scratch>/pwsh` (185 MB) stays until `cleanup_scratch.sh`.
5. **Fable's Tuesday checklist (round-2 nudge 2)** is complete and passing: `step0_pc_tests.ps1`, `windows_check.py` (validate, scan, tier table, `--pattern-self-test`), `README-MAKER.md`, `ps_lint.py`, `ps_parse.sh`, `pins.json`, `tiers.json`, `pc_report.schema.json`, the fail-closed tests and the five redaction fixtures; the Friday items (`pc_tier.schema.json`, `--tier-json-out`, `--hardware-md`, `report_bom`, the UTF-16 test) are also done.

## 7. Known risks left open

- The first real Windows run may show a step `failed` (each is isolated and recorded in `errors[]`), a false refusal from the pattern file (the README tells the maker exactly what to paste), or a policy block (the README says to stop). The six paste-in commands are the last fallback.
- The name rule follows 4.13 literally (whole word plus 4-character fragments of names of 5 or more characters). Default Windows names (`Administrator`, `DESKTOP-ABC123`, `LAPTOP-...`) are audited against the clean fixtures and the script's own strings; a user whose name shares four letters with some other report text will see a refusal naming the category and field, by design. A hex-only fragment of a random computer name can coincide with part of the 64-hex ffmpeg hash by chance (about 0.4 percent for such a name); the refusal is safe, and WP-03 could exempt that one field from fragment matching.
- `ConvertTo-Json` and the CIM objects have only been exercised on pwsh 7.5.4 on Linux with mocks; the first Windows PowerShell 5.1 run is the first real test of both.
