#!/usr/bin/env bash
# adapter_probe.sh: which OpenTimelineIO adapters can write EDL, FCPXML, Kdenlive and MLT here? (WP-06, SP5 hand-off half)
#
#   bash pipeline/roundtrip/adapter_probe.sh [--json FILE] [--python PY] [--with-plugins] [--keep]
#
# WHAT IT DOES (each step is printed before it runs)
#   1  finds the opentimelineio interpreter (default <scratch>/venv-otio/bin/python, pinned opentimelineio==0.18.1)
#   2  writes a synthetic 24 fps timeline169.json from the neutral spec (emit_otio.py --timeline169; no media is created) into a scratch folder
#      <scratch>/wp06/adapter_probe/, because the reused script reads exactly that file name and writes ABSOLUTE paths
#   3  runs research/sources/format-round1/make_otio.py UNCHANGED there (python -I): it writes out.otio and tries the adapters cmx_3600 (EDL),
#      fcpx_xml (FCPXML), kdenlive and mlt_xml, printing WROTE or FAIL for each, then reads out.otio back
#   4  turns that output into JSON (which adapters worked, bytes, the frame rate found in each written file, the error text of those that did not)
#      with every folder name replaced by <work>; the JSON goes to stdout and, with --json, to FILE
#   5  --with-plugins only: repeats 3 and 4 in a THROW-AWAY venv holding opentimelineio==0.18.1 plus the four adapter plug-in packages
#      (otio-cmx3600-adapter 1.0.0, otio-fcpx-xml-adapter 1.0.0, otio-kdenlive-adapter 0.0.3, otio-mlt-adapter 0.3.0; about 4 MB from PyPI, pip --no-cache-dir),
#      then deletes that venv (--keep leaves it). This answers "would the adapters work if they were installed?" without touching venv-otio.
#
# WHY TWO RESULTS. opentimelineio 0.18.1 on its own ships only the otio_json, otioz and otiod adapters; the EDL, FCPXML, Kdenlive and MLT adapters are
# separate packages (research/sources/format-round1/README.txt names them). So the default probe is expected to report all four as NOT working; that is a
# finding, not a failure. Exit 0 means the probe ran and out.otio was written and read back.
#
# It writes only under <scratch>/wp06/ (removed and re-created each run), the --json file, and (with --with-plugins) one venv there. It prints no
# absolute path. PowerShell is not involved: this script is Linux-only; the maker's FilmCraft does its own EDL/FCPXML export (WP-10 T3).
#
# EXIT CODES (build plan 4.3)  0 probe ran, out.otio written and read back   1 out.otio could not be written or read back   2 bad usage
#                              3 environment (no interpreter, no module, pip failed for --with-plugins)
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HERE="$ROOT/pipeline/roundtrip"
MAKE_OTIO="$ROOT/research/sources/format-round1/make_otio.py"
SPEC="$HERE/spec/neutral_timeline.example.json"
SCRATCH="${LJ_SCRATCH:-$(cd "$ROOT/.." && pwd)/build-scratch}"
PY="$SCRATCH/venv-otio/bin/python"; JSON=""; PLUGINS=0; KEEP=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --json) JSON="$2"; shift;;
    --python) PY="$2"; shift;;
    --with-plugins) PLUGINS=1;;
    --keep) KEEP=1;;
    *) echo "usage: adapter_probe.sh [--json FILE] [--python PY] [--with-plugins] [--keep]" >&2; exit 2;;
  esac
  shift
done
echo "[1/5] looking for the opentimelineio interpreter (<scratch>/venv-otio by default) ..."
[ -x "$PY" ] || { echo "adapter_probe: no interpreter at the expected place; create the venv first (see README: python3 -m venv <scratch>/venv-otio and pip install opentimelineio==0.18.1)" >&2; exit 3; }
"$PY" -I -c "import opentimelineio" 2>/dev/null || { echo "adapter_probe: that interpreter has no opentimelineio module" >&2; exit 3; }
[ -f "$MAKE_OTIO" ] || { echo "adapter_probe: research/sources/format-round1/make_otio.py not found" >&2; exit 3; }
echo "      ok"
W="$SCRATCH/wp06/adapter_probe"
mkdir -p "$SCRATCH/wp06" || exit 3
rm -rf "$W" "$SCRATCH/wp06/adapter_probe_plugins"; mkdir -p "$W" || exit 3
echo "[2/5] writing the synthetic 24 fps timeline169.json from the neutral spec (no media files are created) ..."
python3 -I -B "$HERE/emit_otio.py" "$SPEC" --timeline169 "$W/timeline169.json" >/dev/null || { echo "adapter_probe: emit_otio.py failed" >&2; exit 1; }
echo "      ok"

run_probe() {   # PYTHON WORKDIR -> leaves make_otio's output in WORKDIR/probe_stdout.txt and its exit code in WORKDIR/probe_exit.txt
  local py="$1" dir="$2"
  mkdir -p "$dir"; [ "$dir" = "$W" ] || cp "$W/timeline169.json" "$dir/timeline169.json"
  ( cd "$dir" && "$py" -I -B "$MAKE_OTIO" > probe_stdout.txt 2> probe_stderr.txt; echo $? > probe_exit.txt )
}

echo "[3/5] running the reused make_otio.py, unchanged, in the scratch folder (core adapters only) ..."
run_probe "$PY" "$W"
sed 's/^/      /' "$W/probe_stdout.txt"
echo "      make_otio.py exit $(cat "$W/probe_exit.txt")"

PW=""; PKGS_RC=0
[ "$PLUGINS" = 1 ] || echo "[4/5] plug-in venv: skipped (add --with-plugins to build it and probe again)"
if [ "$PLUGINS" = 1 ]; then
  echo "[4/5] building a throw-away venv with the four adapter plug-in packages (pip, about 4 MB) ..."
  PV="$SCRATCH/wp06/adapter_probe_plugins"; PW="$PV/work"
  mkdir -p "$PV"
  if python3 -m venv --without-pip "$PV/venv" && "$PY" -m pip --python "$PV/venv/bin/python" install --no-cache-dir --disable-pip-version-check -q \
       opentimelineio==0.18.1 otio-cmx3600-adapter==1.0.0 otio-fcpx-xml-adapter==1.0.0 otio-kdenlive-adapter==0.0.3 otio-mlt-adapter==0.3.0 > "$PV/pip.txt" 2>&1; then
    echo "      installed; running make_otio.py unchanged again ..."
    run_probe "$PV/venv/bin/python" "$PW"
    sed 's/^/      /' "$PW/probe_stdout.txt"
    "$PV/venv/bin/python" -I -c "import opentimelineio as o; print('      adapters:', ', '.join(o.adapters.available_adapter_names()))"
  else
    echo "adapter_probe: the plug-in venv could not be built; last pip line: $(tail -n 1 "$PV/pip.txt" 2>/dev/null | cut -c1-160)" >&2
    PKGS_RC=3
  fi
fi

echo "[5/5] turning the output into JSON (folders replaced by <work>) ..."
OUTJSON="$SCRATCH/wp06/adapter_probe.json"
python3 -I - "$W" "$PW" "$MAKE_OTIO" "$OUTJSON" "$PKGS_RC" "$ROOT" "$PY" <<'PY'
import ast, hashlib, json, os, re, subprocess, sys
work, pwork, make_otio, out, pkgs_rc, root, core_py = sys.argv[1:8]
ADAPTERS = [("cmx_3600", "EDL (CMX 3600)", "otio-cmx3600-adapter"), ("fcpx_xml", "FCPXML", "otio-fcpx-xml-adapter"),
            ("kdenlive", "Kdenlive project", "otio-kdenlive-adapter"), ("mlt_xml", "MLT XML", "otio-mlt-adapter")]
HINTS = {"fcpx_xml": r'frameDuration="([^"]+)"', "kdenlive": r'frame_rate_num="(\d+)"', "mlt_xml": r'frame_rate_num="(\d+)"', "cmx_3600": ""}
EXT = {"cmx_3600": "edl", "fcpx_xml": "fcpxml", "kdenlive": "kdenlive", "mlt_xml": "mlt"}

def clean(s, *dirs):
    for d in dirs:
        if d:
            s = s.replace(d, "<work>")
    s = re.sub(r"/[^\s'\"]*/", "<dir>/", s)
    return s.split(" options:")[0][:240]

def parse(dirpath):
    stdout = open(os.path.join(dirpath, "probe_stdout.txt"), encoding="utf-8", errors="replace").read().splitlines()
    rc = int(open(os.path.join(dirpath, "probe_exit.txt")).read().strip() or "1")
    res, clips = {}, None
    for line in stdout:
        m = re.match(r"WROTE (\S+) (\d+) bytes", line)
        if m:
            res[m.group(1)] = {"worked": True, "bytes": int(m.group(2)), "error": None}
        m = re.match(r"FAIL\s+(\S+) (\S+) ?(.*)", line)
        if m:
            res[m.group(1)] = {"worked": False, "bytes": None, "error": clean("%s: %s" % (m.group(2), m.group(3)), dirpath, work)}
        m = re.match(r"read back clips: (.*)", line)
        if m:
            try:
                clips = ast.literal_eval(m.group(1))
            except (ValueError, SyntaxError):
                clips = m.group(1)
    rows = {}
    for name, label, pkg in ADAPTERS:
        r = res.get(name, {"worked": False, "bytes": None, "error": "make_otio.py printed nothing for this adapter"})
        r = dict(r, label=label, plugin_package=pkg)
        f = os.path.join(dirpath, "out_otio." + EXT[name])
        if r["worked"] and os.path.isfile(f):
            text = open(f, encoding="utf-8", errors="replace").read()
            if name == "cmx_3600":     # an EDL has no rate field: the last timecode of a 480-frame (20 s) timeline reads 00:00:20:00 at 24 fps, 00:00:19:05 at 25
                tcs = re.findall(r"\d\d:\d\d:\d\d:\d\d", text)
                r["frame_rate_found_in_output"] = ("last timecode " + max(tcs)) if tcs else None
            else:
                m = re.search(HINTS[name], text, re.M)
                r["frame_rate_found_in_output"] = m.group(1) if m else None
        rows[name] = r
    plain = os.path.isfile(os.path.join(dirpath, "out.otio"))
    return {"make_otio_exit": rc, "plain_otio_written": plain, "read_back_clips": clips, "adapters": rows,
            "working": sorted(n for n, r in rows.items() if r["worked"])}

def adapters_of(py):
    try:
        o = subprocess.run([py, "-I", "-c", "import opentimelineio as o, json; print(json.dumps([o.__version__, o.adapters.available_adapter_names()]))"],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=60).stdout.decode()
        return json.loads(o)
    except Exception:
        return [None, []]

core = parse(work)
v, names = adapters_of(core_py)
tl = json.load(open(os.path.join(work, "timeline169.json")))
try:
    unchanged = subprocess.run(["git", "-C", root, "diff", "--quiet", "--", "research/sources/format-round1/make_otio.py"], timeout=30).returncode == 0
except Exception:
    unchanged = None
doc = {"schema": "lj-adapter-probe/1", "opentimelineio": v, "core_adapters_installed": names,
       "make_otio_sha256": hashlib.sha256(open(make_otio, "rb").read()).hexdigest(), "make_otio_unchanged_in_git": unchanged,
       "timeline169": {"fps": tl["fps"], "shots": len(tl["shots"]), "size": [tl["width"], tl["height"]]},
       "core_only": core, "with_plugins": None}
if pwork and os.path.isdir(pwork):
    pdoc = parse(pwork)
    pv, pnames = adapters_of(os.path.join(os.path.dirname(pwork), "venv", "bin", "python"))
    pdoc.update({"opentimelineio": pv, "adapters_installed": pnames})
    doc["with_plugins"] = pdoc
elif pkgs_rc != "0":
    doc["with_plugins"] = {"skipped": "the plug-in venv could not be built (pip or network)"}
doc["working_core_only"] = core["working"]
doc["finding"] = ("opentimelineio %s ships only %s; adapters that wrote a file with it alone: %s" % (v, ", ".join(names) or "?", ", ".join(core["working"]) or "none"))
text = json.dumps(doc, indent=2, sort_keys=True) + "\n"
open(out, "w", encoding="utf-8", newline="\n").write(text)
sys.stdout.write(text)
ok = core["plain_otio_written"] and core["make_otio_exit"] == 0 and core["read_back_clips"] is not None
sys.exit(0 if ok else 1)
PY
RC=$?
if [ -n "$JSON" ] && [ -f "$OUTJSON" ]; then mkdir -p "$(dirname "$JSON")" && cp "$OUTJSON" "$JSON"; fi
rm -f "$OUTJSON"
if [ "$PLUGINS" = 1 ] && [ "$KEEP" = 0 ]; then rm -rf "$SCRATCH/wp06/adapter_probe_plugins"; fi
[ "$RC" = 0 ] || { echo "adapter_probe: out.otio was not written or not read back (see the JSON above); make_otio.py stderr, last line: $(tail -n 1 "$W/probe_stderr.txt" 2>/dev/null | cut -c1-160)" >&2; rm -rf "$W"; exit 1; }
rm -rf "$W"
[ "$PKGS_RC" = 0 ] || exit "$PKGS_RC"
echo "files written: ${JSON:-none} (the scratch folder <scratch>/wp06/ is cleaned up; nothing under the repo changes)"
exit 0
