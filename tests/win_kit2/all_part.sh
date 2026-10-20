# tests/win_kit2/all_part.sh: the --all-only half of run_tests.sh (sourced by it; uses its record, expect and check functions).
# The acceptance lines of the build plan for WP-09, then the real run of the PC runner on this container's ffmpeg.

# ------------------------------------------------------------------ Ken Burns: the plan's acceptance lines
rm -f "$RW"/ex02*.mp4 "$RW"/ex02*.mkv
expect kb.selftest_exit_0_and_prints_the_readback 0 -m 'RESULT: PASS' -m 'PASS disc_aspect' -m 'PASS frames +want 384' -m 'PASS r_frame_rate +want 24/1' -n 'FAIL' -s 'RESULT|disc_aspect|ok: 384' -- $PY $K/kenburns_24.py --selftest --out $RW/ex02.mp4
SELFTEST_OUT="$OUT"
check kb.selftest_wrote_the_four_files_and_no_temp_leftover $( [ -s $RW/ex02.mp4 ] && [ -s $RW/ex02_push_only.mkv ] && [ -s $RW/ex02_zoompan_proof.mp4 ] && [ -s $RW/ex02_push_only_zoompan.mkv ] && ! ls $RW/ex02*.part* >/dev/null 2>&1 && echo 0 || echo 1) "ex02.mp4, ex02_push_only.mkv, ex02_zoompan_proof.mp4, ex02_push_only_zoompan.mkv exist; no .part file"
expect kb.ffprobe_self_check_of_exercise_2 0 -m '^h264,1920,1080,24/1$' -- ffprobe -v error -show_entries "stream=width,height,r_frame_rate,codec_name" -of csv=p=0 -select_streams v:0 $RW/ex02.mp4
expect kb.spec_check_online_h264_exit_0 0 -m 'RESULT: PASS \(27 checks\)' -m 'PASS video\.size +want 1920x1080; got 1920x1080' -m 'PASS video\.fps +want r_frame_rate = avg_frame_rate = 24/1; got r=24/1 avg=24/1' -m 'PASS video\.pix_fmt +want yuv420p' -m 'PASS video\.color_range +want tv' -m 'PASS video\.color_space +want bt709' -m 'PASS video\.frame_count +want nb_frames = round\(duration x 24/1\) = 384' -- $PY pipeline/validators/spec_check.py $RW/ex02.mp4 --profile online_h264
expect kb.mo8_gate_passes_the_sub_pixel_push 0 -m 'RESULT: PASS' -m 'MO8a centre jitter +0\.0[0-4][0-9]* px +limit 0\.05 +PASS' -m 'MO8b edge jitter +0\.0[0-3][0-9]* px +limit 0\.04 +PASS' -m 'lossless-or-intermediate-clip \(ffv1\)' -s 'MO8|RESULT' -- $PY pipeline/validators/mo8_gate.py $RW/ex02_push_only.mkv
expect kb.mo8_gate_fails_the_zoompan_proof_as_documented 1 -m 'RESULT: FAIL' -m 'MO8a centre jitter .* FAIL' -m 'MO8b edge jitter .* FAIL' -s 'MO8|RESULT' -- $PY pipeline/validators/mo8_gate.py $RW/ex02_push_only_zoompan.mkv
PROOF="$(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames,duration -of csv=p=0 $RW/ex02_zoompan_proof.mp4 2>&1 | tr '\n' ' ')"
check kb.zoompan_proof_is_5_seconds_120_frames_not_125 $(printf '%s' "$PROOF" | grep -Eq '^5\.000000,120 ?$' && echo 0 || echo 1) "ffprobe: duration,frames = $PROOF (d=120 for 5 s at 24 fps)"
$PY - "$RW/ex02.mp4" > "$TMP/disc.out" 2>&1 <<'PYEOF'
# an independent reading of the circle (does not import kenburns_24.py): decode frame 1 and frame 60 and measure the yellow disc
import subprocess, sys
import numpy as np
def frame(path, n):
    vf = "trim=start_frame=%d:end_frame=%d,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24" % (n, n + 1)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(1080, 1920, 3).astype(np.float32)
out = []
for n in (1, 60):
    f = frame(sys.argv[1], n)
    d = f - np.array([250, 215, 40], np.float32)
    ys, xs = np.nonzero((d * d).sum(axis=2) < 70 * 70)
    out.append((n, xs.std() / ys.std(), (xs.max() - xs.min() + 1) / float(ys.max() - ys.min() + 1), len(xs)))
ok = all(abs(o[1] - 1) <= 0.01 and abs(o[2] - 1) <= 0.01 for o in out)
print("; ".join("frame %d: spread %.4f box %.4f area %d" % o for o in out))
print("CIRCLE " + ("OK" if ok else "BAD"))
PYEOF
check kb.circle_in_ex02_measures_1_00_pm_0_01_on_two_frames $(grep -q '^CIRCLE OK' "$TMP/disc.out" && echo 0 || echo 1) "independent measurement on the decoded ex02.mp4 (limit 1.00 +- 0.01)" "$(head -1 "$TMP/disc.out")"
$PY "$T/dissolve_check.py" "$RW/ex02.mp4" > "$TMP/dissolve.out" 2>&1
check kb.the_two_joins_are_one_second_dissolves_at_frames_120_and_240 $(grep -q '^DISSOLVES OK' "$TMP/dissolve.out" && echo 0 || echo 1) "the fitted dissolve weight of the decoded frames rises 0 to 1 in steps of 1/24 over output frames 120-143 and 240-263, and is 0 before and 1 after (residual about 1 grey level)" "$(grep -E 'j=12|j= 6' "$TMP/dissolve.out" | head -2 | tr '\n' '|')"
expect wrapper.kenburns_ps1_selftest_runs_the_python_tool_live 0 -m 'RESULT: PASS' -m 'files written: <project>/renders/wp09/ex02_ps\.mp4; ' -m '\[5/5\] Making the video' -n 'category=' -s 'RESULT|files written' -- $PWSH -NoProfile -File $K/kenburns_24.ps1 -Selftest -Out $RW/ex02_ps.mp4
rm -f "$RW"/ex02_ps*

# ------------------------------------------------------------------ the PC runner, real run on this container's ffmpeg
mkdir -p "$TMP/realtemp"
rm -f "$RW/cp_raw_real.json"
FROZEN="$K $T win/tools scripts/redaction_patterns.json pipeline/validators pipeline/lib research/sources/format-round1"
HF0="$(hash_tree $FROZEN)"
expect runner.real_run_passes_and_writes_the_raw_file 0 -m 'ok \(all checks passed\)' -m '8 of 8 within 3/255' -m 'PASTE THIS IN THE CHAT' -m 'files written: renders/wp09/cp_raw_real.json|files written: <project>/renders/wp09/cp_raw_real.json' -m '\[11/11\] Deleting the temporary folder' -n 'REFUSED|FAILED|category=' -s 'RESULT|files written|ok \(' -- env TEMP="$TMP/realtemp" TMPDIR="$TMP/realtemp" $PWSH -NoProfile -File $K/run_checks_pc.ps1 -Out "$RW/cp_raw_real.json"
check runner.real_run_deleted_its_temporary_folder $([ -z "$(ls -A "$TMP/realtemp")" ] && echo 0 || echo 1) "the lj_kit2_* folder under TEMP is gone; entries left: $(ls -A "$TMP/realtemp" | wc -l)"
check runner.raw_record_holds_flags_hash_and_the_8_chains_with_the_phone_ones $($PY -c "
import json,sys
d=json.load(open(sys.argv[1]))
names=[c['name'] for c in d['chains']]
ok = d['schema']=='lj-colour-patch/1' and d['ffmpeg']['configure'] and len(d['ffmpeg']['sha256'])==64 and 'phone_1080' in names and 'phone_720_share' in names and 'h264_online' in names and len(d['controls'])==6 and d['summary']['chains']==8
sys.exit(0 if ok else 1)" "$RW/cp_raw_real.json" && echo 0 || echo 1) "the raw file has the configure flags, the binary SHA-256, 8 chains (6 project, 2 phone) and 6 controls"
expect runner.real_run_derives_and_the_derived_file_passes_public_lint 0 -m 'wrote the derived record' -- bash -c "$PY pipeline/validators/colour_patch.py --derive-from $RW/cp_raw_real.json --out $RW/cp_derived_real.json && $PY scripts/public_lint.py --paths $RW/cp_derived_real.json"
check runner.derived_real_file_has_no_configure_flags_and_8_chains $($PY -c "
import json,sys
d=json.load(open(sys.argv[1])); t=open(sys.argv[1]).read()
sys.exit(0 if (len(d['chains'])==8 and 'configure' not in t and '--enable' not in t and set(d['ffmpeg'])=={'version','sha256'}) else 1)" "$RW/cp_derived_real.json" && echo 0 || echo 1) "8 chain rows, version and sha256 only, no flags"
check runner.real_run_changed_no_project_file $([ "$HF0" = "$(hash_tree $FROZEN)" ] && echo 0 || echo 1) "win/kit2, tests/win_kit2, win/tools, the pattern file, pipeline/validators, pipeline/lib and research/sources/format-round1 hash the same before and after the real run (it writes only the -Out file and its temporary folder)"
# the refusal in the REAL flow: a build that carries a profile path and the user's name in its configure line
$PY "$T/fixtures.py" fake-ffmpeg "$TMP/fakeff" --fake-user "$FAKE" > /dev/null
mkdir -p "$TMP/realtemp2"; rm -f "$RW/cp_raw_refused.json"
expect runner.real_flow_refuses_a_build_with_a_profile_path_and_the_users_name 2 -m 'REFUSED' -m 'REDACTION CHECK FAILED, nothing was written' -m 'category=profile_path_windows field=ffmpeg\.configure\[[0-9]+\] hit=C:\*+' -m 'category=user_name field=ffmpeg\.configure\[[0-9]+\] hit=zo\*+' -m 'skipped \(the scan refused\)' -m 'files written: none' -n "$FAKE" -n 'PASTE THIS IN THE CHAT' -n 'RESULT chains' -- env USERNAME="$FAKE" TEMP="$TMP/realtemp2" TMPDIR="$TMP/realtemp2" $PWSH -NoProfile -File $K/run_checks_pc.ps1 -Ffmpeg "$TMP/fakeff/ffmpeg" -Out "$RW/cp_raw_refused.json"
check runner.real_flow_refusal_wrote_nothing_and_deleted_the_temp_folder $([ ! -e "$RW/cp_raw_refused.json" ] && [ -z "$(ls -A "$TMP/realtemp2")" ] && echo 0 || echo 1) "no output file; temp entries left: $(ls -A "$TMP/realtemp2" | wc -l); neither the tool output nor the paste block was printed (checked by -n above)"
mkdir -p "$TMP/spacebin"; ln -sf "$(command -v ffmpeg)" "$TMP/spacebin/ffmpeg"; mkdir -p "$TMP/with space"; ln -sf "$(command -v ffmpeg)" "$TMP/with space/ffmpeg"; ln -sf "$(command -v ffprobe)" "$TMP/with space/ffprobe"
expect runner.real_run_with_ffmpeg_and_out_in_folders_with_spaces 0 -m '8 of 8 within 3/255' -m 'files written: ' -- env TEMP="$TMP/realtemp" $PWSH -NoProfile -File $K/run_checks_pc.ps1 -Ffmpeg "$TMP/with space/ffmpeg" -Out "$TMP/with space/out dir/colour raw.json"
check runner.the_file_in_the_folder_with_spaces_exists $([ -s "$TMP/with space/out dir/colour raw.json" ] && echo 0 || echo 1) "the raw file was written into a folder created from -Out"

# ------------------------------------------------------------------ one source for the patterns: the lint's own disagreement test, with this consumer present
expect hygiene.public_lint_self_test_includes_this_consumer_and_finds_no_disagreement 0 -m 'consumer win/kit2/run_checks_pc\.ps1: ok' -m 'self-test: no disagreement between consumers' -s 'consumer|self-test' -- $PY scripts/public_lint.py --self-test

# ------------------------------------------------------------------ housekeeping: the two large lossless windows go unless LJ_KEEP_RENDERS=1
if [ "${LJ_KEEP_RENDERS:-0}" != "1" ]; then rm -f "$RW"/ex02_push_only.mkv "$RW"/ex02_push_only_zoompan.mkv; fi
