"""t1_visual.py: SP1 test T1 (smoke) for PhotoCraft, VectorCraft and LightCraft on their Linux CLIs (R8 T1). Imported by visual_app.py.

Runs the CLI by absolute path in the sandbox (env -i, throw-away HOME, timeout, unshare -rn when it works, memory watchdog; VK_ICD_FILENAMES is unset because the
environment is empty): `--version`, the usage text, the command listing, and the libraries the binary links (readelf is a file parser: nothing is executed for it).
Pass: every call that has to work exits 0, the version names the tag, the command listing is not trivial, stderr names no missing library and no GPU or adapter failure.
A plain notice such as "no GPU found, using the CPU renderer" is expected in this container and is only recorded.
"""
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1b_lib as B  # noqa: E402

L = B.L

LISTING_TRIES = {
    "photocraft": [["commands", "--json"], ["commands"]],
    "vectorcraft": [["commands"]],
    "lightcraft": [["commands"], ["--help"], ["help"]],
}
MIN_ENTRIES = {"photocraft": 50, "vectorcraft": 20, "lightcraft": 8}


def count_entries(res):
    """(entries, how): JSON entries that carry an id or name when the output is JSON, else non-empty lines."""
    txt = res["stdout"].strip()
    try:
        obj = json.loads(txt)
    except ValueError:
        obj = None
    if obj is not None:
        n = sum(1 for d in L.walk(obj) if isinstance(d.get("id"), str) or isinstance(d.get("name"), str))
        if n:
            return n, "JSON entries with an id or name"
        if isinstance(obj, list):
            return len(obj), "JSON list items"
    return len([x for x in txt.splitlines() if x.strip()]), "non-empty lines"


def run_t1(cli, app, tag, ck, rec, env_extra=None):
    """Runs T1 and returns the detail dict for the evidence. `ck` is a sp1b_lib.Checks; `cli` a sp1_lib.Cli."""
    ver = tag.lstrip("v")
    detail = {"app": app, "tag": tag}
    print("T1 %s %s: libraries (readelf), --version, usage, command listing" % (app, tag))
    detail["needed_libraries"] = B.needed_libs(cli.binary)
    try:
        detail["cli_bytes"] = os.path.getsize(cli.binary)
        h = hashlib.sha256()
        with open(cli.binary, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        detail["cli_sha256"] = h.hexdigest()  # public build identity, not personal
    except OSError:
        pass
    v = cli.run(["--version"], "--version")
    ck.add("T1.version_exit0", v["rc"] == 0, "exit %s" % v["rc"])
    ck.add("T1.version_names_tag", ver in v["stdout"] + v["stderr"], (v["stdout"].strip() or v["stderr"].strip())[:90])
    detail["version_line"] = (v["stdout"].strip() or v["stderr"].strip())[:120]
    hlp = cli.run(["--help"], "--help")
    ht = hlp["stdout"] or hlp["stderr"]
    ck.add("T1.usage_text", hlp["rc"] in (0, 2) and len(ht.splitlines()) >= 5, "exit %s, %d lines" % (hlp["rc"], len(ht.splitlines())), "the CLI prints its usage")
    detail["help_excerpt"] = B.excerpt(ht, 1500)
    listing, how, tried = None, "", []
    for args in LISTING_TRIES[app]:
        r = cli.run(args, " ".join(args))
        tried.append("%s -> exit %s" % (" ".join(args), r["rc"]))
        n, how = count_entries(r)
        if r["rc"] == 0 and n >= 1:
            listing = (args, r, n)
            if n >= MIN_ENTRIES[app]:
                break
    if listing:
        args, r, n = listing
        ck.add("T1.command_listing", n >= MIN_ENTRIES[app], "`%s`: %d %s (mark: at least %d); tried %s" % (" ".join(args), n, how, MIN_ENTRIES[app], tried),
               "the command surface can be listed and is not trivial")
        detail["command_listing"] = {"args": args, "entries": n, "counted": how, "first_lines": [x[:100] for x in r["stdout"].splitlines()[:6]]}
    else:
        ck.add("T1.command_listing", False, "no listing command worked; tried %s" % tried, "the command surface can be listed")
    allerr = "\n".join(c.get("stderr_tail", "") for c in rec.calls) + "\n" + v["stderr"] + hlp["stderr"]
    bad = [p for p in B.BAD_STDERR if re.search(p, allerr, re.I)]
    notices = sorted({ln.strip()[:100] for ln in allerr.splitlines() if re.search(B.GPU_NOTICE, ln)})[:5]
    ck.add("T1.stderr_clean", not bad, "patterns matched: %s; GPU or CPU-renderer notices recorded, not failed: %s" % (bad or "none", notices or "none"),
           "no missing library, no GPU or adapter failure with VK_ICD_FILENAMES unset")
    detail["gpu_notices"] = notices
    return detail
