#!/usr/bin/env python3
"""make_master.py: the synthetic phone-test master and its caption files (WP-08). Standard library plus node and ffmpeg.

  python3 -I tests/phone/make_master.py --out renders/wp08/master10s.mov --srt renders/wp08/caps.srt [--seconds 10] [--report renders/wp08/scene_report.json] [--work DIR]

What it makes, all synthetic and style-neutral (no family media exists here, none is created or simulated):
  1. the picture: tests/phone/scene/phone_scene.html rendered by the WP-04 harness (pipeline/bin/render.mjs) at 1920x1080, 24 fps, through the prores422hq_master chain of
     pipeline/lib/chains.json (ProRes 422 HQ, BT.709 tags). The scene is a title (Latin), a headline (the first script with strings and headline:true), a moving bar, a stroke ladder
     (1, 2, 3, 4, 6 px lines), three colour patches and percentage rulers; the lower 40% of the picture is empty and static, so the burned captions can be found by differencing;
  2. the sound: a tone ladder (100, 200, 400, 800, 1600, 3200 Hz at -23 dBFS, then pink noise), 48 kHz, PCM 24-bit, stereo (the master's sound, before the phone encode normalises it);
  3. the caption file: SRT cues made ONLY from the strings of pipeline/phone/test_strings.json (a line is those strings joined by spaces, each line at most 32 characters, two lines
     a cue), so no other test text is ever written. Latin cues and one cue for every script that has strings.
It writes the scene's own report (the scene layout, copied into the encode's sidecar by encode_phone.py --layout) next to the master.
Exit 0 done; 2 bad usage; 3 a tool is missing or a stage failed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
STRINGS = os.path.join(ROOT, "pipeline", "phone", "test_strings.json")


def say(m=""):
    sys.stdout.write(m + "\n")
    sys.stdout.flush()


def count_chars(line):
    import unicodedata
    return len([c for c in line if not unicodedata.category(c).startswith("M")])


def fill_line(words, start, max_chars):
    """Words (allowlisted strings) cycled from `start`, joined by spaces, as many as fit in max_chars characters. Returns (line, next index)."""
    cur, k = [], start
    while True:
        w = words[k % len(words)]
        cand = " ".join(cur + [w])
        if cur and count_chars(cand) > max_chars:
            break
        cur.append(w)
        k += 1
        if len(cur) >= 8 or count_chars(cand) > max_chars:
            break
    return " ".join(cur), k


def srt_time(ms):
    h, rem = divmod(int(ms), 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def make_srt(strings, seconds, max_chars=32):
    """Cues from the allowlist only: Latin first, then each script that has strings, then Latin again, spread over the clip with a caption-free stretch at the start and the end."""
    blocks = [(n, [s for s in b.get("strings") or []]) for n, b in strings["scripts"].items()]
    blocks = [(n, s) for n, s in blocks if s]
    order = [blocks[0]] + blocks[1:] + [blocks[0]] + (blocks[1:2] if len(blocks) > 1 else [])
    slots = len(order)
    t0, t1 = 0.5, seconds - 0.7
    span = (t1 - t0) / slots
    cues = []
    for i, (name, strs) in enumerate(order):
        words = [s["text"] for s in strs if s.get("kind", "word") == "word"] or [s["text"] for s in strs]
        a, k = 0, (i * 2) % max(1, len(words))
        l1, k = fill_line(words, k, max_chars)
        l2, k = fill_line(words, k, max_chars - 8)
        start = t0 + i * span
        cues.append((int(start * 1000), int((start + span * 0.8) * 1000), [l1, l2]))
    out = []
    for n, (a, b, lines) in enumerate(cues, 1):
        out.append("%d\n%s --> %s\n%s\n" % (n, srt_time(a), srt_time(b), "\n".join(lines)))
    return "\n".join(out), cues


def run(cmd, cwd=None, env=None, timeout=1800):
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except FileNotFoundError:
        raise SystemExit(3)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--report", default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if a.seconds < 4:
        say("USAGE: --seconds must be at least 4")
        return 2
    for t in ("node", "ffmpeg"):
        if not shutil.which(t):
            say("ENVIRONMENT PROBLEM: %s not found" % t)
            return 3
    with open(STRINGS, encoding="utf-8") as f:
        strings = json.load(f)
    out, srt = os.path.abspath(a.out), os.path.abspath(a.srt)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    os.makedirs(os.path.dirname(srt), exist_ok=True)
    report = os.path.abspath(a.report) if a.report else os.path.splitext(out)[0] + ".scene.json"
    work = tempfile.mkdtemp(prefix="ljphonemaster_", dir=a.work) if a.work else tempfile.mkdtemp(prefix="ljphonemaster_")
    try:
        say("[1/3] Rendering the scene with the harness (%g s, ProRes 422 HQ chain) ..." % a.seconds)
        env = dict(os.environ)
        env.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
        vid = os.path.join(work, "video.mov")
        cmd = ["node", os.path.join("pipeline", "bin", "render.mjs"), "--dir", os.path.join("tests", "phone", "scene"), "--page", "phone_scene.html", "--mount", "/vendor=vendor",
               "--mount", "/lib=pipeline/lib", "--mount", "/phone=pipeline/phone", "--mount", "/scenes=pipeline/scenes", "--seconds", "%g" % a.seconds, "--chain", "prores422hq_master",
               "--ffmpeg", vid, "--json", report, "--quiet", "--overwrite"]
        rc, so, se = run(cmd, cwd=ROOT, env=env)
        if rc != 0 or not os.path.isfile(vid):
            say("ENVIRONMENT PROBLEM: the render failed (exit %d): %s" % (rc, (se or so).strip().splitlines()[-1][:200] if (se or so).strip() else ""))
            return 3
        say("      scene rendered; report written (%s)" % os.path.basename(report))
        say("[2/3] Adding the tone ladder (100 to 3200 Hz at -23 dBFS, then pink noise) ...")
        tones = [100, 200, 400, 800, 1600, 3200]
        step = min(1.2, (a.seconds - 1.0) / (len(tones) + 1.5))
        inputs, labels = [], []
        for i, f in enumerate(tones):
            inputs += ["-f", "lavfi", "-t", "%.3f" % step, "-i", "sine=f=%d:r=48000" % f]
            labels.append("[%d:a]" % (i + 1))
        rest = a.seconds - step * len(tones)
        inputs += ["-f", "lavfi", "-t", "%.3f" % rest, "-i", "anoisesrc=c=pink:r=48000:a=0.3"]
        labels.append("[%d:a]" % (len(tones) + 1))
        fc = "%sconcat=n=%d:v=0:a=1,volume=-23dB,pan=stereo|c0=c0|c1=c0,atrim=0:%.3f[a]" % ("".join(labels), len(labels), a.seconds)
        tmp_out = os.path.join(work, "master.mov")
        cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", vid] + inputs + ["-filter_complex", fc, "-map", "0:v:0", "-map", "[a]", "-c:v", "copy", "-c:a", "pcm_s24le", "-ar", "48000",
               "-map_metadata", "-1", tmp_out]
        rc, so, se = run(cmd, cwd=work)
        if rc != 0:
            say("ENVIRONMENT PROBLEM: the sound could not be added: %s" % se.strip().splitlines()[-1][:200])
            return 3
        shutil.move(tmp_out, out)
        say("[3/3] Writing the caption file from test_strings.json only ...")
        text, cues = make_srt(strings, a.seconds)
        with open(srt, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        say("      %d cues (each line at most 32 characters, two lines)" % len(cues))
        say("files written: %s, %s, %s" % (os.path.basename(out), os.path.basename(srt), os.path.basename(report)))
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
