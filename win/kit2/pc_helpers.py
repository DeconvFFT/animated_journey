#!/usr/bin/env python3
"""pc_helpers.py: two small standard-library helpers for the kit-2 scripts (WP-09). READ-ONLY apart from the one file you name.

  clip         make a 3-second test clip with ffmpeg alone: a built-in test picture (lavfi testsrc2) and a quiet 1 kHz tone,
               encoded through the project's h264_online chain (pipeline/lib/chains.json), so spec_check.py has something
               to look at that the PC's own ffmpeg made. Nothing of yours is read.
  merge-chains write ONE chain file that holds the chains of pipeline/lib/chains.json plus the chains of a second chain
               file (the phone file), so colour_patch.py can test all of them in one run and write one raw record.
  tone-filter  print the audio filter used for the test tone (the tests read it).

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows; no admin rights; nothing is installed, downloaded or changed)
  py -3 -I win\\kit2\\pc_helpers.py clip --ffmpeg C:\\Tools\\ffmpeg\\bin\\ffmpeg.exe --out clip.mp4
  py -3 -I win\\kit2\\pc_helpers.py merge-chains --out chains_all.json [--extra pipeline\\phone\\profile.json]

WHAT IT PRINTS. One line per action ("clip: ...", "merge-chains: ..."), file names by base name only, then "ok". It writes only
the file named by --out. Exit codes (build plan 4.3): 0 ok, 2 bad usage or invalid input, 3 environment problem (ffmpeg not
found, chain file missing, ffmpeg failed).
UNVERIFIED on Windows until the maker runs it; the logic is plain subprocess with an argument list and os.path.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_CHAINS = os.path.join(REPO, "pipeline", "lib", "chains.json")
DEFAULT_PHONE = os.path.join(REPO, "pipeline", "phone", "profile.json")

FPS = 24
# The test tone: a 1 kHz sine at the level that reads -16 LUFS integrated (the online profile's target, W-19) on ffmpeg's ebur128 over
# the whole clip, with a true peak far under -1 dBTP. TONE_GAIN_DB is applied to lavfi `sine` (whose own amplitude is 1/8) after
# the mono source is made stereo. It was calibrated on ffmpeg 6.1.1 by the tests in tests/win_kit2/ (the measured value is recorded
# in build/evidence/wp09/); the PC's ffmpeg is judged by spec_check.py with +-1 LU of tolerance.
TONE_FREQ = 1000
TONE_GAIN_DB = 5.1


class Usage(Exception):
    """Bad usage or invalid input (exit 2)."""


class EnvError(Exception):
    """Missing tool or a failed run (exit 3)."""


def say(msg=""):
    print(msg)
    sys.stdout.flush()


def tone_source(seconds):
    """The lavfi source text for the tone (stereo 48 kHz)."""
    return "sine=frequency=%d:sample_rate=48000:duration=%s" % (TONE_FREQ, seconds)


def tone_filter():
    """The -af text that turns the mono sine into the -16 LUFS stereo test tone."""
    return "aformat=sample_fmts=fltp:channel_layouts=stereo,volume=%sdB" % TONE_GAIN_DB


def resolve_exe(name):
    if not name:
        return None
    if os.path.sep in name or (os.path.altsep and os.path.altsep in name) or os.path.isabs(name):
        return name if os.path.isfile(name) else None
    return shutil.which(name)


def read_chains(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
    except (OSError, ValueError):
        raise EnvError("cannot read the chain file %s (download the WHOLE project folder, not single files)" % os.path.basename(path))
    if not isinstance(d, dict) or not isinstance(d.get("chains"), dict):
        raise Usage("%s is not a chain file (an object with a \"chains\" object)" % os.path.basename(path))
    return d


def make_clip(ffmpeg, out, chains_path, seconds=3):
    """Encode `seconds` of testsrc2 + tone through h264_online. Returns the ffmpeg command used (argument list)."""
    d = read_chains(chains_path)
    ch = d["chains"].get("h264_online")
    if not ch:
        raise Usage("the chain file has no h264_online chain")
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y",
           "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=%d:duration=%s" % (FPS, seconds),
           "-f", "lavfi", "-i", tone_source(seconds),
           "-vf", ch["vf"], "-af", tone_filter()]
    cmd += list(ch["video_args"]) + list(ch["audio_args"]) + ["-t", str(seconds), out]
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    except OSError:
        raise EnvError("cannot run ffmpeg")
    except subprocess.TimeoutExpired:
        raise EnvError("ffmpeg took more than 5 minutes for a 3-second clip")
    if p.returncode != 0 or not os.path.isfile(out):
        tail = p.stderr.decode("utf-8", "replace").strip().splitlines()[-3:]
        raise EnvError("ffmpeg could not make the clip: %s" % " | ".join(t[:160] for t in tail))
    return cmd


def merge_chains(out, base_path, extra_path):
    base = read_chains(base_path)
    chains = dict(base["chains"])
    added = []
    if extra_path:
        extra = read_chains(extra_path)
        for name, ch in extra["chains"].items():
            if name in chains:
                raise Usage("the chain %s is defined in both chain files" % name)
            chains[name] = ch
            added.append(name)
    doc = {"schema": base.get("schema", "lj-chains/1"), "chains": chains,
           "note": "merged at run time from the project's chain files; holds chain definitions only"}
    tmp = out + ".part"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:      # BOM-less UTF-8, LF
        json.dump(doc, f, indent=1, ensure_ascii=True)
        f.write("\n")
    os.replace(tmp, out)
    return sorted(chains), added


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pc_helpers.py", description="Kit-2 helpers (WP-09). See the header of this file.")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("clip", help="make a 3-second test clip with the PC's ffmpeg")
    c.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"))
    c.add_argument("--out", required=True)
    c.add_argument("--chains-file", default=DEFAULT_CHAINS)
    c.add_argument("--seconds", type=int, default=3)
    m = sub.add_parser("merge-chains", help="write one chain file from the project's chain files")
    m.add_argument("--out", required=True)
    m.add_argument("--base", default=DEFAULT_CHAINS)
    m.add_argument("--extra", default=None, help="a second chain file (for example pipeline/phone/profile.json); skipped with a note if it is missing")
    sub.add_parser("tone-filter", help="print the audio filter text of the test tone")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "tone-filter":
            say(tone_filter())
            return 0
        if a.cmd == "clip":
            ffmpeg = resolve_exe(a.ffmpeg)
            if not ffmpeg:
                raise EnvError("ffmpeg not found (%s)" % os.path.basename(a.ffmpeg))
            if not 1 <= a.seconds <= 30:
                raise Usage("--seconds must be between 1 and 30")
            say("clip: making a %d-second test clip (built-in test picture and a quiet tone) with this ffmpeg, through the h264_online chain ..." % a.seconds)
            make_clip(ffmpeg, a.out, a.chains_file, a.seconds)
            say("clip: wrote %s (%d bytes)" % (os.path.basename(a.out), os.path.getsize(a.out)))
            say("ok")
            return 0
        if a.cmd == "merge-chains":
            extra = a.extra
            if extra and not os.path.isfile(extra):
                say("merge-chains: %s was not found, so its chains are skipped (the project's own chains are still tested)" % os.path.basename(extra))
                extra = None
            names, added = merge_chains(a.out, a.base, extra)
            say("merge-chains: wrote %s with %d chains (%d from the second file)" % (os.path.basename(a.out), len(names), len(added)))
            say("ok")
            return 0
        ap.print_usage(sys.stderr)
        return 2
    except Usage as e:
        print("pc_helpers: %s" % e, file=sys.stderr)
        return 2
    except EnvError as e:
        print("pc_helpers: environment problem: %s" % e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
