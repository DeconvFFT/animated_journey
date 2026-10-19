#!/usr/bin/env python3
"""svg_rig.py: a SYNTHETIC SVG rig for the VectorCraft hand-off tests, planted defects for it, and the gate around the reused check_ids.py (WP-06).

  python3 -I pipeline/roundtrip/svg_rig.py gen OUT.svg
  python3 -I pipeline/roundtrip/svg_rig.py plant ids_stripped|kind_changed|pivot_dropped IN.svg OUT.svg
  python3 -I pipeline/roundtrip/svg_rig.py gate RIG.svg TOUCHED.svg [--check-ids PATH] [--label NAME]
  python3 -I pipeline/roundtrip/svg_rig.py finding RIG.svg PLAIN.svg [--extra LABEL=FILE ...] [--inkscape-version TEXT] [--json OUT.json]

gen      writes a style-neutral geometric rig (discs, a bar, an arm, dots, two <use> ticks, one text): unique clean ids on every element that
         moves, data-pivot and data-z on groups (and a few other elements, to probe where a tool drops them), a viewBox that starts at
         0 0 640 360, and NO class, <style>, transform on groups, filters or animation (research/craft-visual.md rig rules).
plant    damages a copy the way a touching tool could:
           ids_stripped   removes every id that nothing references (what default svgo cleanupIds does)
           kind_changed   circle disc-a becomes an ellipse with the same id and data-* (a tool that converts shapes)
           pivot_dropped  removes data-pivot everywhere
gate     runs research/craft-visual-fixtures/check_ids.py UNCHANGED (python3 -I) and turns its output into named reasons:
           ids_lost, data_attr_changed (from its exit code 1), and element_kind_changed.
         WHY THE EXTRA REASON: check_ids.py prints "element kind changed" but its exit code ignores it (it exits 1 only for lost ids or changed
         data-*), so a pure kind change exits 0 there. The gate exits 1 for it too. Both numbers are printed: raw_exit and gate_exit.
finding  records, as JSON, what happened to every data-* attribute, every authored id, the viewBox and the namespaces between the rig and a
         tool's output (the Inkscape finding, WP-06).

EXIT CODES (build plan 4.3)  gen/plant/finding: 0 ok, 2 bad usage or unreadable input   gate: 0 passes, 1 the touched file lost something,
2 bad usage, 3 check_ids.py missing or unparseable output
It reads the files you name and writes only OUT. It never touches the network.
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
NS = {"": SVG, "xlink": XLINK, "inkscape": "http://www.inkscape.org/namespaces/inkscape",
      "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd", "svg": SVG}
DEF_KINDS = ("linearGradient", "radialGradient", "clipPath", "mask", "filter", "symbol", "stop")   # check_ids.py skips these
HERE = os.path.dirname(os.path.abspath(__file__))
CHECK_IDS_DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "research", "craft-visual-fixtures", "check_ids.py"))

RIG = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 640 360" width="640" height="360">
  <defs>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="1" y2="1" data-note="def-probe">
      <stop offset="0" stop-color="#1f3a5f"/><stop offset="1" stop-color="#e8d8a8"/>
    </linearGradient>
    <symbol id="tick" viewBox="0 0 10 10"><rect x="4" y="0" width="2" height="10" fill="#222222"/></symbol>
  </defs>
  <g id="scene" data-z="0">
    <rect id="bg" x="0" y="0" width="640" height="360" fill="url(#bg-grad)"/>
    <g id="orbit" data-pivot="320,180" data-z="2">
      <circle id="disc-a" cx="320" cy="90" r="30" fill="#c0392b" data-role="body"/>
      <circle id="disc-b" cx="420" cy="180" r="20" fill="#2e86c1" data-role="satellite"/>
      <rect id="bar" x="318" y="90" width="4" height="90" fill="#333333" data-pivot="320, 90"/>
    </g>
    <g id="arm" data-pivot="120,300" data-z="3">
      <rect id="arm-upper" x="110" y="220" width="20" height="80" rx="6" fill="#555555"/>
      <path id="arm-lower" d="M110 220 L130 220 L170 160 L150 150 Z" fill="#777777" data-pivot="120.50,220.0"/>
      <ellipse id="hand" cx="160" cy="155" rx="14" ry="10" fill="#999999" data-z="1"/>
    </g>
    <g id="dots" data-pivot="500,300" data-z="4">
      <circle id="dot-1" cx="480" cy="300" r="8" fill="#27ae60"/>
      <circle id="dot-2" cx="500" cy="300" r="8" fill="#f1c40f"/>
      <circle id="dot-3" cx="520" cy="300" r="8" fill="#8e44ad"/>
    </g>
    <g data-role="wrapper-without-id">
      <use id="tick-1" xlink:href="#tick" x="560" y="40" width="10" height="10" data-z="5"/>
      <use id="tick-2" xlink:href="#tick" x="580" y="40" width="10" height="10" data-z="5"/>
    </g>
    <text id="label" x="24" y="340" font-family="sans-serif" font-size="20" fill="#ffffff" data-z="6" data-pivot="24,340">TEST 24</text>
  </g>
</svg>
"""


def _register():
    for p, u in NS.items():
        try:
            ET.register_namespace(p, u)
        except ValueError:
            pass


def local(tag):
    return tag.split("}")[-1]


def parse(path):
    _register()
    try:
        return ET.parse(path).getroot()
    except (ET.ParseError, OSError) as e:
        raise SystemExit("svg_rig: cannot read %s: %s" % (os.path.basename(path), e))


def write(root, path):
    _register()
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


# ---------------------------------------------------------------------------------------------------------------- plant
def referenced_ids(root):
    """Ids that something refers to: url(#id), href="#id" (plain or xlink), or #id in a <style>."""
    refs = set()
    for e in root.iter():
        for k, v in e.attrib.items():
            for m in re.finditer(r"url\(#([^)]+)\)", v):
                refs.add(m.group(1))
            if local(k) == "href" and v.startswith("#"):
                refs.add(v[1:])
        if local(e.tag) == "style" and e.text:
            for m in re.finditer(r"#([A-Za-z][\w.-]*)", e.text):
                refs.add(m.group(1))
    return refs


def plant(kind, src, dst):
    root = parse(src)
    if kind == "ids_stripped":
        keep = referenced_ids(root)
        n = 0
        for e in root.iter():
            i = e.get("id")
            if i and i not in keep:
                del e.attrib["id"]
                n += 1
        note = "removed %d unreferenced ids, kept %s" % (n, sorted(keep))
    elif kind == "kind_changed":
        hit = None
        for e in root.iter():
            if local(e.tag) == "circle" and e.get("id") == "disc-a":
                r = e.attrib.pop("r")
                e.tag = "{%s}ellipse" % SVG
                e.set("rx", r)
                e.set("ry", r)
                hit = e
        if hit is None:
            raise SystemExit("svg_rig: no circle with id disc-a in %s (is this the rig?)" % os.path.basename(src))
        note = "circle disc-a became an ellipse (same id, same data-*)"
    elif kind == "pivot_dropped":
        n = 0
        for e in root.iter():
            if "data-pivot" in e.attrib:
                del e.attrib["data-pivot"]
                n += 1
        note = "removed data-pivot from %d elements" % n
    else:
        raise SystemExit("svg_rig: unknown defect %r" % kind)
    write(root, dst)
    print("planted %s: %s" % (kind, note))
    return 0


# ---------------------------------------------------------------------------------------------------------------- gate
SUMMARY = re.compile(r"ids authored: (\d+) \| lost: (.*?) \| element kind changed: (.*?) \| data-\* changed: (.*)$")


def _lst(txt):
    txt = txt.strip()
    return [] if txt == "none" else list(ast.literal_eval(txt))


def gate(rig, touched, check_ids, label):
    if not os.path.isfile(check_ids):
        print("svg_rig gate: check_ids.py not found at the expected place", file=sys.stderr)
        return 3
    p = subprocess.run([sys.executable, "-I", "-B", check_ids, rig, touched], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=60)
    out = p.stdout.decode("utf-8", "replace")
    m = None
    for line in out.splitlines():
        m = SUMMARY.search(line) or m
    if p.returncode not in (0, 1) or not m:
        print("svg_rig gate: check_ids.py exit %d and no summary line; stderr: %s" % (p.returncode, p.stderr.decode("utf-8", "replace")[-200:]), file=sys.stderr)
        return 3
    authored, lost, kind, data = int(m.group(1)), _lst(m.group(2)), _lst(m.group(3)), _lst(m.group(4))
    reasons = []
    if lost:
        reasons.append("ids_lost")
    if data:
        reasons.append("data_attr_changed")
    if kind:
        reasons.append("element_kind_changed")
    gexit = 1 if reasons else 0
    print("GATE %s: raw_exit=%d gate_exit=%d authored=%d lost=%s kind_changed=%s data_changed=%s reasons=%s" % (
        label or "-", p.returncode, gexit, authored, ",".join(lost) or "none", ",".join(kind) or "none", ",".join(data) or "none",
        ",".join(reasons) or "none"))
    return gexit


# ---------------------------------------------------------------------------------------------------------------- finding
def _sig(e):
    d = sorted((k, v) for k, v in e.attrib.items() if k.startswith("data-"))
    return (local(e.tag), d[0][0], d[0][1]) if d else None


def compare(rig_root, out_root):
    """Match every data-* carrying element of the rig to the tool's output: by id when it has one, else by (tag, first data-* pair)."""
    out_by_id = {e.get("id"): e for e in out_root.iter() if e.get("id")}
    out_by_sig = {}
    for e in out_root.iter():
        if _sig(e):
            out_by_sig.setdefault(_sig(e), e)
    rows, kept, changed, dropped = [], 0, [], []
    by_kind = {}
    for e in rig_root.iter():
        attrs = {k: v for k, v in e.attrib.items() if k.startswith("data-")}
        if not attrs:
            continue
        key = ("#" + e.get("id")) if e.get("id") else "%s[%s=%s]" % _sig(e)
        match = out_by_id.get(e.get("id")) if e.get("id") else out_by_sig.get(_sig(e))
        got_attrs = {k: v for k, v in (match.attrib.items() if match is not None else []) if k.startswith("data-")}
        for k, v in sorted(attrs.items()):
            got = got_attrs.get(k)
            state = "kept" if got == v else ("changed" if got is not None else "dropped")
            rows.append({"element": key, "tag": local(e.tag), "attr": k, "in": v, "out": got, "state": state})
            bk = by_kind.setdefault(local(e.tag), {"total": 0, "kept": 0})
            bk["total"] += 1
            if state == "kept":
                kept += 1
                bk["kept"] += 1
            elif state == "changed":
                changed.append("%s %s: %r -> %r" % (key, k, v, got))
            else:
                dropped.append("%s %s" % (key, k))
    ids_in = {e.get("id"): local(e.tag) for e in rig_root.iter() if e.get("id")}
    ids_out = {e.get("id"): local(e.tag) for e in out_root.iter() if e.get("id")}
    authored = [i for i, t in ids_in.items() if t not in DEF_KINDS]
    added = sorted(i for i in ids_out if i not in ids_in)
    ns_out = sorted({e.tag.split("}")[0][1:] for e in out_root.iter() if e.tag.startswith("{")} |
                    {k.split("}")[0][1:] for e in out_root.iter() for k in e.attrib if k.startswith("{")})
    transforms = sorted((e.get("id") or local(e.tag)) for e in out_root.iter() if e.get("transform"))   # the rig has none
    return {"data_attributes": {"total": len(rows), "kept_verbatim": kept, "changed": changed, "dropped": dropped, "by_element_kind": by_kind,
                                "detail": rows},
            "ids": {"authored": len(authored), "survived": sum(1 for i in authored if i in ids_out and ids_out[i] == ids_in[i]),
                    "lost": sorted(i for i in authored if i not in ids_out), "kind_changed": sorted(i for i in authored if i in ids_out and ids_out[i] != ids_in[i]),
                    "added_by_tool": len(added), "added_examples": added[:8]},
            "viewBox": {"in": rig_root.get("viewBox"), "out": out_root.get("viewBox")},
            "size": {"in": [rig_root.get("width"), rig_root.get("height")], "out": [out_root.get("width"), out_root.get("height")]},
            "namespaces_in_output": ns_out,
            "inkscape_or_sodipodi_attributes": sum(1 for e in out_root.iter() for k in e.attrib if k.startswith("{http://www.inkscape.org") or k.startswith("{http://sodipodi")),
            "transform_added_to": transforms,
            "has_class_or_style": bool(any(e.get("class") or local(e.tag) == "style" for e in out_root.iter()))}


def finding(rig, plain, extras, version, json_path):
    """extras: list of 'label=path' strings (more tool outputs to compare, for example a touched-up copy)."""
    rr = parse(rig)
    doc = {"schema": "lj-svg-finding/1", "tool": "Inkscape", "version": version or "unknown",
           "question": "What does Inkscape do to data-* attributes (and ids, viewBox) on a clean pass-through of the synthetic rig?",
           "plain_svg": compare(rr, parse(plain)), "extra": {}}
    for item in extras or []:
        label, _, path = item.partition("=")
        if not path:
            raise SystemExit("svg_rig: --extra wants LABEL=FILE, got %r" % item)
        doc["extra"][label] = compare(rr, parse(path))
    pd = doc["plain_svg"]["data_attributes"]
    doc["summary"] = ("Inkscape plain-SVG export kept %d of %d data-* attributes verbatim (changed %d, dropped %d) and %d of %d authored ids; "
                      "it added %d ids of its own to elements that had none." % (pd["kept_verbatim"], pd["total"], len(pd["changed"]), len(pd["dropped"]),
                                                                              doc["plain_svg"]["ids"]["survived"], doc["plain_svg"]["ids"]["authored"],
                                                                              doc["plain_svg"]["ids"]["added_by_tool"]))
    print(doc["summary"])
    for label, c in doc["extra"].items():
        d = c["data_attributes"]
        print("  %s: data-* kept %d of %d (changed %d, dropped %d), ids %d of %d, transform added to %s" % (
            label, d["kept_verbatim"], d["total"], len(d["changed"]), len(d["dropped"]), c["ids"]["survived"], c["ids"]["authored"],
            ",".join(c["transform_added_to"]) or "nothing"))
    if json_path:
        os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
        with open(json_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=2, sort_keys=True)
            f.write("\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Synthetic SVG rig, planted defects and the gate around check_ids.py.")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("gen")
    g.add_argument("out")
    p = sub.add_parser("plant")
    p.add_argument("kind", choices=["ids_stripped", "kind_changed", "pivot_dropped"])
    p.add_argument("src")
    p.add_argument("dst")
    t = sub.add_parser("gate")
    t.add_argument("rig")
    t.add_argument("touched")
    t.add_argument("--check-ids", default=CHECK_IDS_DEFAULT)
    t.add_argument("--label", default="")
    f = sub.add_parser("finding")
    f.add_argument("rig")
    f.add_argument("plain")
    f.add_argument("--extra", action="append", metavar="LABEL=FILE", help="another tool output to compare (repeatable)")
    f.add_argument("--inkscape-version")
    f.add_argument("--json")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        if a.cmd == "gen":
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(RIG)
            print("wrote %s" % os.path.basename(a.out))
            return 0
        if a.cmd == "plant":
            return plant(a.kind, a.src, a.dst)
        if a.cmd == "gate":
            return gate(a.rig, a.touched, a.check_ids, a.label)
        if a.cmd == "finding":
            return finding(a.rig, a.plain, a.extra, a.inkscape_version, a.json)
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            return 2
        raise
    return 2


if __name__ == "__main__":
    sys.exit(main())
