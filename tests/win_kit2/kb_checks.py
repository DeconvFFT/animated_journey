#!/usr/bin/env python3
"""kb_checks.py: in-process and command-line checks of win/kit2/kenburns_24.py and win/kit2/pc_helpers.py (WP-09).

  python3 -I -B tests/win_kit2/kb_checks.py --quick|--all [--work DIR]

Prints one line per check:  STATUS name | detail   (STATUS is PASS, FAIL, SKIPPED or UNVERIFIED). Exit 0 if no line is FAIL.
Needs ffmpeg, numpy and Pillow. Writes only under --work (default renders/wp09/kbwork, git-ignored; deleted at the end).
All pictures are synthetic (grey texture, a drawn disc, flat colour patches). No family media exists here.
"""
import argparse
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(ROOT, "win", "kit2")
PY = [sys.executable, "-I", "-B"]
RESULTS = []


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, KIT)
kb = load(os.path.join(KIT, "kenburns_24.py"), "kb_under_test")
ph = kb.pc_helpers


def report(status, name, detail=""):
    RESULTS.append((status, name))
    print("%s %s | %s" % (status, name, detail.replace("\n", " ")[:300]))
    sys.stdout.flush()


def check(name, ok, detail=""):
    report("PASS" if ok else "FAIL", name, detail)


def run(cmd, env=None, timeout=900):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=e, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def kbcli(args, env=None, timeout=900):
    return run(PY + [os.path.join(KIT, "kenburns_24.py")] + args, env, timeout)


# ------------------------------------------------------------------------------------------------------ geometry and arithmetic
def t_geometry():
    bad = []
    for size in ((3000, 2000), (4000, 3000), (1920, 1080), (2000, 3000), (6000, 1000), (3840, 2160)):
        for focus in ((0, 0), (0.5, 0.5), (1, 1), (0.2, 0.9)):
            x, y, w, h = kb.base_window(size[0], size[1], focus)
            if abs(w / h - 16.0 / 9.0) > 1e-12 or x < -1e-9 or y < -1e-9 or x + w > size[0] + 1e-9 or y + h > size[1] + 1e-9:
                bad.append((size, focus, (x, y, w, h)))
    check("kb.base_window_is_exactly_16x9_and_inside", not bad, "30 cases (6 sizes x 4 focus points); bad: %s" % bad[:2])


def t_moves():
    worst_aspect, outside, n_checked = 0.0, [], 0
    for name, mv in kb.MOVES.items():
        m = dict(mv)
        m["name"] = name
        for size in ((3000, 2000), (3840, 2160), (4000, 3000)):
            base = kb.base_window(size[0], size[1], (0.5, 0.5))
            for i in range(144):
                x0, y0, x1, y1 = kb.move_box(m, base, i, 144, clamp=False)
                worst_aspect = max(worst_aspect, abs((x1 - x0) / (y1 - y0) - 16.0 / 9.0))
                tol = 1e-9
                if x0 < base[0] - tol or y0 < base[1] - tol or x1 > base[0] + base[2] + tol or y1 > base[1] + base[3] + tol:
                    outside.append((name, size, i))
                n_checked += 1
    check("kb.every_window_is_16x9", worst_aspect < 1e-9, "%d windows over 4 moves x 3 still sizes; worst aspect error %.2e" % (n_checked, worst_aspect))
    check("kb.builtin_moves_never_need_the_clamp", not outside, "%d windows asked, %d outside their 16:9 window" % (n_checked, len(outside)))
    check("kb.ease_is_flat_at_both_ends", kb.ease(0) == 0 and abs(kb.ease(1) - 1) < 1e-12 and abs(kb.ease(0.5) - 0.5) < 1e-12, "ease(0)=0, ease(0.5)=0.5, ease(1)=1")
    base = kb.base_window(3000, 2000)
    m = dict(kb.MOVES["push"])
    m["name"] = "push"
    a = kb.move_box(m, base, 0, 144)
    b = kb.move_box(m, base, 143, 144)
    check("kb.push_goes_from_whole_window_to_1_15x", abs((a[2] - a[0]) - base[2]) < 1e-9 and abs(base[2] / (b[2] - b[0]) - 1.15) < 1e-9, "start width = base width, end zoom 1.15")


def t_frame_math():
    frames, fade = int(round(6 * kb.FPS)), int(round(1 * kb.FPS))
    total = 3 * frames - 2 * fade
    vf = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=colorspace=bt709"
    g = kb.build_graph(3, frames, fade, vf)
    check("kb.three_moves_of_6s_with_1s_dissolves_are_384_frames", total == 384 and total / 24.0 == 16.0, "3 x 144 - 2 x 24 = %d frames = %.1f s" % (total, total / 24.0))
    offs = [float(x) for x in re.findall(r"xfade=transition=fade:duration=[0-9.]+:offset=([0-9.]+)", g)]
    check("kb.xfade_offsets_are_5s_and_10s", offs == [5.0, 10.0], "offsets %s" % offs)
    check("kb.graph_shape", g.count("xfade=") == 2 and g.count("trim=") == 3 and g.startswith("[0:v]format=gbrp,split=3") and g.endswith("[vout]") and vf in g,
          "2 xfade, 3 trim, planar RGB before the chain vf, the chain vf last")
    durs = set(re.findall(r"duration=([0-9.]+)", g))
    check("kb.dissolve_is_one_second", durs == {"1.000000"}, "durations %s" % sorted(durs))
    stale = re.search(r"(?<![0-9.])25(?![0-9.])", g)
    check("kb.graph_has_no_25", stale is None, "no 25 anywhere in the filter graph")


def t_zoompan():
    zp5, d5 = kb.zoompan_filter(5, 0.15)
    zp6, d6 = kb.zoompan_filter(6, 0.15)
    bad = "d=12" + "5"
    check("kb.zoompan_d_is_seconds_times_24", d5 == 120 and d6 == 144 and "d=120:" in zp5 and "fps=24" in zp5 and bad not in zp5 + zp6, "5 s -> d=%d, 6 s -> d=%d, fps=24" % (d5, d6))


def t_resize_matches_reference():
    import numpy as np
    from PIL import Image
    ref = load(os.path.join(ROOT, "research", "cinematic-quality-fixtures", "zoompan_vs_subpixel_prints.py"), "ref_prints")
    ref.N = 8                                                    # the reference's frame count is a module constant
    src = kb.grey_texture(1920, 1080, 5, 40, 220)               # a 16:9 source, so the whole picture is the base window
    want = ref.pil_resize_box(src, 0.04)
    m = {"name": "push", "z0": 1.0, "z1": 1.04, "c0": (0.5, 0.5), "c1": (0.5, 0.5), "what": ""}
    base = kb.base_window(1920, 1080)
    lan = getattr(Image, "Resampling", Image).LANCZOS
    worst = 0
    for i in range(8):
        box = kb.clamp_box(kb.move_box(m, base, i, 8), src.size)
        got = np.asarray(src.resize((kb.W, kb.H), lan, box=box))
        worst = max(worst, int(np.abs(got.astype(np.int16) - want[i].astype(np.int16)).max()))
    check("kb.resize_is_pixel_identical_to_reference_pil_resize_box", worst == 0, "8 frames of a 4 percent push: worst pixel difference %d (reference: zoompan_vs_subpixel_prints.py, pil_resize_box, ported, not imported)" % worst)


# ------------------------------------------------------------------------------------------------------ stills
def t_loading(work):
    import numpy as np
    from PIL import Image
    p = os.path.join(work, "portrait.jpg")
    img = Image.new("RGB", (400, 300), (10, 120, 200))
    ex = Image.Exif()
    ex[0x0112] = 6                                               # "rotate 90 clockwise to view"
    img.save(p, "JPEG", exif=ex)
    got, notes = kb.load_still(p)
    check("kb.exif_orientation_makes_the_still_upright", got.size == (300, 400) and any("upright" in n for n in notes), "a 400x300 file with orientation 6 loads as %dx%d; notes %s" % (got.size[0], got.size[1], notes))
    # modes
    outs = []
    for mode, make in (("L", lambda: Image.new("L", (64, 36), 200)), ("RGBA", lambda: Image.new("RGBA", (64, 36), (1, 2, 3, 4))),
                       ("P", lambda: Image.new("P", (64, 36), 3)), ("I;16", lambda: Image.fromarray(np.full((36, 64), 65535, np.uint16)))):
        q = os.path.join(work, "mode_%s.png" % mode.replace(";", "_"))
        try:
            make().save(q)
            g, _n = kb.load_still(q)
            outs.append((mode, g.mode, g.size, g.getpixel((0, 0))))
        except Exception as e:                                   # noqa: BLE001
            outs.append((mode, "ERR", type(e).__name__, str(e)[:40]))
    ok = all(o[1] == "RGB" and o[2] == (64, 36) for o in outs) and outs[3][3] == (255, 255, 255)
    check("kb.loads_grey_alpha_palette_and_16bit", ok, "%s" % (outs,))
    q = os.path.join(work, "badicc.png")
    Image.new("RGB", (64, 36), (9, 9, 9)).save(q, icc_profile=b"not a profile")
    g, notes = kb.load_still(q)
    check("kb.unreadable_colour_profile_is_noted_not_fatal", g.size == (64, 36) and any("could not be read" in n for n in notes), "notes %s" % notes)
    open(os.path.join(work, "notimage.jpg"), "wb").write(b"this is text")
    try:
        kb.load_still(os.path.join(work, "notimage.jpg"))
        check("kb.a_text_file_is_refused", False, "no exception")
    except kb.Usage as e:
        check("kb.a_text_file_is_refused", "cannot open" in str(e), str(e)[:100])


def t_squash_control(work):
    """The negative control that gives the 1.00 reading its meaning: a 3:2 still squeezed to 16:9 (what zoompan did) measures about 1.18."""
    import numpy as np
    from PIL import Image
    img, _info = kb.synthetic_still(0)
    lan = getattr(Image, "Resampling", Image).LANCZOS
    squashed = np.asarray(img.resize((kb.W, kb.H), lan))
    base = kb.base_window(*img.size)
    cropped = np.asarray(img.resize((kb.W, kb.H), lan, box=(base[0], base[1], base[0] + base[2], base[1] + base[3])))
    ms, mc = kb.measure_disc(squashed), kb.measure_disc(cropped)
    check("kb.disc_measure_flags_a_squashed_picture", ms is not None and abs(ms[0] - 1.0) > 0.1, "stretching the whole 3:2 still to 16:9 reads %.3f (spread) - the reading is not blind" % (ms[0] if ms else float("nan")))
    check("kb.disc_measure_reads_1_00_on_the_cropped_picture", mc is not None and abs(mc[0] - 1.0) <= 0.01 and abs(mc[1] - 1.0) <= 0.01, "16:9 window cut first: %.4f (spread) %.4f (box)" % mc[:2])


# ------------------------------------------------------------------------------------------------------ the command line
def t_cli_refusals(work):
    stills = [p for p, _ in kb.make_synthetic_stills(work, 2)]
    open(os.path.join(work, "notimage.jpg"), "wb").write(b"this is text")
    cases = [
        ("no stills", [], 2, "at least two stills"),
        ("one still", [stills[0]], 2, "at least two stills"),
        ("missing file", [stills[0], os.path.join(work, "nope.png")], 2, "not found"),
        ("not an image", [stills[0], os.path.join(work, "notimage.jpg")], 2, "cannot open"),
        ("fade longer than half a move", stills + ["--seconds", "2", "--fade", "1.5"], 2, "--fade must be"),
        ("not whole frames", stills + ["--seconds", "6.01"], 2, "whole numbers of frames"),
        ("out is not mp4", stills + ["--out", os.path.join(work, "x.avi")], 2, ".mp4"),
        ("unknown move", stills + ["--moves", "spin"], 2, "unknown move"),
        ("bad focus", stills + ["--focus", "a,b"], 2, "--focus"),
        ("focus out of range", stills + ["--focus", "1.5,0.5"], 2, "between 0 and 1"),
        ("gate frames too few", stills + ["--gate-frames", "5"], 2, "--gate-frames"),
        ("selftest with stills", ["--selftest"] + stills, 2, "takes no stills"),
    ]
    bad = []
    for label, args, want, text in cases:
        out_arg = [] if "--out" in args else ["--out", os.path.join(work, "refusal.mp4")]
        rc, out = kbcli(args + out_arg)
        if rc != want or text not in out:
            bad.append("%s: exit %s, wanted %s, text %r" % (label, rc, want, text))
    check("kb.cli_refuses_bad_input_with_exit_2", not bad, "%d cases; %s" % (len(cases), bad[:2] or "all refused with their message"))
    rc, out = kbcli(stills + ["--out", os.path.join(work, "refusal.mp4")], env={"FFMPEG": os.path.join(work, "no-such-ffmpeg")})
    check("kb.missing_ffmpeg_is_exit_3_with_a_remedy", rc == 3 and "ffmpeg not found" in out and "PATH" in out, "exit %s: %s" % (rc, out.strip().splitlines()[-1][:120]))
    check("kb.nothing_written_on_refusal", not os.path.exists(os.path.join(work, "refusal.mp4")), "no output file after the refusals")


def t_cli_ffmpeg_dies(work):
    fake = os.path.join(work, "dies")
    os.makedirs(fake, exist_ok=True)
    with open(os.path.join(fake, "ffmpeg"), "w") as f:
        f.write("#!/bin/sh\necho 'fake ffmpeg: cannot do this' >&2\nexit 1\n")
    os.chmod(os.path.join(fake, "ffmpeg"), 0o755)
    shutil.copy(shutil.which("ffprobe"), os.path.join(fake, "ffprobe"))
    stills = [p for p, _ in kb.make_synthetic_stills(work, 2)]
    out = os.path.join(work, "dies_out", "x.mp4")
    tmpd = os.path.join(work, "tmpdies")
    os.makedirs(tmpd, exist_ok=True)
    rc, text = kbcli(stills + ["--out", out, "--seconds", "1", "--fade", "0.5"], env={"FFMPEG": os.path.join(fake, "ffmpeg"), "TMPDIR": tmpd, "TEMP": tmpd, "TMP": tmpd})
    left = os.listdir(os.path.dirname(out)) if os.path.isdir(os.path.dirname(out)) else []
    check("kb.ffmpeg_that_dies_gives_exit_3_and_no_partial_file", rc == 3 and "ffmpeg" in text and not left, "exit %s; files left in the output folder: %s" % (rc, left))
    check("kb.temp_folder_is_deleted_after_a_failure", os.listdir(tmpd) == [], "temp folder entries after failure: %s" % os.listdir(tmpd))
    check("kb.failure_text_has_no_absolute_path_of_the_work_folder", tmpd not in text and work not in text, "the scratch path is replaced by <work> or absent")


# ------------------------------------------------------------------------------------------------------ redaction by design (review r1)
FAKE_NAME = "zq_fake" + "person"                                  # an invented profile name, built from two pieces so no file holds it whole


def t_scrub_unit():
    """scrub(): the work, output, project and home folders are masked, longest first, in either slash style and any letter case."""
    saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
    home = "/home/" + FAKE_NAME
    os.environ["HOME"] = os.environ["USERPROFILE"] = home
    try:
        out_dir = home + "/lj/renders/ex02"
        wk = home + "/AppData/Local/Temp/lj_kb_abc123"
        text = "open %s/x.mp4.part.mp4 | log %s/ffmpeg_main.log | tool %s/win/kit2/kenburns_24.py | note %s/Documents/a.jpg" % (out_dir, wk, kb.REPO, home)
        want = "open <out>/x.mp4.part.mp4 | log <work>/ffmpeg_main.log | tool <project>/win/kit2/kenburns_24.py | note <home>/Documents/a.jpg"
        got = kb.scrub(text, wk, out_dir)
        check("redact.scrub_masks_work_out_project_and_home_longest_first", got == want, "got: %s" % got)
        win_out = "C:\\Users\\" + FAKE_NAME + "\\renders\\ex02"
        got2 = kb.scrub("Error opening output C:/Users/" + FAKE_NAME.upper() + "/renders/ex02/x.mp4.part.mp4", None, win_out)
        check("redact.scrub_matches_either_slash_style_and_any_letter_case", got2 == "Error opening output <out>/x.mp4.part.mp4", "got: %s" % got2)
        got3 = kb.scrub("a / b and C:\\x", None, "/") + " | " + kb.scrub("C:\\x", None, "C:\\")
        check("redact.scrub_skips_a_root_so_it_cannot_mangle_the_text", got3 == "a / b and C:\\x | C:\\x", "got: %s" % got3)
        got4 = ph.scrub_paths("see " + home + "/x and " + kb.REPO + "/y")
        check("redact.pc_helpers_scrub_paths_masks_home_and_project_without_extra_folders", got4 == "see <home>/x and <project>/y", "got: %s" % got4)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def t_catch_all_in_process(work):
    """An exception nobody planned for prints ONE line (its kind only) and returns 3: no traceback, no message text, no path."""
    import contextlib
    import io
    stills = [p for p, _ in kb.make_synthetic_stills(os.path.join(work, "ca_src"), 2)] if os.makedirs(os.path.join(work, "ca_src"), exist_ok=True) is None else []
    secret = "boom " + ROOT + " C:\\Users\\" + FAKE_NAME + "\\x.txt"
    line_kb = "kenburns_24: unexpected error (RuntimeError). Nothing of yours was changed; paste this one line in chat.\n"
    line_ph = "pc_helpers: unexpected error (ValueError). Nothing of yours was changed; paste this one line in chat.\n"
    saved_run_job, saved_make_clip = kb.run_job, ph.make_clip

    def boom_runtime(*_a, **_k):
        raise RuntimeError(secret)

    def boom_value(*_a, **_k):
        raise ValueError(secret)

    def boom_ctrl_c(*_a, **_k):
        raise KeyboardInterrupt()

    try:
        for label, fn, line, call in (
                ("kenburns_24", boom_runtime, line_kb, lambda: kb.main(stills + ["--out", os.path.join(work, "ca.mp4")])),
                ("pc_helpers", boom_value, line_ph, lambda: ph.main(["clip", "--out", os.path.join(work, "ca_clip.mp4")]))):
            if label == "kenburns_24":
                kb.run_job = fn
            else:
                ph.make_clip = fn
            err, outp = io.StringIO(), io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(outp):
                rc = call()
            text = err.getvalue()
            check("redact.%s_catch_all_prints_one_line_exit_3_and_no_message_text" % label,
                  rc == 3 and text == line and "boom" not in text + outp.getvalue() and "Traceback" not in text + outp.getvalue() and ROOT not in text + outp.getvalue() and FAKE_NAME not in text + outp.getvalue(),
                  "exit %s; stderr %r" % (rc, text))
        kb.run_job = boom_ctrl_c
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            rc = kb.main(stills + ["--out", os.path.join(work, "ca.mp4")])
        check("redact.ctrl_c_prints_one_line_and_no_traceback", rc == 3 and err.getvalue().startswith("kenburns_24: stopped by you") and "Traceback" not in err.getvalue(), "exit %s; stderr %r" % (rc, err.getvalue()))
    finally:
        kb.run_job, ph.make_clip = saved_run_job, saved_make_clip


def clean_text(text, *paths):
    """True when none of the given paths (nor the repo path, nor a traceback) shows in the text."""
    return "Traceback" not in text and ROOT not in text and all(p not in text for p in paths if p)


def t_redaction_cli(work, quick):
    src = os.path.join(work, "redact_src")
    os.makedirs(src, exist_ok=True)
    stills = [p for p, _ in kb.make_synthetic_stills(src, 2)]
    small = ["--seconds", "1", "--fade", "0.5"]
    # 1. --out below an existing FILE: the reviewer's traceback case
    afile = os.path.join(work, "a_file_not_a_folder.txt")
    with open(afile, "w") as f:
        f.write("mine\n")
    out = os.path.join(afile, "x.mp4")
    rc, text = kbcli(stills + ["--out", out] + small)
    check("redact.out_below_an_existing_file_is_exit_3_with_no_traceback_and_no_path",
          rc == 3 and "cannot create the output folder for x.mp4" in text and clean_text(text, afile, work) and open(afile).read() == "mine\n",
          "exit %s: %s" % (rc, text.strip().splitlines()[-1][:140]))
    # 2. a forced ffmpeg output-open failure: a FOLDER sits where the .part.mp4 file must go
    d = os.path.join(work, "openfail")
    os.makedirs(os.path.join(d, "x.mp4.part.mp4"), exist_ok=True)
    out = os.path.join(d, "x.mp4")
    rc, text = kbcli(stills + ["--out", out] + small)
    check("redact.ffmpeg_output_open_failure_is_exit_3_and_the_folder_is_masked",
          rc == 3 and "environment problem: ffmpeg" in text and "<out>" in text and clean_text(text, d, out) and sorted(os.listdir(d)) == ["x.mp4.part.mp4"],
          "exit %s; the error line says <out>, not the folder; folder after: %s" % (rc, sorted(os.listdir(d))))
    # 3. an unplanned exception through the real command line (--seconds inf overflows int(); a later fix may make it a refusal, which is fine too)
    rc, text = kbcli(stills + ["--out", os.path.join(work, "inf.mp4"), "--seconds", "inf"])
    check("redact.unplanned_exception_on_the_command_line_has_no_traceback",
          rc in (2, 3) and (rc == 2 or "kenburns_24: unexpected error (OverflowError). Nothing of yours was changed; paste this one line in chat." in text) and clean_text(text, work),
          "exit %s: %s" % (rc, text.strip().splitlines()[-1][:140]))
    # 4. pc_helpers on the command line: clip into a place that is a file, merge-chains into a folder that is not there
    rc, text = run(PY + [os.path.join(KIT, "pc_helpers.py"), "clip", "--out", os.path.join(afile, "c.mp4")])
    check("redact.pc_helpers_clip_output_failure_masks_the_folder", rc == 3 and "<out>" in text and clean_text(text, afile, work), "exit %s: %s" % (rc, text.strip().splitlines()[-1][:140]))
    gone = os.path.join(work, "no_such_folder", "m.json")
    rc, text = run(PY + [os.path.join(KIT, "pc_helpers.py"), "merge-chains", "--out", gone])
    check("redact.pc_helpers_merge_chains_into_a_missing_folder_is_exit_3_with_no_traceback", rc == 3 and "cannot write m.json" in text and clean_text(text, gone, work), "exit %s: %s" % (rc, text.strip().splitlines()[-1][:140]))
    if quick:
        return
    # 5. the zoompan proof has its own ffmpeg call: the same open failure there is masked too (the movie itself is made first)
    d2 = os.path.join(work, "openfail2")
    os.makedirs(os.path.join(d2, "x_zoompan_proof.mp4.part.mp4"), exist_ok=True)
    out2 = os.path.join(d2, "x.mp4")
    rc, text = kbcli(stills + ["--out", out2, "--proof-zoompan"] + small)
    check("redact.zoompan_proof_open_failure_is_exit_3_and_the_folder_is_masked", rc == 3 and "zoompan proof" in text and "<out>" in text and clean_text(text, d2, out2), "exit %s: %s" % (rc, text.strip().splitlines()[-1][:140]))



def probe_frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,pix_fmt,color_space", "-of", "json", path],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(r.stdout)["streams"][0]


def t_small_render(work, quick):
    """Two synthetic stills with distinctive file and folder names, a 1-second move each, 0.5-second dissolve: 36 frames."""
    import numpy as np
    d = os.path.join(work, "zzdir_secret")
    os.makedirs(d, exist_ok=True)
    made = kb.make_synthetic_stills(d, 2)
    named = []
    for k, (p, _i) in enumerate(made):
        q = os.path.join(d, "zz_marker_name_%d.png" % (k + 1))
        os.replace(p, q)
        named.append(q)
    out = os.path.join(work, "small", "small.mp4")
    tmpd = os.path.join(work, "tmpsmall")
    os.makedirs(tmpd, exist_ok=True)
    rc, text = kbcli(named + ["--out", out, "--seconds", "1", "--fade", "0.5", "--moves", "push,pull"], env={"TMPDIR": tmpd, "TEMP": tmpd, "TMP": tmpd})
    s = probe_frames(out) if os.path.isfile(out) else {}
    ok = rc == 0 and "RESULT: PASS" in text and s.get("nb_read_frames") == "36" and (s.get("width"), s.get("height")) == (1920, 1080) and s.get("r_frame_rate") == "24/1"
    check("kb.small_render_passes_its_own_readback", ok, "exit %s; frames %s; %sx%s; %s; 2 moves of 1 s, 0.5 s dissolve = 2x24-12 = 36" % (rc, s.get("nb_read_frames"), s.get("width"), s.get("height"), s.get("r_frame_rate")))
    check("kb.output_names_stills_by_number_not_by_file_name", "zz_marker" not in text and "zzdir_secret" not in text and "still 1:" in text, "neither the file names nor the folder name appear in the output")
    check("kb.temp_folder_is_deleted_after_success", os.listdir(tmpd) == [], "temp folder entries after success: %s" % os.listdir(tmpd))
    check("kb.only_the_output_file_is_left", sorted(os.listdir(os.path.dirname(out))) == ["small.mp4"], "folder: %s" % sorted(os.listdir(os.path.dirname(out))))
    # the disc and the patches, measured independently on the decoded output
    frame = kb.decode_frame_rgb(shutil.which("ffmpeg"), out, 1)
    m = kb.measure_disc(frame)
    check("kb.circle_in_the_output_is_round_1_00", m is not None and abs(m[0] - 1.0) <= 0.01 and abs(m[1] - 1.0) <= 0.01, "spread ratio %.4f, bounding-box ratio %.4f (limit 1.00 +- 0.01)" % m[:2] if m else "disc not found")
    info = made[0][1]
    mv = dict(kb.MOVES["push"])
    mv["name"] = "push"
    base = kb.base_window(*info["size"])
    box = kb.move_box(mv, base, 1, 24)
    worst = max(w for *_x, w in kb.measure_patches(frame, info["patches"], box))
    check("kb.flat_colours_come_out_within_3_of_255", worst <= 3.0, "red, grey and skin patches read back within %.1f/255 of the source (W-16 limit 3)" % worst)
    if quick:
        return
    # a second run replaces the file and leaves no .part
    rc2, _t2 = kbcli(named + ["--out", out, "--seconds", "1", "--fade", "0.5", "--moves", "push,pull"])
    check("kb.second_run_replaces_the_output_and_leaves_no_part_file", rc2 == 0 and sorted(os.listdir(os.path.dirname(out))) == ["small.mp4"], "folder after the second run: %s" % sorted(os.listdir(os.path.dirname(out))))
    # a 12-frame lossless window for the gate (the gate's minimum)
    out2 = os.path.join(work, "small", "gate.mp4")
    rc3, t3 = kbcli(named + ["--out", out2, "--seconds", "1", "--fade", "0.5", "--moves", "push,pull", "--gate-window", "--gate-frames", "12"])
    mkv = os.path.join(work, "small", "gate_push_only.mkv")
    s3 = probe_frames(mkv) if os.path.isfile(mkv) else {}
    check("kb.gate_window_has_the_requested_12_frames", rc3 == 0 and s3.get("nb_read_frames") == "12", "exit %s; window frames %s" % (rc3, s3.get("nb_read_frames")))
    rc4, t4 = run(PY + [os.path.join(ROOT, "pipeline", "validators", "mo8_gate.py"), mkv])
    check("kb.gate_accepts_the_12_frame_window", rc4 == 0 and "RESULT: PASS" in t4, "mo8_gate exit %s: %s" % (rc4, [ln.strip() for ln in t4.splitlines() if "MO8" in ln][:2]))


def t_silent_vs_online(work):
    """A silent file fails the full online profile on audio.present only, and passes the video-only profile."""
    stills = [p for p, _ in kb.make_synthetic_stills(os.path.join(work, "silent_src"), 2)] if os.makedirs(os.path.join(work, "silent_src"), exist_ok=True) is None else []
    out = os.path.join(work, "silent", "silent.mp4")
    rc, text = kbcli(stills + ["--out", out, "--seconds", "1", "--fade", "0.5"])
    spec = os.path.join(ROOT, "pipeline", "validators", "spec_check.py")
    rc1, t1 = run(PY + [spec, out, "--profile", "online_h264"])
    failed = re.findall(r"^\s*FAIL (\S+)", t1, re.M)
    rc2, t2 = run(PY + [spec, out, "--profile", "online_h264_video_only", "--profiles-file", os.path.join(KIT, "profiles_kit2.json")])
    check("kb.silent_file_fails_online_h264_on_audio_only", rc == 0 and rc1 == 1 and sorted(failed) == ["audio.present"], "exit %s, failed checks %s" % (rc1, failed))
    check("kb.silent_file_passes_the_video_only_profile", rc2 == 0 and "RESULT: PASS" in t2, "exit %s; %s" % (rc2, t2.strip().splitlines()[-1]))
    with_tone = os.path.join(work, "silent", "tone.mp4")
    rc3, _t3 = kbcli(stills + ["--out", with_tone, "--seconds", "1", "--fade", "0.5", "--test-tone"])
    rc4, t4 = run(PY + [spec, with_tone, "--profile", "online_h264"])
    check("kb.test_tone_file_passes_the_full_online_profile", rc3 == 0 and rc4 == 0, "exit %s: %s" % (rc4, t4.strip().splitlines()[-1]))


def t_profile_matches_settings():
    settings = json.load(open(os.path.join(ROOT, "pipeline", "settings.json")))["profiles"]["online_h264"]
    mine = json.load(open(os.path.join(KIT, "profiles_kit2.json")))["profiles"]["online_h264_video_only"]
    same = all(mine.get(k) == settings.get(k) for k in ("video", "container", "faststart", "chain", "metadata", "decision"))
    check("kb.video_only_profile_has_the_same_video_block_as_online_h264", same and mine["audio"] == {"required": False} and "loudness" not in mine, "video, container, faststart, chain, metadata and decision are identical to pipeline/settings.json online_h264")


def t_user_site(work):
    """`python -I` ignores the pip --user folder; the tool adds it back at the end of the path. Simulated with -S (no site-packages at all)
    and a fake HOME whose user-site folder holds symlinks to the real Pillow and numpy."""
    import PIL
    real_sp = os.path.dirname(PIL.__path__[0])
    home = os.path.join(work, "fakehome")
    env = {"HOME": home, "USERPROFILE": home, "APPDATA": home}
    rc0, out0 = run([sys.executable, "-I", "-S", "-B", "-c", "import site; print(site.getusersitepackages())"], env)
    user_sp = out0.strip().splitlines()[-1]
    inside = user_sp.startswith(home)
    check("kb.the_fake_user_site_is_inside_the_fake_home", inside, "the user-site folder resolves under the fake HOME" if inside else "user site is %s" % user_sp[-60:])
    if not inside:
        return
    rc1, out1 = run([sys.executable, "-I", "-S", "-B", os.path.join(KIT, "kenburns_24.py"), "--check-libs"], env)
    check("kb.without_a_user_site_install_check_libs_says_how_to_install", rc1 == 3 and "py -3 -m pip install --user pillow numpy" in out1, "exit %s: %s" % (rc1, out1.strip().splitlines()[-1][:140]))
    os.makedirs(user_sp, exist_ok=True)
    for name in os.listdir(real_sp):
        if name.lower().startswith(("pil", "pillow", "numpy")):
            os.symlink(os.path.join(real_sp, name), os.path.join(user_sp, name))
    rc2, out2 = run([sys.executable, "-I", "-S", "-B", os.path.join(KIT, "kenburns_24.py"), "--check-libs"], env)
    check("kb.packages_installed_with_pip_user_are_found_under_dash_I", rc2 == 0 and out2.startswith("ok: Pillow"), "exit %s: %s (python -I hides the user folder; the tool adds it back at the end of the search path)" % (rc2, out2.strip().splitlines()[-1][:100]))
    rc3, out3 = run([sys.executable, "-I", "-S", "-B", "-c", "import PIL"], env)
    check("kb.control_python_dash_I_alone_cannot_see_them", rc3 != 0, "a plain import of PIL under -I -S fails (exit %s): the hiding is real, so the line above proves the fallback" % rc3)


# ------------------------------------------------------------------------------------------------------ helpers
def t_helpers(work):
    clip = os.path.join(work, "clip.mp4")
    rc, out = run(PY + [os.path.join(KIT, "pc_helpers.py"), "clip", "--out", clip])
    spec = os.path.join(ROOT, "pipeline", "validators", "spec_check.py")
    rc2, t2 = run(PY + [spec, clip, "--profile", "online_h264"])
    check("helpers.clip_passes_online_h264_with_the_tone_at_16_lufs", rc == 0 and rc2 == 0, "pc_helpers clip exit %s, spec_check exit %s: %s" % (rc, rc2, [ln.strip() for ln in t2.splitlines() if "integrated" in ln][:1]))
    rc3, out3 = run(PY + [os.path.join(KIT, "pc_helpers.py"), "clip", "--out", os.path.join(work, "c2.mp4")], env={"FFMPEG": os.path.join(work, "no-ffmpeg")})
    check("helpers.clip_without_ffmpeg_is_exit_3", rc3 == 3 and "ffmpeg not found" in out3, out3.strip()[-100:])
    merged = os.path.join(work, "merged.json")
    rc4, out4 = run(PY + [os.path.join(KIT, "pc_helpers.py"), "merge-chains", "--out", merged, "--extra", os.path.join(ROOT, "pipeline", "phone", "profile.json")])
    d = json.load(open(merged)) if os.path.isfile(merged) else {"chains": {}}
    have = sorted(d["chains"])
    check("helpers.merge_chains_joins_project_and_phone_chains", rc4 == 0 and "phone_1080" in have and "phone_720_share" in have and "h264_online" in have, "chains: %s" % have)
    rc5, out5 = run(PY + [os.path.join(KIT, "pc_helpers.py"), "merge-chains", "--out", merged, "--extra", os.path.join(work, "missing.json")])
    d5 = json.load(open(merged))
    check("helpers.merge_chains_skips_a_missing_phone_file_with_a_note", rc5 == 0 and "was not found" in out5 and "phone_1080" not in d5["chains"], out5.strip().splitlines()[0][:120])
    rc6, out6 = run(PY + [os.path.join(KIT, "pc_helpers.py"), "merge-chains", "--out", merged, "--extra", os.path.join(ROOT, "pipeline", "lib", "chains.json")])
    check("helpers.merge_chains_refuses_a_clash", rc6 == 2 and "both chain files" in out6, out6.strip()[-100:])


def main(argv=None):
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--all", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("BLOCKED kb_checks | ffmpeg or ffprobe not found")
        return 3
    work = a.work or os.path.join(ROOT, "renders", "wp09", "kbwork")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    try:
        t_geometry()
        t_moves()
        t_frame_math()
        t_zoompan()
        t_resize_matches_reference()
        t_profile_matches_settings()
        t_loading(work)
        t_squash_control(work)
        t_cli_refusals(work)
        t_cli_ffmpeg_dies(work)
        t_scrub_unit()
        t_catch_all_in_process(work)
        t_redaction_cli(work, quick=a.quick)
        t_helpers(work)
        t_user_site(work)
        t_small_render(work, quick=a.quick)
        if a.all:
            t_silent_vs_online(work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if any(s == "FAIL" for s, _ in RESULTS) else 0


if __name__ == "__main__":
    sys.exit(main())
