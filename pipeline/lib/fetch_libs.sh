#!/usr/bin/env bash
# fetch_libs.sh: fetch the pinned test libraries and fonts into the git-ignored vendor/ folder.
#
#   bash pipeline/lib/fetch_libs.sh                    # fetch what is missing or changed (day-1 set)
#   bash pipeline/lib/fetch_libs.sh --check            # no network: verify vendor/ against libs.lock.json
#   bash pipeline/lib/fetch_libs.sh --scripts tamil,telugu   # also fetch those pending_O-10 script fonts
#   bash pipeline/lib/fetch_libs.sh --scripts all      # every script font listed in libs.lock.json
#   bash pipeline/lib/fetch_libs.sh --update           # re-resolve the latest versions instead of the pinned ones
#   options: --vendor DIR   --lock FILE   --quiet
#
# WHAT IT DOES. For each package named in libs.lock.json (gsap, Noto Sans, Kalam, Noto Sans Devanagari
# on day 1; the other script fonts only on request) it runs, in a brand-new empty work folder outside the
# repository:
#     npm view <pkg>@<version> dist.integrity      the registry's own hash
#     npm pack <pkg>@<version> --ignore-scripts    download the tarball; nothing is installed, no lifecycle script runs
#     tar -tzf / tar -xzf <only the named members> list first, refuse unsafe names, extract just the files needed
# then checks the tarball against the registry hash and (when pinned) against the SHA-256 in the lock file,
# copies single files into vendor/js and vendor/fonts, copies the font licence text to pipeline/lib/licences/,
# and writes the versions and SHA-256 values it actually fetched back into libs.lock.json.
# The version is "confirmed at fetch time": with no pin it asks npm for the latest and records the answer.
#
# WHAT IT NEVER DOES. It never runs a package, a build tool or an install script, never runs npm inside a
# downloaded tree, never writes outside vendor/, pipeline/lib/licences/ and libs.lock.json, never reads or
# prints your user name, host name or home folder, and never commits anything. vendor/ is git-ignored.
# GSAP is not committed (its licence is not OSI-approved); fetch it on demand.
#
# EXIT CODES. 0 done (or already up to date). 1 a check failed: a downloaded file does not match the lock or
# the registry hash, or a package has a different licence than recorded. 2 bad usage. 3 environment problem:
# a tool is missing or the npm registry could not be reached (the exact npm error is printed).
# Without the registry the scene still runs: only ?gsap=1 and the font checks need these files.
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export LJ_FETCH_LIB_DIR="$here"
export LJ_FETCH_REPO_DIR="$(cd "$here/../.." && pwd)"

for t in python3 npm tar sha256sum df; do
  if ! command -v "$t" >/dev/null 2>&1; then
    echo "fetch_libs: required tool not found: $t" >&2
    exit 3
  fi
done

case "${1:-}" in
  -h|--help) sed -n '2,/^set -u/p' "${BASH_SOURCE[0]}" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
esac

exec python3 -I - "$@" <<'PYEOF'
import base64, datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile

LIB_DIR = os.environ["LJ_FETCH_LIB_DIR"]
REPO = os.environ["LJ_FETCH_REPO_DIR"]
EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_ENV = 0, 1, 2, 3


def say(msg=""):
    if not QUIET:
        print(msg, flush=True)


def die(code, msg):
    print("fetch_libs: " + msg, file=sys.stderr, flush=True)
    sys.exit(code)


def usage():
    print("usage: bash pipeline/lib/fetch_libs.sh [--check] [--scripts LIST|all] [--update] [--vendor DIR] [--lock FILE] [--quiet]")


args = sys.argv[1:]
QUIET = False
CHECK = False
UPDATE = False
SCRIPTS = set()
VENDOR = os.path.join(REPO, "vendor")
LOCK = os.path.join(LIB_DIR, "libs.lock.json")
i = 0
while i < len(args):
    a = args[i]
    if a in ("-h", "--help"):
        usage(); sys.exit(0)
    elif a == "--quiet": QUIET = True
    elif a == "--check": CHECK = True
    elif a == "--update": UPDATE = True
    elif a in ("--scripts", "--vendor", "--lock"):
        if i + 1 >= len(args): die(EXIT_USAGE, a + " needs a value")
        v = args[i + 1]; i += 1
        if a == "--scripts": SCRIPTS |= {s.strip().lower() for s in v.split(",") if s.strip()}
        elif a == "--vendor": VENDOR = os.path.abspath(v)
        else: LOCK = os.path.abspath(v)
    else:
        die(EXIT_USAGE, "unknown option: " + a)
    i += 1

LIC_DIR = os.path.join(os.path.dirname(LOCK), "licences")


def read_lock():
    try:
        with open(LOCK, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError) as e:
        die(EXIT_USAGE, "cannot read the lock file: %s" % e)
    if d.get("schema") != "lj-libs/1":
        die(EXIT_USAGE, "lock file schema is not lj-libs/1")
    return d


def write_lock(d):
    tmp = LOCK + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, LOCK)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def integrity_of(p):
    h = hashlib.sha512()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha512-" + base64.b64encode(h.digest()).decode("ascii")


def df_mb():
    try:
        out = subprocess.run(["df", "-BM", "-P", REPO], capture_output=True, text=True, env=dict(os.environ, LC_ALL="C")).stdout.splitlines()
        return int(out[1].split()[3].rstrip("M"))
    except Exception:
        return None


def want_fonts(lock):
    """Fonts to fetch now: day-1 entries always, pending ones only when asked."""
    out = []
    for f in lock["fonts"]:
        if f["status"] == "day1" or "all" in SCRIPTS or (set(f["scripts"]) & SCRIPTS):
            out.append(f)
    unknown = {s for s in SCRIPTS if s != "all"} - {s for f in lock["fonts"] for s in f["scripts"]}
    if unknown:
        die(EXIT_USAGE, "no font entry for script(s): " + ", ".join(sorted(unknown)))
    return out


def font_targets(f):
    """Relative (to vendor) files a font entry should have. woff2 for every face, woff for the face whose
    subset is named like the script (the Pillow reference in the font test reads that one)."""
    slug = f["npm"].split("/")[-1]
    t = []
    for sub in f["subsets"]:
        for w in f["weights"]:
            t.append(("fonts/%s-%s-%d-normal.woff2" % (slug, sub, w), sub, w, "woff2"))
            if sub in f["scripts"] and w == 400:
                t.append(("fonts/%s-%s-%d-normal.woff" % (slug, sub, w), sub, w, "woff"))
    return t


def check_entry_files(entry, kind):
    """Return list of (relative path, status) for the files the lock records for this entry."""
    res = []
    if kind == "lib":
        recs = entry.get("files", [])
    else:
        recs = [x for face in entry.get("faces", []) for x in face["files"].values()]
    for r in recs:
        p = os.path.join(VENDOR, r["to"])
        if not os.path.isfile(p):
            res.append((r["to"], "MISSING"))
        elif sha256_file(p) != r["sha256"]:
            res.append((r["to"], "MISMATCH"))
        else:
            res.append((r["to"], "OK"))
    return res


def entry_satisfied(entry, kind):
    if not entry.get("version"):
        return False
    st = check_entry_files(entry, kind)
    return bool(st) and all(s == "OK" for _, s in st)


# ----------------------------------------------------------------------------------------- --check
lock = read_lock()
if CHECK:
    bad = 0
    for e in lock["libs"]:
        for rel, st in check_entry_files(e, "lib") or [("(not fetched yet)", "MISSING")]:
            print("%-9s %s %s" % (st, e["id"], rel)); bad += st != "OK"
    for e in want_fonts(lock):
        if e["status"] != "day1" and not e.get("faces"):
            continue
        for rel, st in check_entry_files(e, "font") or [("(not fetched yet)", "MISSING")]:
            print("%-9s %s %s" % (st, e["id"], rel)); bad += st != "OK"
    for e in lock["fonts"]:
        if e["status"] != "day1" and not e.get("faces"):
            print("%-9s %s (pending_O-10: not fetched; package_confirmed=%s)" % ("PENDING", e["id"], e.get("package_confirmed")))
    print("check: %s" % ("all files match the lock" if not bad else "%d file(s) missing or different (run fetch_libs.sh)" % bad))
    sys.exit(EXIT_OK if not bad else EXIT_FAIL)

# ----------------------------------------------------------------------------------------- fetch
WANT = want_fonts(lock)
scratch_root = os.environ.get("LJ_SCRATCH") or os.path.join(os.path.dirname(REPO), "build-scratch")
try:
    os.makedirs(scratch_root, exist_ok=True)
    WORK = tempfile.mkdtemp(prefix="libs-", dir=scratch_root)
except OSError as e:
    die(EXIT_ENV, "cannot create a work folder in the scratch area: %s" % e.strerror)

ENV = dict(os.environ)
ENV.update({
    "NPM_CONFIG_CACHE": os.path.join(WORK, "npm-cache"),   # throw-away cache: deleted with the work folder
    "npm_config_update_notifier": "false",
    "npm_config_fund": "false",
    "npm_config_audit": "false",
    "npm_config_ignore_scripts": "true",
    "npm_config_loglevel": "error",
})


def npm(cmd_args, cwd):
    """Run npm in a fresh empty folder; on failure print npm's exact error and exit 3."""
    cmd = ["npm"] + cmd_args
    say("  $ " + " ".join(cmd).replace(WORK, "<work>"))
    try:
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
    except subprocess.TimeoutExpired:
        cleanup(); die(EXIT_ENV, "npm timed out after 300 s: " + " ".join(cmd))
    if r.returncode != 0:
        cleanup()
        sys.stderr.write("fetch_libs: npm failed (exit %d): %s\n" % (r.returncode, " ".join(cmd)))
        sys.stderr.write(r.stderr or r.stdout)
        sys.stderr.write("fetch_libs: the npm registry could not be used; nothing was changed. Scenes still run; only ?gsap=1 and the font checks need these files.\n")
        sys.exit(EXIT_ENV)
    return r.stdout


def cleanup():
    shutil.rmtree(WORK, ignore_errors=True)


def tar_list(tgz):
    r = subprocess.run(["tar", "-tzf", tgz], capture_output=True, text=True)
    if r.returncode != 0:
        cleanup(); die(EXIT_FAIL, "cannot list the tarball: " + r.stderr.strip())
    names = [n for n in r.stdout.splitlines() if n]
    for n in names:
        if n.startswith("/") or ".." in n.split("/") or not n.startswith("package/"):
            cleanup(); die(EXIT_FAIL, "unsafe member name in tarball, nothing extracted: " + n)
    return set(names)


def tar_extract(tgz, dest, members):
    os.makedirs(dest, exist_ok=True)
    r = subprocess.run(["tar", "-xzf", tgz, "-C", dest, "--no-same-owner", "--no-same-permissions"] + sorted(members), capture_output=True, text=True)
    if r.returncode != 0:
        cleanup(); die(EXIT_FAIL, "tar extract failed: " + r.stderr.strip())


def fetch_package(npm_name, pinned, label):
    """npm view + npm pack into a new empty folder; returns (version, tgz path, integrity, sha256, bytes)."""
    if pinned and not UPDATE:
        version = pinned
    else:
        version = json.loads(npm(["view", npm_name, "version", "--json"], WORK))
    spec = "%s@%s" % (npm_name, version)
    reg_integrity = json.loads(npm(["view", spec, "dist.integrity", "--json"], WORK))
    d = tempfile.mkdtemp(prefix="pack-", dir=WORK)
    out = npm(["pack", spec, "--pack-destination", d, "--json"], d)
    json.loads(out)  # npm pack --json: must be valid JSON
    cands = [f for f in os.listdir(d) if f.endswith(".tgz")]
    if len(cands) != 1:
        cleanup(); die(EXIT_FAIL, "npm pack wrote an unexpected set of files for " + spec)
    tgz = os.path.join(d, cands[0])
    got = integrity_of(tgz)
    if got != reg_integrity:
        cleanup(); die(EXIT_FAIL, "%s: tarball hash %s does not match the registry's %s" % (spec, got[:24] + "...", reg_integrity[:24] + "..."))
    return version, tgz, got, sha256_file(tgz), os.path.getsize(tgz)


def parse_css(text):
    faces = []
    for m in re.finditer(r"/\*\s*([^*]+?)\s*\*/\s*@font-face\s*\{(.*?)\}", text, re.S):
        body = m.group(2)
        def g(rx):
            mm = re.search(rx, body)
            return mm.group(1).strip() if mm else None
        faces.append({
            "name": m.group(1).strip(),
            "family": g(r"font-family:\s*'([^']+)'"),
            "style": g(r"font-style:\s*(\w+)"),
            "weight": int(g(r"font-weight:\s*(\d+)") or 0),
            "unicode_range": g(r"unicode-range:\s*([^;]+);"),
        })
    return faces


def copy_to_vendor(src, rel):
    dst = os.path.join(VENDOR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".tmp"
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)
    return {"to": rel, "sha256": sha256_file(dst), "bytes": os.path.getsize(dst)}


def verify_pin(entry, sha256, what):
    """If the lock already records a tarball hash for this exact version, a different download is a finding."""
    t = entry.get("tarball")
    if t and entry.get("version") and not UPDATE and t.get("sha256") and t["sha256"] != sha256:
        cleanup(); die(EXIT_FAIL, "%s: downloaded tarball SHA-256 %s differs from the lock's %s" % (what, sha256[:16] + "...", t["sha256"][:16] + "..."))


today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
avail0 = df_mb()
changed = False
fetched_bytes = 0
say("fetch_libs: vendor folder %s" % os.path.relpath(VENDOR, REPO) if VENDOR.startswith(REPO) else "fetch_libs: vendor folder (outside the repo)")
say("fetch_libs: free disk before: %s MB" % avail0)

# ---- libraries (gsap)
for e in lock["libs"]:
    if entry_satisfied(e, "lib") and not UPDATE:
        say("[ok ] %s %s already in vendor/, matches the lock" % (e["id"], e["version"])); continue
    say("[get] %s (%s)" % (e["id"], e["npm"]))
    version, tgz, integ, sha, size = fetch_package(e["npm"], e.get("version") or None, e["id"])
    verify_pin(e, sha, e["id"])
    members = {m["member"] for m in e["members"]} | {"package/package.json"}
    names = tar_list(tgz)
    missing = {m for m in members if m not in names}
    if missing:
        cleanup(); die(EXIT_FAIL, "%s %s: tarball lacks %s" % (e["id"], version, ", ".join(sorted(missing))))
    ex = tempfile.mkdtemp(prefix="ex-", dir=WORK)
    tar_extract(tgz, ex, members)
    pkg = json.load(open(os.path.join(ex, "package/package.json"), encoding="utf-8"))
    if e.get("expected_version") and version != e["expected_version"]:
        say("      note: version %s differs from the planner's expectation %s; the lock records what was fetched" % (version, e["expected_version"]))
    files = [copy_to_vendor(os.path.join(ex, m["member"]), m["to"]) for m in e["members"]]
    if not os.path.isfile(os.path.join(LIB_DIR, e["licence_file"])):
        cleanup(); die(EXIT_FAIL, "licence record missing: pipeline/lib/%s (commit it before fetching)" % e["licence_file"])
    e.update({"version": version, "licence_declared": pkg.get("license"), "fetched_utc_date": today,
              "tarball": {"sha256": sha, "integrity": integ, "bytes": size}, "files": files})
    fetched_bytes += size; changed = True
    say("      %s %s: %d file(s), tarball %d bytes, sha256 %s..." % (e["id"], version, len(files), size, sha[:16]))

# ---- fonts
for e in lock["fonts"]:
    if e["status"] != "day1" and e not in WANT:
        # pending: only confirm that the package name exists (metadata only), once
        if e.get("package_confirmed") is None:
            try:
                r = subprocess.run(["npm", "view", e["npm"], "version", "--json"], cwd=WORK, env=ENV, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
            except subprocess.TimeoutExpired:
                r = None
            if r is not None and r.returncode == 0:
                e["package_confirmed"] = True; e["confirmed_version"] = json.loads(r.stdout); e["confirmed_utc_date"] = today
                e["unverified"] = "package name exists; subsets, file names and glyph coverage not yet checked (no strings for this script until O-10)"
                changed = True
                say("[pend] %s: package exists (version %s), not fetched" % (e["id"], e["confirmed_version"]))
            else:
                say("[pend] %s: could not confirm the package name (left unconfirmed)" % e["id"])
        continue
    if entry_satisfied(e, "font") and not UPDATE:
        say("[ok ] %s %s already in vendor/, matches the lock" % (e["id"], e["version"])); continue
    say("[get] %s (%s)" % (e["id"], e["npm"]))
    version, tgz, integ, sha, size = fetch_package(e["npm"], e.get("version") or None, e["id"])
    verify_pin(e, sha, e["id"])
    slug = e["npm"].split("/")[-1]
    targets = font_targets(e)
    members = {"package/package.json", "package/LICENSE"} | {"package/%d.css" % w for w in e["weights"]}
    members |= {"package/files/%s-%s-%d-normal.%s" % (slug, sub, w, fmt) for (_, sub, w, fmt) in targets}
    names = tar_list(tgz)
    missing = {m for m in members if m not in names}
    if missing:
        cleanup(); die(EXIT_FAIL, "%s %s: tarball lacks %s (the subset or weight names in libs.lock.json need correcting)" % (e["id"], version, ", ".join(sorted(missing))))
    ex = tempfile.mkdtemp(prefix="ex-", dir=WORK)
    tar_extract(tgz, ex, members)
    pkg = json.load(open(os.path.join(ex, "package/package.json"), encoding="utf-8"))
    if pkg.get("license") != e["licence_spdx"]:
        cleanup(); die(EXIT_FAIL, "%s %s declares licence %r, the lock records %r; read the new licence before using it" % (e["id"], version, pkg.get("license"), e["licence_spdx"]))
    faces = []
    for w in e["weights"]:
        css = parse_css(open(os.path.join(ex, "package/%d.css" % w), encoding="utf-8").read())
        for sub in e["subsets"]:
            cf = [c for c in css if c["name"] == "%s-%s-%d-normal" % (slug, sub, w)]
            if len(cf) != 1:
                cleanup(); die(EXIT_FAIL, "%s %s: no @font-face for subset %s weight %d in %d.css" % (e["id"], version, sub, w, w))
            if cf[0]["family"] != e["family"]:
                cleanup(); die(EXIT_FAIL, "%s %s: CSS family %r is not the lock's %r" % (e["id"], version, cf[0]["family"], e["family"]))
            files = {}
            for (rel, tsub, tw, fmt) in targets:
                if tsub == sub and tw == w:
                    files[fmt] = copy_to_vendor(os.path.join(ex, "package/files/%s-%s-%d-normal.%s" % (slug, sub, w, fmt)), rel)
            faces.append({"subset": sub, "weight": w, "style": "normal", "unicode_range": cf[0]["unicode_range"], "files": files})
    os.makedirs(LIC_DIR, exist_ok=True)
    shutil.copyfile(os.path.join(ex, "package/LICENSE"), os.path.join(os.path.dirname(LOCK), e["licence_file"]))
    e.update({"version": version, "licence_declared": pkg.get("license"), "fetched_utc_date": today,
              "tarball": {"sha256": sha, "integrity": integ, "bytes": size}, "faces": faces, "fetched": True})
    if e["status"] != "day1":
        e["package_confirmed"] = True; e["confirmed_version"] = version; e["confirmed_utc_date"] = today
        e["unverified"] = "package fetched and its subset files exist; glyph coverage of the reader's strings not yet checked (A7 runs when strings exist)"
    fetched_bytes += size; changed = True
    nfiles = sum(len(f["files"]) for f in faces)
    say("      %s %s: %d font file(s), tarball %d bytes, sha256 %s..." % (e["id"], version, nfiles, size, sha[:16]))

if changed:
    write_lock(lock)
    say("fetch_libs: libs.lock.json updated")
cleanup()
avail1 = df_mb()
say("fetch_libs: tarballs downloaded: %d bytes; free disk after: %s MB; work folder removed" % (fetched_bytes, avail1))
say("fetch_libs: done")
sys.exit(EXIT_OK)
PYEOF
