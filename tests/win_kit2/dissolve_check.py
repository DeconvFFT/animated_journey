#!/usr/bin/env python3
"""dissolve_check.py: prove that the two joins of the --selftest film are one-second dissolves at the right frames.

  python3 -I -B tests/win_kit2/dissolve_check.py renders/wp09/ex02.mp4

The self-test film is three 144-frame moves (push, pan, pull) of the three synthetic stills, dissolved over 24 frames each, so the
dissolves are output frames 120 to 143 and 240 to 263. This script re-renders the outgoing and incoming move frames with the tool's
own geometry and Pillow, decodes the film frames with the BT.709 read-back, and fits the dissolve weight p of each decoded frame:
    decoded = (1 - p) * outgoing + p * incoming          (least squares over the whole picture)
A dissolve must show p rising 0 to 1 in steps of 1/24, outside it p must be 0 (before) or 1 (after). Prints one line per probe and
DISSOLVES OK or DISSOLVES BAD. Needs ffmpeg, numpy and Pillow. Synthetic pictures only.
"""
import importlib.util
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "win", "kit2")
sys.path.insert(0, KIT)
spec = importlib.util.spec_from_file_location("kb_dissolve", os.path.join(KIT, "kenburns_24.py"))
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


def move_frame(img, name, i, n=144):
    m = dict(kb.MOVES[name])
    m["name"] = name
    base = kb.base_window(*img.size)
    box = kb.clamp_box(kb.move_box(m, base, i, n), img.size)
    lan = getattr(Image, "Resampling", Image).LANCZOS
    return np.asarray(img.resize((kb.W, kb.H), lan, box=box)).astype(np.float32)


def main():
    path = sys.argv[1]
    ffmpeg = shutil.which("ffmpeg")
    stills = [kb.synthetic_still(k)[0] for k in range(3)]
    names = ["push", "pan", "pull"]
    bad = []
    lines = []
    for d in (1, 2):
        start = 120 * d
        for j, want in ((-1, 0.0), (0, 0.0), (6, 6 / 24.0), (12, 0.5), (18, 18 / 24.0), (23, 23 / 24.0), (24, 1.0)):
            f = start + j
            a = move_frame(stills[d - 1], names[d - 1], min(143, f - 120 * (d - 1)))     # outgoing move: it began at output frame 120 * (d - 1)
            b = move_frame(stills[d], names[d], max(0, f - 120 * d))                     # incoming move: it begins at output frame 120 * d
            v = kb.decode_frame_rgb(ffmpeg, path, f).astype(np.float32)
            diff = b - a
            p = float(((v - a) * diff).sum() / (diff * diff).sum())
            err = float(np.abs(v - ((1 - p) * a + p * b)).mean())
            ok = abs(p - want) <= 0.06 and err < 4.0
            lines.append("dissolve %d frame %3d (j=%2d): fitted weight %.3f, expected %.3f, residual %.2f grey levels %s" % (d, f, j, p, want, err, "ok" if ok else "BAD"))
            if not ok:
                bad.append(f)
    for ln in lines:
        print(ln)
    print("DISSOLVES " + ("OK" if not bad else "BAD at frames %s" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
