#!/usr/bin/env python3
"""validate_ora.py: does this OpenRaster (.ora) file obey the Life Journey hand-off rules (R8)? READ-ONLY. Standard library only.

  python3 -I pipeline/roundtrip/validate_ora.py FILE.ora [--profile auto|pipeline|reference] [--allow-offcanvas] [--json OUT.json]
  py -3 -I pipeline\\roundtrip\\validate_ora.py FILE.ora          (Windows PowerShell 5.1 or 7; UNVERIFIED there)

RULES (each is a named check; a failing check prints FAIL <code> and the detail)
  zip_opens               the zip opens and every member passes its CRC                              zip_unreadable
  zip_entries_safe        no duplicate member names, no absolute or '..' paths, total size bounded    zip_duplicate_entry, zip_entry_unsafe, zip_too_large
  mimetype_first          'mimetype' is the first member                                              mimetype_missing, mimetype_not_first
  mimetype_stored         ... and stored, not deflated                                                mimetype_not_stored
  mimetype_content        ... and says exactly image/openraster                                       mimetype_wrong
  stack_xml               stack.xml exists, has no DTD or entity, parses, root <image> has w and h    stack_xml_missing, stack_xml_dtd, stack_xml_unparseable, canvas_size_invalid
  layer_src               every <layer> has a src                                                     layer_src_missing
  layer_png_present       every src exists in the zip (path inside the archive, not absolute)         layer_png_missing, src_path_unsafe
  layer_png_valid         every layer PNG is a well-formed PNG                                        layer_png_invalid
  layer_png_format        8-bit RGBA (straight alpha), no non-sRGB profile                            layer_png_format
  layer_inside_canvas     x, y >= 0 and x + width <= canvas width, y + height <= canvas height         layer_outside_canvas   (WARN with --allow-offcanvas)
  layer_name_unique       names are unique (layers and groups together)                               layer_name_duplicate
  layer_name_pattern      names match ^[A-Za-z][A-Za-z0-9._-]*$                                       layer_name_invalid     (WARN in the reference profile)
  attributes_supported    only the attributes PhotoCraft reads: image version w h xres yres;          attribute_unsupported  (WARN in the reference profile)
                          layer name src x y opacity visibility composite-op; stack adds isolation
  values_valid            opacity 0..1, visibility visible|hidden, composite-op a known svg: operator, x and y whole numbers     layer_value_invalid
  asfound_bottom          pipeline profile only: the bottom layer (last in stack.xml) is L00_asfound   asfound_not_bottom
  mergedimage             mergedimage.png exists and is as large as the canvas                        mergedimage_missing, mergedimage_size

PROFILES  A file we author names its layers by id (L00_asfound, L10_sky ...), so the pipeline profile fails on an invalid name and
  requires L00_asfound at the bottom (W-27). A foreign or reference file (for example the PhotoCraft acceptance fixture, whose layers are
  called 'Title tint' and 'Photo') is checked with the reference profile: the same structural rules, but the naming rules are WARN.
  auto (the default) picks pipeline when any layer name starts with L and two digits and an underscore, else reference.

EXIT CODES (build plan 4.3)  0 every check passes (WARN lines allowed)   1 a check failed   2 bad usage or no such file   3 environment problem
It reads the one file you name, writes only the --json file, and never changes the .ora. It prints the file name as you typed it.
"""
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt_common import Report, png_info  # noqa: E402

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")
LADDER_RE = re.compile(r"^L\d\d_")
IMAGE_ATTRS = {"version", "w", "h", "xres", "yres"}
STACK_ATTRS = {"name", "opacity", "visibility", "composite-op", "isolation", "x", "y"}
LAYER_ATTRS = {"name", "src", "x", "y", "opacity", "visibility", "composite-op"}
COMPOSITE_OPS = {"svg:src-over", "svg:multiply", "svg:screen", "svg:overlay", "svg:darken", "svg:lighten", "svg:color-dodge",
                 "svg:color-burn", "svg:hard-light", "svg:soft-light", "svg:difference", "svg:exclusion", "svg:hue",
                 "svg:saturation", "svg:color", "svg:luminosity", "svg:plus", "svg:dst-in", "svg:dst-out", "svg:src-atop",
                 "svg:dst-atop"}
MAX_TOTAL_BYTES = 512 * 1024 * 1024
STANDARD_MEMBERS = {"mimetype", "stack.xml", "mergedimage.png", "Thumbnails/thumbnail.png"}


def local(tag):
    return tag.split("}")[-1]


def walk(elem, depth=0):
    """Yield (element, depth) for every <layer> and <stack> below elem, in document order (top-first)."""
    for child in elem:
        t = local(child.tag)
        if t in ("layer", "stack"):
            yield child, depth
            if t == "stack":
                for x in walk(child, depth + 1):
                    yield x


def validate(path, profile="auto", allow_offcanvas=False):
    rep = Report("validate_ora", os.path.basename(path))
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError, EOFError, ValueError, NotImplementedError) as e:
        rep.fail("zip_unreadable", "%s: %s" % (type(e).__name__, str(e)[:120]))
        rep.extra["profile"] = profile if profile != "auto" else "reference"
        return rep
    with zf:
        declared = sum(i.file_size for i in zf.infolist())
        if declared > MAX_TOTAL_BYTES:          # refuse before decompressing anything (a zip bomb)
            rep.fail("zip_too_large", "declared uncompressed size %d bytes is over %d; not opened further" % (declared, MAX_TOTAL_BYTES))
            rep.extra["profile"] = profile if profile != "auto" else "reference"
            return rep
        try:
            bad = zf.testzip()
        except Exception as e:  # noqa: BLE001 - any decode problem is a finding
            bad = "(%s)" % type(e).__name__
        if bad:
            rep.fail("zip_unreadable", "member %s fails its CRC or cannot be read" % bad)
            rep.extra["profile"] = profile if profile != "auto" else "reference"
            return rep
        rep.ok("zip_opens", "%d members" % len(zf.infolist()))
        infos = zf.infolist()
        names = [i.filename for i in infos]

        # -------- archive hygiene
        dup = sorted({n for n in names if names.count(n) > 1})
        unsafe = [n for n in names if n.startswith("/") or "\\" in n or ".." in n.split("/") or re.match(r"^[A-Za-z]:", n)]
        total = sum(i.file_size for i in infos)
        rep.check(not dup, "zip_names_unique", "zip_duplicate_entry", "duplicate member names: " + ", ".join(dup[:5]), "no duplicate member names")
        rep.check(not unsafe, "zip_paths_safe", "zip_entry_unsafe", "unsafe member paths: " + ", ".join(unsafe[:5]), "member paths are plain relative paths")
        rep.check(total <= MAX_TOTAL_BYTES, "zip_size_bounded", "zip_too_large", "uncompressed size %d bytes is over %d" % (total, MAX_TOTAL_BYTES),
                  "uncompressed size %d bytes" % total)

        # -------- mimetype
        if "mimetype" not in names:
            rep.fail("mimetype_missing", "no 'mimetype' member")
        else:
            rep.check(names[0] == "mimetype", "mimetype_first", "mimetype_not_first", "first member is %r, not 'mimetype'" % names[0], "'mimetype' is the first member")
            mi = next(i for i in infos if i.filename == "mimetype")
            rep.check(mi.compress_type == zipfile.ZIP_STORED, "mimetype_stored", "mimetype_not_stored",
                      "'mimetype' is compressed (method %d); it must be stored" % mi.compress_type, "'mimetype' is stored")
            content = zf.read("mimetype")
            rep.check(content == b"image/openraster", "mimetype_content", "mimetype_wrong", "'mimetype' holds %r" % content[:40], "'mimetype' says image/openraster")

        # -------- stack.xml
        root = None
        if "stack.xml" not in names:
            rep.fail("stack_xml_missing", "no 'stack.xml' member")
        else:
            raw = zf.read("stack.xml")
            if b"<!DOCTYPE" in raw or b"<!ENTITY" in raw:
                rep.fail("stack_xml_dtd", "stack.xml declares a DTD or an entity; refused (untrusted XML)")
            else:
                try:
                    root = ET.fromstring(raw)
                    rep.ok("stack_xml_parses", "root <%s>" % local(root.tag))
                except ET.ParseError as e:
                    rep.fail("stack_xml_unparseable", str(e)[:120])
        layers, stacks, canvas = [], [], None
        if root is not None:
            def whole(v):
                try:
                    return int(v) if re.match(r"^-?\d+$", str(v).strip()) else None
                except (TypeError, ValueError):
                    return None
            w, h = whole(root.get("w")), whole(root.get("h"))
            ok = local(root.tag) == "image" and w and h and w > 0 and h > 0
            rep.check(ok, "canvas_size", "canvas_size_invalid", "root is <%s> with w=%r h=%r" % (local(root.tag), root.get("w"), root.get("h")),
                      "canvas %sx%s" % (w, h))
            if ok:
                canvas = (w, h)
            stack_el = next((c for c in root if local(c.tag) == "stack"), None)
            if stack_el is None:
                rep.fail("stack_missing", "<image> has no <stack>")
            else:
                for el, depth in walk(stack_el):
                    (layers if local(el.tag) == "layer" else stacks).append(el)
                if not layers:
                    rep.fail("no_layers", "the stack has no <layer>")
            # profile
            if profile == "auto":
                profile = "pipeline" if any(LADDER_RE.match(L.get("name") or "") for L in layers) else "reference"
            rep.extra["profile"] = profile
            strict = profile == "pipeline"

            # -------- attributes
            bad_img = sorted(set(root.attrib) - IMAGE_ATTRS)
            bad = ["image@" + a for a in bad_img]
            bad += ["stack@" + a for s in ([stack_el] if stack_el is not None else []) + stacks for a in sorted(set(s.attrib) - STACK_ATTRS)]
            bad += ["layer(%s)@%s" % (L.get("name"), a) for L in layers for a in sorted(set(L.attrib) - LAYER_ATTRS)]
            rep.check(not bad, "attributes_supported", "attribute_unsupported", "unsupported: " + ", ".join(bad[:8]), "only supported attributes", soft=not strict)
            ver = tuple(int(p) for p in re.findall(r"\d+", root.get("version") or "0.0.3"))
            if stacks and ver >= (0, 0, 6) and any(s.get("isolation") is None for s in stacks):
                rep.warn("group_isolation_implicit", "version %s group without isolation: v0.10.0 reads it as isolate" % root.get("version"))

            # -------- names
            nm = [L.get("name") for L in layers] + [s.get("name") for s in stacks if s.get("name")]
            missing_name = [i for i, L in enumerate(layers) if not L.get("name")]
            rep.check(not missing_name, "layer_names_present", "layer_name_missing", "layers without a name at positions %s" % missing_name[:6], "every layer has a name")
            dupn = sorted({n for n in nm if n and nm.count(n) > 1})
            rep.check(not dupn, "layer_name_unique", "layer_name_duplicate", "duplicate names: " + ", ".join(dupn), "layer names are unique")
            badn = [n for n in nm if n and not NAME_RE.match(n)]
            rep.check(not badn, "layer_name_pattern", "layer_name_invalid", "names that do not match ^[A-Za-z][A-Za-z0-9._-]*$: " + ", ".join(repr(n) for n in badn[:6]),
                      "layer names match the id pattern", soft=not strict)

            # -------- values
            problems = []
            for L in layers:
                nme = L.get("name")
                try:
                    o = float(L.get("opacity", "1.0"))
                    if not 0.0 <= o <= 1.0:
                        problems.append("%s opacity %s" % (nme, L.get("opacity")))
                except ValueError:
                    problems.append("%s opacity %r" % (nme, L.get("opacity")))
                if L.get("visibility", "visible") not in ("visible", "hidden"):
                    problems.append("%s visibility %r" % (nme, L.get("visibility")))
                op = L.get("composite-op", "svg:src-over")
                if op not in COMPOSITE_OPS:
                    problems.append("%s composite-op %r" % (nme, op))
                for a in ("x", "y"):
                    if whole(L.get(a, "0")) is None:
                        problems.append("%s %s %r" % (nme, a, L.get(a)))
            rep.check(not problems, "values_valid", "layer_value_invalid", "; ".join(problems[:6]), "opacity, visibility, composite-op, x, y are valid",
                      soft=not strict)

            # -------- layer images (one row per kind of problem, listing every layer that has it)
            P = {"layer_src_missing": [], "src_path_unsafe": [], "layer_png_missing": [], "layer_png_invalid": [], "layer_png_format": [],
                 "layer_outside_canvas": []}
            n_ok_png = 0
            for L in layers:
                nme = L.get("name") or "(unnamed)"
                src = L.get("src")
                if not src:
                    P["layer_src_missing"].append(nme)
                    continue
                if src.startswith("/") or "\\" in src or ".." in src.split("/") or re.match(r"^[A-Za-z]:", src):
                    P["src_path_unsafe"].append("%s (%r)" % (nme, src))
                    continue
                if src not in names:
                    P["layer_png_missing"].append("%s -> %s" % (nme, src))
                    continue
                try:
                    info = png_info(zf.read(src))
                except ValueError as e:
                    P["layer_png_invalid"].append("%s (%s): %s" % (nme, src, e))
                    continue
                n_ok_png += 1
                fmt_problems = []
                if info["bit_depth"] != 8:
                    fmt_problems.append("bit depth %d" % info["bit_depth"])
                if info["colour_type"] != 6:
                    fmt_problems.append("colour type %d (need 6, RGBA)" % info["colour_type"])
                if info["icc_name"] and "srgb" not in info["icc_name"].lower():
                    fmt_problems.append("embedded profile %r" % info["icc_name"])
                if fmt_problems:
                    P["layer_png_format"].append("%s (%s): %s" % (nme, src, ", ".join(fmt_problems)))
                if canvas:
                    x, y = whole(L.get("x", "0")) or 0, whole(L.get("y", "0")) or 0
                    if not (x >= 0 and y >= 0 and x + info["width"] <= canvas[0] and y + info["height"] <= canvas[1]):
                        P["layer_outside_canvas"].append("%s: %dx%d at (%d,%d) leaves the %dx%d canvas" % (
                            nme, info["width"], info["height"], x, y, canvas[0], canvas[1]))
            ok_name = {"layer_src_missing": "layer_src", "src_path_unsafe": "layer_src_safe", "layer_png_missing": "layer_png_present",
                       "layer_png_invalid": "layer_png_valid", "layer_png_format": "layer_png_8bit_rgba",
                       "layer_outside_canvas": "layer_inside_canvas"}
            for reason in ("layer_src_missing", "src_path_unsafe", "layer_png_missing", "layer_png_invalid", "layer_png_format",
                           "layer_outside_canvas"):
                soft = reason == "layer_outside_canvas" and allow_offcanvas
                rep.check(not P[reason], ok_name[reason], reason, "; ".join(P[reason][:6]),
                          "all %d layers" % len(layers) if layers else "", soft=soft)

            # -------- as-found layer
            if strict and layers:
                bottom = layers[-1].get("name")
                rep.check(bottom == "L00_asfound", "asfound_bottom", "asfound_not_bottom", "bottom layer is %r, not L00_asfound (W-27)" % bottom,
                          "L00_asfound is the bottom layer")

            # -------- merged image
            if "mergedimage.png" not in names:
                rep.fail("mergedimage_missing", "no mergedimage.png")
            else:
                try:
                    mi = png_info(zf.read("mergedimage.png"))
                    if canvas:
                        rep.check((mi["width"], mi["height"]) == canvas, "mergedimage_size_ok", "mergedimage_size",
                                  "mergedimage.png is %dx%d, canvas is %dx%d" % (mi["width"], mi["height"], canvas[0], canvas[1]),
                                  "mergedimage.png matches the canvas")
                except ValueError as e:
                    rep.fail("mergedimage_size", "mergedimage.png is not a well-formed PNG: %s" % e)

            # -------- members nobody references
            used = {L.get("src") for L in layers} | STANDARD_MEMBERS
            extra = [n for n in names if n not in used and not n.endswith("/")]
            if extra:
                rep.warn("unreferenced_member", "members not named by stack.xml: " + ", ".join(extra[:6]))
        else:
            rep.extra["profile"] = profile if profile != "auto" else "reference"
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check an OpenRaster file against the Life Journey hand-off rules (read-only).")
    ap.add_argument("ora")
    ap.add_argument("--profile", choices=["auto", "pipeline", "reference"], default="auto")
    ap.add_argument("--allow-offcanvas", action="store_true", help="a layer outside the canvas is a WARN (PhotoCraft reads off-canvas offsets)")
    ap.add_argument("--json", metavar="OUT.json")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if not os.path.isfile(a.ora):
        print("validate_ora: no such file: %s" % a.ora, file=sys.stderr)
        return 2
    try:
        rep = validate(a.ora, a.profile, a.allow_offcanvas)
    except Exception as e:      # noqa: BLE001 - a file shaped in a way no rule expects must be a named finding, not a traceback
        rep = Report("validate_ora", os.path.basename(a.ora))
        rep.fail("ora_structure_unexpected", "%s: %s (the file is shaped in a way the rules do not expect)" % (type(e).__name__, str(e)[:100]))
        return rep.finish(a.json)
    return rep.finish(a.json)


if __name__ == "__main__":
    sys.exit(main())
