"""A/B push card for the venue test (T6 / D5), round 2: is random frame-to-frame jitter of 0.05 to 0.5 px visible on the real screen from the real seats?

  python -I ab_push_card.py OUTDIR [--still PATH.png|synthetic] [--font PATH.ttf] [--seed 5]

Writes OUTDIR/ab_push_card.mp4 (1920x1080, 24 fps, H.264 CRF 14, yuv420p, BT.709 tags, no audio, about 90 s), ab_push_key.json (the answer key: which clip is which,
with the jitter MEASURED on the decoded file by mo8_audit's estimator) and ab_push_sheet.txt (the recording sheet). Do not open the key before judging.
Contents, in random order inside each part, each clip 4 s (96 frames) after a 2 s number card that does not say what follows:
  Part 1  three A/B pairs. Each pair is the same 4% cosine push-in (from 1.03x to 1.07x, so there is margin for the jitter) rendered two ways, one after the other: Pillow resize(box) with Lanczos (sub-pixel, the finals method)
          and ffmpeg zoompan (integer-rounded crop, the proofs-only method). Which one is A or B is randomised per pair.
  Part 2  a jitter ladder: the Pillow push with random per-frame centre POSITION jitter ADDED at rms 0, 0.05, 0.10, 0.20, 0.30, 0.50 and 1.00 px (1080p pixels, x and y independent,
          Gaussian, seeded). The key also lists what MO8a measures on the decoded file, which is about 1.3 to 1.6 times larger (frame-to-frame displacement residual);
          zoompan from a 4K still measures 0.29 on that scale (position error about 0.22 px) and from a 1080p source 0.59.
Still: a 16:9 image of at least 3840x2160. 'synthetic' (default) makes a worst-case chart: 1/f noise texture, hairlines (1 px at 1080p, white on dark and black on light) and small text.
Use a real print as well if the maker wants the realistic case. Needs ffmpeg, numpy, Pillow. Judge from the FRONT row and the BACK row, with the room as it will be.
Windows: python -I ab_push_card.py C:\\LJ\\card   (ffmpeg on PATH or set FFMPEG=C:\\path\\ffmpeg.exe)."""
import os, sys, json, math, subprocess, argparse, random, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
W, H, FPS, N, AMT = 1920, 1080, 24, 96, 0.04
Z0 = 1.03          # the push runs from 1.03x to 1.07x so that the added jitter never reaches the picture edge (a 3% margin is 28 px at 1080p)
RUNGS = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 1.00]


def synthetic_still(seed=3, size=(3840, 2160)):
    """Aperiodic worst-case chart: 1/f noise texture, 300 random hairline segments (2 px at 4K = 1 px at 1080p, white and black) and 10 small text blocks at random places.
    (A regular grid of lines fooled the Lucas-Kanade estimator in the first try: periodic structure aliases the shift estimate, so none is used.)"""
    rng = np.random.default_rng(seed)
    w, h = size
    f = np.fft.fftfreq(w)[None, :] ** 2 + np.fft.fftfreq(h)[:, None] ** 2
    amp = 1.0 / np.maximum(np.sqrt(f), 1e-3) ** 1.0
    amp[0, 0] = 0
    base = np.fft.ifft2(amp * np.exp(2j * np.pi * rng.random((h, w)))).real
    base = (base - base.min()) / (base.max() - base.min())
    img = (60 + 120 * base).astype(np.float32)
    im = Image.fromarray(np.stack([img] * 3, -1).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for k in range(300):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h); L = rng.uniform(120, 700); th = rng.uniform(0, math.pi)
        dx, dy = 0.5 * L * math.cos(th), 0.5 * L * math.sin(th)
        d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(250, 250, 250) if k % 2 == 0 else (5, 5, 5), width=2)
    try:
        ft = ImageFont.truetype(find_font(None), 44)
    except Exception:
        ft = ImageFont.load_default()
    for k in range(10):
        x, y = int(rng.uniform(100, w - 500)), int(rng.uniform(100, h - 200))
        d.rectangle([x, y, x + 360, y + 110], fill=(235, 235, 235))
        d.text((x + 12, y + 30), "Aa 0123 hairline", fill=(10, 10, 10), font=ft)
    return im


def find_font(p):
    for c in ([p] if p else []) + ["C:\\Windows\\Fonts\\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        if c and os.path.exists(c): return c
    raise FileNotFoundError("pass --font PATH.ttf")


def zoom_at(i): return Z0 + AMT * (0.5 - 0.5 * math.cos(math.pi * i / (N - 1)))


def pillow_push(src, jit=None):
    """Pillow resize(box) with Lanczos; jit = (N,2) array of centre offsets in OUTPUT pixels."""
    sw, sh = src.size; k = sw / W
    for i in range(N):
        z = zoom_at(i); w, h = sw / z, sh / z; x0, y0 = (sw - w) / 2, (sh - h) / 2
        if jit is not None: x0 += jit[i, 0] * k / z; y0 += jit[i, 1] * k / z
        yield np.asarray(src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)))


def zoompan_push(png):
    z = f"{Z0}+{AMT}*(0.5-0.5*cos(PI*on/{N-1}))"
    vf = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}:d={N},format=rgb24"
    r = subprocess.run([FFMPEG, "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", png, "-vf", vf, "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    for fr in np.frombuffer(r.stdout, np.uint8).reshape(N, H, W, 3): yield fr


def card(text, sub, font):
    im = Image.new("RGB", (W, H), (16, 16, 16)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(font, 150); f2 = ImageFont.truetype(font, 48)
    tw = d.textlength(text, font=f1); d.text(((W - tw) / 2, H / 2 - 110), text, fill=(235, 235, 235), font=f1)
    tw = d.textlength(sub, font=f2); d.text(((W - tw) / 2, H / 2 + 80), sub, fill=(150, 150, 150), font=f2)
    return np.asarray(im)


def write_sheet(path):
    with open(path, "w") as f:
        f.write("A/B push card: recording sheet (fill in BEFORE opening ab_push_key.json)\nDate/time:        Venue:        Projector/display:        Lights as at the event: yes / no\n"
                "Seat (front row / middle / back row):        Distance to screen (m):        Picture height (m):        Distance in screen heights:\n\n")
        f.write("PART 1. Per pair: which of A or B looks steadier (or 'same')? Does the other one shimmer / crawl / buzz on the hairlines and text?\n")
        for p in (1, 2, 3): f.write(f"  Pair {p}: steadier = A / B / same     difference visible from this seat? yes / no     comment:\n")
        f.write("\nPART 2. Per ladder clip: is the picture visibly less steady than a perfectly smooth push would be? (no / maybe / yes)\n")
        for j in range(1, len(RUNGS) + 1): f.write(f"  Ladder {j}: no / maybe / yes     comment:\n")
        f.write("\nThen open ab_push_key.json. For each ladder clip it lists the injected position jitter (injected_rms_px) AND what mo8_audit.py measures on the decoded file (measured_centre_jit_px = MO8a).\n"
                "MO8a reads about 1.3 to 1.6 times the injected position jitter (it is the frame-to-frame displacement residual, which adds a factor of about 1.33 for white jitter, plus the codec floor).\n"
                "Take the lowest rung you marked 'yes' from the FRONT row and from the BACK row, and the lowest marked 'maybe'. Set the MO8a limit to half the measured_centre_jit_px of the lowest front-row 'yes',\n"
                "and never above the measured_centre_jit_px of the lowest 'maybe'.\n")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("outdir"); ap.add_argument("--still", default="synthetic"); ap.add_argument("--font", default=None); ap.add_argument("--seed", type=int, default=5)
    a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True); font = find_font(a.font)
    rnd = random.Random(a.seed); nprng = np.random.default_rng(a.seed)
    src = synthetic_still() if a.still == "synthetic" else Image.open(a.still).convert("RGB")
    if src.size[0] < 3840: print("warning: still is smaller than 3840 px wide; zoompan comparison will be weaker", file=sys.stderr)
    tmp = tempfile.mkdtemp(prefix="abcard_"); png = os.path.join(tmp, "still.png"); src.save(png)
    mp4 = os.path.join(a.outdir, "ab_push_card.mp4")
    enc = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    key = []; frame_no = 0
    def put(frames):
        nonlocal frame_no
        for fr in frames: enc.stdin.write(np.ascontiguousarray(fr).tobytes()); frame_no += 1
    put([card("A/B PUSH CARD", "4% push-in, 4 s clips. Judge steadiness. Part 1: pairs. Part 2: ladder.", font)] * (3 * FPS))
    # part 1
    clips = []
    for pair in range(1, 4):
        order = ["pillow", "zoompan"]; rnd.shuffle(order)
        for slot, kind in zip("AB", order): clips.append(("pair", pair, slot, kind, None))
    # part 2
    rungs = RUNGS[:]; rnd.shuffle(rungs)
    for j, r in enumerate(rungs, 1): clips.append(("ladder", j, None, "pillow_jitter", r))
    last_part = None
    for part, idx, slot, kind, rung in clips:
        label = f"PAIR {idx}  {slot}" if part == "pair" else f"LADDER {idx}"
        if part != last_part:
            put([card("PART 1  A/B PAIRS" if part == "pair" else "PART 2  LADDER", "", font)] * FPS); last_part = part
        put([card(label, "watch the whole clip", font)] * (2 * FPS))
        start = frame_no
        if kind == "pillow": put(pillow_push(src))
        elif kind == "zoompan": put(zoompan_push(png))
        else:
            jit = nprng.normal(0, rung / math.sqrt(2), (N, 2)) if rung > 0 else np.zeros((N, 2))
            put(pillow_push(src, jit))
        key.append(dict(label=label, part=part, kind=kind, injected_rms_px=rung, first_frame=start, frames=N))
    put([card("END", "", font)] * (2 * FPS))
    enc.stdin.close(); enc.wait()
    # measure the DECODED file, one clip at a time (the whole card would need 13 GB of memory)
    import mo8_audit as ma
    for k in key:
        r = subprocess.run([FFMPEG, "-v", "error", "-i", mp4, "-vf", f"trim=start_frame={k['first_frame']}:end_frame={k['first_frame'] + k['frames']},setpts=PTS-STARTPTS,format=rgb24",
                            "-f", "rawvideo", "-"], capture_output=True, check=True)
        seg = np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W, 3)
        res = ma.audit(seg)
        k["measured_centre_jit_px"] = res["mo8a_centre_jit_px"]; k["measured_edge_jit_px"] = res["mo8b_edge_jit_px"]; k["measured_rough"] = res["mo8c_rough"]
        k["measured_centre_jit_d4_px"] = res["mo8a_d4_px"]; k["measured_edge_jit_d4_px"] = res["mo8b_d4_px"]
    json.dump(dict(still=a.still, seed=a.seed, fps=FPS, frames_per_clip=N, push=AMT, clips=key), open(os.path.join(a.outdir, "ab_push_key.json"), "w"), indent=1)
    write_sheet(os.path.join(a.outdir, "ab_push_sheet.txt"))
    print("wrote", mp4)
    import shutil; shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
