#!/usr/bin/env python3
"""collect_results.py: build spikes/sp2_route_a/results.json from the WP-04 evidence (read only; writes results.json).

One row per SP2 item of research/agent-pipeline.md R11 (subset (a), (d), (e), (f), (g); (b) and (c) replaced as justified in the plan),
and the R11 pass rule evaluated on the measured numbers. python3 -I spikes/sp2_route_a/collect_results.py
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVID = os.path.join(REPO, "build", "evidence", "wp04")


def ev(name):
    try:
        with open(os.path.join(EVID, name + ".json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def status(e):
    return e["status"] if e else "NOT RUN"


def main():
    t = {n: ev(n) for n in ("a1_determinism", "a2_negative_control", "a3_shards_resume", "a4_kill_resume", "a5_chain_output", "a6_flat_fps", "a6_concurrency",
                            "a6_chapter_2400", "a6_chapter_2400_ram", "testcard_fps", "history_independence", "max_seconds_resume", "chain_parity", "a7_fonts", "a7_add_script", "a8_errors", "a9_path_safety", "a10_alpha", "webgl_smoke", "gsap_equivalence", "mo8_precheck", "a11_mo8_gate")}
    flat = t["a6_flat_fps"]["data"] if t["a6_flat_fps"] else {}
    conc = t["a6_concurrency"]["data"] if t["a6_concurrency"] else {}
    chap = t["a6_chapter_2400"]["data"] if t["a6_chapter_2400"] and t["a6_chapter_2400"]["status"] == "PASS" else ((t["a6_chapter_2400_ram"] or {}).get("data") or {})
    chap_variant = "guarded lj_with_disk stage" if t["a6_chapter_2400"] and t["a6_chapter_2400"]["status"] == "PASS" else "RAM-output fallback (the guarded stage was %s)" % status(t["a6_chapter_2400"])
    smoke = t["webgl_smoke"]["data"] if t["webgl_smoke"] else {}
    rows = [
        {"item": "(a) flat scene speed", "test": "a6_flat_fps", "status": status(t["a6_flat_fps"]), "pass_mark": ">= 8 fps", "measured_fps": flat.get("throughput_fps"), "peak_rss": flat.get("peak_rss")},
        {"item": "(b) rough.js + GSAP + baked grain", "test": "replaced", "status": "REPLACED",
         "note": "rough.js is a style choice for G1 and adds nothing to a harness test; the seeded-LCG texture with a float-precision push from a cosine ease (and its GSAP twin, gsap_equivalence) covers the determinism and MO8 questions",
         "gsap_equivalence": status(t["gsap_equivalence"]), "mo8_precheck": status(t["mo8_precheck"])},
        {"item": "(c) three.js voxel diorama", "test": "dropped (D-29); WebGL/SwiftShader smoke instead", "status": status(t["webgl_smoke"]), "pass_mark": "(was >= 2 fps for the diorama; the smoke has no pass mark, it records fps)", "measured_fps": smoke.get("throughput_fps"), "gl_renderer": smoke.get("renderer")},
        {"item": "(d) self-hosted OFL fonts per script", "test": "a7_fonts (+ a7_add_script)", "status": status(t["a7_fonts"]), "add_a_script": status(t["a7_add_script"]),
         "scripts_tested": (t["a7_fonts"] or {}).get("data", {}).get("scripts_tested"), "NOT_TESTED": (t["a7_fonts"] or {}).get("data", {}).get("NOT_TESTED")},
        {"item": "(e) 1, 2 and 4 concurrent pages", "test": "a6_concurrency", "status": status(t["a6_concurrency"]), "fps_by_pages": {k: v.get("throughput_fps") for k, v in conc.get("by_pages", {}).items()}, "best_pages": conc.get("best_pages")},
        {"item": "(f) 2,400-frame chapter piped to ffmpeg", "test": "a6_chapter_2400 (+ a6_chapter_2400_ram)", "status": status(t["a6_chapter_2400"]), "fallback_status": status(t["a6_chapter_2400_ram"]), "measured_by": chap_variant, "frames": chap.get("frames"), "seconds": chap.get("seconds_render"), "fps": chap.get("throughput_fps"),
         "peak_rss": chap.get("peak_rss"), "png_files_seen": chap.get("png_files_max_seen"), "output_bytes": chap.get("output_bytes")},
        {"item": "(g) kill at 50% and resume", "test": "a4_kill_resume", "status": status(t["a4_kill_resume"]), "detail": (t["a4_kill_resume"] or {}).get("actual")},
    ]
    r11 = {
        "rule": "Pass: (a) at least 8 fps, at most 100 differing pixels per frame between two runs, no OOM, resume works, tags correct. Fail: Route A moves to HyperFrames or Remotion (pinned) or to the maker's PC",
        "a_fps_ge_8": bool(flat.get("throughput_fps") and flat["throughput_fps"] >= 8),
        "determinism_le_100_px": status(t["a1_determinism"]) == "PASS", "negative_control_catches_nondeterminism": status(t["a2_negative_control"]) == "PASS",
        "no_oom": bool(chap.get("peak_rss")) and "PASS" in (status(t["a6_chapter_2400"]), status(t["a6_chapter_2400_ram"])), "resume_works": status(t["a4_kill_resume"]) == "PASS" and status(t["a3_shards_resume"]) == "PASS",
        "tags_correct": status(t["a5_chain_output"]) == "PASS",
    }
    r11["verdict"] = "PASS" if all(v for k, v in r11.items() if k not in ("rule", "verdict")) else "NOT PASSED (see the rows)"
    r11["open_item"] = "the guarded lj_with_disk 2,400-frame stage is %s; rerun `bash tests/render/run_tests.sh --all --only a6_chapter_2400` when Avail - planned >= 400 MB" % status(t["a6_chapter_2400"]) if status(t["a6_chapter_2400"]) != "PASS" else None
    out = {"schema": "lj-sp2-results/1", "sources": "build/evidence/wp04/*.json", "rows": rows, "r11": r11,
           "other_tests": {n: status(t[n]) for n in ("a3_shards_resume", "a5_chain_output", "a8_errors", "a9_path_safety", "a10_alpha", "gsap_equivalence", "mo8_precheck", "a11_mo8_gate", "history_independence", "max_seconds_resume", "chain_parity", "testcard_fps")}}
    with open(os.path.join(REPO, "spikes", "sp2_route_a", "results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for r in rows:
        print("%-44s %s" % (r["item"], r["status"]))
    print("R11: %s" % r11["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
