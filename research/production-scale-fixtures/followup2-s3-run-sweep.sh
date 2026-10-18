#!/bin/bash
PY=/tmp/claude-0/-home-user/8016b042-43ae-5ade-a7e4-661ffdf4579d/scratchpad/bpyenv/venv/bin/python
SC=research/production-scale-fixtures/followup2-s3-kitchen-standin.py
OUT=/tmp/claude-0/-home-user/8016b042-43ae-5ade-a7e4-661ffdf4579d/scratchpad/s3out
echo "container: $(nproc) vCPU, $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2), $(free -g | awk '/Mem/{print $2}') GB RAM, no GPU" 
for cfg in "8 0 0" "64 0 0" "128 0 0" "64 1 0" "128 1 0" "128 1 1" "64 1 0"; do
  set -- $cfg
  s=$(date +%s.%N)
  $PY $SC -- $OUT 1920 1080 $1 $2 $3 2>/dev/null | grep RESULT
  e=$(date +%s.%N)
  echo "  process_total_s=$(echo "$e - $s" | bc)"
done
echo ALLDONE
