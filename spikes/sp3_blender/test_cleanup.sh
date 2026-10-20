#!/usr/bin/env bash
# test_cleanup.sh: regression test for the SP3 cleanup defect found in the first real run (Tue 20 Oct 2026).
#
#   bash spikes/sp3_blender/test_cleanup.sh                 test the repository's run_sp3.sh        (exit 0 PASS, 1 FAIL)
#   bash spikes/sp3_blender/test_cleanup.sh --script FILE   test another copy of the script (for example the one before the fix:
#                                                            git show <commit>:spikes/sp3_blender/run_sp3.sh > /tmp/old.sh)
#
# THE DEFECT. run_inner kept its work folder in a local variable S and cleaned up with  trap 'rm -rf -- "$S"' EXIT.  An EXIT trap runs when the whole
# script exits, after run_inner has returned, when the local S no longer exists; under set -u that is "S: unbound variable" and rm never ran, so the
# venv (1,008 MB) and the renders (14 MB) were left on the shared volume. A failing step (die inside the function) hid it, because the trap then runs
# while S is still in scope. So the test must let run_inner run to the END.
#
# HOW. A temporary copy of the repository layout (the script, scripts/lj_guard.sh) and a stand-in python3 on PATH: "python3 -m venv DIR" makes a fake venv whose
# python answers pip, the bpy version query and the scene run, all successfully. No Blender, no download, no network, a few seconds, under 1 MB.
# PASS means: run_inner exits 0, the work folder is gone, and nothing says "unbound variable". Writes only under a mktemp folder, removed at the end.
set -u
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SUT="$HERE/run_sp3.sh"
if [[ "${1:-}" == "--script" ]]; then SUT="${2:-}"; [[ -f "$SUT" ]] || { echo "test_cleanup: no such file: ${2:-}" >&2; exit 2; }; fi
T="$(mktemp -d)" || { echo "test_cleanup: cannot make a temporary folder" >&2; exit 2; }
trap 'rm -rf -- "$T"' EXIT
mkdir -p "$T/root/spikes/sp3_blender" "$T/root/scripts" "$T/root/build/evidence/wp10" "$T/scratch" "$T/shim"
cp "$ROOT/scripts/lj_guard.sh" "$T/root/scripts/lj_guard.sh"
cp "$SUT" "$T/root/spikes/sp3_blender/run_sp3.sh"
cat > "$T/shim/python3" <<'EOF'
#!/usr/bin/env bash
if [[ "${1:-}" == "-m" && "${2:-}" == "venv" ]]; then
  mkdir -p "$3/bin"
  cat > "$3/bin/python" <<'EOP'
#!/usr/bin/env bash
case "$*" in
  *"-m pip"*) exit 0;;
  *"import bpy"*) echo "5.2.2 LTS"; exit 0;;
  *) echo "RESULT fake-scene-line"; exit 0;;
esac
EOP
  chmod +x "$3/bin/python"; exit 0
fi
exec /usr/bin/python3 "$@"
EOF
chmod +x "$T/shim/python3"
out="$(PATH="$T/shim:$PATH" LJ_SCRATCH="$T/scratch" bash "$T/root/spikes/sp3_blender/run_sp3.sh" --run-inner 2>&1)"; rc=$?
left="no"; [[ -e "$T/scratch/sp3" ]] && left="yes"
bad="no"; grep -q "unbound variable" <<<"$out" && bad="yes"
echo "run_inner exit code: $rc; work folder left behind: $left; 'unbound variable' in the output: $bad"
if [[ $rc -eq 0 && "$left" == "no" && "$bad" == "no" ]]; then echo "PASS: the work folder is removed when run_inner runs to the end"; exit 0; fi
echo "FAIL: the work folder is not removed (or run_inner failed)"; exit 1
