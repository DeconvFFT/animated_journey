#!/usr/bin/env python3
"""mo8_gate.py: the MO8 motion gate (W-41). Does a slow push-in or pull-out move smoothly at the sub-pixel level?

It WRAPS the reused audit script research/cinematic-quality-fixtures/mo8_audit.py: it runs that file in place with
`python3 -I -B` (never copied, never edited, no bytecode files written beside it), reads the two fourth-difference estimators the register names, and applies the gates:
  MO8a   mo8a_d4_px  centre jitter of the fitted x/y translation, in 1080p pixels   gate: at most 0.05 px
  MO8b   mo8b_d4_px  edge-equivalent zoom jitter (zoom-rate residual x 960 px)       gate: at most 0.04 px
  MO8c   roughness (mo8c_rough)  INFORMATIONAL only; the "1.3 x a Pillow reference" ratio is informational too (W-41)
The gate is a number from pixels, so it does not care which tool made the move. Measured on this container: a Pillow
resize(box) sub-pixel push reads about 0.003 px (passes); an ffmpeg zoompan push from a 1080p picture reads about 0.6 px (fails).

IT APPLIES TO THE MASTER BEFORE THE DELIVERY ENCODE (W-41). Give it a folder of numbered PNG frames, or a clip made with the
ffv1_lossless or prores422hq_master chain. A clip that is already H.264 is measured too, but the result is approximate (the codec
adds up to about 0.015 px) and the verdict says so; never judge a render by its delivery file when the master exists.

CLIP LENGTH (RAM). mo8_audit loads every frame at 1920x1080 into memory (about 6 MB a frame, twice over while it decodes), so the
default limit is 96 frames (a 4 s push at 24 fps, the length the thresholds were set on). A longer input is REFUSED with a message, not
truncated silently: cut a window of at most 96 frames (for example  ffmpeg -i IN -frames:v 96 -c:v ffv1 OUT.mkv ). --max-frames can raise
the limit up to a hard ceiling of 120 frames; anything over 120 is always refused. Fewer than 12 frames is refused too (the fourth
difference needs a run of frames).

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows; needs ffmpeg, numpy and Pillow for the audit it wraps)
  python3 -I pipeline/validators/mo8_gate.py renders/push_frames/            a folder of numbered PNGs
  python3 -I pipeline/validators/mo8_gate.py master_push.mkv --json OUT.json
  Options: --ffmpeg PATH (also FFMPEG), --max-frames N (96, at most 120), --a-limit 0.05, --b-limit 0.04, --json OUT.json,
           --audit PATH (default research/cinematic-quality-fixtures/mo8_audit.py beside the repo root)

WHAT IT PRINTS. One block per input: frames, input kind, MO8a / MO8b with limit and PASS / FAIL, roughness (information), ease class,
RESULT. The JSON (schema lj-mo8gate/1) has the same numbers. Inputs are named by base name only. It writes only the file named by --json.

EXIT CODES (build plan 4.3)  0 every input passes both gates   1 an input fails a gate   2 bad usage or a refusal (too many or too few
frames, not a clip or a PNG folder)   3 environment problem (ffmpeg, numpy, Pillow or the audit script missing, or the audit crashed)
UNVERIFIED on Windows until the maker runs it. Verified on ffmpeg 6.1.1, Python 3.13, numpy 2.5, Pillow 12.3 (Linux).
"""
import argparse
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys

TOOL_VERSION = 1
SCHEMA = "lj-mo8gate/1"
A_LIMIT = 0.05
B_LIMIT = 0.04
DEFAULT_MAX = 96
HARD_MAX = 120
MIN_FRAMES = 12
LOSSLESS_CODECS = {"ffv1", "prores", "rawvideo", "png", "utvideo", "huffyuv", "ffvhuff"}


class Usage(Exception):
    """Bad usage or a refusal (exit 2)."""


class EnvError(Exception):
    """Missing tool or a crashed audit (exit 3)."""


def say(msg=""):
    print(msg)
    sys.stdout.flush()


def write_json(path, obj):
    text = json.dumps(obj, indent=2, ensure_ascii=True) + "\n"
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def resolve_exe(name):
    if not name:
        return None
    if os.path.sep in name or (os.path.altsep and os.path.altsep in name) or os.path.isabs(name):
        return name if os.path.isfile(name) else None
    return shutil.which(name)


def default_audit():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "..", "research", "cinematic-quality-fixtures", "mo8_audit.py"))


def run(cmd, env=None, timeout=900):
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=timeout)
    except FileNotFoundError:
        raise EnvError("cannot run %s (not found)" % os.path.basename(str(cmd[0])))
    except subprocess.TimeoutExpired:
        raise EnvError("the audit timed out")
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ffprobe_for(ffmpeg):
    d, b = os.path.split(ffmpeg)
    if b.lower().startswith("ffmpeg"):
        sib = os.path.join(d, "ffprobe" + b[len("ffmpeg"):])
        if os.path.isfile(sib):
            return sib
    return shutil.which("ffprobe")


def probe_clip(ffmpeg, path):
    """frames (packet count), codec name, pixel size."""
    ffprobe = ffprobe_for(ffmpeg)
    if not ffprobe:
        raise EnvError("ffprobe not found (it ships beside ffmpeg)")
    rc, out, err = run([ffprobe, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=codec_name,width,height,nb_read_packets", "-of", "json", path], timeout=300)
    if rc != 0:
        raise Usage("%s is not a video ffprobe can read" % os.path.basename(path))
    try:
        s = json.loads(out)["streams"][0]
        return int(s["nb_read_packets"]), s.get("codec_name"), (s.get("width"), s.get("height"))
    except (ValueError, KeyError, IndexError):
        raise Usage("%s has no readable video stream" % os.path.basename(path))


def describe_input(ffmpeg, path, max_frames):
    """Return (kind, frame_count, note) or raise Usage for a refusal."""
    base = os.path.basename(path.rstrip("/\\"))
    if os.path.isdir(path):
        n = len(glob.glob(os.path.join(path, "*.png")))
        if n == 0:
            raise Usage("%s: no .png frames in that folder" % base)
        kind, note = "png-folder", "a folder of PNG frames is the best input: it is the master itself"
    elif os.path.isfile(path):
        n, codec, _size = probe_clip(ffmpeg, path)
        if codec in LOSSLESS_CODECS:
            kind, note = "lossless-or-intermediate-clip (%s)" % codec, "a lossless / ProRes clip: good, this is a master"
        else:
            kind = "lossy-clip (%s)" % codec
            note = ("this clip is lossy (%s), so it is a delivery-style encode: the codec adds up to about 0.015 px to the numbers. "
                    "The gate applies to the master BEFORE the delivery encode (W-41); measure the master when you have it." % codec)
    else:
        raise Usage("%s: not a file or a folder" % base)
    if n < MIN_FRAMES:
        raise Usage("%s has %d frame(s); at least %d are needed for the fourth-difference estimate" % (base, n, MIN_FRAMES))
    if n > max_frames:
        raise Usage("%s has %d frames, over the limit of %d. mo8_audit loads every frame into memory (about 6 MB each at 1080p), "
                    "so cut a window of at most %d frames, for example: ffmpeg -i IN -frames:v %d -c:v ffv1 OUT.mkv"
                    % (base, n, max_frames, max_frames, min(max_frames, DEFAULT_MAX)))
    return kind, n, note


def audit(audit_path, ffmpeg, path):
    env = dict(os.environ)
    env["FFMPEG"] = ffmpeg
    cmd = [sys.executable, "-I", "-B", audit_path, "--no-h264", path]      # -B: no .pyc files written next to the reused scripts
    rc, out, err = run(cmd, env=env)
    rec = None
    for ln in out.splitlines()[::-1]:
        ln = ln.strip()
        if ln.startswith("{"):
            try:
                rec = json.loads(ln)
                break
            except ValueError:
                continue
    if rc != 0 or rec is None:
        tail = (err.strip().splitlines() or ["no message"])[-1][:200]
        if "numpy" in err or "PIL" in err:
            raise EnvError("the audit needs numpy and Pillow (%s)" % tail)
        raise EnvError("the audit failed (exit %d): %s" % (rc, tail))
    return rec


def gate_one(args, ffmpeg, path):
    base = os.path.basename(path.rstrip("/\\"))
    kind, n, note = describe_input(ffmpeg, path, args.max_frames)
    rec = audit(args.audit, ffmpeg, path)
    a, b = rec.get("mo8a_d4_px"), rec.get("mo8b_d4_px")
    if a is None or b is None or a != a or b != b:       # None or NaN
        raise EnvError("the audit gave no usable fourth-difference numbers for %s" % base)
    a_ok, b_ok = a <= args.a_limit, b <= args.b_limit
    res = {"input": base, "input_kind": kind, "frames": n, "master_before_encode": kind.startswith("png") or kind.startswith("lossless"),
           "mo8a_d4_px": a, "mo8a_limit": args.a_limit, "mo8a_pass": a_ok,
           "mo8b_d4_px": b, "mo8b_limit": args.b_limit, "mo8b_pass": b_ok,
           "informational": {"mo8c_rough": rec.get("mo8c_rough"), "mo8a_centre_jit_px_9frame": rec.get("mo8a_centre_jit_px"),
                             "mo8b_edge_jit_px_9frame": rec.get("mo8b_edge_jit_px"), "zoom_total_pct": rec.get("zoom_total_pct"),
                             "ease_class": rec.get("ease_class")},
           "note": note, "verdict": "PASS" if (a_ok and b_ok) else "FAIL"}
    return res


def print_one(r):
    say("mo8_gate: %s  (%d frames, %s)" % (r["input"], r["frames"], r["input_kind"]))
    say("  MO8a centre jitter   %.4f px   limit %.2f   %s" % (r["mo8a_d4_px"], r["mo8a_limit"], "PASS" if r["mo8a_pass"] else "FAIL"))
    say("  MO8b edge jitter     %.4f px   limit %.2f   %s" % (r["mo8b_d4_px"], r["mo8b_limit"], "PASS" if r["mo8b_pass"] else "FAIL"))
    inf = r["informational"]
    say("  roughness (MO8c) %s, ease class %s, total zoom %s%%   [information only, W-41]" % (inf["mo8c_rough"], inf["ease_class"], inf["zoom_total_pct"]))
    say("  NOTE %s" % r["note"])
    say("  RESULT: %s" % r["verdict"])


def build_parser():
    p = argparse.ArgumentParser(prog="mo8_gate.py", description="MO8 motion gate (W-41). See the header of this file.")
    p.add_argument("inputs", nargs="+", help="a folder of numbered PNG frames, or a clip of at most 96 frames")
    p.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"))
    p.add_argument("--max-frames", type=int, default=DEFAULT_MAX, help="frames allowed (default 96; never more than 120)")
    p.add_argument("--a-limit", type=float, default=A_LIMIT, help="MO8a gate in px (0.05)")
    p.add_argument("--b-limit", type=float, default=B_LIMIT, help="MO8b gate in px (0.04)")
    p.add_argument("--audit", default=None, help="path of mo8_audit.py (default: research/cinematic-quality-fixtures/mo8_audit.py)")
    p.add_argument("--json", default=None, help="write the results here")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.max_frames > HARD_MAX:
            raise Usage("--max-frames %d is over the hard ceiling of %d frames (RAM)" % (args.max_frames, HARD_MAX))
        if args.max_frames < MIN_FRAMES:
            raise Usage("--max-frames must be at least %d" % MIN_FRAMES)
        args.audit = args.audit or default_audit()
        if not os.path.isfile(args.audit):
            raise EnvError("the audit script was not found (research/cinematic-quality-fixtures/mo8_audit.py)")
        ffmpeg = resolve_exe(args.ffmpeg)
        if not ffmpeg:
            raise EnvError("ffmpeg not found (%s)" % os.path.basename(args.ffmpeg))
        say("mo8_gate: the gate applies to the MASTER before the delivery encode (W-41). Limits: MO8a %.2f px, MO8b %.2f px; at most %d frames." %
            (args.a_limit, args.b_limit, args.max_frames))
        results = []
        for path in args.inputs:                       # refuse before any heavy work: check every input first
            describe_input(ffmpeg, path, args.max_frames)
        for path in args.inputs:
            r = gate_one(args, ffmpeg, path)
            print_one(r)
            results.append(r)
        out = {"schema": SCHEMA, "tool_version": TOOL_VERSION, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
               "limits": {"mo8a_d4_px": args.a_limit, "mo8b_d4_px": args.b_limit, "max_frames": args.max_frames},
               "applies_to": "the master before the delivery encode (W-41)", "results": results,
               "verdict": "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"}
        if args.json:
            write_json(args.json, out)
        return 0 if out["verdict"] == "PASS" else 1
    except Usage as e:
        print("mo8_gate: REFUSED: %s" % e, file=sys.stderr)
        return 2
    except EnvError as e:
        print("mo8_gate: environment problem: %s" % e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
