# Agent-on-PC rules

*Written 2026-10-18 by the Fable advisor from `DECISIONS.md` W-28 (critic gap 5). These rules bind any agent that runs a command on the maker's Windows PC, whether through a remote-device tool, a scheduled script or a command the maker pastes. They apply only if the read-only probe in W-28 succeeds; until then creator-threads Exit B stands and no agent touches the PC.*

1. **Separate account.** Every agent command runs under the project's own Windows account (W-26), never the maker's personal account and never one she shares.
2. **No family media.** An agent never opens, lists, previews, hashes, copies or uploads a file inside the VeraCrypt container or any folder holding her photographs, audio or video. The container stays dismounted while an agent session is open; `lj.ps1 run <shot>` is started by the maker's hand, and the agent reads only the validator JSON and the `preview` proxy it writes back (W-23, W-24).
3. **No screenshots, no screen reading.** No desktop screenshot, screen recording or OCR of the display. Test cards and synthetic material are the only images an agent may be shown from the PC.
4. **Claude app closed during renders.** Renders and Blender timings run with the Claude desktop app closed (D-10); the agent reads the result afterwards from the files named in the brief.
5. **Read-only first.** The first call in any session is read-only (`step0_pc_tests.ps1`, `ffmpeg -version`, `windows_check.py`). Anything that writes runs only from a script already committed to the repo, with its README, and never writes outside `C:\lj\` or the repo clone.
6. **A log of every command.** Every command and its exit code is appended to `logs/agent-on-pc.jsonl` (no user name, no machine name, no path under the personal profile), committed at `lj.ps1 close` (W-26).
7. **No names.** Output committed to the repo carries no Windows user name, PC name, Wi-Fi name or family name (`maker-pc.json` and `windows_check_report.json` are scrubbed before commit; agent-pipeline Pitfall 10).
8. **Nothing installed, nothing upgraded.** No package, app, driver or Craft build is installed or upgraded by an agent; pins are frozen Sun 25 Oct (W-22) and the maker runs every installer.
9. **Secrecy checks first.** The shared-library check ("unknown counts as yes") and the Mum-test on the device run before any scan, render or upload (W-26); if either fails, the agent stops and writes it down.
10. **Stop on doubt.** Any prompt, dialog, file name or window the agent did not expect ends the session; the agent reports it in the next review and the maker decides.

A violation of any rule is logged as a slip (D-19), stops agent access to the PC until the maker re-enables it in `decisions.csv`, and is read by Fable at the next gate.
