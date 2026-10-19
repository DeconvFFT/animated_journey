#!/usr/bin/env python3
"""t1_smoke.py: SP1 test T1 (smoke) for one Craft CLI.

USAGE  python3 -I t1_smoke.py --app filmcraft|effectcraft --tag vX.Y.Z --cli ABSOLUTE_PATH --home DIR --work DIR [--profile lean|full] [--plan-json JSON]
WHAT IT DOES  (R8 T1) runs the CLI by absolute path in the sandbox (env -i, throw-away HOME, timeout, unshare -rn when it works; VK_ICD_FILENAMES is
unset because the environment is empty): `--version`, the command list (first lines only), `info --json` (EffectCraft) or `--demo inspect sequence`
(FilmCraft), and `describe` of the commands the later tests use. It lists the libraries the binary links with readelf (a file parser: nothing is
executed for that). Pass: every call exits 0, the version contains the tag, and stderr names no missing library and no GPU or adapter failure.
WRITES  build/evidence/wp07/t1_<app>_<tag>.json (evidence envelope) and describe_<app>_<tag>.json (the parameter documents, small).
EXIT CODES  0 pass; 1 a check failed (a finding); 2 the harness could not run it.
NEVER TOUCHES  anything outside --home and --work, except the evidence files. It reads only synthetic or empty projects.
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402

DESCRIBE = {
    "filmcraft": ["file.newProject", "file.import", "file.newSequence", "timeline.place", "effects.setParam", "effects.setInterpolation",
                  "sequence.applyVideoTransition", "file.exportInterchange"],
    "effectcraft": ["comp.new", "layer.newText", "layer.newSolid", "layer.newShape", "layer.addShapeItem", "edit.pasteSvg", "layer.setSwitch",
                    "layer.newCamera", "prop.addKey", "prop.set"],
}
BAD_STDERR = [r"error while loading shared libraries", r"cannot open shared object", r"GLIBC_[0-9.]+' not found", r"panicked at",
              # a GPU or adapter ERROR; a plain notice such as "no GPU found, using the CPU renderer" is expected on this container and is only recorded
              r"(?i)(error|fail|fatal|panic|unable|cannot)[^\n]*(\bgpu\b|adapter|vulkan|wgpu)", r"(?i)(\bgpu\b|adapter|vulkan|wgpu)[^\n]*(error|fail|fatal|panic|unable|cannot)"]
GPU_NOTICE = r"(?i)(\bgpu\b|adapter|vulkan|wgpu|software|cpu)"


def needed_libs(path):
    try:
        p = subprocess.run(["readelf", "-d", path], capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    libs = re.findall(r"\(NEEDED\)\s+Shared library: \[([^\]]+)\]", p.stdout)
    return sorted(libs) if p.returncode == 0 else None


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", required=True, choices=("filmcraft", "effectcraft"))
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cli", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--profile", default="lean")
    ap.add_argument("--plan-json", default="{}")
    ap.add_argument("--mini", action="store_true", help="tests only: marks the envelope as a mechanism test against a stand-in CLI")
    a = ap.parse_args(argv)
    if not os.path.isabs(a.cli) or not os.path.isfile(a.cli):
        print("ERROR: --cli must be an existing absolute path", file=sys.stderr)
        return 2
    name = "%s_%s" % (a.app, a.tag)
    ver = a.tag.lstrip("v")
    rec = L.Recorder()
    cli = L.Cli(a.cli, a.home, a.work, rec, timeout_s=120)
    checks, problems = [], []

    def check(cid, ok, measured, note=""):
        checks.append({"id": cid, "pass": bool(ok), "measured": measured, "note": note})
        if not ok:
            problems.append("%s: %s" % (cid, measured))

    print("T1 %s %s: libraries (readelf), --version, command list, state query, describe" % (a.app, a.tag))
    libs = needed_libs(a.cli)
    v = cli.run(["--version"], "--version")
    check("T1.version_exit0", v["rc"] == 0, "exit %s" % v["rc"])
    check("T1.version_names_tag", ver in v["stdout"] + v["stderr"], (v["stdout"].strip() or v["stderr"].strip())[:80])
    if a.app == "filmcraft":
        cmds = cli.run(["commands"], "commands")
        info = cli.json(["--demo", "inspect", "sequence", "--compact"], "--demo inspect sequence --compact")
        info_ok = info["rc"] == 0 and info["json"] is not None
        info_label = "--demo inspect sequence prints JSON"
    else:
        cmds = cli.run(["commands"], "commands")
        info = cli.json(["info", "--json"], "info --json")
        info_ok = info["rc"] == 0 and info["json"] is not None
        info_label = "info --json prints JSON"
    lines = cmds["stdout"].splitlines()
    check("T1.commands_exit0", cmds["rc"] == 0, "exit %s, %d lines" % (cmds["rc"], len(lines)))
    check("T1.commands_list_not_trivial", len(lines) >= 20, "%d lines (the first 5: %s)" % (len(lines), " | ".join(x.strip()[:40] for x in lines[:5])))
    check("T1.state_query_ok", info_ok, "%s: exit %s" % (info_label, info["rc"]))
    desc, missing = {}, []
    for cid in DESCRIBE[a.app]:
        dres = cli.json(["describe", cid] if a.app == "filmcraft" else ["--json", "exec", "--list", "--filter", cid, "--schemas"], "describe " + cid)
        if dres["rc"] == 0 and dres["json"] is not None and cid in json.dumps(dres["json"]):
            desc[cid] = dres["json"]
        elif dres["rc"] == 0 and cid in dres["stdout"]:
            desc[cid] = {"text": dres["stdout"][:1500]}  # plain-text listing
        else:
            alt = cli.run(["commands", "--filter", cid] if a.app == "effectcraft" else ["commands", cid], "commands " + cid)  # the command list as a second source
            if alt["rc"] == 0 and cid in alt["stdout"]:
                desc[cid] = {"text": alt["stdout"][:1500], "note": "found in the command list; the parameter document was not available"}
            else:
                missing.append(cid)
    check("T1.describe_commands_known", not missing, "missing: %s" % (missing or "none"),
          "the later tests send parameters named in these documents; a missing command is a command-surface change")
    allerr = "\n".join(r.get("stderr_tail", "") for r in rec.calls) + "\n" + v["stderr"] + cmds["stderr"] + info["stderr"]
    bad = [p for p in BAD_STDERR if re.search(p, allerr, re.I)]
    notices = sorted({ln.strip()[:100] for ln in allerr.splitlines() if re.search(GPU_NOTICE, ln)})[:5]
    check("T1.stderr_clean", not bad, "patterns matched: %s; GPU or CPU-renderer notices recorded, not failed: %s" % (bad or "none", notices or "none"),
          "no missing library, no GPU or adapter failure with VK_ICD_FILENAMES unset")
    check("T1.every_call_exit0_or_listed", all(c["rc"] == 0 for c in rec.calls if not c["call"].startswith("describe")), [c["rc"] for c in rec.calls[:6]])
    L.write_json(os.path.join(L.EVID, "describe_%s.json" % name), {"schema": "lj-describe/1", "app": a.app, "tag": a.tag, "commands": desc, "missing": missing})

    status = "PASS" if not problems else "FAIL"
    if a.mini:
        status = "UNVERIFIED" if not problems else "FAIL"
    L.envelope("t1_" + name + ("_mini" if a.mini else ""), status, "exit 0 everywhere, the version names %s, no missing library or GPU error, the command list and a state query work" % ver,
               "%d checks, %d failed%s" % (len(checks), len(problems), (": " + "; ".join(problems)) if problems else ""),
               notes="Linux CLI only: a pass here proves nothing about Windows.",
               unverified_reasons=(["stand-in CLI: a mechanism test of the harness"] if a.mini else []) + ["Windows behaviour is not tested by a Linux CLI run"],
               extra={"app": a.app, "tag": a.tag, "profile": a.profile, "mini": a.mini, "checks": checks, "needed_libraries": libs, "calls": rec.calls,
                      "sandbox": {"env": "env -i with HOME, TMPDIR, XDG_*, PATH only", "network_isolation": "unshare -rn" if L.unshare_ok() else "not available",
                                  "vk_icd_filenames": "unset", "timeout_s": 120}})
    for c in checks:
        print("  %s  %s  %s" % ("PASS" if c["pass"] else "FAIL", c["id"], c["measured"]))
    print("T1 %s: %s" % (name, status))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
