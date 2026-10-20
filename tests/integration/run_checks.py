#!/usr/bin/env python3
"""run_checks.py: the WP-11b test driver (called by tests/integration/run_tests.sh; it can also be run alone).

  python3 -I tests/integration/run_checks.py --mode quick|all [--only name,name] [--list] [--work renders/wp11b] [--evidence build/evidence/wp11b]

What it proves (build plan WP-11b): that the pieces of weeks 1 and 2 FIT TOGETHER.
  parity.*     two packages' files say the same thing: settings card = settings.json = chains.json; phone row = PHONE-ROW.md = profile.json, and profile.json = the
               register's W-63/W-18 figures (DECISIONS.md wins; the card is judged against the register on those figures); the harness
               built-in chain = chains.json; win/pins.json = release_assets.json = W-22; decisions.csv = the register; the pc_report fields windows_check.py reads
               exist in the schema; lj.ps1 close v0 calls current script names and has no deleting or committing switch; every script with test strings has a
               Noto family; the 'Scripts tested' line = scripts_tested.json
  redaction.*  public_lint.py --self-test with zero skipped consumers; no raw-PC-report file name anywhere outside tests/win/fixtures; build/evidence/pc/ holds
               only schema-valid derived files and none of the fixtures' GPU, CPU or driver strings; the derivation tools leak none either
  disk.*       from every evidence envelope's df figures: the 400 MB rule for stages over 100 MB, the 250 MB hard floor (with a reviewed exceptions list), the
               tarball ledger, the 2 GB download allowance, and df after cleanup_scratch.sh
  e2e.*  (all) the WP-04 test card through --chain and spec_check.py; the A11 MO8 pair; a harness master through the phone encode, spec_check, phone_check and fill_20x9
  hygiene.*    stale_check --new-only, public_lint over the build and over the diff, the theme guard, no file over 1 MB, no binary, new text under 8 MB, no ignored
               file tracked or staged, the .gitignore backstop for raw PC reports
  docs.* / readiness.* / index.*   pipeline/README.md and the staged skill are real; P-LOCK-readiness-W2.md has a status on every row and no PASS for anything that
               needs Windows; INDEX.md has the thirteen rows with evidence links that exist
  ctrl.*       negative controls: a planted defect in a copy of the input makes the checker fail (a test that cannot fail proves nothing)

One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail     and one lj-evidence/1 envelope per test (build plan 4.2) in <evidence>/tests_<mode>.jsonl
(with --only: tests_<mode>_only.jsonl and summary_<mode>_only.json instead, so a partial run never replaces the mode's evidence; nothing reads the _only files as evidence).
Exit 0 if no line is FAIL or BLOCKED; 1 if a line FAILs; 3 if a line is BLOCKED; 2 for a bad option. UNVERIFIED (Windows behaviour) is never counted as a pass.
Everything is synthetic: the only media are generated test cards and tones. Windows behaviour is never claimed. Writes only under build/evidence/wp11b/, renders/wp11b/
and the scratch folder (all removed again except the evidence).
"""
import argparse
import datetime
import fnmatch
import glob
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SCRATCH = os.environ.get("LJ_SCRATCH", os.path.normpath(os.path.join(ROOT, "..", "build-scratch")))
PY = [sys.executable, "-I", "-B"]
COUNTS = {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0}
STATE = {"min_avail": None, "start": None}
ARGS = None
REG = []
S = {}                                   # shared between tests of one run
BUILD_ROOTS = ["win", "scripts", "pipeline", "ops", "spikes", "tests", "build", "skills-staging", "reviews/build"]
NEW_TEXT_LIMIT_BYTES = 8_000_000      # gate review r1 (Mon 19 Oct 2026): the plan's 5 MB was too tight for 13 packages of tests and evidence; measured 7.06 MB at the gate
PWSH = os.path.join(SCRATCH, "pwsh", "pwsh")
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------------------------- plumbing
def sh(args, timeout=600, env=None, cwd=None, inp=None):
    e = dict(os.environ)
    for k in ("FFMPEG", "FFPROBE"):
        e.pop(k, None)
    if env:
        e.update(env)
    try:
        p = subprocess.run(args, cwd=cwd or ROOT, stdin=subprocess.DEVNULL if inp is None else None, input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout, env=e)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %s s" % timeout
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def avail_mb():
    try:
        st = os.statvfs("/")
        return int(st.f_bavail * st.f_frsize // (1024 * 1024))
    except OSError:
        return 0


def clean(s, n=900):
    s = str(s).replace(ROOT, ".").replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    s = re.sub(r"/home/(?!user\b)[^\s'\"]+", "<path>", s)
    return s[:n]


def scrub(s):
    s = str(s).replace(ROOT, ".").replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return re.sub(r"/home/(?!user\b)[^\s'\"]+", "<path>", s)


def rel(path):
    return os.path.relpath(path, ROOT)


def p(*parts):
    return os.path.join(ROOT, *parts)


def read_text(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def read_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def work(*parts):
    return os.path.join(ARGS.work, *parts)


def ev(*parts):
    return os.path.join(ARGS.evidence, *parts)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ledger(label):
    try:
        with open(os.path.join(SCRATCH, "disk-ledger.jsonl"), encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if '"label":"%s"' % label in l]
        return rows[-1] if rows else None
    except OSError:
        return None


class DiskWatch:
    """Polls Avail every 0.5 s in a thread and keeps the minimum (the envelope's avail_mb_min for a stage that does not run under the guard's own watchdog)."""

    def __init__(self):
        self.min = avail_mb()
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop.wait(0.5):
            a = avail_mb()
            if a and a < self.min:
                self.min = a

    def __enter__(self):
        self._t.start()
        return self

    def __exit__(self, *a):
        self._stop.set()
        self._t.join(2)
        a = avail_mb()
        if a and a < self.min:
            self.min = a


def ffmpeg_version():
    rc, out, err = sh(["ffmpeg", "-version"], timeout=20)
    m = re.search(r"ffmpeg version (\S+)", out)
    return m.group(1) if m else "unknown"


def record(name, status, expected, actual, unverified="", planned=0, note="", lg=None, disk=None):
    COUNTS[status] += 1
    a = avail_mb()
    s0 = STATE["start"]
    lo = min([x for x in (s0, a) if x] or [0])
    if disk:
        s0, a, lo = disk["start"], disk["end"], disk["min"]
    row = ledger(lg) if lg else None
    if row:
        s0, a, lo = row["avail_mb_start"], row["avail_mb_end"], min(row["avail_mb_min"], lo)
    STATE["min_avail"] = lo if STATE["min_avail"] is None else min(STATE["min_avail"], lo)
    env = {"platform": "linux", "ffmpeg": ARGS.ffv, "nproc": os.cpu_count(), "python": "%d.%d.%d" % sys.version_info[:3], "node": "22.x"}
    rec = {"schema": "lj-evidence/1", "package": "WP-11b", "test": name, "date_utc": TODAY, "status": status, "env": env,
           "disk": {"avail_mb_start": s0, "planned_write_mb": planned, "avail_mb_min": lo, "avail_mb_end": a, "floor_mb": 400, "hard_floor_mb": 250},
           "expected": clean(expected), "actual": clean(actual, 1500), "notes": note, "unverified_reasons": [unverified] if unverified else []}
    with open(ARGS.jsonl, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("%-10s %-44s %s" % (status, name, clean(actual)[:200].replace("\n", " ")), flush=True)
    sys.stdout.flush()


def test(name, modes=("quick", "all")):
    def deco(fn):
        REG.append((name, modes, fn))
        return fn
    return deco


class Skip(Exception):
    pass


class Blocked(Exception):
    pass


def check(name, ok, expected, actual, unverified="", planned=0, lg=None, note="", disk=None):
    record(name, "PASS" if ok else "FAIL", expected, actual, unverified, planned, note=note, lg=lg, disk=disk)
    return ok


def listing(items, n=6, sep="; "):
    items = list(items)
    s = sep.join(str(x) for x in items[:n])
    return s + ("%s... and %d more" % (sep, len(items) - n) if len(items) > n else "")


# ----------------------------------------------------------------------------------------------- repository file sets
def git(*a):
    return sh(["git"] + list(a), timeout=120)


def repo_files(include_ignored=False):
    """Tracked files plus untracked files that are not ignored (what a commit could contain). Repo-relative, sorted."""
    rc, out, err = git("ls-files", "-z")
    tracked = [x for x in out.split("\0") if x]
    rc2, out2, err2 = git("ls-files", "-z", "--others", "--exclude-standard")
    others = [x for x in out2.split("\0") if x]
    files = sorted(set(tracked) | set(others))
    return [f for f in files if os.path.isfile(p(f))]


def in_roots(path, roots=BUILD_ROOTS):
    return any(path == r or path.startswith(r + "/") for r in roots)


def build_baseline():
    """The commit before the build started: the parent of the commit that first added the build plan (no hash is written into any file)."""
    rc, out, err = git("log", "--diff-filter=A", "--format=%H", "--", "build/BUILD-PLAN-W1-2.md")
    first = [l for l in out.split() if l]
    if not first:
        return None
    rc, out, err = git("rev-parse", first[-1] + "^")
    return out.strip() if rc == 0 else None


# ----------------------------------------------------------------------------------------------- markdown tables
def md_rows(text):
    """{first cell without emphasis marks: [cells]} for every table row with at least 6 cells."""
    rows = {}
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.count("|") >= 7:
            cells = [c.strip() for c in s.strip("|").split("|")]
            key = re.sub(r"[*`]", "", cells[0]).strip()
            if key and not set(key) <= set("-: "):
                rows.setdefault(key, cells)
    return rows


def find_row(rows, prefix):
    for k, v in rows.items():
        if k.startswith(prefix):
            return v
    return None


def need(text, needles, where):
    """needles: [(string, why)]. Returns the list of problems (a needle missing from text)."""
    return ["%s: missing %r (%s)" % (where, n, why) for n, why in needles if n not in text]


def arg_after(args, flag):
    try:
        return args[args.index(flag) + 1]
    except (ValueError, IndexError):
        return None


# ----------------------------------------------------------------------------------------------- parity: settings card
def card_problems(card, settings, chains):
    """Every number the card states for TD-1 to TD-4, colour and sound, computed from pipeline/settings.json and pipeline/lib/chains.json."""
    rows = md_rows(card)
    probs = []
    pic, fps, cap, loud = settings["picture"], settings["fps"], settings["captions"], settings["loudness"]
    aud, mast, prof = settings["audio"], settings["master"], settings["profiles"]
    ven, bk = chains["h264_venue"], chains["h264_backup_main40"]

    def t(prefix):
        r = find_row(rows, prefix)
        if r is None:
            probs.append("card has no row starting %r" % prefix)
            return ""
        return " ".join(r[1:])

    crf = arg_after(ven["video_args"], "-crf")
    vmax = arg_after(ven["video_args"], "-maxrate")
    ab = arg_after(ven["audio_args"], "-b:a")
    bkb = arg_after(bk["video_args"], "-b:v")
    vp, vl = prof["venue_h264"]["video"]["profile"][0], prof["venue_h264"]["video"]["level"][0]
    bp, bl = prof["venue_h264_backup_main40"]["video"]["profile"][0], prof["venue_h264_backup_main40"]["video"]["level"][0]
    probs += need(t("TD-1"), [("%dx%d" % (pic["width"], pic["height"]), "picture size"), ("%d px" % pic["stills_long_edge_px"], "stills long edge"),
                              ("ProRes 422 HQ", "master codec"), ("10-bit 4:2:2", "master pix_fmt yuv422p10le"),
                              ("PCM %d-bit %d kHz" % (aud["master_bit_depth"], aud["sample_rate_hz"] // 1000), "master audio"),
                              ("prores,%d,%d,%s" % (pic["width"], pic["height"], mast["pix_fmt"]), "the ffprobe line it prints")], "TD-1")
    probs += need(t("TD-2"), [("%d fps" % fps["num"], "frame rate"), (fps["text"] + "," + fps["text"], "the ffprobe line it prints")], "TD-2")
    probs += need(t("TD-3"), [("FontSize=%d" % cap["font_size"], "caption size"), ("%d characters a line" % cap["max_chars_per_line"], "line length"),
                              ("%d characters a second" % cap["max_chars_per_second"], "reading speed"), ("%d%% by %d%%" % (cap["safe_box_percent"], cap["safe_box_percent"]), "safe box")], "TD-3")
    probs += need(t("TD-4"), [("%s %.1f" % (vp, vl / 10.0), "venue profile and level"), ("yuv420p", "pix_fmt"), ("AAC-LC", "audio codec"), ("%s kbps" % ab.rstrip("k"), "audio bitrate"),
                              ("CRF %s" % crf, "venue CRF"), ("%s Mbps" % vmax.rstrip("M"), "venue cap"), ("+faststart", "faststart"),
                              ("%s %.1f" % (bp, bl / 10.0), "backup profile and level"), ("%s Mbps" % bkb.rstrip("M"), "backup rate"),
                              (settings["dcp"]["standard"], "DCP standard"), ("1998x1080", "2K Flat container"), (str(settings["dcp"]["fps"]) + " fps", "DCP rate")], "TD-4")
    probs += need(t("Colour"), [("within %d of 255" % settings["colour"]["colour_patch_tolerance_of_255"], "colour-patch tolerance"), ("BT.1886", "video transfer"), ("sRGB", "stills")], "Colour")
    cands = loud["venue_lufs_candidates"]
    probs += need(t("Sound"), [("%d dBTP" % loud["true_peak_max_dbtp"], "true peak ceiling"), ("%d, %d and %d LUFS" % tuple(cands), "venue candidates"),
                               ("%d LUFS" % loud["online_lufs"], "online loudness"), ("%d kHz, %d-bit" % (aud["sample_rate_hz"] // 1000, aud["master_bit_depth"]), "master audio")], "Sound")
    if "signed: %s" % ("yes" if settings.get("signed") else "no") not in card:
        probs.append("signature block: the card says a different signed state from settings.json (signed=%s)" % settings.get("signed"))
    return probs


@test("parity.settings_card_vs_settings_json")
def t_card_settings():
    card = read_text(p("ops", "SETTINGS-CARD.md"))
    settings = read_json(p("pipeline", "settings.json"))
    chains = read_json(p("pipeline", "lib", "chains.json"))["chains"]
    probs = card_problems(card, settings, chains)
    n = len(md_rows(card))
    check("parity.settings_card_vs_settings_json", not probs, "every number in the card rows TD-1 to TD-4, Colour and Sound equals pipeline/settings.json and the venue chains of pipeline/lib/chains.json",
          "%d card rows read; %s" % (n, "all equal" if not probs else listing(probs)))


# ----------------------------------------------------------------------------------------------- parity: phone row
def rate_mbps(arg):
    """'8M' -> 8.0, '3500k' -> 3.5 (an ffmpeg -maxrate argument in Mb/s)."""
    a = str(arg).strip()
    return int(a[:-1]) / 1000.0 if a.endswith("k") else float(a.rstrip("M"))


def register_phone_facts(dec_text):
    """What DECISIONS.md says about the phone files. The register wins over every package file (CLAUDE.md, D-21), so every figure W-63 and W-18 state is read here
    the way t_pins reads W-22. Returns (facts, problems); a figure a row no longer states in the shape read here is a problem (fail closed), never a silent default."""
    facts, probs = {}, []
    w63 = re.search(r"^\| W-63 \|.*$", dec_text, re.M)
    w18 = re.search(r"^\| W-18 \|.*$", dec_text, re.M)
    if not w63:
        probs.append("DECISIONS.md has no W-63 row")
    else:
        m = re.search(r"PH1, the phone master:.*?CRF (\d+) with an? ([0-9.]+) Mb/s cap", w63.group(0))
        if m:
            facts["ph1_crf"], facts["ph1_cap_mbps"] = m.group(1), float(m.group(2))
        else:
            probs.append("W-63 no longer states 'PH1 ... CRF n with a n Mb/s cap' in the shape this test reads")
        m = re.search(r"PH2, the small copy:\*\*\s*1280x720, CRF (\d+), ([0-9.]+) Mb/s cap, level ([0-9.]+),", w63.group(0))
        if m:
            facts["ph2_crf"], facts["ph2_cap_mbps"], facts["ph2_level"] = m.group(1), float(m.group(2)), m.group(3)
        else:
            probs.append("W-63 no longer states 'PH2 ... 1280x720, CRF n, n Mb/s cap, level n' in the shape this test reads")
    if not w18:
        probs.append("DECISIONS.md has no W-18 row")
    else:
        m = re.search(r"phone file carries its own caption setting: `FontSize=(\d+)`, `MarginV` (\d+), two lines, at most (\d+) characters", w18.group(0))
        if m:
            facts["font_size"], facts["margin_v"], facts["max_chars"] = int(m.group(1)), int(m.group(2)), int(m.group(3))
        else:
            probs.append("W-18 no longer states 'the phone file ... FontSize=n, MarginV n, two lines, at most n characters' in the shape this test reads")
    return facts, probs


def phone_register_problems(profile, reg):
    """profile.json against the register's figures. Returns [(label, register text, profile text)] for every figure that differs; the register is the truth."""
    if not reg:
        return []
    ch, st = profile["chains"], profile["caption"]["styles"]["phone"]
    p1, p2 = ch["phone_1080"]["video_args"], ch["phone_720_share"]["video_args"]
    pairs = [("PH1 CRF", reg.get("ph1_crf"), arg_after(p1, "-crf"), ""), ("PH1 cap", reg.get("ph1_cap_mbps"), rate_mbps(arg_after(p1, "-maxrate")), " Mb/s"),
             ("PH2 CRF", reg.get("ph2_crf"), arg_after(p2, "-crf"), ""), ("PH2 cap", reg.get("ph2_cap_mbps"), rate_mbps(arg_after(p2, "-maxrate")), " Mb/s"),
             ("PH2 level", reg.get("ph2_level"), arg_after(p2, "-level"), ""), ("phone caption FontSize", reg.get("font_size"), st["font_size"], ""),
             ("phone caption MarginV", reg.get("margin_v"), st["margin_v"], ""), ("phone caption characters a line", reg.get("max_chars"), st["max_chars_per_line"], "")]
    out = []
    for label, r, v, unit in pairs:
        if r is None:
            continue
        same = (abs(float(r) - float(v)) < 1e-9) if unit else (str(r) == str(v))
        if not same:
            fmt = (lambda x: "%g%s" % (x, unit)) if unit else str
            out.append((label, fmt(r), fmt(v)))
    return out


def phone_needles(profile, fill, venue_fill=None, register=None):
    """The facts a Phone row must state. Taken from profile.json, except that a figure DECISIONS.md states in W-63 or W-18 (passed as `register`) is the register's."""
    ch, pr = profile["chains"], profile["profiles"]
    st = profile["caption"]["styles"]["phone"]
    p1, p2 = ch["phone_1080"], ch["phone_720_share"]
    reg = register or {}
    n = []
    pv1, pv2 = pr["phone_1080"]["video"], pr["phone_720_share"]["video"]
    n.append(("%dx%d" % (pv1["width"], pv1["height"]), "PH1 size"))
    n.append(("%dx%d" % (pv2["width"], pv2["height"]), "PH2 size"))
    n.append(("%s fps" % pv1["fps"].split("/")[0], "frame rate"))
    n.append(("%s %.1f" % (pv1["profile"][0], pv1["level"][0] / 10.0), "PH1 profile and level"))
    n.append(("CRF %s" % reg.get("ph1_crf", arg_after(p1["video_args"], "-crf")), "PH1 CRF"))
    n.append(("%g Mb/s" % reg["ph1_cap_mbps"] if "ph1_cap_mbps" in reg else "%s Mb/s" % arg_after(p1["video_args"], "-maxrate").rstrip("M"), "PH1 cap"))
    n.append(("CRF %s" % reg.get("ph2_crf", arg_after(p2["video_args"], "-crf")), "PH2 CRF"))
    n.append(("%g Mb/s" % reg.get("ph2_cap_mbps", rate_mbps(arg_after(p2["video_args"], "-maxrate"))), "PH2 cap"))
    n.append(("level %s" % reg["ph2_level"] if "ph2_level" in reg else "level %.1f" % (pv2["level"][0] / 10.0), "PH2 level"))
    n.append(("%s kbps" % arg_after(p1["audio_args"], "-b:a").rstrip("k"), "PH1 audio bitrate"))
    n.append(("FontSize=%d" % reg.get("font_size", st["font_size"]), "phone caption size"))
    n.append(("`MarginV` %d" % reg.get("margin_v", st["margin_v"]), "phone caption margin"))
    n.append(("%d characters a line" % reg.get("max_chars", st["max_chars_per_line"]), "phone caption line length"))
    n.append(("%d LUFS" % pr["phone_1080"]["loudness"]["integrated_lufs"][0], "loudness"))
    n.append(("%d dBTP" % pr["phone_1080"]["loudness"]["true_peak_max_dbtp"], "true peak"))
    n.append(("+faststart", "faststart"))
    if fill:
        pos = [v["position"] for v in fill["scenarios"]["fill_20x9"]["scripts"].values() if v and v.get("position")]
        tops = [x["caption_top_pct"] for x in pos]
        bots = [x["caption_bottom_pct"] for x in pos]
        n.append(("%.1f%% to %.1f%%" % (min(tops), max(bots)), "measured caption block (fill_20x9_phone.json)"))
        n.append(("%.1f%%" % max(bots), "caption bottom"))
        n.append(("%.1f%%" % float(st["box_bottom_max_pct"]), "fill_20x9 limit"))
    return n


def phone_row_from_text(text):
    r = find_row(md_rows(text), "Phone")
    return None if r is None else " ".join(r[1:])


def phone_row_text(path):
    return phone_row_from_text(read_text(path))


@test("parity.phone_row_md_vs_profile_json")
def t_phone_row_md():
    prof = read_json(p("pipeline", "phone", "profile.json"))
    fill = read_json(p("build", "evidence", "wp08", "fill_20x9_phone.json"))
    text = phone_row_text(p("pipeline", "phone", "PHONE-ROW.md"))
    if text is None:
        return check("parity.phone_row_md_vs_profile_json", False, "PHONE-ROW.md has the Phone row", "no row starting 'Phone'")
    probs = need(text, phone_needles(prof, fill), "PHONE-ROW.md Phone row")
    ven = read_json(p("build", "evidence", "wp08", "fill_20x9_venue_margin.json"))
    vb = max(v["position"]["caption_bottom_pct"] for v in ven["scenarios"]["fill_20x9"]["scripts"].values() if v and v.get("position"))
    if "%.1f%%" % vb not in read_text(p("pipeline", "phone", "PHONE-ROW.md")):
        probs.append("PHONE-ROW.md: the venue-margin caption bottom %.1f%% (fill_20x9_venue_margin.json) is not quoted" % vb)
    check("parity.phone_row_md_vs_profile_json", not probs, "the Phone row of PHONE-ROW.md states what profile.json says (sizes, rates, CRF, caps, levels, caption size, margin, line length, loudness) and the measured caption block of build/evidence/wp08/fill_20x9_phone.json",
          "all equal (%d facts)" % len(phone_needles(prof, fill)) if not probs else listing(probs))


def register_fix_text(conflicts):
    """The one fix line for any disagreement between profile.json and DECISIONS.md. Never an instruction to move the card against the register."""
    remeasure = ""
    if any("characters a line" in l for l, r, v in conflicts):
        remeasure = " (the caption block was measured at the profile's line length: re-run phone_check.py --scenario fill_20x9 if the profile moves)"
    return ("regenerate pipeline/phone/profile.json and PHONE-ROW.md to W-63/W-18 (%s)%s, or have the orchestrator log the profile's figures (%s) in DECISIONS.md; "
            "only then paste section 1 of pipeline/phone/PHONE-ROW.md over the card's Phone row" % ("; ".join("%s %s" % (l, r) for l, r, v in conflicts), remeasure, "; ".join("%s %s" % (l, v) for l, r, v in conflicts)))


@test("parity.phone_profile_vs_register")
def t_phone_profile_register():
    prof = read_json(p("pipeline", "phone", "profile.json"))
    reg, rprobs = register_phone_facts(read_text(p("DECISIONS.md")))
    exp = ("pipeline/phone/profile.json (WP-08) states the figures DECISIONS.md states for the phone files in W-63 and W-18 (PH1 CRF and cap, PH2 CRF, cap and level, phone caption FontSize, MarginV and characters a line); "
           "the register wins over every package file")
    if rprobs:
        return check("parity.phone_profile_vs_register", False, exp, "the register could not be read: %s" % listing(rprobs, 3))
    conflicts = phone_register_problems(prof, reg)
    if conflicts:
        check("parity.phone_profile_vs_register", False, exp,
              "pipeline/phone/profile.json disagrees with DECISIONS.md, which wins: %s. The settings card follows the register on these figures. FIX (owner WP-08, its round-1 nudge 3; or the orchestrator): %s; "
              "never change the card to the profile's figures while the register says otherwise" % (listing(["%s: profile.json %s, register %s" % (l, v, r) for l, r, v in conflicts], 4), register_fix_text(conflicts)))
    else:
        check("parity.phone_profile_vs_register", True, exp, "profile.json equals the register in all %d figures (PH2 cap %g Mb/s, %d characters a line)" % (len(reg), reg["ph2_cap_mbps"], reg["max_chars"]))


@test("parity.card_phone_row_vs_phone_row_md")
def t_card_phone_row():
    prof = read_json(p("pipeline", "phone", "profile.json"))
    fill = read_json(p("build", "evidence", "wp08", "fill_20x9_phone.json"))
    text = phone_row_text(p("ops", "SETTINGS-CARD.md"))
    exp = ("the Phone row of ops/SETTINGS-CARD.md carries the register's figures (DECISIONS.md W-63, W-18) and, for every other fact, the facts of PHONE-ROW.md and profile.json "
           "(the orchestrator pastes section 1 of PHONE-ROW.md over it before Sun 1 Nov, but only once profile.json agrees with the register)")
    if text is None:
        return check("parity.card_phone_row_vs_phone_row_md", False, exp, "no row starting 'Phone'")
    reg, rprobs = register_phone_facts(read_text(p("DECISIONS.md")))
    conflicts = phone_register_problems(prof, reg) if not rprobs else []
    needles = phone_needles(prof, fill, register=None if rprobs else reg)
    probs = need(text, needles, "SETTINGS-CARD.md Phone row")
    if probs:
        if rprobs:
            fix = "the register could not be read (%s), so do not paste anything yet" % listing(rprobs, 2)
            side = ""
        elif conflicts:
            fix = register_fix_text(conflicts) + ". Do not paste PHONE-ROW.md while profile.json and the register disagree: it would move the card away from W-63 and W-18"
            side = "pipeline/phone/profile.json is the file that disagrees with DECISIONS.md (%s; see parity.phone_profile_vs_register); the card is judged against the register on those figures. " % listing(["%s %s, register %s" % (l, v, r) for l, r, v in conflicts], 3)
        else:
            fix = "paste section 1 of pipeline/phone/PHONE-ROW.md over the Phone row"
            side = ""
        check("parity.card_phone_row_vs_phone_row_md", False, exp, "%s%d fact(s) differ; the card still holds the pre-measurement proposal. %s. FIX (orchestrator): %s" % (side, len(probs), listing(probs, 4), fix))
    else:
        check("parity.card_phone_row_vs_phone_row_md", True, exp, "all %d facts equal%s" % (len(needles), "" if not conflicts else " (profile.json disagrees with the register on %d figure(s); see parity.phone_profile_vs_register)" % len(conflicts)))


def card_language_problems(card, st):
    m = re.search(r"`Caption and font test ran in: ([^`]+)`", card)
    if not m:
        return ["no 'Caption and font test ran in:' line in the card"]
    line = m.group(1)
    probs = []
    for sc in st["scripts_tested"]:
        if sc.lower() not in line.lower():
            probs.append("script %r (tested %s) is not in the card line" % (sc, st["date_utc"]))
    if st["date_utc"] not in line:
        probs.append("the card line has no %s (it reads %r)" % (st["date_utc"], re.findall(r"on ([^;]+);", line)[:1]))
    if "<" in line.split(";")[0]:
        probs.append("the card line still has a placeholder")
    return probs


@test("parity.card_language_note_vs_scripts_tested")
def t_card_language():
    card = read_text(p("ops", "SETTINGS-CARD.md"))
    st = read_json(p("build", "evidence", "wp08", "scripts_tested.json"))
    exp = "the card's language line names every script scripts_tested.json says was tested, with its date, and no placeholder (the orchestrator pastes the 'Scripts tested:' line of PHONE-ROW.md)"
    probs = card_language_problems(card, st)
    if probs:
        check("parity.card_language_note_vs_scripts_tested", False, exp, "%s. FIX (orchestrator): replace the line with the 'Scripts tested:' line of pipeline/phone/PHONE-ROW.md" % listing(probs, 4))
    else:
        check("parity.card_language_note_vs_scripts_tested", True, exp, "tested %s on %s" % (",".join(st["scripts_tested"]), st["date_utc"]))


# ----------------------------------------------------------------------------------------------- parity: render built-in chain
@test("parity.render_builtin_chain_vs_chains_json")
def t_builtin_chain():
    js = "import('./pipeline/bin/render.mjs').then(m=>{process.stdout.write(JSON.stringify(m.BUILTIN_CHAINS))}).catch(e=>{process.stderr.write(String(e));process.exit(1)})"
    rc, out, err = sh(["node", "-e", js], timeout=60)
    exp = "pipeline/bin/render.mjs BUILTIN_CHAINS.h264 equals chains.json h264_venue in container, vf, video_args, expect, expect_extra and alpha; the built-in has no audio (a frames-only harness)"
    if rc != 0:
        return check("parity.render_builtin_chain_vs_chains_json", False, exp, "node could not import render.mjs: %s" % err[-200:])
    b = json.loads(out)["h264"]
    f = read_json(p("pipeline", "lib", "chains.json"))["chains"]["h264_venue"]
    diffs = [k for k in ("container", "vf", "video_args", "expect", "expect_extra", "alpha") if b.get(k) != f.get(k)]
    if b.get("audio_args"):
        diffs.append("audio_args (the built-in has audio arguments)")
    check("parity.render_builtin_chain_vs_chains_json", not diffs, exp,
          "equal in 6 fields; the built-in carries %d audio arguments" % len(b.get("audio_args") or []) if not diffs else "differs in %s" % diffs)


# ----------------------------------------------------------------------------------------------- parity: profiles and chains
def profile_chain_problems(profiles, chains, where):
    """Every profile that names a chain: the chain exists and what the chain promises (pix_fmt, colour tags, codec) is what the profile demands."""
    probs, n = [], 0
    for name, pr in profiles.items():
        cn = pr.get("chain")
        if not cn:
            continue
        n += 1
        ch = chains.get(cn)
        if ch is None:
            probs.append("%s: profile %s names chain %s, which does not exist" % (where, name, cn))
            continue
        ex, v = ch.get("expect") or {}, pr.get("video") or {}
        if ex.get("pix_fmt") and v.get("pix_fmt") and ex["pix_fmt"] not in v["pix_fmt"]:
            probs.append("%s: chain %s promises pix_fmt %s but profile %s wants %s" % (where, cn, ex["pix_fmt"], name, v["pix_fmt"]))
        for k in ("color_range", "color_space", "color_primaries", "color_transfer"):
            if ex.get(k) and v.get(k) and ex[k] not in v[k] and ex[k] != "unknown":
                probs.append("%s: chain %s promises %s=%s but profile %s wants %s" % (where, cn, k, ex[k], name, v[k]))
        if ex.get("codec") and v.get("codec") and ex["codec"] != v["codec"]:
            probs.append("%s: chain %s promises codec %s but profile %s wants %s" % (where, cn, ex["codec"], name, v["codec"]))
        ef = (ch.get("expect_extra") or {}).get("profile")
        if ef and v.get("profile") and ef not in v["profile"]:
            probs.append("%s: chain %s promises profile %s but profile %s wants %s" % (where, cn, ef, name, v["profile"]))
        if bool(ch.get("alpha")) != bool(v.get("alpha")):
            probs.append("%s: chain %s alpha=%s but profile %s alpha=%s" % (where, cn, ch.get("alpha"), name, v.get("alpha")))
    return probs, n


@test("parity.profiles_vs_chains")
def t_profiles_chains():
    st = read_json(p("pipeline", "settings.json"))
    ch = read_json(p("pipeline", "lib", "chains.json"))["chains"]
    ph = read_json(p("pipeline", "phone", "profile.json"))
    a, na = profile_chain_problems(st["profiles"], ch, "settings.json")
    b, nb = profile_chain_problems(ph["profiles"], ph["chains"], "phone/profile.json")
    unapproved = [n for n, c in ch.items() if not c.get("approved")] + [n for n, c in ph["chains"].items() if not c.get("approved")]
    check("parity.profiles_vs_chains", not (a + b) and na >= 5 and nb == 2,
          "every delivery profile of settings.json (5) and phone/profile.json (2) names a chain that exists and that promises the pix_fmt, codec, level class, alpha and BT.709 tags the profile demands",
          "%d settings profiles and %d phone profiles agree with their chains; chains not yet approved: %s" % (na, nb, ", ".join(unapproved) or "none") if not (a + b) else listing(a + b),
          note="phone_720_share stays unapproved until a maker's-PC ffmpeg build has been tested (W-16)")


# ----------------------------------------------------------------------------------------------- parity: pins
W22_RE = {"photocraft": r"PhotoCraft \*\*v?([0-9.]+)\*\*", "vectorcraft": r"VectorCraft \*\*v?([0-9.]+)\*\*", "lightcraft": r"LightCraft \*\*v?([0-9.]+)\*\*",
          "filmcraft": r"FilmCraft \*\*v?([0-9.]+)\*\*", "effectcraft": r"EffectCraft \*\*v?([0-9.]+)\*\*"}


def pin_problems(pins, assets, w22):
    probs = []
    ra = {}
    for r in assets["pins"]:
        ra.setdefault(r["app"], {})[r["role"]] = r["version"]
    for app, rx in W22_RE.items():
        m = re.search(rx, w22)
        reg = m.group(1) if m else None
        pj = pins["apps"].get(app, {}).get("pin")
        ar = ra.get(app, {}).get("pin")
        if not (reg and reg == pj == ar):
            probs.append("%s: W-22 says %s, win/pins.json says %s, release_assets.json says %s" % (app, reg, pj, ar))
    mf = re.search(r"fallback v?([0-9.]+)", w22)
    if not (mf and pins["apps"]["filmcraft"]["fallback"] == mf.group(1) == ra.get("filmcraft", {}).get("fallback")):
        probs.append("filmcraft fallback: W-22 %s, pins.json %s, release_assets.json %s" % (mf and mf.group(1), pins["apps"]["filmcraft"]["fallback"], ra.get("filmcraft", {}).get("fallback")))
    if "0.7.2" not in pins["apps"]["filmcraft"].get("retired", []):
        probs.append("filmcraft 0.7.2 (retired in W-22) is not in win/pins.json retired")
    if pins["apps"]["soundcraft"].get("pin") is not None or "soundcraft" in ra:
        probs.append("soundcraft must be unpinned and absent from the pins list (W-22, D-12)")
    return probs


@test("parity.pins_vs_release_assets_vs_w22")
def t_pins():
    pins = read_json(p("win", "pins.json"))
    assets = read_json(p("spikes", "sp1_craft_cli", "release_assets.json"))
    reg = read_text(p("DECISIONS.md"))
    m = re.search(r"^\| W-22 \|.*$", reg, re.M)
    probs = pin_problems(pins, assets, m.group(0) if m else "")
    check("parity.pins_vs_release_assets_vs_w22", not probs, "win/pins.json pins and fallback = spikes/sp1_craft_cli/release_assets.json versions = the W-22 row of DECISIONS.md (five pins, FilmCraft fallback 0.8.0 and 0.7.2 retired, SoundCraft unpinned)",
          "equal: " + ", ".join("%s %s" % (a, pins["apps"][a]["pin"]) for a in W22_RE) if not probs else listing(probs))


@test("parity.decisions_csv_vs_register")
def t_decisions_csv():
    rc, out, err = sh(PY + ["scripts/decisions_to_csv.py", "--check", "ops/decisions.csv"], timeout=60)
    last = [l for l in (out + err).strip().splitlines() if l.strip()]
    exp = "scripts/decisions_to_csv.py --check ops/decisions.csv exits 0 (every ID of DECISIONS.md is in the mirror, with the same title, value and status)"
    if rc == 0:
        return check("parity.decisions_csv_vs_register", True, exp, last[-1] if last else "exit 0")
    check("parity.decisions_csv_vs_register", False, exp, "exit %d: %s. FIX: python3 -I scripts/decisions_to_csv.py --write ops/decisions.csv (the mirror is generated, never hand-typed)" % (rc, listing(last[:-1][-3:] + last[-1:], 4)))


# ----------------------------------------------------------------------------------------------- parity: pc_report fields
class _TL(list):
    def __init__(self, items, path, seen):
        list.__init__(self, items)
        self._p, self._s = path, seen

    def __getitem__(self, i):
        v = list.__getitem__(self, i)
        return _wrap(v, self._p, self._s) if not isinstance(i, slice) else [_wrap(x, self._p, self._s) for x in v]

    def __iter__(self):
        for v in list.__iter__(self):
            yield _wrap(v, self._p, self._s)


class _TD(dict):
    def __init__(self, d, path, seen):
        dict.__init__(self, d)
        self._p, self._s = path, seen

    def _k(self, k):
        return (self._p + "." if self._p else "") + str(k)

    def __getitem__(self, k):
        self._s.add(self._k(k))
        return _wrap(dict.__getitem__(self, k), self._k(k), self._s)

    def get(self, k, default=None):
        self._s.add(self._k(k))
        return self[k] if dict.__contains__(self, k) else default

    def __contains__(self, k):
        self._s.add(self._k(k))
        return dict.__contains__(self, k)

    def items(self):
        for k in dict.keys(self):
            yield k, self[k]

    def values(self):
        for k in dict.keys(self):
            yield self[k]


def _wrap(v, path, seen):
    if isinstance(v, dict):
        return _TD(v, path, seen)
    if isinstance(v, list):
        return _TL(v, path + "[]", seen)
    return v


def schema_paths(schema, prefix=""):
    """Every property path of a JSON schema, with [] for array items."""
    out = set()
    props = schema.get("properties", {})
    for k, v in props.items():
        pth = (prefix + "." if prefix else "") + k
        out.add(pth)
        t = v.get("type")
        if v.get("type") == "array" or (isinstance(t, list) and "array" in t):
            out |= schema_paths(v.get("items", {}), pth + "[]")
        out |= schema_paths(v, pth) if v.get("properties") else set()
        if v.get("additionalProperties") and isinstance(v["additionalProperties"], dict):
            out.add(pth + ".*")
            out |= schema_paths(v["additionalProperties"], pth + ".*")
    return out


def norm_path(pth):
    return re.sub(r"\.\d+", "", pth)


@test("parity.pc_report_fields_in_schema")
def t_pc_fields():
    wc = load_module(p("scripts", "windows_check.py"), "windows_check_under_test")
    schema = read_json(p("win", "schema", "pc_report.schema.json"))
    tiers = read_json(p("win", "tiers.json"))
    pins = read_json(p("win", "pins.json"))
    allowed = schema_paths(schema)
    seen = set()
    ran = 0
    for fx in sorted(glob.glob(p("tests", "win", "fixtures", "report_*.json"))):
        try:
            rep = read_json(fx)
        except ValueError:
            continue
        errs = []
        wc.validate(rep, schema, schema, "", errs)
        if errs:
            continue
        tr = _wrap(rep, "", seen)
        try:
            a = wc.assess(tr, tiers, pins)
            if a.get("windows_report"):
                wc.print_table(tr, a, tiers, out=lambda *x, **k: None)
                wc.tier_file(tr, a, rep["generated_utc"][:10])
                wc.hardware_md(tr, a, tiers, rep["generated_utc"][:10])
            ran += 1
        except Exception as e:                                   # a fixture the tool cannot analyse is not this test's concern
            continue
    # the reads in main() that the functions above do not make
    src = read_text(p("scripts", "windows_check.py"))
    for m in re.finditer(r"""report\[["']([a-z_]+)["']\]""", src):
        seen.add(m.group(1))
    # fields the redaction file names (the scan reads them by name)
    pat = read_json(p("scripts", "redaction_patterns.json"))
    named = set(pat["name_checks"]["hardware_name_fields"])
    for fe in pat["field_exemptions"]:
        named |= set(fe["fields"])
    seen_n = set(seen)
    missing = sorted(s for s in seen_n if s not in allowed)
    named_missing = []
    for n in sorted(named):
        rx = re.compile("^" + re.escape(n).replace(r"\*", r"[^.\[\]]+") + "$")          # tools.*.version: any tool's version field
        if not any(rx.match(a) for a in allowed):
            named_missing.append(n)
    exp = "every pc_report field windows_check.py reads (traced on %d fixtures) is in win/schema/pc_report.schema.json; the fields scripts/redaction_patterns.json names are listed too" % ran
    check("parity.pc_report_fields_in_schema", ran >= 5 and not missing, exp,
          "%d fixtures traced, %d distinct fields read by windows_check.py, none outside the schema%s; %d fields named by scripts/redaction_patterns.json, %s" % (
              ran, len(seen_n), "" if not missing else " EXCEPT " + listing(missing), len(named),
              "all in the schema" if not named_missing else "NOTE (harmless, WP-03's file): %s names a field the schema does not have, so that exemption never applies" % listing(named_missing)),
          note="" if not named_missing else "dead field exemption in scripts/redaction_patterns.json: " + ", ".join(named_missing))


# ----------------------------------------------------------------------------------------------- parity: lj.ps1 close v0
def strip_ps(text):
    """The code of a PowerShell file with comments, here-strings and string literals removed (so a word in a message is not read as a command)."""
    t = re.sub(r"<#.*?#>", "", text, flags=re.S)
    t = re.sub(r"@'.*?'@", "''", t, flags=re.S)
    t = re.sub(r'@".*?"@', '""', t, flags=re.S)
    t = re.sub(r"'(?:[^']|'')*'", "''", t)
    t = re.sub(r'"(?:[^"`\n]|`.)*"', '""', t)
    return re.sub(r"(?m)#.*$", "", t)


# What a STATIC scan of the code (comments, here-strings and string literals already removed) can see. Short aliases (rd, md, iex ...) are matched in command position only, so a
# variable such as $rd is not a command. Commands invoked from a string or a variable (& 'Remove-Item' $x, $c = 'Remove-Item'; & $c $x) are NOT visible to any static scan:
# the behavioural tests in tests/win_lj/ (nothing changes, nothing is written, on fake trees) are what prove those absent.
CMD_POS = r"(?m)(?:^|[;|&{(=])\s*"
GIT_VERBS = r"(?:commit|push|add|rm|mv|reset|clean|checkout|restore|stash|tag|merge|rebase|pull|fetch|init|clone|apply|am|revert|cherry-pick)"
MUTATING = [r"\bRemove-Item\b", r"\bMove-Item\b", r"\bRename-Item\b", r"\bCopy-Item\b", r"\bNew-Item\b", r"\bSet-Content\b", r"\bAdd-Content\b", r"\bOut-File\b", r"\bClear-Content\b",
            r"\bSet-ItemProperty\b", r"\bRemove-ItemProperty\b", r"\bNew-ItemProperty\b", r"\bInvoke-WebRequest\b", r"\bInvoke-RestMethod\b", r"\bStart-BitsTransfer\b", r"\bSet-ExecutionPolicy\b",
            r"\b(?:Invoke-Expression|Start-Process|Tee-Object|Export-Csv|Export-Clixml|Compress-Archive|Expand-Archive)\b",
            CMD_POS + r"(?:sc|ri|rm|del|erase|mv|mi|cp|copy|move|ren|rni|rd|rmdir|md|mkdir|iex)\s+(?![=+*/]|-\s)",
            r"\[(?:System\.)?IO\.File\]::(?:Delete|Move|Copy|Replace|Write\w*|Append\w*|Create\w*|Open\w*)", r"\[(?:System\.)?IO\.Directory\]::(?:Delete|Move|Create\w*)",
            r"\.Delete\(", r"\.MoveTo\(", r"\.CopyTo\(", r"\.Create\(",
            r"(?:^|[\s&;(])git(?:\.exe)?(?:\s+-{1,2}[A-Za-z][\w-]*(?:=\S+)?(?:\s+[^\s-]\S*)?)*\s+" + GIT_VERBS + r"\b",
            r"(?<![<>|-])>{1,2}(?!>)(?![&=])\s*(?!\$null\b)\S"]                # file redirection ('x' > $f, $log >> $f); not 2>&1, not 2>$null
DANGER_SWITCH = ["apply", "commit", "includewindowsrecent", "push", "delete", "remove", "clean", "force", "backup", "yes", "confirm", "purge", "wipe", "overwrite"]


def lj_problems(text, repo_files_set):
    probs = []
    code = strip_ps(text)
    for rx in MUTATING:
        for m in re.finditer(rx, code, flags=re.M | re.I):
            line = code.count("\n", 0, m.start()) + 1
            probs.append("code line ~%d uses %r (a deleting, writing, committing, redirecting or downloading command)" % (line, m.group(0).strip()))
    opts = set()
    for m in re.finditer(r"\$(?:valueOpts|flagOpts)\s*=\s*@\(([^)]*)\)", text):
        opts |= set(re.findall(r"'([a-z]+)'", m.group(1)))
    if not opts:
        probs.append("could not find the option lists ($valueOpts / $flagOpts)")
    for o in sorted(opts):
        if any(d in o for d in DANGER_SWITCH):
            probs.append("a working option named %r exists (v0 has no deleting, committing or backup switch)" % o)
    refused = set(re.findall(r"'(apply|commit|includewindowsrecent)'", text))
    if refused != {"apply", "commit", "includewindowsrecent"}:
        probs.append("the refusal of -Apply, -Commit and -IncludeWindowsRecent is incomplete (found %s)" % sorted(refused))
    if "stale_check.py" not in text or "--new-only" not in text:
        probs.append("close does not call stale_check.py --new-only")
    if "public_lint.py" not in text:
        probs.append("close does not call public_lint.py")
    for name in sorted(set(re.findall(r"\b([A-Za-z0-9_]+\.(?:py|ps1|sh))\b", text))):
        if name == "lj.ps1":
            continue
        if not any(f.endswith("/" + name) or f == name for f in repo_files_set):
            probs.append("names a script that does not exist in the repo: %s" % name)
    return probs, sorted(opts)


@test("parity.lj_close_v0_names_and_switches")
def t_lj_static():
    text = read_text(p("win", "lj.ps1"))
    files = set(repo_files())
    probs, opts = lj_problems(text, files)
    check("parity.lj_close_v0_names_and_switches", not probs,
          "lj.ps1 calls stale_check.py --new-only and public_lint.py (current names), every script name it mentions exists, it defines no deleting, committing, writing or downloading option, and its code shows no mutating cmdlet, "
          "alias, file redirection or git verb to a static scan (string-invoked commands such as & 'Remove-Item' or & $c cannot be seen by a scan: the behavioural tests in tests/win_lj/ prove them absent)",
          "working options %s; the three v1 switches are refused; no mutating cmdlet, alias, redirection or git verb visible to the static scan (string-invoked commands are proved absent by tests/win_lj/, not by this scan)" % opts if not probs else listing(probs))


@test("parity.lj_close_v0_refusals_and_help")
def t_lj_dynamic():
    exp = "pwsh win/lj.ps1 close -Apply / -Commit / -IncludeWindowsRecent each exit 2 with 'not in v0 ... nothing was done' and 'files written: none'; help says DRY RUN ONLY"
    if not os.path.isfile(PWSH):
        return record("parity.lj_close_v0_refusals_and_help", "UNVERIFIED", exp, "PowerShell 7 is not installed in the scratch folder (win/tools/fetch_pwsh.sh); only the static checks ran", "pwsh missing: the dynamic refusal check did not run")
    probs = []
    for sw in ("-Apply", "-Commit", "-IncludeWindowsRecent"):
        rc, out, err = sh([PWSH, "-NoProfile", "-NonInteractive", "-File", "win/lj.ps1", "close", sw], timeout=60)
        if rc != 2 or "not in v0" not in out or "nothing was done" not in out or "files written: none" not in out:
            probs.append("%s: exit %d, output %r" % (sw, rc, clean(out)[:80]))
    rc, out, err = sh([PWSH, "-NoProfile", "-NonInteractive", "-File", "win/lj.ps1", "help"], timeout=60)
    if rc != 0 or "DRY RUN ONLY" not in out:
        probs.append("help: exit %d, no 'DRY RUN ONLY'" % rc)
    check("parity.lj_close_v0_refusals_and_help", not probs, exp, "PowerShell 7.5.4 on Linux: 3 refusals exit 2, help says dry run only" if not probs else listing(probs),
          unverified="Windows PowerShell 5.1 behaviour of lj.ps1 is UNVERIFIED until the maker's PC runs it")


# ----------------------------------------------------------------------------------------------- parity: fonts and scripts tested
def noto_problems(strings, libs):
    probs, ok = [], []
    for name, blk in strings["scripts"].items():
        if not (blk.get("strings") or []):
            continue
        fonts = [f for f in libs["fonts"] if name in f.get("scripts", []) and f.get("role") == "script_family"]
        fam = blk.get("noto_family")
        if not fonts:
            probs.append("script %r has test strings but no script_family font in libs.lock.json" % name)
            continue
        f = fonts[0]
        if not f["family"].startswith("Noto"):
            probs.append("script %r: the family is %r, not a Noto family" % (name, f["family"]))
        if fam and fam != f["family"]:
            probs.append("script %r: test_strings.json names %r, libs.lock.json has %r" % (name, fam, f["family"]))
        if f.get("status") != "day1" or not f.get("version"):
            probs.append("script %r: the font entry is not fetched (status %r, version %r)" % (name, f.get("status"), f.get("version")))
        ok.append("%s=%s" % (name, f["family"]))
    return probs, ok


@test("parity.noto_family_per_script_with_strings")
def t_noto():
    strings = read_json(p("pipeline", "phone", "test_strings.json"))
    libs = read_json(p("pipeline", "lib", "libs.lock.json"))
    probs, ok = noto_problems(strings, libs)
    pend = [n for n, b in strings["scripts"].items() if not (b.get("strings") or [])]
    check("parity.noto_family_per_script_with_strings", not probs and len(ok) >= 2, "every script with strings in test_strings.json has a fetched Noto family in libs.lock.json that matches test_strings.json",
          "%s; %d scripts without strings are pending (%s)" % (", ".join(ok), len(pend), ",".join(pend)) if not probs else listing(probs))


def scripts_line(text):
    m = re.search(r"Scripts tested: ([a-z, ]+?) \(neutral strings\) on (\d{4}-\d{2}-\d{2}); NOT TESTED: ([a-z, ]+?) \(", text)
    return None if not m else ([s.strip() for s in m.group(1).split(",")], m.group(2), [s.strip() for s in m.group(3).split(",")])


@test("parity.phone_row_scripts_tested_vs_json")
def t_scripts_tested():
    st = read_json(p("build", "evidence", "wp08", "scripts_tested.json"))
    strings = read_json(p("pipeline", "phone", "test_strings.json"))
    got = scripts_line(read_text(p("pipeline", "phone", "PHONE-ROW.md")))
    exp = "the 'Scripts tested:' line of PHONE-ROW.md = scripts_tested.json (tested, not tested, date) = the scripts that have strings in test_strings.json"
    if not got:
        return check("parity.phone_row_scripts_tested_vs_json", False, exp, "no parsable 'Scripts tested:' line in PHONE-ROW.md")
    tested, date, nt = got
    with_strings = [n for n, b in strings["scripts"].items() if (b.get("strings") or [])]
    probs = []
    if tested != st["scripts_tested"]:
        probs.append("PHONE-ROW tested %s, scripts_tested.json %s" % (tested, st["scripts_tested"]))
    if nt != st["scripts_not_tested"]:
        probs.append("PHONE-ROW not tested %s, scripts_tested.json %s" % (nt, st["scripts_not_tested"]))
    if date != st["date_utc"]:
        probs.append("PHONE-ROW date %s, scripts_tested.json %s" % (date, st["date_utc"]))
    if sorted(tested) != sorted(with_strings):
        probs.append("tested %s but test_strings.json has strings for %s" % (tested, with_strings))
    check("parity.phone_row_scripts_tested_vs_json", not probs, exp, "tested %s on %s; NOT TESTED %s" % (",".join(tested), date, ",".join(nt)) if not probs else listing(probs))


# ----------------------------------------------------------------------------------------------- redaction
@test("redaction.self_test_zero_skipped_consumers")
def t_selftest():
    rc, out, err = sh(PY + ["scripts/public_lint.py", "--self-test", "--fail-on-skip"], timeout=300)
    cons = re.findall(r"^consumer (\S+): ok", out, flags=re.M)
    want = ["scripts/public_lint.py", "scripts/windows_check.py", "win/step0_pc_tests.ps1", "win/kit2/run_checks_pc.ps1"]
    skipped = re.findall(r"SKIPPED[^\n]*", out)
    ok = rc == 0 and cons == want and not skipped and "no disagreement" in out
    check("redaction.self_test_zero_skipped_consumers", ok, "public_lint.py --self-test --fail-on-skip: exit 0, all four consumers ok, no SKIPPED, no disagreement",
          "exit %d; consumers ok: %s; skipped: %s" % (rc, cons, skipped or "none"))
    S["selftest_out"] = out
    n = re.search(r"(\d+) samples", out)
    record("redaction.consumers_on_windows_powershell_5_1", "UNVERIFIED", "win/step0_pc_tests.ps1 and win/kit2/run_checks_pc.ps1 agree with the other consumers on Windows PowerShell 5.1",
           "the self-test ran those two consumers on PowerShell 7.5.4 on Linux (%s samples); Windows PowerShell 5.1 can not run here" % (n.group(1) if n else "?"),
           unverified="Windows PowerShell 5.1 consumers of the pattern file: UNVERIFIED until the maker's PC runs -PatternSelfTest")


def deny_globs():
    pat = read_json(p("scripts", "redaction_patterns.json"))
    cfg = read_json(p("scripts", "public_lint.config.json"))
    return pat["path_denylist"], pat.get("path_denylist_exempt_dirs", []), cfg.get("denylist_exempt_globs", [])


def denylist_hits(root, globs, exempt, exempt_globs=()):
    hits = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules")]
        for f in fn:
            full = os.path.join(dp, f)
            rp = os.path.relpath(full, root).replace(os.sep, "/")
            if any(rp == e.rstrip("/") or rp.startswith(e.rstrip("/") + "/") for e in exempt):
                continue
            if any(fnmatch.fnmatch(f, eg.split("/")[-1]) for eg in exempt_globs):          # **/*.schema.json: a schema describes a report and holds no data
                continue
            for g in globs:
                base = g.split("/")[-1]
                if fnmatch.fnmatch(f, base):
                    hits.append(rp)
                    break
    return sorted(hits)


@test("redaction.path_denylist")
def t_denylist():
    globs, exempt, eg = deny_globs()
    hits = denylist_hits(ROOT, globs, exempt, eg)
    check("redaction.path_denylist", not hits, "no file in the repo tree (ignored folders included) outside %s (and not a *.schema.json, which describes a report and holds no data) matches %s" % (exempt, globs),
          "none found (%s scanned)" % ", ".join(globs) if not hits else "file names matching the denylist: %s" % listing(hits))


def fixture_secrets():
    """The GPU, CPU, driver and Vulkan device strings of the synthetic fixtures (anything of 5+ characters)."""
    out = set()
    for fx in glob.glob(p("tests", "win", "fixtures", "report_*.json")):
        try:
            r = read_json(fx)
        except ValueError:
            continue
        vals = [(r.get("cpu") or {}).get("name")]
        for g in r.get("gpus") or []:
            vals += [g.get("name"), g.get("driver_version")]
        for d in (r.get("vulkan") or {}).get("devices") or []:
            vals.append(d if isinstance(d, str) else (d or {}).get("name"))
        for v in vals:
            if isinstance(v, str) and len(v.strip()) >= 5:
                out.add(v.strip())
    return sorted(out)


def schema_errors(inst, schema):
    wc = S.get("wc") or load_module(p("scripts", "windows_check.py"), "windows_check_under_test")
    S["wc"] = wc
    errs = []
    wc.validate(inst, schema, schema, "", errs)
    return errs


def pc_dir_problems(pc_dir, secrets):
    tier_schema = read_json(p("win", "schema", "pc_tier.schema.json"))
    chain_schema = read_json(p("pipeline", "validators", "pc_chains.schema.json"))
    probs, seen = [], []
    if not os.path.isdir(pc_dir):
        return ["build/evidence/pc/ does not exist"], seen
    for f in sorted(os.listdir(pc_dir)):
        full = os.path.join(pc_dir, f)
        if not os.path.isfile(full):
            continue
        seen.append(f)
        txt = read_text(full)
        for s in secrets:
            if s in txt:
                probs.append("%s contains a fixture GPU/CPU/driver string (%s...)" % (f, s[:2]))
        if f.endswith(".json"):
            try:
                d = json.loads(txt)
            except ValueError:
                probs.append("%s is not valid JSON" % f)
                continue
            if re.match(r"pc_tier.*\.json$", f):
                schema = tier_schema
            elif re.match(r"pc_chains.*\.json$", f):
                schema = chain_schema
            else:
                probs.append("%s is not a derived file name (pc_tier*.json or pc_chains*.json)" % f)
                continue
            for pth, why in schema_errors(d, schema)[:3]:
                probs.append("%s: %s %s" % (f, pth, why))
        elif not f.lower().endswith((".md", ".txt")):
            probs.append("%s: only derived .json, .md and .txt files may be filed here" % f)
    return probs, seen


@test("redaction.pc_evidence_folder")
def t_pc_folder():
    secrets = fixture_secrets()
    probs, seen = pc_dir_problems(p("build", "evidence", "pc"), secrets)
    check("redaction.pc_evidence_folder", not probs and len(secrets) >= 5, "every file under build/evidence/pc/ is a derived pc_tier*.json or pc_chains*.json that validates against its schema, and none holds a GPU, CPU or driver string of the %d synthetic fixture strings checked" % len(secrets),
          "%d file(s) in the folder (%s); %s; %d fixture strings checked; %s" % (len(seen), ", ".join(seen) or "none", "no derived file has been filed yet: the orchestrator files into it after the maker's first paste" if not [x for x in seen if x.endswith(".json")] else "derived files present", len(secrets), "no problem" if not probs else listing(probs)))


@test("redaction.derivation_tools_leak_nothing")
def t_derive():
    secrets = fixture_secrets()
    tmp = tempfile.mkdtemp(prefix="wp11b-derive.", dir=SCRATCH if os.path.isdir(SCRATCH) else None)
    probs, n = [], 0
    try:
        tier_schema = read_json(p("win", "schema", "pc_tier.schema.json"))
        for fx in sorted(glob.glob(p("tests", "win", "fixtures", "report_*.json"))):
            out = os.path.join(tmp, "tier_%s.json" % os.path.basename(fx)[:-5])
            rc, so, se = sh(PY + ["scripts/windows_check.py", "--tier-json-out", out, fx], timeout=60)
            if not os.path.isfile(out):
                continue                                             # a fixture the checker refuses or calls not-Windows writes nothing: right
            n += 1
            txt = read_text(out)
            errs = schema_errors(json.loads(txt), tier_schema)
            if errs:
                probs.append("%s: %s" % (os.path.basename(fx), errs[0]))
            for s in secrets:
                if s in txt:
                    probs.append("%s leaked %s..." % (os.path.basename(out), s[:2]))
        # colour-patch: a raw file with a planted configure flag containing a profile path and a user name must derive to a file with neither
        raw = os.path.join(tmp, "colour_patch_raw.json")
        rc, so, se = sh(PY + ["pipeline/validators/colour_patch.py", "--ffmpeg", "ffmpeg", "--chain-file", "pipeline/lib/chains.json", "--chain", "h264_venue", "--json", raw], timeout=300)
        derived = os.path.join(tmp, "derived.json")
        if rc in (0, 1) and os.path.isfile(raw):
            d = json.loads(read_text(raw))
            planted = "--prefix=/ho" + "me/zzplanted/ffmpeg-build"
            blob = json.dumps(d)
            if "configure" not in blob:
                probs.append("the raw colour-patch file has no configure field to plant into")
            else:
                def plant(o):
                    if isinstance(o, dict):
                        for k in list(o):
                            if "configure" in k.lower():
                                o[k] = (o[k] + " " + planted) if isinstance(o[k], str) else (list(o[k]) + [planted])
                            else:
                                plant(o[k])
                    elif isinstance(o, list):
                        for x in o:
                            plant(x)
                plant(d)
                with open(raw, "w", encoding="utf-8") as f:
                    json.dump(d, f)
                rc2, so2, se2 = sh(PY + ["pipeline/validators/colour_patch.py", "--derive-from", raw, "--out", derived], timeout=60)
                if rc2 != 0 or not os.path.isfile(derived):
                    probs.append("--derive-from failed: exit %d %s" % (rc2, clean(so2 + se2)[:120]))
                else:
                    dt = read_text(derived)
                    if "zzplanted" in dt or "configure" in dt.lower() or "/home/" in dt:
                        probs.append("the derived colour-patch file kept the planted configure flag, a path or a name")
                    for pth, why in schema_errors(json.loads(dt), read_json(p("pipeline", "validators", "pc_chains.schema.json")))[:2]:
                        probs.append("derived chains: %s %s" % (pth, why))
        else:
            probs.append("colour_patch.py could not make a raw file (exit %d)" % rc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check("redaction.derivation_tools_leak_nothing", not probs and n >= 8,
          "windows_check.py --tier-json-out on every synthetic fixture yields schema-valid files with no GPU, CPU or driver string; colour_patch.py --derive-from drops a planted configure flag with a path and a name",
          "%d tier files derived and checked against %d fixture strings; chains derivation clean" % (n, len(secrets)) if not probs else listing(probs))


@test("redaction.no_raw_report_shapes_in_evidence")
def t_raw_shapes():
    bad = []
    for f in glob.glob(p("build", "evidence", "**", "*.json"), recursive=True) + glob.glob(p("build", "evidence", "**", "*.jsonl"), recursive=True):
        try:
            txt = read_text(f)
        except OSError:
            continue
        if re.search(r'"(?:gpus|vulkan)"\s*:\s*[\[{]', txt) and re.search(r'"(?:cpu|powershell)"\s*:\s*\{', txt):
            bad.append(rel(f))
        if re.search(r'"configure(?:_flags)?"\s*:', txt) and "lj-pc-chains" not in txt:
            bad.append(rel(f) + " (configure flags)")
    check("redaction.no_raw_report_shapes_in_evidence", not bad, "no file under build/evidence/ has the shape of a raw pc_report.json (gpus + cpu + powershell) or a raw colour-patch file (configure flags)",
          "none found" if not bad else "raw shapes: %s" % listing(bad))


@test("redaction.gitignore_backstop_for_raw_reports")
def t_gitignore():
    names = ["pc_report.json", "pc_report_local.json", "colour_patch_pc.json", "maker-pc.json", "scripts/public_lint.deny.local.txt"]
    rc, out, err = git("check-ignore", "--no-index", "-v", *names)
    ignored = {l.split("\t")[-1] for l in out.splitlines() if "\t" in l}
    miss = [n for n in names if n not in ignored]
    check("redaction.gitignore_backstop_for_raw_reports", not miss, ".gitignore ignores pc_report*.json, colour_patch_pc*.json, maker-pc*.json and the local deny list (the Q-3 backstop of the build plan; public_lint also refuses these names by path)",
          "all %d sample names ignored" % len(names) if not miss else "not ignored: %s. FIX (orchestrator, Q-3): add `pc_report*.json`, `colour_patch_pc*.json`, `maker-pc*.json`, `*.local.*` and `logs/` to .gitignore" % ", ".join(miss))


# ----------------------------------------------------------------------------------------------- disk: from the evidence envelopes
def all_envelopes():
    """Every lj-evidence/1 object under build/evidence (json and jsonl). Returns [(relpath, obj)]."""
    rows = []
    for f in sorted(glob.glob(p("build", "evidence", "**", "*.json*"), recursive=True)):
        if not f.endswith((".json", ".jsonl")) or os.path.basename(f).endswith("_only.jsonl"):             # a partial (--only) development run is never evidence
            continue
        try:
            txt = read_text(f)
        except OSError:
            continue
        objs = []
        if f.endswith(".jsonl"):
            for line in txt.splitlines():
                try:
                    objs.append(json.loads(line))
                except ValueError:
                    pass
        else:
            try:
                objs = [json.loads(txt)]
            except ValueError:
                pass
        for o in objs:
            if isinstance(o, dict) and o.get("schema") == "lj-evidence/1":
                rows.append((rel(f), o))
    return rows


PLAN_FLOOR_MB, PLAN_HARD_FLOOR_MB = 400, 250                      # the plan's rule (build plan 4.9, lj_with_disk): start minus planned write at or above 400 MB, minimum never below 250 MB


def floor_of(d, key, plan):
    """The floor an envelope is held to: its own figure if that is higher, never lower than the plan's. An envelope cannot lower the plan's floors."""
    v = d.get(key, plan)
    return max(v, plan) if isinstance(v, (int, float)) and not isinstance(v, bool) else plan


def budget_problems(rows, big_mb=100):
    probs, n_big = [], 0
    for path, o in rows:
        d = o.get("disk") or {}
        pl = d.get("planned_write_mb") or 0
        if pl > big_mb:
            n_big += 1
            s, mn = d.get("avail_mb_start"), d.get("avail_mb_min")
            fl, hf = floor_of(d, "floor_mb", PLAN_FLOOR_MB), floor_of(d, "hard_floor_mb", PLAN_HARD_FLOOR_MB)
            if s is None or s - pl < fl:
                probs.append("%s %s (%s): avail_mb_start %s - planned %s = %s, below %s" % (o.get("package"), o.get("test"), path, s, pl, None if s is None else s - pl, fl))
            if mn is None or mn < hf:
                probs.append("%s %s (%s): avail_mb_min %s is below the %s MB hard floor" % (o.get("package"), o.get("test"), path, mn, hf))
    return probs, n_big


@test("disk.stage_budget_rule_from_envelopes")
def t_budget():
    rows = all_envelopes()
    probs, n_big = budget_problems(rows)
    S["envelopes"] = rows
    check("disk.stage_budget_rule_from_envelopes", not probs and n_big >= 5, "every envelope with planned_write_mb above 100 has avail_mb_start - planned >= 400 and avail_mb_min >= 250",
          "%d envelopes read; %d stages with planned_write_mb above 100, all within the rule" % (len(rows), n_big) if not probs else listing(probs))


@test("disk.every_envelope_carries_df_figures")
def t_disk_object():
    rows = S.get("envelopes") or all_envelopes()
    keys = ("avail_mb_start", "planned_write_mb", "avail_mb_min", "avail_mb_end")
    bad = []
    for path, o in rows:
        d = o.get("disk")
        if not isinstance(d, dict) or any(not isinstance(d.get(k), (int, float)) for k in keys):
            bad.append("%s %s (%s)" % (o.get("package"), o.get("test"), path))
        elif d["avail_mb_min"] > min(d["avail_mb_start"], d["avail_mb_end"]) + 2:
            bad.append("%s %s: avail_mb_min %s is above both start %s and end %s" % (o.get("package"), o.get("test"), d["avail_mb_min"], d["avail_mb_start"], d["avail_mb_end"]))
    pk = sorted({o.get("package") for _, o in rows})
    check("disk.every_envelope_carries_df_figures", not bad, "every lj-evidence/1 envelope has a disk object with avail_mb_start, planned_write_mb, avail_mb_min and avail_mb_end (build plan 4.2)",
          "%d envelopes from %d packages (%s) all carry the four figures" % (len(rows), len(pk), ",".join(pk)) if not bad else listing(bad))


def crossing_problems(rows, exceptions):
    ex = {(e["package"], e["test"]) for e in exceptions}
    seen, probs = [], []
    for path, o in rows:
        d = o.get("disk") or {}
        mn = d.get("avail_mb_min")
        if isinstance(mn, (int, float)) and mn < floor_of(d, "hard_floor_mb", PLAN_HARD_FLOOR_MB):
            key = (o.get("package"), o.get("test"))
            seen.append(key)
            if key not in ex:
                probs.append("%s %s (%s): avail_mb_min %s is under the 250 MB hard floor and is not on the reviewed exceptions list" % (key[0], key[1], path, mn))
    return probs, sorted(set(seen))


@test("disk.hard_floor_crossings_are_explained")
def t_crossings():
    rows = S.get("envelopes") or all_envelopes()
    exc = read_json(p("tests", "integration", "disk_exceptions.json"))["exceptions"]
    probs, seen = crossing_problems(rows, exc)
    stale = [e for e in exc if (e["package"], e["test"]) not in set(seen)]
    if stale:
        probs.append("exceptions that no envelope needs any more (remove them): %s" % listing(["%s %s" % (e["package"], e["test"]) for e in stale]))
    check("disk.hard_floor_crossings_are_explained", not probs, "an envelope whose avail_mb_min is under the 250 MB hard floor is on the reviewed list tests/integration/disk_exceptions.json with a reason (the volume is shared; a stage with planned_write_mb 0 can see another job's writes)",
          "%d crossing(s), all listed with a reason: %s" % (len(seen), listing(["%s %s" % k for k in seen])) if not probs else listing(probs))


@test("disk.each_tarball_downloaded_once")
def t_ledger():
    rc, out, err = sh(PY + ["spikes/sp1b_readback/check_ledger.py"], timeout=60)
    ok_line = "each fetched once or with a recorded exception: OK" in out
    # independent recount of the two download ledgers
    fetches = {}
    for f in (p("build", "evidence", "wp07", "download_ledger.jsonl"), p("build", "evidence", "wp10", "download_ledger.jsonl")):
        if os.path.isfile(f):
            for line in read_text(f).splitlines():
                if line.strip():
                    r = json.loads(line)
                    fetches.setdefault(r["asset"], []).append(r)
    twice = {a: [(r.get("fetch"), r.get("exception")) for r in v] for a, v in fetches.items() if len(v) > 1}
    unexplained = {a: v for a, v in twice.items() if any(not e for _, e in v[1:])}
    sound = [a for a in fetches if a.startswith("soundcraft")]
    total = sum(r["bytes"] for v in fetches.values() for r in v)
    S["ledger_total_bytes"] = total
    S["ledger_assets"] = len(fetches)
    first = (out.strip().splitlines() or [""])[0]
    check("disk.each_tarball_downloaded_once", rc == 0 and ok_line and not unexplained and not sound and len(fetches) == 5,
          "check_ledger.py exits 0 and an independent recount of the WP-07 and WP-10 download ledgers shows each of the five pinned Craft tarballs fetched once (any second fetch carries a recorded exception) and no SoundCraft file",
          "check_ledger exit %d: %s; recount: %d tarballs, %d with a second fetch (all explained: %s), %.1f MB in total" % (rc, first[:170], len(fetches), len(twice), not unexplained, total / 1e6))


def pwsh_tarball_bytes():
    """The PowerShell tarball size, read from evidence instead of typed here. build/evidence/wp01a/fetch_pwsh_guarded.json is the guarded fetch's envelope; it holds the df figures
    (planned 275 MB) but no byte count, so the size is the measured line ('size N bytes') of the transcript written by that same run, checked against EXPECT_SIZE of
    win/tools/fetch_pwsh.sh. Returns (bytes or None, source text, problems)."""
    probs = []
    env = p("build", "evidence", "wp01a", "fetch_pwsh_guarded.json")
    run = p("build", "evidence", "wp01a", "fetch_pwsh_guarded_run.txt")
    sh_path = p("win", "tools", "fetch_pwsh.sh")
    try:
        e = read_json(env)
        if e.get("status") != "PASS" or e.get("package") != "WP-01a":
            probs.append("build/evidence/wp01a/fetch_pwsh_guarded.json is not a PASS envelope of WP-01a (status %r)" % e.get("status"))
    except (OSError, ValueError) as ex:
        probs.append("build/evidence/wp01a/fetch_pwsh_guarded.json cannot be read (%s)" % type(ex).__name__)
    measured = expected = None
    try:
        m = re.search(r"(?m)^\s*size (\d+) bytes\s*$", read_text(run))
        measured = int(m.group(1)) if m else None
    except OSError:
        pass
    try:
        m = re.search(r"(?m)^EXPECT_SIZE=(\d+)\s*$", read_text(sh_path))
        expected = int(m.group(1)) if m else None
    except OSError:
        pass
    if measured is None:
        probs.append("build/evidence/wp01a/fetch_pwsh_guarded_run.txt has no 'size N bytes' line")
    if expected is None:
        probs.append("win/tools/fetch_pwsh.sh has no EXPECT_SIZE line")
    if measured is not None and expected is not None and measured != expected:
        probs.append("the fetch measured %d bytes but win/tools/fetch_pwsh.sh expects %d" % (measured, expected))
    return measured, "measured size in build/evidence/wp01a/fetch_pwsh_guarded_run.txt (envelope fetch_pwsh_guarded.json), equal to EXPECT_SIZE of win/tools/fetch_pwsh.sh", probs


@test("disk.downloads_under_2gb_allowance")
def t_allowance():
    total = S.get("ledger_total_bytes")
    if total is None:
        total = 0
        for f in (p("build", "evidence", "wp07", "download_ledger.jsonl"), p("build", "evidence", "wp10", "download_ledger.jsonl")):
            if os.path.isfile(f):
                total += sum(json.loads(l)["bytes"] for l in read_text(f).splitlines() if l.strip())
    pwsh, src, pprobs = pwsh_tarball_bytes()
    libs = read_json(p("pipeline", "lib", "libs.lock.json"))
    npm = sum((x.get("tarball") or {}).get("bytes", 0) for x in libs["libs"] + libs["fonts"])
    wheel = 1_000_000                                               # the OTIO wheel (about 0.8 MB)
    exp = "the Craft tarballs (ledgers) + PowerShell (its size read from the guarded fetch's evidence) + the npm packs of libs.lock.json + the OTIO wheel stay under the 2 GB allowance"
    if pwsh is None or pprobs:
        return check("disk.downloads_under_2gb_allowance", False, exp, "the PowerShell tarball size could not be taken from evidence: %s" % listing(pprobs, 3))
    grand = total + pwsh + npm + wheel
    check("disk.downloads_under_2gb_allowance", grand < 2 * 1024 ** 3, exp,
          "%.0f MB Craft + %.1f MB PowerShell (%d bytes, from the fetch evidence) + %.0f MB npm packs + about 1 MB wheel = %.0f MB of 2048 MB" % (total / 1e6, pwsh / 1e6, pwsh, npm / 1e6, grand / 1e6))


def parse_cleanup(out):
    free = re.search(r"total that --yes would free: ([0-9.]+) MB in (\d+) item", out)
    before = re.search(r"df before: Avail (\d+) MB", out)
    return (float(free.group(1)) if free else None, int(free.group(2)) if free else None, int(before.group(1)) if before else None)


@test("disk.cleanup_scratch_dry_run_and_df")
def t_cleanup_dry():
    def tree_sig():
        sig = []
        for root in (os.path.join(SCRATCH, "pwsh"), os.path.join(SCRATCH, "venv-otio"), p("vendor", "craft"), p("vendor", "craft-sp1b"), p("renders")):
            tot = 0
            for dp, dn, fn in os.walk(root):
                for f in fn:
                    try:
                        tot += os.lstat(os.path.join(dp, f)).st_size
                    except OSError:
                        pass
            sig.append(tot)
        return sig
    s0 = tree_sig()
    a0 = avail_mb()
    rc, out, err = sh(["bash", "scripts/cleanup_scratch.sh"], timeout=120)
    free, items, before = parse_cleanup(out)
    s1 = tree_sig()
    ok = rc == 0 and free is not None and "Dry run: nothing was deleted" in out and s0 == s1
    S["cleanup_free_mb"], S["cleanup_items"] = free, items
    proj = (a0 + free) if free is not None else None
    check("disk.cleanup_scratch_dry_run_and_df", ok, "scripts/cleanup_scratch.sh (dry run, the default) lists what --yes would free, deletes nothing (sizes of the listed trees unchanged), and df is reported",
          "exit %d; df now Avail %s MB; --yes would free %s MB in %s item(s), so Avail would be about %s MB; the trees were unchanged: %s. The real --yes is NOT run here: it would delete the PowerShell used by the Windows-script tests (see LJ_INTEGRATION_REAL_CLEANUP)" % (rc, a0, free, items, None if proj is None else int(proj), s0 == s1))


@test("disk.cleanup_scratch_yes_reports_df_after")
def t_cleanup_yes():
    tmp = tempfile.mkdtemp(prefix="wp11b-cleanup.", dir=SCRATCH if os.path.isdir(SCRATCH) else None)
    try:
        scratch = os.path.join(tmp, "fake-scratch")
        root = os.path.join(tmp, "fake-repo")
        for d in ("pwsh", "venv-x", "keep-me"):
            os.makedirs(os.path.join(scratch, d))
        os.makedirs(os.path.join(root, "vendor", "craft"))
        os.makedirs(os.path.join(root, "vendor", "js"))
        os.makedirs(os.path.join(root, "renders", "wp99"))
        os.makedirs(os.path.join(root, "renders", "final"))
        with open(os.path.join(scratch, "venv-x", "pyvenv.cfg"), "w") as f:
            f.write("home = x\n")
        sizes = {"pwsh/blob": 12, "venv-x/blob": 6, "keep-me/blob": 3}
        for k, mb in sizes.items():
            with open(os.path.join(scratch, k), "wb") as f:
                f.write(b"\0" * (mb * 1024 * 1024))
        for k, mb in {"vendor/craft/blob": 8, "vendor/js/lib.js": 1, "renders/wp99/blob": 5, "renders/final/keep": 1}.items():
            with open(os.path.join(root, k), "wb") as f:
                f.write(b"\0" * (mb * 1024 * 1024))
        rc, out, err = sh(["bash", "scripts/cleanup_scratch.sh", "--yes", "--scratch", scratch, "--root", root], timeout=120)
        gone = [x for x in (os.path.join(scratch, "pwsh"), os.path.join(scratch, "venv-x"), os.path.join(root, "vendor", "craft"), os.path.join(root, "renders", "wp99")) if not os.path.exists(x)]
        kept = [x for x in (os.path.join(scratch, "keep-me", "blob"), os.path.join(root, "vendor", "js", "lib.js"), os.path.join(root, "renders", "final", "keep")) if os.path.exists(x)]
        b = re.search(r"df before: Avail (\d+) MB", out)
        a = re.search(r"df after:\s*Avail (\d+) MB", out)
        m = re.search(r"free space: (\d+) MB before, (\d+) MB after", out)
        ok = rc == 0 and len(gone) == 4 and len(kept) == 3 and (m is not None or (a is not None and b is not None))
        figs = ("before %s MB, after %s MB" % (m.group(1), m.group(2))) if m else ("before %s, after %s" % (b and b.group(1), a and a.group(1)))
        check("disk.cleanup_scratch_yes_reports_df_after", ok, "cleanup_scratch.sh --yes on a faithful fake tree (about 36 MB: pwsh, a venv, vendor/craft, renders/wp99 listed; vendor/js, renders/final and another scratch folder kept) removes exactly the listed items and prints df before and after",
              "exit %d; 4 of 4 listed items removed, 3 of 3 kept items intact; df %s; no absolute path in the output: %s" % (rc, figs, ROOT not in out and SCRATCH not in out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------------------------- hygiene
def parse_stale(out):
    hits = []
    for l in out.splitlines():
        m = re.match(r"NEW (FAIL|WARN) (\S+?):(\d+) \[([^\]]+)\]", l)
        if m:
            hits.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
    return hits


@test("hygiene.stale_check_new_only")
def t_stale():
    rc, out, err = sh(PY + ["scripts/stale_check.py", "--new-only"], timeout=300)
    hits = parse_stale(out)
    S["stale_hits"] = hits
    fails = [h for h in hits if h[0] == "FAIL"]
    by_area = {}
    for h in hits:
        by_area.setdefault(h[1].split("/")[0] if h[1].split("/")[0] != ".claude" else ".claude/skills", []).append(h)
    build_hits = [h for h in hits if in_roots(h[1])]
    summ = (out.strip().splitlines() or [""])[-1]
    if rc == 0:
        return check("hygiene.stale_check_new_only", True, "stale_check.py --new-only exits 0 (the build introduced no new stale value)", summ)
    check("hygiene.stale_check_new_only", False, "stale_check.py --new-only exits 0 (the build introduced no new stale value)",
          "exit %d: %s. By area: %s. In the build's own folders (WP owners): %s. FIX: the Haiku scribe passes / orchestrator for .claude, playbooks and research hits; the owners for scripts hits (the retired-ID examples in comments), then re-cut the baseline with stale_check.py --baseline" % (
              rc, summ, ", ".join("%s %d" % (k, len(v)) for k, v in sorted(by_area.items())), listing(["%s:%d [%s]" % (h[1], h[2], h[3]) for h in build_hits]) or "none"))


@test("hygiene.public_lint_over_the_diff")
def t_lint_diff():
    rc, out, err = sh(PY + ["scripts/public_lint.py"], timeout=300)
    summ = [l for l in out.splitlines() if l.startswith("public_lint:")]
    findings = [l for l in out.splitlines() if l.startswith("FINDING")]
    cats = sorted({l.split()[2] for l in findings})
    files = sorted({l.split()[3] if len(l.split()) > 3 else "?" for l in findings})
    # `--diff` is not a flag of scripts/public_lint.py: its default mode IS the diff against HEAD plus untracked files
    check("hygiene.public_lint_over_the_diff", rc == 0, "public_lint.py (its default mode: added lines of the diff against HEAD plus untracked files; the plan's '--diff' spelling does not exist) exits 0",
          "exit %d: %s%s" % (rc, summ[-1] if summ else "no summary", "" if rc == 0 else "; %d finding(s) in %s: %s.%s" % (len(findings), listing(files, 4), ",".join(cats), " FIX (orchestrator): these are tracked __pycache__ files that predate the build; run git rm --cached on them" if all("__pycache__" in x for x in files) else " Read the findings with python3 -I scripts/public_lint.py")))


@test("hygiene.public_lint_over_the_build_folders")
def t_lint_build():
    rc, out, err = sh(PY + ["scripts/public_lint.py", "--paths"] + BUILD_ROOTS, timeout=300)
    summ = [l for l in out.splitlines() if l.startswith("public_lint:")]
    check("hygiene.public_lint_over_the_build_folders", rc == 0, "public_lint.py --paths over every build folder (%s): exit 0, no identifying-data finding, no hygiene finding" % ", ".join(BUILD_ROOTS),
          "exit %d: %s" % (rc, summ[-1] if summ else clean(out)[-200:]))


@test("hygiene.public_lint_whole_tree_audit", modes=("all",))
def t_lint_all():
    jf = os.path.join(SCRATCH if os.path.isdir(SCRATCH) else tempfile.gettempdir(), "wp11b-lint-all.json")
    rc, out, err = sh(PY + ["scripts/public_lint.py", "--all", "--json", jf], timeout=300)
    findings = [l for l in out.splitlines() if l.startswith("FINDING")]
    in_build, outside = [], {}
    for l in findings:
        parts = l.split()
        path = parts[3].split(":")[0] if len(parts) > 3 else ""
        if in_roots(path):
            in_build.append("%s %s" % (parts[2], parts[3]))
        else:
            outside[path.split("/")[0]] = outside.get(path.split("/")[0], 0) + 1
    try:
        os.unlink(jf)
    except OSError:
        pass
    summ = [l for l in out.splitlines() if l.startswith("public_lint:")]
    check("hygiene.public_lint_whole_tree_audit", not in_build, "a whole-tree audit (public_lint.py --all) finds nothing in the build's folders; findings elsewhere are reported for the orchestrator (they predate the build)",
          "%s. In the build's folders: %s. Elsewhere (Learn-phase files, masked, listed by top folder): %s" % (summ[-1] if summ else "no summary", listing(in_build) or "none", ", ".join("%s %d" % kv for kv in sorted(outside.items())) or "none"),
          note="the findings outside the build are e-mail-shaped and handle-shaped strings in quoted research and playbook text; they are listed for the orchestrator, not counted as a failure of the build")


@test("hygiene.theme_guard")
def t_theme():
    rc, out, err = sh(PY + ["scripts/public_lint.py", "--theme"], timeout=120)
    rc2, out2, err2 = sh(PY + ["scripts/public_lint.py", "--theme", "--paths", "pipeline/scenes", "pipeline/phone/test_strings.json", "ops/GATHER.md", "skills-staging"], timeout=120)
    s1 = [l for l in out.splitlines() if l.startswith("theme guard:")]
    s2 = [l for l in out2.splitlines() if l.startswith("theme guard:")]
    check("hygiene.theme_guard", rc == 0 and rc2 == 0, "the D-28 theme guard is clean on the new theme-bearing files (default scope) and on pipeline/scenes, test_strings.json, ops/GATHER.md and skills-staging/ explicitly",
          "default scope exit %d: %s; explicit exit %d: %s. LIMIT: a keyword scan can not judge iconography; Fable reads the pictures" % (rc, (s1 or ["?"])[-1], rc2, (s2 or ["?"])[-1]))


@test("hygiene.no_file_over_1mb")
def t_size():
    files = repo_files()
    sizes = sorted(((os.path.getsize(p(f)), f) for f in files), reverse=True)
    big = [(s, f) for s, f in sizes if s > 1_000_000]
    check("hygiene.no_file_over_1mb", not big, "no tracked or untracked-but-not-ignored file is over 1 MB (the build plan's limit; nothing large belongs in a public repo)",
          ("%d files checked; the largest is %s at %d bytes" % (len(files), sizes[0][1], sizes[0][0])) if not big else listing(["%s (%d bytes)" % (f, s) for s, f in big]))


@test("hygiene.no_binary_file")
def t_binary():
    bad = []
    allow = read_json(p("scripts", "public_lint.config.json")).get("allow_binary", [])
    allowed = []
    for f in repo_files():
        if any(fnmatch.fnmatch(f, g) for g in allow):
            allowed.append(f)
            continue
        try:
            with open(p(f), "rb") as fh:
                if b"\0" in fh.read(1 << 20):
                    bad.append(f)
        except OSError:
            pass
    check("hygiene.no_binary_file", not bad, "no tracked or untracked-but-not-ignored file holds a NUL byte (no binary), except the two reviewed synthetic fixtures on the allow_binary list of scripts/public_lint.config.json",
          "%d files scanned, none binary (%d reviewed fixtures allowed by the lint config)" % (len(repo_files()), len(allowed)) if not bad else "binary files: %s.%s" % (listing(bad), " FIX (orchestrator): git rm --cached on the tracked __pycache__ files (they are compiled caches that .gitignore already ignores)" if all("__pycache__" in x for x in bad) else ""))


@test("hygiene.new_text_under_8mb")
def t_new_text():
    base = build_baseline()
    if not base:
        raise Skip("the build baseline commit could not be found")
    rc, out, err = git("diff", "--name-only", "--diff-filter=AM", "-z", base)
    changed = [x for x in out.split("\0") if x]
    rc2, out2, err2 = git("ls-files", "-z", "--others", "--exclude-standard")
    changed += [x for x in out2.split("\0") if x]
    files = sorted({f for f in changed if os.path.isfile(p(f)) and in_roots(f)})
    tot = sum(os.path.getsize(p(f)) for f in files)
    by = {}
    for f in files:
        k = "/".join(f.split("/")[:2]) if f.startswith(("build/", "tests/")) else f.split("/")[0]
        by[k] = by.get(k, 0) + os.path.getsize(p(f))
    top = sorted(by.items(), key=lambda kv: -kv[1])[:5]
    S["new_text_bytes"] = tot
    check("hygiene.new_text_under_8mb", tot < NEW_TEXT_LIMIT_BYTES, "the text the build added or changed in its own folders (%s) since the commit before the build is under %d MB (the plan said 5; raised to 8 at gate review round 1 because the 13 packages' tests, evidence envelopes and fixtures came to about 7 MB; raise it again only with a note, do not let it drift)" % (", ".join(BUILD_ROOTS), NEW_TEXT_LIMIT_BYTES // 1_000_000),
          "%.2f MB in %d files; largest: %s%s" % (tot / 1e6, len(files), ", ".join("%s %.2f MB" % (k, v / 1e6) for k, v in top),
                                                   "" if tot < NEW_TEXT_LIMIT_BYTES else ". FIX (orchestrator decision): accept a higher limit or prune the duplicate per-run text files (build/evidence is the largest part: envelopes, transcripts and per-test logs)"))


@test("hygiene.no_ignored_file_tracked_or_staged")
def t_ignored():
    rc, out, err = git("ls-files", "-ci", "--exclude-standard")
    tracked_ignored = [x for x in out.splitlines() if x]
    # a staged DELETION of an ignored file (git rm --cached) is the fix, not the fault, so deletions are left out (gate review r1)
    rc2, out2, err2 = git("diff", "--cached", "--name-only", "--diff-filter=d")
    staged = [x for x in out2.splitlines() if x]
    staged_ignored = []
    if staged:
        rc3, out3, err3 = git("check-ignore", "--no-index", *staged)
        staged_ignored = [x for x in out3.splitlines() if x]
    bad = sorted(set(tracked_ignored) | set(staged_ignored))
    check("hygiene.no_ignored_file_tracked_or_staged", not bad, "no file that .gitignore ignores is tracked or staged (no git add -f of media or caches)",
          "%d staged file(s), none ignored; nothing tracked is ignored" % len(staged) if not bad else "tracked or staged although ignored: %s. FIX (orchestrator): git rm --cached on them" % listing(bad))


# ----------------------------------------------------------------------------------------------- docs, readiness, index
PATHISH = re.compile(r"^(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]*$")
CODE_PREFIXES = ("pipeline/", "scripts/", "win/", "ops/", "tests/", "spikes/", "build/", "skills-staging/", "playbooks/", "research/")


def path_tokens(text):
    """Repo-relative paths named in backticks (first word of each) and the file arguments of the commands in code fences."""
    toks = []
    for m in re.finditer(r"`([^`\n]+)`", text):
        toks.append(m.group(1).strip().split(" ")[0].rstrip(",.;:)"))
    infence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            infence = not infence
            continue
        if infence:
            for w in line.split():
                toks.append(w.strip("'\"").rstrip(",.;:)"))
    return toks


def path_problems(text, prefixes=CODE_PREFIXES):
    """Paths under the code folders that do not exist (placeholders, globs, git-ignored output folders and the scratch placeholder are skipped)."""
    skip_prefix = ("renders/", "exports/", "media/", "vendor/", "<scratch>", "build/evidence/wp", "C:", "%")
    missing = []
    for tok in path_tokens(text):
        if not PATHISH.match(tok) or not tok.startswith(prefixes) or any(c in tok for c in "*<>{}$") or "NN" in tok or tok.startswith(skip_prefix):
            continue
        if not os.path.exists(p(tok)):
            missing.append(tok)
    return sorted(set(missing))


@test("docs.pipeline_readme")
def t_pipeline_readme():
    f = p("pipeline", "README.md")
    if not os.path.isfile(f):
        return check("docs.pipeline_readme", False, "pipeline/README.md exists", "missing")
    text = read_text(f)
    lines = text.splitlines()
    heads = [l.lstrip("# ").strip().lower() for l in lines if l.startswith("#")]
    need_h = ["layout", "how to run", "evidence"]
    miss_h = [h for h in need_h if not any(h in x for x in heads)]
    missing = path_problems(text)
    # every tool the README tells the reader to run must exist and be runnable with --help or --list-style flags where it has them
    tools = ["pipeline/bin/render.mjs", "pipeline/validators/spec_check.py", "pipeline/validators/colour_patch.py", "pipeline/validators/mo8_gate.py", "pipeline/phone/encode_phone.sh",
             "pipeline/phone/phone_check.py", "scripts/public_lint.py", "scripts/stale_check.py", "scripts/run_week2_checks.sh"]
    unnamed = [t for t in tools if t not in text]
    ok = len(lines) <= 140 and not miss_h and not missing and not unnamed
    check("docs.pipeline_readme", ok, "pipeline/README.md is one page (140 lines or fewer) with Layout, How to run and Where evidence goes sections, names every tool, and every repo path it mentions exists",
          "%d lines; sections ok: %s; tools not named: %s; paths that do not exist: %s" % (len(lines), not miss_h, unnamed or "none", missing or "none"))


@test("docs.staged_skill_update")
def t_skill():
    d = p("skills-staging", "agent-first-production-pipeline")
    sk, ch = os.path.join(d, "SKILL.md"), os.path.join(d, "CHANGES.md")
    exp = "skills-staging/agent-first-production-pipeline/ has SKILL.md (same name, every heading of the installed skill kept) and CHANGES.md, points steps 8 to 16 and the validator checklist at the real scripts, records F-12, the lj.ps1 commands that exist and what they do not do yet, rule 4.13 and the raw-versus-derived rule"
    if not (os.path.isfile(sk) and os.path.isfile(ch)):
        return check("docs.staged_skill_update", False, exp, "SKILL.md or CHANGES.md missing")
    new, old = read_text(sk), read_text(p(".claude", "skills", "agent-first-production-pipeline", "SKILL.md"))
    name_ok = re.search(r"^name: agent-first-production-pipeline$", new, re.M) is not None and new.startswith("---")
    old_heads = [l for l in old.splitlines() if l.startswith("## ")]
    miss_heads = [h for h in old_heads if h not in new.splitlines()]
    chg = read_text(ch)
    must = [("F-12", "the ProRes 422 HQ colour finding"), ("lj.ps1 doctor", "the doctor command"), ("lj.ps1 close", "the close command"), ("dry run", "close is a dry run in v0"),
            ("redaction_patterns.json", "rule 4.13"), ("pc_tier.json", "the derived tier file"), ("raw", "the raw-versus-derived rule"), ("derived", "the raw-versus-derived rule"),
            ("spec_check.py", "real validator"), ("colour_patch.py", "real validator"), ("mo8_gate.py", "real validator"), ("render.mjs", "real harness"), ("stale_check.py", "real script"), ("public_lint.py", "real script")]
    missing_terms = [w for w, why in must if w not in new]
    missing_paths = path_problems(new) + path_problems(chg)
    ok = name_ok and not miss_heads and not missing_terms and not missing_paths and len(chg.strip()) > 400
    check("docs.staged_skill_update", ok, exp, "front matter ok: %s; installed headings missing: %s; terms missing: %s; paths that do not exist: %s; CHANGES.md %d characters" % (
        name_ok, miss_heads or "none", missing_terms or "none", missing_paths or "none", len(chg)))


STATUS_RE = [r"^PASS \(container\)$", r"^UNVERIFIED \(Windows\)$", r"^maker-owed \([^)]+\)$", r"^not started \(week [0-9-]+\)$"]
CLOSE_PHRASE = "v0 dry-run done; v1 not started (week 4)"


def readiness_problems(text, check_links=True):
    """Parse the P-LOCK readiness tables. A status table is one whose header row has '#' and 'Status'; a row of it has an id in its first cell: M or C and one or two digits (M1 ... M99,
    C1 ... C99). Any other row under such a header (a typo'd id, a merged cell, a lower-case id) is a problem, so no row can hide a PASS by failing to parse. Returns (problems, rows)."""
    probs, rows = [], []
    hdr_ok = False
    cols = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            hdr_ok = False                                       # a table ends at the first line that is not a table row
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == "#" and "Status" in cells:
            hdr_ok = True
            cols = cells
            continue
        if len(cells) >= 2 and cells[0] == "#":
            hdr_ok = False                                       # another kind of table (the findings table has no Status column)
            continue
        if not hdr_ok or all(set(c) <= set("-: ") for c in cells):
            continue                                             # not a status table, or the |---|---| separator line
        if re.match(r"^[MC][0-9]{1,2}$", cells[0]):
            rows.append(dict(zip(cols, cells)))
        else:
            probs.append("a row under a '# ... Status' header has a first cell that is not an id (M1 to M99 or C1 to C99): %r" % cells[0][:40])
    ids = [r["#"] for r in rows]
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        probs.append("%s appears more than once" % i)
    for i in ["M%d" % n for n in range(1, 9)]:
        if i not in ids:
            probs.append("the eight must-pass items are not all present (missing %s)" % i)
    for r in rows:
        st = r.get("Status", "").replace("**", "").strip()
        if not st:
            probs.append("%s has no status" % r["#"])
            continue
        if not any(re.match(rx, st) for rx in STATUS_RE):
            probs.append("%s has a status outside the vocabulary: %r" % (r["#"], st))
        win = r.get("Needs Windows", "").lower().strip()
        if win not in ("yes", "no"):
            probs.append("%s: 'Needs Windows' must be yes or no (found %r)" % (r["#"], win))
        if win == "yes" and st.startswith("PASS"):
            probs.append("%s needs Windows and must not read PASS" % r["#"])
        if st.startswith("PASS") and win == "yes":
            pass
        if "lj.ps1" in r.get("Item", "") and "close" in r.get("Item", ""):
            if CLOSE_PHRASE not in " ".join(r.values()):
                probs.append("%s (lj.ps1 close) must read %r" % (r["#"], CLOSE_PHRASE))
            if st.startswith("PASS"):
                probs.append("%s (lj.ps1 close) must never read PASS" % r["#"])
        if check_links:
            ev_cell = r.get("Evidence", "")
            paths = re.findall(r"`([^`]+)`", ev_cell)
            if not paths:
                probs.append("%s cites no evidence path" % r["#"])
            for pth in paths:
                if any(c in pth for c in "*<>") or pth.startswith(("renders/", "vendor/")):
                    continue
                if not os.path.exists(p(pth)):
                    probs.append("%s cites %s, which does not exist" % (r["#"], pth))
    if not any("lj.ps1" in r.get("Item", "") and "close" in r.get("Item", "") for r in rows):
        probs.append("there is no row for lj.ps1 close")
    return probs, rows


@test("readiness.map_statuses_and_evidence")
def t_readiness():
    f = p("build", "evidence", "P-LOCK-readiness-W2.md")
    exp = "build/evidence/P-LOCK-readiness-W2.md: the eight must-pass items and the other P-LOCK conditions each have one status from {PASS (container), UNVERIFIED (Windows), maker-owed (date), not started (week N)}, nothing that needs Windows reads PASS, lj.ps1 close reads '%s', every cited evidence path exists" % CLOSE_PHRASE
    if not os.path.isfile(f):
        return check("readiness.map_statuses_and_evidence", False, exp, "the file does not exist")
    probs, rows = readiness_problems(read_text(f))
    cnt = {}
    for r in rows:
        k = re.sub(r"\(.*", "", r.get("Status", "").replace("**", "")).strip()
        cnt[k] = cnt.get(k, 0) + 1
    check("readiness.map_statuses_and_evidence", not probs and len(rows) >= 20, exp, "%d rows (%s)%s" % (len(rows), ", ".join("%s %d" % kv for kv in sorted(cnt.items())), "" if not probs else "; " + listing(probs)))


def index_problems(text, base_dir):
    probs = []
    rows = [l for l in text.splitlines() if re.match(r"^\| \d+ \| WP-", l)]
    want = ["WP-01a", "WP-01b", "WP-02", "WP-03", "WP-04", "WP-05", "WP-06", "WP-07", "WP-08", "WP-09", "WP-10", "WP-11a", "WP-11b"]
    got = [re.match(r"^\| \d+ \| (WP-[0-9ab]+) ", l).group(1) for l in rows]
    for w in want:
        if got.count(w) != 1:
            probs.append("%s appears %d times (want one row)" % (w, got.count(w)))
    nlinks = 0
    for l in rows:
        links = re.findall(r"\]\(([^)]+)\)", l)
        if not links:
            probs.append("a row for %s has no evidence link" % re.match(r"^\| \d+ \| (WP-[0-9ab]+)", l).group(1))
        for ln in links:
            nlinks += 1
            if not os.path.exists(os.path.join(base_dir, ln)):
                probs.append("link %s does not exist" % ln)
    return probs, len(rows), nlinks


@test("index.thirteen_rows_with_existing_links")
def t_index():
    f = p("build", "evidence", "INDEX.md")
    exp = "build/evidence/INDEX.md has one row for each of the thirteen entries (WP-01a to WP-11b) and every evidence link on every row exists"
    if not os.path.isfile(f):
        raise Skip("INDEX.md has not been written yet (run scripts/run_week2_checks.sh --quick)")
    probs, n, nl = index_problems(read_text(f), os.path.dirname(f))
    gen = re.search(r"Generated by `[^`]+` on (\S+)", read_text(f))
    check("index.thirteen_rows_with_existing_links", not probs and n == 13, exp, "%d rows, %d links, generated %s%s" % (n, nl, gen.group(1) if gen else "?", "" if not probs else "; " + listing(probs)))


@test("index.runner_lists_thirteen_areas_landed")
def t_runner_list():
    rc, out, err = sh(["bash", "scripts/run_week2_checks.sh", "--list"], timeout=60)
    m = re.search(r"Landed: (\d+) of (\d+)", out)
    areas = re.findall(r"^\s+\d+\s+(\S+)\s+(WP-\S+)", out, flags=re.M)
    missing = [a for a, w in areas if not os.path.isfile(p("tests", a, "run_tests.sh"))]
    check("index.runner_lists_thirteen_areas_landed", rc == 0 and m and m.group(1) == m.group(2) == "13" and len(areas) == 13 and not missing,
          "scripts/run_week2_checks.sh --list shows the 13 areas WP-01a to WP-11b in order, all landed (no NOT LANDED), and every tests/<area>/run_tests.sh exists",
          "exit %d; %s; areas: %s; missing run_tests.sh: %s" % (rc, m.group(0) if m else "no 'Landed:' line", ",".join(a for a, w in areas), missing or "none"))


# ----------------------------------------------------------------------------------------------- negative controls
@test("ctrl.checkers_fail_on_planted_defects")
def t_controls():
    probs = []
    tried = [0, 0]                      # planted defects tried, known-good states proved to pass

    def noticed(label, cond):
        tried[0] += 1
        if not cond:
            probs.append("%s was not noticed" % label)

    def passes(label, cond):
        tried[1] += 1
        if not cond:
            probs.append("%s did not pass" % label)

    # 1. settings card: change FontSize, drop a candidate loudness
    card = read_text(p("ops", "SETTINGS-CARD.md"))
    settings = read_json(p("pipeline", "settings.json"))
    chains = read_json(p("pipeline", "lib", "chains.json"))["chains"]
    base = len(card_problems(card, settings, chains))
    noticed("FontSize=24 on the card", len(card_problems(card.replace("FontSize=23", "FontSize=24"), settings, chains)) > base)
    noticed("a dropped loudness candidate on the card", len(card_problems(card.replace("-23, -18 and -16", "-23 and -16"), settings, chains)) > base)
    # 2. phone row: a wrong CRF; the register against the profile; and the proof that the PASTED state passes (the live FAIL is the card's state, not the checker's).
    #    The planted profiles and rows below are built from the real ones, so these controls hold whichever state (3.5 and 32, or 4 and 36) the real files are in.
    prof = read_json(p("pipeline", "phone", "profile.json"))
    fill = read_json(p("build", "evidence", "wp08", "fill_20x9_phone.json"))
    dec = read_text(p("DECISIONS.md"))
    reg, rprobs = register_phone_facts(dec)
    passes("the register's W-63 and W-18 rows are read (PH1/PH2 CRF, caps, level, caption size, margin and characters a line)", not rprobs and len(reg) == 8)

    def planted_profile(cap_k, chars):
        pp = json.loads(json.dumps(prof))
        a2 = pp["chains"]["phone_720_share"]["video_args"]
        a2[a2.index("-maxrate") + 1] = cap_k
        pp["caption"]["styles"]["phone"]["max_chars_per_line"] = chars
        return pp
    p35, p4 = planted_profile("3500k", 32), planted_profile("4M", 36)
    row = phone_row_text(p("pipeline", "phone", "PHONE-ROW.md"))
    row4 = row.replace("3.5 Mb/s", "4 Mb/s").replace("32 characters a line", "36 characters a line")        # the row as regenerated to the register
    row35 = row4.replace("4 Mb/s", "3.5 Mb/s").replace("36 characters a line", "32 characters a line")      # the row as WP-08 wrote it
    b0 = len(need(row, phone_needles(prof, fill), "x"))
    noticed("CRF 21 in the phone row", len(need(row.replace("CRF 20", "CRF 21"), phone_needles(prof, fill), "x")) > b0)
    passes("a Phone row of 3.5 Mb/s and 32 characters against a profile of 3.5 and 32", not need(row35, phone_needles(p35, fill), "x"))
    noticed("a 4 Mb/s cap in place of 3.5 for PH2", bool(need(row35.replace("3.5 Mb/s", "4 Mb/s"), phone_needles(p35, fill), "x")))
    noticed("36 characters a line in place of 32", bool(need(row35.replace("32 characters a line", "36 characters a line"), phone_needles(p35, fill), "x")))
    noticed("profile.json at PH2 3.5 Mb/s and 32 characters while the register says 4 and 36 (parity.phone_profile_vs_register)",
            [x[0] for x in phone_register_problems(p35, {"ph2_cap_mbps": 4.0, "max_chars": 36})] == ["PH2 cap", "phone caption characters a line"])
    noticed("profile.json with only the PH2 cap off the register", [x[0] for x in phone_register_problems(planted_profile("3500k", 36), {"ph2_cap_mbps": 4.0, "max_chars": 36})] == ["PH2 cap"])
    noticed("profile.json with only the line length off the register", [x[0] for x in phone_register_problems(planted_profile("4M", 32), {"ph2_cap_mbps": 4.0, "max_chars": 36})] == ["phone caption characters a line"])
    passes("profile.json regenerated to the register (4 Mb/s, 36 characters)", not phone_register_problems(p4, {"ph2_cap_mbps": 4.0, "max_chars": 36}))
    # these planted registers are made with regular expressions, so they work whether DECISIONS.md still says 4 Mb/s and 36 characters or was amended to 3.5 and 32 (gate review r1)
    dec_35_32 = re.sub(r"([0-9.]+) Mb/s cap, level", "3.5 Mb/s cap, level", dec, count=1)
    dec_35_32 = re.sub(r"(two lines, at most )\d+( characters)", r"\g<1>32\g<2>", dec_35_32, count=1)
    reg_amended = register_phone_facts(dec_35_32)
    passes("a register amended to 3.5 Mb/s and 32 characters against the profile that holds them", not reg_amended[1] and not phone_register_problems(p35, reg_amended[0]))
    noticed("a register row that no longer states the PH2 cap in the shape the test reads (fails closed)", bool(register_phone_facts(re.sub(r"[0-9.]+ Mb/s cap, level", "four megabit cap, level", dec, count=1))[1]))
    noticed("a register without a W-18 row (fails closed)", bool(register_phone_facts(dec.replace("| W-18 |", "| W-18x |"))[1]))
    reg_row = phone_needles(p4, fill, register={"ph2_cap_mbps": 4.0, "max_chars": 36})
    passes("the card row pasted from a PHONE-ROW.md regenerated to the register (4 Mb/s, 36 characters)", not need(row4, reg_row, "x"))
    noticed("the card row pasted from the 3.5 Mb/s, 32-character PHONE-ROW.md while the register says 4 and 36", bool(need(row35, reg_row, "x")))
    pr_line = next((l for l in read_text(p("pipeline", "phone", "PHONE-ROW.md")).splitlines() if l.startswith("| **Phone**")), None)
    cd_line = next((l for l in card.splitlines() if l.startswith("| **Phone**")), None)
    if pr_line and cd_line:
        pasted = card.replace(cd_line, pr_line)
        passes("the card with PHONE-ROW.md pasted over its Phone row (against the profile it was made from)", not need(phone_row_from_text(pasted), phone_needles(prof, fill), "x"))
    st = read_json(p("build", "evidence", "wp08", "scripts_tested.json"))
    pl = scripts_line(read_text(p("pipeline", "phone", "PHONE-ROW.md")))
    cm = re.search(r"`Caption and font test ran in: [^`]+`", card)
    if pl and cm:
        pasted_lang = card.replace(cm.group(0), "`Caption and font test ran in: %s (neutral strings) on %s; NOT TESTED: %s`" % (", ".join(pl[0]), pl[1], ", ".join(pl[2])))
        passes("the card with the 'Scripts tested' line pasted into its language note", not card_language_problems(pasted_lang, st))
        noticed("a language note without a date", bool(card_language_problems(pasted_lang.replace(pl[1], "<date>"), st)))
    # 3. pins: a wrong version in the copy of pins.json
    pins = json.loads(json.dumps(read_json(p("win", "pins.json"))))
    assets = read_json(p("spikes", "sp1_craft_cli", "release_assets.json"))
    w22 = re.search(r"^\| W-22 \|.*$", read_text(p("DECISIONS.md")), re.M).group(0)
    p0 = len(pin_problems(pins, assets, w22))
    pins["apps"]["photocraft"]["pin"] = "0.10.1"
    noticed("photocraft 0.10.1 in win/pins.json", len(pin_problems(pins, assets, w22)) > p0)
    # 4. lj.ps1: planted switch, planted Remove-Item, planted stale script name
    lj = read_text(p("win", "lj.ps1"))
    files = set(repo_files())
    l0 = len(lj_problems(lj, files)[0])
    noticed("a working -Apply option in lj.ps1", len(lj_problems(lj.replace("$flagOpts = @('skipchecks')", "$flagOpts = @('skipchecks', 'apply')"), files)[0]) > l0)
    noticed("a call to a script that does not exist", len(lj_problems(lj + "\n& python -I scripts/stale_check_old.py\n", files)[0]) > l0)
    # the static scan: one planted line of each form a scan can see (a string-invoked command, & 'Remove-Item' or & $c, cannot be seen by any scan; tests/win_lj/ proves those absent)
    for plant in ("Remove-Item -Recurse $x", "rd $x -Recurse", "rmdir $x", "mkdir $x", "md $x", "$d = md $x", "rm -Recurse -Force $x", "'x' > $file", "$log >> $file", "Invoke-Expression $cmd", "iex $cmd",
                  "Start-Process git -ArgumentList 'commit'", "Export-Csv $p", "Export-Clixml $p", "Tee-Object -FilePath $p", "Compress-Archive $a $b", "Expand-Archive $a $b",
                  "& git commit -m x", "& git -C $r commit -m x", "git.exe --no-pager push", "git -c user.name=x commit -m y", "[IO.File]::WriteAllText($p, 'x')"):
        noticed("%s in lj.ps1 (static scan)" % plant, len(lj_problems(lj + "\n" + plant + "\n", files)[0]) > l0)
    for good in ("$a = & $cmd.Source @probe 2>$null", "$o = & $py.exe @all 2>&1", "foreach ($rd in $removeDirs) { $rd.shown }", "$md = 3", "& git -C $r status", "& git rev-parse --show-toplevel", "$n = $a.Length - 1"):
        passes("%s in lj.ps1 (static scan reads no mutation)" % good, len(lj_problems(lj + "\n" + good + "\n", files)[0]) == l0)
    # 5. noto: a script with strings and no font
    strings = json.loads(json.dumps(read_json(p("pipeline", "phone", "test_strings.json"))))
    libs = read_json(p("pipeline", "lib", "libs.lock.json"))
    strings["scripts"]["tamil"]["strings"] = [{"id": "x", "text": "x"}]
    noticed("a Tamil string with no fetched font", any("tamil" in x for x in noto_problems(strings, libs)[0]))
    # 6. the denylist scanner on a planted tree
    td = tempfile.mkdtemp(prefix="wp11b-ctrl.", dir=SCRATCH if os.path.isdir(SCRATCH) else None)
    try:
        os.makedirs(os.path.join(td, "tests", "win", "fixtures"))
        os.makedirs(os.path.join(td, "build", "evidence"))
        for f in ("tests/win/fixtures/pc_report_ok.json", "build/evidence/pc_report.json", "build/evidence/colour_patch_pc_1.json", "build/evidence/maker-pc.json"):
            open(os.path.join(td, f), "w").write("{}")
        globs, exempt, eg = deny_globs()
        open(os.path.join(td, "build", "evidence", "pc_report.schema.json"), "w").write("{}")      # a schema is exempt by name
        hits = denylist_hits(td, globs, exempt, eg)
        noticed("three raw-report file names on a planted tree (and not the fixture or the schema)", sorted(hits) == ["build/evidence/colour_patch_pc_1.json", "build/evidence/maker-pc.json", "build/evidence/pc_report.json"])
    finally:
        shutil.rmtree(td, ignore_errors=True)
    # 7. the pc folder check on a planted folder: a tier file with a fixture GPU string, an unknown json, an extra property
    td = tempfile.mkdtemp(prefix="wp11b-ctrl.", dir=SCRATCH if os.path.isdir(SCRATCH) else None)
    try:
        secrets = fixture_secrets()
        tier = {"schema": "lj-pc-tier/1", "date": "2026-10-19", "note": secrets[0] if secrets else "x"}
        json.dump(tier, open(os.path.join(td, "pc_tier_bad.json"), "w"))
        open(os.path.join(td, "notes.json"), "w").write("{}")
        pr, seen = pc_dir_problems(td, secrets)
        noticed("a tier file with a fixture GPU string, a missing field and an extra field", any("not part of the report format" in x or "is missing" in x for x in pr) and any("fixture GPU" in x for x in pr))
        noticed("a .json that is not a derived file name", any("not a derived file name" in x for x in pr))
    finally:
        shutil.rmtree(td, ignore_errors=True)
    # 8. the disk rule: planted envelopes
    good = ("WP-X", {"package": "WP-X", "test": "t", "disk": {"avail_mb_start": 900, "planned_write_mb": 300, "avail_mb_min": 560, "avail_mb_end": 700}})
    bad1 = ("WP-X", {"package": "WP-X", "test": "t", "disk": {"avail_mb_start": 650, "planned_write_mb": 300, "avail_mb_min": 560, "avail_mb_end": 700}})
    bad2 = ("WP-X", {"package": "WP-X", "test": "t", "disk": {"avail_mb_start": 900, "planned_write_mb": 300, "avail_mb_min": 240, "avail_mb_end": 700}})
    passes("a stage that kept the 400 MB rule and the 250 MB floor", not budget_problems([good])[0])
    noticed("start minus planned under 400 MB", bool(budget_problems([bad1])[0]))
    noticed("a minimum under the 250 MB hard floor", bool(budget_problems([bad2])[0]))
    cr = ("x", {"package": "WP-Y", "test": "crossing", "disk": {"avail_mb_min": 100, "hard_floor_mb": 250}})
    noticed("an unlisted hard-floor crossing", bool(crossing_problems([cr], [])[0]))
    passes("a listed hard-floor crossing", not crossing_problems([cr], [{"package": "WP-Y", "test": "crossing"}])[0])
    # an envelope cannot lower the plan's floors: floor_mb 0 / hard_floor_mb 0 on a stage that broke both rules
    lowered = ("x", {"package": "WP-Z", "test": "lowered", "disk": {"avail_mb_start": 300, "planned_write_mb": 150, "avail_mb_min": 260, "avail_mb_end": 300, "floor_mb": 0, "hard_floor_mb": 0}})
    lowered_min = ("x", {"package": "WP-Z", "test": "lowered_min", "disk": {"avail_mb_start": 900, "planned_write_mb": 150, "avail_mb_min": 100, "avail_mb_end": 300, "floor_mb": 0, "hard_floor_mb": 0}})
    noticed("an envelope with floor_mb 0 and hard_floor_mb 0 and start minus planned of 150 (the budget rule)", bool(budget_problems([lowered])[0]))
    noticed("an envelope with hard_floor_mb 0 and a minimum of 100 (the budget rule)", bool(budget_problems([lowered_min])[0]))
    noticed("an envelope with hard_floor_mb 0 and a minimum of 100 (the crossing rule)", bool(crossing_problems([lowered_min], [])[0]))
    noticed("an envelope with a non-numeric floor and a minimum of 100", bool(crossing_problems([("x", {"package": "WP-Z", "test": "str", "disk": {"avail_mb_min": 100, "hard_floor_mb": "none"}})], [])[0]))
    passes("an envelope that raises the floors above the plan's and keeps them", not budget_problems([("x", {"package": "WP-Z", "test": "stricter", "disk": {
        "avail_mb_start": 1500, "planned_write_mb": 300, "avail_mb_min": 700, "avail_mb_end": 900, "floor_mb": 600, "hard_floor_mb": 500}})])[0])
    # 9. readiness parser on planted maps
    f = p("build", "evidence", "P-LOCK-readiness-W2.md")
    if os.path.isfile(f):
        t0 = read_text(f)
        n0 = len(readiness_problems(t0, check_links=False)[0])
        win_row = re.search(r"^\| (M1) \|.*$", t0, re.M)
        if win_row:
            mutated = t0.replace(win_row.group(0), re.sub(r"\| (maker-owed \([^)]*\)) \|", "| PASS (container) |", win_row.group(0), count=1))
            noticed("PASS on a Windows row of the readiness map", len(readiness_problems(mutated, check_links=False)[0]) > n0)
        noticed("a changed lj.ps1 close wording", len(readiness_problems(t0.replace(CLOSE_PHRASE, "v0 done"), check_links=False)[0]) > n0)
        noticed("a status outside the vocabulary", len(readiness_problems(t0.replace("not started (week 4)", "somewhere later", 1), check_links=False)[0]) > n0)
        noticed("a deleted status cell", len(readiness_problems(re.sub(r"(?m)^(\| C2 \|[^|]*\|[^|]*\|) not started \(week 3\) \|", r"\1  |", t0), check_links=False)[0]) > n0)
        # a row whose id the old pattern did not accept hid its PASS: an added M9 (Needs Windows yes, PASS (container)), a typo'd id, a lower-case id, a merged cell
        m8 = re.search(r"(?m)^\| M8 \|.*$", t0)
        if m8:
            m9 = "| M9 | A ninth item | yes | PASS (container) | planted | `ops/SETTINGS-CARD.md` | none |"
            noticed("an added M9 row that needs Windows and reads PASS (container)", any("M9" in x and "must not read PASS" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n" + m9), check_links=False)[0]))
            noticed("an added row with the id 'M 9' (does not parse as an id)", any("not an id" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n" + m9.replace("M9", "M 9")), check_links=False)[0]))
            noticed("an added row with the id 'm9' (lower case)", any("not an id" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n" + m9.replace("M9", "m9")), check_links=False)[0]))
            noticed("an added row with a merged first cell", any("not an id" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n| M9 and M10 | x | yes | PASS (container) | p | `ops/SETTINGS-CARD.md` | none |"), check_links=False)[0]))
            noticed("a duplicated M8 row", any("more than once" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n" + m8.group(0)), check_links=False)[0]))
            noticed("a three-digit id C100 (outside M or C and two digits)", any("not an id" in x for x in readiness_problems(t0.replace(m8.group(0), m8.group(0) + "\n" + m9.replace("M9", "C100")), check_links=False)[0]))
        passes("the real readiness map has no row that fails to parse", not any("not an id" in x for x in readiness_problems(t0, check_links=False)[0]))
    # 10. index parser
    idx = p("build", "evidence", "INDEX.md")
    if os.path.isfile(idx):
        t0 = read_text(idx)
        n0 = len(index_problems(t0, os.path.dirname(idx))[0])
        drop = next((l for l in t0.splitlines() if re.match(r"^\| \d+ \| WP-05 ", l)), None)
        if drop:
            noticed("a missing INDEX row", len(index_problems(t0.replace(drop, ""), os.path.dirname(idx))[0]) > n0)
        noticed("a dead INDEX link", len(index_problems(t0.replace("](wp05/", "](wp05-gone/"), os.path.dirname(idx))[0]) > n0)
    # 11. profile versus chain: a chain that promises a different pixel format, and a profile naming a chain that does not exist
    chs = json.loads(json.dumps(read_json(p("pipeline", "lib", "chains.json"))["chains"]))
    sprof = read_json(p("pipeline", "settings.json"))["profiles"]
    passes("the real profiles against the real chains", not profile_chain_problems(sprof, chs, "x")[0])
    chs["h264_venue"]["expect"]["pix_fmt"] = "yuv422p"
    noticed("a chain promising yuv422p for a yuv420p profile", bool(profile_chain_problems(sprof, chs, "x")[0]))
    chs2 = {k: v for k, v in read_json(p("pipeline", "lib", "chains.json"))["chains"].items() if k != "h264_online"}
    noticed("a profile naming a chain that does not exist", bool(profile_chain_problems(sprof, chs2, "x")[0]))
    # 12. stale parse
    passes("the stale-hit parser on its sample", parse_stale("NEW FAIL a/b.md:3 [S-01.x] text\nNEW WARN c.md:9 [S-02.y] t") == [("FAIL", "a/b.md", 3, "S-01.x"), ("WARN", "c.md", 9, "S-02.y")])
    # 13. a partial (--only) run must not replace the mode's evidence: seed a scratch evidence folder, run one cheap test with --only, and see the seeds untouched
    td = tempfile.mkdtemp(prefix="wp11b-ctrl.", dir=SCRATCH if os.path.isdir(SCRATCH) else None)
    try:
        seed_j, seed_s = '{"seed":"whole-run evidence"}\n', '{"seed":"whole-run summary"}\n'
        open(os.path.join(td, "tests_quick.jsonl"), "w").write(seed_j)
        open(os.path.join(td, "summary_quick.json"), "w").write(seed_s)
        rc, out, err = sh(PY + [os.path.join(HERE, "run_checks.py"), "--mode", "quick", "--only", "parity.pins", "--evidence", td, "--work", os.path.join(td, "work")], timeout=120)
        kept = read_text(os.path.join(td, "tests_quick.jsonl")) == seed_j and read_text(os.path.join(td, "summary_quick.json")) == seed_s
        wrote = os.path.isfile(os.path.join(td, "tests_quick_only.jsonl")) and os.path.isfile(os.path.join(td, "summary_quick_only.json"))
        noticed("a --only run that replaces tests_quick.jsonl or summary_quick.json (it must write the _only files)", kept and wrote and rc == 0)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    check("ctrl.checkers_fail_on_planted_defects", not probs and tried[0] >= 25, "each checker above fails on a planted defect in a copy of its input (card, phone row and the profile against the register, language note, pins, lj.ps1 static scan, Noto font, denylist, pc folder, disk rule and lowered floors, readiness map ids, index, profile and chain, the --only outputs) and passes the known-good states, among them the card row pasted from a PHONE-ROW.md regenerated to the register (W-63, W-18)",
          ("%d planted defects were each caught and %d known-good states passed" % (tried[0], tried[1])) if not probs else listing(probs))


# ----------------------------------------------------------------------------------------------- end to end (all)
def guarded(label, planned, cmd, timeout=1800):
    script = '. scripts/lj_guard.sh && lj_with_disk %d %s -- "$@"' % (planned, label)
    return sh(["bash", "-c", script, "bash"] + cmd, timeout=timeout)


def guard_blocked(rc, out, err):
    txt = out + err
    return rc == 3 and any(w in txt for w in ("REFUSED", "BUSY", "DISK-FLOOR"))


def ffprobe_json(path, entries="stream=codec_name,profile,level,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_frames,color_range,color_space,color_primaries,color_transfer,channels,sample_rate"):
    rc, out, err = sh(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", path], timeout=120)
    return json.loads(out) if rc == 0 and out.strip() else {}


def render_cmd(extra):
    return ["node", "pipeline/bin/render.mjs", "--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet"] + extra


def rmtree(path):
    shutil.rmtree(path, ignore_errors=True)


@test("e2e.testcard_through_chain_checked_by_spec_check", modes=("all",))
def t_e2e_spec():
    d = work("e2e_spec")
    rmtree(d)
    os.makedirs(d)
    env = {"PLAYWRIGHT_BROWSERS_PATH": "/opt/pw-browsers"}
    exp = "the WP-04 test card rendered by render.mjs --chain h264_venue (2 s, 48 frames) passes spec_check.py in its video-only view of venue_h264 (every video check), and with a tone muxed in passes the full venue_h264 profile (28 checks incl. loudness) "
    with DiskWatch() as dw:
        s0 = avail_mb()
        vid = os.path.join(d, "venue_video.mp4")
        rc, out, err = sh(render_cmd(["--page", "scenes/testcard/scene.html", "--seconds", "2", "--chain", "h264_venue", "--ffmpeg", rel(vid), "--json", rel(os.path.join(d, "r.json"))]), timeout=300, env=env)
        if rc != 0:
            return check("e2e.testcard_through_chain_checked_by_spec_check", False, exp, "render.mjs exit %d: %s" % (rc, clean(err)[-200:]))
        rep = read_json(os.path.join(d, "r.json"))
        # the video-only view of the real venue_h264 profile: the same video block, no audio and no loudness (derived at test time, so it can not drift from settings.json)
        st = read_json(p("pipeline", "settings.json"))
        prof = json.loads(json.dumps(st["profiles"]["venue_h264"]))
        prof["audio"] = {"required": False}
        prof.pop("loudness", None)
        prof["description"] = "video-only view of venue_h264 (derived at test time)"
        pf = os.path.join(d, "video_only.json")
        json.dump({"profiles": {"venue_h264_video_only": prof}}, open(pf, "w"))
        r1 = sh(PY + ["pipeline/validators/spec_check.py", rel(vid), "--profiles-file", rel(pf), "--profile", "venue_h264_video_only", "--json", ev("e2e_spec_check_video_only.json")], timeout=300)
        # a tone, then the full profile
        gen = load_module(p("tests", "validators", "gen_fixtures.py"), "gen_fixtures_for_tone")
        mux = os.path.join(d, "venue_muxed.mp4")
        ven = read_json(p("pipeline", "lib", "chains.json"))["chains"]["h264_venue"]
        rcm, om, em = sh(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", rel(vid), "-f", "lavfi", "-i", gen.tone(-18.0, 2), "-map", "0:v", "-map", "1:a", "-c:v", "copy"] + ven["audio_args"] +
                         ["-movflags", "+faststart", "-map_metadata", "-1", rel(mux)], timeout=120)
        r2 = sh(PY + ["pipeline/validators/spec_check.py", rel(mux), "--profile", "venue_h264", "--json", ev("e2e_spec_check_venue_h264.json")], timeout=300) if rcm == 0 else (rcm, om, em)
        # negative control: the same video file against the 25 fps and 720p views of the profile must fail
        bad = json.loads(json.dumps(prof))
        bad["video"]["fps"] = "25/1"
        bad["video"]["height"] = 720
        json.dump({"profiles": {"venue_wrong": bad}}, open(os.path.join(d, "wrong.json"), "w"))
        r3 = sh(PY + ["pipeline/validators/spec_check.py", rel(vid), "--profiles-file", rel(os.path.join(d, "wrong.json")), "--profile", "venue_wrong"], timeout=300)
        n1 = re.search(r"RESULT: PASS \((\d+) checks\)", r1[1])
        n2 = re.search(r"RESULT: PASS \((\d+) checks\)", r2[1])
        probe = ffprobe_json(vid)
        v = (probe.get("streams") or [{}])[0]
        size = os.path.getsize(vid)
    chain = rep.get("chain") or {}
    ok = r1[0] == 0 and n1 and r2[0] == 0 and n2 and r3[0] == 1 and "video.fps" in r3[1] and rep.get("chain_check", {}).get("ok") and chain.get("name") == "h264_venue" and chain.get("source") == "chains.json"
    check("e2e.testcard_through_chain_checked_by_spec_check", bool(ok), exp + "; a 25 fps / 720p view of the same file must FAIL (negative control)",
          "render ok (%s frames, %.1f fps, chain %s); video-only view: exit %d %s; full venue_h264 with a -18 LUFS tone: exit %d %s; control (25 fps, 720): exit %d naming video.fps; ffprobe %sx%s %s %s; file %d bytes" % (
              rep.get("frames_rendered"), rep.get("throughput_fps") or 0, "%s from %s" % (chain.get("name"), chain.get("source")), r1[0], n1.group(0) if n1 else "-", r2[0], n2.group(0) if n2 else "-", r3[0], v.get("width"), v.get("height"), v.get("r_frame_rate"), v.get("pix_fmt"), size),
          disk={"start": s0, "end": avail_mb(), "min": dw.min})
    rmtree(d)


@test("e2e.a11_mo8_pair", modes=("all",))
def t_e2e_mo8():
    gate = p("pipeline", "validators", "mo8_gate.py")
    env = {"PLAYWRIGHT_BROWSERS_PATH": "/opt/pw-browsers"}
    cache = p("research", "cinematic-quality-fixtures", "__pycache__")
    had_cache = os.path.isdir(cache)
    rows = {}
    with DiskWatch() as dw:
        s0 = avail_mb()
        for mode in ("transform", "layout"):
            d = work("e2e_mo8_" + mode)
            rmtree(d)
            r = sh(render_cmd(["--page", "scenes/testcard/scene.html?view=detail&push=%s&dur=1.9583333" % mode, "--out", rel(d), "--frames", "0:48"]), timeout=300, env=env)
            jf = ev("e2e_mo8_%s.json" % mode)
            rc, out, err = sh(PY + [rel(gate), rel(d), "--json", jf], timeout=300)
            try:
                gj = read_json(jf)
            except (OSError, ValueError):
                gj = {}
            lines = [l.strip() for l in out.splitlines() if "MO8" in l and "limit" in l]
            rows[mode] = {"render_exit": r[0], "gate_exit": rc, "lines": lines, "verdict": [l.strip() for l in out.splitlines() if "RESULT" in l]}
            rmtree(d)
    if not had_cache:
        rmtree(cache)
    ok = rows["transform"]["render_exit"] == 0 and rows["layout"]["render_exit"] == 0 and rows["transform"]["gate_exit"] == 0 and rows["layout"]["gate_exit"] == 1
    check("e2e.a11_mo8_pair", ok, "WP-04 A11: the test card with ?push=transform (a sub-pixel push by transform) passes pipeline/validators/mo8_gate.py (exit 0) and ?push=layout (the negative control, animated width/height/left/top) fails it (exit 1); 48 frames of ?view=detail each",
          "transform: render %d, gate exit %d %s %s; layout: render %d, gate exit %d %s %s" % (rows["transform"]["render_exit"], rows["transform"]["gate_exit"], rows["transform"]["verdict"], rows["transform"]["lines"],
                                                                                                rows["layout"]["render_exit"], rows["layout"]["gate_exit"], rows["layout"]["verdict"], rows["layout"]["lines"]),
          disk={"start": s0, "end": avail_mb(), "min": dw.min})


def moov_before_mdat(path):
    import struct
    names, total = [], os.path.getsize(path)
    with open(path, "rb") as f:
        pos = 0
        while pos + 8 <= total:
            f.seek(pos)
            size, typ = struct.unpack(">I4s", f.read(8))
            hl = 8
            if size == 1:
                size, hl = struct.unpack(">Q", f.read(8))[0], 16
            elif size == 0:
                size = total - pos
            names.append(typ.decode("latin-1"))
            if size < hl:
                break
            pos += size
    return "moov" in names and "mdat" in names and names.index("moov") < names.index("mdat"), names


@test("e2e.phone_encode_from_harness_master_incl_fill_20x9", modes=("all",))
def t_e2e_phone():
    d = work("e2e_phone")
    rmtree(d)
    os.makedirs(d)
    master, srt, rep = os.path.join(d, "master.mov"), os.path.join(d, "caps.srt"), os.path.join(d, "scene_report.json")
    exp = "a ProRes 422 HQ master rendered by the WP-04 harness (prores422hq_master chain, 6 s) passes spec_check.py master_prores422hq; encode_phone.sh makes PH1 that passes spec_check.py phone_1080 (profile.json) and colour_patch.py; phone_check.py --scenario fill_20x9 puts the caption bottom at or above the 88% line; a clip burned with the venue margin fails it"
    with DiskWatch() as dw:
        s0 = avail_mb()
        rc, out, err = guarded("wp11b-master", 100, PY + ["tests/phone/make_master.py", "--out", rel(master), "--srt", rel(srt), "--seconds", "6", "--report", rel(rep)], timeout=1800)
        if guard_blocked(rc, out, err):
            raise Blocked((out + err).strip().splitlines()[-1][:300])
        if rc != 0:
            return check("e2e.phone_encode_from_harness_master_incl_fill_20x9", False, exp, "make_master.py exit %d: %s" % (rc, clean(out + err)[-250:]))
        pm = sh(PY + ["pipeline/validators/spec_check.py", rel(master), "--profile", "master_prores422hq", "--json", ev("e2e_spec_check_master.json")], timeout=600)
        pmv = (ffprobe_json(master).get("streams") or [{}])[0]
        phone = os.path.join(d, "phone.mp4")
        er = sh(["bash", "pipeline/phone/encode_phone.sh", rel(master), rel(srt), rel(phone), "--layout", rel(rep)], timeout=1800)
        if guard_blocked(*er):
            raise Blocked((er[1] + er[2]).strip().splitlines()[-1][:300])
        sc = sh(PY + ["pipeline/validators/spec_check.py", rel(phone), "--profiles-file", "pipeline/phone/profile.json", "--profile", "phone_1080", "--json", ev("e2e_spec_check_phone_1080.json")], timeout=600) if er[0] == 0 else (er[0], "", "")
        cp = sh(PY + ["pipeline/validators/colour_patch.py", "--ffmpeg", "ffmpeg", "--chain-file", "pipeline/phone/profile.json", "--chain", "phone_1080"], timeout=300)
        fr = sh(PY + ["pipeline/phone/phone_check.py", rel(phone), "--scenario", "fill_20x9", "--json", ev("e2e_fill_20x9_phone.json"), "--quiet"], timeout=900) if er[0] == 0 else (er[0], "", "")
        ven = os.path.join(d, "venue_margin.mp4")
        er2 = sh(["bash", "pipeline/phone/encode_phone.sh", rel(master), rel(srt), rel(ven), "--style", "venue_fs23", "--layout", rel(rep), "--overwrite"], timeout=1800)
        fr2 = sh(PY + ["pipeline/phone/phone_check.py", rel(ven), "--scenario", "fill_20x9", "--json", ev("e2e_fill_20x9_venue_margin.json"), "--quiet"], timeout=900) if er2[0] == 0 else (er2[0], "", "")
        ok_atoms, names = moov_before_mdat(phone) if os.path.isfile(phone) else (False, [])
        bots = []
        for fn in ("e2e_fill_20x9_phone.json", "e2e_fill_20x9_venue_margin.json"):
            try:
                j = read_json(ev(fn))
                bots.append(max(v["position"]["caption_bottom_pct"] for v in j["scenarios"]["fill_20x9"]["scripts"].values() if v.get("position")))
            except (OSError, ValueError, KeyError):
                bots.append(None)
        dur = float(ffprobe_json(phone, "format=duration").get("format", {}).get("duration") or 0) if os.path.isfile(phone) else 0
        br = os.path.getsize(phone) * 8.0 / dur / 1e6 if dur else 0
        cap = read_json(p("pipeline", "phone", "profile.json"))["chains"]["phone_1080"]["bitrate_cap_mbps"]
        led = ledger("wp11b-master")
    master_ok = pm[0] == 0 and pmv.get("codec_name") == "prores" and pmv.get("profile") == "HQ" and pmv.get("r_frame_rate") == "24/1" and str(pmv.get("nb_frames")) == "144"
    ok = (master_ok and er[0] == 0 and sc[0] == 0 and cp[0] == 0 and fr[0] == 0 and fr2[0] == 1 and ok_atoms and br <= cap * 1.10
          and bots[0] is not None and bots[1] is not None and bots[0] <= 88.0 < bots[1])
    check("e2e.phone_encode_from_harness_master_incl_fill_20x9", bool(ok), exp,
          "master: spec_check exit %d (%s %sx%s %s fps %s frames); PH1 encode exit %d, spec_check phone_1080 exit %d, colour_patch exit %d, %.2f Mbps against a cap of %g + 10%%, moov before mdat %s; fill_20x9: phone style exit %d caption bottom %s%%, venue-margin clip exit %d bottom %s%% (limit 88)" % (
              pm[0], pmv.get("profile"), pmv.get("width"), pmv.get("height"), pmv.get("r_frame_rate"), pmv.get("nb_frames"), er[0], sc[0], cp[0], br, cap, ok_atoms, fr[0], bots[0], fr2[0], bots[1]),
          planned=100, lg="wp11b-master" if led else None, disk=None if led else {"start": s0, "end": avail_mb(), "min": dw.min})
    rmtree(d)


# ----------------------------------------------------------------------------------------------- driver
def main(argv=None):
    global ARGS
    ap = argparse.ArgumentParser(prog="run_checks.py")
    ap.add_argument("--mode", choices=("quick", "all"), default="quick")
    ap.add_argument("--only", default="")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--work", default=os.path.join(ROOT, "renders", "wp11b"))
    ap.add_argument("--evidence", default=os.path.join(ROOT, "build", "evidence", "wp11b"))
    ARGS = ap.parse_args(argv)
    if ARGS.list:
        for name, modes, _ in REG:
            print("%-52s %s" % (name, "quick + all" if "quick" in modes else "all"))
        return 0
    os.makedirs(ARGS.evidence, exist_ok=True)
    os.makedirs(ARGS.work, exist_ok=True)
    only = [x for x in ARGS.only.split(",") if x]
    # A partial (--only) run must never replace the mode's evidence: it writes tests_<mode>_only.jsonl and summary_<mode>_only.json, files nothing reads as evidence.
    suffix = "_only" if only else ""
    ARGS.jsonl = os.path.join(ARGS.evidence, "tests_%s%s.jsonl" % (ARGS.mode, suffix))
    open(ARGS.jsonl, "w").close()
    ARGS.ffv = ffmpeg_version()
    STATE["start"] = avail_mb()
    t0 = time.time()
    print("tests/integration/run_checks.py --mode %s   (Avail now %d MB, ffmpeg %s)" % (ARGS.mode, STATE["start"], ARGS.ffv), flush=True)
    timings = []
    for name, modes, fn in REG:
        if only and not any(name == o or name.startswith(o) for o in only):
            continue
        if ARGS.mode not in modes:
            continue
        t1 = time.time()
        try:
            fn()
        except Skip as e:
            record(name, "SKIPPED", "the check runs", "SKIPPED: %s" % e)
        except Blocked as e:
            record(name, "BLOCKED", "the disk guard allows the stage", "BLOCKED: %s" % e)
        except Exception as e:                                           # a crash in a test is a FAIL of that test, with the cleaned message
            record(name, "FAIL", "the check runs to a verdict", "the check crashed: %s: %s" % (type(e).__name__, clean(e, 300)))
        timings.append((time.time() - t1, name))
    if not os.environ.get("LJ_KEEP_WORK"):
        rmtree(ARGS.work)
    secs = time.time() - t0
    print("SUMMARY %s: %d PASS, %d FAIL, %d BLOCKED, %d UNVERIFIED, %d SKIPPED in %.0f s; lowest Avail seen %s MB" % (
        ARGS.mode, COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BLOCKED"], COUNTS["UNVERIFIED"], COUNTS["SKIPPED"], secs, STATE["min_avail"]))
    slow = sorted(timings, reverse=True)[:5]
    print("slowest: " + "; ".join("%s %.1f s" % (n, t) for t, n in slow))
    summ = {"schema": "lj-evidence-summary/1", "package": "WP-11b", "mode": ARGS.mode, "date_utc": TODAY, "counts": COUNTS, "seconds": round(secs, 1), "lowest_avail_mb": STATE["min_avail"],
            "slowest": [{"test": n, "seconds": round(t, 1)} for t, n in slow]}
    if only:
        summ["partial_run_only"] = only
    with open(os.path.join(ARGS.evidence, "summary_%s%s.json" % (ARGS.mode, suffix)), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summ, f, indent=1, sort_keys=True)
        f.write("\n")
    if COUNTS["FAIL"]:
        return 1
    if COUNTS["BLOCKED"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
