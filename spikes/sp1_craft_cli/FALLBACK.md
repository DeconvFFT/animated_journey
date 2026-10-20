# SP1 fallback: if the Craft downloads are blocked (or the CLIs fail in the container)

*Written in advance (Mon 19 Oct 2026) so the decision does not have to be made under pressure. It follows build plan WP-07 item 4 and ROADMAP 5.2. `blocked_proof.json` is the evidence that triggers it.*

## When this applies

Either of these is the trigger:

1. **A download is blocked.** `run_sp1.sh` stops with exit 3 and writes `build/evidence/wp07/blocked_proof.json`: the URL (no query string), the HTTP status, curl's exit code, **curl's stderr word for word**, the HTTP status lines the proxy and GitHub returned, and the time. It never records the proxy address or credentials. One example of the file's shape is made by the test `blocked.force_bad_asset` (a deliberately wrong asset name gives HTTP 404, curl exit 22, "The requested URL returned error: 404").
2. **A hash does not match.** That is not a blocked download; it is a stop-and-report. `asset_tool.py verify` prints `REJECTED`, nothing is extracted, and `release_assets.json` says `usable: false` if the mismatch is in the table. `--all` stops at once: the 0.8.0 fallback is not fetched and EffectCraft is not started (the fallback exists only for a 0.9.0 that passed the hash and failed T1 or T2); the stage envelope says `FAIL`, "hash mismatch (stop and report)"; run_sp1.sh exits 1. A corrupt tarball in `vendor/craft/_keep/` is the one exception that heals itself: it is deleted, fetched again once and the ledger records the exception. Nobody builds on a mismatching file until the orchestrator has looked.

(Today, Mon 19 Oct, downloads are reachable: the release assets answer 302 and then 200. The proof path exists because the proxy may change.)

## What happens instead

- **SP1 becomes maker-PC evidence only.** The Sat 24 Oct five-minute tests (`MAKER-CRAFT-ZIPS.md`) are the only evidence about the Craft apps. They already cover everything the apps need to be pinned: version, signature, pass or fail, memory, and where each app writes.
- **The container renders with ffmpeg, Pillow and Chromium** (Route A and the photo-motion chains of `playbooks/agent-pipeline.md`). **The Craft CLIs are not used in the container.** Nothing in the plan depends on them there.
- **ROADMAP 5.2 stays as the table says** ("Craft CLIs: only if SP1 T2/T4 pass"): they stay off the container's render path.
- **FilmCraft and EffectCraft stay maker-side refinement tools** (D-11: agents generate, apps refine), reached through the OTIO / FCP7 XML hand-off bundle and `lj.ps1 run <shot>` on the PC (W-23), never as a render engine in the cloud.
- **WP-10 does the same for the other three apps:** their tarballs are fetched there once; if they are blocked, its T1 and read-backs move to the maker's PC and are marked `BLOCKED`, not `PASS`.
- **No new dependency is created.** The release table (`release_assets.json`) and the Windows guide do not need the Linux tarballs at all: the six `SHA256SUMS.txt` files are enough for the maker's hash checks.

## What to do next, in order

1. Read `blocked_proof.json`. Is it a 403 or 407 from the proxy (a policy denial: do not retry, report it), a 404 (the asset name or tag is wrong: check the tag with the maker's release page), or a timeout (retry once later, within the download allowance of 2,560 MB, raised from 2,048 MB on 2026-10-20)?
2. Do not look for another route to the same files (no mirror, no other host). A policy denial is an answer.
3. Mark T1, T2 and T4 in `VERDICT-SP1A.md` as `NOT RUN: download blocked` with the proof file named, and say in the decision paragraph that the R8 rule was not applied.
4. Tell the maker nothing changes for Saturday: the guide and the five-minute tests are unaffected.

## If the CLIs download fine but fail

That is a **result**, not a block. T2 failing means FilmCraft stays maker-side and the container renders with ffmpeg and code. T4 failing on memory or speed means EffectCraft is limited to titles and line-draw on the maker's PC. Both are written in `VERDICT-SP1A.md` by `drivers/verdict.py` from the measurements, and neither changes any date in the plan.
