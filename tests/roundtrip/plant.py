"""plant.py: plant defects in the synthetic ORA and OTIO files (WP-06 tests only). Standard library only.

Every function takes a good file and writes a damaged copy that has exactly the one defect named. Nothing here reads or writes anything but the two
paths it is given. The synthetic files come from pipeline/roundtrip/emit_ora_layers.py and emit_otio.py; no photograph is involved.
"""
import copy
import json
import re
import struct
import zipfile
import zlib

STAMP = (1980, 1, 1, 0, 0, 0)


# ----------------------------------------------------------------------------------------------------------------------- ORA
def read_members(path):
    """[(name, bytes, compress_type)] in archive order."""
    out = []
    with zipfile.ZipFile(path) as z:
        for i in z.infolist():
            out.append([i.filename, z.read(i.filename), i.compress_type])
    return out


def write_members(path, members):
    with zipfile.ZipFile(path, "w") as z:
        for name, data, method in members:
            zi = zipfile.ZipInfo(name, STAMP)
            zi.compress_type = method
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def _stack(members, fn):
    for m in members:
        if m[0] == "stack.xml":
            m[1] = fn(m[1].decode("utf-8")).encode("utf-8")


def png_bytes(width, height, colour_type=6, bit_depth=8):
    """A tiny valid PNG (flat grey), any colour type and depth the tests need."""
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[colour_type]
    row = b"\x00" + bytes([128]) * (channels * width * (bit_depth // 8))
    raw = row * height

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, bit_depth, colour_type, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


ORA_DEFECTS = {
    # name: (the reason code it must trigger, description)
    "missing_layer_png": ("layer_png_missing", "the PNG of layer L20_figure is removed from the archive"),
    "duplicate_name": ("layer_name_duplicate", "layer L20_figure is renamed L10_restored"),
    "layer_outside_canvas": ("layer_outside_canvas", "layer L20_figure moved to x=500 so it leaves the 640x360 canvas"),
    "mimetype_not_first": ("mimetype_not_first", "stack.xml is written before mimetype"),
    "mimetype_not_stored": ("mimetype_not_stored", "mimetype is deflated instead of stored"),
    "mimetype_wrong": ("mimetype_wrong", "mimetype says image/png"),
    "layer_name_invalid": ("layer_name_invalid", "layer L20_figure is renamed 'L20 figure' (a space)"),
    "asfound_not_bottom": ("asfound_not_bottom", "L10_restored and L00_asfound swap places in stack.xml"),
    "zip_unreadable": ("zip_unreadable", "the file is cut short"),
    "stack_xml_unparseable": ("stack_xml_unparseable", "stack.xml is not XML"),
    "stack_xml_dtd": ("stack_xml_dtd", "stack.xml carries an entity declaration"),
    "attribute_unsupported": ("attribute_unsupported", "layer L20_figure gets edit-locked=\"true\" (locks do not round-trip)"),
    "layer_png_format": ("layer_png_format", "layer L10_restored is an RGB PNG without alpha"),
    "layer_png_invalid": ("layer_png_invalid", "the PNG of layer L10_restored is cut short"),
    "mergedimage_size": ("mergedimage_size", "mergedimage.png is 10x10"),
    "src_path_unsafe": ("src_path_unsafe", "layer L20_figure src is an absolute path"),
    "layer_src_missing": ("layer_src_missing", "layer L20_figure has no src attribute"),
    "layer_value_invalid": ("layer_value_invalid", "layer L20_figure opacity is 1.5"),
    "no_stack_xml": ("stack_xml_missing", "the stack.xml member is removed"),
}


def plant_ora(kind, src, dst):
    if kind == "zip_unreadable":
        data = open(src, "rb").read()
        open(dst, "wb").write(data[: len(data) // 2])
        return
    m = read_members(src)
    names = [x[0] for x in m]
    if kind == "missing_layer_png":
        m = [x for x in m if x[0] != "data/L20_figure.png"]
    elif kind == "duplicate_name":
        _stack(m, lambda s: s.replace('name="L20_figure"', 'name="L10_restored"'))
    elif kind == "layer_outside_canvas":
        _stack(m, lambda s: re.sub(r'(name="L20_figure" src="[^"]+" x=")\d+', r"\g<1>500", s))
    elif kind == "mimetype_not_first":
        i, j = names.index("mimetype"), names.index("stack.xml")
        m[i], m[j] = m[j], m[i]
    elif kind == "mimetype_not_stored":
        m[names.index("mimetype")][2] = zipfile.ZIP_DEFLATED
    elif kind == "mimetype_wrong":
        m[names.index("mimetype")][1] = b"image/png"
    elif kind == "layer_name_invalid":
        _stack(m, lambda s: s.replace('name="L20_figure"', 'name="L20 figure"'))
    elif kind == "asfound_not_bottom":
        def swap(s):
            lines = s.split("\n")
            a = [i for i, l in enumerate(lines) if 'name="L10_restored"' in l][0]
            b = [i for i, l in enumerate(lines) if 'name="L00_asfound"' in l][0]
            lines[a], lines[b] = lines[b], lines[a]
            return "\n".join(lines)
        _stack(m, swap)
    elif kind == "stack_xml_unparseable":
        _stack(m, lambda s: "this is not xml <<<")
    elif kind == "stack_xml_dtd":
        _stack(m, lambda s: s.replace("<image ", '<!DOCTYPE image [<!ENTITY e "x">]><image ', 1).replace("?>\n", "?>\n", 1))
    elif kind == "attribute_unsupported":
        _stack(m, lambda s: s.replace('name="L20_figure"', 'name="L20_figure" edit-locked="true"'))
    elif kind == "layer_png_format":
        m[names.index("data/L10_restored.png")][1] = png_bytes(640, 360, colour_type=2)
    elif kind == "layer_png_invalid":
        k = names.index("data/L10_restored.png")
        m[k][1] = m[k][1][:40]
    elif kind == "mergedimage_size":
        m[names.index("mergedimage.png")][1] = png_bytes(10, 10)
    elif kind == "src_path_unsafe":
        _stack(m, lambda s: s.replace('src="data/L20_figure.png"', 'src="/data/L20_figure.png"'))
    elif kind == "layer_src_missing":
        _stack(m, lambda s: s.replace(' src="data/L20_figure.png"', ""))
    elif kind == "layer_value_invalid":
        _stack(m, lambda s: re.sub(r'(name="L20_figure"[^>]*opacity=")[^"]+', r"\g<1>1.5", s))
    elif kind == "no_stack_xml":
        m = [x for x in m if x[0] != "stack.xml"]
    else:
        raise ValueError(kind)
    write_members(dst, m)


# ----------------------------------------------------------------------------------------------------------------------- OTIO
def _clips(doc, track=0):
    return [c for c in doc["tracks"]["children"][track]["children"] if c["OTIO_SCHEMA"].startswith("Clip")]


def _all_rates(o, rate):
    if isinstance(o, dict):
        if o.get("OTIO_SCHEMA", "").startswith("RationalTime"):
            o["rate"] = rate
        for v in o.values():
            _all_rates(v, rate)
    elif isinstance(o, list):
        for v in o:
            _all_rates(v, rate)


# (reason code the validator must name, description, codes that may legitimately accompany it because the file is otherwise consistent)
OTIO_DEFECTS = {
    "clip_outside_available_range": ("clip_outside_available_range", "the available_range of ch01_s02 is cut to 100 frames while the clip uses 120", ()),
    "rate_not_24_one_time": ("rate_not_24", "global_start_time is written at the old project rate", ()),
    "rate_not_24_whole_file": ("rate_not_24", "every rate in the file is the old project rate (an un-rebased template)", ("filmcraft_ticks_mismatch",)),
    "media_missing": ("media_missing", "ch01_s03 points at media/ch01_s99.png, which does not exist", ()),
    "dissolve_longer_than_neighbour": ("dissolve_longer_than_neighbour", "the first dissolve is 400 frames (in_offset 200) next to a 120-frame clip", ()),
    "dissolve_pair_too_long": ("dissolve_longer_than_neighbour", "the two dissolves around ch01_s02 need 140 frames and the clip has 120", ()),
    "target_url_absolute": ("target_url_absolute", "ch01_s01 uses a file:// URL with a drive letter", ()),
    "target_url_backslash": ("target_url_backslash", "ch01_s01 uses media\\ch01_s01.png", ()),
    "image_sequence_reference": ("image_sequence_reference", "ch01_s01 uses an ImageSequenceReference", ()),
    "media_reference_missing": ("media_reference_missing", "ch01_s01 has a MissingReference", ()),
    "markers_missing": ("markers_missing", "every marker is removed", ()),
    "filmcraft_key_unknown": ("filmcraft_key_unknown", "metadata.filmcraft gets a key FilmCraft does not read", ()),
    "filmcraft_effect_unknown": ("filmcraft_effect_unknown", "an effect named blur is added", ()),
    "filmcraft_value_shape": ("filmcraft_value_shape", "the scale value is a bare number instead of {\"Float\": n}", ()),
    "filmcraft_keyframe_time": ("filmcraft_keyframe_time", "a keyframe sits beyond the end of the clip", ()),
    "filmcraft_ticks_mismatch": ("filmcraft_ticks_mismatch", "duration_ticks says 6 s for a 5 s clip", ()),
    "motion_edge_exposed": ("motion_edge_exposed", "ch01_s01 drifts 200 px sideways at the start scale, so black shows", ()),
    "dissolve_without_neighbour": ("dissolve_without_neighbour", "a dissolve is the last item of the track", ()),
    "no_video_track": ("no_video_track", "the Video track is renamed Audio", ()),
    "schema_not_timeline": ("schema_not_timeline", "the root is a Stack", ()),
    "otio_json_invalid": ("otio_json_invalid", "the file is cut short", ()),
    "clip_duration_invalid": ("clip_duration_invalid", "ch01_s02 has a zero-length source_range", ("filmcraft_ticks_mismatch", "dissolve_longer_than_neighbour")),
}


def plant_otio(kind, src, dst):
    raw = open(src, encoding="utf-8").read()
    if kind == "otio_json_invalid":
        open(dst, "w", encoding="utf-8").write(raw[: len(raw) // 2])
        return
    d = json.loads(raw)
    v = d["tracks"]["children"][0]["children"]
    clips = _clips(d)
    if kind == "clip_outside_available_range":
        clips[1]["media_references"]["DEFAULT_MEDIA"]["available_range"]["duration"]["value"] = 100.0
    elif kind == "rate_not_24_one_time":
        d["global_start_time"]["rate"] = 25.0
    elif kind == "rate_not_24_whole_file":
        _all_rates(d, 25.0)
    elif kind == "media_missing":
        clips[2]["media_references"]["DEFAULT_MEDIA"]["target_url"] = "media/ch01_s99.png"
    elif kind == "dissolve_longer_than_neighbour":
        t = [x for x in v if x["OTIO_SCHEMA"].startswith("Transition")][0]
        t["in_offset"]["value"], t["out_offset"]["value"] = 200.0, 200.0
    elif kind == "dissolve_pair_too_long":
        ts = [x for x in v if x["OTIO_SCHEMA"].startswith("Transition")]
        ts[0]["out_offset"]["value"] = 70.0
        ts[1]["in_offset"]["value"] = 70.0
        ts[0]["in_offset"]["value"] = 12.0
        ts[1]["out_offset"]["value"] = 12.0
    elif kind == "target_url_absolute":
        clips[0]["media_references"]["DEFAULT_MEDIA"]["target_url"] = "file:///C:/lj/media/ch01_s01.png"
    elif kind == "target_url_backslash":
        clips[0]["media_references"]["DEFAULT_MEDIA"]["target_url"] = "media\\ch01_s01.png"
    elif kind == "image_sequence_reference":
        clips[0]["media_references"]["DEFAULT_MEDIA"] = {"OTIO_SCHEMA": "ImageSequenceReference.1", "target_url_base": "media/", "name_prefix": "ch01_s",
                                                         "name_suffix": ".png", "start_frame": 1, "frame_step": 1, "rate": 24.0, "frame_zero_padding": 2,
                                                         "missing_frame_policy": "error", "available_range": None, "metadata": {}}
    elif kind == "media_reference_missing":
        clips[0]["media_references"]["DEFAULT_MEDIA"] = {"OTIO_SCHEMA": "MissingReference.1", "name": "", "available_range": None, "metadata": {}}
    elif kind == "markers_missing":
        d["tracks"]["markers"] = []
        for c in clips + _clips(d, 1):
            c["markers"] = []
    elif kind == "filmcraft_key_unknown":
        clips[0]["metadata"]["filmcraft"]["warp_factor"] = 3
    elif kind == "filmcraft_effect_unknown":
        clips[0]["metadata"]["filmcraft"]["effects"].append({"effect": "blur", "enabled": True, "params": {}})
    elif kind == "filmcraft_value_shape":
        clips[0]["metadata"]["filmcraft"]["effects"][0]["params"]["scale"]["value"] = 66.67
    elif kind == "filmcraft_keyframe_time":
        clips[0]["metadata"]["filmcraft"]["effects"][0]["params"]["scale"]["keyframes"][1]["time"] = 99999999999999
    elif kind == "filmcraft_ticks_mismatch":
        clips[0]["metadata"]["filmcraft"]["duration_ticks"] = 6 * 254016000000
    elif kind == "motion_edge_exposed":
        p = clips[0]["metadata"]["filmcraft"]["effects"][0]["params"]["position"]
        p["keyframes"][0]["value"] = {"Vec2": {"x": 760.0, "y": 540.0}}
        p["value"] = {"Vec2": {"x": 760.0, "y": 540.0}}
    elif kind == "dissolve_without_neighbour":
        v.append(copy.deepcopy([x for x in v if x["OTIO_SCHEMA"].startswith("Transition")][0]))
    elif kind == "no_video_track":
        d["tracks"]["children"][0]["kind"] = "Audio"
    elif kind == "schema_not_timeline":
        d["OTIO_SCHEMA"] = "Stack.1"
    elif kind == "clip_duration_invalid":
        clips[1]["source_range"]["duration"]["value"] = 0.0
    else:
        raise ValueError(kind)
    open(dst, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=2) + "\n")


def nested_group_ora(src, dst, version="0.0.3", isolation=True):
    """A GOOD file with a nested group: L20_figure and L10_restored inside <stack name="G10_group">. Used for the valid-group tests, not as a defect."""
    m = read_members(src)

    def wrap(s):
        lines = s.split("\n")
        a = [i for i, l in enumerate(lines) if 'name="L20_figure"' in l][0]
        b = [i for i, l in enumerate(lines) if 'name="L10_restored"' in l][0]
        iso = ' isolation="isolate"' if isolation else ""
        lines.insert(b + 1, "</stack>")
        lines.insert(a, '<stack name="G10_group"%s>' % iso)
        return "\n".join(lines).replace('version="0.0.3"', 'version="%s"' % version)
    _stack(m, wrap)
    write_members(dst, m)
