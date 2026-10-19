#!/usr/bin/env bash
# run_sp2.sh: the SP2 driver (Route A frame capture), build plan WP-04.
#
#   bash spikes/sp2_route_a/run_sp2.sh             # run every acceptance test, then collect results.json
#   bash spikes/sp2_route_a/run_sp2.sh --collect   # only collect results.json from build/evidence/wp04/ (no rendering)
#
# SP2 is judged by the package's tests (research/agent-pipeline.md R11, subset justified in the plan): this driver runs
# `bash tests/render/run_tests.sh --all` (timed runs under lj_bench, the 2,400-frame run under lj_with_disk) and then
# collect_results.py turns the evidence into results.json, one row per SP2 item (a) to (g), plus the pass/fail rule of R11.
# VERDICT-SP2.md is written by hand from results.json. It reads and writes only under the repository (renders/, build/evidence/wp04/,
# spikes/sp2_route_a/); it prints no host, user or absolute path.
set -u
cd "$(dirname "$0")/../.." || exit 3
if [ "${1:-}" != "--collect" ]; then
  bash tests/render/run_tests.sh --all
  rc=$?
else
  rc=0
fi
python3 -I spikes/sp2_route_a/collect_results.py || exit 3
exit $rc
