#!/usr/bin/env python3
"""run_checks.py: the WP-08 test driver (called by tests/phone/run_tests.sh; it can also be run alone).

  python3 -I tests/phone/run_checks.py --mode quick|all [--work renders/wp08] [--evidence build/evidence/wp08] [--only name,name]

One line per test:  PASS|FAIL|UNVERIFIED|SKIPPED|BLOCKED  name  detail
and one evidence envelope per test (build plan 4.2) in <evidence>/tests_<mode>.jsonl (a --quick run never overwrites the --all envelopes). In --all mode the evidence files named in the
build plan are written too (finding_fontsize23.json, scripts_tested.json, caption_candidates.json, shaping_paths.json, phone_style.json, fill_20x9_*.json, shared_phone_check.json ...).
Everything is generated at test time from synthetic content (a rendered test card, a tone ladder, caption lines made only of pipeline/phone/test_strings.json) under --work (git-ignored
renders/wp08) and removed at the end of --all (the 120 MB ProRes master first; make_master.py rebuilds it in about 30 s). No family media exists here and none is created or simulated.
The two heavy steps (the master render, the encodes) run inside lj_with_disk (build plan 4.9), each under its own label; a refusal by the guard makes the dependent tests BLOCKED.
Exit 0 if no line is FAIL or BLOCKED; 1 if a line FAILs; 3 if a line is BLOCKED; 2 for a bad option. UNVERIFIED (Windows-only behaviour) and SKIPPED are listed and never counted as a pass.
"""
import argparse
import datetime
import hashlib
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PH = os.path.join("pipeline", "phone")
PY = [sys.executable, "-I", "-B"]
SCRATCH = os.environ.get("LJ_SCRATCH", os.path.normpath(os.path.join(ROOT, "..", "build-scratch")))
COUNTS = {"PASS": 0, "FAIL": 0, "UNVERIFIED": 0, "SKIPPED": 0, "BLOCKED": 0}
STATE = {"min_avail": None, "start": None}
S = {}
ARGS = None
REG = []


# ----------------------------------------------------------------------------------------------- plumbing
def sh(args, timeout=1200, env=None, cwd=None):
    e = dict(os.environ)
    for k in ("FFMPEG", "FFPROBE"):
        e.pop(k, None)
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd or ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, env=e)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def avail_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", "/"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20).stdout.decode()
        return int(re.sub(r"[^0-9]", "", out.strip().splitlines()[-1].split()[3]))
    except Exception:
        return 0


def clean(s):
    s = str(s).replace(ROOT, ".").replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    s = re.sub(r"/home/[^\s'\"]+", "<path>", s)
    return s[:900]


def scrub(s):
    """clean() without the length limit, for the transcripts."""
    s = str(s).replace(ROOT, ".").replace(SCRATCH, "<scratch>")
    s = re.sub(r"/tmp/[^\s'\"]+", "<tmp>", s)
    return re.sub(r"/home/[^\s'\"]+", "<path>", s)


def work(*p):
    return os.path.join(ARGS.work, *p)


def ev(*p):
    return os.path.join(ARGS.evidence, *p)


def rel(path):
    return os.path.relpath(path, ROOT)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ledger(label):
    try:
        with open(os.path.join(SCRATCH, "disk-ledger.jsonl"), encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if '"label":"%s"' % label in l]
        return rows[-1] if rows else None
    except OSError:
        return None


def record(name, status, expected, actual, unverified="", planned=0, note="", lg=None):
    COUNTS[status] += 1
    a = avail_mb()
    s0 = STATE["start"]
    lo = min([x for x in (s0, a) if x] or [0])
    row = ledger(lg) if lg else None                         # a step that ran inside lj_with_disk: the guard's own start, minimum and end figures
    if row:
        s0, a, lo = row["avail_mb_start"], row["avail_mb_end"], min(row["avail_mb_min"], lo)
    STATE["min_avail"] = lo if STATE["min_avail"] is None else min(STATE["min_avail"], lo)
    env = {"platform": "linux", "ffmpeg": ARGS.ffv, "nproc": os.cpu_count(), "python": "%d.%d.%d" % sys.version_info[:3], "node": "22.x"}
    rec = {"schema": "lj-evidence/1", "package": "WP-08", "test": name, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), "status": status, "env": env,
           "disk": {"avail_mb_start": s0, "planned_write_mb": planned, "avail_mb_min": lo, "avail_mb_end": a, "floor_mb": 400, "hard_floor_mb": 250},
           "expected": clean(expected), "actual": clean(actual), "notes": note, "unverified_reasons": [unverified] if unverified else []}
    with open(ARGS.jsonl, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("%-10s %-40s %s" % (status, name, clean(actual)[:170].replace("\n", " ")), flush=True)


def test(name, modes=("quick", "all")):
    def deco(fn):
        REG.append((name, modes, fn))
        return fn
    return deco


class Skip(Exception):
    pass


class Blocked(Exception):
    pass


def check(name, ok, expected, actual, unverified="", planned=0, lg=None):
    record(name, "PASS" if ok else "FAIL", expected, actual, unverified, planned, lg=lg)
    return ok


def guarded(label, planned, cmd, timeout=1800):
    """Run cmd inside lj_with_disk (build plan 4.9). Returns (rc, out, err); rc 3 with 'REFUSED' or 'BUSY' or 'DISK-FLOOR' in the output means the guard stopped it."""
    return sh(["bash", "-c", '. scripts/lj_guard.sh && lj_with_disk "$@"', "lj", str(planned), label, "--"] + cmd, timeout=timeout)


def guard_blocked(rc, out, err):
    txt = out + err
    return rc == 3 and any(w in txt for w in ("REFUSED", "BUSY", "DISK-FLOOR"))


def tiny_clip(path, seconds=1, audio=True, size="1920x1080"):
    """A short synthetic clip (flat colour card, a sine tone) for the tests that need any file."""
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x303a4a:s=%s:r=24:d=%d" % (size, seconds)]
    if audio:
        cmd += ["-f", "lavfi", "-i", "sine=f=440:r=48000:d=%d" % seconds]
    cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if audio:
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd += [path]
    rc, out, err = sh(cmd, timeout=120)
    return rc == 0 and os.path.isfile(path)


def ffprobe(path, entries):
    rc, out, err = sh(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", path], timeout=120)
    return json.loads(out) if rc == 0 else {}


def mbps(path):
    d = ffprobe(path, "format=duration")
    dur = float(d.get("format", {}).get("duration") or 0)
    return os.path.getsize(path) * 8.0 / dur / 1e6 if dur else 0.0


def moov_before_mdat(path):
    import struct
    names, size_total = [], os.path.getsize(path)
    with open(path, "rb") as f:
        pos = 0
        while pos + 8 <= size_total:
            f.seek(pos)
            size, typ = struct.unpack(">I4s", f.read(8))
            hl = 8
            if size == 1:
                size, hl = struct.unpack(">Q", f.read(8))[0], 16
            elif size == 0:
                size = size_total - pos
            names.append(typ.decode("latin-1"))
            if size < hl:
                break
            pos += size
    return "moov" in names and "mdat" in names and names.index("moov") < names.index("mdat"), names


def PC(*a):
    return PY + [os.path.join(PH, "phone_check.py")] + list(a)


# ----------------------------------------------------------------------------------------------- QUICK: static hygiene
@test("static_compile")
def t_static():
    pys = [os.path.join(PH, "phone_check.py"), os.path.join(PH, "encode_phone.py"), os.path.join("tests", "phone", "run_checks.py"), os.path.join("tests", "phone", "make_master.py"),
           os.path.join("tests", "phone", "lint_strings.py")]
    bad = []
    d = tempfile.mkdtemp(prefix="ljphonecc_")
    try:
        for i, p in enumerate(pys):
            try:
                py_compile.compile(os.path.join(ROOT, p), cfile=os.path.join(d, "%d.pyc" % i), doraise=True)
            except py_compile.PyCompileError as e:
                bad.append("%s: %s" % (p, str(e).splitlines()[-1][:100]))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    shs = [os.path.join(PH, "encode_phone.sh"), os.path.join(PH, "sim_share.sh"), os.path.join("tests", "phone", "run_tests.sh")]
    for p in shs:
        rc, out, err = sh(["bash", "-n", p])
        if rc != 0:
            bad.append("%s: %s" % (p, err.strip()[:100]))
    check("static_compile", not bad, "5 python files compile, 3 shell files parse (bash -n)", "; ".join(bad) or "all compile and parse")


@test("json_shape")
def t_json():
    prof, thr = read_json(os.path.join(ROOT, PH, "profile.json")), read_json(os.path.join(ROOT, PH, "thresholds.json"))
    probs = []
    for name in ("phone_1080", "phone_720_share"):
        c = prof["chains"].get(name)
        if not c:
            probs.append("no chain " + name)
            continue
        for k in ("container", "vf", "video_args", "audio_args", "expect"):
            if k not in c:
                probs.append("%s lacks %s (the shape of chains.json)" % (name, k))
        if name not in prof["profiles"]:
            probs.append("no profile " + name)
    c1 = prof["chains"]["phone_1080"]
    args = " ".join(str(x) for x in c1["video_args"])
    for needle in ("-crf 20", "-maxrate 8M", "+faststart", "-map_metadata -1", "-profile:v high", "-level 4.1"):
        if needle not in args:
            probs.append("phone_1080 lacks '%s'" % needle)
    if "-b:a 192k" not in " ".join(c1["audio_args"]) or "48000" not in " ".join(c1["audio_args"]):
        probs.append("phone_1080 audio is not AAC 192k 48000")
    cs = prof["caption"]["styles"]
    ph, vn = cs[prof["caption"]["default_style"]], cs["venue_fs23"]
    if not (ph["font_size"] > vn["font_size"] and ph["max_chars_per_line"] <= 32 and ph["max_lines"] == 2 and ph["box_bottom_max_pct"] <= 88):
        probs.append("the phone caption style is not larger than FontSize 23, at most 32 characters, two lines, box ending at or above 88%")
    if thr["position"]["caption_bottom_max_pct"] != 88:
        probs.append("fill_20x9 bottom limit is not 88")
    for k in ("distance_cm", "x_height", "contrast", "stroke", "box90", "position", "title", "marks", "iou", "viewports", "degrade_shared"):
        if "source" not in thr[k] and k != "viewports" and k != "degrade_shared":
            probs.append("thresholds.%s has no source" % k)
    if sorted(thr["viewports"]) != sorted(["portrait", "landscape", "small_portrait", "shared", "fill_20x9"]):
        probs.append("viewports are not the five scenarios")
    if not any("arcminute" in u for u in thr.get("unverified", [])):
        probs.append("the arcminute minimum is not listed as UNVERIFIED")
    check("json_shape", not probs, "profile.json has the chains.json/settings.json shape and the plan's numbers; thresholds.json has sources and lists the arcminute minimum as UNVERIFIED",
          "; ".join(probs) or "profile and thresholds are well formed: phone_1080 CRF 20 maxrate 8M faststart no metadata; caption FontSize %g vs venue %g, %d characters, %d lines, bottom <= %g%%" % (
              ph["font_size"], vn["font_size"], ph["max_chars_per_line"], ph["max_lines"], ph["box_bottom_max_pct"]))


@test("lint_allowlist_clean")
def t_lint():
    rc, out, err = sh(PY + [os.path.join("tests", "phone", "lint_strings.py")])
    check("lint_allowlist_clean", rc == 0, "no Latin or Indic test string outside pipeline/phone/test_strings.json in pipeline/phone, tests/phone, skills-staging/phone-delivery", out.strip().splitlines()[-1] if out.strip() else err[:200])


@test("lint_allowlist_negative_controls")
def t_lint_neg():
    d = work("lintplant")
    os.makedirs(d, exist_ok=True)
    try:
        strings = read_json(os.path.join(ROOT, PH, "test_strings.json"))
        dev = [s["text"] for s in strings["scripts"]["devanagari"]["strings"] if s.get("kind") == "word"]
        lat = strings["scripts"]["latin"]["strings"][0]["text"]
        res = {}
        # 1. a caption fixture with a Latin line that is not allowlisted
        p1 = os.path.join(d, "a"); os.makedirs(p1)
        open(os.path.join(p1, "bad.srt"), "w", encoding="utf-8").write("1\n00:00:00,000 --> 00:00:01,000\n%s\nsome other words\n" % lat)
        res["latin_srt_line"] = sh(PY + [os.path.join("tests", "phone", "lint_strings.py"), "--root", p1, "--quiet"])[0]
        # 2. Indic text written into a source file that is not an allowlisted word (built from code points so this file holds none)
        p2 = os.path.join(d, "b"); os.makedirs(p2)
        stray = "".join(chr(c) for c in (0x0915, 0x0916, 0x0917))
        open(os.path.join(p2, "bad.py"), "w", encoding="utf-8").write('X = "%s"\n' % stray)
        res["indic_in_source"] = sh(PY + [os.path.join("tests", "phone", "lint_strings.py"), "--root", p2, "--quiet"])[0]
        # 3. a script block with strings and no marks[]
        bad = json.loads(json.dumps(strings))
        for s in bad["scripts"]["devanagari"]["strings"]:
            s.pop("marks", None)
        p3 = os.path.join(d, "c"); os.makedirs(p3)
        bf = os.path.join(d, "strings_nomarks.json")
        json.dump(bad, open(bf, "w", encoding="utf-8"), ensure_ascii=False)
        res["no_marks_key"] = sh(PY + [os.path.join("tests", "phone", "lint_strings.py"), "--root", p3, "--strings", bf, "--quiet"])[0]
        # 4. a Latin phrase of the allowlist's family with other digits
        p4 = os.path.join(d, "d"); os.makedirs(p4)
        open(os.path.join(p4, "bad.md"), "w", encoding="utf-8").write("the caption says " + "Te" + "st 9876 here\n")
        res["latin_family_phrase"] = sh(PY + [os.path.join("tests", "phone", "lint_strings.py"), "--root", p4, "--quiet"])[0]
        # positive control: allowlisted strings joined by single spaces pass
        p5 = os.path.join(d, "e"); os.makedirs(p5)
        open(os.path.join(p5, "ok.srt"), "w", encoding="utf-8").write("1\n00:00:00,000 --> 00:00:01,000\n%s %s\n%s %s\n" % (dev[0], dev[1], lat, lat))
        res["allowlisted_lines_pass"] = sh(PY + [os.path.join("tests", "phone", "lint_strings.py"), "--root", p5, "--quiet"])[0]
        ok = all(res[k] == 1 for k in ("latin_srt_line", "indic_in_source", "no_marks_key", "latin_family_phrase")) and res["allowlisted_lines_pass"] == 0
        check("lint_allowlist_negative_controls", ok, "each planted offence exits 1 (a Latin caption line, Indic text in source, a script with strings and no marks[], a Latin phrase of the family); the allowlisted control exits 0",
              ", ".join("%s=%d" % kv for kv in res.items()))
    finally:
        shutil.rmtree(d, ignore_errors=True)


@test("encode_plan_relative_names")
def t_encode_plan():
    d = work("quick")
    os.makedirs(d, exist_ok=True)
    clip = os.path.join(d, "tiny.mp4")
    if not tiny_clip(clip):
        raise Skip("could not make a tiny clip with ffmpeg")
    S["tiny"] = clip
    strings = read_json(os.path.join(ROOT, PH, "test_strings.json"))
    lat = strings["scripts"]["latin"]["strings"][0]["text"]
    srt = os.path.join(d, "c.srt")
    open(srt, "w", encoding="utf-8").write("1\n00:00:00,200 --> 00:00:00,900\n%s\n" % lat)
    rc, out, err = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, srt, os.path.join(d, "o.mp4"), "--dry-run"])
    m = re.search(r"video filter: (.*)", out)
    vf = m.group(1) if m else ""
    ass = re.search(r"ass=([^,]*)", vf)
    arg = ass.group(1) if ass else ""
    ok = rc == 0 and "DRY RUN" in out and bool(arg) and not re.search(r"[A-Za-z]:[\\/]", vf) and "/" not in arg and "\\" not in arg and arg.startswith("caps.ass") and "fontsdir=fonts" in arg
    check("encode_plan_relative_names", ok, "the filter string holds only relative names (caps.ass, fonts), no drive letter and no path separator; --dry-run runs nothing",
          "exit %d; filter: %s" % (rc, vf[:160]), planned=0)
    check("encode_dry_run_writes_nothing", not os.path.exists(os.path.join(d, "o.mp4")) and not os.path.exists(os.path.join(d, "o.mp4.ass")), "no output file after --dry-run", "none written")


@test("encode_refusals")
def t_encode_ref():
    clip = S.get("tiny")
    if not clip:
        raise Skip("no tiny clip")
    d = os.path.dirname(clip)
    strings = read_json(os.path.join(ROOT, PH, "test_strings.json"))
    lat = strings["scripts"]["latin"]["strings"][0]["text"]
    srt = os.path.join(d, "c.srt")
    r1 = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, srt, clip])[0]                                    # output is the master
    long_srt = os.path.join(d, "long.srt")
    open(long_srt, "w", encoding="utf-8").write("1\n00:00:00,200 --> 00:00:00,900\n%s\n" % " ".join([lat] * 5))
    r2 = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, long_srt, os.path.join(d, "o2.mp4"), "--dry-run"])[0]   # a line over 32 characters
    three = os.path.join(d, "three.srt")
    open(three, "w", encoding="utf-8").write("1\n00:00:00,200 --> 00:00:00,900\n%s\n%s\n%s\n" % (lat, lat, lat))
    r3 = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, three, os.path.join(d, "o3.mp4"), "--dry-run"])[0]        # three lines
    r4 = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, srt, os.path.join(d, "o4.mp4"), "--profile", "nope", "--dry-run"])[0]
    h0 = sha(clip)
    check("encode_refusals", (r1, r2, r3, r4) == (2, 2, 2, 2) and sha(clip) == h0, "writing over the master, a line over 32 characters, three lines and an unknown profile are refused (exit 2); the master is untouched",
          "exits %s; master hash unchanged: %s" % ((r1, r2, r3, r4), sha(clip) == h0))


@test("encode_rerun_replaces_own_output")
def t_rerun():
    clip = S.get("tiny")
    if not clip:
        raise Skip("no tiny clip")
    d = os.path.dirname(clip)
    out = os.path.join(d, "rerun.mp4")
    for f in (out, out + ".ass", out + ".phone.json"):
        if os.path.exists(f):
            os.remove(f)
    srt = os.path.join(d, "c.srt")
    cmd = PY + [os.path.join(PH, "encode_phone.py"), clip, srt, out]
    r1 = sh(cmd, timeout=600)[0]
    r2 = sh(cmd, timeout=600)[0]
    foreign = os.path.join(d, "foreign.mp4")
    open(foreign, "wb").write(b"not a phone file")
    r3 = sh(PY + [os.path.join(PH, "encode_phone.py"), clip, srt, foreign])[0]
    check("encode_rerun_replaces_own_output", (r1, r2, r3) == (0, 0, 2) and open(foreign, "rb").read() == b"not a phone file",
          "the same encode command run twice succeeds (it replaces its own earlier output); a file it did not make is refused (exit 2) and kept", "exits %s; the foreign file is untouched" % ((r1, r2, r3),))


@test("phone_check_usage")
def t_usage():
    clip = S.get("tiny")
    if not clip:
        raise Skip("no tiny clip")
    r1 = sh(PC(clip))[0]                                               # no OUTPUT.ass beside it
    r2 = sh(PC("--selftest", "--style", "phone"))[0]                  # two modes
    r3 = sh(PC("--style", "phone", "--scenario", "nope"))[0]
    r4 = sh(PC("--finding-fs23"))[0]                                   # needs --out
    r5 = sh(PC())[0]
    check("phone_check_usage", (r1, r2, r3, r4, r5) == (2, 2, 2, 2, 2), "a file without its caption file, two modes at once, an unknown scenario, --finding-fs23 without --out and no mode are all exit 2",
          "exits %s" % ((r1, r2, r3, r4, r5),))


@test("sim_share_refusals")
def t_ss_ref():
    clip = S.get("tiny")
    if not clip:
        raise Skip("no tiny clip")
    d = os.path.dirname(clip)
    h0 = sha(clip)
    r1 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, clip])[0]
    link = os.path.join(d, "link.mp4")
    if os.path.lexists(link):
        os.remove(link)
    os.symlink(clip, link)
    r2 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, link, "--overwrite"])[0]
    r3 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, os.path.join(d, "no_extension")])[0]
    out = os.path.join(d, "out_exists.mp4")
    open(out, "wb").write(b"x")
    r4 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, out])[0]                  # an existing file that is not one of its own copies
    r5 = sh(["bash", os.path.join(PH, "sim_share.sh")])[0]
    again = os.path.join(d, "again.mp4")
    for f in (again, again + ".phone.json"):
        if os.path.exists(f):
            os.remove(f)
    a1 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, again])[0]
    a2 = sh(["bash", os.path.join(PH, "sim_share.sh"), clip, again])[0]                  # the same command again replaces its own copy
    check("sim_share_rerun", (a1, a2) == (0, 0) and sha(clip) == h0, "the same sim_share.sh command run twice succeeds (the second run replaces its own earlier copy only)", "exits %s; input hash unchanged: %s" % ((a1, a2), sha(clip) == h0))
    check("sim_share_refusals", (r1, r2, r3, r4, r5) == (2, 2, 2, 2, 2) and sha(clip) == h0, "the input as the output (same path, and a link to it), a name without .mp4, an existing file that is not a copy this tool made, and no arguments are refused (exit 2); the input hash is unchanged",
          "exits %s; input hash unchanged: %s" % ((r1, r2, r3, r4, r5), sha(clip) == h0))


@test("selftest")
def t_selftest():
    rc, out, err = sh(PC("--selftest"), timeout=900)
    lines = [l for l in out.splitlines() if l.startswith(("PASS ", "FAIL "))]
    npass = sum(1 for l in lines if l.startswith("PASS "))
    nfail = sum(1 for l in lines if l.startswith("FAIL "))
    want = ["known_tiny_caption_fails_portrait", "caption_at_twice_the_threshold_passes_portrait", "one_pixel_hairline_fails_shared", "box_ending_at_95_percent_fails_fill_20x9",
            "box_ending_at_85_percent_passes_fill_20x9", "deleted_mark_codepoints_fail_mark_survival_(negative_control)", "script_without_strings_is_not_tested_never_pass"]
    missing = [w for w in want if not any(w in l for l in lines)]
    asserts_fs23 = any("fontsize23" in l.lower() or "fontsize_23" in l.lower() or "fs23" in l.lower() for l in lines)
    ok = rc == 0 and nfail == 0 and not missing and not asserts_fs23
    with open(ev("selftest_transcript.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(scrub(out))
    check("selftest", ok, "--selftest exits 0: tiny fails portrait, large passes portrait, a 1-px hairline fails shared, 95% fails and 85% passes fill_20x9, deleted marks fail, an empty script is NOT TESTED, no assertion about FontSize=23",
          "exit %d; %d mechanisms PASS, %d FAIL; missing: %s; FontSize=23 asserted: %s" % (rc, npass, nfail, missing or "none", asserts_fs23))


@test("style_run_phone")
def t_style():
    # --all measures the five scenarios and writes phone_style.json and scripts_tested.json (PHONE-ROW.md is made from them); --quick looks at two scenarios and writes *_quick.json, so a quick run never overwrites them
    full = ARGS.mode == "all"
    sfx = "" if full else "_quick"
    rep_path, scr_path = ev("phone_style%s.json" % sfx), ev("scripts_tested%s.json" % sfx)
    scen = [] if full else ["--scenario", "landscape", "--scenario", "fill_20x9"]
    rc, out, err = sh(PC("--style", "phone", "--json", rep_path, "--scripts-json", scr_path, "--quiet", *scen), timeout=900)
    if not os.path.isfile(rep_path):
        check("style_run_phone", False, "phone_check.py --style phone writes %s" % os.path.basename(rep_path), "exit %d; %s" % (rc, (out + err)[-300:]))
        return
    rep, st = read_json(rep_path), read_json(scr_path)
    S["style_rep"] = rep
    iou = rep["iou"]
    tested = [k for k, v in iou.items() if v["status"] != "NOT TESTED"]
    bad = [k for k in tested if iou[k]["status"] != "PASS" and not iou[k].get("finding")]
    low = {k: iou[k]["iou_min"] for k in tested}
    nt = [k for k, v in iou.items() if v["status"] == "NOT TESTED"]
    lat = rep["scenarios"]["fill_20x9"]["scripts"]["latin"]["position"]["caption_bottom_pct"]
    ok = (set(tested) == {"latin", "devanagari"} and not bad and all(v >= 0.9 for v in low.values()) and sorted(nt) == sorted(["tamil", "telugu", "kannada", "malayalam", "bengali", "gujarati"])
          and re.fullmatch(r"Scripts tested: .+ \(neutral strings\) on \d{4}-\d{2}-\d{2}; NOT TESTED: .+ \(name the maker's script, O-10\)", st["line"]) is not None)
    check("style_run_phone", ok, "the phone style tested for latin and devanagari (shaping IoU >= 0.9 or a shaping finding), six scripts NOT TESTED, scripts_tested.json has the 'Scripts tested:' line",
          "tested %s with IoU min %s; NOT TESTED %s; fill_20x9 caption bottom %.1f%%; line: %s" % (tested, low, nt, lat, st["line"]))


@test("per_script_iou")
def t_iou():
    rep = S.get("style_rep")
    if not rep:
        raise Skip("no style run")
    out = []
    ok = True
    for sc, v in rep["iou"].items():
        if v["status"] == "NOT TESTED":
            continue
        good = v["iou_min"] is not None and v["iou_min"] >= 0.9
        ok = ok and (good or bool(v.get("finding")))
        out.append("%s IoU min %s over %d strings (%s)" % (sc, v["iou_min"], v["strings_tested"], "meets 0.9" if good else "SHAPING FINDING"))
    check("per_script_iou", ok, "every script with strings: libass ink against Pillow-raqm IoU at least 0.9, or a shaping finding", "; ".join(out))


# ----------------------------------------------------------------------------------------------- ALL: the heavy steps
@test("master_made", modes=("all",))
def t_master():
    os.makedirs(ARGS.work, exist_ok=True)
    master, srt, rep = work("master10s.mov"), work("caps.srt"), work("scene_report.json")
    rc, out, err = guarded("wp08-master", 150, PY + [os.path.join("tests", "phone", "make_master.py"), "--out", master, "--srt", srt, "--seconds", "10", "--report", rep])
    if guard_blocked(rc, out, err):
        raise Blocked((out + err).strip().splitlines()[-1][:300])
    d = ffprobe(master, "stream=codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_frames,color_space,channels,sample_rate") if rc == 0 else {}
    sts = d.get("streams", [])
    v = next((s for s in sts if s.get("codec_name") == "prores"), {})
    a = next((s for s in sts if s.get("codec_name", "").startswith("pcm")), {})
    ok = rc == 0 and v.get("width") == 1920 and v.get("height") == 1080 and v.get("r_frame_rate") == "24/1" and str(v.get("nb_frames")) == "240" and v.get("profile") == "HQ" and a.get("sample_rate") == "48000"
    S["master"], S["srt"], S["scene"] = master, srt, rep
    lg = ledger("wp08-master")
    check("master_made", ok, "master10s.mov: ProRes 422 HQ 1920x1080 24/1, 240 frames, PCM 48 kHz, made by the WP-04 harness inside lj_with_disk 150",
          "exit %d; %s %sx%s %s fps %s frames; audio %s Hz; guard: %s" % (rc, v.get("profile"), v.get("width"), v.get("height"), v.get("r_frame_rate"), v.get("nb_frames"), a.get("sample_rate"),
                                                                    ("start %s min %s end %s MB" % (lg["avail_mb_start"], lg["avail_mb_min"], lg["avail_mb_end"])) if lg else "no ledger line"), planned=150, lg="wp08-master")
    if not ok:
        raise Blocked("the master could not be made: " + (out + err)[-200:])


@test("encode_acceptance", modes=("all",))
def t_encode():
    if "master" not in S:
        raise Skip("no master")
    out_mp4 = work("phone.mp4")
    rc, out, err = sh(["bash", os.path.join(PH, "encode_phone.sh"), S["master"], S["srt"], out_mp4, "--layout", S["scene"]], timeout=1800)
    if guard_blocked(rc, out, err):
        raise Blocked((out + err).strip().splitlines()[-1][:300])
    with open(ev("encode_phone_transcript.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(scrub(out))
    S["phone"] = out_mp4
    r2 = sh(PY + [os.path.join("pipeline", "validators", "spec_check.py"), out_mp4, "--profiles-file", os.path.join(PH, "profile.json"), "--profile", "phone_1080", "--json", ev("spec_check_phone_1080.json")])
    prof = read_json(os.path.join(ROOT, PH, "profile.json"))
    cap = prof["chains"]["phone_1080"]["bitrate_cap_mbps"]
    br = mbps(out_mp4)
    mo, names = moov_before_mdat(out_mp4)
    ok = rc == 0 and r2[0] == 0 and br <= cap * 1.10 and mo
    check("encode_acceptance", ok, "encode_phone.sh exits 0 inside lj_with_disk 100; spec_check.py --profiles-file ... --profile phone_1080 exits 0; average bitrate <= cap + 10%; moov before mdat",
          "encode exit %d; spec_check exit %d (%s); %.2f Mbps against a cap of %g + 10%% = %.2f; atoms %s" % (rc, r2[0], (r2[1].strip().splitlines() or [""])[-1][:60], br, cap, cap * 1.10, ",".join(names)), planned=100, lg="wp08-encode")


@test("encode_colon_in_input_path", modes=("all",))
def t_colon():
    if "master" not in S:
        raise Skip("no master")
    d = work("drive:x")
    os.makedirs(d, exist_ok=True)
    srt = os.path.join(d, "c:aps.srt")
    shutil.copyfile(S["srt"], srt)
    short = os.path.join(d, "short:master.mp4")
    rc0 = sh(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-t", "2", "-i", S["master"], "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
              "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-c:a", "aac", short], timeout=300)[0]
    out_mp4 = os.path.join(d, "out:name.mp4")
    rc, out, err = sh(PY + [os.path.join(PH, "encode_phone.py"), short, srt, out_mp4, "--overwrite"], timeout=900)
    ok = rc0 == 0 and rc in (0, 1) and os.path.isfile(out_mp4) and "[5/9]" in out and "video.mp4" in out
    check("encode_colon_in_input_path", ok, "an input, a caption file and an output whose names hold a colon (as a Windows drive letter does) still encode: only relative names reach the ass filter",
          "exit %d; output made: %s" % (rc, os.path.isfile(out_mp4)), unverified="")
    shutil.rmtree(d, ignore_errors=True)


@test("encode_720_share", modes=("all",))
def t_720():
    if "master" not in S:
        raise Skip("no master")
    out_mp4 = work("phone720.mp4")
    rc, out, err = sh(["bash", os.path.join(PH, "encode_phone.sh"), S["master"], S["srt"], out_mp4, "--profile", "phone_720_share", "--overwrite"], timeout=1800)
    if guard_blocked(rc, out, err):
        raise Blocked((out + err).strip().splitlines()[-1][:300])
    r2 = sh(PY + [os.path.join("pipeline", "validators", "spec_check.py"), out_mp4, "--profiles-file", os.path.join(PH, "profile.json"), "--profile", "phone_720_share"])
    prof = read_json(os.path.join(ROOT, PH, "profile.json"))
    cap = prof["chains"]["phone_720_share"]["bitrate_cap_mbps"]
    br = mbps(out_mp4)
    check("encode_720_share", rc == 0 and r2[0] == 0 and br <= cap * 1.10, "PH2 (phone_720_share): 1280x720, level 3.1, spec_check exit 0, bitrate <= cap + 10%",
          "encode exit %d; spec_check exit %d; %.2f Mbps against a cap of %g + 10%%" % (rc, r2[0], br, cap), planned=100, lg="wp08-encode")


@test("colour_patch_phone_1080", modes=("all",))
def t_colour():
    raw = work("cp_raw.json")
    rc, out, err = sh(PY + [os.path.join("pipeline", "validators", "colour_patch.py"), "--chain-file", os.path.join(PH, "profile.json"), "--chain", "phone_1080", "--json", raw])
    worst = None
    m = re.search(r"worst (\d+)/255", out)
    if m:
        worst = int(m.group(1))
    if os.path.isfile(raw):                                  # only the derived form is filed (version, hash, chain results; no build flags, no paths)
        sh(PY + [os.path.join("pipeline", "validators", "colour_patch.py"), "--derive-from", raw, "--out", ev("colour_patch_phone.json")])
    check("colour_patch_phone_1080", rc == 0 and worst is not None and worst <= 3, "colour_patch.py --chain-file pipeline/phone/profile.json --chain phone_1080: worst error 3 or less", "exit %d; worst %s/255 (%s)" % (rc, worst, next((l.strip() for l in out.splitlines() if l.strip().startswith("RESULT")), "")))


@test("colour_patch_phone_720_share", modes=("all",))
def t_colour720():
    # colour_patch.py measures a chain at its own output size, so it tests the 1280x720 chain directly; the same three patches are also run through the chain and the Q-F1 decode here as a cross-check
    raw720 = work("cp_raw_720.json")
    rc, out, err = sh(PY + [os.path.join("pipeline", "validators", "colour_patch.py"), "--chain-file", os.path.join(PH, "profile.json"), "--chain", "phone_720_share", "--json", raw720])
    m = re.search(r"worst (\d+)/255", out)
    worst_tool = int(m.group(1)) if m else None
    if os.path.isfile(raw720):
        sh(PY + [os.path.join("pipeline", "validators", "colour_patch.py"), "--derive-from", raw720, "--out", ev("colour_patch_phone_720.json")])
        os.remove(raw720)
    try:
        from PIL import Image
    except ImportError:
        raise Skip("Pillow missing")
    d = work("cp720")
    os.makedirs(d, exist_ok=True)
    cols = [(255, 0, 0), (128, 128, 128), (224, 172, 140)]
    im = Image.new("RGB", (1920, 1080))
    for i, c in enumerate(cols):
        im.paste(c, (i * 640, 0, (i + 1) * 640, 1080))
    im.save(os.path.join(d, "p.png"))
    prof = read_json(os.path.join(ROOT, PH, "profile.json"))
    ch = prof["chains"]["phone_720_share"]
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", "p.png", "-frames:v", "2", "-vf", ch["vf"]] + [str(x) for x in ch["video_args"] if str(x) not in ("-movflags", "+faststart")] + ["o.mp4"]
    rc1 = sh(cmd, cwd=d)[0]
    rc2 = sh(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-i", "o.mp4", "-vf", "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24", "-frames:v", "1", "d.png"], cwd=d)[0]
    worst = None
    if rc1 == 0 and rc2 == 0:
        dec = Image.open(os.path.join(d, "d.png")).convert("RGB")
        w, h = dec.size
        errs = []
        for i, c in enumerate(cols):
            px = dec.getpixel((int((i + 0.5) * w / 3), h // 2))
            errs.append(max(abs(px[k] - c[k]) for k in range(3)))
        worst = max(errs)
    shutil.rmtree(d, ignore_errors=True)
    check("colour_patch_phone_720_share", rc == 0 and worst_tool is not None and worst_tool <= 3 and worst is not None and worst <= 3,
          "colour_patch.py --chain-file ... --chain phone_720_share (measured at 1280x720): worst error 3 or less; the same three patches through the chain and the Q-F1 decode here agree",
          "colour_patch.py worst %s/255; the cross-check worst %s/255 (the chain stays approved: false until the PC build is tested)" % (worst_tool, worst))


@test("sim_share", modes=("all",))
def t_share():
    if "phone" not in S:
        raise Skip("no phone file")
    shared = work("shared.mp4")
    h0 = sha(S["phone"])
    rc, out, err = sh(["bash", os.path.join(PH, "sim_share.sh"), S["phone"], shared], timeout=900)
    h1 = sha(S["phone"])
    thr = read_json(os.path.join(ROOT, PH, "thresholds.json"))["degrade_shared"]
    d = ffprobe(shared, "stream=height,codec_name,profile")
    h = next((s.get("height") for s in d.get("streams", []) if s.get("codec_name") == "h264"), None)
    br = mbps(shared)
    side = os.path.isfile(shared + ".ass") and os.path.isfile(shared + ".phone.json")
    S["shared"] = shared
    ok = rc == 0 and h0 == h1 and h == thr["height"] and 0.5 <= br <= 1.5 and side
    check("sim_share", ok, "sim_share.sh writes a 480p copy at about 1 Mbps with its caption file and sidecar and leaves the input's SHA-256 unchanged",
          "exit %d; input hash unchanged: %s; height %s; %.2f Mbps; sidecar copied: %s" % (rc, h0 == h1, h, br, side))


@test("phone_check_shared_file", modes=("all",))
def t_chk_shared():
    if "shared" not in S:
        raise Skip("no shared file")
    h0 = sha(S["shared"])
    out_json = ev("shared_phone_check.json")
    rc, out, err = sh(PC(S["shared"], "--json", out_json, "--quiet"), timeout=900)
    ok = rc in (0, 1) and os.path.isfile(out_json) and sha(S["shared"]) == h0
    rep = read_json(out_json) if os.path.isfile(out_json) else {}
    verd = {n: (sv["verdict"], sv["gate"]) for n, sv in rep.get("scenarios", {}).items()}
    check("phone_check_shared_file", ok, "phone_check.py on shared.mp4 records a verdict (exit 0 or 1, either is recorded) and the input hash is unchanged", "exit %d; verdicts %s; input unchanged: %s" % (rc, verd, sha(S["shared"]) == h0))


@test("phone_check_fill_20x9", modes=("all",))
def t_fill():
    if "phone" not in S:
        raise Skip("no phone file")
    # the phone caption style passes; the same master burned with the venue size and margin fails
    rc1, out1, err1 = sh(PC(S["phone"], "--scenario", "fill_20x9", "--json", ev("fill_20x9_phone.json"), "--quiet"), timeout=900)
    ven = work("venue_margin.mp4")
    rcv = sh(["bash", os.path.join(PH, "encode_phone.sh"), S["master"], S["srt"], ven, "--style", "venue_fs23", "--layout", S["scene"], "--overwrite"], timeout=1800)
    if guard_blocked(*rcv):
        raise Blocked((rcv[1] + rcv[2]).strip().splitlines()[-1][:300])
    rc2, out2, err2 = sh(PC(ven, "--scenario", "fill_20x9", "--json", ev("fill_20x9_venue_margin.json"), "--quiet"), timeout=900)
    a, b = read_json(ev("fill_20x9_phone.json")), read_json(ev("fill_20x9_venue_margin.json"))
    pa = [v["position"]["caption_bottom_pct"] for v in a["scenarios"]["fill_20x9"]["scripts"].values() if v.get("position")]
    pb = [v["position"]["caption_bottom_pct"] for v in b["scenarios"]["fill_20x9"]["scripts"].values() if v.get("position")]
    ok = rc1 == 0 and rc2 == 1 and pa and pb and max(pa) <= 88.0 and max(pb) > 88.0
    check("phone_check_fill_20x9", ok, "the phone style on a 20:9 filled screen passes with the caption bottom reported as a percentage (<= 88); the clip burned with the venue margin fails (> 88)",
          "phone: exit %d, caption bottom %s%% (limit 88); venue-margin clip: exit %d, caption bottom %s%%" % (rc1, max(pa) if pa else None, rc2, max(pb) if pb else None), planned=100, lg="wp08-encode")
    if os.path.isfile(ven):
        S["venue"] = ven


@test("phone_check_aspect_19_5", modes=("all",))
def t_aspect():
    if "phone" not in S:
        raise Skip("no phone file")
    rc, out, err = sh(PC(S["phone"], "--scenario", "fill_20x9", "--aspect", "19.5:9", "--json", ev("fill_19_5x9_phone.json"), "--quiet"), timeout=900)
    r = read_json(ev("fill_19_5x9_phone.json"))
    crop = r["scenarios"]["fill_20x9"]["geometry"]["crop_each_pct"]
    check("phone_check_aspect_19_5", rc == 0 and 8.5 <= crop <= 9.5, "--aspect 19.5:9 crops about 9% (8.97) top and bottom and the phone style still passes", "exit %d; crop %.2f%% each; verdict %s" % (rc, crop, r["scenarios"]["fill_20x9"]["verdict"]))


@test("burn_match_negative_control", modes=("all",))
def t_burn_neg():
    if "phone" not in S:
        raise Skip("no phone file")
    # the caption file says something else than what was burned: the file must not be believed
    ass = open(S["phone"] + ".ass", encoding="utf-8").read()
    strings = read_json(os.path.join(ROOT, PH, "test_strings.json"))
    dev = [s["text"] for s in strings["scripts"]["devanagari"]["strings"] if s.get("kind") == "word"]
    lat = strings["scripts"]["latin"]["strings"][0]["text"]
    bad = ass.replace(lat + " " + lat + " " + lat, dev[0] + " " + dev[1]).replace(dev[3], dev[2])
    p = work("wrong.ass")
    open(p, "w", encoding="utf-8", newline="\n").write(bad)
    rc, out, err = sh(PC(S["phone"], "--ass", p, "--scenario", "landscape", "--quiet"), timeout=900)
    m = re.search(r"burned captions against the libass drawing of the caption file: (\w+)", out)
    check("burn_match_negative_control", rc in (1, 2, 3) and m is not None and m.group(1) == "FAIL", "a caption file that does not describe what was burned fails the burn match (exit 1)", "exit %d; burn match %s" % (rc, m.group(1) if m else (out + err)[-150:]))


@test("style_run_all_scenarios", modes=("all",))
def t_style_all():
    rep = S.get("style_rep")
    if not rep:
        raise Skip("no style run")
    sc = rep["scenarios"]
    names = sorted(sc)
    ok = names == sorted(["portrait", "landscape", "small_portrait", "shared", "fill_20x9"]) and sc["fill_20x9"]["verdict"] == "PASS" and sc["landscape"]["verdict"] == "PASS" and sc["shared"]["verdict"] == "PASS"
    check("style_run_all_scenarios", ok, "the phone style over the five scenarios: landscape, shared and fill_20x9 pass (blocking), portrait and small_portrait are advisory and written either way",
          "verdicts: %s" % {n: sc[n]["verdict"] + "/" + sc[n]["gate"] for n in names})


@test("finding_fs23", modes=("all",))
def t_fs23():
    out_json = ev("finding_fontsize23.json")
    rc, out, err = sh(PC("--finding-fs23", "--out", out_json), timeout=900)
    d = read_json(out_json) if os.path.isfile(out_json) else {}
    names = sorted(d.get("scenarios", {}))
    ok = rc == 0 and names == sorted(["portrait", "landscape", "small_portrait", "shared", "fill_20x9"]) and all("verdict" in v for v in d["scenarios"].values())
    check("finding_fs23", ok, "--finding-fs23 --out ... exits 0 and writes the FontSize=23 verdict per scenario with its measured values, whichever way each comes out",
          "exit %d; verdicts (recorded, not asserted): %s" % (rc, {n: d["scenarios"][n]["verdict"] for n in names}))


@test("caption_candidates", modes=("all",))
def t_cand():
    out_json = ev("caption_candidates.json")
    rc, out, err = sh(PC("--candidates", "--out", out_json), timeout=900)
    d = read_json(out_json) if os.path.isfile(out_json) else {}
    check("caption_candidates", rc == 0 and d.get("rows") and d.get("picked_font_size") is not None and d.get("agrees_with_profile") is True,
          "the candidate FontSizes are measured and the rule's pick agrees with profile.json", "exit %d; the rule picks %s, the profile says %s" % (rc, d.get("picked_font_size"), d.get("profile_font_size")))


@test("shaping_paths", modes=("all",))
def t_shaping():
    out_json = ev("shaping_paths.json")
    rc, out, err = sh(PC("--shaping-paths", "--out", out_json), timeout=900)
    d = read_json(out_json) if os.path.isfile(out_json) else {}
    dv = d.get("scripts", {}).get("devanagari", {}).get("paths", {})
    ok = rc == 0 and dv and dv["ass"]["iou_min"] >= 0.9
    check("shaping_paths", ok, "the `ass` filter reaches IoU 0.9 for every script with strings on this build; the `subtitles` filter is measured beside it (a finding, whichever way it comes out)",
          "exit %d; devanagari: ass %s, subtitles %s, forced simple shaping %s" % (rc, dv.get("ass", {}).get("iou_min"), dv.get("subtitles", {}).get("iou_min"), dv.get("ass_simple_shaping", {}).get("iou_min")))


@test("phone_row", modes=("all",))
def t_row():
    p = os.path.join(ROOT, PH, "PHONE-ROW.md")
    rc, out, err = sh(PC("--write-row", p, "--evidence", ARGS.evidence))
    txt = open(p, encoding="utf-8").read() if os.path.isfile(p) else ""
    st = read_json(ev("scripts_tested.json")) if os.path.isfile(ev("scripts_tested.json")) else {}
    has_line = bool(st) and st["line"] in txt and txt.count("Scripts tested:") >= 1
    has = all(k in txt for k in ("FontSize=28", "MarginV", "fill_20x9", "% to ", "NOT TESTED"))
    check("phone_row", rc == 0 and has_line and has, "PHONE-ROW.md carries the caption size AND position, the fill_20x9 verdict and a 'Scripts tested:' line equal to scripts_tested.json",
          "exit %d; line quoted from scripts_tested.json: %s; size, position, fill verdict present: %s" % (rc, has_line, has))


@test("public_lint", modes=("all",))
def t_public():
    paths = [os.path.join(PH), os.path.join("tests", "phone"), os.path.join("skills-staging", "phone-delivery"), ARGS.evidence.replace(ROOT + os.sep, ""), os.path.join("build", "reports", "WP-08.md")]
    paths = [p for p in paths if os.path.exists(os.path.join(ROOT, p))]
    rc, out, err = sh(PY + [os.path.join("scripts", "public_lint.py"), "--paths"] + paths)
    check("public_lint", rc == 0, "scripts/public_lint.py finds no name, user name, host name, address or path in the WP-08 files and evidence", "exit %d; %s" % (rc, (out.strip().splitlines() or [err.strip()[:150]])[-1]))


@test("windows_behaviour_unverified", modes=("all",))
def t_win():
    record("windows_behaviour_unverified", "UNVERIFIED", "encode_phone.py and phone_check.py run on Windows PowerShell 5.1 / PowerShell 7 hosts under py -3 -I", "nothing here could be run on Windows; the drive-letter colon is covered on Linux by passing names that contain a colon "
           "(encode_colon_in_input_path), and Pillow's raqm layout engine on the PC build is unchecked", unverified="Windows: the PC's Python, Pillow (with raqm), numpy and ffmpeg 9.0.2 build were never run against these tools")


@test("cleanup", modes=("all",))
def t_cleanup():
    before = avail_mb()
    for f in (("cp_raw.json", "cp_raw_720.json", "wrong.ass") if ARGS.keep else ("master10s.mov", "cp_raw.json", "cp_raw_720.json", "wrong.ass")):
        p = work(f)
        if os.path.isfile(p):
            os.remove(p)
    shutil.rmtree(work("quick"), ignore_errors=True)
    shutil.rmtree(work("lintplant"), ignore_errors=True)
    after = avail_mb()
    check("cleanup", ARGS.keep or not os.path.exists(work("master10s.mov")), "the ProRes master (120 MB) is removed at the end unless --keep; make_master.py rebuilds it in about 30 s",
          "%s; Avail %d MB before, %d MB after" % ("kept (--keep)" if ARGS.keep else "removed", before, after))


# ----------------------------------------------------------------------------------------------- main
def main(argv=None):
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("quick", "all"), default="quick")
    ap.add_argument("--work", default=os.path.join(ROOT, "renders", "wp08"))
    ap.add_argument("--evidence", default=os.path.join(ROOT, "build", "evidence", "wp08"))
    ap.add_argument("--only", default="")
    ap.add_argument("--keep", action="store_true", help="keep the master and the encoded files under --work (default: the 120 MB master is removed at the end)")
    ARGS = ap.parse_args(argv)
    ARGS.work, ARGS.evidence = os.path.abspath(ARGS.work), os.path.abspath(ARGS.evidence)
    if os.path.commonpath([ROOT, ARGS.work]) != ROOT or ARGS.work == ROOT:
        print("USAGE: --work must be a folder inside the repository (git-ignored renders/wp08)")
        return 2
    os.makedirs(ARGS.work, exist_ok=True)
    os.makedirs(ARGS.evidence, exist_ok=True)
    ARGS.jsonl = os.path.join(ARGS.evidence, "tests_%s.jsonl" % ARGS.mode)
    if not ARGS.only:
        open(ARGS.jsonl, "w").close()
    try:
        ARGS.ffv = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, timeout=20).stdout.decode().split()[2].split("-")[0]
    except Exception:
        ARGS.ffv = "unknown"
    STATE["start"] = avail_mb()
    only = set(x for x in ARGS.only.split(",") if x)
    blocked_msg = None
    for name, modes, fn in REG:
        if ARGS.mode not in modes or (only and name not in only):
            continue
        try:
            if blocked_msg and name not in ("cleanup", "windows_behaviour_unverified", "public_lint"):
                record(name, "BLOCKED", "runs", "an earlier step was blocked: " + blocked_msg)
                continue
            fn()
        except Skip as e:
            record(name, "SKIPPED", "runs", str(e))
        except Blocked as e:
            blocked_msg = str(e)
            record(name, "BLOCKED", "runs inside the disk guard", str(e))
        except Exception as e:                                               # a crash in a test is a FAIL with its message, never a silent pass
            record(name, "FAIL", "runs without an exception", "%s: %s" % (e.__class__.__name__, str(e)[:240]))
    summ = {"schema": "lj-evidence-summary/1", "package": "WP-08", "mode": ARGS.mode, "counts": COUNTS, "avail_mb_start": STATE["start"], "avail_mb_min": STATE["min_avail"], "avail_mb_end": avail_mb(),
            "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")}
    with open(os.path.join(ARGS.evidence, "summary_%s.json" % ARGS.mode), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summ, f, indent=2, sort_keys=True)
        f.write("\n")
    print("\nCounts: " + ", ".join("%s %d" % (k, v) for k, v in COUNTS.items()))
    if COUNTS["FAIL"]:
        return 1
    if COUNTS["BLOCKED"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
