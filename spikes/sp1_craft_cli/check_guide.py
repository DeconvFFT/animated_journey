#!/usr/bin/env python3
"""check_guide.py: checks MAKER-CRAFT-ZIPS.md against release_assets.json and against its own safety rules (standard library only).

USAGE  python3 -I spikes/sp1_craft_cli/check_guide.py [--guide FILE] [--assets FILE] [--json OUT]
CHECKS (one line each: PASS, FAIL or UNVERIFIED with the reason)
  G1  every PowerShell fence carries a mode marker (<!-- lj:mode=readonly --> or setup) and is ASCII
  G2  every fence parses with the real PowerShell parser (pwsh 7: System.Management.Automation.Language.Parser); UNVERIFIED if pwsh is not found
  G3  every fence passes win/tools/ps_lint.py (the Windows PowerShell 5.1 rules): readonly fences in its read-only mode, setup fences with --allow-write
  G4  every file name, size and SHA-256 in the guide equals release_assets.json; every 64-hex string in the guide is a known hash; all five pins and the fallback appear
  G5  the Step 3 hash-check fence, run on Linux against made-up files: an intact file prints OK, a copy with ONE BYTE FLIPPED prints MISMATCH, a missing one MISSING
  G6  the two "where did it write" fences, run on Linux against a made-up profile (including an AppData folder OUTSIDE the profile): every output line starts with
      %USERPROFILE%\\ (or <app folder>), and neither the made-up profile path nor the made-up user name appears; the fences are read-only (the tree is unchanged)
  G7  a tarball with one byte flipped is rejected by asset_tool.py before any extraction, and run_sp1.sh calls the check before its first tar -x
EXIT CODES  0 no FAIL (UNVERIFIED lines allowed); 1 a FAIL; 2 bad usage.
NEVER TOUCHES  anything but a temporary folder under the scratch area, removed again. Windows behaviour stays UNVERIFIED: pwsh on Linux is a proxy.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "drivers"))
import sp1_lib as L  # noqa: E402

FENCE = re.compile(r"(?P<marker><!--\s*lj:mode=(?P<mode>\w+)(?P<attrs>[^>]*)-->\s*\n)?```(?P<lang>[A-Za-z0-9]*)[ \t]*\n(?P<body>.*?)\n```", re.S)
results = []


def rec(cid, status, text):
    results.append({"id": cid, "status": status, "text": text})
    print("%-10s %s  %s" % (status, cid, text))


def find_pwsh():
    for c in (os.environ.get("PWSH"), os.path.join(L.SCRATCH, "pwsh", "pwsh"), shutil.which("pwsh")):
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def run_pwsh(pw, script_text, env_extra=None, timeout=120):
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp"), "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "POWERSHELL_TELEMETRY_OPTOUT": "1"}
    env.update(env_extra or {})
    p = subprocess.run([pw, "-NoProfile", "-NonInteractive", "-Command", script_text], capture_output=True, text=True, env=env, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def fences(text):
    out = []
    for m in FENCE.finditer(text):
        if m.group("lang") in ("powershell", "pwsh", "ps1"):
            attrs = m.group("attrs") or ""
            kind = re.search(r"lj:kind=(\w+)", attrs)
            out.append({"mode": m.group("mode"), "kind": kind.group(1) if kind else None, "body": m.group("body"), "line": text[:m.start()].count("\n") + 1})
    return out


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--guide", default=os.path.join(HERE, "MAKER-CRAFT-ZIPS.md"))
    ap.add_argument("--assets", default=L.ASSETS_FILE)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    try:
        text = open(a.guide, "r", encoding="utf-8").read()
        assets = L.read_json(a.assets)
    except (OSError, ValueError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    fs = fences(text)
    tmp = tempfile.mkdtemp(prefix="wp07-check-", dir=L.SCRATCH if os.path.isdir(L.SCRATCH) else None)
    try:
        # G1
        bad = [f["line"] for f in fs if f["mode"] not in ("readonly", "setup")]
        nonascii = [i for i, ch in enumerate(text) if ord(ch) > 127]
        rec("G1.fences_marked_and_ascii", "PASS" if fs and not bad and not nonascii else "FAIL",
            "%d PowerShell fences; without a mode marker: %s; non-ASCII characters: %d" % (len(fs), bad or "none", len(nonascii)))
        files = []
        for i, f in enumerate(fs):
            p = os.path.join(tmp, "fence%02d_%s.ps1" % (i, f["mode"]))
            with open(p, "w", encoding="ascii", errors="replace", newline="\n") as fh:
                fh.write(f["body"] + "\n")
            files.append((p, f))
        # G2
        pw = find_pwsh()
        if pw:
            script = ("$bad = 0; foreach ($p in $args) { }; " +
                      "$list = @(" + ",".join("'%s'" % p for p, _ in files) + "); foreach ($p in $list) { $t = $null; $e = $null; "
                      "[System.Management.Automation.Language.Parser]::ParseFile($p, [ref]$t, [ref]$e) | Out-Null; "
                      "if ($e.Count -gt 0) { $bad++; 'PARSE ERROR in ' + (Split-Path $p -Leaf) + ': ' + $e[0].Message } }; 'parse errors: ' + $bad")
            rc, out, err = run_pwsh(pw, script)
            ok = rc == 0 and out.strip().endswith("parse errors: 0")
            rec("G2.pwsh_parses_every_fence", "PASS" if ok else "FAIL", "pwsh 7 Parser::ParseFile on %d fences: %s" % (len(files), out.strip().splitlines()[-1] if out.strip() else err[:200]))
        else:
            rec("G2.pwsh_parses_every_fence", "UNVERIFIED", "pwsh was not found (run win/tools/fetch_pwsh.sh); G3 is the only syntax gate then")
        # G3
        lint = os.path.join(REPO, "win", "tools", "ps_lint.py")
        if os.path.exists(lint):
            fails = []
            for p, f in files:
                cmd = [sys.executable, "-I", lint] + (["--allow-write"] if f["mode"] == "setup" else []) + [p]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    fails.append("%s: %s" % (os.path.basename(p), (r.stdout + r.stderr).strip().splitlines()[0:2]))
            rec("G3.ps51_lint_every_fence", "PASS" if not fails else "FAIL", "%d fences linted (readonly fences in read-only mode); problems: %s" % (len(files), fails or "none"))
        else:
            rec("G3.ps51_lint_every_fence", "UNVERIFIED", "win/tools/ps_lint.py is not present")
        # G4
        known = {}
        for pin in assets["pins"]:
            for k in ("linux_x86_64_tarball", "windows_x64_portable_zip", "windows_x64_msi"):
                known[pin[k]["name"]] = (pin[k]["sha256"], pin[k].get("bytes"))
        problems = []
        pairs = re.findall(r"`?([a-z]+-[0-9.]+-windows-x64-portable\.zip)`?\s*\|\s*([0-9.]+)\s*\|\s*`([0-9a-f]{64})`", text)
        if len(pairs) != 6:
            problems.append("table has %d file rows, expected 6" % len(pairs))
        for name, mb, h in pairs:
            if name not in known:
                problems.append("unknown file name " + name)
            else:
                if known[name][0] != h:
                    problems.append("%s: hash differs from release_assets.json" % name)
                if known[name][1] and abs(float(mb) - known[name][1] / 1048576.0) > 0.06:
                    problems.append("%s: size %s MB differs from %.1f" % (name, mb, known[name][1] / 1048576.0))
        for name, h in re.findall(r"'([a-z]+-[0-9.]+-windows-x64-portable\.zip)'\s*=\s*'([0-9a-f]{64})'", text):
            if name not in known or known[name][0] != h:
                problems.append("fence entry %s does not match release_assets.json" % name)
        allhex = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", text))
        allknown = {v[0] for v in known.values()} | {p["sums_file_sha256"] for p in assets["pins"]}
        stray = sorted(h[:12] for h in allhex - allknown)
        if stray:
            problems.append("64-hex strings that are not in release_assets.json: %s" % stray)
        for pin in assets["pins"]:
            z = pin["windows_x64_portable_zip"]["name"]
            if z not in text:
                problems.append("%s is not in the guide" % z)
        rec("G4.names_sizes_hashes_match_assets", "PASS" if not problems else "FAIL", "%d table rows, %d distinct 64-hex strings; problems: %s" % (len(pairs), len(allhex), problems or "none"))
        # G5 (pwsh): the hash-check fence against made-up files
        hashfence = next((f for f in fs if "Get-FileHash" in f["body"] and f["mode"] == "readonly"), None)
        if pw and hashfence:
            d = os.path.join(tmp, "dl")
            os.makedirs(d)
            intact, flipped = b"made-up zip content\n" * 500, None
            flipped = bytearray(intact)
            flipped[len(flipped) // 2] ^= 0x01
            open(os.path.join(d, "a-1.0.0-windows-x64-portable.zip"), "wb").write(intact)
            open(os.path.join(d, "b-1.0.0-windows-x64-portable.zip"), "wb").write(bytes(flipped))
            h = hashlib.sha256(intact).hexdigest()
            body = re.sub(r"\$want = \[ordered\]@\{.*?\n\}", "$want = [ordered]@{\n    'a-1.0.0-windows-x64-portable.zip' = '%s'\n    'b-1.0.0-windows-x64-portable.zip' = '%s'\n    'c-1.0.0-windows-x64-portable.zip' = '%s'\n}" % (h, h, h), hashfence["body"], flags=re.S)
            body = body.replace("C:\\lj\\dl", d)
            rc, out, err = run_pwsh(pw, body)
            lines = [x.split() for x in out.strip().splitlines()]
            got = {x[1]: x[0] for x in lines if len(x) >= 2}
            ok = got.get("a-1.0.0-windows-x64-portable.zip") == "OK" and got.get("b-1.0.0-windows-x64-portable.zip") == "MISMATCH" and got.get("c-1.0.0-windows-x64-portable.zip") == "MISSING"
            rec("G5.hash_fence_rejects_one_flipped_byte", "PASS" if ok else "FAIL", "intact -> %s, one byte flipped -> %s, missing -> %s (pwsh on Linux, made-up files; Windows UNVERIFIED)" % (
                got.get("a-1.0.0-windows-x64-portable.zip"), got.get("b-1.0.0-windows-x64-portable.zip"), got.get("c-1.0.0-windows-x64-portable.zip")))
        else:
            rec("G5.hash_fence_rejects_one_flipped_byte", "UNVERIFIED", "pwsh not found or the hash fence is missing")
        # G6 (pwsh): the where-did-it-write fences
        wa = next((f for f in fs if f["kind"] == "where_appdata"), None)
        wf = next((f for f in fs if f["kind"] == "where_appfolder"), None)
        if pw and wa and wf:
            user = "Zq7MadeUpUser"
            prof = os.path.join(tmp, "Users", user)
            roam = os.path.join(prof, "AppData", "Roaming")
            loc_outside = os.path.join(tmp, "redirected", "Local")  # an AppData that lives OUTSIDE the profile
            appdir = os.path.join(tmp, "tools", "filmcraft-v0.9.0")
            for p in (os.path.join(roam, "FilmCraft", "data"), os.path.join(roam, "Temp", "x"), os.path.join(loc_outside, "FilmCraft", "Recovery"), os.path.join(appdir, "data")):
                os.makedirs(p)
            open(os.path.join(appdir, "filmcraft.exe"), "w").write("x")
            open(os.path.join(appdir, "data", "preferences.json"), "w").write("{}")
            snap = sorted(os.path.join(r, n) for r, ds, fn in os.walk(tmp) for n in ds + fn)
            env = {"APPDATA": roam, "LOCALAPPDATA": loc_outside, "USERPROFILE": prof}
            rc1, out1, err1 = run_pwsh(pw, wa["body"], env)
            body2 = re.sub(r"\$app = '[^']*'", "$app = '%s'" % appdir, wf["body"], count=1)
            rc2, out2, err2 = run_pwsh(pw, body2, env)
            lines1 = [x for x in out1.splitlines() if x.strip()]
            lines2 = [x for x in out2.splitlines() if x.strip()]
            leaks = [x for x in lines1 + lines2 if user in x or tmp in x or "Zq7" in x]
            form1 = [x for x in lines1 if not x.startswith("%USERPROFILE%\\")]
            form2 = [x for x in lines2 if not x.startswith("<app folder>")]
            temp_listed = [x for x in lines1 if re.search(r"[\\/]Temp([\\/]|$)", x)]
            after = sorted(os.path.join(r, n) for r, ds, fn in os.walk(tmp) for n in ds + fn)
            ok = rc1 == 0 and rc2 == 0 and lines1 and lines2 and not leaks and not form1 and not form2 and not temp_listed and snap == after
            rec("G6.where_did_it_write_prints_only_generalised_paths", "PASS" if ok else "FAIL",
                "line 1 printed %d lines, line 2 printed %d; not in %%USERPROFILE%% form: %s; leaks of the made-up profile or user: %s; Temp listed: %s; tree unchanged: %s; exit %s/%s %s" % (
                    len(lines1), len(lines2), (form1 + form2)[:3] or "none", leaks[:3] or "none", temp_listed or "none", snap == after, rc1, rc2, (err1 + err2)[:150].strip()))
        else:
            rec("G6.where_did_it_write_prints_only_generalised_paths", "UNVERIFIED", "pwsh not found or the two where-did-it-write fences are missing")
        # G7: Linux side, tarball integrity before extraction
        ok7, msg7 = linux_flip_check(tmp)
        rec("G7.flipped_tarball_rejected_before_extraction", "PASS" if ok7 else "FAIL", msg7)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if a.json:
        L.write_json(a.json, {"schema": "lj-guide-check/1", "guide": "spikes/sp1_craft_cli/MAKER-CRAFT-ZIPS.md", "date_utc": L.today(), "results": results})
    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    print("check_guide: %d PASS, %d FAIL, %d UNVERIFIED" % (sum(r["status"] == "PASS" for r in results), n_fail, sum(r["status"] == "UNVERIFIED" for r in results)))
    return 1 if n_fail else 0


def linux_flip_check(tmp):
    """A made-up release asset table and tarball; the same file with one byte flipped must be REJECTED by asset_tool.py verify (exit 1, nothing extracted);
    and in run_sp1.sh the verify call must come before the first tar extraction."""
    import io
    import tarfile
    d = os.path.join(tmp, "flip")
    os.makedirs(d)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        data = b"made-up cli\n" * 200
        ti = tarfile.TarInfo("filmcraft-0.9.0-linux-x86_64/bin/filmcraft-cli")
        ti.size = len(data)
        tf.addfile(ti, io.BytesIO(data))
    good = buf.getvalue()
    h = hashlib.sha256(good).hexdigest()
    pin = {"app": "filmcraft", "tag": "v0.9.0", "version": "0.9.0", "role": "pin",
           "linux_x86_64_tarball": {"name": "filmcraft-0.9.0-linux-x86_64.tar.gz", "sha256": h, "bytes": len(good)},
           "windows_x64_portable_zip": {"name": "z", "sha256": "0" * 64, "bytes": 1}, "windows_x64_msi": {"name": "m", "sha256": "1" * 64, "bytes": 1}}
    assets = os.path.join(d, "assets.json")
    json.dump({"schema": "lj-release-assets/1", "pins": [pin]}, open(assets, "w"))
    gp = os.path.join(d, "good.tar.gz")
    bp = os.path.join(d, "bad.tar.gz")
    open(gp, "wb").write(good)
    b = bytearray(good)
    b[len(b) // 2] ^= 0x01
    open(bp, "wb").write(bytes(b))
    env = dict(os.environ, LJ_SP1_ASSETS=assets, LJ_SP1_R8="none", LJ_SP1_EVIDENCE=d)
    tool = os.path.join(HERE, "drivers", "asset_tool.py")
    rg = subprocess.run([sys.executable, "-I", tool, "verify", gp, "filmcraft", "v0.9.0"], capture_output=True, text=True, env=env)
    rb = subprocess.run([sys.executable, "-I", tool, "verify", bp, "filmcraft", "v0.9.0"], capture_output=True, text=True, env=env)
    lines = open(os.path.join(HERE, "run_sp1.sh"), encoding="utf-8").read().splitlines()
    v = next((i for i, x in enumerate(lines) if 'asset_tool.py" verify' in x), None)
    t = next((i for i, x in enumerate(lines) if re.search(r"\btar -xzf\b", x) and not x.lstrip().startswith("#")), None)
    order = v is not None and t is not None and v < t
    ok = rg.returncode == 0 and rb.returncode == 1 and "REJECTED" in rb.stdout and "Nothing was extracted" in rb.stdout and order
    return ok, "intact tarball -> exit %s (%s); one byte flipped -> exit %s (%s); verify call at run_sp1.sh line %s precedes the first tar -xzf at line %s: %s" % (
        rg.returncode, rg.stdout.strip()[:20], rb.returncode, rb.stdout.strip()[:60], (v or 0) + 1, (t or 0) + 1, order)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
