# SP4 protocol: what does the container do while the session is idle?

*For the orchestrator. Armed by WP-10 on Mon 19 Oct 2026; nothing here has been run on the real question, because a package cannot make its own session idle (build plan F-07).
The tools (`job.sh`, `gaps.py`) are tested with fixture logs and a 60 s run; the experiment itself is yours.*

## The question

`playbooks/agent-pipeline.md` Step 3 lists SP4 as: "how the cloud container behaves when idle. Open question: does a running background job keep it awake?" The answer decides
whether a long job started in a session (a render shard run, a nightly batch) can be left to finish while the maker's tab is closed, or whether such work has to run while the
session is open and be resumable. Route A frames already resume after a kill (SP2, `a4`), so the cost of the "no" answer is known: shards are started again on return.

## Steps (about 40 minutes of the container's time, one evening of the maker's)

1. **Before.** In the session, record `df -h /` (Avail, Use%) and the date. Note the container is idle: no other job of yours is running.
2. **Start the probe** so it outlives the shell, from the repository root, with a log name you choose (the job prints the name to a stdout that `nohup` throws away, so name it yourself):
   `nohup bash spikes/sp4_idle/job.sh --out ../build-scratch/sp4/idle-1.log > /dev/null 2>&1 &`
   (`../build-scratch` is the scratch folder, written `<scratch>` in committed files.) It writes one line (an epoch second) every 10 s for 25 minutes (1,500 s), with a start line and an end line that carry
   `df` Avail. It writes under 1 MB, makes no network call, reads nothing personal and never overwrites a log (a second run needs a new name).
3. **Go idle.** Ask the maker to close the tab (the whole ask: "close this tab for the evening"; no project detail is needed). Leave the session idle for **at least 10 minutes**, and
   ideally the full 25 minutes of the job, so the log covers an idle stretch longer than any plausible timeout. Do not poke the session meanwhile (a message wakes it and spoils the test).
4. **Return.** Open the session again. Straight away run `python3 -I spikes/sp4_idle/gaps.py ../build-scratch/sp4/idle-1.log --json build/evidence/wp10/sp4_gaps.json` (the JSON keeps the numbers) and `df -h /`.
   If the job is still running the verdict is `running` (exit 3): wait for its end line and run it again.
5. **Read the verdict** (the table below), record it in `spikes/VERDICTS-W2.md` (row SP4: status Done, the verdict word, the maximum gap, the idle length, the date) and in
   `build/evidence/wp10/sp4_gaps.json`. Nothing else about the maker's evening is recorded.

## Reading the verdict

| `gaps.py` says | It means | What changes in the plan |
|---|---|---|
| **kept awake** (exit 0) | the job reached its end line and no gap was over 30 s: a running background job kept the container running while the tab was closed | long jobs may run unattended inside one session; keep shards of 10 minutes or less and resumable anyway (SP2 `a4`) |
| **paused** (exit 1) | the job reached its end, but one or more gaps over 30 s: the container was frozen and thawed. The longest gap is the freeze | a job makes progress only while the session is open; start shards on return, never rely on the night |
| **killed** (exit 1) | no end line and the log stops short (or ends with reason=term): the job was ended from outside | long jobs must be restartable from files on disk (they are: Route A resumes, the guard cleans up); the orchestrator restarts them on return and never assumes the night's work happened |
| **running** (exit 3) | the log is still being written | wait and read it again |

A single answer from one evening is one observation. If the verdict is surprising (a gap of exactly the job's own length, or a kill at a round number of minutes), repeat once.

## Observations while the test is still not run (dated; not the verdict)

*Tue 20 Oct 2026, from the orchestrator's sessions of that day, with the checkpoint commits as the dating evidence. Nothing here answers the question above, and no overnight run was started.*

* **The container restarted twice on Tue 20 Oct 2026, both times during long workflows.** The first restart was at about 01:56 UTC (the checkpoint commit `2fdbdb4`, 01:57, says "before container restart"; the SP3 run-2 report notes that the container then landed on a different CPU model). The second was at about 03:38 UTC (the running container's boot time reads 03:38 UTC; the checkpoint commit `3a500dd` is stamped 03:39 and says "before second container restart"). So the container that began at the first restart ran roughly 1 h 40 min, and the one that began at the second was still running at 05:57 UTC (at least 2 h 19 min). Two data points, no pattern.
* **Each restart ended every running workflow and every detached background job, while the files on disk survived.** Work resumed from the committed WIP checkpoints, because the workflows themselves were gone. The scratchpad's kept environments (created 18 Oct) are still there, so the disk outlived both restarts. Whether the disk survives a reclaimed container, a new one rather than a restarted one, is not shown.
* **What this is and is not.** The restarts happened in active sessions, so they are not the idle test, and their cause is unknown. In the table above the nearest reading is "killed" (ended from outside), with the same consequence: long jobs must be restartable from files on disk, and the night's work cannot be assumed to have happened. Whether a running job keeps an idle container awake is still open.
* **What it means for render shards (true whatever the cause):**
  1. **Short shards.** Keep each shard to 10 minutes or less of wall time, so a restart costs at most the shard in flight. The two lifetimes above prove no minimum, so no longer figure is safe.
  2. **Resumable frames.** Render in PNG shard mode (`pipeline/bin/render.mjs` writes each frame as `.tmp` then renames it, clears stale `.tmp` files and re-renders any incomplete PNG; SP2 `a4`), and start the same command again after a restart. Never leave a long job as one piped video process: video mode is one process and cannot resume (`pipeline/bin/README-render.md`).
  3. **State in git.** The shard plan, the exact command lines and the progress notes live in small text files that are committed, not in a running workflow or a background job's memory. Frames stay in the git-ignored `renders/` (no binaries in git), so a finished render that matters is copied to the maker's storage, since a reclaimed container may start empty.
  4. **Commit before long runs.** Make a WIP checkpoint commit (as `2fdbdb4` and `3a500dd` were) before starting anything longer than one shard.
  5. **Expect a different host after a restart.** SP3 run 2 was 1.96 to 2.06 times slower than run 1 after the first restart, so a shard is timed on the host it will run on and given margin.

## What was NOT done, and why (build plan WP-10 item 3)

- **(d) cold versus cached setup timing**: needs a second set-up of the toolchain on a fresh container, which needs the disk (the volume is at about 700 MB free) and a session restart; not run.
- **(e) the Gemini API key test**: a call to a third-party service. D-15 says nothing personal goes to a third-party service without the maker's recorded OK, and a test key would be a new account on the maker's behalf; not run, and not to be run without that OK.
- **(f) a 50 MB git push**: it would put 50 MB into a PUBLIC repository (D-26) that cannot be cleaned; not run. If the question matters, it can be asked of a scratch repository the maker creates for it, never of this one.

## Files

| File | What it is |
|---|---|
| `job.sh` | the probe: `--seconds` (default 1500), `--interval` (default 10), `--out`. Never overwrites a log. Prints the log's name as `<scratch>/sp4/...`. |
| `gaps.py` | the reader: maximum gap, every gap over `--gap-limit` (default 30 s), the verdict, exit 0 / 1 / 2 / 3. `--now EPOCH` and `--json OUT` for tests and for the evidence. |
| `tests/spikes/fixtures/log_*.txt` | synthetic logs: clean, a planted 5-minute gap, killed, ended by TERM, a 29 s hiccup, unreadable, still running. |
