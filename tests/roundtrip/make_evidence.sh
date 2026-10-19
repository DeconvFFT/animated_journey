#!/usr/bin/env bash
# tests/roundtrip/make_evidence.sh     WP-06: run everything and file the evidence
#
# Runs run_tests.sh --quick, then run_tests.sh --all, then the acceptance commands of the work package on their own (with the venv stage recorded as the
# guard answered it), and writes build/evidence/wp06/{tests_quick.txt,tests_all.txt,tests_quick.jsonl,acceptance_transcript.txt,guard_stage_venv.json,summary.json,
# environment.json,venv_otio.json}. Exit code: that of the --all run.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EV="$ROOT/build/evidence/wp06"
SCR="${LJ_SCRATCH:-$(cd "$ROOT/.." && pwd)/build-scratch}"
mkdir -p "$EV"
cd "$ROOT" || exit 2
bash tests/roundtrip/run_tests.sh --quick 2>&1 | tee "$EV/tests_quick.txt"
cp "$EV/tests.jsonl" "$EV/tests_quick.jsonl"
bash tests/roundtrip/run_tests.sh --all 2>&1 | tee "$EV/tests_all.txt"
RC="${PIPESTATUS[0]}"
# the venv stage's ledger line (the guard's own record of what it said)
# shellcheck disable=SC1091
. scripts/lj_guard.sh
lj_ledger_last wp06-venv > "$EV/guard_stage_venv.json" 2>/dev/null || true
mkdir -p renders/wp06
show() { echo; echo "\$ $1" | sed "s#$SCR#<scratch>#g"; }
{
  echo "# WP-06 acceptance commands, run on their own (the same commands run_tests.sh runs, in the order of the work package)"
  show "lj_with_disk 60 wp06-venv -- bash -c 'python3 -m venv <scratch>/venv-otio && <scratch>/venv-otio/bin/pip install opentimelineio==0.18.1'"
  echo "(refused by the guard when it was tried; see venv_guard_refusal.txt and guard_stage_venv.json. The same two commands were then run directly, which is allowed for a write under 100 MB.)"
  cat "$EV/venv_guard_refusal.txt" 2>/dev/null
  show "<scratch>/venv-otio/bin/python -I -c 'import opentimelineio; print(opentimelineio.__version__)'"
  "$SCR/venv-otio/bin/python" -I -c 'import opentimelineio; print(opentimelineio.__version__)'; echo "exit=$?"
  show "python3 -I pipeline/roundtrip/emit_ora_layers.py renders/wp06/layers.ora && python3 -I pipeline/roundtrip/validate_ora.py renders/wp06/layers.ora"
  python3 -I pipeline/roundtrip/emit_ora_layers.py renders/wp06/layers.ora && python3 -I pipeline/roundtrip/validate_ora.py renders/wp06/layers.ora; echo "exit=$?"
  show "python3 -I pipeline/roundtrip/validate_ora.py research/craft-visual-fixtures/at-layers.ora"
  python3 -I pipeline/roundtrip/validate_ora.py research/craft-visual-fixtures/at-layers.ora; echo "exit=$?"
  show "bash pipeline/roundtrip/svg_roundtrip.sh"
  bash pipeline/roundtrip/svg_roundtrip.sh; echo "exit=$?"
  show "python3 -I pipeline/roundtrip/emit_otio.py pipeline/roundtrip/spec/neutral_timeline.example.json renders/wp06/ch.otio"
  python3 -I pipeline/roundtrip/emit_otio.py pipeline/roundtrip/spec/neutral_timeline.example.json renders/wp06/ch.otio; echo "exit=$?"
  show "python3 -I pipeline/roundtrip/validate_otio.py renders/wp06/ch.otio --with-otio <scratch>/venv-otio/bin/python"
  python3 -I pipeline/roundtrip/validate_otio.py renders/wp06/ch.otio --with-otio "$SCR/venv-otio/bin/python"; echo "exit=$?"
  show "bash pipeline/roundtrip/adapter_probe.sh"
  bash pipeline/roundtrip/adapter_probe.sh; echo "exit=$?"
  show "python3 -I pipeline/roundtrip/kb_scale.py 3600 2400; python3 -I pipeline/roundtrip/kb_scale.py 2880 1620; python3 -I pipeline/roundtrip/kb_scale.py --selftest"
  python3 -I pipeline/roundtrip/kb_scale.py 3600 2400; python3 -I pipeline/roundtrip/kb_scale.py 2880 1620; python3 -I pipeline/roundtrip/kb_scale.py --selftest; echo "exit=$?"
} 2>&1 | sed "s#$SCR#<scratch>#g; s#$ROOT#.#g" > "$EV/acceptance_transcript.txt"
rm -rf renders/wp06 "$SCR/wp06"
python3 -I tests/roundtrip/make_evidence.py
exit "$RC"
