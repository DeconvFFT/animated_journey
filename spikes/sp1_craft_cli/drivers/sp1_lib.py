"""sp1_lib.py: shared helpers for the WP-07 drivers (standard library only).

WHAT IT IS. Small pieces every SP1 driver needs: the repo and scratch locations, a scrubber that keeps identifying data out of
anything a driver writes, a curl wrapper that records the exact status and stderr, a sandboxed runner (env -i, throw-away HOME,
timeout, unshare -rn when it works) with a resident-memory watchdog, ffprobe helpers, and the evidence envelope of build plan 4.2.

HOW IT IS USED. The drivers add this folder to sys.path from __file__ (python3 -I does not do that by itself) and import it.
It is never run on its own: `python3 -I spikes/sp1_craft_cli/drivers/sp1_lib.py --selftest` runs its own small checks.

WHAT IT NEVER TOUCHES. It reads df, /proc and the files it is given. It writes only where a caller tells it to. It starts only
the commands a caller passes (curl, ffmpeg, ffprobe, and the Craft CLIs the drivers run inside the sandbox).
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SP1 = os.path.realpath(os.path.join(HERE, ".."))
REPO = os.path.realpath(os.path.join(SP1, "..", ".."))
SCRATCH = os.environ.get("LJ_SCRATCH") or os.path.join(os.path.dirname(REPO), "build-scratch")
EVID = os.environ.get("LJ_SP1_EVIDENCE") or os.path.join(REPO, "build", "evidence", "wp07")
PACKAGE = "WP-07"
RELEASE_BASE = os.environ.get("LJ_RELEASE_BASE") or "https://github.com/storytold"
ASSETS_FILE = os.environ.get("LJ_SP1_ASSETS") or os.path.join(SP1, "release_assets.json")
PAGE = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096

DOC_IPS = ("192.0.2.", "198.51.100.", "203.0.113.")


# ----------------------------------------------------------------------------- time, files, hashes
def now_s():
    """UTC, whole seconds (4.2: nothing finer than a second)."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=True)
        f.write("\n")
    os.replace(tmp, path)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def append_jsonl(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, sort_keys=True, ensure_ascii=True) + "\n")


def rel(path):
    """A repo-relative or <scratch> path for anything that is written down."""
    p = os.path.abspath(path)
    if p == REPO or p.startswith(REPO + os.sep):
        return os.path.relpath(p, REPO)
    if p == SCRATCH or p.startswith(SCRATCH + os.sep):
        return "<scratch>" + p[len(SCRATCH):]
    return "<outside>"


# ----------------------------------------------------------------------------- scrubbing
_IPV4 = re.compile(r"(?<![0-9.])(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?![0-9.])")
_CREDS = re.compile(r"(https?://)[^/\s:@]+:[^/\s@]*@")
_QUERY = re.compile(r"(https?://[^\s?\"'<>]+)\?[^\s\"'<>]*")
_HOMES = re.compile(r"/(?:home|Users)/(?!user\b)[A-Za-z0-9._-]+")


def scrub(text):
    """Remove what must not reach a public file: IP addresses (documentation ranges and 127.0.0.1 stay), credentials in URLs,
    URL query strings (signed release links carry tokens), other users' home folders, the repo and scratch paths."""
    if not text:
        return text

    def ip(m):
        s = m.group(0)
        if s == "127.0.0.1" or s.startswith(DOC_IPS):
            return s
        return "<ip>"

    text = text.replace(REPO, "<repo>").replace(SCRATCH, "<scratch>")
    text = _CREDS.sub(r"\1<credentials-removed>@", text)
    text = _QUERY.sub(r"\1?<query-removed>", text)
    text = _HOMES.sub("/home/<user>", text)
    text = re.sub(r"(?<![A-Za-z0-9_])/root(?![A-Za-z0-9_])", "<home>", text)
    return _IPV4.sub(ip, text)


# ----------------------------------------------------------------------------- disk
def df_avail_mb():
    """Avail of / in MB, the same way scripts/lj_guard.sh reads it (LJ_DF_CMD overrides; an integer alone is accepted)."""
    try:
        cmd = os.environ.get("LJ_DF_CMD")
        if cmd:
            out = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=20, env=dict(os.environ, LC_ALL="C")).stdout
        else:
            out = subprocess.run(["df", "-BM", "-P", "/"], capture_output=True, text=True, timeout=20, env=dict(os.environ, LC_ALL="C")).stdout
    except Exception:
        return None
    m = re.fullmatch(r"\s*([0-9]+)\s*", out)
    if m:
        return int(m.group(1))
    for line in out.splitlines()[1:]:
        cols = line.split()
        if len(cols) >= 4:
            d = re.sub(r"[^0-9]", "", cols[3])
            if d:
                return int(d)
    return None


def dir_size_mb(path):
    total = 0
    for root, _dirs, files in os.walk(path):
        for fn in files:
            try:
                total += os.lstat(os.path.join(root, fn)).st_size
            except OSError:
                pass
    return round(total / 1048576.0, 1)


def disk_object(planned_mb=0, start=None, minimum=None, end=None):
    """The `disk` object that every envelope must carry (4.2)."""
    env_start = os.environ.get("LJ_DISK_START_MB")
    env_planned = os.environ.get("LJ_DISK_PLANNED_MB")
    s = start if start is not None else (int(env_start) if env_start and env_start.isdigit() else df_avail_mb())
    e = end if end is not None else df_avail_mb()
    p = planned_mb if planned_mb else (int(env_planned) if env_planned and env_planned.isdigit() else 0)
    vals = [v for v in (s, e, minimum) if v is not None]
    return {
        "avail_mb_start": s,
        "planned_write_mb": p,
        "avail_mb_min": min(vals) if vals else None,
        "avail_mb_end": e,
        "floor_mb": int(os.environ.get("LJ_FLOOR_MB", "400")),
        "hard_floor_mb": int(os.environ.get("LJ_HARD_FLOOR_MB", "250")),
    }


# ----------------------------------------------------------------------------- evidence envelope (4.2)
def tool_version(argv):
    try:
        out = subprocess.run(argv, capture_output=True, text=True, timeout=20).stdout
        m = re.search(r"version\s+([0-9][0-9A-Za-z.\-]*)", out)
        return m.group(1) if m else out.splitlines()[0][:40]
    except Exception:
        return None


def env_block():
    return {
        "platform": "linux",
        "ffmpeg": tool_version(["ffmpeg", "-version"]),
        "nproc": os.cpu_count(),
        "python": "%d.%d" % sys.version_info[:2],
        "contaminated": os.environ.get("LJ_BENCH_CONTAMINATED", "not-timed"),
    }


def envelope(test, status, expected, actual, notes="", unverified_reasons=None, disk=None, extra=None, out_dir=None):
    assert status in ("PASS", "FAIL", "UNVERIFIED", "SKIPPED", "BLOCKED"), status
    rec = {
        "schema": "lj-evidence/1",
        "package": PACKAGE,
        "test": test,
        "date_utc": today(),
        "status": status,
        "env": env_block(),
        "disk": disk or disk_object(),
        "expected": expected,
        "actual": scrub(actual) if isinstance(actual, str) else actual,
        "notes": scrub(notes),
        "unverified_reasons": list(unverified_reasons or []),
        "stage": os.environ.get("LJ_DISK_LABEL", ""),
    }
    if extra:
        rec["detail"] = extra
    d = out_dir or EVID
    write_json(os.path.join(d, test + ".json"), rec)
    return rec


# ----------------------------------------------------------------------------- the asset table
def load_assets(path=None):
    return read_json(path or ASSETS_FILE)


def find_pin(assets, app, tag):
    for p in assets["pins"]:
        if p["app"] == app and p["tag"] == tag:
            return p
    return None


def asset_url(app, tag, name):
    return "%s/%s/releases/download/%s/%s" % (RELEASE_BASE, app, tag, name)


# ----------------------------------------------------------------------------- curl, with the exact evidence
def _status_lines(headers):
    return [ln.strip() for ln in headers.splitlines() if ln.startswith("HTTP/")]


def _last_code(lines):
    codes = [int(m.group(1)) for ln in lines for m in [re.match(r"HTTP/\S+\s+(\d{3})", ln)] if m and "onnection" not in ln]
    return codes[-1] if codes else 0


def curl_head(url, max_time=60):
    """HEAD with redirects. Returns status (final), status lines (the proxy reply included), content length, exit code, stderr."""
    t0 = time.monotonic()
    p = subprocess.run(["curl", "-sS", "-I", "-L", "--connect-timeout", "20", "--max-time", str(max_time), "-D", "-", "-o", "/dev/null", url],
                       capture_output=True, text=True)
    lines = _status_lines(p.stdout)
    blocks = p.stdout.replace("\r", "").split("\n\n")
    clen = None
    for b in reversed([x for x in blocks if x.strip()]):
        m = re.search(r"(?im)^content-length:\s*([0-9]+)\s*$", b)
        if m:
            clen = int(m.group(1))
            break
    return {"status": _last_code(lines), "status_lines": lines, "content_length": clen, "curl_exit": p.returncode,
            "stderr": p.stderr.strip(), "seconds": round(time.monotonic() - t0, 1)}


def curl_get(url, out_path, max_time=1500, retries=2):
    """GET into out_path. -f makes a 4xx/5xx an exit 22 with curl's own one-line message on stderr."""
    t0 = time.monotonic()
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    p = subprocess.run(["curl", "-f", "-sS", "-L", "--connect-timeout", "20", "--max-time", str(max_time), "--retry", str(retries), "--retry-delay", "3",
                        "-o", out_path, "-w", "%{http_code}", url], capture_output=True, text=True)
    code = int(p.stdout.strip()) if p.stdout.strip().isdigit() else 0
    size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    return {"status": code, "curl_exit": p.returncode, "stderr": p.stderr.strip(), "bytes": size, "seconds": round(time.monotonic() - t0, 1)}


def curl_probe(url, max_time=60):
    """A 1 KB ranged GET with -f: when the asset is missing or blocked this gives curl's own exit code and one-line stderr, which a HEAD
    request (exit 0 even on a 404) does not."""
    t0 = time.monotonic()
    p = subprocess.run(["curl", "-f", "-sS", "-L", "-r", "0-1023", "--connect-timeout", "20", "--max-time", str(max_time), "-o", "/dev/null", "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    code = int(p.stdout.strip()) if p.stdout.strip().isdigit() else 0
    return {"status": code, "curl_exit": p.returncode, "stderr": p.stderr.strip(), "seconds": round(time.monotonic() - t0, 1)}


def proxy_status_line(url):
    """A proxy status line without credentials: only HTTP status lines are kept, never headers, addresses or tokens."""
    h = curl_head(url, max_time=30)
    return h["status_lines"][:4]


def write_blocked_proof(path, url, status, curl_exit, stderr, status_lines=None, context=None, bytes_received=0):
    """blocked_proof.json: URL (no query), HTTP status, curl exit code, curl's stderr verbatim, the proxy/status lines, the time."""
    raw = stderr or ""
    clean = scrub(raw)
    rec = {
        "schema": "lj-blocked-proof/1",
        "package": PACKAGE,
        "url": scrub(url),
        "http_status": status,
        "curl_exit_code": curl_exit,
        "curl_stderr_verbatim": clean,
        "curl_stderr_was_scrubbed": clean != raw,
        "http_status_lines": [scrub(x) for x in (status_lines or [])],
        "proxy": "outbound HTTPS goes through the session's agent proxy (address and credentials deliberately not recorded)",
        "bytes_received": bytes_received,
        "time_utc": now_s(),
        "context": context or {},
        "fallback": "spikes/sp1_craft_cli/FALLBACK.md",
    }
    write_json(path, rec)
    return rec


# ----------------------------------------------------------------------------- the sandbox and the watchdog
_UNSHARE = None


def unshare_ok():
    """Does `unshare -rn true` work here? (recorded in the evidence; the Craft binaries run without a network when it does)"""
    global _UNSHARE
    if _UNSHARE is None:
        try:
            _UNSHARE = subprocess.run(["unshare", "-rn", "true"], capture_output=True, timeout=20).returncode == 0
        except Exception:
            _UNSHARE = False
    return _UNSHARE


def sandbox_argv(binary, args, home, timeout_s=600, extra_env=None):
    """env -i with a throw-away HOME, a bounded run, no network when unshare works. No Craft binary sees anything but `home`."""
    env = {
        "HOME": home,
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "TMPDIR": os.path.join(home, "tmp"),
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "XDG_CACHE_HOME": os.path.join(home, ".cache"),
        "XDG_DATA_HOME": os.path.join(home, ".local", "share"),
    }
    env.update(extra_env or {})
    for d in (env["TMPDIR"], env["XDG_CONFIG_HOME"], env["XDG_CACHE_HOME"], env["XDG_DATA_HOME"]):
        os.makedirs(d, exist_ok=True)
    argv = ["env", "-i"] + ["%s=%s" % kv for kv in sorted(env.items())] + ["timeout", "--kill-after=10", str(int(timeout_s))]
    if unshare_ok():
        argv += ["unshare", "-rn"]
    return argv + [binary] + list(args)


def _stat_fields(pid):
    try:
        with open("/proc/%s/stat" % pid, "rb") as f:
            data = f.read().decode("latin-1")
    except OSError:
        return None
    r = data[data.rindex(")") + 2:].split()
    return r  # r[0]=state r[1]=ppid r[2]=pgrp r[3]=session


def session_pids(sid):
    out = []
    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue
        r = _stat_fields(name)
        if r and r[3] == str(sid):
            out.append(int(name))
    return out


def session_rss_kb(sid):
    total = 0
    for pid in session_pids(sid):
        try:
            with open("/proc/%d/statm" % pid) as f:
                total += int(f.read().split()[1]) * PAGE // 1024
        except (OSError, ValueError, IndexError):
            pass
    return total


def kill_session(sid):
    for pid in session_pids(sid):
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass


_LIVE_SIDS = set()


def _on_term(signum, frame):
    """The disk guard stops a stage with SIGTERM to its process group. A sandboxed Craft run lives in its own session, so the group signal would not
    reach it: stop every live session first, then leave (the stage's cleanup trap removes the folders)."""
    for sid in list(_LIVE_SIDS):
        kill_session(sid)
    sys.exit(143)


try:
    signal.signal(signal.SIGTERM, _on_term)
except ValueError:  # not the main thread
    pass


def run_watched(argv, cwd, out_path, err_path, rss_kill_mb=10240, wall_s=None, poll_s=0.25):
    """Run argv in its own session; poll the summed resident memory of the whole session every poll_s seconds; SIGKILL it all above
    rss_kill_mb (the plan's 10 GB: ulimit -v is not used because wgpu maps large address ranges). Returns the measurements.
    max_rss_mb is the kernel's own figure for the process tree (wait4 rusage); polled_rss_mb is what the watchdog saw."""
    t0 = time.monotonic()
    killed = None
    peak = 0
    with open(out_path, "wb") as fo, open(err_path, "wb") as fe:
        p = subprocess.Popen(argv, cwd=cwd, stdout=fo, stderr=fe, stdin=subprocess.DEVNULL, start_new_session=True)
        sid = p.pid
        _LIVE_SIDS.add(sid)
        while True:
            pid, st, ru = os.wait4(p.pid, os.WNOHANG)
            if pid != 0:
                break
            rss = session_rss_kb(sid)
            peak = max(peak, rss)
            if killed is None and rss > rss_kill_mb * 1024:
                killed = "rss-watchdog"
                kill_session(sid)
            if killed is None and wall_s and time.monotonic() - t0 > wall_s:
                killed = "wall-clock"
                kill_session(sid)
            time.sleep(poll_s)
    p.returncode = os.waitstatus_to_exitcode(st)
    kill_session(sid)  # anything the command left behind
    _LIVE_SIDS.discard(sid)
    wall = time.monotonic() - t0
    return {
        "rc": p.returncode,
        "wall_s": round(wall, 2),
        "user_s": round(ru.ru_utime, 2),
        "sys_s": round(ru.ru_stime, 2),
        "max_rss_mb": round(ru.ru_maxrss / 1024.0, 1),
        "polled_rss_mb": round(peak / 1024.0, 1),
        "killed": killed,
    }


def tail(path, n=600):
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - n))
            return scrub(f.read().decode("utf-8", "replace"))
    except OSError:
        return ""


# ----------------------------------------------------------------------------- ffprobe and friends
def ffprobe_stream(path, count_frames=True, timeout=600):
    args = ["ffprobe", "-v", "error", "-select_streams", "v:0"]
    if count_frames:
        args.append("-count_frames")
    args += ["-show_entries", "stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,nb_frames,color_space,color_transfer,color_primaries,color_range",
             "-of", "json", path]
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    try:
        s = json.loads(p.stdout)["streams"][0]
    except (ValueError, KeyError, IndexError):
        return {"error": scrub(p.stderr.strip()[:300] or "ffprobe printed no stream")}
    return s


def decode_errors(path, timeout=900):
    """`ffmpeg -v error -i FILE -f null -` : the plan's decode check; an empty string is a pass."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"], capture_output=True, text=True, timeout=timeout)
    return scrub(p.stderr.strip())


def has_moov(path):
    """Is there a moov atom in the first or last megabyte of an MP4/MOV? (an interrupted H.264 render has none)"""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            head = f.read(1 << 20)
            f.seek(max(0, size - (1 << 20)))
            tailb = f.read()
        return b"moov" in head or b"moov" in tailb
    except OSError:
        return False


class Recorder:
    """Collects the CLI calls a driver makes (command words only, no paths) so the evidence shows exactly what ran."""

    def __init__(self):
        self.calls = []

    def add(self, label, res, tail_text=""):
        rec = {"call": label, "rc": res.get("rc"), "wall_s": res.get("wall_s"), "max_rss_mb": res.get("max_rss_mb"), "killed": res.get("killed")}
        if res.get("rc") not in (0, None):
            rec["stderr_tail"] = tail_text[-400:]
        self.calls.append(rec)


# ----------------------------------------------------------------------------- a Craft CLI inside the sandbox
class Cli:
    """One Craft command-line binary, always run through sandbox_argv and run_watched. Output goes to files under work/t/, never to a
    pipe, so a long export cannot block on a full pipe. `run` returns the measurements plus the stdout and stderr text."""

    def __init__(self, binary, home, work, rec=None, rss_kill_mb=10240, timeout_s=900, extra_env=None):
        self.binary, self.home, self.work, self.rec = binary, home, work, rec or Recorder()
        self.rss_kill_mb, self.timeout_s, self.extra_env = rss_kill_mb, timeout_s, dict(extra_env or {})
        self.tdir = os.path.join(work, "t")
        os.makedirs(self.tdir, exist_ok=True)
        self.n = 0
        self.peak_rss_mb = 0.0

    def run(self, args, label=None, timeout_s=None, extra_env=None, cwd=None):
        self.n += 1
        out_p = os.path.join(self.tdir, "o%04d.txt" % self.n)
        err_p = os.path.join(self.tdir, "e%04d.txt" % self.n)
        env = dict(self.extra_env)
        env.update(extra_env or {})
        argv = sandbox_argv(self.binary, args, self.home, timeout_s or self.timeout_s, env)
        res = run_watched(argv, cwd or self.tdir, out_p, err_p, rss_kill_mb=self.rss_kill_mb, wall_s=(timeout_s or self.timeout_s) + 30)
        try:
            with open(out_p, "rb") as f:
                out = f.read(4 << 20).decode("utf-8", "replace")
        except OSError:
            out = ""
        err = tail(err_p, 4000)
        res["stdout"], res["stderr"] = out, err
        self.peak_rss_mb = max(self.peak_rss_mb, res["max_rss_mb"])
        self.rec.add(label or " ".join(str(a) for a in args[:3]), res, err)
        for pth in (out_p, err_p):
            try:
                os.remove(pth)
            except OSError:
                pass
        return res

    def json(self, args, label=None, **kw):
        res = self.run(args, label, **kw)
        txt = res["stdout"].strip()
        obj = None
        for cand in (txt, txt.splitlines()[-1] if txt else ""):
            try:
                obj = json.loads(cand)
                break
            except ValueError:
                continue
        res["json"] = obj
        return res


def walk(obj):
    """Every dict inside a JSON value, depth first."""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def shape_of(obj, depth=3):
    """The key structure of a JSON value without any of its values (what the next iteration of a driver needs to see)."""
    if depth == 0:
        return "..."
    if isinstance(obj, dict):
        return {k: shape_of(v, depth - 1) for k, v in list(obj.items())[:12]}
    if isinstance(obj, list):
        return [shape_of(obj[0], depth - 1)] if obj else []
    return type(obj).__name__


# ----------------------------------------------------------------------------- self-test
def _selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok = ok and cond

    check("scrub removes a public IPv4", scrub("connect to " + "8.8." + "4.4 port 443") == "connect to <ip> port 443")
    check("scrub keeps 127.0.0.1 and documentation ranges", scrub("127.0.0.1 192.0.2.7 198.51.100.1 203.0.113.9") == "127.0.0.1 192.0.2.7 198.51.100.1 203.0.113.9")
    check("scrub removes URL credentials", "secret" not in scrub("http://user:secret@host/x"))
    check("scrub removes a signed query", scrub("https://h.example/a/b?sig=abc&x=1") == "https://h.example/a/b?<query-removed>")
    check("scrub generalises another user's home", scrub("/home/" + "someone/x") == "/home/<user>/x")
    check("scrub keeps version strings", scrub("filmcraft 0.9.0 and 10.0.22631.4317") == "filmcraft 0.9.0 and 10.0.22631.4317")
    os.environ["LJ_DF_CMD"] = "echo 900"
    check("LJ_DF_CMD echo 900 gives 900", df_avail_mb() == 900)
    del os.environ["LJ_DF_CMD"]
    check("session_rss_kb of a missing session is 0", session_rss_kb(2 ** 30) == 0)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
