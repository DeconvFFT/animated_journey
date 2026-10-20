#!/usr/bin/env python3
"""visual_app.py: SP1b for one of PhotoCraft, VectorCraft, LightCraft: T1 (smoke) then the read-backs, on the Linux CLI. Called by run_sp1b.sh inside its disk stage.

USAGE  python3 -I visual_app.py --app photocraft|vectorcraft|lightcraft --tag vX.Y.Z --cli ABSOLUTE_PATH --home DIR --work DIR [--plan-json JSON]
WRITES build/evidence/wp10/t1_<app>_<tag>.json and readback_<app>_<tag>.json (lj-evidence/1, every one labelled linux-cli: "Linux CLI result; not evidence for Windows").
EXIT CODES  0 T1 and the read-backs pass   1 a criterion failed (a finding about the app)   2 the harness could not drive the CLI (not a verdict on the app)
NEVER TOUCHES  anything outside --home, --work and the evidence folder. Only synthetic files are used.
"""
import argparse
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402
import t1_visual  # noqa: E402
import readback  # noqa: E402

L = B.L
READBACK = {"photocraft": readback.photocraft, "vectorcraft": readback.vectorcraft, "lightcraft": readback.lightcraft}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", required=True, choices=sorted(READBACK))
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cli", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--plan-json", default="{}")
    a = ap.parse_args(argv)
    if not os.path.isabs(a.cli) or not os.path.isfile(a.cli):
        print("ERROR: --cli must be an existing absolute path", file=sys.stderr)
        return 2
    name = "%s_%s" % (a.app, a.tag)
    rec = L.Recorder()
    extra = {"LIGHTCRAFT_GPU": "0"} if a.app == "lightcraft" else {}
    cli = L.Cli(a.cli, a.home, a.work, rec, rss_kill_mb=10240, timeout_s=300, extra_env=extra)
    sandbox = {"env": "env -i with HOME, TMPDIR, XDG_*, PATH only (LIGHTCRAFT_GPU=0 for LightCraft)", "network_isolation": "unshare -rn" if L.unshare_ok() else "not available",
               "timeout_s": 300, "rss_kill_mb": 10240, "vk_icd_filenames": "unset"}
    t1 = B.Checks()
    detail1 = t1_visual.run_t1(cli, a.app, a.tag, t1, rec)
    B.envelope("t1_" + name, t1.status(), "exit 0 where it has to work, the version names %s, the command listing is not trivial, no missing library or GPU error" % a.tag.lstrip("v"),
               "%d checks, %d failed%s" % (len(t1.rows), len(t1.problems), (": " + "; ".join(t1.problems)) if t1.problems else ""),
               extra=dict(detail1, checks=t1.rows, calls=list(rec.calls), sandbox=sandbox, profile="cli-member-only"))
    print("T1 %s: %s" % (name, t1.status()))
    if rec.calls and rec.calls[0]["rc"] in (126, 127, None):
        print("HARNESS ERROR: the CLI does not start at all (exit %s)" % rec.calls[0]["rc"])
        return 2
    rb, findings = B.Checks(), []
    print("Read-backs %s" % a.app)
    try:
        extra_detail = READBACK[a.app](cli, a.work, rb, findings) or {}
    except readback.HarnessError as e:
        print("HARNESS ERROR: %s" % e)
        B.envelope("readback_" + name, "UNVERIFIED", "read-backs measured", "the harness could not run them: %s" % L.scrub(str(e)),
                   notes="a harness problem, NOT a verdict on the app.", extra={"app": a.app, "tag": a.tag, "checks": rb.rows, "findings": findings, "calls": list(rec.calls)})
        return 2
    B.envelope("readback_" + name, rb.status(), "the playbook's read-back passes: the file is read, converted and written, the layer names or ids survive",
               "%d criteria, %d failed%s; %d findings%s" % (len(rb.rows), len(rb.problems), (": " + "; ".join(rb.problems)) if rb.problems else "", len(findings),
                                                        ("; HARNESS EXCEPTIONS (a driver bug, not a verdict): " + "; ".join(rb.harness)) if rb.harness else ""),
               extra=dict(extra_detail, app=a.app, tag=a.tag, checks=rb.rows, findings=findings, calls=list(rec.calls), sandbox=sandbox,
                          inputs="synthetic: WP-06 emitters and the reused fixtures of research/craft-visual-fixtures"))
    print("Read-back %s: %s" % (name, rb.status()))
    if rb.harness:
        return 2
    return 0 if not t1.problems and not rb.problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
