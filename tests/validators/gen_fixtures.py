#!/usr/bin/env python3
"""gen_fixtures.py: the good fixtures and the planted-defect generator for pipeline/validators (WP-05, SP5 media half).

Everything is generated at test time, from synthetic content only (three flat colour patches and a sine tone), into a git-ignored
folder (renders/wp05/). Nothing here is a photo, a person or a place; no family media is used or simulated.

  python3 -I tests/validators/gen_fixtures.py OUTDIR --set good|defects|mo8|all [--ffmpeg ffmpeg] [--only NAME ...]

It writes the media files and OUTDIR/manifest_<set>.json: for every file, which profile it belongs to and what spec_check.py must
say (pass, or fail naming these check ids). run_checks.py reads the manifest and holds spec_check to it.

The good files are encoded with the project's OWN chains (pipeline/lib/chains.json), so this also exercises the chains end to end.
A planted defect changes exactly one thing in a good recipe (the frame rate, the pixel format, the tone, a tag ...).

Sizes stay small: 2 s of H.264 is a few hundred KB; ProRes is cut to 1 s (about 3 to 5 MB each); the MO8 clips are the only large
files (about 10 MB each) and the runner deletes them straight after use.
"""
import argparse
import importlib.util
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import zlib

sys.dont_write_bytecode = True      # importing the reused ab_push_card.py must not leave .pyc files in research/
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
W, H = 1920, 1080
PATCHES = [(255, 0, 0, 255), (128, 128, 128, 200), (224, 172, 140, 128)]      # the W-16 patches (+ alpha for the overlay)


# ----------------------------------------------------------------------------------------------- tiny helpers
def run(cmd, timeout=600):
    p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def write_png(path, rgba):
    """Three flat vertical patches as a PNG (stdlib only). rgba=True writes the alpha too."""
    ch = 4 if rgba else 3
    row = b"".join(bytes(p[:ch]) * (W // 3) for p in PATCHES)
    row = row + bytes(PATCHES[-1][:ch]) * (W - len(row) // ch)
    raw = (b"\x00" + row) * H

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6 if rgba else 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def tone(level_lufs, seconds, burst=None, rate=48000):
    """Identical stereo 1 kHz sine whose integrated loudness is about level_lufs (for identical channels I = peak level, measured).
    burst: amplitude of a 2 ms click added at t=1 s (a high peak with almost no loudness)."""
    amp = 10 ** (level_lufs / 20.0)
    if burst:
        ex = "%.5f*sin(2*PI*1000*t)+if(between(t,1,1.002),%.3f*sin(2*PI*500*t),0)" % (amp, burst)
        return "aevalsrc=exprs='%s|%s':s=%d:d=%s" % (ex, ex, rate, seconds)
    ex = "%.5f*sin(2*PI*1000*t)" % amp
    return "aevalsrc=exprs=%s|%s:s=%d:d=%s" % (ex, ex, rate, seconds)


def load_chains():
    with open(os.path.join(ROOT, "pipeline", "lib", "chains.json"), encoding="utf-8") as f:
        return json.load(f)["chains"]


EXT = {"mp4": ".mp4", "mov": ".mov", "mkv": ".mkv"}


def encode(ffmpeg, out, still, chain, *, seconds=2, fps=24, lufs=-18.0, burst=None, rate=48000, vf=None, video_args=None, audio_args=None,
           audio=True, meta=None, extra_out=None, drop_args=()):
    """One clip: the still looped at fps for `seconds`, the tone, through `chain` with optional replacements."""
    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", str(fps), "-i", still]
    if audio:
        cmd += ["-f", "lavfi", "-i", tone(lufs, seconds, burst, rate)]
    cmd += ["-frames:v", str(int(fps * seconds))]
    vfx = chain["vf"] if vf is None else vf
    if vfx:
        cmd += ["-vf", vfx]
    vargs = list(chain["video_args"] if video_args is None else video_args)
    for d in drop_args:                                  # remove "-flag value" pairs
        while d in vargs:
            i = vargs.index(d)
            del vargs[i:i + 2]
    cmd += vargs
    if audio:
        cmd += ["-map", "0:v:0", "-map", "1:a:0"] + list(chain["audio_args"] if audio_args is None else audio_args)
    for k, v in (meta or {}).items():
        cmd += ["-metadata", "%s=%s" % (k, v)]
    cmd += list(extra_out or []) + [out]
    rc, so, se = run(cmd)
    if rc != 0:
        raise RuntimeError("ffmpeg failed for %s: %s" % (os.path.basename(out), (se.strip().splitlines() or ["?"])[-1][:200]))


def faststart_off(chain):
    return [a for a in chain["video_args"] if a not in ("-movflags", "+faststart")]


def entry(f, profile, expect, **kw):
    e = {"file": f, "profile": profile, "expect": expect}
    e.update(kw)
    return e


# defects that change one thing and so must trip exactly the check(s) named; the others trip one named check plus an unavoidable second one
ISOLATED = {"d_720p.mp4", "d_true_peak.mp4", "d_44k1_audio.mp4", "d_title_tag.mp4", "d_not_faststart.mp4", "d_online_too_loud.mp4",
            "d_level40.mp4", "d_no_audio.mp4", "d_mono.mp4", "d_frame_count.mp4", "d_bt601_under_709_tags.mp4"}


# ----------------------------------------------------------------------------------------------- the sets
def phone_profile_file(path):
    """A stand-in for WP-08's pipeline/phone/profile.json (same shape: chains + profiles). WP-08 supplies the real one."""
    vf = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
    doc = {
        "schema": "lj-chains/1", "note": "synthetic stand-in for the phone profile, generated by tests/validators/gen_fixtures.py",
        "chains": {"phone_1080": {
            "container": "mp4", "alpha": False, "vf": vf,
            "video_args": ["-c:v", "libx264", "-profile:v", "high", "-level", "4.0", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M",
                           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                           "-movflags", "+faststart", "-map_metadata", "-1"],
            "audio_args": ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"],
            "expect": {"codec": "h264", "profile": "High", "pix_fmt": "yuv420p", "color_range": "tv", "color_space": "bt709",
                       "color_primaries": "bt709", "color_transfer": "bt709"},
            "approved": False, "notes": "test stand-in"}},
        "profiles": {"phone_1080": {
            "description": "phone file (synthetic stand-in): 1080p24 H.264 High 4.0, AAC-LC, -16 LUFS", "chain": "phone_1080",
            "container": "mp4", "faststart": True,
            "video": {"codec": "h264", "profile": ["High"], "level": [40], "pix_fmt": ["yuv420p"], "width": 1920, "height": 1080, "fps": "24/1",
                      "color_range": ["tv"], "color_space": ["bt709"], "color_primaries": ["bt709"], "color_transfer": ["bt709"], "alpha": False, "max_mbps": 8},
            "audio": {"required": True, "codec": ["aac"], "profile": ["LC"], "sample_rate": 48000, "channels": [2]},
            "loudness": {"true_peak_max_dbtp": -1.0, "integrated_lufs": [-16], "tolerance_lu": 1.0}, "metadata": "neutral"}}}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2)
    return path


def build_good(ffmpeg, out_dir, only=None):
    ch = load_chains()
    still = os.path.join(out_dir, "patches.png")
    still4 = os.path.join(out_dir, "patches_rgba.png")
    write_png(still, False)
    write_png(still4, True)
    phone = phone_profile_file(os.path.join(out_dir, "phone_profile.json"))
    phone_chain = json.load(open(phone, encoding="utf-8"))["chains"]["phone_1080"]
    man = []

    def want(name):
        return only is None or name in only
    recipes = [
        ("g_master_hq.mov", "master_prores422hq", dict(chain=ch["prores422hq_master"], seconds=1, lufs=-20)),
        ("g_venue_m18.mp4", "venue_h264", dict(chain=ch["h264_venue"], lufs=-18)),
        ("g_venue_m23.mp4", "venue_h264", dict(chain=ch["h264_venue"], lufs=-23)),
        ("g_venue_m16.mp4", "venue_h264", dict(chain=ch["h264_venue"], lufs=-16)),
        ("g_backup_main40.mp4", "venue_h264_backup_main40", dict(chain=ch["h264_backup_main40"], lufs=-18)),
        ("g_online_m16.mp4", "online_h264", dict(chain=ch["h264_online"], lufs=-16)),
        ("g_online_m16_edge.mp4", "online_h264", dict(chain=ch["h264_online"], lufs=-16.8)),
        ("g_overlay_4444.mov", "overlay_prores4444_alpha", dict(chain=ch["prores4444_alpha"], seconds=1, audio=False, still=still4)),
        ("g_phone_1080.mp4", "phone_1080", dict(chain=phone_chain, lufs=-16, profiles_file="phone_profile.json")),
    ]
    for name, profile, kw in recipes:
        if not want(name):
            continue
        kw = dict(kw)
        chain = kw.pop("chain")
        st = kw.pop("still", still)
        pf = kw.pop("profiles_file", None)
        encode(ffmpeg, os.path.join(out_dir, name), st, chain, **kw)
        man.append(entry(name, profile, "pass", profiles_file=pf, why="good file for the %s profile" % profile))
    return man


def build_defects(ffmpeg, out_dir, only=None):
    ch = load_chains()
    venue = ch["h264_venue"]
    still = os.path.join(out_dir, "patches.png")
    still4 = os.path.join(out_dir, "patches_rgba.png")
    if not os.path.isfile(still):
        write_png(still, False)
    if not os.path.isfile(still4):
        write_png(still4, True)
    man = []

    def want(name):
        return only is None or name in only

    def mk(name, profile, must_fail, why, *, chain=None, still_=None, **kw):
        if not want(name):
            return
        encode(ffmpeg, os.path.join(out_dir, name), still_ or still, chain or venue, **kw)
        man.append(entry(name, profile, "fail" if must_fail else "pass", must_fail=must_fail, why=why, isolated=name in ISOLATED))

    vf709 = venue["vf"]
    # --- the ten defects the plan names
    pc = vf709.replace("format=yuv420p", "format=yuvj420p").replace("out_range=tv", "out_range=pc").replace("range=tv", "range=pc")
    pc_args = [("pc" if a == "tv" else a) for a in venue["video_args"]]
    mk("d_yuvj420p.mp4", "venue_h264", ["video.pix_fmt"], "full-range yuvj420p instead of yuv420p", vf=pc, video_args=pc_args)
    mk("d_25fps.mp4", "venue_h264", ["video.fps"], "25 fps instead of 24", fps=25)
    mk("d_720p.mp4", "venue_h264", ["video.size"], "1280x720 instead of 1920x1080", vf="scale=1280:720," + vf709)
    # BT.601 matrix under BT.709 tags: a bare -pix_fmt encode with the four tags. spec_check must PASS it (tags are fine); colour_patch fails it.
    bare = [a for a in venue["video_args"]] + ["-pix_fmt", "yuv420p"]
    mk("d_bt601_under_709_tags.mp4", "venue_h264", [], "bare -pix_fmt yuv420p from RGB with BT.709 tags: BT.601 pixels on ffmpeg 6.1.1; the tags pass", vf="", video_args=bare)
    mk("d_prores4444_no_alpha.mov", "overlay_prores4444_alpha", ["video.alpha"], "ProRes 4444 without an alpha plane", chain=ch["prores4444_alpha"],
       still_=still4, seconds=1, audio=False,
       vf="scale=out_color_matrix=bt709:out_range=tv,format=yuv444p10le,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv")
    mk("d_true_peak.mp4", "venue_h264", ["audio.true_peak"], "a 2 ms click near full scale: true peak above -1 dBTP, loudness still about -18", burst=0.98)
    mk("d_44k1_audio.mp4", "venue_h264", ["audio.sample_rate"], "44.1 kHz audio", rate=44100,
       audio_args=["-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-ac", "2"])
    mk("d_16bit_master.mov", "master_prores422hq", ["audio.bits"], "16-bit PCM under the master profile", chain=ch["prores422hq_master"], seconds=1, lufs=-20,
       audio_args=["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"])
    mk("d_title_tag.mp4", "venue_h264", ["metadata.neutral"], "a title metadata tag", meta={"title": "Selftest Title"},
       video_args=[a for a in venue["video_args"] if a not in ("-map_metadata", "-1")])
    # truncated MP4: encoded without faststart (moov at the end), then cut to 60 percent of its bytes -> no moov
    if want("d_truncated.mp4"):
        full = os.path.join(out_dir, "_full_nofast.mp4")
        encode(ffmpeg, full, still, venue, video_args=faststart_off(venue))
        data = open(full, "rb").read()
        with open(os.path.join(out_dir, "d_truncated.mp4"), "wb") as f:
            f.write(data[: int(len(data) * 0.6)])
        os.remove(full)
        man.append(entry("d_truncated.mp4", "venue_h264", "fail", must_fail=["container.readable", "container.moov"], why="MP4 cut to 60 percent: the moov atom is gone"))
    # frame count disagrees with duration x 24: stream-copy trim keeps all frames but an edit list shortens the duration
    if want("d_frame_count.mp4"):
        src = os.path.join(out_dir, "_gop.mp4")
        encode(ffmpeg, src, still, venue)
        rc, so, se = run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-ss", "0.5", "-i", src, "-c", "copy", "-movflags", "+faststart", os.path.join(out_dir, "d_frame_count.mp4")])
        os.remove(src)
        if rc != 0:
            raise RuntimeError("trim failed: " + se.strip()[-200:])
        man.append(entry("d_frame_count.mp4", "venue_h264", "fail", must_fail=["video.frame_count"], isolated=True, why="48 frames but duration 1.5 s (edit list): 48 != round(1.5 x 24)"))
    # --- extras
    mk("d_not_faststart.mp4", "venue_h264", ["container.faststart"], "moov after mdat", video_args=faststart_off(venue))
    mk("d_untagged.mp4", "venue_h264", ["video.color_space"], "no colour tags at all (no setparams, no tag flags)", vf="scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
       video_args=["-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-movflags", "+faststart", "-map_metadata", "-1"])
    mk("d_online_too_loud.mp4", "online_h264", ["audio.integrated"], "integrated loudness -13 LUFS under the -16 profile", chain=ch["h264_online"], lufs=-13)
    mk("d_level40.mp4", "venue_h264", ["video.level"], "H.264 level 4.0 under the High 4.1 venue profile",
       video_args=[("4.0" if a == "4.1" else a) for a in venue["video_args"]])
    mk("d_no_audio.mp4", "venue_h264", ["audio.present"], "no audio stream", audio=False)
    mk("d_mono.mp4", "venue_h264", ["audio.channels"], "mono audio", audio_args=["-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "1"])
    return man


def build_mo8(ffmpeg, out_dir, only=None):
    """MO8 clips. Needs numpy and Pillow, and reuses research/cinematic-quality-fixtures/ab_push_card.py in place."""
    here = os.path.join(ROOT, "research", "cinematic-quality-fixtures")
    sys.path.insert(0, here)
    spec = importlib.util.spec_from_file_location("ab_push_card", os.path.join(here, "ab_push_card.py"))
    ab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ab)
    from PIL import Image
    man = []
    ab.Z0 = 1.0
    still = None

    def want(name):
        return only is None or name in only

    def pipe(name, frames):
        p = subprocess.Popen([ffmpeg, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "24", "-i", "-",
                              "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", os.path.join(out_dir, name)], stdin=subprocess.PIPE)
        for fr in frames:
            p.stdin.write(fr.tobytes())
        p.stdin.close()
        if p.wait() != 0:
            raise RuntimeError("ffmpeg failed for " + name)
    if want("mo8_pillow96.mp4") or want("mo8_zoompan96.mp4") or want("mo8_pillow_frames"):
        still = ab.synthetic_still()
    if want("mo8_pillow96.mp4"):
        pipe("mo8_pillow96.mp4", ab.pillow_push(still))
        man.append(entry("mo8_pillow96.mp4", None, "pass", kind="mo8", why="Pillow resize(box) sub-pixel push, 96 frames, H.264 CRF 14 (disk-friendly stand-in for a master)"))
    if want("mo8_zoompan96.mp4"):
        png = os.path.join(out_dir, "_still1080.png")
        still.resize((1920, 1080), Image.LANCZOS).save(png)
        pipe("mo8_zoompan96.mp4", ab.zoompan_push(png))
        os.remove(png)
        man.append(entry("mo8_zoompan96.mp4", None, "fail", kind="mo8", must_fail=["mo8a", "mo8b"], why="ffmpeg zoompan push from a 1080p picture, 96 frames, H.264 CRF 14"))
    if want("mo8_pillow_frames"):
        d = os.path.join(out_dir, "mo8_pillow_frames")
        os.makedirs(d, exist_ok=True)
        # 12 frames from the middle of the 96-frame push (frames 40 to 51): the minimum the gate accepts. A PNG folder is the best master
        # input. Grey PNGs (mode L, the chart is grey) are a third of the size and give the same luma, which is all the audit reads.
        gray = still.convert("L")
        for i, fr in enumerate(ab.pillow_push(gray)):
            if 40 <= i < 52:
                Image.fromarray(fr).save(os.path.join(d, "f_%06d.png" % (i - 40)), compress_level=1)
            elif i >= 52:
                break
        man.append(entry("mo8_pillow_frames", None, "pass", kind="mo8", why="12 PNG frames of a Pillow push: the gate's best input"))
    # refusals: cheap clips, counted before any frame is loaded
    for n in (97, 121, 130):
        name = "mo8_long%d.mp4" % n
        if want(name):
            rc, so, se = run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24",
                              "-frames:v", str(n), "-c:v", "libx264", "-crf", "30", os.path.join(out_dir, name)])
            if rc != 0:
                raise RuntimeError("ffmpeg failed for " + name)
            man.append(entry(name, None, "refuse", kind="mo8", frames=n, why="%d frames: over the limit" % n))
    if want("mo8_short6.mp4"):
        run([ffmpeg, "-hide_banner", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24", "-frames:v", "6",
             "-c:v", "libx264", "-crf", "30", os.path.join(out_dir, "mo8_short6.mp4")])
        man.append(entry("mo8_short6.mp4", None, "refuse", kind="mo8", frames=6, why="6 frames: too few for the fourth difference"))
    return man


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("outdir")
    ap.add_argument("--set", default="all", choices=["good", "defects", "mo8", "all"])
    ap.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"))
    ap.add_argument("--only", nargs="*", default=None, help="only these file names")
    a = ap.parse_args(argv)
    os.makedirs(a.outdir, exist_ok=True)
    ffmpeg = shutil.which(a.ffmpeg) or a.ffmpeg
    sets = ["good", "defects", "mo8"] if a.set == "all" else [a.set]
    for s in sets:
        fn = {"good": build_good, "defects": build_defects, "mo8": build_mo8}[s]
        man = fn(ffmpeg, a.outdir, set(a.only) if a.only else None)
        with open(os.path.join(a.outdir, "manifest_%s.json" % s), "w", encoding="utf-8", newline="\n") as f:
            json.dump(man, f, indent=2)
        print("gen_fixtures: %s: %d file(s)" % (s, len(man)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
