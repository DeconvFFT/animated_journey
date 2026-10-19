#!/usr/bin/env python3
"""WP-04 tests (build plan 5, WP-04, acceptance A1 to A11 and SP2). Run through tests/render/run_tests.sh.

Every test writes one evidence envelope (schema lj-evidence/1) to build/evidence/wp04/<test>.json; tests.jsonl, summary.json and
tests_<mode>.txt summarise a run. Renders go to renders/wp04/ and <scratch>/wp04-*, both git-ignored, and are deleted as soon as hashed.
No identifying data is written: paths are repo-relative or <scratch>, and captured text is scrubbed before it is stored.
"""
import datetime
import glob
import hashlib
import http.client
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRATCH = os.environ.get("LJ_SCRATCH") or os.path.join(os.path.dirname(REPO), "build-scratch")
EVID = os.path.join(REPO, "build", "evidence", "wp04")
RENDERS = os.path.join(REPO, "renders", "wp04")
RENDER = ["node", "pipeline/bin/render.mjs"]
SCENE = ["--dir", "pipeline", "--mount", "/vendor=vendor"]
TESTCARD = "scenes/testcard/scene.html"
FLAT = "scenes/testcard/flat.html"
ENVV = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
TESTS = []  # (name, fn, quick)


# --------------------------------------------------------------------------------------------------------------- plumbing
def test(name, quick=False):
    def deco(fn):
        TESTS.append((name, fn, quick))
        return fn
    return deco


def scrub(text):
    if text is None:
        return ""
    t = str(text)
    t = t.replace(SCRATCH, "<scratch>").replace(REPO, "<repo>")
    t = re.sub(r"/root(/[^\s'\"]*)?", "<home>", t)
    t = re.sub(r"/home/[A-Za-z0-9_.-]+(/[^\s'\"]*)?", lambda m: "/home/user" + (m.group(1) or ""), t)
    return t


def avail_mb():
    st = os.statvfs("/")
    return math.ceil(st.f_bavail * st.f_frsize / 1048576)


def sh(cmd, timeout=900, env=None, cwd=REPO, input_text=None):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env or ENVV, input=input_text)
        return r.returncode, r.stdout, r.stderr, time.time() - t0
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT after %ss" % timeout, time.time() - t0


def render(args, timeout=600, env=None, bench=False, label=None, planned_mb=None):
    """Run render.mjs; bench=True puts it under lj_bench, planned_mb puts it under lj_with_disk as well."""
    cmd = RENDER + args
    if bench:
        cmd = ["bash", "scripts/lj_guard.sh", "bench"] + cmd
    if planned_mb:
        cmd = ["bash", "scripts/lj_guard.sh", "with_disk", str(planned_mb), label or "wp04-render", "--"] + cmd
    e = dict(ENVV)
    if env:
        e.update(env)
    if label:
        e["LJ_BENCH_LABEL"] = label
    return sh(cmd, timeout=timeout, env=e)


def settle(max_s=150):
    """Wait until the 1-minute load average is under the guard's contamination limit (0.25 x nproc), so a timed run is not contaminated by the test
    that ran just before it. If other jobs keep the machine busy the run goes ahead and lj_bench flags it contaminated, as it should."""
    lim = 0.25 * (os.cpu_count() or 1)
    t0 = time.time()
    while True:
        l1 = float(open("/proc/loadavg").read().split()[0])
        if l1 <= lim or time.time() - t0 >= max_s:
            return {"settled": l1 <= lim, "load1": l1, "waited_s": round(time.time() - t0)}
        time.sleep(5)


def last_json(text):
    for line in reversed((text or "").strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except ValueError:
                continue
    return None


def rel(p):
    return os.path.relpath(p, REPO) if os.path.isabs(p) and p.startswith(REPO) else p


def rmtree(p):
    shutil.rmtree(p, ignore_errors=True)


def frames(d):
    return sorted(glob.glob(os.path.join(d, "f_*.png")))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def hashes(d):
    return {os.path.basename(f): sha(f) for f in frames(d)}


def ae(a, b, fuzz="1%"):
    """differing pixels, ImageMagick compare -metric AE -fuzz (the plan's tolerance test)"""
    r = subprocess.run(["compare", "-metric", "AE", "-fuzz", fuzz, a, b, "null:"], capture_output=True, text=True)
    m = re.match(r"\s*([0-9.e+]+)", r.stderr or "")
    if not m:
        raise RuntimeError("compare gave no number: " + (r.stderr or "")[:200])
    return int(float(m.group(1)))


def tool_version(cmd, rx):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        m = re.search(rx, r.stdout + r.stderr)
        return m.group(1) if m else None
    except OSError:
        return None


def ffprobe(path, entries="width,height,r_frame_rate,avg_frame_rate,nb_frames,pix_fmt,color_range,color_space,color_primaries,color_transfer,codec_name"):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=" + entries, "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


def result(status, expected, actual, notes="", data=None, unverified=None, planned_mb=0, avail_min=None):
    return {"status": status, "expected": expected, "actual": actual, "notes": notes, "data": data or {}, "unverified": unverified or [], "planned_mb": planned_mb, "avail_min": avail_min}


def envelope(name, res, start_mb, end_mb):
    mins = [x for x in (start_mb, end_mb, res.get("avail_min")) if x is not None]
    return {
        "schema": "lj-evidence/1", "package": "WP-04", "test": name, "date_utc": TODAY, "status": res["status"],
        "env": {"platform": "linux", "ffmpeg": tool_version(["ffmpeg", "-version"], r"ffmpeg version (\S+)"), "nproc": os.cpu_count(),
                "python": "%d.%d.x" % sys.version_info[:2], "node": tool_version(["node", "--version"], r"v?(\S+)"), "chromium": CHROMIUM[0]},
        "disk": {"avail_mb_start": start_mb, "planned_write_mb": res.get("planned_mb", 0), "avail_mb_min": min(mins), "avail_mb_end": end_mb, "floor_mb": 400, "hard_floor_mb": 250},
        "expected": scrub(res["expected"]), "actual": scrub(res["actual"]), "notes": scrub(res["notes"]), "unverified_reasons": res["unverified"],
        "data": json.loads(scrub(json.dumps(res["data"], ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)))),
    }


CHROMIUM = [None]


def note_chromium(rep):
    if rep and rep.get("chromium"):
        CHROMIUM[0] = rep["chromium"]


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def bench_note(stderr):
    m = re.search(r"bench: nproc=(\d+) loadavg_start=(\S+ \S+ \S+) contaminated=(\w+)", stderr or "")
    return {"nproc": int(m.group(1)), "loadavg_start": m.group(2), "contaminated": m.group(3)} if m else None


def descendants(pid):
    out, stack = [], [pid]
    while stack:
        p = stack.pop()
        try:
            kids = [int(x) for x in open("/proc/%d/task/%d/children" % (p, p)).read().split()]
        except OSError:
            kids = []
        out += kids
        stack += kids
    return out


def alive(pid):
    try:
        os.kill(pid, 0)
        with open("/proc/%d/stat" % pid) as f:
            return f.read().split(")")[-1].split()[0] != "Z"
    except OSError:
        return False


# --------------------------------------------------------------------------------------------------------------- quick tests
@test("args_usage", quick=True)
def t_args_usage():
    base = ["--dir", "pipeline", "--page", FLAT]
    cases = [
        (["--bogus"], 2), ([], 2), (["--page", "x", "--shard", "3/2"], 2), (["--page", "x", "--seconds", "1", "--frames", "0:5"], 2),
        (["--page", "x", "--fps", "abc"], 2), (["--dir", "pipeline", "--page", "nope.html"], 2), (["--dir", "pipeline", "--page", "../README.md"], 2),
        (base + ["--mount", "novalue"], 2), (base + ["--mount", "/v=does-not-exist"], 2), (base + ["--mount", "/=pipeline"], 2),
        (base + ["--chain", "nosuch", "--ffmpeg", "x.mp4"], 2), (base + ["--chain", "h264", "--shard", "0/2"], 2), (base + ["--frames", "5:5"], 2),
        (base + ["--concurrency", "9"], 2), (base + ["--w", "5"], 2), (base + ["--alpha=yes"], 2),
        (base + ["--out", "renders/wp04/_usage", "--seconds", "1"], 3, {"PW_CHROMIUM": "/nonexistent/chrome"}),
    ]
    rows, bad = [], []
    for c in cases:
        args, want = c[0], c[1]
        rc, out, err, _ = render(args, timeout=60, env=c[2] if len(c) > 2 else None)
        rows.append({"args": " ".join(args), "exit": rc, "want": want, "stderr": scrub(err.strip().splitlines()[0] if err.strip() else "")})
        if rc != want:
            bad.append(rows[-1])
    rc, out, err, _ = render(["--help"], timeout=30)
    rows.append({"args": "--help", "exit": rc, "want": 0, "mentions_seekTo": "seekTo" in out})
    if rc != 0 or "seekTo" not in out:
        bad.append(rows[-1])
    rc, out, err, _ = render(base + ["--chain", "h264", "--ffmpeg", "renders/wp04/_usage/x.mp4", "--seconds", "1", "--ffmpeg-bin", "/nonexistent/ffmpeg"], timeout=90)
    rows.append({"args": "--ffmpeg-bin /nonexistent", "exit": rc, "want": 3, "stderr": scrub(err.strip().splitlines()[-1] if err.strip() else "")})
    if rc != 3 or os.path.exists(os.path.join(RENDERS, "_usage", "x.mp4")) or os.path.exists(os.path.join(RENDERS, "_usage", "x.mp4.partial")):
        bad.append(rows[-1])
    rmtree(os.path.join(RENDERS, "_usage"))
    return result("PASS" if not bad else "FAIL", "%d bad-usage and environment cases exit 2 or 3 with a message; --help exits 0" % (len(cases) + 2), "%d of %d cases as wanted" % (len(rows) - len(bad), len(rows)), data={"cases": rows, "bad": bad})


@test("strings_file", quick=True)
def t_strings():
    path = os.path.join(REPO, "pipeline", "phone", "test_strings.json")
    raw = open(path, "rb").read()
    problems = []
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("file has a BOM")
    d = json.loads(raw.decode("utf-8"))
    if d.get("schema") != "lj-teststrings/1" or "rules" not in d:
        problems.append("schema or rules missing")
    sc = d.get("scripts", {})
    want_pending = ["tamil", "telugu", "kannada", "malayalam", "bengali", "gujarati"]
    for s in want_pending:
        if sc.get(s) != {"status": "pending_O-10", "strings": []}:
            problems.append("%s is not an empty pending_O-10 block" % s)
    lat = sc.get("latin", {})
    if lat.get("font_script_tag") != "Latn" or [x["id"] for x in lat.get("strings", [])] != ["lat-test"] or lat["strings"][0]["text"] != "Test 0123":
        problems.append("latin entry differs from 4.15")
    dev = sc.get("devanagari", {})
    if dev.get("font_script_tag") != "Deva" or dev.get("noto_family") != "Noto Sans Devanagari" or dev.get("headline") is not True:
        problems.append("devanagari header differs from 4.15")
    want = {"dev-digits": "\u0966\u0967\u0968\u0969\u096a\u096b\u096c\u096d\u096e\u096f", "dev-pariksha": "\u092a\u0930\u0940\u0915\u094d\u0937\u0923",
            "dev-pustak": "\u092a\u0941\u0938\u094d\u0924\u0915", "dev-din": "\u0926\u093f\u0928", "dev-sankhya": "\u0938\u0902\u0916\u094d\u092f\u093e", "dev-shabd": "\u0936\u092c\u094d\u0926"}
    got = {x["id"]: x["text"] for x in dev.get("strings", [])}
    if got != want:
        problems.append("devanagari strings differ from the frozen day-1 list: %s" % sorted(set(got.items()) ^ set(want.items())))
    kinds = {"above", "below", "pre_base", "post_base", "split", "conjunct"}
    for x in dev.get("strings", []):
        if x.get("checked_by_reader") is not False:
            problems.append("%s: checked_by_reader must be the boolean false until the maker confirms" % x["id"])
        if not isinstance(x.get("marks"), list):
            problems.append("%s: marks[] missing" % x["id"])
        for m in x.get("marks", []):
            if m.get("kind") not in kinds:
                problems.append("%s: unknown mark kind %s" % (x["id"], m.get("kind")))
            for cp in m.get("codepoints", []):
                if not re.fullmatch(r"U\+[0-9A-F]{4}", cp) or chr(int(cp[2:], 16)) not in x["text"]:
                    problems.append("%s: mark %s does not occur in the text" % (x["id"], cp))
        for ch in x["text"]:
            o = ord(ch)
            if not (0x0900 <= o <= 0x097F) or o in (0x0950, 0x0964, 0x0965, 0x0970):
                problems.append("%s: character U+%04X is outside the neutral Devanagari set (no OM sign, no danda, no abbreviation sign)" % (x["id"], o))
        if x["kind"] == "word" and not x.get("gloss"):
            problems.append("%s: gloss missing" % x["id"])
    for name, blk in sc.items():
        for x in blk.get("strings", []):
            if "checked_by_reader" not in x:
                problems.append("%s: no checked_by_reader" % x.get("id"))
    return result("PASS" if not problems else "FAIL", "4.15 v1: Latin entry, Devanagari digits and five plain nouns with marks[] and checked_by_reader false, six empty pending_O-10 blocks, neutral characters only",
                  "ok" if not problems else "; ".join(problems), data={"scripts_with_strings": [k for k, v in sc.items() if v.get("strings")], "pending": want_pending, "devanagari_ids": sorted(got)})


@test("libs_lock", quick=True)
def t_libs_lock():
    problems = []
    lock = read_json(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"))
    if lock.get("schema") != "lj-libs/1":
        problems.append("schema")
    rc, out, err, _ = sh(["bash", "pipeline/lib/fetch_libs.sh", "--check"], timeout=60)
    if rc != 0:
        problems.append("fetch_libs.sh --check exit %d: %s" % (rc, out.strip().splitlines()[-1] if out.strip() else err.strip()))
    hexre = re.compile(r"^[0-9a-f]{64}$")
    n_files = 0
    for e in lock["libs"] + lock["fonts"]:
        lic = os.path.join(REPO, "pipeline", "lib", e["licence_file"])
        fetched = e.get("version") and (e.get("files") or e.get("faces"))
        if fetched and not os.path.isfile(lic):
            problems.append("licence text missing for %s" % e["id"])
        if fetched and not hexre.match(e["tarball"]["sha256"]):
            problems.append("tarball sha256 malformed for %s" % e["id"])
        recs = e.get("files", []) + [x for f in e.get("faces", []) for x in f["files"].values()]
        for r in recs:
            n_files += 1
            if not hexre.match(r["sha256"]) or r["to"].startswith("/") or ".." in r["to"]:
                problems.append("bad file record %s" % r["to"])
    gs = [e for e in lock["libs"] if e["id"] == "gsap"][0]
    if gs.get("committed") is not False or not gs.get("version"):
        problems.append("gsap must be locked with committed false")
    r1 = subprocess.run(["git", "check-ignore", "-q", "vendor/js/gsap.min.js"], cwd=REPO)
    tracked = subprocess.run(["git", "ls-files", "vendor"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    if r1.returncode != 0 or tracked:
        problems.append("vendor/ is not git-ignored or something under it is tracked")
    pend = [e for e in lock["fonts"] if e["status"] == "pending_O-10"]
    if sorted(s for e in pend for s in e["scripts"]) != sorted(["tamil", "telugu", "kannada", "malayalam", "bengali", "gujarati"]):
        problems.append("pending script fonts differ from the six scripts of 4.15")
    day1 = sorted(e["id"] for e in lock["fonts"] if e["status"] == "day1")
    if day1 != ["kalam", "noto-sans", "noto-sans-devanagari"]:
        problems.append("day-1 fonts: %s" % day1)
    txt = open(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"), encoding="utf-8").read()
    if re.search(r"/home/|/root|C:\\\\Users", txt):
        problems.append("an absolute path is in the lock file")
    return result("PASS" if not problems else "FAIL", "lock parses, every fetched file matches its SHA-256, licence texts exist, gsap not committed, vendor/ ignored, six pending script fonts",
                  "ok (%d file records, %d pending script fonts)" % (n_files, len(pend)) if not problems else "; ".join(problems),
                  data={"gsap_version": gs.get("version"), "day1": day1, "pending": [e["id"] for e in pend], "pending_confirmed": {e["id"]: e.get("package_confirmed") for e in pend}})


@test("fetch_libs_offline", quick=True)
def t_fetch_offline():
    work = os.path.join(SCRATCH, "wp04-offline")
    rmtree(work)
    os.makedirs(os.path.join(work, "lib"))
    lock = read_json(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"))
    for e in lock["libs"] + lock["fonts"]:
        for k in ("version", "tarball", "files", "faces", "fetched", "fetched_utc_date", "licence_declared"):
            e.pop(k, None)
        if e.get("status") != "day1" and "npm" in e:
            e["package_confirmed"] = True
    json.dump(lock, open(os.path.join(work, "lib", "libs.lock.json"), "w"), indent=1)
    before = sha(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"))
    env = dict(ENVV, npm_config_registry="http://127.0.0.1:9/", npm_config_fetch_retries="0", npm_config_fetch_retry_mintimeout="100", npm_config_fetch_timeout="5000")
    env.pop("npm_config_https_proxy", None)
    env["npm_config_noproxy"] = "127.0.0.1"
    rc, out, err, secs = sh(["bash", "pipeline/lib/fetch_libs.sh", "--vendor", os.path.join(work, "vendor"), "--lock", os.path.join(work, "lib", "libs.lock.json")], timeout=120, env=env)
    after = sha(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"))
    wrote = glob.glob(os.path.join(work, "vendor", "**", "*"), recursive=True)
    ok = rc == 3 and "npm failed" in err and re.search(r"ECONNREFUSED|ENOTFOUND|EAI_AGAIN|ETIMEDOUT|ECONNRESET|fetch failed|network", err) and before == after and not [w for w in wrote if os.path.isfile(w)]
    first = [l for l in err.splitlines() if l.strip()][:6]
    rmtree(work)
    return result("PASS" if ok else "FAIL", "registry unreachable: exit 3, the exact npm error printed, nothing written, repo lock unchanged",
                  "exit %d; stderr (first lines): %s" % (rc, " | ".join(first)), data={"exit": rc, "stderr_head": first, "seconds": round(secs, 1)})


A9_CANARY = "CANARY-PARENT-FILE-0001"


def serve(dir_, extra=()):
    p = subprocess.Popen(RENDER + ["--serve", "--dir", dir_] + list(extra), cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=ENVV)
    line = p.stdout.readline()
    info = json.loads(line)
    port = int(re.search(r":(\d+)/", info["serving"]).group(1))
    return p, port


def listen_addrs(port):
    """local addresses of the listening TCP sockets on this port (from /proc/net/tcp and tcp6)"""
    found = set()
    for fn, v6 in (("/proc/net/tcp", False), ("/proc/net/tcp6", True)):
        try:
            lines = open(fn).read().splitlines()[1:]
        except OSError:
            continue
        for ln in lines:
            f = ln.split()
            addr, prt = f[1].split(":")
            if f[3] == "0A" and int(prt, 16) == port:
                if not v6:
                    found.add(".".join(str(int(addr[i:i + 2], 16)) for i in (6, 4, 2, 0)))
                else:
                    found.add("v6:" + addr)
    return found


def raw_get(port, path, method="GET", host=None):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    c.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
    c.putheader("Host", host or "127.0.0.1:%d" % port)
    c.endheaders()
    r = c.getresponse()
    body = r.read().decode("utf-8", "replace")
    c.close()
    return r.status, body


@test("a9_path_safety", quick=True)
def t_a9():
    work = os.path.join(SCRATCH, "wp04-a9")
    rmtree(work)
    os.makedirs(os.path.join(work, "root", "sub"))
    os.makedirs(os.path.join(work, "mnt"))
    open(os.path.join(work, "package.json"), "w").write(A9_CANARY)           # the canary lives ABOVE the served root
    open(os.path.join(work, "root", "ok.txt"), "w").write("OK")
    open(os.path.join(work, "root", "sub", "in.txt"), "w").write("IN")
    open(os.path.join(work, "mnt", "m.txt"), "w").write("MOUNT")
    os.symlink(os.path.join(work, "package.json"), os.path.join(work, "root", "link.json"))
    p, port = serve(os.path.join(work, "root"), ["--mount", "/m=" + os.path.join(work, "mnt")])
    rows, bad = [], []
    try:
        cases = [("GET", "/ok.txt", 200, "OK"), ("GET", "/sub/in.txt", 200, "IN"), ("HEAD", "/ok.txt", 200, None), ("GET", "/m/m.txt", 200, "MOUNT"),
                 ("GET", "/ok.txt?x=1#frag", 200, "OK"),
                 ("GET", "/../package.json", 404, None), ("GET", "/%2e%2e/package.json", 404, None), ("GET", "/%2E%2E/package.json", 404, None),
                 ("GET", "/sub/%2e%2e/%2e%2e/package.json", 404, None), ("GET", "/sub/../../package.json", 404, None), ("GET", "/..%2fpackage.json", 404, None),
                 ("GET", "/%2e%2e%2fpackage.json", 404, None), ("GET", "/%252e%252e/package.json", 404, None), ("GET", "/m/../package.json", 404, None),
                 ("GET", "/m/%2e%2e/root/ok.txt", 404, None), ("GET", "/..\\package.json", 404, None), ("GET", "/%5c..%5cpackage.json", 404, None),
                 ("GET", "/link.json", 404, None), ("GET", "/%00", 404, None), ("GET", "/", 404, None), ("GET", "/%zz", 400, None), ("POST", "/ok.txt", 405, None)]
        for method, path, want, body in cases:
            st, b = raw_get(port, path, method)
            leaked = A9_CANARY in b
            ok = st == want and (body is None or b == body) and not leaked
            rows.append({"method": method, "path": path, "status": st, "want": want, "leaked_canary": leaked})
            if not ok:
                bad.append(rows[-1])
        st, b = raw_get(port, "/ok.txt", host="evil.example:80")
        rows.append({"method": "GET", "path": "/ok.txt", "host": "evil.example", "status": st, "want": 403})
        if st != 403:
            bad.append(rows[-1])
        bound_local = listen_addrs(port) == {"127.0.0.1"}
        rows.append({"check": "listens on 127.0.0.1 only", "listening_addresses": sorted(listen_addrs(port)), "bound_local_only": bound_local})
        if not bound_local:
            bad.append(rows[-1])
    finally:
        p.terminate()
        p.wait(timeout=10)
    # negative control: the unfixed R7 handler (path.join of the decoded URL, no root check) leaks the canary through the same request
    ctl = os.path.join(work, "r7_unfixed.mjs")
    open(ctl, "w").write("import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';\n"
                         "const root = process.argv[2];\n"
                         "const srv = http.createServer((q, r) => fs.readFile(path.join(root, decodeURIComponent(q.url.split('?')[0])), (e, b) => e ? (r.writeHead(404), r.end()) : (r.writeHead(200), r.end(b)))).listen(0, '127.0.0.1', () => console.log(srv.address().port));\n")
    cp = subprocess.Popen(["node", ctl, os.path.join(work, "root")], stdout=subprocess.PIPE, text=True, cwd=work)
    cport = int(cp.stdout.readline())
    try:
        st, b = raw_get(cport, "/%2e%2e/package.json")
    finally:
        cp.terminate()
        cp.wait(timeout=10)
    control_leaks = st == 200 and A9_CANARY in b
    rows.append({"check": "negative control: unfixed R7 handler serves the canary", "status": st, "leaks": control_leaks})
    if not control_leaks:
        bad.append(rows[-1])
    rmtree(work)
    return result("PASS" if not bad else "FAIL", "/../package.json and /%2e%2e/... return 404 (also encoded, double-encoded, backslash, symlink and mount variants); the unfixed R7 handler leaks the canary (control)",
                  "%d checks, %d wrong" % (len(rows), len(bad)), data={"rows": rows, "bad": bad})


def clean_out(*names):
    for n in names:
        rmtree(os.path.join(RENDERS, n))


@test("a8_errors", quick=True)
def t_a8():
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet"]
    rows, bad = [], []

    def check(name, cond, detail):
        rows.append({"check": name, "ok": bool(cond), "detail": detail})
        if not cond:
            bad.append(rows[-1])
    clean_out("a8t", "a8a", "a8f", "a8n", "a8v")
    # ?throw=1: exits 2, no frame of this run is left (the throw is at t >= 0.5, so frames 0-11 were written first and removed again)
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?throw=1", "--out", "renders/wp04/a8t", "--seconds", "2", "--json", "renders/wp04/a8t.json"], timeout=120)
    rep = read_json(os.path.join(RENDERS, "a8t.json"))
    note_chromium(rep)
    left = os.listdir(os.path.join(RENDERS, "a8t")) if os.path.isdir(os.path.join(RENDERS, "a8t")) else []
    check("throw=1 exit 2", rc == 2, "exit %d" % rc)
    check("throw=1 leaves no frame and no .tmp", not [f for f in left if f.startswith("f_") or f.endswith(".tmp")], "left: %s" % left)
    check("throw=1 message names the planned error", "planned" in err, scrub(err.strip().splitlines()[-2] if err.strip() else ""))
    check("throw=1 report records the error and the removal", rep.get("ok") is False and rep.get("output_removed") is True and rep.get("error", {}).get("kind") == "scene", json.dumps(rep.get("error")))
    # ?throw=async: only an uncaught error. Default: frames kept, exit 2 at the end. --fail-on-pageerror: stop at once, output removed.
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?throw=async", "--out", "renders/wp04/a8a", "--seconds", "0.5"], timeout=120)
    n = len(frames(os.path.join(RENDERS, "a8a")))
    check("throw=async default: all frames kept, exit 2", rc == 2 and n == 12, "exit %d, %d frames" % (rc, n))
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?throw=async", "--out", "renders/wp04/a8f", "--seconds", "0.5", "--fail-on-pageerror"], timeout=120)
    left = os.listdir(os.path.join(RENDERS, "a8f")) if os.path.isdir(os.path.join(RENDERS, "a8f")) else []
    check("throw=async --fail-on-pageerror: exit 2, no frames", rc == 2 and not [f for f in left if f.startswith("f_") or f.endswith(".tmp")], "exit %d, left %s" % (rc, left))
    # video mode: no partial file
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?throw=1", "--seconds", "2", "--chain", "h264", "--ffmpeg", "renders/wp04/a8v/x.mp4"], timeout=120)
    vleft = os.listdir(os.path.join(RENDERS, "a8v")) if os.path.isdir(os.path.join(RENDERS, "a8v")) else []
    check("throw=1 in video mode: exit 2, no output file, no .partial", rc == 2 and not vleft, "exit %d, left %s" % (rc, vleft))
    # ?net=1: exit 2 naming the URL
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?net=1", "--out", "renders/wp04/a8n", "--seconds", "1", "--json", "renders/wp04/a8n.json"], timeout=120)
    rep = read_json(os.path.join(RENDERS, "a8n.json"))
    url = "https://example.invalid/lj-net-probe.png"
    left = os.listdir(os.path.join(RENDERS, "a8n")) if os.path.isdir(os.path.join(RENDERS, "a8n")) else []
    check("net=1 exit 2", rc == 2, "exit %d" % rc)
    check("net=1 names the blocked URL", url in err and url in rep.get("blocked_requests", []), scrub(err.strip().splitlines()[-2] if err.strip() else ""))
    check("net=1 leaves no frame", not [f for f in left if f.startswith("f_") or f.endswith(".tmp")], "left %s" % left)
    clean_out("a8t", "a8a", "a8f", "a8n", "a8v")
    for f in ("a8t.json", "a8n.json"):
        try:
            os.unlink(os.path.join(RENDERS, f))
        except OSError:
            pass
    return result("PASS" if not bad else "FAIL", "?throw=1 exits 2 with no partial output; ?net=1 exits 2 naming the URL; --fail-on-pageerror stops at the first uncaught error", "%d checks, %d failed" % (len(rows), len(bad)), data={"checks": rows})


@test("a10_alpha", quick=True)
def t_a10():
    clean_out("a10", "a10n")
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet"]
    rc, out, err, _ = render(base + ["--page", TESTCARD + "?alpha=1", "--out", "renders/wp04/a10", "--frames", "0:3", "--alpha"], timeout=120)
    f0 = os.path.join(RENDERS, "a10", "f_000000.png")
    ident = subprocess.run(["identify", "-format", "%[channels] %[opaque]", f0], capture_output=True, text=True).stdout.strip() if rc == 0 else ""
    from PIL import Image
    im = Image.open(f0).convert("RGBA") if rc == 0 else None
    corner_a = im.getpixel((2, 2))[3] if im else None
    title_a = max(im.getpixel((x, 60))[3] for x in range(70, 400)) if im else None
    rc2, _, _, _ = render(base + ["--page", TESTCARD, "--out", "renders/wp04/a10n", "--frames", "0:1"], timeout=120)
    ident2 = subprocess.run(["identify", "-format", "%[channels] %[opaque]", os.path.join(RENDERS, "a10n", "f_000000.png")], capture_output=True, text=True).stdout.strip() if rc2 == 0 else ""
    clean_out("a10", "a10n")
    ok = rc == 0 and ident.startswith("srgba") and ident.lower().endswith("false") and corner_a == 0 and title_a == 255 and rc2 == 0 and not ident2.startswith("srgba")
    return result("PASS" if ok else "FAIL", "--alpha frames report an alpha channel (identify %[channels] gives srgba, not opaque); background alpha 0, text alpha 255; frames without --alpha have none",
                  "with --alpha: '%s', corner alpha %s, text alpha %s; without: '%s'" % (ident, corner_a, title_a, ident2), data={"alpha_identify": ident, "corner_alpha": corner_a, "text_alpha": title_a, "plain_identify": ident2})


@test("colour_patches", quick=True)
def t_patches():
    clean_out("cp")
    rc, out, err, _ = render(["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD, "--out", "renders/wp04/cp", "--frames", "0:1", "--json", "renders/wp04/cp.json"], timeout=120)
    from PIL import Image
    rep = read_json(os.path.join(RENDERS, "cp.json"))
    note_chromium(rep)
    im = Image.open(os.path.join(RENDERS, "cp", "f_000000.png")).convert("RGB")
    want = [((255, 0, 0), 930 + 160), ((128, 128, 128), 930 + 480), ((224, 172, 140), 930 + 800)]
    rows = []
    for rgb, cx in want:
        px = [im.getpixel((cx + dx, 767 + dy)) for dx in range(-60, 61, 20) for dy in range(-20, 21, 10)]
        rows.append({"want": rgb, "all_equal": all(p == rgb for p in px), "sample": px[0]})
    clean_out("cp")
    try:
        os.unlink(os.path.join(RENDERS, "cp.json"))
    except OSError:
        pass
    ok = rc == 0 and all(r["all_equal"] for r in rows) and im.size == (1920, 1080)
    return result("PASS" if ok else "FAIL", "the three-patch strip is exactly 255,0,0 / 128,128,128 / 224,172,140 in the PNG (no colour management shift), frame 1920x1080", json.dumps(rows), data={"patches": rows, "size": im.size})


@test("chain_parity", quick=True)
def t_chain_parity():
    """The built-in h264 chain (used when pipeline/lib/chains.json is absent) must equal h264_venue in that file; WP-11b asserts it again."""
    cf = os.path.join(REPO, "pipeline", "lib", "chains.json")
    rc, out, err, _ = sh(["node", "-e", "import('./pipeline/bin/render.mjs').then(m => console.log(JSON.stringify(m.BUILTIN_CHAINS.h264)))"], timeout=30)
    if rc != 0:
        return result("FAIL", "the built-in chain can be read", scrub(err[-300:]))
    builtin = json.loads(out.strip().splitlines()[-1])
    if not os.path.isfile(cf):
        return result("SKIPPED", "built-in h264 equals h264_venue in chains.json", "SKIPPED: pipeline/lib/chains.json has not landed (WP-05)", data={"builtin": builtin})
    fc = read_json(cf)["chains"]["h264_venue"]
    keys = ("container", "vf", "video_args", "expect", "expect_extra")
    diffs = {k: {"built_in": builtin.get(k), "chains_json": fc.get(k)} for k in keys if builtin.get(k) != fc.get(k)}
    rc2, out2, err2, _ = render(["--list-chains"], timeout=30)
    rc3, out3, err3, _ = render(["--list-chains", "--chains-file", "does-not-exist.json"], timeout=30)
    ok = not diffs and rc2 == 0 and "h264\tchains.json:h264_venue" in out2 and rc3 == 0 and "h264\tbuilt-in" in out3
    return result("PASS" if ok else "FAIL", "built-in h264 equals h264_venue (container, vf, video_args, expect); --chain h264 resolves to the file when present and to the built-in when it is not",
                  "differences: %s; with the file: %s; without: %s" % (diffs or "none", out2.splitlines()[0] if out2 else "", out3.strip()), data={"differences": diffs})


@test("a1_determinism_lite", quick=True)
def t_a1_lite():
    clean_out("a1l1", "a1l2")
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD, "--frames", "0:6"]
    r1 = render(base + ["--out", "renders/wp04/a1l1"], timeout=120)
    r2 = render(base + ["--out", "renders/wp04/a1l2"], timeout=120)
    h1, h2 = hashes(os.path.join(RENDERS, "a1l1")), hashes(os.path.join(RENDERS, "a1l2"))
    clean_out("a1l1", "a1l2")
    ok = r1[0] == 0 and r2[0] == 0 and len(h1) == 6 and h1 == h2
    return result("PASS" if ok else "FAIL", "two separate processes, frames 0-5: identical SHA-256 (the full 48-frame A1 runs under --all)", "%d/%d frames identical" % (sum(h1[k] == h2.get(k) for k in h1), len(h1)))


# --------------------------------------------------------------------------------------------------------------- full tests
@test("a1_determinism")
def t_a1():
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--frames", "0:48"]
    clean_out("a1x", "a1y", "a1fx", "a1fy")
    rows = {}
    # filter off: exact
    r1 = render(base + ["--page", TESTCARD, "--out", "renders/wp04/a1x", "--json", "renders/wp04/a1x.json"], timeout=300)
    r2 = render(base + ["--page", TESTCARD, "--out", "renders/wp04/a1y"], timeout=300)
    h1, h2 = hashes(os.path.join(RENDERS, "a1x")), hashes(os.path.join(RENDERS, "a1y"))
    rep = read_json(os.path.join(RENDERS, "a1x.json"))
    note_chromium(rep)
    rep_ok = all(rep["frame_sha256"][str(i)] == h1["f_%06d.png" % i] for i in range(48))
    same = sum(h1.get(k) == h2.get(k) for k in h1)
    rows["filter_off"] = {"frames": len(h1), "identical": same, "report_hashes_match_files": rep_ok, "exit": [r1[0], r2[0]]}
    # filter on: at most 100 differing pixels per frame
    f1 = render(base + ["--page", TESTCARD + "?filter=1", "--out", "renders/wp04/a1fx"], timeout=300)
    f2 = render(base + ["--page", TESTCARD + "?filter=1", "--out", "renders/wp04/a1fy"], timeout=300)
    diffs = [ae(a, b) for a, b in zip(frames(os.path.join(RENDERS, "a1fx")), frames(os.path.join(RENDERS, "a1fy")))]
    hf1, hf2 = hashes(os.path.join(RENDERS, "a1fx")), hashes(os.path.join(RENDERS, "a1fy"))
    rows["filter_on"] = {"frames": len(diffs), "max_differing_px": max(diffs) if diffs else None, "hash_identical": sum(hf1.get(k) == hf2.get(k) for k in hf1), "exit": [f1[0], f2[0]]}
    # the filter variant really differs from the plain one (the filter is exercised)
    d_plain_vs_filter = ae(frames(os.path.join(RENDERS, "a1x"))[20], frames(os.path.join(RENDERS, "a1fx"))[20])
    rows["filter_changes_pixels"] = d_plain_vs_filter
    clean_out("a1x", "a1y", "a1fx", "a1fy")
    try:
        os.unlink(os.path.join(RENDERS, "a1x.json"))
    except OSError:
        pass
    ok = (rows["filter_off"]["identical"] == 48 and rep_ok and r1[0] == 0 and r2[0] == 0 and len(diffs) == 48 and max(diffs) <= 100 and f1[0] == 0 and f2[0] == 0 and d_plain_vs_filter > 100)
    return result("PASS" if ok else "FAIL", "two processes, frames 0-47: identical SHA-256 per frame (filter off); at most 100 differing pixels per frame with ?filter=1 (compare -metric AE -fuzz 1%)",
                  "filter off: %d/48 identical; filter on: max %s differing px (%d hash-identical); filter changes %d px" % (same, rows["filter_on"]["max_differing_px"], rows["filter_on"]["hash_identical"], d_plain_vs_filter), data=rows)


@test("a2_negative_control")
def t_a2():
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--frames", "0:6", "--page", TESTCARD + "?random=1"]
    clean_out("a2x", "a2y")
    r1 = render(base + ["--out", "renders/wp04/a2x"], timeout=200)
    r2 = render(base + ["--out", "renders/wp04/a2y"], timeout=200)
    diffs = [ae(a, b) for a, b in zip(frames(os.path.join(RENDERS, "a2x")), frames(os.path.join(RENDERS, "a2y")))]
    h1, h2 = hashes(os.path.join(RENDERS, "a2x")), hashes(os.path.join(RENDERS, "a2y"))
    clean_out("a2x", "a2y")
    ok = r1[0] == 0 and r2[0] == 0 and len(diffs) == 6 and min(diffs) > 100 and not any(h1[k] == h2[k] for k in h1)
    return result("PASS" if ok else "FAIL", "?random=1 frames from two processes differ by more than 100 pixels (the determinism test catches a nondeterministic scene)",
                  "differing pixels per frame: %s" % diffs, data={"differing_px": diffs, "hash_identical": sum(h1[k] == h2[k] for k in h1)})


@test("a3_shards_resume")
def t_a3():
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD, "--frames", "0:48"]
    clean_out("a3s", "a3p")
    r1 = render(base + ["--out", "renders/wp04/a3s"], timeout=300)
    single = hashes(os.path.join(RENDERS, "a3s"))
    ps = [subprocess.Popen(RENDER + base + ["--out", "renders/wp04/a3p", "--shard", "%d/2" % i], cwd=REPO, env=ENVV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in (0, 1)]
    outs = [p.communicate(timeout=300) for p in ps]
    sharded = hashes(os.path.join(RENDERS, "a3p"))
    equal = single == sharded and len(single) == 48
    j = [last_json(o[0]) for o in outs]
    disjoint = j[0]["frames"] == 24 and j[1]["frames"] == 24
    # a second invocation renders 0 frames (both shards, and the whole range)
    r2 = render(base + ["--out", "renders/wp04/a3p", "--shard", "0/2"], timeout=200)
    r3 = render(base + ["--out", "renders/wp04/a3p"], timeout=200)
    j2, j3 = last_json(r2[1]), last_json(r3[1])
    tmp_left = glob.glob(os.path.join(RENDERS, "a3p", "*.tmp"))
    # a different scene into the same folder is refused (resume must not trust frames from another scene)
    r4 = render(["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--frames", "0:48", "--page", TESTCARD + "?push=layout", "--out", "renders/wp04/a3p"], timeout=120)
    refused = r4[0] == 2 and "different scene" in r4[2]
    ok = r1[0] == 0 and equal and disjoint and j2 and j2["frames"] == 0 and j2["skipped"] == 24 and j3 and j3["frames"] == 0 and j3["skipped"] == 48 and not tmp_left and refused
    clean_out("a3s", "a3p")
    return result("PASS" if ok else "FAIL", "shards 0/2 + 1/2 equal a single run frame for frame (hash-identical, disjoint); a second invocation renders 0 frames; a changed scene in the same folder is refused",
                  "equal=%s shard frames %s/%s; rerun shard: %s; rerun whole: %s; refused different scene: %s" % (equal, j[0]["frames"], j[1]["frames"], {k: j2[k] for k in ("frames", "skipped")} if j2 else None, {k: j3[k] for k in ("frames", "skipped")} if j3 else None, refused),
                  data={"identical": sum(single[k] == sharded.get(k) for k in single), "second_invocation": [j2, j3], "refusal": scrub(r4[2].strip().splitlines()[-1] if r4[2].strip() else "")})


@test("history_independence")
def t_history():
    """SP2 finding: without --disable-partial-raster and --disable-gpu-compositing a frame's edge pixels depend on the frames rendered before it in the same page.
    The flat SVG scene rendered by 1 page and by 4 pages must give identical frames with the harness defaults; the negative control drops both flags
    (PW_DROP_FLAGS) and must reproduce differences, so this test provably catches the problem."""
    base = ["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:96"]

    def digest_pair(env):
        out = {}
        for n in (1, 4):
            clean_out("hi%d" % n)
            r = render(base + ["--out", "renders/wp04/hi%d" % n, "--concurrency", str(n)], timeout=300, env=env)
            out[n] = hashes(os.path.join(RENDERS, "hi%d" % n))
            out["rc%d" % n] = r[0]
            clean_out("hi%d" % n)
        return sum(out[1].get(k) != out[4].get(k) for k in out[1]), len(out[1]), (out["rc1"], out["rc4"])
    d_def, n_def, rc_def = digest_pair(None)
    d_ctl, n_ctl, rc_ctl = digest_pair({"PW_DROP_FLAGS": "--disable-partial-raster --disable-gpu-compositing"})
    ok = rc_def == (0, 0) and rc_ctl == (0, 0) and n_def == 96 and n_ctl == 96 and d_def == 0 and d_ctl > 0
    return result("PASS" if ok else "FAIL", "with the harness defaults 1 page and 4 pages give identical frames (0 of 96 differ); with both flags dropped (negative control) they differ",
                  "defaults: %d of %d frames differ; control without the two flags: %d of %d frames differ" % (d_def, n_def, d_ctl, n_ctl),
                  data={"defaults_differing_frames": d_def, "control_differing_frames": d_ctl, "frames": n_def, "dropped_flags": ["--disable-partial-raster", "--disable-gpu-compositing"]})


@test("a4_kill_resume")
def t_a4():
    # SP2 g. flat.html keeps the 240-frame runs small (about 6 MB); resume mechanics do not depend on the scene.
    base = ["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:240"]
    clean_out("a4ref", "a4k")
    ref = render(base + ["--out", "renders/wp04/a4ref", "--json", "renders/wp04/a4ref.json"], timeout=600)
    ref_h = hashes(os.path.join(RENDERS, "a4ref"))
    rep = read_json(os.path.join(RENDERS, "a4ref.json"))
    note_chromium(rep)
    p = subprocess.Popen(RENDER + base + ["--out", "renders/wp04/a4k"], cwd=REPO, env=ENVV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    t0 = time.time()
    n = 0
    while time.time() - t0 < 300 and p.poll() is None:
        n = len(frames(os.path.join(RENDERS, "a4k")))
        if n >= 120:
            break
        time.sleep(0.05)
    kids = descendants(p.pid)
    profile_dirs = set()
    for k in kids:                                     # a SIGKILLed Playwright cannot remove Chromium's temp profile: find it before the kill, remove it after
        try:
            for a in open("/proc/%d/cmdline" % k, "rb").read().split(b"\0"):
                if a.startswith(b"--user-data-dir="):
                    profile_dirs.add(a.split(b"=", 1)[1].decode())
        except OSError:
            pass
    killed_at = len(frames(os.path.join(RENDERS, "a4k")))
    os.kill(p.pid, signal.SIGKILL)
    p.wait(timeout=30)
    time.sleep(0.2)
    orphans = []
    for _ in range(100):
        orphans = [k for k in kids if alive(k)]
        if not orphans:
            break
        time.sleep(0.1)
    leaked_children = list(orphans)
    for k in orphans:
        try:
            os.kill(k, signal.SIGKILL)
        except OSError:
            pass
    time.sleep(0.5)
    for d in profile_dirs:
        if os.path.basename(d).startswith("playwright_chromiumdev_profile-") and os.path.dirname(d) == "/tmp":
            rmtree(d)
    after_kill = len(frames(os.path.join(RENDERS, "a4k")))
    tmp_after_kill = len(glob.glob(os.path.join(RENDERS, "a4k", "*.tmp")))
    # the kill may or may not have caught a frame mid-write: plant both artefacts so the sweep and the truncation check are always exercised
    out_dir = os.path.join(RENDERS, "a4k")
    open(os.path.join(out_dir, "f_000239.png.tmp"), "wb").write(b"half a frame")
    victim = frames(out_dir)[killed_at // 2]
    with open(victim, "r+b") as f:
        f.truncate(1000)
    planted = {"tmp": "f_000239.png.tmp", "truncated": os.path.basename(victim)}
    res = render(base + ["--out", "renders/wp04/a4k", "--json", "renders/wp04/a4k.json"], timeout=600)
    rrep = read_json(os.path.join(RENDERS, "a4k.json"))
    final_h = hashes(out_dir)
    tmp_final = glob.glob(os.path.join(out_dir, "*.tmp"))
    equal = final_h == ref_h and len(final_h) == 240
    ok = (ref[0] == 0 and len(ref_h) == 240 and 100 <= killed_at < 240 and res[0] == 0 and equal and not tmp_final and not leaked_children
          and rrep["frames_skipped_existing"] == after_kill - 1 and rrep["frames_rendered"] == 240 - (after_kill - 1))
    clean_out("a4ref", "a4k")
    for f in ("a4ref.json", "a4k.json"):
        try:
            os.unlink(os.path.join(RENDERS, f))
        except OSError:
            pass
    return result("PASS" if ok else "FAIL", "SIGKILL a 240-frame run at about 50%; the rerun completes; no .tmp files; 240 frames; hashes equal an uninterrupted run",
                  "killed with %d frames on disk; resume rendered %d, skipped %d; final 240 frames equal reference: %s; .tmp left: %d; browser processes left behind: %d" % (killed_at, rrep["frames_rendered"], rrep["frames_skipped_existing"], equal, len(tmp_final), len(leaked_children)),
                  data={"killed_at_frames": killed_at, "frames_after_kill": after_kill, "tmp_after_kill": tmp_after_kill, "planted": planted, "resume": {k: rrep[k] for k in ("frames_rendered", "frames_skipped_existing")}, "leaked_children": len(leaked_children), "scene": "flat.html"})


@test("a5_chain_output")
def t_a5():
    clean_out("a5")
    os.makedirs(os.path.join(RENDERS, "a5"))
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD, "--seconds", "2"]
    r = render(base + ["--chain", "h264", "--ffmpeg", "renders/wp04/a5/out.mp4", "--json", "renders/wp04/a5/out.json"], timeout=300)
    rep = read_json(os.path.join(RENDERS, "a5", "out.json"))
    note_chromium(rep)
    st = ffprobe(os.path.join(RENDERS, "a5", "out.mp4"))
    want = {"width": 1920, "height": 1080, "r_frame_rate": "24/1", "nb_frames": "48", "pix_fmt": "yuv420p", "color_range": "tv", "color_space": "bt709", "color_primaries": "bt709", "color_transfer": "bt709", "codec_name": "h264"}
    got = {k: (st.get(k) if k in ("width", "height") else str(st.get(k))) for k in want}
    mism = {k: (got[k], v) for k, v in want.items() if got[k] != v}
    dec = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(RENDERS, "a5", "out.mp4"), "-f", "null", "-"], capture_output=True, text=True)
    pngs = glob.glob(os.path.join(RENDERS, "a5", "*.png"))
    # encode the same range from PNG frames (the sharded workflow): same tags, same frame count
    # the same chain from the built-in table (chains.json hidden): same tags, same bytes as the file's h264_venue when the two are equal
    rb = render(base + ["--chains-file", "does-not-exist.json", "--chain", "h264", "--ffmpeg", "renders/wp04/a5/builtin.mp4"], timeout=300)
    stb = ffprobe(os.path.join(RENDERS, "a5", "builtin.mp4")) if rb[0] == 0 else {}
    gotb = {k: (stb.get(k) if k in ("width", "height") else str(stb.get(k))) for k in want}
    mismb = {k: (gotb[k], v) for k, v in want.items() if gotb[k] != v}
    builtin_same = rb[0] == 0 and sha(os.path.join(RENDERS, "a5", "out.mp4")) == sha(os.path.join(RENDERS, "a5", "builtin.mp4"))
    r2 = render(base + ["--out", "renders/wp04/a5/frames", "--json", "renders/wp04/a5/png.json"], timeout=300)
    r3 = render(base + ["--out", "renders/wp04/a5/frames", "--encode", "--chain", "h264", "--ffmpeg", "renders/wp04/a5/enc.mp4", "--json", "renders/wp04/a5/enc.json"], timeout=300)
    st2 = ffprobe(os.path.join(RENDERS, "a5", "enc.mp4"))
    got2 = {k: (st2.get(k) if k in ("width", "height") else str(st2.get(k))) for k in want}
    mism2 = {k: (got2[k], v) for k, v in want.items() if got2[k] != v}
    same_bytes = sha(os.path.join(RENDERS, "a5", "out.mp4")) == sha(os.path.join(RENDERS, "a5", "enc.mp4"))
    size = os.path.getsize(os.path.join(RENDERS, "a5", "out.mp4"))
    profile = st.get("profile") if False else ffprobe(os.path.join(RENDERS, "a5", "out.mp4"), "profile").get("profile")
    ok = r[0] == 0 and not mism and dec.returncode == 0 and dec.stderr.strip() == "" and not pngs and rep["chain_check"]["ok"] and r2[0] == 0 and r3[0] == 0 and not mism2 and rb[0] == 0 and not mismb and profile == "High"
    clean_out("a5")
    return result("PASS" if ok else "FAIL", "--chain h264 writes 48 frames; ffprobe 1920x1080, r_frame_rate 24/1, nb_frames 48, yuv420p, tv, bt709 matrix/primaries/transfer; decodes clean; no PNGs written in video mode",
                  "ffprobe: %s; mismatches: %s; decode errors: '%s'; --encode from PNG frames mismatches: %s; piped and PNG-encoded files byte-identical: %s" % (json.dumps(got), mism, dec.stderr.strip()[:80], mism2, same_bytes),
                  data={"ffprobe": got, "file_bytes": size, "chain_check_in_report": rep["chain_check"]["ok"], "encode_from_frames_ffprobe": got2, "byte_identical_pipe_vs_png": same_bytes, "profile": profile, "builtin_chain_ffprobe": gotb, "builtin_byte_identical_to_chains_json": builtin_same, "chain_source": rep["chain"]["source"]})


@test("a6_flat_fps")
def t_a6_fps():
    clean_out("a6f")
    st = settle()
    r = render(["--dir", "pipeline", "--quiet", "--page", FLAT, "--out", "renders/wp04/a6f", "--frames", "0:96", "--json", "renders/wp04/a6f.json"], timeout=600, bench=True, label="wp04-a6-flat")
    rep = read_json(os.path.join(RENDERS, "a6f.json"))
    note_chromium(rep)
    n = len(frames(os.path.join(RENDERS, "a6f")))
    clean_out("a6f")
    try:
        os.unlink(os.path.join(RENDERS, "a6f.json"))
    except OSError:
        pass
    fps = rep["throughput_fps"]
    return result("PASS" if r[0] == 0 and n == 96 and fps >= 8 else "FAIL", "flat scene at least 8 fps (R11 pass mark); actual recorded; peak RSS recorded",
                  "%.2f fps over 96 frames (%.1f s), peak RSS %s" % (fps, rep["seconds_render"], rep["peak_rss"]),
                  data={"settle": st, "throughput_fps": fps, "seconds_render": rep["seconds_render"], "peak_rss": rep["peak_rss"], "bench": bench_note(r[2]), "report_bench": rep.get("bench")})


@test("a6_concurrency")
def t_a6_conc():
    rows = {}
    for n in (1, 2, 4):
        clean_out("a6c")
        st = settle(90)
        r = render(["--dir", "pipeline", "--quiet", "--page", FLAT, "--out", "renders/wp04/a6c", "--frames", "0:96", "--concurrency", str(n), "--json", "renders/wp04/a6c.json"], timeout=600, bench=True, label="wp04-a6-conc%d" % n)
        rep = read_json(os.path.join(RENDERS, "a6c.json"))
        note_chromium(rep)
        h = hashes(os.path.join(RENDERS, "a6c"))
        rows[str(n)] = {"settle": st, "exit": r[0], "frames": len(h), "throughput_fps": rep["throughput_fps"], "seconds_render": rep["seconds_render"], "peak_rss": rep["peak_rss"], "bench": bench_note(r[2]), "digest": rep["frame_sha256_digest"]}
    clean_out("a6c")
    try:
        os.unlink(os.path.join(RENDERS, "a6c.json"))
    except OSError:
        pass
    same = len({v["digest"] for v in rows.values()}) == 1
    ok = all(v["exit"] == 0 and v["frames"] == 96 for v in rows.values()) and same
    best = max(rows, key=lambda k: rows[k]["throughput_fps"])
    return result("PASS" if ok else "FAIL", "1, 2 and 4 concurrent pages timed on the flat scene; frames identical at every level (SP2 e)",
                  "fps by pages: %s; best %s pages; frame digests identical across levels: %s" % ({k: v["throughput_fps"] for k, v in rows.items()}, best, same), data={"by_pages": rows, "best_pages": int(best), "digests_identical": same})


@test("testcard_fps")
def t_testcard_fps():
    """Informational: speed on the heavy scene (full-frame texture, text, grid) for budgeting. The R11 pass mark applies to the flat scene (a6_flat_fps)."""
    rows = {}
    for n in (1, 4):
        clean_out("tf")
        st = settle(90)
        r = render(["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD, "--out", "renders/wp04/tf", "--frames", "0:96", "--concurrency", str(n), "--json", "renders/wp04/tf.json"], timeout=600, bench=True, label="wp04-testcard-c%d" % n)
        rep = read_json(os.path.join(RENDERS, "tf.json"))
        note_chromium(rep)
        png_bytes = sum(os.path.getsize(f) for f in frames(os.path.join(RENDERS, "tf")))
        rows[str(n)] = {"settle": st, "exit": r[0], "frames": rep["frames_rendered"], "throughput_fps": rep["throughput_fps"], "peak_rss": rep["peak_rss"], "bench": bench_note(r[2]), "avg_png_kb": round(png_bytes / max(rep["frames_rendered"], 1) / 1024)}
    clean_out("tf")
    try:
        os.unlink(os.path.join(RENDERS, "tf.json"))
    except OSError:
        pass
    ok = all(v["exit"] == 0 and v["frames"] == 96 for v in rows.values())
    return result("PASS" if ok else "FAIL", "speed of the full test card recorded for budgeting (no pass mark)",
                  "fps by pages: %s; average PNG %s KB" % ({k: v["throughput_fps"] for k, v in rows.items()}, rows["1"]["avg_png_kb"]), data={"by_pages": rows})


@test("a6_chapter_2400")
def t_a6_chapter():
    # SP2 f: a 100 s chapter (2,400 frames) piped straight into ffmpeg; no PNG ever written. One lj_with_disk stage (250 MB planned in the plan;
    # the guard decides). The plan's 250 is a ceiling; when the guard refuses it the figure is computed from a measured 240-frame clip (4.9: computed, not guessed).
    out_dir = os.path.join(RENDERS, "a6")
    clean_out("a6")
    os.makedirs(out_dir)
    settle()
    best = 2
    try:
        prev = read_json(os.path.join(EVID, "a6_concurrency.json"))
        best = prev["data"]["best_pages"]
    except (OSError, KeyError, ValueError):
        pass
    cal = render(["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:240", "--chain", "h264", "--ffmpeg", "renders/wp04/a6/cal.mp4", "--concurrency", str(best)], timeout=300)
    cal_bytes = os.path.getsize(os.path.join(out_dir, "cal.mp4")) if cal[0] == 0 else None
    os.unlink(os.path.join(out_dir, "cal.mp4")) if cal_bytes else None
    est_mb = int(math.ceil(cal_bytes * 10 * 1.5 / 1048576)) + 5 if cal_bytes else 250     # 10 x the 240-frame clip, 1.5 x margin, 5 MB of ffmpeg and temp files
    planned = 250
    args = ["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:2400", "--chain", "h264", "--ffmpeg", "renders/wp04/a6/chapter.mp4", "--concurrency", str(best), "--json", "renders/wp04/a6/chapter.json"]
    cmd = ["bash", "scripts/lj_guard.sh", "with_disk", str(planned), "wp04-a6-chapter", "--", "bash", "scripts/lj_guard.sh", "bench"] + RENDER + args
    sampler = {"png_max": 0, "tmp_max": 0, "bytes_max": 0, "samples": 0}
    note = ""

    def run_staged(cmd, planned):
        env = dict(ENVV, LJ_BENCH_LABEL="wp04-a6-chapter")
        p = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while p.poll() is None:
            names = os.listdir(out_dir)
            sampler["png_max"] = max(sampler["png_max"], len([n for n in names if n.endswith(".png")]))
            sampler["tmp_max"] = max(sampler["tmp_max"], len([n for n in names if n.endswith(".tmp")]))
            sampler["bytes_max"] = max(sampler["bytes_max"], sum(os.path.getsize(os.path.join(out_dir, n)) for n in names))
            sampler["samples"] += 1
            time.sleep(2)
        o, e = p.communicate()
        return p.returncode, o, e

    # the volume is shared and other jobs write to it: wait (up to 10 minutes) until the guard's own rule, Avail - planned >= 400 MB, can hold; the guard stays the authority
    need = est_mb + 400 + 3
    waited, t_w = 0, time.time()
    while avail_mb() < need and time.time() - t_w < 600:
        time.sleep(10)
    waited = round(time.time() - t_w)
    a0 = avail_mb()
    rc, o, e = run_staged(cmd, planned)
    guard_msg = scrub(e)
    if rc == 3 and "REFUSED" in e:
        first_refusal = [l for l in e.splitlines() if "REFUSED" in l][0]
        planned = est_mb
        cmd = ["bash", "scripts/lj_guard.sh", "with_disk", str(planned), "wp04-a6-chapter", "--", "bash", "scripts/lj_guard.sh", "bench"] + RENDER + args
        note = "the guard refused the plan's 250 MB at Avail %d MB (%s); PLANNED_MB recomputed from a measured 240-frame clip (%d bytes): %d MB" % (a0, scrub(first_refusal.strip()), cal_bytes or 0, planned)
        rc, o, e = run_staged(cmd, planned)
        guard_msg = scrub(e)
    a1 = avail_mb()
    ledger = subprocess.run(["bash", "scripts/lj_guard.sh", "ledger", "wp04-a6-chapter"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    try:
        led = json.loads(ledger)
    except ValueError:
        led = {}
    if rc == 3 and ("REFUSED" in e or "BUSY" in e or "DISK-FLOOR" in e):
        clean_out("a6")
        return result("BLOCKED", "2,400 frames piped into ffmpeg under one lj_with_disk stage", "guard: " + guard_msg.strip().splitlines()[-1], notes=note + " Waited %d s for headroom first." % waited, planned_mb=planned, data={"guard": guard_msg.strip().splitlines()[-3:], "ledger": led, "waited_for_disk_s": waited})
    rep = read_json(os.path.join(out_dir, "chapter.json"))
    note_chromium(rep)
    st = ffprobe(os.path.join(out_dir, "chapter.mp4"))
    size = os.path.getsize(os.path.join(out_dir, "chapter.mp4"))
    pngs = len(glob.glob(os.path.join(out_dir, "*.png")))
    expect = {"nb_frames": "2400", "width": 1920, "height": 1080, "pix_fmt": "yuv420p", "r_frame_rate": "24/1"}
    got = {k: (st.get(k) if k in ("width", "height") else str(st.get(k))) for k in expect}
    # the encoded run must fit the plan: the disk the run used is the output file, not 2,400 PNGs (a flat PNG is about 25 KB; 2,400 would be tens of MB)
    ok = rc == 0 and got == expect and pngs == 0 and sampler["png_max"] == 0 and sampler["tmp_max"] == 0 and rep["chain_check"]["ok"] and rep["frames_rendered"] == 2400
    clean_out("a6")
    fps = rep["throughput_fps"]
    return result("PASS" if ok else "FAIL", "a 2,400-frame (100 s) run piped straight into ffmpeg completes with no PNG accumulation (disk used equals the output size, not the frame count); peak RSS recorded",
                  "%d frames in %.1f s (%.2f fps, %d pages); output %d bytes; PNG files seen during the run: %d; peak RSS %s; Avail %d -> %d MB; ledger min %s MB" % (rep["frames_rendered"], rep["seconds_render"], fps, best, size, sampler["png_max"], rep["peak_rss"], a0, a1, led.get("avail_mb_min")),
                  notes=note, planned_mb=planned, avail_min=led.get("avail_mb_min"),
                  data={"frames": rep["frames_rendered"], "seconds_render": rep["seconds_render"], "throughput_fps": fps, "concurrency": best, "peak_rss": rep["peak_rss"], "output_bytes": size, "ffprobe": got, "png_files_max_seen": sampler["png_max"], "tmp_files_max_seen": sampler["tmp_max"], "dir_bytes_max_seen": sampler["bytes_max"], "samples": sampler["samples"],
                        "ledger": led, "calibration_bytes_240": cal_bytes, "plan_planned_mb": 250, "used_planned_mb": planned, "waited_for_disk_s": waited, "bench": rep.get("bench")})


@test("a6_chapter_2400_ram")
def t_chapter_ram():
    """Fallback for SP2 (f) when the guarded stage above is BLOCKED because the shared volume has no headroom: the same 2,400-frame run, output written to RAM-backed /dev/shm
    so the volume is not touched at all (nothing for the guard to protect), still timed under lj_bench. It does not replace the guarded stage: that stays BLOCKED until
    Avail - planned >= 400 MB and is rerun then. Skipped when the guarded stage ran."""
    try:
        prev = read_json(os.path.join(EVID, "a6_chapter_2400.json"))
    except (OSError, ValueError):
        prev = None
    if prev and prev["status"] == "PASS":
        return result("SKIPPED", "fallback only when the guarded 2,400-frame stage is BLOCKED", "SKIPPED: the guarded stage ran and passed")
    shm = "/dev/shm/lj-wp04-a6"
    rmtree(shm)
    os.makedirs(shm)
    best = 4
    try:
        best = read_json(os.path.join(EVID, "a6_concurrency.json"))["data"]["best_pages"]
    except (OSError, KeyError, ValueError):
        pass
    st = settle()
    args = ["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:2400", "--chain", "h264", "--ffmpeg", shm + "/chapter.mp4", "--concurrency", str(best), "--json", shm + "/chapter.json"]
    cmd = ["bash", "scripts/lj_guard.sh", "bench"] + RENDER + args
    env = dict(ENVV, LJ_BENCH_LABEL="wp04-a6-chapter-ram")
    a0 = avail_mb()
    p = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    seen = {"png_max": 0, "tmp_max": 0, "avail_min": a0, "samples": 0}
    while p.poll() is None:
        names = os.listdir(shm)
        seen["png_max"] = max(seen["png_max"], len([n for n in names if n.endswith(".png")]), len(glob.glob(os.path.join(RENDERS, "**", "*.png"), recursive=True)))
        seen["tmp_max"] = max(seen["tmp_max"], len([n for n in names if n.endswith(".tmp")]))
        seen["avail_min"] = min(seen["avail_min"], avail_mb())
        seen["samples"] += 1
        time.sleep(2)
    o, e = p.communicate()
    a1 = avail_mb()
    try:
        rep = read_json(shm + "/chapter.json")
        stp = ffprobe(shm + "/chapter.mp4")
        size = os.path.getsize(shm + "/chapter.mp4")
    except (OSError, ValueError):
        rmtree(shm)
        return result("FAIL", "2,400 frames piped into ffmpeg", "the run left no report or video: exit %s %s" % (p.returncode, scrub(e[-300:])))
    note_chromium(rep)
    expect = {"nb_frames": "2400", "width": 1920, "height": 1080, "pix_fmt": "yuv420p", "r_frame_rate": "24/1"}
    got = {k: (stp.get(k) if k in ("width", "height") else str(stp.get(k))) for k in expect}
    pngs = glob.glob(os.path.join(shm, "*.png"))
    rmtree(shm)
    ok = p.returncode == 0 and got == expect and not pngs and seen["png_max"] == 0 and seen["tmp_max"] == 0 and rep["chain_check"]["ok"] and rep["frames_rendered"] == 2400
    return result("PASS" if ok else "FAIL", "a 2,400-frame (100 s) run piped straight into ffmpeg completes with no PNG accumulation, peak RSS recorded; output in RAM-backed /dev/shm (volume untouched)",
                  "%d frames in %.1f s (%.2f fps, %d pages); output %d bytes; PNG files seen anywhere during the run: %d; peak RSS %s; volume Avail %d -> %d MB (min seen %d MB, other jobs write to it)" % (rep["frames_rendered"], rep["seconds_render"], rep["throughput_fps"], best, size, seen["png_max"], rep["peak_rss"], a0, a1, seen["avail_min"]),
                  notes="FALLBACK variant: the guarded lj_with_disk stage (a6_chapter_2400) was BLOCKED by the guard because the shared volume had no headroom; it is not replaced by this test and is rerun when Avail - planned >= 400 MB.",
                  data={"frames": rep["frames_rendered"], "seconds_render": rep["seconds_render"], "throughput_fps": rep["throughput_fps"], "concurrency": best, "peak_rss": rep["peak_rss"], "output_bytes": size, "ffprobe": got,
                        "png_files_max_seen": seen["png_max"], "tmp_files_max_seen": seen["tmp_max"], "samples": seen["samples"], "bench": rep.get("bench"), "settle": st, "volume_avail_mb": {"start": a0, "end": a1, "min": seen["avail_min"]}},
                  avail_min=seen["avail_min"])


def a7_analyse(strings_path, lock_path, vendor_dir, extra_mounts=None, query="", tag="a7", negative=True):
    """The shared body of A7. Returns (data, per_script, problems)."""
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    strings = read_json(strings_path)
    lock = read_json(lock_path)
    with_strings = [k for k, v in strings["scripts"].items() if v.get("strings")]
    not_tested = [k for k in strings["scripts"] if k not in with_strings]
    fam, ref = {}, {}
    for e in lock["fonts"]:
        if e["role"] != "script_family" or not e.get("faces"):
            continue
        for s in e["scripts"]:
            fam[s] = e["family"]
            for f in e["faces"]:
                if f["subset"] == s and f["weight"] == 400 and "woff" in f["files"]:
                    ref[s] = f["files"]["woff"]["to"]
    lang = {"latin": "en", "devanagari": "hi", "tamil": "ta", "telugu": "te", "kannada": "kn", "malayalam": "ml", "bengali": "bn", "gujarati": "gu"}
    items = []
    for s in with_strings:
        for st in strings["scripts"][s]["strings"]:
            items.append({"id": st["id"], "script": s, "text": st["text"], "family": fam.get(s, "MISSING"), "px": 96, "lang": lang.get(s)})
    probe_items = [{k: v for k, v in i.items() if k != "script"} for i in items]
    neg = None
    if negative and "devanagari" in with_strings and "latin" in fam:
        dev = [i for i in items if i["script"] == "devanagari" and i["id"] == "dev-pariksha"] or [i for i in items if i["script"] == "devanagari"]
        neg = {"id": "neg-devanagari-in-latin-only-family", "script": "devanagari", "text": dev[0]["text"], "family": fam["latin"], "px": 96, "lang": "hi"}
        probe_items.append({k: v for k, v in neg.items() if k != "script"})
    work = os.path.join(RENDERS, tag)
    clean_out(tag)
    os.makedirs(work)
    plan = {"items": probe_items, "extra_mounts": extra_mounts or [], "query": query}
    json.dump(plan, open(os.path.join(work, "plan.json"), "w"), ensure_ascii=False)
    rc, out, err, _ = sh(["node", "tests/render/fonts_probe.mjs", "--plan", os.path.join(work, "plan.json"), "--out", os.path.join(work, "png"), "--dir", "pipeline", "--mount", "/vendor=" + vendor_dir], timeout=180)
    if rc != 0:
        return {"error": scrub(err)[-600:]}, {}, ["probe failed: " + scrub(err)[-300:]]
    probe = json.loads(out.strip().splitlines()[-1])

    def ink(p):
        return np.asarray(Image.open(p).convert("L")) < 128

    def crop(m):
        ys, xs = np.nonzero(m)
        return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else m[:0, :0]

    def iou_aligned(a, b):
        a, b = crop(a), crop(b)
        if a.size == 0 and b.size == 0:
            return 1.0, 0, 0
        H, W = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
        A, B = np.zeros((H, W), bool), np.zeros((H, W), bool)
        A[:a.shape[0], :a.shape[1]], B[:b.shape[0], :b.shape[1]] = a, b
        u = int((A | B).sum())
        return (int((A & B).sum()) / u if u else 1.0), u, int((A ^ B).sum())

    def raw_iou(a, b):
        u = int((a | b).sum())
        return int((a & b).sum()) / u if u else 1.0

    def reference_ink(script, text, px, lg):
        font = ImageFont.truetype(os.path.join(vendor_dir, ref[script]), px, layout_engine=ImageFont.Layout.RAQM)
        im = Image.new("L", (1500, 202), 255)
        ImageDraw.Draw(im).text((0, 0), text, font=font, fill=0, language=lg)
        return int((np.asarray(im) < 128).sum())

    IOU_MAX, INK_MIN = 0.8, 0.5     # (J) judgement thresholds; N below is derived from the blocked-font baseline of this same run
    rows = []
    pl = {r["id"]: r for r in probe["loaded"]["items"]}
    pb = {r["id"]: r for r in probe["blocked"]["items"]}
    for it in items + ([neg] if neg else []):
        L = ink(os.path.join(work, "png", "loaded", it["id"] + ".png"))
        B = ink(os.path.join(work, "png", "blocked", it["id"] + ".png"))
        iou, union, xor = iou_aligned(L, B)
        refk = reference_ink(it["script"], it["text"], it["px"], it["lang"]) if it["script"] in ref and it is not neg else None
        loaded_faces = [f for f in pl[it["id"]]["faces"] if f["status"] == "loaded"]
        row = {"id": it["id"], "script": it["script"], "family": it["family"], "check_loaded": pl[it["id"]]["check"], "check_blocked": pb[it["id"]]["check"], "faces_loaded": len(loaded_faces),
               "loaded_ink_px": int(L.sum()), "blocked_ink_px": int(B.sum()), "ink_union_aligned": union, "ink_xor_aligned": xor, "iou_aligned": round(iou, 4), "iou_unaligned": round(raw_iou(L, B), 4),
               "N_min_differing_px": int(math.ceil((1 - IOU_MAX) * union)), "reference_ink_px": refk, "ink_ratio_vs_reference": round(int(L.sum()) / refk, 3) if refk else None}
        row["a_iou_le_0_8"] = bool(iou <= IOU_MAX)
        row["b_ink_ge_0_5_ref"] = bool(refk is not None and int(L.sum()) >= INK_MIN * refk)
        row["check_ok"] = bool(row["check_loaded"]) and row["faces_loaded"] >= 1
        row["pass"] = bool(row["a_iou_le_0_8"] and row["b_ink_ge_0_5_ref"] and row["check_ok"]) if it is not neg else None
        rows.append(row)
    per_script = {}
    for s in with_strings:
        rs = [r for r in rows if r["script"] == s and not r["id"].startswith("neg-")]
        per_script[s] = {"status": "PASS" if rs and all(r["pass"] for r in rs) else "FAIL", "family": fam.get(s), "strings": len(rs)}
    problems = [s for s, v in per_script.items() if v["status"] != "PASS"]
    neg_row = [r for r in rows if r["id"].startswith("neg-")]
    neg_ok = None
    if neg_row:
        neg_ok = not neg_row[0]["a_iou_le_0_8"]       # the control must FAIL (a): loaded and blocked look the same because the Latin-only family has no Devanagari glyphs
    data = {"thresholds": {"iou_max": IOU_MAX, "ink_min_ratio_vs_pillow_raqm": INK_MIN, "marked": "(J) judgement; N_min_differing_px per row is derived from that row's own blocked-font baseline"},
            "scripts_tested": with_strings, "NOT_TESTED": not_tested, "per_script": per_script, "rows": rows, "chromium": probe["chromium"],
            "outside_requests": probe["loaded"]["outside_requests"] + probe["blocked"]["outside_requests"],
            "comparison": "ink masks are cropped to their bounding boxes before the IoU: the primary font's metrics move the baseline between the loaded and the fallback render, which would otherwise hide an unchanged glyph shape (the raw, unaligned IoU is recorded too)",
            "negative_control": {"present": bool(neg_row), "control_fails_a_as_required": neg_ok}}
    CHROMIUM[0] = probe["chromium"]
    clean_out(tag)
    return data, per_script, problems + ([] if neg_ok in (True, None) else ["negative control did not fail (a)"])


@test("a7_fonts")
def t_a7():
    data, per_script, problems = a7_analyse(os.path.join(REPO, "pipeline", "phone", "test_strings.json"), os.path.join(REPO, "pipeline", "lib", "libs.lock.json"), os.path.join(REPO, "vendor"))
    if "error" in data:
        return result("FAIL", "font check per script", data["error"])
    nt = data["NOT_TESTED"]
    ok = not problems and set(data["scripts_tested"]) >= {"latin", "devanagari"} and data["negative_control"]["control_fails_a_as_required"] is True and not data["outside_requests"]
    summ = "; ".join("%s %s (%s)" % (s, v["status"], v["family"]) for s, v in per_script.items())
    return result("PASS" if ok else "FAIL", "per script with strings (day 1 Latin and Devanagari): document.fonts.check true for the Noto family; loaded vs font-blocked IoU of ink masks <= 0.8; loaded ink >= 0.5x Pillow-raqm reference; Devanagari in a Latin-only family fails (a); scripts without strings listed NOT TESTED",
                  "%s; NOT TESTED: %s; negative control fails (a) as required: %s; problems: %s" % (summ, ", ".join(nt), data["negative_control"]["control_fails_a_as_required"], problems or "none"), data=data)


@test("a7_add_script")
def t_a7_add():
    """Adding a script is three small steps and no new package (4.10): a font entry (already in libs.lock.json), one block in test_strings.json,
    one more npm pack. Proved end to end on a throw-away copy with Tamil digits (neutral); never committed."""
    work = os.path.join(SCRATCH, "wp04-addscript")
    rmtree(work)
    os.makedirs(os.path.join(work, "lib"))
    shutil.copytree(os.path.join(REPO, "vendor"), os.path.join(work, "vendor"))
    shutil.copy(os.path.join(REPO, "pipeline", "lib", "libs.lock.json"), os.path.join(work, "lib", "libs.lock.json"))
    rc, out, err, _ = sh(["bash", "pipeline/lib/fetch_libs.sh", "--scripts", "tamil", "--vendor", os.path.join(work, "vendor"), "--lock", os.path.join(work, "lib", "libs.lock.json"), "--quiet"], timeout=240)
    if rc == 3:
        rmtree(work)
        return result("SKIPPED", "fetch one more script font with npm pack", "the registry could not be reached (exit 3), so the add-a-script flow was not run", notes=scrub(err.strip()[-300:]))
    if rc != 0:
        rmtree(work)
        return result("FAIL", "fetch one more script font with npm pack", "fetch_libs.sh exit %d: %s" % (rc, scrub(err.strip()[-300:])))
    strings = read_json(os.path.join(REPO, "pipeline", "phone", "test_strings.json"))
    strings["scripts"]["tamil"] = {"font_script_tag": "Taml", "noto_family": "Noto Sans Tamil", "strings": [
        {"id": "tam-digits", "text": "\u0be6\u0be7\u0be8\u0be9\u0bea\u0beb\u0bec\u0bed\u0bee\u0bef", "kind": "digits", "marks": [], "checked_by_reader": False}]}
    json.dump(strings, open(os.path.join(work, "lib", "test_strings.json"), "w"), ensure_ascii=False, indent=1)
    data, per_script, problems = a7_analyse(os.path.join(work, "lib", "test_strings.json"), os.path.join(work, "lib", "libs.lock.json"), os.path.join(work, "vendor"),
                                            extra_mounts=[{"prefix": "/tmplib", "dir": os.path.join(work, "lib")}], query="&lock=/tmplib/libs.lock.json", tag="a7add", negative=False)
    # the scene itself gets a caption row for the new script, read from the file (never typed in)
    r = render(["--dir", "pipeline", "--quiet", "--page", TESTCARD + "?lock=/tmplib/libs.lock.json&strings=/tmplib/test_strings.json", "--mount", "/vendor=" + os.path.join(work, "vendor"), "--mount", "/tmplib=" + os.path.join(work, "lib"),
                "--out", "renders/wp04/a7s", "--frames", "0:1", "--json", "renders/wp04/a7s.json"], timeout=120)
    rep = read_json(os.path.join(RENDERS, "a7s.json")) if r[0] == 0 else {}
    rows_in_scene = sorted((rep.get("scene_report") or {}).get("strings", {}).keys())
    clean_out("a7s")
    try:
        os.unlink(os.path.join(RENDERS, "a7s.json"))
    except OSError:
        pass
    rmtree(work)
    ok = not problems and data.get("scripts_tested") == ["latin", "devanagari", "tamil"] and data.get("NOT_TESTED") == ["telugu", "kannada", "malayalam", "bengali", "gujarati"] and rows_in_scene == ["devanagari", "latin", "tamil"]
    return result("PASS" if ok else "FAIL", "a script with strings is picked up by the font check and the caption area with no code change: Tamil digits added to a throw-away copy; the other five stay NOT TESTED",
                  "scripts tested %s; NOT TESTED %s; scene caption rows %s; per script %s; problems %s" % (data.get("scripts_tested"), data.get("NOT_TESTED"), rows_in_scene, {k: v["status"] for k, v in per_script.items()}, problems or "none"),
                  data={k: data[k] for k in ("scripts_tested", "NOT_TESTED", "per_script") if k in data}, unverified=["Tamil glyph coverage was checked on neutral digits only; a reader of the script has not looked at them (pending_O-10)"])


@test("max_seconds_resume")
def t_maxsec():
    """--max-seconds is the soft cap for the 10-minute container foreground limit: stop after the current frame, say how to resume, exit 0."""
    base = ["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:240", "--out", "renders/wp04/ms"]
    clean_out("ms")
    r1 = render(base + ["--max-seconds", "6", "--json", "renders/wp04/ms.json"], timeout=300)
    rep1 = read_json(os.path.join(RENDERS, "ms.json"))
    n1 = len(frames(os.path.join(RENDERS, "ms")))
    r2 = render(base + ["--json", "renders/wp04/ms.json"], timeout=300)
    rep2 = read_json(os.path.join(RENDERS, "ms.json"))
    n2 = len(frames(os.path.join(RENDERS, "ms")))
    tmp = glob.glob(os.path.join(RENDERS, "ms", "*.tmp"))
    ref = render(["--dir", "pipeline", "--quiet", "--page", FLAT, "--frames", "0:240", "--out", "renders/wp04/ms2"], timeout=300)
    equal = hashes(os.path.join(RENDERS, "ms")) == hashes(os.path.join(RENDERS, "ms2"))
    clean_out("ms", "ms2")
    try:
        os.unlink(os.path.join(RENDERS, "ms.json"))
    except OSError:
        pass
    ok = (r1[0] == 0 and rep1["complete"] is False and 0 < n1 < 240 and rep1["remaining"] == 240 - n1 and "resume" in (rep1["resume_hint"] or "")
          and r2[0] == 0 and rep2["complete"] is True and n2 == 240 and rep2["frames_skipped_existing"] == n1 and not tmp and equal)
    return result("PASS" if ok else "FAIL", "--max-seconds 6 stops early with exit 0, complete=false and a resume hint; the same command then finishes and equals an uninterrupted run",
                  "first run stopped with %d of 240 frames (remaining %s); second run skipped %s, now %d frames; equal to uninterrupted: %s" % (n1, rep1["remaining"], rep2["frames_skipped_existing"], n2, equal),
                  data={"first": {k: rep1[k] for k in ("complete", "frames_rendered", "remaining", "resume_hint")}, "second": {k: rep2[k] for k in ("complete", "frames_rendered", "frames_skipped_existing")}})


@test("webgl_smoke")
def t_webgl():
    clean_out("sm")
    st = settle(90)
    r = render(["--dir", "pipeline", "--quiet", "--page", "scenes/testcard/smoke3d.html", "--out", "renders/wp04/sm", "--seconds", "1", "--json", "renders/wp04/sm.json"], timeout=300, bench=True, label="wp04-webgl-smoke")
    rep = read_json(os.path.join(RENDERS, "sm.json"))
    note_chromium(rep)
    info = rep.get("scene_report") or {}
    h = hashes(os.path.join(RENDERS, "sm"))
    from PIL import Image
    import numpy as np
    fs_ = frames(os.path.join(RENDERS, "sm"))
    glc = np.asarray(Image.open(fs_[12]).convert("L").crop((1120, 190, 1840, 910))).astype(float) if fs_ else None
    std = float(glc.std()) if glc is not None else None
    clean_out("sm")
    try:
        os.unlink(os.path.join(RENDERS, "sm.json"))
    except OSError:
        pass
    ok = r[0] == 0 and len(h) == 24 and len(set(h.values())) == 24 and info.get("webgl") is True and std is not None and std > 8 and "swiftshader" in (info.get("renderer") or "").lower()
    return result("PASS" if ok else "FAIL", "WebGL on SwiftShader renders (one CSS 3D plane and one raw WebGL triangle), every frame different, canvas not blank; fps recorded (replaces the dropped voxel diorama, SP2 c)",
                  "%.2f fps over 24 frames; GL renderer '%s'; distinct frames %d/24; GL canvas luminance std %.1f" % (rep["throughput_fps"], info.get("renderer"), len(set(h.values())), std or -1),
                  data={"settle": st, "throughput_fps": rep["throughput_fps"], "renderer": info.get("renderer"), "vendor": info.get("vendor"), "gl_version": info.get("version"), "distinct_frames": len(set(h.values())), "gl_canvas_luma_std": std, "peak_rss": rep["peak_rss"], "bench": bench_note(r[2])})


@test("gsap_equivalence")
def t_gsap():
    if not os.path.isfile(os.path.join(REPO, "vendor", "js", "gsap.min.js")):
        return result("SKIPPED", "?gsap=1 frames match the cosine ease", "SKIPPED: vendor/js/gsap.min.js is not present (run pipeline/lib/fetch_libs.sh)")
    base = ["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--frames", "0:96", "--shard", "0/8"]
    clean_out("g0", "g1")
    r0 = render(base + ["--page", TESTCARD, "--out", "renders/wp04/g0"], timeout=300)
    r1 = render(base + ["--page", TESTCARD + "?gsap=1", "--out", "renders/wp04/g1", "--json", "renders/wp04/g1.json"], timeout=300)
    rep = read_json(os.path.join(RENDERS, "g1.json"))
    diffs = [ae(a, b) for a, b in zip(frames(os.path.join(RENDERS, "g0")), frames(os.path.join(RENDERS, "g1")))]
    clean_out("g0", "g1")
    try:
        os.unlink(os.path.join(RENDERS, "g1.json"))
    except OSError:
        pass
    ok = r0[0] == 0 and r1[0] == 0 and len(diffs) == 12 and max(diffs) <= 100
    return result("PASS" if ok else "FAIL", "the same ease through GSAP's paused timeline, tl.time(t,false), matches the cosine ease: at most 100 differing pixels (fuzz 1%) on 12 frames of the push",
                  "differing pixels per frame (frames 0,8,...,88): %s; GSAP %s" % (diffs, (rep.get("scene_report") or {}).get("gsap")), data={"differing_px": diffs, "gsap_version": (rep.get("scene_report") or {}).get("gsap")})


@test("mo8_precheck")
def t_mo8():
    audit = os.path.join(REPO, "research", "cinematic-quality-fixtures", "mo8_audit.py")
    if not os.path.isfile(audit):
        return result("SKIPPED", "MO8 pre-check", "research/cinematic-quality-fixtures/mo8_audit.py not found")
    rows = {}
    for mode in ("transform", "layout"):
        clean_out("mo8_" + mode)
        r = render(["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD + "?view=detail&push=%s&dur=1.9583333" % mode, "--out", "renders/wp04/mo8_" + mode, "--frames", "0:48"], timeout=300)
        rc, out, err, _ = sh(["python3", "-I", "-B", audit, "--no-h264", os.path.join(RENDERS, "mo8_" + mode)], timeout=300, cwd=os.path.dirname(audit))
        d = last_json(out) or {}
        rows[mode] = {"render_exit": r[0], "audit_exit": rc, **{k: d.get(k) for k in ("frames", "mo8a_d4_px", "mo8b_d4_px", "mo8a_centre_jit_px", "mo8b_edge_jit_px", "ease_class")}}
        clean_out("mo8_" + mode)
    t, l = rows["transform"], rows["layout"]
    ok = (t["mo8a_d4_px"] is not None and t["mo8a_d4_px"] <= 0.05 and t["mo8b_d4_px"] <= 0.04 and l["mo8a_d4_px"] > 0.05 and l["mo8b_d4_px"] > 0.04 and t["frames"] == 48)
    return result("PASS" if ok else "FAIL", "PRE-CHECK for A11 with the existing research/mo8_audit.py (the WP-05 gate is not used here): ?push=transform within MO8a 0.05 px and MO8b 0.04 px (4th-difference numbers); ?push=layout over both limits",
                  "transform: MO8a %s px, MO8b %s px; layout: MO8a %s px, MO8b %s px (48 frames, ?view=detail)" % (t["mo8a_d4_px"], t["mo8b_d4_px"], l["mo8a_d4_px"], l["mo8b_d4_px"]), data=rows,
                  notes="Not A11. A11 is run by WP-11b with pipeline/validators/mo8_gate.py once WP-05 lands.")


@test("a11_mo8_gate")
def t_a11():
    """A11 (needs WP-05): ?push=transform passes pipeline/validators/mo8_gate.py and ?push=layout fails it. The plan has WP-11b run it; it is run here as soon as the
    gate exists, with the frame set the gate is meant to measure (?view=detail: the full card also has a moving bar and a counter)."""
    gate = os.path.join(REPO, "pipeline", "validators", "mo8_gate.py")
    if not os.path.isfile(gate):
        return result("SKIPPED", "?push=transform passes the MO8 gate and ?push=layout fails it (needs WP-05)", "SKIPPED: pipeline/validators/mo8_gate.py has not landed; WP-11b runs A11")
    cache = os.path.join(REPO, "research", "cinematic-quality-fixtures", "__pycache__")
    had_cache = os.path.isdir(cache)
    rows = {}
    for mode in ("transform", "layout"):
        clean_out("a11_" + mode)
        r = render(["--dir", "pipeline", "--mount", "/vendor=vendor", "--quiet", "--page", TESTCARD + "?view=detail&push=%s&dur=1.9583333" % mode, "--out", "renders/wp04/a11_" + mode, "--frames", "0:48"], timeout=300)
        rc, out, err, _ = sh(["python3", "-I", "-B", gate, os.path.join(RENDERS, "a11_" + mode), "--json", os.path.join(RENDERS, "a11_%s.json" % mode)], timeout=300)
        try:
            gj = read_json(os.path.join(RENDERS, "a11_%s.json" % mode))
        except (OSError, ValueError):
            gj = {}
        rows[mode] = {"render_exit": r[0], "gate_exit": rc, "result_line": [l.strip() for l in out.splitlines() if "RESULT" in l], "lines": [l.strip() for l in out.splitlines() if "MO8" in l and "limit" in l]}
        clean_out("a11_" + mode)
        try:
            os.unlink(os.path.join(RENDERS, "a11_%s.json" % mode))
        except OSError:
            pass
    if not had_cache:
        rmtree(cache)      # the gate runs mo8_audit.py in a child process that writes bytecode into research/; remove what this test created
    ok = rows["transform"]["gate_exit"] == 0 and rows["layout"]["gate_exit"] == 1 and rows["transform"]["render_exit"] == 0 and rows["layout"]["render_exit"] == 0
    return result("PASS" if ok else "FAIL", "?push=transform passes the MO8 gate (exit 0) and ?push=layout fails it (exit 1), 48 frames of ?view=detail",
                  "transform: exit %s %s %s; layout: exit %s %s %s" % (rows["transform"]["gate_exit"], rows["transform"]["result_line"], rows["transform"]["lines"], rows["layout"]["gate_exit"], rows["layout"]["result_line"], rows["layout"]["lines"]),
                  data=rows, notes="WP-11b repeats this with the final gate. The frame set for the gate is ?view=detail, 48 to 96 frames.")


# --------------------------------------------------------------------------------------------------------------- driver
def summarize():
    """Rewrite summary.json, tests.jsonl and tests_all.txt from the per-test evidence files (after a partial rerun with --only)."""
    envs, lines, counts = [], [], {}
    for name, _, _ in TESTS:
        pth = os.path.join(EVID, name + ".json")
        if not os.path.isfile(pth):
            continue
        e = read_json(pth)
        envs.append(e)
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        lines.append("%-8s %-22s %5.1fs  %s" % (e["status"], name, e["data"].get("seconds", 0), e["actual"][:230]))
    summary = {"schema": "lj-evidence-summary/1", "package": "WP-04", "mode": "all", "date_utc": TODAY, "counts": counts, "seconds": round(sum(e["data"].get("seconds", 0) for e in envs), 1),
               "tests": {e["test"]: e["status"] for e in envs}, "chromium": CHROMIUM[0] or next((e["env"].get("chromium") for e in envs if e["env"].get("chromium")), None)}
    with open(os.path.join(EVID, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(os.path.join(EVID, "tests.jsonl"), "w", encoding="utf-8") as f:
        for e in envs:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
    with open(os.path.join(EVID, "tests_all.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n" + json.dumps(counts, sort_keys=True) + "\n")
    print("summarized %d tests: %s" % (len(envs), json.dumps(counts, sort_keys=True)))
    return 1 if counts.get("FAIL") or counts.get("BLOCKED") else 0


def main():
    args = sys.argv[1:]
    mode = args[0] if args else "--quick"
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    if mode == "--summarize":
        return summarize()
    if mode == "--list":
        for n, _, q in TESTS:
            print("%-22s %s" % (n, "quick+all" if q else "all"))
        return 0
    os.makedirs(EVID, exist_ok=True)
    os.makedirs(RENDERS, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    selected = [t for t in TESTS if (mode == "--all" or t[2]) and (only is None or t[0] in only)]
    if only:
        missing = only - {t[0] for t in TESTS}
        if missing:
            print("unknown test(s): %s" % ", ".join(sorted(missing)), file=sys.stderr)
            return 2
    lines, envs, counts = [], [], {}
    t_all = time.time()
    for name, fn, quick in selected:
        a0 = avail_mb()
        t0 = time.time()
        try:
            res = fn()
        except Exception as e:  # a crash in a test is a FAIL with the reason, never a silent pass
            res = result("FAIL", "the test runs", "test crashed: %s: %s" % (type(e).__name__, e))
        secs = time.time() - t0
        a1 = avail_mb()
        env = envelope(name, res, a0, a1)
        env["data"]["seconds"] = round(secs, 1)
        with open(os.path.join(EVID, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(env, f, indent=1, ensure_ascii=False, sort_keys=True)
            f.write("\n")
        envs.append(env)
        counts[res["status"]] = counts.get(res["status"], 0) + 1
        line = "%-8s %-22s %5.1fs  %s" % (res["status"], name, secs, scrub(res["actual"])[:230])
        lines.append(line)
        print(line, flush=True)
    summary = {"schema": "lj-evidence-summary/1", "package": "WP-04", "mode": mode.lstrip("-"), "date_utc": TODAY, "counts": counts, "seconds": round(time.time() - t_all, 1),
               "tests": {e["test"]: e["status"] for e in envs}, "chromium": CHROMIUM[0]}
    with open(os.path.join(EVID, "summary.json" if only is None else "summary_partial.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
        f.write("\n")
    if only is None:
        with open(os.path.join(EVID, "tests.jsonl" if mode == "--all" else "tests_quick.jsonl"), "w", encoding="utf-8") as f:
            for e in envs:
                f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
        with open(os.path.join(EVID, "tests_all.txt" if mode == "--all" else "tests_quick.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n\n" + json.dumps(counts, sort_keys=True) + "\n")
    print("summary: %s in %.0f s" % (json.dumps(counts, sort_keys=True), time.time() - t_all))
    return 1 if counts.get("FAIL") or counts.get("BLOCKED") else 0


if __name__ == "__main__":
    sys.exit(main())
