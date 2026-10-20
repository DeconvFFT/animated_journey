"""sp1b_lib.py: shared helpers for the WP-10 drivers (standard library; Pillow only for the synthetic test cards).

WHAT IT IS. A thin layer over the WP-07 library (spikes/sp1_craft_cli/drivers/sp1_lib.py, REUSED, not copied): it points the evidence folder at
build/evidence/wp10, sets the package name WP-10, stamps every envelope with the label that this is a Linux CLI result, and builds the SYNTHETIC
hand-off inputs by calling the WP-06 emitters (pipeline/roundtrip). Nothing here opens a photograph; no family media exists or may be created.

HOW IT IS USED. The drivers add their own folder to sys.path from __file__ (python3 -I does not do it) and `import sp1b_lib as B`.
`python3 -I spikes/sp1b_readback/drivers/sp1b_lib.py --selftest` runs its small checks.

NEVER TOUCHES anything outside the folders a caller names and the evidence folder.
"""
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SP1B = os.path.realpath(os.path.join(HERE, ".."))
REPO = os.path.realpath(os.path.join(SP1B, "..", ".."))
os.environ.setdefault("LJ_SP1_EVIDENCE", os.path.join(REPO, "build", "evidence", "wp10"))
sys.path.insert(0, os.path.join(REPO, "spikes", "sp1_craft_cli", "drivers"))
import sp1_lib as L  # noqa: E402  (the WP-07 library, reused)

L.PACKAGE = "WP-10"
EVID = L.EVID
LABEL = "linux-cli"
LABEL_TEXT = "Linux CLI result; not evidence for Windows"
WIN_REASON = "Windows behaviour is not tested by a Linux CLI run (the maker's Windows five-minute test is the real evidence)"
RT = os.path.join(REPO, "pipeline", "roundtrip")
FIX = os.path.join(REPO, "research", "craft-visual-fixtures")

BAD_STDERR = [r"error while loading shared libraries", r"cannot open shared object", r"GLIBC_[0-9.]+' not found", r"panicked at",
              r"(?i)(error|fail|fatal|panic|unable|cannot)[^\n]*(\bgpu\b|adapter|vulkan|wgpu)", r"(?i)(\bgpu\b|adapter|vulkan|wgpu)[^\n]*(error|fail|fatal|panic|unable|cannot)"]
GPU_NOTICE = r"(?i)(\bgpu\b|adapter|vulkan|wgpu|software|cpu)"


def envelope(test, status, expected, actual, notes="", unverified_reasons=None, extra=None, disk=None):
    """lj-evidence/1 (build plan 4.2) plus the Linux-CLI label in the notes and in detail.label."""
    detail = {"label": LABEL, "label_text": LABEL_TEXT}
    detail.update(extra or {})
    n = (notes + " " if notes else "") + LABEL_TEXT + "."
    return L.envelope(test, status, expected, actual, notes=n, unverified_reasons=[WIN_REASON] + list(unverified_reasons or []), disk=disk, extra=detail)


class Checks:
    """A list of {id, pass, measured, note} with a printer; `problems` is what failed."""

    def __init__(self, prefix=""):
        self.rows, self.problems, self.prefix = [], [], prefix
        self.harness = []   # exceptions in THIS harness (a bug in the driver, not a verdict on the app); they make the envelope UNVERIFIED

    def add(self, cid, ok, measured, note=""):
        cid = self.prefix + cid
        self.rows.append({"id": cid, "pass": bool(ok), "measured": measured if isinstance(measured, (int, float, bool, list, dict)) else L.scrub(str(measured)), "note": note})
        if not ok:
            self.problems.append("%s: %s" % (cid, measured))
        print("  %s  %s  %s" % ("PASS" if ok else "FAIL", cid, str(measured)[:230]))

    def status(self):
        if self.harness:
            return "UNVERIFIED"
        return "PASS" if not self.problems else "FAIL"

    def section(self, label, fn, *args):
        """Run one section; an exception that is not a deliberate HarnessError is recorded and the other sections still run."""
        try:
            return fn(*args)
        except Exception as e:  # noqa: BLE001  (a driver bug must leave evidence, not a traceback)
            if type(e).__name__ == "HarnessError":
                raise
            msg = "%s: %s: %s" % (label, type(e).__name__, L.scrub(str(e))[:200])
            self.harness.append(msg)
            print("  HARNESS EXCEPTION  " + msg)
            return None


def run_py(args, timeout=300, cwd=None):
    """Run one of the repo's own tools under python3 -I and return (rc, stdout, stderr)."""
    p = subprocess.run([sys.executable, "-I"] + list(args), capture_output=True, text=True, timeout=timeout, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


# ----------------------------------------------------------------------------- synthetic inputs (WP-06 emitters, the reused fixtures)
def make_wp06_ora(path):
    rc, out, err = run_py([os.path.join(RT, "emit_ora_layers.py"), path])
    return rc == 0 and os.path.exists(path), (out + err).strip()


def make_wp06_rig(path):
    rc, out, err = run_py([os.path.join(RT, "svg_rig.py"), "gen", path])
    return rc == 0 and os.path.exists(path), (out + err).strip()


def make_test_jpeg(path, w=3000, h=2000, variant=0):
    """A synthetic scan-like test card: a smooth colour ramp, a grid, patches and the size in digits. Deterministic. Not a photograph."""
    from PIL import Image, ImageDraw
    # a smooth colour ramp built from one row of bytes (fast), then a grid, patches and the size in digits
    row = bytearray()
    for x in range(w):
        row += bytes((int(40 + 150 * x / w + 12 * variant) % 256, int(60 + 100 * x / w + 7 * variant) % 256, 90))
    data = bytearray()
    for y in range(h):
        b = int(60 + 90 * y / h)
        r2 = bytearray(row)
        r2[2::3] = bytes([b]) * w
        data += r2
    im = Image.frombytes("RGB", (w, h), bytes(data))
    d = ImageDraw.Draw(im)
    step = max(w // 20, 40)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=(30, 30, 30))
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(30, 30, 30))
    pw = w // 6
    for i, col in enumerate(((150, 60, 50), (60, 130, 70), (60, 80, 150), (170, 160, 80))):
        d.rectangle([i * pw + 20, h - pw - 20, i * pw + pw, h - 20], fill=col)
    d.text((w // 2, h // 2), "SYNTHETIC TEST CARD %d  %dx%d" % (variant, w, h), fill=(240, 240, 235), anchor="mm")
    im.save(path, "JPEG", quality=90)
    return os.path.exists(path)


def mean_luma(path):
    from PIL import Image
    im = Image.open(path).convert("L")
    h = im.histogram()
    tot = sum(h)
    return sum(i * c for i, c in enumerate(h)) / float(tot)


def image_size(path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def ora_expected(path):
    """(canvas (w, h), layer names top-first) from a .ora's stack.xml, read with the standard library only."""
    import zipfile
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("stack.xml"))
    names = [e.get("name") for e in root.iter("layer")]
    return (int(root.get("w")), int(root.get("h"))), names


def json_names(obj):
    """Every value of a "name" key in a JSON value, depth first (a layer tree whatever its exact shape)."""
    out = []
    for d in L.walk(obj):
        v = d.get("name")
        if isinstance(v, str):
            out.append(v)
    return out


def layer_names(obj):
    """Layer names from a PhotoCraft `info` document: the "layers" lists (recursively) when there are some, else every "name"."""
    out = []

    def rec(lst):
        for e in lst:
            if isinstance(e, dict):
                if isinstance(e.get("name"), str):
                    out.append(e["name"])
                for k in ("children", "layers"):
                    if isinstance(e.get(k), list):
                        rec(e[k])
    found = False
    for d in L.walk(obj):
        if isinstance(d.get("layers"), list) and d["layers"] and all(isinstance(x, dict) for x in d["layers"]):
            rec(d["layers"])
            found = True
            break
    return out if found else json_names(obj)


def needed_libs(path):
    try:
        p = subprocess.run(["readelf", "-d", path], capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    libs = re.findall(r"\(NEEDED\)\s+Shared library: \[([^\]]+)\]", p.stdout)
    return sorted(libs) if p.returncode == 0 else None


def excerpt(text, n=1200):
    t = L.scrub(text or "").strip()
    return t[:n]


def _selftest():
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok = ok and cond
    check("package is WP-10", L.PACKAGE == "WP-10")
    check("evidence folder is wp10", EVID.replace(os.sep, "/").endswith("build/evidence/wp10") or "LJ_SP1_EVIDENCE" in os.environ)
    check("json_names walks nested dicts", json_names({"a": {"name": "x", "k": [{"name": "y"}]}}) == ["x", "y"])
    check("layer_names uses the layers list", layer_names({"name": "doc", "layers": [{"name": "A"}, {"name": "B", "children": [{"name": "C"}]}]}) == ["A", "B", "C"])
    check("layer_names falls back to every name", layer_names({"name": "doc", "x": {"name": "Q"}}) == ["doc", "Q"])
    with tempfile.TemporaryDirectory() as d:
        j = os.path.join(d, "t.jpg")
        check("make_test_jpeg writes a JPEG", make_test_jpeg(j, 300, 200) and image_size(j) == (300, 200) and open(j, "rb").read(2) == b"\xff\xd8")
        o = os.path.join(d, "t.ora")
        okk, msg = make_wp06_ora(o)
        check("make_wp06_ora writes the WP-06 layered still", okk and ora_expected(o)[1][0] == "L30_label" and ora_expected(o)[1][-1] == "L00_asfound")
        s = os.path.join(d, "t.svg")
        okk, msg = make_wp06_rig(s)
        check("make_wp06_rig writes the WP-06 rig", okk and "disc-a" in open(s).read())
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
