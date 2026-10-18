#!/usr/bin/env python3
"""Ken Burns push-in on each still, then a crossfade between stills (ffmpeg zoompan + xfade).

Python port of the bash in research note T3 (tested 2026-10-18 on ffmpeg 6.1.1, [65]).
ffmpeg runs through subprocess with an argument list, so it works in PowerShell.
Inputs are scaled to a square, as in the tested run: crop non-square stills first.

Usage:
  python kenburns_xfade.py still1.png still2.png still3.png --out move.mp4
  python kenburns_xfade.py --selftest
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw


def build_command(images, out, fps=24, dur=4, fade=1, size=1080, upscale=3840, zoom_gain=0.08):
    """Return the ffmpeg argument list. dur and fade are seconds per still and per crossfade."""
    n = len(images)
    if n < 2:
        raise ValueError("need at least two stills for a crossfade")
    frames_per_clip = fps * (dur + fade)
    cmd = ["ffmpeg", "-y"]
    # One image = one frame. Do NOT add "-loop 1": zoompan then emits d frames per input frame,
    # so a looped still turns a 5-second clip into 633 seconds (research note T3, trap found [L]).
    for img in images:
        cmd += ["-i", str(img)]
    parts = []
    for i in range(n):
        parts.append(
            f"[{i}:v]scale={upscale}:{upscale},"
            f"zoompan=z='1+{zoom_gain}*on/({fps}*({dur}+{fade}))':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames_per_clip}:s={size}x{size}:fps={fps},format=yuv420p[v{i}]"
        )
    prev = "v0"
    for k in range(1, n):
        label = "out" if k == n - 1 else f"x{k}"
        parts.append(f"[{prev}][v{k}]xfade=transition=fade:duration={fade}:offset={k * dur}[{label}]")
        prev = label
    cmd += ["-filter_complex", ";".join(parts), "-map", "[out]",
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)]
    return cmd


def render(images, out, **kw):
    cmd = build_command(images, out, **kw)
    t0 = time.perf_counter()
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return time.perf_counter() - t0


def probe(path):
    """Return (frame count, duration in seconds) using ffprobe, read by field name."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames,duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    stream = json.loads(r.stdout)["streams"][0]
    return int(stream["nb_read_frames"]), float(stream["duration"])


def selftest():
    """Three synthetic 1080x1080 stills, default settings: expect 13.0 s and 312 frames."""
    with tempfile.TemporaryDirectory() as tmp:
        stills = []
        for i, colour in enumerate([(120, 150, 180), (190, 150, 110), (110, 170, 120)]):
            img = Image.new("RGB", (1080, 1080), colour)
            ImageDraw.Draw(img).ellipse((340 + 40 * i, 340, 740 + 40 * i, 740), fill=(240, 225, 205))
            p = Path(tmp) / f"still{i}.png"
            img.save(p)
            stills.append(p)
        out = Path(tmp) / "selftest.mp4"
        secs = render(stills, out)
        frames, duration = probe(out)
    ok = frames == 312 and abs(duration - 13.0) < 0.05
    print(f"frames={frames} duration={duration:.3f} s render={secs:.1f} s "
          f"(expected 312 frames, 13.0 s) -> {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ken Burns push-in and crossfade through ffmpeg.")
    ap.add_argument("stills", nargs="*", help="two or more square stills, in order")
    ap.add_argument("--out", default="move.mp4", help="output video (default move.mp4)")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--dur", type=int, default=4, help="seconds per still, before the crossfade")
    ap.add_argument("--fade", type=int, default=1, help="crossfade seconds")
    ap.add_argument("--size", type=int, default=1080, help="output square size")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if len(a.stills) < 2:
        ap.error("give at least two stills, or --selftest")
    secs = render(a.stills, a.out, fps=a.fps, dur=a.dur, fade=a.fade, size=a.size)
    print(f"wrote {a.out} in {secs:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
