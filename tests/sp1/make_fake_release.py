#!/usr/bin/env python3
"""make_fake_release.py: build a small FAKE release tree for testing run_sp1.sh without the network (standard library only).

USAGE  python3 -I tests/sp1/make_fake_release.py --out DIR [--bug WORDS] [--bug-effect WORDS] [--flip-byte APP] [--big-gui-mb N]
Writes DIR/www/<app>/releases/download/<tag>/<asset> for the six pins of spikes/sp1_craft_cli/config.json: SHA256SUMS.txt, the Linux tarball, the Windows
portable zip and the MSI (all tiny stand-ins), and DIR/r8.json (the "independent" hashes, for LJ_SP1_R8). The FilmCraft and EffectCraft tarballs hold the
stand-in CLIs of tests/sp1/fake_craft/ (a Python script as bin/<app>-cli, a zero-filled bin/<app> standing in for the GUI, a LICENSE, a small lib/ file).
--bug puts words in the FilmCraft fake_bug.txt (leak offset dropframe offline dissolve crash stepped encodedblend); --bug-effect does the same for EffectCraft
(noalpha nondeterministic slow badprores nodecode oom). --bug and --bug-effect take effect only under run_sp1.sh --profile full (the lean plan does
not extract bin/fake_bug.txt). --flip-byte APP flips one byte of that tarball AFTER the sums were written (a corrupted download).
Serve DIR/www with: python3 -u -m http.server 0 --bind 127.0.0.1 --directory DIR/www   (the test runner does).
Nothing here is FilmCraft or EffectCraft, and no hash here is a real one.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import tarfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "spikes", "sp1_craft_cli", "config.json")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tarball(app, ver, bug_words, big_gui_mb):
    top = "%s-%s-linux-x86_64" % (app, ver)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=6) as tf:
        def add(name, data, mode=0o644):
            ti = tarfile.TarInfo("%s/%s" % (top, name))
            ti.size = len(data)
            ti.mode = mode
            ti.mtime = 1700000000
            tf.addfile(ti, io.BytesIO(data))
        cli = open(os.path.join(HERE, "fake_craft", "%s-cli" % app), "rb").read()
        add("bin/%s-cli" % app, cli, 0o755)
        add("bin/fake_bug.txt", (bug_words or "").encode())
        add("bin/fake_version.txt", ver.encode())
        add("bin/%s" % app, b"\0" * (big_gui_mb * 1048576), 0o755)
        add("lib/libfake.so", b"stand-in library\n" * 100)
        add("LICENSE", b"stand-in\n")
    return buf.getvalue()


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--bug", default="")
    ap.add_argument("--bug-effect", default="")
    ap.add_argument("--flip-byte", default="")
    ap.add_argument("--big-gui-mb", type=int, default=2)
    a = ap.parse_args(argv)
    cfg = json.load(open(CFG))
    www = os.path.join(a.out, "www")
    shutil.rmtree(a.out, ignore_errors=True)
    r8 = {"schema": "lj-r8-hashes/1", "source": "fake", "independence": "fake", "expected": [], "no_independent_value": [], "no_independent_value_note": "fake",
          "expected_linux_tarball_bytes": {}}
    for pin in cfg["pins"]:
        app, tag = pin["app"], pin["tag"]
        ver = tag.lstrip("v")
        d = os.path.join(www, app, "releases", "download", tag)
        os.makedirs(d)
        files = {}
        if app in ("filmcraft", "effectcraft"):
            words = a.bug if app == "filmcraft" else a.bug_effect
            files["%s-%s-linux-x86_64.tar.gz" % (app, ver)] = tarball(app, ver, words, a.big_gui_mb)
        else:
            files["%s-%s-linux-x86_64.tar.gz" % (app, ver)] = b"not downloaded by WP-07: %s\n" % app.encode() * 50
        files["%s-%s-windows-x64-portable.zip" % (app, ver)] = b"PK stand-in zip %s\n" % app.encode() * 20
        files["%s-%s-windows-x64.msi" % (app, ver)] = b"stand-in msi %s\n" % app.encode() * 20
        lines = []
        for name, data in sorted(files.items()):
            lines.append("%s  %s" % (sha(data), name))
        open(os.path.join(d, "SHA256SUMS.txt"), "w").write("\n".join(lines) + "\n")
        for name, data in files.items():
            if a.flip_byte == app and name.endswith(".tar.gz"):
                b = bytearray(data)
                b[len(b) // 2] ^= 0x01
                data = bytes(b)
            open(os.path.join(d, name), "wb").write(data)
        tb = "%s-%s-linux-x86_64.tar.gz" % (app, ver)
        zp = "%s-%s-windows-x64-portable.zip" % (app, ver)
        if app in ("filmcraft", "effectcraft"):
            r8["expected"].append({"app": app, "tag": tag, "kind": "linux_x86_64_tarball", "sha256": sha(files[tb]), "where": "fake"})
            r8["expected"].append({"app": app, "tag": tag, "kind": "windows_x64_portable_zip", "sha256": sha(files[zp]), "where": "fake"})
        else:
            r8["no_independent_value"].append("%s %s" % (app, tag))
        r8["expected_linux_tarball_bytes"]["%s %s" % (app, tag)] = len(files[tb])
    json.dump(r8, open(os.path.join(a.out, "r8.json"), "w"), indent=1)
    print("fake release tree under %s (%d pins)" % (a.out, len(cfg["pins"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
