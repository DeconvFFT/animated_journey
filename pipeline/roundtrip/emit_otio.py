#!/usr/bin/env python3
"""emit_otio.py: turn the neutral timeline spec into an OpenTimelineIO (.otio) file for FilmCraft (WP-06). Standard library only; writes plain JSON.

  python3 -I pipeline/roundtrip/emit_otio.py SPEC.json OUT.otio [--timeline169 PATH]
  python3 -I pipeline/roundtrip/emit_otio.py SPEC.json --timeline169 PATH        (only the make_otio.py input; no .otio, no media)
  python3 -I pipeline/roundtrip/emit_otio.py pipeline/roundtrip/spec/neutral_timeline.example.json renders/wp06/ch.otio

Input   a spec of schema lj-neutral-timeline/1 (pipeline/roundtrip/spec/neutral_timeline.example.json): frame rate, sequence size, ordered shots
        {id, source, source_size, duration_frames, motion, transition_out, markers}, sequence markers, audio cues. See the README for every field.
Output  OUT.otio, 24 frames a second (W-14, S-01), rebased from the 25 fps E2 template of research/craft-motion.md R3: Timeline.1 / Stack.1 / Track.1
        (V1 Video, A1 Audio) / Clip.2 / Transition.1 (SMPTE_Dissolve) / Marker.2 / Gap.1, one ExternalReference per clip with a RELATIVE target_url (Kdenlive
        and FilmCraft read relative paths; absolute file:// URLs are not found, craft-motion.md F3) and an available_range, and metadata.filmcraft on each
        clip: scale_to_frame false, gain_db, source_in_ticks, duration_ticks and, when the shot has motion, a "motion" effect with scale and position
        keyframes (Float and Vec2 values; interpolation Linear then the shot's ease).
        A dissolve of N frames is written as in_offset N//2 and out_offset N-N//2 and consumes no timeline time (OTIO semantics), so the timeline is the sum
        of the clip durations.
Ken Burns scale is computed by kb_scale.py from source_size and the sequence size ("from": "cover" or "fit", "zoom": end/start ratio, "direction": in|out)
        or given as literal numbers ("scale": [66.67, 80.0]). The move is refused (exit 2) if it would show black at the frame edge.
Media  "synthetic_media": true marks a TEST spec: media files that are missing are generated (numbered test-card PNGs and a sine WAV, make_media.py) next
        to OUT.otio, resolved from each target_url. An existing file is never touched. A spec without that flag never creates media.
        --timeline169 PATH also writes the input file format of the reused research/sources/format-round1/make_otio.py (adapter_probe.sh needs it).
UNVERIFIED: that FilmCraft reads this file as intended (WP-10 T3 and the maker's Windows test); the unit of Position (sequence pixels, picture centre);
        which side of a keyframe its interp applies to; that an available_range on a still does not confuse FilmCraft (the template has null).

EXIT CODES (build plan 4.3)  0 written   2 bad usage or an invalid spec (the message says which field)   3 environment (Pillow missing for synthetic media)
It reads SPEC, may read media headers, and writes OUT.otio, the optional --timeline169 file and, for a synthetic spec only, the missing test media.
"""
import argparse
import json
import os
import re
import struct
import sys
import wave

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb_scale  # noqa: E402

FPS = 24
TICKS_PER_SECOND = 254016000000
TICKS_PER_FRAME = TICKS_PER_SECOND // FPS            # 10,584,000,000 at 24 fps (exact)
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")
COLOURS = {"PINK", "RED", "ORANGE", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "MAGENTA", "BLACK", "WHITE"}
EASES = {"Linear", "EaseOut"}      # the two interpolations that appear in the evidenced E2 template (research/craft-motion.md R3)
SCHEMA = "lj-neutral-timeline/1"


class SpecError(Exception):
    pass


# --------------------------------------------------------------------------------------------------------------- OTIO pieces
def rt(value):
    return {"OTIO_SCHEMA": "RationalTime.1", "rate": float(FPS), "value": float(value)}


def tr(start, duration):
    return {"OTIO_SCHEMA": "TimeRange.1", "start_time": rt(start), "duration": rt(duration)}


def marker(m, where):
    return {"OTIO_SCHEMA": "Marker.2", "name": m["name"], "comment": m.get("comment", ""), "color": m["color"], "metadata": {},
            "marked_range": tr(where, 0)}


def ext_ref(name, url, available_frames):
    return {"DEFAULT_MEDIA": {"OTIO_SCHEMA": "ExternalReference.1", "name": name, "target_url": url,
                              "available_range": tr(0, available_frames) if available_frames else None, "metadata": {}}}


def clip(name, url, ref_name, src_start, frames, available, markers, metadata):
    return {"OTIO_SCHEMA": "Clip.2", "name": name, "enabled": True, "markers": markers, "effects": [],
            "source_range": tr(src_start, frames), "media_references": ext_ref(ref_name, url, available),
            "active_media_reference_key": "DEFAULT_MEDIA", "metadata": metadata}


def gap(frames):
    return {"OTIO_SCHEMA": "Gap.1", "name": "", "enabled": True, "markers": [], "effects": [], "metadata": {},
            "source_range": tr(0, frames)}


def dissolve(frames):
    a = frames // 2
    return {"OTIO_SCHEMA": "Transition.1", "name": "Cross Dissolve", "transition_type": "SMPTE_Dissolve", "metadata": {},
            "in_offset": rt(a), "out_offset": rt(frames - a)}


def fvalue(v):
    return {"Float": round(float(v), 2)}


def vvalue(x, y):
    return {"Vec2": {"x": float(x), "y": float(y)}}


def motion_effect(s0, s1, p0, p1, ease, dur_ticks):
    def kf(a, b, val):
        return [{"time": 0, "value": val(a), "interp": "Linear"}, {"time": dur_ticks, "value": val(b), "interp": ease}]
    return {"effect": "motion", "enabled": True, "params": {
        "scale": {"value": fvalue(s0), "keyframes": kf(s0, s1, fvalue)},
        "position": {"value": vvalue(*p0), "keyframes": kf(p0, p1, lambda p: vvalue(*p))}}}


# --------------------------------------------------------------------------------------------------------------- spec checks
def need(cond, msg):
    if not cond:
        raise SpecError(msg)


def is_rel(p):
    return isinstance(p, str) and p and not (p.startswith("/") or "\\" in p or re.match(r"^[A-Za-z]:", p) or "://" in p or p.startswith("file:")
                                              or ".." in p.split("/"))


def png_size(path):
    """(w, h) from a PNG header, or None."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
            return struct.unpack(">II", head[16:24])
    except OSError:
        pass
    return None


def wav_frames24(path):
    try:
        with wave.open(path, "rb") as w:
            return int(round(w.getnframes() * FPS / float(w.getframerate())))
    except (OSError, wave.Error, EOFError):
        return None


def load_spec(path):
    try:
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        raise SpecError("cannot read the spec: %s" % e)
    need(isinstance(spec, dict) and spec.get("schema") == SCHEMA, "spec.schema must be %r" % SCHEMA)
    need(spec.get("fps") == FPS, "spec.fps must be %d (W-14, S-01); got %r" % (FPS, spec.get("fps")))
    seq = spec.get("sequence") or {}
    need(seq.get("width") == 1920 and seq.get("height") == 1080,
         "spec.sequence must be 1920x1080: the shape of metadata.filmcraft.settings for any other size is not known (export a template from FilmCraft once)")
    need(isinstance(spec.get("shots"), list) and spec["shots"], "spec.shots must be a non-empty list")
    ids = set()
    for i, s in enumerate(spec["shots"]):
        where = "spec.shots[%d]" % i
        need(isinstance(s, dict), where + " must be an object")
        need(ID_RE.match(str(s.get("id", ""))), where + ".id must match ^[A-Za-z][A-Za-z0-9._-]*$")
        need(s["id"] not in ids, where + ".id %r is used twice" % s["id"])
        ids.add(s["id"])
        need(is_rel(s.get("source")), where + ".source must be a relative path with forward slashes (no drive letter, scheme, backslash or '..')")
        need(isinstance(s.get("duration_frames"), int) and s["duration_frames"] > 0, where + ".duration_frames must be a positive whole number")
        mo = s.get("motion")
        if mo is not None:
            need(isinstance(mo, dict), where + ".motion must be an object")
            need(mo.get("ease", "Linear") in EASES, where + ".motion.ease must be one of %s" % sorted(EASES))
            sc = mo.get("scale")
            need(isinstance(sc, list) and len(sc) == 2 or (isinstance(sc, dict) and sc.get("from") in ("cover", "fit")),
                 where + ".motion.scale must be [start, end] or {from: cover|fit, zoom: ratio, direction: in|out}")
            if isinstance(sc, dict):
                need(isinstance(s.get("source_size"), list) and len(s["source_size"]) == 2, where + ".source_size [w, h] is needed to compute the scale")
                need(isinstance(sc.get("zoom", 1.0), (int, float)) and sc.get("zoom", 1.0) >= 1.0, where + ".motion.scale.zoom must be a number >= 1")
                need(sc.get("direction", "in") in ("in", "out"), where + ".motion.scale.direction must be in or out")
            pos = mo.get("position", [[960, 540], [960, 540]])
            need(isinstance(pos, list) and len(pos) == 2 and all(isinstance(p, list) and len(p) == 2 for p in pos), where + ".motion.position must be [[x, y], [x, y]]")
        td = s.get("transition_out")
        if td is not None:
            need(td.get("type") == "dissolve", where + ".transition_out.type must be dissolve")
            f = td.get("frames")
            need(isinstance(f, int) and f > 0, where + ".transition_out.frames must be a positive whole number")
            need(i < len(spec["shots"]) - 1, where + ": the last shot can not have transition_out")
        for j, m in enumerate(s.get("markers", [])):
            check_marker(m, where + ".markers[%d]" % j, s["duration_frames"])
    for j, m in enumerate(spec.get("markers", [])):
        check_marker(m, "spec.markers[%d]" % j, None)
    for k, a in enumerate(spec.get("audio", [])):
        where = "spec.audio[%d]" % k
        need(ID_RE.match(str(a.get("id", ""))), where + ".id must match ^[A-Za-z][A-Za-z0-9._-]*$")
        need(is_rel(a.get("source")), where + ".source must be a relative path with forward slashes")
        need(isinstance(a.get("duration_frames"), int) and a["duration_frames"] > 0, where + ".duration_frames must be a positive whole number")
        need(isinstance(a.get("start_frame", 0), int) and a.get("start_frame", 0) >= 0, where + ".start_frame must be a whole number >= 0")
        need(isinstance(a.get("gain_db", 0.0), (int, float)), where + ".gain_db must be a number")
    return spec


def check_marker(m, where, limit):
    need(isinstance(m, dict) and isinstance(m.get("name"), str) and m["name"], where + ".name must be text")
    need(m.get("color") in COLOURS, where + ".color must be one of %s" % sorted(COLOURS))
    need(isinstance(m.get("at_frame"), int) and m["at_frame"] >= 0, where + ".at_frame must be a whole number >= 0")
    if limit is not None:
        need(m["at_frame"] < limit, where + ".at_frame must fall inside the shot (0 to %d)" % (limit - 1))


# --------------------------------------------------------------------------------------------------------------- build
def build(spec, out_dir, make_media_fn=None):
    """Return (otio dict, info dict). make_media_fn(out_dir, spec) is called first for a synthetic spec."""
    created = []
    sw, sh = spec["sequence"]["width"], spec["sequence"]["height"]
    avail_still = spec.get("still_available_frames", 240)
    need(isinstance(avail_still, int) and avail_still > 0, "spec.still_available_frames must be a positive whole number")
    items, total, transitions, n_markers = [], 0, 0, len(spec.get("markers", []))
    shots = spec["shots"]
    for i, s in enumerate(shots):
        frames = s["duration_frames"]
        dur_ticks = frames * TICKS_PER_FRAME
        need(frames <= avail_still, "spec.shots[%d]: duration_frames %d is longer than still_available_frames %d" % (i, frames, avail_still))
        full = os.path.join(out_dir, *s["source"].split("/"))
        actual = png_size(full)
        if actual and s.get("source_size") and tuple(actual) != tuple(s["source_size"]):
            raise SpecError("spec.shots[%d].source_size %s does not match the PNG header %dx%d" % (i, s["source_size"], actual[0], actual[1]))
        meta = {}
        mo = s.get("motion")
        if mo:
            sc = mo["scale"]
            if isinstance(sc, dict):
                w, h = s["source_size"]
                base = kb_scale.scale_for(sc["from"], w, h, sw, sh)
                far = round(base * sc.get("zoom", 1.0), 2)
                s0, s1 = (far, base) if sc.get("direction", "in") == "out" else (base, far)
            else:
                s0, s1 = float(sc[0]), float(sc[1])
            p0, p1 = mo.get("position", [[sw // 2, sh // 2], [sw // 2, sh // 2]])
            if s.get("source_size"):
                w, h = s["source_size"]
                ok, worst = kb_scale.move_is_edge_safe(w, h, sw, sh, [(s0, p0[0], p0[1]), (s1, p1[0], p1[1])])
                need(ok, "spec.shots[%d] (%s): the move would show %.1f px of black at the frame edge (scale %.2f -> %.2f, position %s -> %s)" % (
                    i, s["id"], -worst, s0, s1, p0, p1))
            meta = {"filmcraft": {"scale_to_frame": False, "gain_db": 0.0, "source_in_ticks": 0, "duration_ticks": dur_ticks,
                                  "effects": [motion_effect(s0, s1, p0, p1, mo.get("ease", "Linear"), dur_ticks)]}}
        mk = [marker(m, m["at_frame"]) for m in s.get("markers", [])]
        n_markers += len(mk)
        items.append(clip(s["id"], s["source"], os.path.basename(s["source"]), 0, frames, avail_still, mk, meta))
        total += frames
        td = s.get("transition_out")
        if td:
            items.append(dissolve(td["frames"]))
            transitions += 1
    v1 = {"OTIO_SCHEMA": "Track.1", "name": "V1", "kind": "Video", "metadata": {}, "children": items}
    a_items = []
    cursor = 0
    audio = spec.get("audio", [])
    for a in audio:
        start = a.get("start_frame", 0)
        need(start >= cursor, "spec.audio: cues must be in time order and not overlap on one track")
        if start > cursor:
            a_items.append(gap(start - cursor))
        full = os.path.join(out_dir, *a["source"].split("/"))
        avail = wav_frames24(full) or a["duration_frames"]
        need(a["duration_frames"] <= avail, "spec.audio %s: duration_frames %d is longer than the file (%d frames at 24)" % (a["id"], a["duration_frames"], avail))
        meta = {"filmcraft": {"gain_db": float(a.get("gain_db", 0.0)), "source_in_ticks": 0, "duration_ticks": a["duration_frames"] * TICKS_PER_FRAME}}
        if a.get("duck_against"):
            meta["life_journey"] = {"duck_against": a["duck_against"]}
        a_items.append(clip(a["id"], a["source"], os.path.basename(a["source"]), 0, a["duration_frames"], avail, [], meta))
        cursor = start + a["duration_frames"]
    a1 = {"OTIO_SCHEMA": "Track.1", "name": "A1", "kind": "Audio", "metadata": {}, "children": a_items}
    children = [v1] + ([a1] if a_items else [])
    doc = {"OTIO_SCHEMA": "Timeline.1", "name": spec.get("name", "Life Journey timeline"), "global_start_time": rt(0),
           "metadata": {"life_journey": {"emitter": "emit_otio/1", "spec_schema": SCHEMA, "fps": FPS, "synthetic": bool(spec.get("synthetic_media"))}},
           "tracks": {"OTIO_SCHEMA": "Stack.1", "name": "tracks", "metadata": {},
                      "markers": [marker(m, m["at_frame"]) for m in spec.get("markers", [])], "children": children}}
    if spec.get("synthetic_media") and make_media_fn:        # only after every check above passed: a refused spec leaves nothing behind
        created = make_media_fn(out_dir, spec)
    info = {"clips": len(shots), "transitions": transitions, "markers": n_markers, "audio_cues": len(audio), "frames": total,
            "media_created": [p for p, what in created if what == "created"]}
    return doc, info


def timeline169(spec):
    """The input file of research/sources/format-round1/make_otio.py (it reads a file with exactly this shape)."""
    def move(s):
        mo = s.get("motion") or {}
        sc = mo.get("scale")
        if isinstance(sc, dict):
            return "zoom_out" if sc.get("direction") == "out" else ("zoom_in" if sc.get("zoom", 1.0) > 1.0 else "hold")
        return "hold" if not sc else ("zoom_in" if sc[1] > sc[0] else "zoom_out" if sc[1] < sc[0] else "hold")
    voice = (spec.get("audio") or [{"source": "media/mix.wav"}])[0]["source"]
    return {"fps": FPS, "width": spec["sequence"]["width"], "height": spec["sequence"]["height"], "crossfade": 1.0,
            "audio": {"voice": voice, "music": voice, "music_gain_db": -18},
            "shots": [{"id": s["id"], "file": s["source"], "dur": s["duration_frames"] / float(FPS), "move": move(s)} for s in spec["shots"]]}


def write_json(path, doc):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:      # UTF-8, no BOM, LF
        json.dump(doc, f, indent=2, ensure_ascii=True)
        f.write("\n")


def _make_media(out_dir, spec):
    import make_media
    sizes = {tuple(s["source_size"]) for s in spec["shots"] if s.get("source_size")}
    size = sizes.pop() if len(sizes) == 1 else (2880, 1620)
    res = []
    for i, s in enumerate(spec["shots"], 1):
        p = os.path.join(out_dir, *s["source"].split("/"))
        if os.path.exists(p):
            res.append((p, "kept"))
            continue
        make_media.still_png(p, size[0], size[1], i, s["id"].upper().replace("_", " "))
        res.append((p, "created"))
    for a in spec.get("audio", []):
        p = os.path.join(out_dir, *a["source"].split("/"))
        if os.path.exists(p):
            res.append((p, "kept"))
            continue
        make_media.sine_wav(p, a["duration_frames"] / float(FPS))
        res.append((p, "created"))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Neutral timeline spec to OTIO at 24 fps with metadata.filmcraft.")
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?", help="the .otio to write (leave out with --timeline169 to write only that file; no media is generated then)")
    ap.add_argument("--timeline169", metavar="PATH", help="also write the input file of the reused make_otio.py")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if not a.out and not a.timeline169:
        print("emit_otio: give OUT.otio, or --timeline169 PATH, or both", file=sys.stderr)
        return 2
    try:
        spec = load_spec(a.spec)
        if not a.out:
            write_json(a.timeline169, timeline169(spec))
            print("wrote %s (the make_otio.py input only; no .otio, no media)" % a.timeline169)
            return 0
        out_dir = os.path.dirname(os.path.abspath(a.out))
        doc, info = build(spec, out_dir, _make_media)
    except SpecError as e:
        print("emit_otio: invalid spec: %s" % e, file=sys.stderr)
        return 2
    except ImportError:
        print("emit_otio: Pillow is not installed, so the synthetic test cards can not be generated", file=sys.stderr)
        return 3
    write_json(a.out, doc)
    if a.timeline169:
        write_json(a.timeline169, timeline169(spec))
    print("wrote %s: %d clips, %d dissolves, %d markers, %d audio cue(s), %d frames at %d fps (%.1f s)%s" % (
        a.out, info["clips"], info["transitions"], info["markers"], info["audio_cues"], info["frames"], FPS, info["frames"] / float(FPS),
        ("; generated %d test media file(s)" % len(info["media_created"])) if info["media_created"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
