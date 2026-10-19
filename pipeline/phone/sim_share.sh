#!/usr/bin/env bash
# sim_share.sh IN.mp4 OUT.mp4 [--overwrite]      WP-08 (D-27): imitate what a messenger does to a phone file
#
# Re-encodes the file to 480p at about 1 Mbps with x264 veryfast (Main profile), the numbers of `degrade_shared` in pipeline/phone/thresholds.json (the one place they live),
# so that `python3 -I pipeline/phone/phone_check.py OUT.mp4` can say whether the captions, strokes and marks still read in the copy a relative would receive.
# It is a model of "a messenger", not any service's encoder (no service limits or behaviour are asserted anywhere; UNVERIFIED).
#
#   bash pipeline/phone/sim_share.sh renders/wp08/phone.mp4 renders/wp08/shared.mp4 && python3 -I pipeline/phone/phone_check.py renders/wp08/shared.mp4
#
# NEVER OVERWRITES ITS INPUT: it refuses when OUT is IN (same path, same file, or a link to it), refuses an existing OUT without --overwrite, writes OUT through a temporary
# name, and compares the SHA-256 of IN before and after (a change is an error, exit 3). Beside OUT it writes OUT.ass and OUT.phone.json (copies of IN's caption file and sidecar,
# the sidecar marked as a shared copy) so that phone_check.py can read them. It uses no network, prints base file names only, and needs ffmpeg, python3 and sha256sum.
# Exit codes: 0 done; 2 bad usage; 3 environment problem (a tool is missing, ffmpeg failed, the input changed).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IN="${1:-}"; OUT="${2:-}"; OVER=0
[ "${3:-}" = "--overwrite" ] && OVER=1
if [ -z "$IN" ] || [ -z "$OUT" ]; then
  sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
fi
for t in ffmpeg python3 sha256sum; do command -v "$t" >/dev/null 2>&1 || { echo "ENVIRONMENT PROBLEM: $t not found" >&2; exit 3; }; done
[ -f "$IN" ] || { echo "USAGE: the input $(basename "$IN") does not exist" >&2; exit 2; }
if [ -e "$OUT" ]; then
  if [ "$IN" -ef "$OUT" ]; then echo "USAGE: refusing: the output is the input ($(basename "$IN")); sim_share.sh never overwrites its input" >&2; exit 2; fi
  [ "$OVER" = 1 ] || { echo "USAGE: $(basename "$OUT") already exists (use --overwrite)" >&2; exit 2; }
fi
if [ "$(readlink -f "$IN")" = "$(readlink -f "$OUT")" ]; then echo "USAGE: refusing: the output is the input" >&2; exit 2; fi
case "$OUT" in *.mp4) ;; *) echo "USAGE: the output name must end in .mp4" >&2; exit 2;; esac

# the degrade numbers, read from thresholds.json (stdlib only)
read -r H VB MR BS PRE PROF AB < <(python3 -I - "$HERE/thresholds.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))["degrade_shared"]
print(d["height"], d["video_bitrate"], d["maxrate"], d["bufsize"], d["preset"], d["profile"], d["audio_bitrate"])
PY
)
[ -n "${H:-}" ] || { echo "ENVIRONMENT PROBLEM: could not read degrade_shared from thresholds.json" >&2; exit 3; }

H0="$(sha256sum "$IN" | cut -d' ' -f1)"
echo "sim_share.sh: $(basename "$IN") -> $(basename "$OUT"): ${H}p, ${VB} (max ${MR}), x264 ${PRE} ${PROF}, AAC ${AB}, faststart, no metadata"
echo "input SHA-256 before: ${H0:0:16}..."
TMP="${OUT}.part.mp4"
rm -f "$TMP"
TAGS="setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"
HAS_A="$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$IN" 2>/dev/null | head -1)"
AUDIO=(-an); [ -n "$HAS_A" ] && AUDIO=(-c:a aac -b:a "$AB" -ar 48000 -ac 2)
ffmpeg -hide_banner -nostdin -v error -y -i "$IN" \
  -vf "scale=-2:${H}:flags=bicubic:out_color_matrix=bt709:out_range=tv,format=yuv420p,${TAGS}" \
  -c:v libx264 -preset "$PRE" -profile:v "$PROF" -b:v "$VB" -maxrate "$MR" -bufsize "$BS" -g 48 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  "${AUDIO[@]}" -movflags +faststart -map_metadata -1 -fflags +bitexact -f mp4 "$TMP"
RC=$?
if [ "$RC" -ne 0 ] || [ ! -s "$TMP" ]; then rm -f "$TMP"; echo "ENVIRONMENT PROBLEM: ffmpeg failed (exit $RC)" >&2; exit 3; fi
mv -f "$TMP" "$OUT"
H1="$(sha256sum "$IN" | cut -d' ' -f1)"
if [ "$H0" != "$H1" ]; then echo "ENVIRONMENT PROBLEM: the input file changed while it was read (this must never happen)" >&2; exit 3; fi
echo "input SHA-256 after:  ${H1:0:16}... (unchanged)"

WROTE="$(basename "$OUT")"
if [ -f "$IN.ass" ]; then cp -f "$IN.ass" "$OUT.ass"; WROTE="$WROTE, $(basename "$OUT").ass"; fi
if [ -f "$IN.phone.json" ]; then
  python3 -I - "$IN.phone.json" "$OUT.phone.json" "$OUT" "$(basename "$IN")" <<'PY'
import hashlib, json, os, subprocess, sys
src, dst, out, base_in = sys.argv[1:5]
d = json.load(open(src, encoding="utf-8"))
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
d["shared_copy_of"] = base_in
d["tool"] = "sim_share.sh (sidecar copied from the input and marked)"
d["output"] = {"name": os.path.basename(out), "bytes": os.path.getsize(out), "sha256": h, "note": "a messenger-class copy (480p, about 1 Mbps); width and height are those of the copy"}
json.dump(d, open(dst, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
open(dst, "a").write("\n")
PY
  WROTE="$WROTE, $(basename "$OUT").phone.json"
fi
SZ=$(stat -c %s "$OUT")
echo "files written: $WROTE ($SZ bytes)"
exit 0
