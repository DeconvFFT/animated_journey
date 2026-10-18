"""Round 2: zoompan on a PNG still: centre jitter with an RGB path through the filter against a yuv420p chain (what a normal command line produces).
  python3 -I zoompan_pixel_format.py   (run in an empty scratch folder; writes and deletes zpfmt.png and zpfmt_c.mp4)"""
import sys, subprocess, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ab_push_card as ab, mo8_audit as ma
ab.Z0 = 1.0
still = ab.synthetic_still(); still.save("zpfmt.png")
N = 96; z = f"1+0.04*(0.5-0.5*cos(PI*on/{N-1}))"
zp = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=24:d={N}"
def run(vf, extra):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", "zpfmt.png", "-vf", vf, "-frames:v", str(N)] + extra, capture_output=True, check=True)
    return r.stdout
def raw(vf): return np.frombuffer(run(vf, ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]), np.uint8).reshape(N, 1080, 1920, 3)
rows = {}
rows["A: ...,format=rgb24 (zoompan runs in rgb24)"] = raw(zp + ",format=rgb24")
rows["B: ...,format=yuv420p in the filter chain"] = raw(zp + ",format=yuv420p")
rows["C: no format filter; x264 -pix_fmt yuv420p as output option"] = None
run(zp, ["-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-f", "mp4", "zpfmt_c.mp4"]) if False else None
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", "zpfmt.png", "-vf", zp, "-frames:v", str(N), "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "zpfmt_c.mp4"], check=True)
rows["C: no format filter; x264 -pix_fmt yuv420p as output option"] = ma.load_video("zpfmt_c.mp4")
for k, fr in rows.items():
    r = ma.audit(fr)
    print(json.dumps(dict(case=k, a=r["mo8a_centre_jit_px"], a_d4=r["mo8a_d4_px"], b=r["mo8b_edge_jit_px"], b_d4=r["mo8b_d4_px"], c=r["mo8c_rough"])), flush=True)
os.remove("zpfmt.png"); os.remove("zpfmt_c.mp4")
