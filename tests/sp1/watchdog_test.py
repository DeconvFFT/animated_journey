#!/usr/bin/env python3
"""watchdog_test.py: the resident-memory watchdog and the wall-clock kill of sp1_lib.run_watched, tested with a small allocator (standard library only).
Prints PASS or FAIL lines; exit 0 if all pass. A process that grows past the limit is killed in a few seconds; a quiet one is not; a sleeper is stopped
by the wall clock; the figures (max RSS from the kernel, polled RSS) are plausible. Uses at most 350 MB of memory for a few seconds and no disk."""
import os
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "spikes", "sp1_craft_cli", "drivers"))
import sp1_lib as L  # noqa: E402

GROW = ("import time\nb=[]\nfor i in range(35):\n    x=bytearray(10*1024*1024)\n    for k in range(0,len(x),4096): x[k]=1\n    b.append(x)\n    time.sleep(0.15)\ntime.sleep(20)\n")
QUIET = "import time\nx=bytearray(20*1024*1024)\nfor k in range(0,len(x),4096): x[k]=1\ntime.sleep(0.5)\n"
SLEEP = "import time\ntime.sleep(60)\n"


def run(code, **kw):
    d = tempfile.mkdtemp(prefix="wd_", dir=L.SCRATCH if os.path.isdir(L.SCRATCH) else None)
    try:
        return L.run_watched([sys.executable, "-I", "-c", code], d, os.path.join(d, "o"), os.path.join(d, "e"), **kw)
    finally:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        os.rmdir(d)


ok = True


def check(name, cond, detail):
    global ok
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    ok = ok and cond


r = run(GROW, rss_kill_mb=150)
check("watchdog.kills_above_limit", r["killed"] == "rss-watchdog" and r["wall_s"] < 15 and r["polled_rss_mb"] >= 150, "killed by %s after %.1f s, polled peak %.0f MB, kernel max %.0f MB" % (r["killed"], r["wall_s"], r["polled_rss_mb"], r["max_rss_mb"]))
r = run(QUIET, rss_kill_mb=150)
check("watchdog.leaves_a_quiet_process", r["killed"] is None and r["rc"] == 0 and 15 < r["max_rss_mb"] < 120, "exit %s, kernel max %.0f MB, polled %.0f MB" % (r["rc"], r["max_rss_mb"], r["polled_rss_mb"]))
r = run(SLEEP, rss_kill_mb=150, wall_s=2)
check("watchdog.wall_clock_kill", r["killed"] == "wall-clock" and r["wall_s"] < 8, "killed by %s after %.1f s" % (r["killed"], r["wall_s"]))
sys.exit(0 if ok else 1)
