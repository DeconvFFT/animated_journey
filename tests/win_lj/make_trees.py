#!/usr/bin/env python3
"""make_trees.py DEST: build the synthetic folder trees that the lj.ps1 tests walk (WP-01b).

Everything is invented and tiny: plain text files with made-up names, nothing that looks like a photo, nothing
personal. DEST must be outside the repository (the runner uses <scratch>/wp01b-trees). The script only ever
deletes a DEST that carries its own marker file, and it never follows symbolic links when it does.

Trees (all under DEST):
  planted/    the root the tests point lj.ps1 close at. Holds the planted targets (xmp sidecars under work/,
              Recovery / Auto-Save / cache folders under tools/), canaries that must never be listed
              (media/, archive/, masters/, originals/, work/media/, another git repository, an encrypted
              container file) and links (a link to a folder outside, a link to a file outside, a broken link,
              a link named Recovery that points outside).
  outside/    sits next to planted/; the links point here. Nothing in it may ever be listed.
  appdata/    stand-ins for %APPDATA% (Roaming) and %LOCALAPPDATA% (Local).
  fakehome/   stand-in profile folder (fakehome/user1) used by the "root is the profile root" tests.
  empty/      a root with nothing to remove.
It also writes DEST/expected.json: the exact would-remove list the planted tree should produce.
"""
import json
import os
import shutil
import sys

MARKER = ".lj-win-lj-trees"


def w(path, text="synthetic placeholder\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return len(text.encode("utf-8"))


def d(path):
    os.makedirs(path, exist_ok=True)


def link(target, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.symlink(target, path)


def main(argv):
    if len(argv) != 1:
        print("usage: make_trees.py DEST", file=sys.stderr)
        return 2
    dest = os.path.abspath(argv[0])
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if dest == repo or dest.startswith(repo + os.sep):
        print("make_trees: DEST must be outside the repository", file=sys.stderr)
        return 2
    if os.path.lexists(dest):
        if not os.path.isfile(os.path.join(dest, MARKER)):
            print("make_trees: DEST exists and is not one of these trees; refusing to delete it", file=sys.stderr)
            return 2
        shutil.rmtree(dest)  # rmtree removes links, it does not follow them
    d(dest)
    w(os.path.join(dest, MARKER), "created by tests/win_lj/make_trees.py\n")

    out = os.path.join(dest, "outside")
    w(os.path.join(out, "OUTSIDE-CANARY.xmp"))
    w(os.path.join(out, "secret.xmp"))
    w(os.path.join(out, "Recovery", "OUTSIDE-CANARY-recovery.dat"))

    R = os.path.join(dest, "planted")
    expected = []  # (relative path with / separators, kind, files, bytes)

    def want(rel, kind, files, nbytes):
        expected.append({"path": rel, "kind": kind, "files": files, "bytes": nbytes})

    # --- planted xmp sidecars under work/
    b = w(os.path.join(R, "work", "ch01", "scan-0001.xmp"), "x" * 100)
    want("work/ch01/scan-0001.xmp", "xmp", 1, b)
    b = w(os.path.join(R, "work", "ch01", "scan-0002.XMP"), "y" * 2048)
    want("work/ch01/scan-0002.XMP", "xmp", 1, b)
    w(os.path.join(R, "work", "ch01", "scan-0001.dat"))                       # not a target
    b = w(os.path.join(R, "work", "ch02", "deep", "a", "b", "shot-0003.xmp"), "z" * 10)
    want("work/ch02/deep/a/b/shot-0003.xmp", "xmp", 1, b)
    w(os.path.join(R, "work", "ch02", "notes.txt"))                           # not a target
    awkward = "[draft] #1 $x `a'.xmp"
    b = w(os.path.join(R, "work", "ch03", awkward), "q" * 7)
    want("work/ch03/" + awkward, "xmp", 1, b)
    b = w(os.path.join(R, "work", "ch03", "unicode-é-0004.xmp"), "u" * 33)
    want("work/ch03/unicode-é-0004.xmp", "xmp", 1, b)
    w(os.path.join(R, "stray.xmp"))                                           # xmp outside any work folder: not a target
    w(os.path.join(R, "tools", "photocraft-0.10.0", "stray.xmp"))             # xmp under tools: not a target in v0

    # --- canaries inside the work area that must be protected
    w(os.path.join(R, "work", "media", "CANARY-nested-media.xmp"))
    # --- links
    d(os.path.join(R, "work"))
    link("../../outside", os.path.join(R, "work", "link-out"))
    link("../../outside/secret.xmp", os.path.join(R, "work", "link-file.xmp"))
    link("../../nonexistent.xmp", os.path.join(R, "work", "broken.xmp"))

    # --- planted tools: Recovery / Auto-Save / cache
    base = os.path.join(R, "tools")
    n = 0
    b1 = w(os.path.join(base, "photocraft-0.10.0", "Recovery", "autosave-0001.dat"), "a" * 1000)
    b2 = w(os.path.join(base, "photocraft-0.10.0", "Recovery", "autosave-0002.dat"), "b" * 3000)
    want("tools/photocraft-0.10.0/Recovery", "Recovery", 2, b1 + b2)
    sizes = [w(os.path.join(base, "filmcraft-0.9.0", "Auto-Save", "p-%03d.dat" % i), "c" * (500 * i)) for i in (1, 2, 3)]
    want("tools/filmcraft-0.9.0/Auto-Save", "Auto-Save", 3, sum(sizes))
    w(os.path.join(base, "filmcraft-0.9.0", "Recovery", "media", "CANARY-held.dat"))   # Recovery holding a protected folder: HELD
    s1 = w(os.path.join(base, "lightcraft-0.9.1", "cache", "thumbs", "0001.dat"), "t" * 700)
    s2 = w(os.path.join(base, "lightcraft-0.9.1", "cache", "thumbs", "0002.dat"), "t" * 900)
    want("tools/lightcraft-0.9.1/cache", "cache", 2, s1 + s2)
    rb = w(os.path.join(base, "lightcraft-0.9.1", "LightCraftData", "recent.json"), "[]\n")
    want("tools/lightcraft-0.9.1/LightCraftData/recent.json", "lightcraft/recent_files", 1, rb)
    t1 = w(os.path.join(base, "lightcraft-0.9.1", "LightCraftData", "thumbcache", "t1.dat"), "m" * 111)
    t2 = w(os.path.join(base, "lightcraft-0.9.1", "LightCraftData", "thumbcache", "t2.dat"), "m" * 222)
    want("tools/lightcraft-0.9.1/LightCraftData/thumbcache", "lightcraft/cache", 2, t1 + t2)
    link("../../../outside/Recovery", os.path.join(base, "vectorcraft-0.13.1", "Recovery"))   # a link named Recovery pointing outside
    d(os.path.join(base, "effectcraft-0.11.1", "cache"))                                      # empty cache folder
    want("tools/effectcraft-0.11.1/cache", "cache", 0, 0)
    link("../../../../outside/secret.xmp", os.path.join(base, "effectcraft-0.11.1", "Recovery", "link-inside"))  # Recovery holding a link: HELD
    s3 = w(os.path.join(base, "soundcraft-0.8.0", "Cache", "x.dat"), "s" * 64)                 # capital C: names are matched without case
    want("tools/soundcraft-0.8.0/Cache", "Cache", 1, s3)
    w(os.path.join(base, "RECOVERY-notes.txt"))                                              # a file, not a folder: ignored

    # --- canaries that must never be listed
    for name in ("media", "archive", "masters", "originals"):
        w(os.path.join(R, name, "CANARY-%s-1.dat" % name))
        w(os.path.join(R, name, "work", "CANARY-%s-2.xmp" % name))
        w(os.path.join(R, name, "Recovery", "CANARY-%s-3.dat" % name))
    w(os.path.join(R, "vault.hc"), "not a real container\n")
    w(os.path.join(R, "otherrepo", ".git", "HEAD"), "ref: refs/heads/main\n")
    w(os.path.join(R, "otherrepo", "work", "CANARY-otherrepo.xmp"))
    w(os.path.join(R, "cache", "CANARY-rootcache.dat"))        # a cache folder that is NOT under tools: left alone

    # --- appdata stand-ins
    A = os.path.join(dest, "appdata")
    w(os.path.join(A, "Roaming", "PhotoCraft", "recent.json"), "[]\n")
    w(os.path.join(A, "Local", "PhotoCraft", "Recovery", "r1.dat"), "r" * 300)
    w(os.path.join(A, "Roaming", "Microsoft", "CANARY-not-an-app-folder.dat"))
    # --- fake profile
    d(os.path.join(dest, "fakehome", "user1"))
    w(os.path.join(dest, "fakehome", "user1", "Documents", "CANARY-profile.dat"))
    # --- empty root
    d(os.path.join(dest, "empty"))
    # --- a root that is a link, and a root with a .git folder (for the refusal tests)
    link("planted", os.path.join(dest, "root-link"))
    w(os.path.join(dest, "gitroot", ".git", "HEAD"), "ref: refs/heads/main\n")

    # --- config used with the env-variable test (the committed planted.config.json has no env variables)
    cfg = {
        "schema": "lj-config/1", "root": "planted", "tools_root": "tools",
        "apps": {
            "photocraft": {"status": "UNVERIFIED",
                           "recent_files": ["%APPDATA%/PhotoCraft/recent.json"],
                           "cache": ["%LOCALAPPDATA%/PhotoCraft/Recovery", "%APPDATA%/Microsoft"]}
        }
    }
    with open(os.path.join(dest, "planted_appdata.config.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

    with open(os.path.join(dest, "expected.json"), "w", encoding="utf-8") as f:
        json.dump({"schema": "lj-win-lj-expected/1", "note": "paths are relative to planted/; with the committed planted.config.json",
                   "would_remove": sorted(expected, key=lambda e: e["path"].lower())}, f, indent=2, ensure_ascii=False)
    print("built synthetic trees under DEST (planted, outside, appdata, fakehome, empty, gitroot, root-link)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
