"""Round 2: build and export a one-still push or pan with the FilmCraft CLI (headless), for the MO8 / pan-classifier checks.
Tested with filmcraft-cli 0.9.0, Linux x86_64 tarball (SHA-256 ea67953c...1632, matches the release's SHA256SUMS.txt), CPU export.
The Windows build of the same tag has the same engine; run this on the maker's PC with filmcraft-cli.exe to confirm (set FILMCRAFT_CLI).

  python3 -I filmcraft_push.py STILL.png OUT.mov [--kind push|pan] [--interp linear|bezier|autoBezier|continuousBezier|easeIn|easeOut|easeInOut|FIRST:LAST]
                               [--preset "Apple ProRes 422 HQ"] [--frames 96] [--fps 24] [--amount 0.04] [--pan-px 760] [--work DIR]
Push: Motion `scale` keyframes S0 -> S0*(1+amount), S0 chosen so the still fills the frame (4K still: 50.0 -> 52.0).
Pan: scale 100 (1:1 pixels on a 3840-wide still), Motion `position` x from 960 to 960 - pan_px (content moves left).
easeInOut = easeOut on the first keyframe and easeIn on the last (slow start, slow arrival); FIRST:LAST sets the two keyframes separately. Prints the export JSON. Needs a 16:9 still of at least 2x the sequence size.
The FilmCraft CLI is started with an empty environment (env -i) so it sees no credentials."""
import os, sys, json, argparse, subprocess, shutil, tempfile

TICKS = 254016000000
CLI = os.environ.get("FILMCRAFT_CLI", "filmcraft-cli")


def run(args, project=None, save=False, save_as=None, check=True):
    cmd = [CLI]
    if project: cmd += ["--project", project]
    if save: cmd += ["--save"]
    if save_as: cmd += ["--save-as", save_as]
    cmd += args
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("FC_HOME", tempfile.gettempdir())} if os.name != "nt" else None
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if check and r.returncode != 0:
        raise SystemExit(f"filmcraft-cli failed ({r.returncode}): {' '.join(args[:3])}\n{r.stderr[-800:]}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("still"); ap.add_argument("out")
    ap.add_argument("--kind", default="push"); ap.add_argument("--interp", default="linear")
    ap.add_argument("--preset", default="Apple ProRes 422 HQ"); ap.add_argument("--frames", type=int, default=96)
    ap.add_argument("--fps", type=int, default=24); ap.add_argument("--amount", type=float, default=0.04)
    ap.add_argument("--pan-px", type=float, default=760.0); ap.add_argument("--work", default=None)
    a = ap.parse_args()
    work = a.work or tempfile.mkdtemp(prefix="fcpush_")
    os.makedirs(work, exist_ok=True)
    still = os.path.join(work, "still.png"); shutil.copyfile(a.still, still)
    proj = os.path.join(work, "t.fcproj")
    run(["exec", "file.newProject", "name=t"], save_as=proj)
    run(["exec", "file.import", json.dumps({"paths": [still]})], project=proj, save=True)
    run(["exec", "file.newSequence", json.dumps({"name": "s", "width": 1920, "height": 1080, "fps": a.fps, "sampleRate": 48000})], project=proj, save=True)
    dur = a.frames * TICKS // a.fps
    run(["exec", "timeline.place", json.dumps({"item": 1, "track": "V1", "seconds": 0, "duration": dur, "audio": False})], project=proj, save=True)
    fr = TICKS // a.fps; t_last = (a.frames - 1) * fr
    if a.kind == "push":
        p, v0, v1 = "scale", 50.0, 50.0 * (1 + a.amount)
    else:
        p, v0, v1 = "position", [960.0, 540.0], [960.0 - a.pan_px, 540.0]
        run(["exec", "effects.setParam", json.dumps({"clip": 9, "effect": "motion", "param": "scale", "value": 100.0})], project=proj, save=True)
    for t, v in ((0, v0), (t_last, v1)):
        run(["exec", "effects.setParam", json.dumps({"clip": 9, "effect": "motion", "param": p, "value": v, "time": t, "keyframe": True})], project=proj, save=True)
    # --interp NAME sets both keyframes to NAME; --interp FIRST:LAST sets them separately, e.g. easeOut:easeIn.
    # Observed in 0.9.0: easeIn/easeOut act like Premiere's temporal ease. A segment K0->K1 is shaped by K0's OUTGOING ease (easeOut = leave slowly) and K1's INCOMING
    # ease (easeIn = arrive slowly); easeIn on the first and easeOut on the last keyframe do nothing (the move stays linear, byte-identical to a linear export).
    interp = tuple(a.interp.split(":")) if ":" in a.interp else {"easeInOut": ("easeOut", "easeIn")}.get(a.interp, (a.interp, a.interp))
    if a.interp != "linear":
        for t, ip in ((0, interp[0]), (t_last, interp[1])):
            run(["exec", "effects.setInterpolation", json.dumps({"clip": 9, "effect": "motion", "param": p, "mediaTime": t, "interpolation": ip})], project=proj, save=True)
    out = os.path.abspath(a.out)
    print(run(["export", out, "--preset", a.preset], project=proj))
    if a.work is None: shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
