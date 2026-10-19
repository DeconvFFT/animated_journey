#!/usr/bin/env python3
"""validate_otio.py: does this OpenTimelineIO (.otio) file obey the Life Journey hand-off rules (R8)? READ-ONLY. Standard library only.

  python3 -I pipeline/roundtrip/validate_otio.py FILE.otio [--with-otio [PYTHON]] [--no-media-check] [--lenient-filmcraft] [--json OUT.json]
  python3 -I pipeline/roundtrip/validate_otio.py renders/wp06/ch.otio --with-otio /home/user/build-scratch/venv-otio/bin/python
  py -3 -I pipeline\\roundtrip\\validate_otio.py FILE.otio          (Windows PowerShell 5.1 or 7; UNVERIFIED there)

JSON-LEVEL RULES (each is one named check; a failing check prints FAIL <reason> and what is wrong)
  json_parses              the file is JSON                                                                 otio_json_invalid, otio_structure_unexpected (a shape no rule expects)
  timeline_schema          the root is a Timeline with a Stack of tracks, at least one Video track           schema_not_timeline, no_video_track
  rate_24                  every RationalTime in the file has rate 24 (W-14, S-01)                           rate_not_24
  clip_duration            every clip has a positive duration (source_range, else available_range)           clip_duration_invalid
  media_reference          every clip has an ExternalReference (not Missing, not an image sequence)          media_reference_missing, image_sequence_reference
  target_url_relative      target_url is a relative path with forward slashes (no drive, scheme, backslash)  target_url_absolute, target_url_backslash
  target_url_inside_folder no '..' segment in target_url: the hand-off folder must be copyable as a unit     target_url_escapes_folder
  media_exists             the file named by target_url exists, resolved from the .otio's folder             media_missing         (off with --no-media-check)
  clips_present            at least one Video track holds a Clip (an empty Video track hands over nothing)   no_clips
  track_children_flat      no Stack or Track inside a Track, no Stack inside the top Stack: clips in a nested   nested_composition
                           composition would never reach the per-clip rules above, so nesting is refused
  source_in_available      source_range lies inside available_range (when there is one)                     clip_outside_available_range
  dissolve_fits            each Transition sits between two clips and its in_offset and out_offset fit       dissolve_longer_than_neighbour, dissolve_without_neighbour,
                           inside them (a clip between two dissolves must hold both: out of one + in of the next)  dissolve_offset_invalid
  markers_present          the file carries at least one Marker (stack, track or clip)                       markers_missing
  filmcraft_keys_known     metadata.filmcraft has only known keys (scale_to_frame, gain_db, source_in_ticks, duration_ticks, effects, settings)   filmcraft_key_unknown
  filmcraft_effects        effects are motion with scale (Float) and position (Vec2) params; values well shaped   filmcraft_effect_unknown, filmcraft_value_shape
  filmcraft_keyframes      keyframe times are whole ticks, ascending, inside [0, duration_ticks]             filmcraft_keyframe_time
  filmcraft_ticks          duration_ticks and source_in_ticks agree with the clip at 24 fps within 1/1000 s  filmcraft_ticks_mismatch
  motion_edge_safe         where the media is a PNG: a Linear Ken Burns move never shows black at the frame edge (1080p assumed)   motion_edge_exposed
  (WARN only: interp names other than Linear and EaseOut, which are the two the evidenced template uses = filmcraft_interp_unverified)

--lenient-filmcraft turns the three filmcraft_*_unknown / value rules into WARN (for a file FilmCraft itself exported, which may carry more).
--with-otio [PYTHON]   also loads the file with opentimelineio in that interpreter (default <scratch>/venv-otio/bin/python, skipped with a WARN if
                       it is not there; an explicit PYTHON that does not exist is exit 3): version (pin 0.18.1), clip, transition and marker counts agree
                       with the JSON-level counts, the timeline duration agrees, and metadata.filmcraft survives a write and read unchanged.

EXIT CODES (build plan 4.3)  0 every check passes (WARN lines allowed)   1 a check failed   2 bad usage or no such file   3 environment (an explicit --with-otio interpreter is missing or broke)
It reads the .otio and the media it names (headers only), writes only the --json file, and prints the file name as you typed it.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt_common import Report  # noqa: E402
import kb_scale  # noqa: E402

RATE = 24
TICKS_PER_SECOND = 254016000000
TICK_TOLERANCE = TICKS_PER_SECOND // 1000
PINNED_OTIO = "0.18.1"
KNOWN_KEYS = {"scale_to_frame", "gain_db", "source_in_ticks", "duration_ticks", "effects", "settings"}
KNOWN_EFFECTS = {"motion"}
KNOWN_PARAMS = {"scale": "Float", "position": "Vec2"}
EVIDENCED_INTERP = {"Linear", "EaseOut"}
SEQ_W, SEQ_H = 1920, 1080


def schema_of(o):
    return o.get("OTIO_SCHEMA", "") if isinstance(o, dict) else ""


def is_a(o, name):
    return schema_of(o).split(".")[0] == name


def secs(t):
    """RationalTime dict to Fraction seconds (exact for whole-frame values)."""
    return Fraction(t["value"]) / Fraction(t["rate"])


def rt_ok(t):
    return isinstance(t, dict) and is_a(t, "RationalTime") and isinstance(t.get("value"), (int, float)) and isinstance(t.get("rate"), (int, float)) and t["rate"] > 0


def range_of(r):
    """TimeRange dict to (start, end) Fractions in seconds, or None."""
    if not (isinstance(r, dict) and rt_ok(r.get("start_time")) and rt_ok(r.get("duration"))):
        return None
    s, d = secs(r["start_time"]), secs(r["duration"])
    return s, s + d


def walk_rationals(o, path="$"):
    if isinstance(o, dict):
        if is_a(o, "RationalTime"):
            yield path, o
        for k, v in o.items():
            for x in walk_rationals(v, path + "." + k):
                yield x
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for x in walk_rationals(v, "%s[%d]" % (path, i)):
                yield x


def ref_of(clip):
    if "media_references" in clip:
        refs = clip.get("media_references") or {}
        return refs.get(clip.get("active_media_reference_key"))
    return clip.get("media_reference")


def item_duration(it):
    if is_a(it, "Transition"):
        return Fraction(0)
    r = range_of(it.get("source_range"))
    if r is None and is_a(it, "Clip"):
        ref = ref_of(it)
        r = range_of(ref.get("available_range")) if isinstance(ref, dict) else None
    return (r[1] - r[0]) if r else None


def png_size(path):
    import struct
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
            return struct.unpack(">II", head[16:24])
    except OSError:
        pass
    return None


def kf_value(v, kind):
    """Float -> float; Vec2 -> (x, y); else None."""
    try:
        if kind == "Float" and set(v) == {"Float"} and isinstance(v["Float"], (int, float)):
            return float(v["Float"])
        if kind == "Vec2" and set(v) == {"Vec2"} and set(v["Vec2"]) == {"x", "y"} and all(isinstance(v["Vec2"][a], (int, float)) for a in "xy"):
            return (float(v["Vec2"]["x"]), float(v["Vec2"]["y"]))
    except (TypeError, KeyError):
        pass
    return None


def validate(path, check_media=True, lenient=False):
    rep = Report("validate_otio", os.path.basename(path))
    info = {"clips": 0, "transitions": 0, "markers": 0, "frames": None}
    try:
        with open(path, "rb") as f:
            raw = f.read()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        doc = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError) as e:
        rep.fail("otio_json_invalid", "%s: %s" % (type(e).__name__, str(e)[:120]))
        return rep, info
    rep.ok("json_parses", "%d bytes" % len(raw))
    base = os.path.dirname(os.path.abspath(path))

    # ----- structure
    stack = doc.get("tracks") if isinstance(doc, dict) else None
    tracks = [t for t in (stack or {}).get("children", []) if is_a(t, "Track")] if is_a(stack or {}, "Stack") else []
    if not is_a(doc, "Timeline") or not is_a(stack or {}, "Stack"):
        rep.fail("schema_not_timeline", "root is %r with tracks %r (need Timeline and Stack)" % (schema_of(doc), schema_of(stack or {})))
        return rep, info
    rep.ok("timeline_schema", "%s, %d tracks" % (schema_of(doc), len(tracks)))
    rep.check(any(t.get("kind") == "Video" for t in tracks), "video_track_present", "no_video_track", "the Stack has no Video track", "a Video track exists")

    # ----- rate
    def rate_of(o):
        r = o.get("rate")
        return float(r) if isinstance(r, (int, float)) and not isinstance(r, bool) else None
    bad_rates = [(p, o.get("rate")) for p, o in walk_rationals(doc) if rate_of(o) != float(RATE)]
    n_rt = sum(1 for _ in walk_rationals(doc))
    rep.check(not bad_rates, "rate_24", "rate_not_24",
              "%d of %d times are not at %d fps (first: %s has rate %s)" % (len(bad_rates), n_rt, RATE, bad_rates[0][0], bad_rates[0][1]) if bad_rates else "",
              "all %d times are at %d fps" % (n_rt, RATE))

    # ----- clips
    P = {k: [] for k in ("clip_duration_invalid", "media_reference_missing", "image_sequence_reference", "target_url_absolute", "target_url_backslash",
                         "target_url_escapes_folder", "media_missing", "clip_outside_available_range")}
    clips = []
    for ti, tr in enumerate(tracks):
        for ci, it in enumerate(tr.get("children", [])):
            if is_a(it, "Clip"):
                clips.append((ti, ci, it))
    info["clips"] = len(clips)
    for ti, ci, c in clips:
        nm = "%s/%s" % (tracks[ti].get("name"), c.get("name"))
        d = item_duration(c)
        if d is None or d <= 0:
            P["clip_duration_invalid"].append(nm)
        ref = ref_of(c)
        if not isinstance(ref, dict) or is_a(ref, "MissingReference"):
            P["media_reference_missing"].append(nm)
            continue
        if is_a(ref, "ImageSequenceReference"):
            P["image_sequence_reference"].append(nm)
            continue
        if not is_a(ref, "ExternalReference"):
            P["media_reference_missing"].append("%s (%s)" % (nm, schema_of(ref)))
            continue
        url = ref.get("target_url") or ""
        absolute = url.startswith("/") or url.startswith("\\\\") or bool(re.match(r"^[A-Za-z]:[\\/]", url)) or "://" in url or url.startswith("file:")
        if not url:
            P["media_reference_missing"].append("%s (empty target_url)" % nm)
        elif absolute:
            P["target_url_absolute"].append("%s -> %s" % (nm, url[:60]))
        elif "\\" in url:
            P["target_url_backslash"].append("%s -> %s" % (nm, url[:60]))
        elif ".." in url.split("/"):                      # the same test emit_otio.is_rel applies to a spec; normpath would hide it, so look at the segments
            P["target_url_escapes_folder"].append("%s -> %s" % (nm, url[:60]))
        elif check_media and not os.path.isfile(os.path.normpath(os.path.join(base, *url.split("/")))):
            P["media_missing"].append("%s -> %s" % (nm, url))
        ar, sr = range_of(ref.get("available_range")), range_of(c.get("source_range"))
        if ar and sr and not (ar[0] <= sr[0] and sr[1] <= ar[1]):
            P["clip_outside_available_range"].append("%s: source %s..%ss is outside available %s..%ss" % (
                nm, float(sr[0]), float(sr[1]), float(ar[0]), float(ar[1])))
    ok_names = {"clip_duration_invalid": "clip_duration", "media_reference_missing": "media_reference", "image_sequence_reference": "media_reference_single_file",
                "target_url_absolute": "target_url_relative", "target_url_backslash": "target_url_forward_slashes",
                "target_url_escapes_folder": "target_url_inside_folder", "media_missing": "media_exists",
                "clip_outside_available_range": "source_in_available"}
    for reason in ("clip_duration_invalid", "media_reference_missing", "image_sequence_reference", "target_url_absolute", "target_url_backslash",
                   "target_url_escapes_folder", "media_missing", "clip_outside_available_range"):
        if reason == "media_missing" and not check_media:
            rep.warn("media_exists_skipped", "--no-media-check")
            continue
        rep.check(not P[reason], ok_names[reason], reason, "; ".join(P[reason][:5]) + (" (+%d more)" % (len(P[reason]) - 5) if len(P[reason]) > 5 else ""),
                  "all %d clips" % len(clips))

    # ----- something to hand over, and nothing hidden from the rules above
    video_clips = sum(1 for t in tracks if t.get("kind") == "Video" for it in (t.get("children") or []) if is_a(it, "Clip"))
    rep.check(video_clips > 0, "clips_present", "no_clips",
              "no Video track holds a Clip (%d clip(s) on other tracks): there is nothing to hand to FilmCraft" % len(clips),
              "%d clip(s) on the Video track(s)" % video_clips)
    nested = ["%s holds a %s" % (t.get("name"), schema_of(it).split(".")[0]) for t in tracks for it in (t.get("children") or []) if is_a(it, "Stack") or is_a(it, "Track")]
    nested += ["the top Stack holds a Stack named %r" % t.get("name") for t in (stack.get("children") or []) if is_a(t, "Stack")]
    rep.check(not nested, "track_children_flat", "nested_composition",
              "; ".join(nested[:4]) + " (clips inside a nested composition are not checked by the other rules; flatten the timeline)",
              "every track holds clips, gaps and transitions only")

    # ----- dissolves
    dprob = []
    n_trans = 0
    for tr in tracks:
        ch = tr.get("children", [])
        for i, it in enumerate(ch):
            if not is_a(it, "Transition"):
                continue
            n_trans += 1
            nm = "%s #%d" % (tr.get("name"), i)
            prev = ch[i - 1] if i > 0 else None
            nxt = ch[i + 1] if i + 1 < len(ch) else None
            if prev is None or nxt is None or is_a(prev, "Transition") or is_a(nxt, "Transition"):
                dprob.append(("dissolve_without_neighbour", "%s has no clip on both sides" % nm))
                continue
            if not (rt_ok(it.get("in_offset")) and rt_ok(it.get("out_offset"))):
                dprob.append(("dissolve_offset_invalid", "%s offsets are not RationalTimes" % nm))
                continue
            a, b = secs(it["in_offset"]), secs(it["out_offset"])
            if a < 0 or b < 0 or a + b == 0:
                dprob.append(("dissolve_offset_invalid", "%s offsets %s and %s" % (nm, float(a) * RATE, float(b) * RATE)))
                continue
            dp, dn = item_duration(prev), item_duration(nxt)
            if dp is not None and a > dp:
                dprob.append(("dissolve_longer_than_neighbour", "%s: in_offset %g frames is longer than the clip before it (%g frames)" % (nm, float(a) * RATE, float(dp) * RATE)))
            if dn is not None and b > dn:
                dprob.append(("dissolve_longer_than_neighbour", "%s: out_offset %g frames is longer than the clip after it (%g frames)" % (nm, float(b) * RATE, float(dn) * RATE)))
        for i, it in enumerate(ch):                       # a clip between two dissolves must hold both halves
            if is_a(it, "Clip") and 0 < i < len(ch) - 1 and is_a(ch[i - 1], "Transition") and is_a(ch[i + 1], "Transition"):
                t0, t1, d = ch[i - 1], ch[i + 1], item_duration(it)
                if rt_ok(t0.get("out_offset")) and rt_ok(t1.get("in_offset")) and d is not None and secs(t0["out_offset"]) + secs(t1["in_offset"]) > d:
                    dprob.append(("dissolve_longer_than_neighbour", "%s/%s: the two dissolves around it need %g frames, it has %g" % (
                        tr.get("name"), it.get("name"), float(secs(t0["out_offset"]) + secs(t1["in_offset"])) * RATE, float(d) * RATE)))
    info["transitions"] = n_trans
    for reason in ("dissolve_without_neighbour", "dissolve_offset_invalid", "dissolve_longer_than_neighbour"):
        rows = [d for r, d in dprob if r == reason]
        rep.check(not rows, {"dissolve_without_neighbour": "dissolve_between_clips", "dissolve_offset_invalid": "dissolve_offsets_valid",
                             "dissolve_longer_than_neighbour": "dissolve_fits"}[reason], reason, "; ".join(rows[:4]), "%d dissolve(s)" % n_trans)

    # ----- markers
    nm_stack = len(stack.get("markers", []) or [])
    nm_tracks = sum(len(t.get("markers", []) or []) for t in tracks)
    nm_clips = sum(len(c.get("markers", []) or []) for _, _, c in clips)
    info["markers"] = nm_stack + nm_tracks + nm_clips
    rep.check(info["markers"] > 0, "markers_present", "markers_missing", "no Marker anywhere in the file", "%d markers (%d on the stack, %d on clips)" % (
        info["markers"], nm_stack + nm_tracks, nm_clips))

    # ----- track length
    lengths = []
    for tr in tracks:
        tot = Fraction(0)
        for it in tr.get("children", []):
            d = item_duration(it)
            tot += d or 0
        lengths.append(tot)
    if lengths:
        info["frames"] = int(max(lengths) * RATE)

    # ----- metadata.filmcraft
    fm = {k: [] for k in ("filmcraft_key_unknown", "filmcraft_effect_unknown", "filmcraft_value_shape", "filmcraft_keyframe_time",
                          "filmcraft_ticks_mismatch", "motion_edge_exposed")}
    warn_interp = set()
    n_fc = 0
    for ti, ci, c in clips:
        meta = (c.get("metadata") or {}).get("filmcraft")
        if meta is None:
            continue
        n_fc += 1
        nm = "%s/%s" % (tracks[ti].get("name"), c.get("name"))
        if not isinstance(meta, dict):
            fm["filmcraft_value_shape"].append("%s: metadata.filmcraft is not an object" % nm)
            continue
        for k in sorted(set(meta) - KNOWN_KEYS):
            fm["filmcraft_key_unknown"].append("%s: key %r" % (nm, k))
        dur = item_duration(c)
        sr = range_of(c.get("source_range"))
        for key, expect in (("duration_ticks", (dur * TICKS_PER_SECOND) if dur is not None else None),
                            ("source_in_ticks", (sr[0] * TICKS_PER_SECOND) if sr else None)):
            if key in meta and expect is not None:
                if not isinstance(meta[key], int) or abs(Fraction(meta[key]) - expect) > TICK_TOLERANCE:
                    fm["filmcraft_ticks_mismatch"].append("%s: %s %r, the clip says %s" % (nm, key, meta[key], int(expect)))
        dur_ticks = meta.get("duration_ticks") if isinstance(meta.get("duration_ticks"), int) else (int(dur * TICKS_PER_SECOND) if dur is not None else None)
        if "gain_db" in meta and not isinstance(meta["gain_db"], (int, float)):
            fm["filmcraft_value_shape"].append("%s: gain_db is not a number" % nm)
        if "scale_to_frame" in meta and not isinstance(meta["scale_to_frame"], bool):
            fm["filmcraft_value_shape"].append("%s: scale_to_frame is not true or false" % nm)
        effects = meta.get("effects", [])
        if not isinstance(effects, list):
            fm["filmcraft_value_shape"].append("%s: effects is not a list" % nm)
            continue
        scale_keys, pos_keys = None, None
        for e in effects:
            if not isinstance(e, dict) or "effect" not in e or not isinstance(e.get("params", {}), dict):
                fm["filmcraft_value_shape"].append("%s: an effect without effect or params" % nm)
                continue
            if e["effect"] not in KNOWN_EFFECTS:
                fm["filmcraft_effect_unknown"].append("%s: effect %r" % (nm, e["effect"]))
                continue
            for pname, p in e.get("params", {}).items():
                kind = KNOWN_PARAMS.get(pname)
                if kind is None:
                    fm["filmcraft_effect_unknown"].append("%s: param %r of %s" % (nm, pname, e["effect"]))
                    continue
                if not isinstance(p, dict) or kf_value(p.get("value"), kind) is None:
                    fm["filmcraft_value_shape"].append("%s: %s value is not a %s" % (nm, pname, kind))
                    continue
                keys, last = [], -1
                for k in p.get("keyframes", []):
                    t = k.get("time") if isinstance(k, dict) else None
                    val = kf_value(k.get("value"), kind) if isinstance(k, dict) else None
                    if not isinstance(t, int) or isinstance(t, bool) or val is None:
                        fm["filmcraft_value_shape"].append("%s: a %s keyframe has time %r and value %r" % (nm, pname, t, k.get("value") if isinstance(k, dict) else k))
                        continue
                    if t < 0 or t < last or (dur_ticks is not None and t > dur_ticks + TICK_TOLERANCE):
                        fm["filmcraft_keyframe_time"].append("%s: %s keyframe at %d ticks (clip is %s)" % (nm, pname, t, dur_ticks))
                    last = t
                    if k.get("interp") not in EVIDENCED_INTERP:
                        warn_interp.add(str(k.get("interp")))
                    keys.append((t, val, k.get("interp")))
                if pname == "scale":
                    scale_keys = keys
                if pname == "position":
                    pos_keys = keys
        if scale_keys and pos_keys and len(scale_keys) == len(pos_keys):    # scale and position share the same keyframe times and easing, so the keys decide the edges
            ref = ref_of(c)
            url = (ref or {}).get("target_url") if isinstance(ref, dict) else None
            size = png_size(os.path.normpath(os.path.join(base, *url.split("/")))) if url and not url.startswith("/") and "://" not in url and ".." not in url.split("/") else None
            if size:
                ok, worst = kb_scale.move_is_edge_safe(size[0], size[1], SEQ_W, SEQ_H, [(s[1], p[1][0], p[1][1]) for s, p in zip(scale_keys, pos_keys)])
                if not ok:
                    fm["motion_edge_exposed"].append("%s: %.1f px of black at the frame edge" % (nm, -worst))
    soft_unknown = lenient
    groups = (("filmcraft_key_unknown", "filmcraft_keys_known", soft_unknown), ("filmcraft_effect_unknown", "filmcraft_effects", soft_unknown),
              ("filmcraft_value_shape", "filmcraft_values", soft_unknown), ("filmcraft_keyframe_time", "filmcraft_keyframes", False),
              ("filmcraft_ticks_mismatch", "filmcraft_ticks", False), ("motion_edge_exposed", "motion_edge_safe", False))
    for reason, okname, soft in groups:
        rep.check(not fm[reason], okname, reason, "; ".join(fm[reason][:4]), "%d clip(s) carry metadata.filmcraft" % n_fc, soft=soft)
    if warn_interp:
        rep.warn("filmcraft_interp_unverified", "interp name(s) %s are not in the evidenced template (Linear, EaseOut)" % ", ".join(sorted(warn_interp)))
    return rep, info


OTIO_PROBE = r'''
import json, sys
import opentimelineio as otio
path = sys.argv[1]
tl = otio.adapters.read_from_file(path)
clips = list(tl.find_clips())
trans = [t for tr in tl.tracks for t in tr if isinstance(t, otio.schema.Transition)]
raw = json.load(open(path, encoding="utf-8"))
again = json.loads(otio.adapters.write_to_string(tl, "otio_json"))
def fm(doc):
    out = {}
    for tr in doc["tracks"]["children"]:
        for it in tr["children"]:
            if it.get("OTIO_SCHEMA", "").startswith("Clip"):
                out[tr["name"] + "/" + it["name"]] = (it.get("metadata") or {}).get("filmcraft")
    return out
print(json.dumps({"version": otio.__version__, "clips": len(clips), "transitions": len(trans),
                  "markers": len(tl.tracks.markers) + sum(len(t.markers) for t in tl.tracks) + sum(len(c.markers) for c in clips),
                  "duration_frames": tl.duration().rescaled_to(24).value, "global_start_rate": tl.global_start_time.rate,
                  "filmcraft_preserved": fm(raw) == fm(again), "clips_with_filmcraft": sum(1 for v in fm(raw).values() if v is not None)}))
'''


def otio_probe(rep, info, path, py):
    """Load the file in the opentimelineio interpreter and compare with the JSON-level numbers. Returns 0 or 3."""
    try:
        p = subprocess.run([py, "-I", "-c", OTIO_PROBE, os.path.abspath(path)], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=90)
    except (OSError, subprocess.TimeoutExpired) as e:
        print("validate_otio: could not run the opentimelineio interpreter: %s" % type(e).__name__, file=sys.stderr)
        return 3
    if p.returncode != 0:
        msg = (p.stderr.decode("utf-8", "replace").strip().splitlines() or ["(no message)"])[-1]
        if "No module named" in msg and "opentimelineio" in msg:
            print("validate_otio: that interpreter has no opentimelineio module (%s)" % msg[:120], file=sys.stderr)
            return 3
        rep.fail("otio_load_failed", msg[:200])
        return 0
    r = json.loads(p.stdout.decode("utf-8").strip().splitlines()[-1])
    rep.ok("otio_loads", "opentimelineio %s read the file" % r["version"])
    if r["version"] == PINNED_OTIO:
        rep.ok("otio_version_pinned", PINNED_OTIO)
    else:
        rep.warn("otio_version_unpinned", "opentimelineio %s, the pin is %s" % (r["version"], PINNED_OTIO))
    same = (r["clips"], r["transitions"], r["markers"]) == (info["clips"], info["transitions"], info["markers"])
    rep.check(same, "otio_counts_match", "otio_counts_differ", "library: %d clips, %d transitions, %d markers; JSON: %d, %d, %d" % (
        r["clips"], r["transitions"], r["markers"], info["clips"], info["transitions"], info["markers"]),
        "%d clips, %d transitions, %d markers" % (r["clips"], r["transitions"], r["markers"]))
    if info["frames"] is not None:
        rep.check(int(round(r["duration_frames"])) == info["frames"], "otio_duration_matches", "otio_duration_differs",
                  "library says %s frames, the JSON adds up to %s" % (r["duration_frames"], info["frames"]), "%d frames at 24 fps" % info["frames"])
    rep.check(r["global_start_rate"] == RATE, "otio_global_start_rate", "otio_global_start_rate_not_24", "global_start_time rate %s" % r["global_start_rate"], "rate 24")
    if r["clips_with_filmcraft"]:
        rep.check(r["filmcraft_preserved"], "otio_filmcraft_preserved", "otio_filmcraft_lost",
                  "metadata.filmcraft changed after a write and read by the library", "%d clip(s): unchanged after write and read" % r["clips_with_filmcraft"])
    return 0


def default_py():
    scratch = os.environ.get("LJ_SCRATCH") or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "build-scratch"))
    return os.path.join(scratch, "venv-otio", "bin", "python")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check an OTIO file against the Life Journey hand-off rules (read-only).")
    ap.add_argument("otio")
    ap.add_argument("--with-otio", nargs="?", const="auto", metavar="PYTHON")
    ap.add_argument("--no-media-check", action="store_true")
    ap.add_argument("--lenient-filmcraft", action="store_true")
    ap.add_argument("--json", metavar="OUT.json")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if not os.path.isfile(a.otio):
        print("validate_otio: no such file: %s" % a.otio, file=sys.stderr)
        return 2
    try:
        rep, info = validate(a.otio, not a.no_media_check, a.lenient_filmcraft)
    except Exception as e:      # noqa: BLE001 - a file shaped in a way no rule expected must be a named finding, not a traceback
        rep = Report("validate_otio", os.path.basename(a.otio))
        rep.fail("otio_structure_unexpected", "%s: %s (the file is shaped in a way the rules do not expect)" % (type(e).__name__, str(e)[:100]))
        return rep.finish(a.json)
    if a.with_otio:
        py = default_py() if a.with_otio == "auto" else a.with_otio
        if not os.path.isfile(py):
            if a.with_otio != "auto":
                print("validate_otio: the --with-otio interpreter does not exist", file=sys.stderr)
                return 3
            rep.warn("otio_load_skipped", "no opentimelineio venv found (<scratch>/venv-otio); JSON-level checks only")
        else:
            if "json_parses" in [c for _, c, _ in rep.rows] and "schema_not_timeline" not in rep.failed_codes():
                rc = otio_probe(rep, info, a.otio, py)
                if rc:
                    return rc
    return rep.finish(a.json)


if __name__ == "__main__":
    sys.exit(main())
