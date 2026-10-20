#!/usr/bin/env python3
"""fixtures.py: synthetic test inputs for WP-09 (win/kit2). Every planted value is built from fragments here, at run time, and written
only to a git-ignored folder or the scratch folder: no file of the repository holds a flagged string. All names are invented.

  python3 -I tests/win_kit2/fixtures.py raw-clean OUT.json
  python3 -I tests/win_kit2/fixtures.py raw-planted KIND OUT.json --fake-user NAME        KIND: path | name_only | hex65 | ip | ip_doc | email
  python3 -I tests/win_kit2/fixtures.py fake-ffmpeg DIR --fake-user NAME [--kind path|name_only]   a wrapper that plants a flag in `ffmpeg -version`
  python3 -I tests/win_kit2/fixtures.py samples OUT.json                                  the samples file of the 4.13 consumer contract
  python3 -I tests/win_kit2/fixtures.py tamper FILE OFFSET                                flip one bit of one byte (running it twice restores the file)
"""
import argparse
import importlib.util
import json
import os
import stat
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BS = chr(92)


def clean_record():
    """A raw colour_patch record of the lj-colour-patch/1 shape, made by hand (not by an ffmpeg run) so it is fast and fixed."""
    def chain(name, we):
        return {"name": name, "kind": "chain", "worst_error": we, "worst_error_accurate": we, "pass": we <= 3, "error": None}
    return {
        "schema": "lj-colour-patch/1", "tool_version": 1, "date_utc": "2026-10-20",
        "platform": {"system": "Windows", "machine": "AMD64", "python": "3.13.15"},
        "ffmpeg": {"version_line": "ffmpeg version 9.0.2-essentials_build-www.gyan.dev Copyright (c) 2000-2025 the FFmpeg developers",
                   "version": "9.0.2-essentials_build-www.gyan.dev",
                   "configure": ["--enable-gpl", "--enable-version3", "--enable-static", "--disable-w32threads", "--disable-autodetect",
                                 "--enable-fontconfig", "--enable-iconv", "--enable-gnutls", "--enable-libxml2", "--enable-libx264"],
                   "sha256": "a" * 32 + "b" * 32},
        "tolerance": 3,
        "patches": [{"name": "red", "rgb": [255, 0, 0]}, {"name": "grey50", "rgb": [128, 128, 128]}, {"name": "skin", "rgb": [224, 172, 140]}],
        "decode": "scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24", "chain_file": "chains_all.json",
        "chains": [chain("h264_venue", 1), chain("h264_online", 1), chain("prores422hq_master", 2), chain("phone_1080", 1)],
        "controls": [chain("control_h264_scale_first_B", 1), chain("control_wrong_matrix_bt601", 25)],
        "read_back": "scale=1920:1080:flags=neighbor",
        "summary": {"chains": 4, "chains_failed": [], "chains_error": [], "approval_violations": [], "controls_misbehaved": [], "traps_present": []},
    }


def planted_record(kind, fake_user):
    r = clean_record()
    conf = r["ffmpeg"]["configure"]
    if kind == "path":
        conf.append("--prefix=C:" + BS + "Users" + BS + fake_user + BS + "ffbuild")
        conf.append("--extra-cflags=-I/home/" + fake_user + "/inc")
    elif kind == "name_only":
        conf.append("--extra-version=" + fake_user)
    elif kind == "hex65":
        r["ffmpeg"]["version_line"] += " build " + "c" * 65
    elif kind == "ip":
        conf.append("--extra-ldflags=-L" + "10." + "1.2" + ".3")
    elif kind == "ip_doc":
        conf.append("--extra-ldflags=-L" + "192." + "0.2" + ".1")          # a documentation address: allowed
    elif kind == "email":
        conf.append("--contact=" + "someone" + "@" + "mail-host-example" + "." + "org")
    else:
        raise SystemExit("unknown kind " + kind)
    return r


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def fake_ffmpeg(dest, fake_user, kind):
    """A sh wrapper named ffmpeg that runs the real ffmpeg but adds one planted build flag to the `configuration:` line of -version."""
    real = None
    for d in os.environ.get("PATH", "").split(os.pathsep):
        c = os.path.join(d, "ffmpeg")
        if os.path.isfile(c) and os.access(c, os.X_OK):
            real = c
            break
    if not real:
        raise SystemExit("no real ffmpeg on PATH")
    os.makedirs(dest, exist_ok=True)
    flag = ("--prefix=C:" + BS + "Users" + BS + fake_user + BS + "ffbuild") if kind == "path" else ("--extra-version=" + fake_user)
    path = os.path.join(dest, "ffmpeg")
    body = ("#!/bin/sh\n"
            'case "$*" in\n'
            "  *-version*) REAL \"$@\" | F='FLAG' awk '/^configuration:/ { print $0 \" \" ENVIRON[\"F\"]; next } { print }' ;;\n"
            "  *) exec REAL \"$@\" ;;\n"
            "esac\n").replace("REAL", real).replace("FLAG", flag)
    with open(path, "w", newline="\n") as f:
        f.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def samples(out):
    spec = importlib.util.spec_from_file_location("lj_public_lint", os.path.join(ROOT, "scripts", "public_lint.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pat = mod.load_patterns(os.path.join(ROOT, "scripts", "redaction_patterns.json"))
    texts, kinds, _expect = mod.samples_from(pat)
    write_json(out, {"samples": texts, "file_kind": kinds})
    return len(texts)


def tamper(path, offset):
    with open(path, "rb") as f:
        b = bytearray(f.read())
    b[offset] ^= 1
    with open(path, "wb") as f:
        f.write(b)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("raw-clean"); a.add_argument("out")
    b = sub.add_parser("raw-planted"); b.add_argument("kind"); b.add_argument("out"); b.add_argument("--fake-user", required=True)
    c = sub.add_parser("fake-ffmpeg"); c.add_argument("dest"); c.add_argument("--fake-user", required=True); c.add_argument("--kind", default="path")
    d = sub.add_parser("samples"); d.add_argument("out")
    t = sub.add_parser("tamper"); t.add_argument("file"); t.add_argument("offset", type=int)
    x = ap.parse_args(argv)
    if x.cmd == "raw-clean":
        write_json(x.out, clean_record())
    elif x.cmd == "raw-planted":
        write_json(x.out, planted_record(x.kind, x.fake_user))
    elif x.cmd == "fake-ffmpeg":
        print(fake_ffmpeg(x.dest, x.fake_user, x.kind))
    elif x.cmd == "samples":
        print("samples: %d" % samples(x.out))
    elif x.cmd == "tamper":
        tamper(x.file, x.offset)
    else:
        ap.print_usage()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
