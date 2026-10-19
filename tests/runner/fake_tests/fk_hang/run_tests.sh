#!/usr/bin/env bash
# Fake HANGING area for tests/runner. Ignores TERM, starts a background child, records both pids in
# $FK_PIDFILE (if set) and sleeps for 300 s. The runner must kill the whole process group.
set -u
trap '' TERM
sleep 300 &
child=$!
[[ -n "${FK_PIDFILE:-}" ]] && printf '%s %s\n' "$$" "$child" > "$FK_PIDFILE"
echo "fk_hang: mode=${1#--} (about to hang)"
sleep 300
echo "fk_hang: should never get here"
