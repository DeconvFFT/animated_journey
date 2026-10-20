#!/usr/bin/env python3
"""make_fake_release.py: build a small FAKE release tree for testing run_sp1b.sh without the network (standard library only).

USAGE  python3 -I tests/spikes/make_fake_release.py --out DIR [--bug-photo WORDS] [--bug-vector WORDS] [--bug-light WORDS] [--flip-byte APP] [--flip-kept] [--cli-pad-mb N]
Writes DIR/www/<app>/releases/download/<tag>/<asset> for PhotoCraft, VectorCraft, LightCraft and FilmCraft (the pins of spikes/sp1_craft_cli/release_assets.json), each tarball holding the
stand-in CLI of tests/spikes/fake_craft/ as bin/<app>-cli (a Python script with its planted-defect words baked in), a zero-filled bin/<app> standing in for the GUI, and a small share/ file;
DIR/release_assets.json (the table, for LJ_SP1_ASSETS) and DIR/kept/<filmcraft tarball> (what WP-07 would have kept). --flip-byte APP flips one byte of that app's served tarball AFTER the sums
were written; --flip-kept does the same to the kept FilmCraft copy. Nothing here is a Craft app and no hash here is a real one.
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
PINS = [("photocraft", "v0.10.0"), ("vectorcraft", "v0.13.1"), ("lightcraft", "v0.9.1"), ("filmcraft", "v0.9.0")]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tarball(app, ver, bug, gui_mb=3, pad_mb=0):
    top = "%s-%s-linux-x86_64" % (app, ver)
    src = open(os.path.join(HERE, "fake_craft", app + "-cli"), "r", encoding="utf-8").read()
    src = src.replace('BUG = os.environ.get("FAKE_BUG", "")', 'BUG = %r' % bug)
    if pad_mb:
        src += "\n# " + "\0" * (pad_mb * 1048576) + "\n"   # a big CLI member that compresses to nothing: the exact need after the download exceeds the estimate
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=6) as tf:
        def add(name, data, mode=0o644):
            ti = tarfile.TarInfo("%s/%s" % (top, name))
            ti.size = len(data)
            ti.mode = mode
            ti.mtime = 1700000000
            tf.addfile(ti, io.BytesIO(data))
        add("bin/%s-cli" % app, src.encode("utf-8"), 0o755)
        add("bin/%s" % app, b"\0" * (gui_mb * 1048576), 0o755)
        add("share/doc/LICENSE", b"stand-in\n")
    return buf.getvalue()


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--bug-photo", default="")
    ap.add_argument("--bug-vector", default="")
    ap.add_argument("--bug-light", default="")
    ap.add_argument("--flip-byte", default="")
    ap.add_argument("--flip-kept", action="store_true")
    ap.add_argument("--cli-pad-mb", type=int, default=0, help="pad every stand-in CLI with this many MB of zero bytes")
    a = ap.parse_args(argv)
    shutil.rmtree(a.out, ignore_errors=True)
    bugs = {"photocraft": a.bug_photo, "vectorcraft": a.bug_vector, "lightcraft": a.bug_light, "filmcraft": ""}
    pins = []
    for app, tag in PINS:
        ver = tag.lstrip("v")
        d = os.path.join(a.out, "www", app, "releases", "download", tag)
        os.makedirs(d)
        name = "%s-%s-linux-x86_64.tar.gz" % (app, ver)
        data = tarball(app, ver, bugs[app], pad_mb=a.cli_pad_mb)
        good = data
        if a.flip_byte == app:
            b = bytearray(data)
            b[len(b) // 2] ^= 0x01
            data = bytes(b)
        open(os.path.join(d, name), "wb").write(data)
        open(os.path.join(d, "SHA256SUMS.txt"), "w").write("%s  %s\n" % (sha(good), name))
        pins.append({"app": app, "tag": tag, "role": "pin", "linux_x86_64_tarball": {"name": name, "bytes": len(good), "sha256": sha(good)}})
        if app == "filmcraft":
            os.makedirs(os.path.join(a.out, "kept"))
            kept = bytearray(good)
            if a.flip_kept:
                kept[len(kept) // 2] ^= 0x01
            open(os.path.join(a.out, "kept", name), "wb").write(bytes(kept))
    json.dump({"schema": "lj-release-assets/1", "usable": True, "pins": pins, "soundcraft": {"status": "not pinned, not fetched"}}, open(os.path.join(a.out, "release_assets.json"), "w"), indent=1)
    print("fake release tree under %s (%d pins)" % (a.out, len(pins)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
