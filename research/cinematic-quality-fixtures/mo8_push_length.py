"""Round 2: MO8 numbers for a PERFECT sub-pixel push (Pillow resize box, Lanczos) and for ffmpeg zoompan at different push lengths, to show that the 9-frame-mean
edge jitter (and roughness) of FQ2 contain the ease curve's own curvature while the fourth-difference version does not.
  python3 -I mo8_push_length.py OUT.jsonl [lengths in frames, comma list: 24,48,72,96,144]
Uses the generated worst-case chart from ab_push_card.synthetic_still() (aperiodic, 3840x2160), a 4% cosine push from 1.00x, 1080p output, raw frames (no codec)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import ab_push_card as ab, mo8_audit as ma
out = sys.argv[1]; lens = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "24,48,72,96,144").split(",")]
ab.Z0 = 1.0
still = ab.synthetic_still(); png = out + ".still.png"; still.save(png)
for N in lens:
    ab.N = N
    for name, frames in (("pillow resize box", np.stack(list(ab.pillow_push(still)))), ("zoompan from 4K", np.stack(list(ab.zoompan_push(png))))):
        r = ma.audit(frames)
        rec = dict(N=N, seconds=round(N / 24, 2), method=name, a=r["mo8a_centre_jit_px"], b_9fr=r["mo8b_edge_jit_px"], c_rough=r["mo8c_rough"], a_d4=r["mo8a_d4_px"], b_d4=r["mo8b_d4_px"])
        open(out, "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
os.remove(png)
