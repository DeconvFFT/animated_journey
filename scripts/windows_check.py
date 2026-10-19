#!/usr/bin/env python3
"""windows_check.py: validate a pasted PC inventory report and print the hardware tier table.

WHAT IT DOES
  Reads one pc_report.json (written by win/step0_pc_tests.ps1 on the maker's PC and pasted in chat),
  decides whether it is valid, scans it for identifying data with the SAME pattern file every other
  scanner uses (scripts/redaction_patterns.json), and prints a tier table that the playbooks key on.
  Standard library only. Run it as:   python3 -I scripts/windows_check.py REPORT.json
  (on the PC:                         py -3 -I scripts\\windows_check.py REPORT.json)

WHAT IT NEVER DOES
  It never prints a flagged value in full (first two characters plus asterisks), never writes anything
  unless an output option is given, never writes after an identifying-data finding (exit 2), and never
  stores a user, computer or domain name. It does not touch the network.

USAGE
  windows_check.py [--forbid WORD ...] [--json-out PATH] [--tier-json-out PATH] [--hardware-md PATH] REPORT|-
                       (REPORT of - reads standard input, so a pasted raw report never needs to be written to a file)
  windows_check.py --pattern-self-test SAMPLES.json     (pattern check only; no report needed)

  --forbid WORD        also refuse WORD (a name). For container-side tests with INVENTED names only:
                       on the maker's PC put real names in the git-ignored scripts/public_lint.deny.local.txt
                       (one word per line) so no name is ever typed into a shell history.
  --json-out PATH      the printed table as JSON. For chat or scratch use; it carries exact sizes.
  --tier-json-out PATH the DERIVED tier file (schema win/schema/pc_tier.schema.json): buckets and verdict
                       words only. This is the only form of PC data that may be filed in the repository.
  --hardware-md PATH   a bucketed draft of decisions/hardware.md (no model names).

EXIT CODES (build plan 4.3)
  0  the report is valid and nothing needs a human (a low tier is information, not a failure)
  1  valid, but a finding needs a human: VRAM unreadable, ffmpeg or Python missing, ffmpeg without
     libx264 or libass, a Craft pin mismatch, or not a Windows report
  2  invalid input, identifying data found, or the pattern file is missing or invalid (fail closed)
  3  environment problem (this tool's own data files are missing)

Windows behaviour behind the report fields is UNVERIFIED until the maker's first real report.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS_PATH = HERE / "redaction_patterns.json"
WIN_DIR = HERE.parent / "win"
DENY_LOCAL_DEFAULT = "public_lint.deny.local.txt"

REQUIRED_CATEGORY_IDS = ("email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux",
                         "token_shape", "guid_serial", "handle")
HARDWARE_NAME_FIELDS_FALLBACK = ("cpu.name", "gpus[].name", "gpus[].vendor", "os.caption")


class FailClosed(Exception):
    """The pattern file is missing or unusable: nothing may be accepted or written."""


class EnvProblem(Exception):
    """One of this tool's own data files is missing or unreadable (exit 3)."""


# ----------------------------------------------------------------------------- pattern file (4.13)
def _join(sample):
    if isinstance(sample, dict):
        if "parts" in sample:
            return "".join(str(x) for x in sample["parts"])
        return str(sample.get("text", sample.get("value", "")))
    return "".join(sample) if isinstance(sample, list) else str(sample)


def _flags(s):
    f = 0
    if s and "i" in s:
        f |= re.IGNORECASE
    return f


def _as_list(v):
    if v is None:
        return []
    return list(v) if isinstance(v, (list, tuple)) else [v]


class Patterns:
    def __init__(self, data, path):
        self.path = path
        self.data = data
        self.version = data.get("version")
        self.categories = []
        for c in data["categories"]:
            self.categories.append({
                "id": c["id"], "scope": c.get("scope", "both"),
                "rx": re.compile(c["regex"], _flags(c.get("flags", ""))),
                "positive": [_join(s) for s in _as_list(c.get("positive_samples"))],
                "negative": [_join(s) for s in _as_list(c.get("negative_samples"))],
            })
        self.exemptions = []
        for e in _as_list(data.get("exemptions")):
            cats = _as_list(e.get("category") or e.get("categories") or e.get("applies_to") or e.get("category_id"))
            self.exemptions.append({"id": e.get("id", ""), "cats": cats or None,
                                    "rx": re.compile(e["regex"], _flags(e.get("flags", "")))})
        self.field_exemptions = []
        for fe in _as_list(data.get("field_exemptions")):
            cats = _as_list(fe.get("category") or fe.get("categories") or fe.get("id") or fe.get("applies_to"))
            fields = _as_list(fe.get("fields") or fe.get("field") or fe.get("paths") or fe.get("path"))
            if not cats or not fields:
                raise FailClosed("a field_exemptions entry has no category or no fields")
            self.field_exemptions.append({"cats": cats, "fields": [norm_spec(f) for f in fields]})
        nc = data.get("name_checks") or {}
        self.min_name_len = int(nc.get("min_name_len", 3))
        self.fragment_len = int(nc.get("fragment_len", 4))
        self.fragment_min_name_len = int(nc.get("fragment_min_name_len", 5))
        self.hardware_fields = [norm_spec(f) for f in _as_list(nc.get("hardware_name_fields")) or HARDWARE_NAME_FIELDS_FALLBACK]
        self.hardware_action = nc.get("hardware_field_action", "report")
        mk = data.get("mask") or {}
        self.mask_keep = int(mk.get("keep", 2))
        self.mask_fill = str(mk.get("fill", "*")) or "*"
        self.mask_cap = int(mk.get("cap", 8))
        self.placeholders = [str(x) for x in _as_list(data.get("placeholders"))]
        ld = data.get("local_deny")
        if isinstance(ld, dict):
            ld = ld.get("path") or ld.get("file")
        self.local_deny_name = Path(str(ld)).name if ld else DENY_LOCAL_DEFAULT

    def report_categories(self):
        return [c for c in self.categories if c["scope"] in ("report", "both")]


def load_patterns(path=PATTERNS_PATH):
    p = Path(path)
    if not p.is_file():
        raise FailClosed("the pattern file scripts/redaction_patterns.json is missing (download the WHOLE project folder, not single files)")
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        raise FailClosed("the pattern file scripts/redaction_patterns.json does not parse as JSON")
    if not isinstance(data, dict) or not isinstance(data.get("categories"), list) or not data["categories"]:
        raise FailClosed("the pattern file has no categories")
    ids = {c.get("id") for c in data["categories"] if isinstance(c, dict)}
    missing = [i for i in REQUIRED_CATEGORY_IDS if i not in ids]
    if missing:
        raise FailClosed("the pattern file lacks required categories: " + ", ".join(missing))
    try:
        return Patterns(data, p)
    except FailClosed:
        raise
    except (KeyError, TypeError, ValueError, re.error) as e:
        raise FailClosed("the pattern file is not valid (%s)" % type(e).__name__)


# ----------------------------------------------------------------------------- field paths and masking
def norm_spec(spec):
    """gpus[].name, gpus[*].name and gpus[0].name all become gpus[].name."""
    return re.sub(r"\[[^\]]*\]", "[]", str(spec))


def norm_path(path):
    return re.sub(r"\[[0-9]+\]", "[]", path)


def spec_regex(spec):
    """A field spec becomes an anchored regex: [] marks any array index, * matches any run of characters."""
    return re.compile("^" + re.escape(norm_spec(spec)).replace(r"\*", ".*") + "$")


def field_matches(spec, path):
    return bool(spec_regex(spec).match(norm_path(path)))


def mask(value, keep=2, fill="*", cap=8):
    value = str(value)
    if len(value) <= keep:
        return fill * max(1, len(value))
    return value[:keep] + fill * min(len(value) - keep, cap)


def safe_key(k):
    k = str(k)
    return k if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,31}", k) else "<key>"


def walk_strings(obj, path=""):
    """Yield (path, string) for every string leaf. Keys are never searched."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, (path + "." if path else "") + safe_key(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, "%s[%d]" % (path, i))


# ----------------------------------------------------------------------------- the scan
def category_hits(pat, path, text):
    """Pattern-category hits on one string: list of (category_id, matched_text)."""
    hits = []
    for c in pat.report_categories():
        for m in c["rx"].finditer(text):
            if any(c["id"] in fe["cats"] and any(field_matches(f, path) for f in fe["fields"]) for fe in pat.field_exemptions):
                continue
            if m.group(0) in pat.placeholders:
                continue  # a documented placeholder from the pattern file is not a leak
            span = m.span()
            exempt = False
            for ex in pat.exemptions:
                if ex["cats"] is not None and c["id"] not in ex["cats"]:
                    continue
                if any(es[0] <= span[0] and span[1] <= es[1] for es in (mm.span() for mm in ex["rx"].finditer(text))):
                    exempt = True
                    break
            if not exempt:
                hits.append((c["id"], m.group(0)))
    return hits


def name_hit(text, name, allow_fragments, pat):
    """Whole-name (case-insensitive, whole word) or 4-character-fragment hit. Returns the matched text or None."""
    low = text.lower()
    nl = name.lower()
    if re.search(r"(?<![a-z0-9])" + re.escape(nl) + r"(?![a-z0-9])", low):
        return name
    if allow_fragments and len(name) >= pat.fragment_min_name_len:
        n = pat.fragment_len
        for i in range(len(name) - n + 1):
            frag = nl[i:i + n]
            if frag in low:
                return name[i:i + n]
    return None


def scan_report(pat, report, names):
    """names: list of (category, value, allow_fragments). Returns (refusals, notes, skipped)."""
    refusals, notes, skipped = [], [], []
    seen = set()
    usable = []
    for cat, val, frag in names:
        if len(val) < pat.min_name_len:
            skipped.append((cat, len(val)))
        else:
            usable.append((cat, val, frag))
    for path, text in walk_strings(report):
        for cid, matched in category_hits(pat, path, text):
            key = (cid, path, matched)
            if key not in seen:
                seen.add(key)
                refusals.append((cid, path, mask(matched, pat.mask_keep, pat.mask_fill, pat.mask_cap)))
        if path.startswith("redaction.name_hits_in_hardware_fields"):
            continue  # our own masked bookkeeping: category ids, field paths, two-letter hits
        for cat, val, frag in usable:
            matched = name_hit(text, val, frag, pat)
            if matched is None:
                continue
            key = (cat, path)
            if key in seen:
                continue
            seen.add(key)
            hit = (cat, path, mask(matched, pat.mask_keep, pat.mask_fill, pat.mask_cap))
            if pat.hardware_action == "report" and any(field_matches(f, path) for f in pat.hardware_fields):
                notes.append(hit)
            else:
                refusals.append(hit)
    return refusals, notes, skipped


def read_local_deny(pat):
    """The optional git-ignored scripts/public_lint.deny.local.txt: one word per line, written in Notepad
    (UTF-8, UTF-8 with BOM, UTF-16 or Windows-1252). Never printed; used only for the name check."""
    p = HERE / pat.local_deny_name
    words = []
    try:
        if p.is_file():
            raw = p.read_bytes()
            try:
                text, _enc = decode_bytes(raw)
            except UnicodeError:
                text = raw.decode("cp1252", errors="replace")
            for line in text.splitlines():
                w = line.strip()
                if w and not w.startswith("#"):
                    words.append(w)
    except OSError:
        pass
    return words


# ----------------------------------------------------------------------------- reading the report
def decode_bytes(raw):
    """UTF-8, UTF-8 with BOM, UTF-16 (with or without BOM). Returns (text, label)."""
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8"), "UTF-8 with BOM"
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16"), "UTF-16 with BOM"
    if len(raw) >= 4 and raw[1:2] == b"\x00" and raw[3:4] == b"\x00":
        return raw.decode("utf-16-le"), "UTF-16 LE (no BOM)"
    if len(raw) >= 4 and raw[0:1] == b"\x00" and raw[2:3] == b"\x00":
        return raw.decode("utf-16-be"), "UTF-16 BE (no BOM)"
    return raw.decode("utf-8"), "UTF-8"


# ----------------------------------------------------------------------------- mini JSON Schema validator
def _jtype(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "integer" if v.is_integer() else "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    if isinstance(v, dict):
        return "object"
    return "other"


def _type_ok(v, want):
    t = _jtype(v)
    return t == want or (want == "number" and t == "integer")


def _resolve(root, ref):
    node = root
    for part in ref.lstrip("#/").split("/"):
        if part:
            node = node[part]
    return node


def validate(inst, schema, root, path, errs):
    if "$ref" in schema:
        schema = _resolve(root, schema["$ref"])
    if "const" in schema:
        if _jtype(inst) != _jtype(schema["const"]) or inst != schema["const"]:
            errs.append((path, "must equal the fixed value"))
            return
    want = schema.get("type")
    if want is not None:
        wants = want if isinstance(want, list) else [want]
        if not any(_type_ok(inst, w) for w in wants):
            errs.append((path, "has the wrong type (found %s, expected %s)" % (_jtype(inst), "/".join(wants))))
            return
    if "enum" in schema and inst not in schema["enum"]:
        errs.append((path, "is not one of the allowed values"))
    if isinstance(inst, str):
        if "maxLength" in schema and len(inst) > schema["maxLength"]:
            errs.append((path, "is longer than %d characters" % schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            errs.append((path, "does not match the required form"))
    if isinstance(inst, (int, float)) and not isinstance(inst, bool):
        if "minimum" in schema and inst < schema["minimum"]:
            errs.append((path, "is below the minimum"))
        if "maximum" in schema and inst > schema["maximum"]:
            errs.append((path, "is above the maximum"))
    if isinstance(inst, list):
        if "maxItems" in schema and len(inst) > schema["maxItems"]:
            errs.append((path, "has too many items"))
        if "items" in schema:
            for i, v in enumerate(inst):
                validate(v, schema["items"], root, "%s[%d]" % (path, i), errs)
    if isinstance(inst, dict):
        props = schema.get("properties", {})
        for r in schema.get("required", []):
            if r not in inst:
                errs.append(((path + "." if path else "") + r, "is missing"))
        for k, v in inst.items():
            sub = (path + "." if path else "") + (k if k in props else "<unknown key>")
            if k in props:
                validate(v, props[k], root, sub, errs)
            elif schema.get("additionalProperties") is False:
                errs.append((sub, "is not part of the report format"))


# ----------------------------------------------------------------------------- tiers
def load_json_file(path, what):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        raise EnvProblem("%s is missing or unreadable" % what)


def vkey(v):
    m = re.match(r"^\s*v?(\d+)\.(\d+)(?:\.(\d+))?", str(v or ""))
    return tuple(int(x) if x is not None else 0 for x in m.groups()) if m else None


def vendor_family(vendor, name):
    s = ("%s %s" % (vendor or "", name or "")).lower()
    if "nvidia" in s:
        return "NVIDIA"
    if "amd" in s or "advanced micro" in s or "radeon" in s or re.search(r"\bati\b", s):
        return "AMD"
    if "intel" in s:
        return "Intel"
    return "other"


def is_software_gpu(g, tiers):
    if g.get("is_software"):
        return True
    n = (g.get("name") or "").lower()
    return any(p.lower() in n for p in tiers["gpu"]["software_name_patterns"])


def tier_by_min(value, tier_list, key):
    for t in tier_list:
        if value >= t[key]:
            return t["id"]
    return tier_list[-1]["id"]


def vram_bucket(v, tiers):
    vb = tiers["vram_buckets"]
    x = v + vb["tolerance_gb"]
    label = vb["labels"][0]
    for edge, lab in zip(vb["edges_gb"], vb["labels"][1:]):
        if x >= edge:
            label = lab
    return label


def assess(report, tiers, pins):
    """Everything the table and the tier file need. No names, only verdicts and numbers."""
    r = {"findings": [], "info": []}
    osr = report["os"]
    r["windows_report"] = osr["platform"] == "windows"
    if not r["windows_report"]:
        r["findings"].append("NOT A WINDOWS REPORT: os.platform is %s. A report made on Linux or macOS (a test run) says nothing about the maker's PC." % osr["platform"])
        return r

    # --- edition
    eid = osr.get("edition_id") or ""
    ed = tiers["edition"]
    if any(eid.startswith(p) for p in ed["home_prefixes"]):
        fam = "home"
    elif any(eid.startswith(p) for p in ed["pro_or_higher_prefixes"]):
        fam = "pro-or-higher"
    else:
        fam = "unknown"
    r["edition_family"] = fam
    r["edition_id"] = eid or "unknown"
    try:
        r["build_major"] = int(str(osr.get("build") or "").split(".")[0])
    except ValueError:
        r["build_major"] = None

    # --- GPU
    real, vendor_best, readable = [], None, []
    unreadable = 0
    for g in report["gpus"]:
        if is_software_gpu(g, tiers):
            continue
        real.append(g)
        trusted = g["vram_source"] in tiers["gpu"]["vram_sources_trusted"] or g["vram_source"] == "adapterram"
        if g["vram_gb"] is not None and trusted:
            fam_g = vendor_family(g.get("vendor"), g.get("name"))
            tid = tier_by_min(g["vram_gb"], tiers["gpu"]["tiers"], "min_vram_gb")
            cap = tiers["gpu"].get("non_nvidia_max_tier")
            capped_note = None
            if cap and fam_g != "NVIDIA":
                order = [t["id"] for t in tiers["gpu"]["tiers"]]
                if order.index(tid) < order.index(cap):  # list is best-first, so a smaller index is a higher tier
                    tid, capped_note = cap, "non-NVIDIA card: capped at %s until a test says otherwise" % cap
            readable.append((g["vram_gb"], tid, fam_g, g["vram_source"], capped_note))
        else:
            unreadable += 1
    r["gpu_real_count"] = len(real)
    if not real:
        r["gpu_tier"], r["vram_bucket"] = "none", "none"
        r["gpu_detail"] = "no graphics device other than a software one (CPU-only path; cloud steps only where Decision 6 allows)"
    elif readable:
        order = [t["id"] for t in tiers["gpu"]["tiers"]]
        best = min(readable, key=lambda x: order.index(x[1]))
        r["gpu_tier"] = best[1]
        r["vram_bucket"] = vram_bucket(max(x[0] for x in readable), tiers)
        r["gpu_detail"] = "%s, %.1f GB read from %s%s" % (best[2], best[0], best[3], ("; " + best[4]) if best[4] else "")
        r["vram_gb"] = best[0]
        r["vram_source"] = best[3]
        if unreadable:
            r["info"].append("%d other graphics device(s) have unreadable VRAM; the tier uses the readable one" % unreadable)
    else:
        r["gpu_tier"], r["vram_bucket"] = "unknown", "unreadable"
        r["gpu_detail"] = "a graphics device is present but its VRAM could not be read"
        r["findings"].append("VRAM unreadable: AdapterRAM stops near 4 GB, and neither nvidia-smi nor the registry value answered. Open Task Manager, Performance, GPU, and read 'Dedicated GPU memory'; tell the orchestrator the number.")

    # --- RAM, Blender floor
    ram = report["ram"]["total_gb"]
    r["ram_gb"] = ram
    if ram is None:
        r["ram_tier"] = "unknown"
    else:
        r["ram_tier"] = tier_by_min(ram, tiers["ram"]["tiers"], "min_gb")
    r["wsl2"] = ("ok (%s GB or more)" % tiers["ram"]["wsl2_ok_tier"].rstrip("+")) if r["ram_tier"] == tiers["ram"]["wsl2_ok_tier"] else "not advised (under 16 GB; run one heavy program at a time)"
    bf = tiers["blender_floor"]
    below = []
    if report["cpu"]["cores"] is not None and report["cpu"]["cores"] < bf["cores"]:
        below.append("cores")
    if ram is not None and ram + 0.5 < bf["ram_gb"]:
        below.append("RAM")
    if readable and max(x[0] for x in readable) + tiers["vram_buckets"]["tolerance_gb"] < bf["vram_gb"]:
        below.append("VRAM")
    r["blender_floor"] = "meets (%d cores / %d GB RAM / %d GB VRAM)" % (bf["cores"], bf["ram_gb"], bf["vram_gb"]) if not below else "below on: " + ", ".join(below)
    if r["gpu_tier"] == "none":
        below.append("GPU")
        r["blender_floor"] = "below on: " + ", ".join(below) + " (no graphics card: Blender still runs, Cycles on the CPU, EEVEE and the viewport slowly)"
    elif r["gpu_tier"] == "unknown":
        r["blender_floor"] += "; GPU memory unreadable, so the VRAM part is not judged"

    # --- disk
    drives = report["disks"]
    r["disks"] = drives
    if drives:
        best = max(drives, key=lambda d: d["free_gb"])
        r["disk_best"] = best
        r["disk_tier"] = tier_by_min(best["free_gb"], tiers["disk"]["tiers"], "min_free_gb")
    else:
        r["disk_tier"] = "unknown"

    # --- display
    p = report["display"]["primary"]
    if p and p.get("width"):
        r["display_class"] = tier_by_min(p["width"], tiers["display"]["classes"], "min_width")
    else:
        r["display_class"] = "unknown"

    if report["redaction"]["self_scan_passed"] is not True:
        r["info"].append("the report says its own identifying-data scan did not pass: do not file it and do not paste it again")

    # --- tools
    t = report["tools"]
    ff = t["ffmpeg"]
    r["ffmpeg_found"] = ff["found"]
    if not ff["found"]:
        r["findings"].append("ffmpeg is not installed or not on PATH (playbooks/agent-pipeline.md Step 2 gives the winget line).")
    else:
        k = vkey(ff["version"])
        r["ffmpeg_numeric"] = ".".join(str(x) for x in k[:3]) if k and re.match(r"^\s*v?\d+\.\d+\.\d+", str(ff["version"])) else (("%d.%d" % k[:2]) if k else None)
        if k and k[0] < tiers["ffmpeg"]["min_major"]:
            r["findings"].append("ffmpeg %s is older than the planner's floor of %d.x; install the build named in playbooks/agent-pipeline.md Step 2." % (r["ffmpeg_numeric"], tiers["ffmpeg"]["min_major"]))
        for feat, label in (("has_libx264", "libx264 (venue and phone H.264 files)"), ("has_libass", "libass (burned-in captions)")):
            if ff.get(feat) is False:
                r["findings"].append("this ffmpeg build lacks %s; use a full build." % label)
            elif ff.get(feat) is None:
                r["info"].append("ffmpeg feature %s could not be read" % feat)
        if ff.get("has_zscale") is False:
            r["info"].append("ffmpeg has no zscale filter (optional: the frozen chains do not use it)")
    if not t["ffprobe"]["found"]:
        r["info"].append("ffprobe not found (it ships with ffmpeg; the validators need it)")
    py = t["python"]
    kp = vkey(py["version"])
    r["python_ok"] = bool(py["found"] and kp and kp >= vkey(tiers["python"]["min_version"]))
    if not py["found"]:
        r["findings"].append("Python is not installed (playbooks/agent-pipeline.md Step 2: Python 3.13 by winget).")
    elif kp is None:
        r["findings"].append("Python was found but its version could not be read; run 'py -0' and tell the orchestrator.")
    elif not r["python_ok"]:
        r["findings"].append("Python %s is older than %s; install 3.13." % (py["version"], tiers["python"]["min_version"]))
    r["git_ok"] = bool(t["git"]["found"])
    if not r["git_ok"]:
        r["info"].append("Git not installed yet (needed from the week-4 session close, not today)")

    # --- Craft pins
    r["craft"] = craft_status(report, pins)
    for a in r["craft"]["rows"]:
        if a["status"] == "mismatch":
            r["findings"].append("Craft pin mismatch: %s %s is not the pinned %s%s (win/pins.json, W-22)." % (a["app"], a["versions"], a["pin"], (" or fallback " + a["fallback"]) if a["fallback"] else ""))

    # --- shared PC hint (chat only; never filed)
    n = report["local_accounts_count"]
    if n is None:
        r["shared_pc_hint"] = "unknown (could not count local accounts)"
    elif n >= tiers["accounts"]["shared_hint_threshold"]:
        r["shared_pc_hint"] = "%d enabled local accounts: the PC may be shared. Ask O-03; if she can reach this PC, use the separate project account (W-26)." % n
    else:
        r["shared_pc_hint"] = "%d enabled local account: no sign of sharing from the machine alone. O-03 is still about her home, so still ask." % n
    return r


def craft_status(report, pins):
    found = {}
    for f in report["craft_apps"]["found"]:
        found.setdefault(f["app"], []).append(f["version"])
    absent = set(report["craft_apps"]["not_found"])
    rows = []
    for app, spec in pins["apps"].items():
        pin, fb, retired = spec.get("pin"), spec.get("fallback"), spec.get("retired", [])
        vers = found.get(app, [])
        if not pin:
            status = "unpinned"          # SoundCraft: learning only, no pin (W-22, D-12)
        elif not vers:
            status = "absent"
        elif pin in vers:
            status = "match"
        elif fb and fb in vers:
            status = "fallback-pin"
        else:
            status = "mismatch"
        retired_seen = [v for v in vers if v in retired]
        rows.append({"app": app, "status": status, "versions": ", ".join(vers) if vers else "-", "pin": pin, "fallback": fb,
                     "retired": retired_seen, "learning_only": pin is None})
    return {"rows": rows}


# ----------------------------------------------------------------------------- printing
STATUS_WORDS = {"match": "match", "fallback-pin": "fallback pin", "mismatch": "MISMATCH", "absent": "absent", "unpinned": "unpinned (learning only)"}


def print_table(report, a, tiers, out=print):
    out("TIER TABLE (chat use only: it shows exact sizes; file pc_tier.json, never this)")
    if not a["windows_report"]:
        return
    out("  gpu_tier        %-10s %s" % (a["gpu_tier"], a["gpu_detail"]))
    out("  ram_tier        %-10s %s GB; WSL2 %s" % (a["ram_tier"], ("%.1f" % a["ram_gb"]) if a["ram_gb"] is not None else "?", a["wsl2"]))
    if a["edition_family"] == "pro-or-higher":
        ed = "Pro or higher (%s): BitLocker can be offered; a VeraCrypt file container works too" % a["edition_id"]
    elif a["edition_family"] == "home":
        ed = "Home (%s): BitLocker not offered; the VeraCrypt file container works on Home (W-25)" % a["edition_id"]
    else:
        ed = "edition not recognised (%s): ask the orchestrator" % a["edition_id"]
    out("  edition         %-10s %s" % (a["edition_family"], ed))
    if a.get("disk_best"):
        c = [d for d in a["disks"] if d["drive"] == "C"]
        out("  disk            %-10s best drive has %.1f GB free%s" % (a["disk_tier"], a["disk_best"]["free_gb"],
                                                                   ("; C: has %.1f GB free" % c[0]["free_gb"]) if c else ""))
    else:
        out("  disk            unknown    no drive was listed")
    p = report["display"]["primary"]
    out("  display         %-10s %s" % (a["display_class"], ("%sx%s at %s Hz, scale %s%%, %s screen(s)" % (p["width"], p["height"], p["refresh_hz"], p["scale_percent"], report["display"]["count"])) if p else "not read"))
    out("  blender floor   %s" % a["blender_floor"])
    ff = report["tools"]["ffmpeg"]
    if ff["found"]:
        feats = " ".join(n.replace("has_", "") + ("" if ff.get(n) else "(NO)" if ff.get(n) is False else "(?)") for n in ("has_libx264", "has_libass", "has_zscale"))
        sha = (ff.get("sha256") or "")[:12]
        out("  ffmpeg          %s  %s  sha256 %s..." % (a.get("ffmpeg_numeric") or ff["version"], feats, sha if sha else "unreadable"))
        out("                  run the colour-patch test on this build (it is the build the PC will use; the container used %s)" % tiers["ffmpeg"]["container_build"])
    else:
        out("  ffmpeg          not found")
    py = report["tools"]["python"]
    out("  python          %s" % ("%s%s" % (py["version"], "" if a["python_ok"] else " (too old)") if py["found"] else "not found"))
    gi = report["tools"]["git"]
    out("  git             %s" % (gi["version"] if gi["found"] else "not found"))
    out("  other tools     " + ", ".join("%s %s" % (n, "yes" if report["tools"][n]["found"] else "no") for n in ("winget", "magick", "inkscape", "blender", "wsl")) +
        ", veracrypt %s" % {True: "yes", False: "no", None: "?"}[report["tools"]["veracrypt_installed"]])
    out("  craft pins      " + "; ".join("%s %s%s" % (r["app"], STATUS_WORDS[r["status"]], (" (%s)" % r["versions"]) if r["versions"] != "-" else "") for r in a["craft"]["rows"]))
    for r in a["craft"]["rows"]:
        if r["retired"]:
            out("                  %s %s is retired" % (r["app"], ", ".join(r["retired"])))
    out("  shared_pc_hint  %s" % a["shared_pc_hint"])
    if report["claude_desktop_running"]:
        out("  note            the Claude desktop app was running; close it before renders (D-10)")


def tier_file(report, a, day):
    ff = report["tools"]["ffmpeg"]
    num = a.get("ffmpeg_numeric")
    return {
        "schema": "lj-pc-tier/1",
        "date": day,
        "windows": {"edition_family": a["edition_family"], "build_major": a["build_major"]},
        "gpu_tier": a["gpu_tier"],
        "vram_bucket": a["vram_bucket"],
        "ram_tier": a["ram_tier"],
        "disk_tier": a["disk_tier"],
        "display_class": a["display_class"],
        "ffmpeg": {"version": num if (ff["found"] and num) else None,
                   "sha256": ff.get("sha256") if ff["found"] else None,
                   "has_libx264": ff.get("has_libx264") if ff["found"] else None,
                   "has_libass": ff.get("has_libass") if ff["found"] else None,
                   "has_zscale": ff.get("has_zscale") if ff["found"] else None},
        "python_ok": bool(a["python_ok"]),
        "git_ok": bool(a["git_ok"]),
        "craft_pins": [{"app": r["app"], "status": r["status"]} for r in a["craft"]["rows"]],
    }


def hardware_md(report, a, tiers, day):
    vulk = report["vulkan"]
    devs = vulk.get("devices", [])
    real_dev = [d for d in devs if not any(p.lower() in d.lower() for p in tiers["gpu"]["software_name_patterns"])]
    vstate = "yes" if real_dev else ("software device only (counts as no GPU)" if devs else "no")
    gfam = "none"
    for g in report["gpus"]:
        if not is_software_gpu(g, tiers):
            gfam = vendor_family(g.get("vendor"), g.get("name"))
            break
    lines = [
        "# Hardware (derived, bucketed draft)",
        "",
        "Draft written by `scripts/windows_check.py --hardware-md` from a pasted PC report. It carries tier words and buckets only: no CPU or GPU model, no driver, no exact size, no account count. The orchestrator reviews it before it is placed in `decisions/hardware.md`.",
        "",
        "- Date run: %s (day only)" % day,
        "- GPU tier: %s (vendor family: %s)" % (a["gpu_tier"], gfam),
        "- VRAM bucket (GB): %s" % a["vram_bucket"],
        "- RAM tier (GB): %s (WSL2 %s)" % (a["ram_tier"], "ok" if a["wsl2"].startswith("ok") else "not advised"),
        "- Free disk tier: %s (judged on the drive with the most free space; thresholds in `win/tiers.json`)" % a["disk_tier"],
        "- Vulkan device listed: %s (runtime library present: %s)" % (vstate, {True: "yes", False: "no", None: "unknown"}[vulk.get("runtime_dll_present")]),
        "- Windows: build %s, edition family %s" % (a["build_major"] if a["build_major"] is not None else "unknown", a["edition_family"]),
        "- Display class: %s" % a["display_class"],
        "- Scanner: (the maker fills this in by hand; it is not read from the PC)",
        "- Capture gear on hand: (the maker fills this in by hand)",
        "",
    ]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- pattern self-test (4.13)
def load_samples(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(data, dict) and isinstance(data.get("samples"), (dict, list)):
        data = data["samples"]
    out = {}
    if isinstance(data, dict):
        for k, v in data.items():
            out[str(k)] = _join(v)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            if isinstance(v, dict):
                out[str(v.get("id", i))] = _join(v)
            else:
                out[str(i)] = _join(v)
    else:
        raise ValueError("unrecognised samples file")
    return out


def pattern_self_test(pat, samples_path):
    samples = load_samples(samples_path)
    results = {}
    for sid, text in samples.items():
        ids = []
        for cid, _m in category_hits(pat, "", text):
            if cid not in ids:
                ids.append(cid)
        results[sid] = ids
    return {"consumer": "scripts/windows_check.py", "patterns_version": pat.version, "results": results}


# ----------------------------------------------------------------------------- main
def parse_args(argv):
    ap = argparse.ArgumentParser(prog="windows_check.py", add_help=True, allow_abbrev=False,
                                 description="Validate a pasted PC inventory report and print the hardware tier table.")
    ap.add_argument("report", nargs="?", help="pc_report.json (UTF-8, UTF-8 with BOM or UTF-16); - reads the pasted report from standard input, so it never has to be saved")
    ap.add_argument("--forbid", action="append", default=[], metavar="WORD", help="also refuse this name (invented names in tests only)")
    ap.add_argument("--json-out", metavar="PATH")
    ap.add_argument("--tier-json-out", metavar="PATH")
    ap.add_argument("--hardware-md", metavar="PATH")
    ap.add_argument("--pattern-self-test", metavar="SAMPLES.json")
    return ap.parse_args(argv)


def write_text(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")  # a Windows console may not encode every character of a masked hit
        except (AttributeError, ValueError):
            pass
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0

    # 1. fail closed on the pattern file BEFORE anything else is read
    try:
        pat = load_patterns()
    except FailClosed as e:
        print("REDACTION PATTERNS UNAVAILABLE, nothing was checked and nothing was written: %s" % e)
        return 2

    if args.pattern_self_test:
        try:
            res = pattern_self_test(pat, args.pattern_self_test)
        except (OSError, ValueError):
            print("windows_check: cannot read the samples file", file=sys.stderr)
            return 2
        print(json.dumps(res, sort_keys=True))
        return 0

    if not args.report:
        print("usage: windows_check.py [options] REPORT.json   (see --help)", file=sys.stderr)
        return 2
    try:
        raw = sys.stdin.buffer.read() if args.report == "-" else Path(args.report).read_bytes()
    except OSError:
        print("windows_check: cannot read the report file", file=sys.stderr)
        return 2
    try:
        text, enc = decode_bytes(raw)
        report = json.loads(text)
    except (UnicodeError, ValueError) as e:
        where = " (line %d, column %d)" % (e.lineno, e.colno) if isinstance(e, json.JSONDecodeError) else ""
        print("INVALID: the file is not readable JSON%s. Nothing was written." % where)
        return 2
    if not isinstance(report, dict):
        print("INVALID: the report must be a JSON object. Nothing was written.")
        return 2

    print("PC REPORT CHECK")
    print("encoding: %s" % enc)

    # 2. identifying-data scan (same pattern file; names from --forbid and the local deny list)
    names = [("user_name", w, True) for w in args.forbid] + [("local_deny", w, False) for w in read_local_deny(pat)]
    refusals, notes, skipped = scan_report(pat, report, names)
    for cat, n in skipped:
        print("NOTE name check skipped for a %s of %d character(s): shorter than %d, so it would match ordinary words (the pattern checks still ran)" % (cat, n, pat.min_name_len))
    for cat, field, hit in notes:
        print("NOTE category=%s field=%s hit=%s (a hardware-name field: reported, not refused)" % (cat, field, hit))
    if refusals:
        print("REDACTION CHECK FAILED, identifying data found; nothing was written. Do not paste this report anywhere.")
        for cat, field, hit in refusals:
            print("category=%s field=%s hit=%s" % (cat, field, hit))
        return 2
    print("identifying-data scan: PASS (patterns version %s)" % (pat.version,))

    # 3. schema
    try:
        schema = load_json_file(WIN_DIR / "schema" / "pc_report.schema.json", "win/schema/pc_report.schema.json")
        tiers = load_json_file(WIN_DIR / "tiers.json", "win/tiers.json")
        pins = load_json_file(WIN_DIR / "pins.json", "win/pins.json")
    except EnvProblem as e:
        print("ENVIRONMENT: %s (download the whole project folder)" % e)
        return 3
    errs = []
    validate(report, schema, schema, "", errs)
    if errs:
        print("INVALID: the report does not match win/schema/pc_report.schema.json. Nothing was written.")
        for p, why in errs[:20]:
            print("  schema: %s %s" % (p or "(top level)", why))
        if len(errs) > 20:
            print("  schema: ... and %d more" % (len(errs) - 20))
        return 2
    print("schema: PASS (report format v%s from %s)" % (report["schema_version"], report["tool"]))

    # 4. tiers
    a = assess(report, tiers, pins)
    if not a["windows_report"]:
        for f in a["findings"]:
            print(f)
        print("RESULT: exit 1 (valid report, but not a Windows report; no tier file was written)")
        return 1
    print_table(report, a, tiers)
    for i in a["info"]:
        print("INFO: %s" % i)
    for f in a["findings"]:
        print("FINDING: %s" % f)

    day = report["generated_utc"][:10]
    if args.json_out:
        write_text(args.json_out, json.dumps({
            "schema": "lj-pc-check/1", "filing": "chat or scratch only; it carries exact sizes. File pc_tier.json instead.",
            "windows_report": True, "gpu_tier": a["gpu_tier"], "gpu_detail": a["gpu_detail"], "ram_tier": a["ram_tier"], "ram_gb": a["ram_gb"],
            "wsl2": a["wsl2"], "edition_family": a["edition_family"], "disk_tier": a["disk_tier"], "display_class": a["display_class"],
            "blender_floor": a["blender_floor"], "shared_pc_hint": a["shared_pc_hint"], "craft": a["craft"]["rows"],
            "findings": a["findings"], "info": a["info"], "exit": 1 if a["findings"] else 0}, indent=2, sort_keys=True) + "\n")
        print("wrote: json-out (chat or scratch use only)")
    if args.tier_json_out:
        tf = tier_file(report, a, day)
        tschema = load_json_file(WIN_DIR / "schema" / "pc_tier.schema.json", "win/schema/pc_tier.schema.json")
        terrs = []
        validate(tf, tschema, tschema, "", terrs)
        if terrs:
            print("INTERNAL: the derived tier file does not match its own schema; nothing was written")
            for p, why in terrs[:10]:
                print("  schema: %s %s" % (p, why))
            return 3
        write_text(args.tier_json_out, json.dumps(tf, indent=2, sort_keys=False) + "\n")
        print("wrote: tier-json-out (buckets and verdict words only; the only PC data that may be filed)")
    if args.hardware_md:
        write_text(args.hardware_md, hardware_md(report, a, tiers, day))
        print("wrote: hardware-md (bucketed draft, no model names)")

    if a["findings"]:
        print("RESULT: exit 1 (valid; %d finding(s) need a human)" % len(a["findings"]))
        return 1
    print("RESULT: exit 0 (valid; nothing needs a human. A low tier is information, not a failure.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
