#!/usr/bin/env python3
"""fetch_sums.py: fetch every pin's SHA256SUMS.txt (a few KB each) and write release_assets.json.

USAGE  python3 -I spikes/sp1_craft_cli/drivers/fetch_sums.py [--out FILE] [--sums-dir DIR] [--blocked-proof FILE] [--no-head]
WHAT IT DOES
  For the six pins in config.json (PhotoCraft 0.10.0, VectorCraft 0.13.1, LightCraft 0.9.1, FilmCraft 0.9.0 and its fallback 0.8.0,
  EffectCraft 0.11.1) it downloads <base>/<app>/releases/download/<tag>/SHA256SUMS.txt (the release page and the REST API answer 403
  from this container, F-04), keeps the file verbatim under build/evidence/wp07/sums/, and records per pin: the Linux x86_64 tarball and
  the Windows x64 portable zip (name, SHA-256, size from a HEAD request), plus the MSI name so the maker can recognise the file not to use.
  It then compares the listing with the independent values of r8_hashes.json (research/craft-motion.md, read 2026-10-18).
  SoundCraft is recorded as "not pinned, not fetched". Nothing but those six text files and 12 HEAD requests is downloaded.
EXIT CODES  0 written and all comparisons match; 1 an R8 value or a size disagrees (STOP AND REPORT: nothing may be built on the table);
            2 bad usage or an unreadable sums file; 3 a download was blocked (blocked_proof.json written).
WHAT IT NEVER TOUCHES  anything outside the output files; it runs no downloaded file and sends nothing but GET and HEAD requests.
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # python3 -I ignores PYTHONDONTWRITEBYTECODE
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sp1_lib as L  # noqa: E402

KINDS = (
    ("linux_x86_64_tarball", "{app}-{ver}-linux-x86_64.tar.gz"),
    ("windows_x64_portable_zip", "{app}-{ver}-windows-x64-portable.zip"),
    ("windows_x64_msi", "{app}-{ver}-windows-x64.msi"),
)
INTEGRITY_NOTE = ("These hashes prove integrity only, not origin. Every hash in this file comes from the SHA256SUMS.txt that GitHub serves next to the asset, "
                  "so a file that matches is complete and unaltered since publication, but the listing and the file share one host and a match does not show who "
                  "published it. Only the values marked r8_compared were also read independently on 2026-10-18.")


def parse_sums(text):
    rows = {}
    for ln in text.splitlines():
        m = re.fullmatch(r"([0-9a-f]{64}) [ *](\S+)", ln.rstrip())
        if m:
            rows[m.group(2)] = m.group(1)
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=L.ASSETS_FILE)
    ap.add_argument("--sums-dir", default=os.path.join(L.EVID, "sums"))
    ap.add_argument("--blocked-proof", default=os.path.join(L.EVID, "blocked_proof.json"))
    ap.add_argument("--no-head", action="store_true", help="skip the HEAD requests (sizes stay null)")
    ap.add_argument("--config", default=os.path.join(L.SP1, "config.json"))
    ap.add_argument("--r8", default=os.environ.get("LJ_SP1_R8") or os.path.join(L.SP1, "r8_hashes.json"))
    a = ap.parse_args(argv)

    cfg = L.read_json(a.config)
    r8 = L.read_json(a.r8)
    os.makedirs(a.sums_dir, exist_ok=True)
    pins = []
    for pin in cfg["pins"]:
        app, tag = pin["app"], pin["tag"]
        ver = tag.lstrip("v")
        url = L.asset_url(app, tag, "SHA256SUMS.txt")
        dest = os.path.join(a.sums_dir, "%s-%s-SHA256SUMS.txt" % (app, tag))
        print("[fetch] %s %s SHA256SUMS.txt" % (app, tag))
        res = L.curl_get(url, dest, max_time=120)
        if res["curl_exit"] != 0 or res["status"] != 200:
            if os.path.exists(dest):
                os.remove(dest)
            L.write_blocked_proof(a.blocked_proof, url, res["status"], res["curl_exit"], res["stderr"],
                                  status_lines=L.curl_head(url, 30)["status_lines"], context={"step": "sums", "app": app, "tag": tag})
            print("BLOCKED: %s %s: HTTP %s, curl exit %s. blocked_proof.json written. Fallback: spikes/sp1_craft_cli/FALLBACK.md"
                  % (app, tag, res["status"], res["curl_exit"]))
            return 3
        text = open(dest, "r", encoding="utf-8", errors="replace").read()
        rows = parse_sums(text)
        if not rows:
            print("ERROR: %s %s: no 'hash  name' lines found in SHA256SUMS.txt" % (app, tag))
            return 2
        entry = {"app": app, "tag": tag, "version": ver, "role": pin["role"], "tarball_fetched_by": pin["tarball_fetched_by"],
                 "sums_file": os.path.relpath(dest, L.REPO) if dest.startswith(L.REPO) else "<outside>",
                 "sums_file_sha256": L.sha256_file(dest), "sums_file_bytes": os.path.getsize(dest), "assets_listed": len(rows)}
        for kind, pattern in KINDS:
            name = pattern.format(app=app, ver=ver)
            h = rows.get(name)
            rec = {"name": name, "sha256": h, "bytes": None}
            if h is None:
                rec["missing_from_listing"] = True
            elif not a.no_head:
                hd = L.curl_head(L.asset_url(app, tag, name), 60)
                if hd["curl_exit"] != 0 or hd["status"] != 200:
                    L.write_blocked_proof(a.blocked_proof, L.asset_url(app, tag, name), hd["status"], hd["curl_exit"], hd["stderr"],
                                          status_lines=hd["status_lines"], context={"step": "head", "app": app, "tag": tag, "asset": name})
                    print("BLOCKED: HEAD %s: HTTP %s, curl exit %s" % (name, hd["status"], hd["curl_exit"]))
                    return 3
                rec["bytes"] = hd["content_length"]
            entry[kind] = rec
        pins.append(entry)

    # comparisons: the independent values and the planned sizes
    rows_cmp = []
    mismatch = False
    for ex in r8["expected"]:
        pin = next((p for p in pins if p["app"] == ex["app"] and p["tag"] == ex["tag"]), None)
        got = pin[ex["kind"]]["sha256"] if pin else None
        st = "match" if got == ex["sha256"] else "MISMATCH"
        mismatch = mismatch or st != "match"
        rows_cmp.append({"app": ex["app"], "tag": ex["tag"], "kind": ex["kind"], "independent_sha256": ex["sha256"], "listing_sha256": got, "status": st, "where": ex["where"]})
        if pin and st == "match":
            pin[ex["kind"]]["r8_compared"] = True
    size_rows = []
    for key, want in r8["expected_linux_tarball_bytes"].items():
        app, tag = key.split()
        pin = next((p for p in pins if p["app"] == app and p["tag"] == tag), None)
        got = pin["linux_x86_64_tarball"]["bytes"] if pin else None
        st = "skipped (no HEAD)" if got is None else ("match" if got == want else "DIFFERENT")
        mismatch = mismatch or st == "DIFFERENT"
        size_rows.append({"pin": key, "planned_bytes": want, "head_bytes": got, "status": st})

    doc = {
        "schema": "lj-release-assets/1",
        "fetched_date_utc": L.today(),
        "fetched_by": "WP-07 spikes/sp1_craft_cli/drivers/fetch_sums.py",
        "source_pattern": "https://github.com/storytold/<app>/releases/download/<tag>/<asset>",
        "integrity_note": INTEGRITY_NOTE,
        "usable": not mismatch,
        "r8_comparison": {"status": "MISMATCH" if any(r["status"] != "match" for r in rows_cmp) else "all match", "rows": rows_cmp,
                          "not_compared": r8["no_independent_value"], "not_compared_note": r8["no_independent_value_note"]},
        "size_comparison": {"status": "DIFFERENT" if any(r["status"] == "DIFFERENT" for r in size_rows) else "all match", "rows": size_rows},
        "pins": pins,
        "soundcraft": cfg["soundcraft"],
        "disk_note": "No tarball is downloaded by this tool. FilmCraft 0.9.0 and EffectCraft 0.11.1 are fetched once each by run_sp1.sh; the other three by WP-10.",
    }
    L.write_json(a.out, doc)
    print("wrote %s (%d pins, R8 comparison: %s, sizes: %s)" % (L.rel(a.out), len(pins), doc["r8_comparison"]["status"], doc["size_comparison"]["status"]))
    if mismatch:
        print("STOP AND REPORT: a hash or a size differs from the independent value. release_assets.json says usable=false. Do not build on this table.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
