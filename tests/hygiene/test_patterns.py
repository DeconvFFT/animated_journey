#!/usr/bin/env python3
"""test_patterns.py: is scripts/redaction_patterns.json (build plan 4.13) internally consistent?

WHAT IT CHECKS (each check prints PASS or FAIL with the reason; nothing else is touched)
  1. the file parses, has schema/version/dialect and every required category id
  2. every regex compiles in Python, uses only the common Python/.NET subset (no named groups,
     no possessive quantifiers, no atomic groups, no inline flags, no \\d \\w \\s style escapes,
     fixed-width lookbehind) and finishes quickly on hostile input
  3. every category has at least one positive and one negative sample, and they behave
  4. every sample the plan requires is present (and behaves)
  5. the file contains none of the strings it forbids (raw text scan, and no flagged sample
     appears joined in the raw text)
  6. exemptions, field exemptions, name checks, mask, placeholders, path denylist, local deny
     are present as 4.13 says

HOW TO RUN   python3 -I tests/hygiene/test_patterns.py [--no-marker] [--json OUT]
EXIT         0 all checks pass; 1 at least one check failed; 2 the file cannot be read
SIDE EFFECT  when every check passes it writes build/evidence/wp03/LANDED-4.13.txt (one line, the
             marker WP-01a and the orchestrator look for) unless --no-marker is given.
NEVER        reads anything outside the repository, touches the network, or prints a flagged value.
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = ROOT / "scripts" / "redaction_patterns.json"
MARKER = ROOT / "build" / "evidence" / "wp03" / "LANDED-4.13.txt"

REQUIRED_IDS = ["email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux",
                "token_shape", "guid_serial", "handle"]
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" :: " + detail) if detail and not ok else ""))
    return ok


def join(x):
    return "".join(x) if isinstance(x, list) else str(x)


# ----------------------------------------------------------------------------- dialect scan
def dialect_problems(rx):
    """Return a list of dialect violations in one regex source string."""
    probs = []
    i, n = 0, len(rx)
    in_class = False
    prev_quant = False
    while i < n:
        ch = rx[i]
        if ch == "\\":
            nxt = rx[i + 1] if i + 1 < n else ""
            if nxt.isalnum() and nxt != "b":
                probs.append("escape \\%s at %d (only \\b and backslash-punctuation are in the dialect)" % (nxt, i))
            if in_class and nxt == "b":
                probs.append("\\b inside a class means backspace in Python and is different in .NET")
            i += 2
            prev_quant = False
            continue
        if in_class:
            if ch == "]":
                in_class = False
            elif ch == "[":
                probs.append("unescaped [ inside a class at %d" % i)
            i += 1
            prev_quant = False
            continue
        if ch == "[":
            in_class = True
            i += 1
            if i < n and rx[i] == "^":
                i += 1
            if i < n and rx[i] == "]":
                probs.append("a class that starts with ] at %d" % i)
            prev_quant = False
            continue
        if ch == "(":
            if rx.startswith("(?", i):
                rest = rx[i + 2:i + 4]
                head = rx[i:i + 3]
                if head in ("(?:", "(?=", "(?!"):
                    pass
                elif rx.startswith("(?<=", i) or rx.startswith("(?<!", i):
                    pass
                elif head == "(?>":
                    probs.append("atomic group at %d" % i)
                elif head in ("(?P", "(?<") or re.match(r"\(\?<[A-Za-z_]", rx[i:i + 5]) or re.match(r"\(\?'", rx[i:i + 3]):
                    probs.append("named group at %d" % i)
                elif re.match(r"\(\?[a-zA-Z-]+[:)]", rx[i:i + 12]):
                    probs.append("inline flags at %d" % i)
                elif head == "(?#":
                    probs.append("comment group at %d" % i)
                elif head == "(?(":
                    probs.append("conditional group at %d" % i)
                else:
                    probs.append("unknown group construct at %d" % i)
            else:
                probs.append("capturing group at %d (use (?: ) )" % i)
            i += 1
            prev_quant = False
            continue
        if ch in "*+?":
            if prev_quant and ch == "+":
                probs.append("possessive quantifier at %d" % i)
            # a lazy ? after a quantifier is fine; a quantifier after a quantifier otherwise is an error
            was_quant = prev_quant
            prev_quant = (ch in "*+?") and not (ch == "?" and was_quant)
            i += 1
            continue
        if ch == "{":
            m = re.match(r"\{[0-9]+(?:,[0-9]*)?\}", rx[i:])
            if not m:
                probs.append("literal or malformed { at %d" % i)
                i += 1
            else:
                i += m.end()
                if i < n and rx[i] == "+":
                    probs.append("possessive quantifier after {m,n} at %d" % i)
                prev_quant = True
            continue
        prev_quant = False
        i += 1
    if in_class:
        probs.append("unterminated class")
    return probs


# ----------------------------------------------------------------------------- engine (mirrors 4.13 consumers)
class Engine:
    def __init__(self, data):
        self.d = data
        self.cats = []
        for c in data["categories"]:
            self.cats.append((c["id"], re.compile(c["regex"], re.I if "i" in c.get("flags", "") else 0), c.get("scope", "both")))
        self.ex = [(e.get("category"), re.compile(e["regex"], re.I if "i" in e.get("flags", "") else 0)) for e in data.get("exemptions", [])]
        self.ph = set(data.get("placeholders", []))

    def hits(self, text, scope=None):
        out = []
        for cid, rx, sc in self.cats:
            if scope and sc not in (scope, "both"):
                continue
            for m in rx.finditer(text):
                if m.group(0) in self.ph:
                    continue
                exempt = False
                for ecat, erx in self.ex:
                    if ecat != cid:
                        continue
                    for em in erx.finditer(text):
                        if em.start() <= m.start() and m.end() <= em.end():
                            exempt = True
                            break
                    if exempt:
                        break
                if not exempt and cid not in out:
                    out.append(cid)
        return out


def main(argv):
    marker = "--no-marker" not in argv
    json_out = None
    if "--json" in argv:
        json_out = argv[argv.index("--json") + 1]
    try:
        raw = PATTERNS.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, ValueError) as e:
        print("FAIL  pattern file unreadable or not JSON (%s)" % type(e).__name__)
        return 2

    # 1. structure
    check("file has schema, version, dialect", data.get("schema") == "lj-redaction-patterns/1" and data.get("version") == 1 and data.get("dialect"))
    ids = [c.get("id") for c in data.get("categories", [])]
    check("every required category id is present", all(i in ids for i in REQUIRED_IDS), "missing: %s" % [i for i in REQUIRED_IDS if i not in ids])
    check("category ids are unique", len(ids) == len(set(ids)))
    shape_ok = True
    for c in data["categories"]:
        for k in ("id", "scope", "action", "regex", "flags", "description", "positive_samples", "negative_samples"):
            if k not in c:
                shape_ok = False
        if c.get("scope") not in ("report", "text", "both") or c.get("action") != "refuse" or c.get("flags") not in ("", "i"):
            shape_ok = False
    check("every category has id, scope, action=refuse, regex, flags ('' or 'i'), description and samples", shape_ok)
    handle = [c for c in data["categories"] if c["id"] == "handle"]
    check("handle is text-scope (never applied to a PC report)", handle and handle[0]["scope"] == "text")
    check("all other required categories apply to reports as well as text",
          all(c["scope"] == "both" for c in data["categories"] if c["id"] in REQUIRED_IDS and c["id"] != "handle"))

    # 2. regex: compile, dialect, speed
    compile_ok, dialect_ok, speed_ok = True, True, True
    bad = []
    hostile = ["A1" * 20000, "0123456789abcdef" * 4000, "1.2.3." * 8000, "a:" * 20000, "@" * 20000, "/home/" * 8000,
               "C:\\Users\\" * 4000, "-" * 40000, "x@" * 10000 + "." * 10000, "AAAA1" * 8000, "http://" + "a" * 40000]
    for obj in list(data["categories"]) + list(data.get("exemptions", [])):
        rx = obj["regex"]
        try:
            comp = re.compile(rx, re.I if "i" in obj.get("flags", "") else 0)
        except re.error as e:
            compile_ok = False
            bad.append("%s: %s" % (obj.get("id"), e))
            continue
        for p in dialect_problems(rx):
            dialect_ok = False
            bad.append("%s: %s" % (obj.get("id"), p))
        t0 = time.time()
        for h in hostile:
            comp.search(h)
            list(comp.finditer(h[:20000]))
        if time.time() - t0 > 3.0:
            speed_ok = False
            bad.append("%s: slow on hostile input (%.1fs)" % (obj.get("id"), time.time() - t0))
    check("every regex compiles in Python (this also proves lookbehinds are fixed-width)", compile_ok, "; ".join(bad))
    check("no regex uses a construct outside the Python/.NET common subset", dialect_ok, "; ".join(bad))
    check("no regex is slow on hostile input", speed_ok, "; ".join(bad))
    check("dialect scanner self-check: it does flag named groups, \\d and possessive quantifiers",
          dialect_problems("(?P<a>x)") and dialect_problems("\\d") and dialect_problems("a++") and not dialect_problems("(?:a|b)+[0-9]{2,3}\\b(?<![x])"))

    eng = Engine(data)

    # 3. samples per category
    per_ok = True
    why = []
    for c in data["categories"]:
        pos, neg = c.get("positive_samples", []), c.get("negative_samples", [])
        if not pos or not neg:
            per_ok = False
            why.append("%s needs a positive and a negative sample" % c["id"])
        for k, s in enumerate(pos):
            if c["id"] not in eng.hits(join(s)):
                per_ok = False
                why.append("%s positive %d is not flagged" % (c["id"], k))
        for k, s in enumerate(neg):
            if c["id"] in eng.hits(join(s)):
                per_ok = False
                why.append("%s negative %d is flagged" % (c["id"], k))
        for s in pos:
            if not isinstance(s, list) or len(s) < 2:
                per_ok = False
                why.append("%s has a positive sample that is not an array of at least two fragments" % c["id"])
    check("every category has >=1 positive and >=1 negative sample, positives split into fragments, and each behaves", per_ok, "; ".join(why))

    cross_ok, why = True, []
    for s in data.get("samples", []):
        got = eng.hits(join(s["parts"]))
        if s.get("file_kind") == "code":
            got = [g for g in got if g != "handle"]
        if sorted(got) != sorted(s["expect"]):
            cross_ok = False
            why.append("%s expected %s got %s" % (s["id"], s["expect"], got))
    check("every cross-cutting sample gives exactly its declared answer", cross_ok, "; ".join(why))

    # 4. required samples (by joined text, so the check does not depend on ids)
    all_samples = {}
    for c in data["categories"]:
        for k, s in enumerate(c["positive_samples"]):
            all_samples["%s.pos.%d" % (c["id"], k)] = (join(s), c["id"], "pos")
        for k, s in enumerate(c["negative_samples"]):
            all_samples["%s.neg.%d" % (c["id"], k)] = (join(s), c["id"], "neg")
    for s in data.get("samples", []):
        all_samples[s["id"]] = (join(s["parts"]), None, "x")
    texts = [v[0] for v in all_samples.values()]

    def has(pred):
        return any(pred(t) for t in texts)

    req_neg = ["192.0.2.1", "198.51.100.7", "203.0.113.9", "127.0.0.1", "10.0.22631.4317", "31.0.15.5222", "23.40.27.06", "6.1.1", "9.0.2",
               "C:\\Users\\<user>", "%USERPROFILE%", "/home/user", "<scratch>", "ffmpeg version 9.0.2-essentials_build-www.gyan.dev"]
    miss = [r for r in req_neg if r not in texts and not has(lambda t, r=r: t == r)]
    check("required negative samples are present", not miss, "missing: %s" % miss)
    check("required negative: /home/user/build-scratch reads as <scratch> and is not flagged",
          "/home/user/build-scratch" in texts and not eng.hits("/home/user/build-scratch"))
    check("required negative: a 64-hex SHA-256", has(lambda t: re.fullmatch("[0-9a-f]{64}", t) is not None) and
          all(not eng.hits(t) for t in texts if re.fullmatch("[0-9a-f]{64}", t)))
    check("required negative: a splatting variable in PowerShell code",
          any(s["id"] == "x.powershell_splatting" and s["file_kind"] == "code" and not s["expect"] for s in data["samples"]))
    req_pos = {
        "e-mail on an invented domain": lambda t: eng.hits(t) == ["email"] and "@" in t,
        "IPv4 outside the documentation ranges": lambda t: eng.hits(t) == ["ipv4"],
        "full IPv6": lambda t: eng.hits(t) == ["ipv6"] and t.count(":") == 7,
        "MAC": lambda t: eng.hits(t) == ["mac"],
        "Windows profile path under a real-looking user name": lambda t: eng.hits(t) == ["profile_path_windows"],
        "Linux home path under a name other than user": lambda t: eng.hits(t) == ["profile_path_linux"] and t.startswith("/home/"),
        "GitHub-token-shaped string of full length": lambda t: eng.hits(t) == ["token_shape"] and t.startswith("ghp_") and len(t) >= 40,
        "GUID": lambda t: eng.hits(t) == ["guid_serial"] and re.fullmatch(r"[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", t) is not None,
        "32-hex run": lambda t: eng.hits(t) == ["guid_serial"] and re.fullmatch("[0-9a-f]{32}", t) is not None,
        "65-hex run": lambda t: eng.hits(t) == ["guid_serial"] and re.fullmatch("[0-9a-f]{65}", t) is not None,
        "serial-like token": lambda t: eng.hits(t) == ["guid_serial"] and re.fullmatch("[A-Z0-9]{10,40}", t) is not None,
        "at-sign handle in prose": lambda t: eng.hits(t) == ["handle"] and "@" in t and " " in t,
    }
    for label, pred in req_pos.items():
        check("required positive: " + label, has(pred))
    check("required positive: 32-to-63 hex still flagged next to the 64 exemption",
          any(s["id"] == "x.hex_63" and s["expect"] == ["guid_serial"] for s in data["samples"]))

    # 5. the file contains none of the strings it forbids
    file_hits = []
    for line_no, line in enumerate(raw.split("\n"), 1):
        for h in eng.hits(line):
            file_hits.append("%s on line %d" % (h, line_no))
    check("the raw file text raises no hit in any category (it does not trip the lint on itself)", not file_hits, "; ".join(file_hits[:5]))
    joined_present = []
    for sid, (t, cat, kind) in all_samples.items():
        flagged = (kind == "pos") or (kind == "x" and sid in [s["id"] for s in data["samples"] if s["expect"]])
        if flagged and t in raw:
            joined_present.append(sid)
    check("no flagged sample appears joined anywhere in the raw file text", not joined_present, ", ".join(joined_present))
    unsplit = [c["id"] for c in data["categories"] for s in c["positive_samples"] if len(join(s)) > 12 and len(s) < 2]
    check("positive samples are all split into fragments", not unsplit)

    # 6. the rest of 4.13
    ex_ids = [e.get("id") for e in data.get("exemptions", [])]
    check("exemption sha256_64hex exists for guid_serial and matches exactly 64 hex not flanked by hex digits",
          "sha256_64hex" in ex_ids and next(e for e in data["exemptions"] if e["id"] == "sha256_64hex")["category"] == "guid_serial"
          and re.search(next(e for e in data["exemptions"] if e["id"] == "sha256_64hex")["regex"], "a" * 64) is not None
          and re.search(next(e for e in data["exemptions"] if e["id"] == "sha256_64hex")["regex"], "a" * 65) is None
          and re.search(next(e for e in data["exemptions"] if e["id"] == "sha256_64hex")["regex"], "a" * 63) is None)
    guid_only = [c for c in data["categories"] if c["id"] == "guid_serial"][0]
    sha_samples = [join(s) for s in guid_only["negative_samples"] if re.fullmatch("[0-9a-f]{64}", join(s))]
    check("without the exemption the guid_serial regex WOULD flag a 64-hex (the exemption is what saves it)",
          sha_samples and re.search(guid_only["regex"], sha_samples[0]) is not None and "guid_serial" not in eng.hits(sha_samples[0]))
    fe = data.get("field_exemptions", [])
    need_fields = {"gpus[].driver_version", "os.version", "os.build", "powershell.version", "tools.*.version"}
    have_fields = set(f for e in fe if e.get("category") == "ipv4" for f in e.get("fields", []))
    check("field_exemptions covers ipv4 in the version fields", need_fields <= have_fields, "missing: %s" % sorted(need_fields - have_fields))
    nc = data.get("name_checks", {})
    check("name_checks: sources, min_name_len 3, fragment_len 4, hardware fields, report-not-refuse",
          nc.get("sources") == ["user", "computer", "domain"] and nc.get("min_name_len") == 3 and nc.get("fragment_len") == 4
          and set(nc.get("hardware_name_fields", [])) == {"cpu.name", "gpus[].name", "gpus[].vendor", "os.caption"}
          and nc.get("hardware_field_action") == "report")
    check("mask keeps 2 characters and fills with *", data.get("mask", {}).get("keep") == 2 and data["mask"].get("fill") == "*")
    need_ph = {"C:\\Users\\<user>", "%USERPROFILE%", "/home/user", "/home/user/build-scratch"}
    check("placeholders list the four generic paths (and <scratch> is the alias of the last)",
          need_ph <= set(data.get("placeholders", [])) and data.get("placeholder_aliases", {}).get("/home/user/build-scratch") == "<scratch>")
    check("path_denylist has the three raw-report globs and the fixture dir is the only exemption",
          set(data.get("path_denylist", [])) == {"**/pc_report*.json", "**/colour_patch_pc*.json", "**/maker-pc*.json"}
          and data.get("path_denylist_exempt_dirs") == ["tests/win/fixtures/"])
    check("local_deny names the git-ignored deny file", data.get("local_deny") == "scripts/public_lint.deny.local.txt")

    failed = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d passed, %d failed" % (len(RESULTS), len(RESULTS) - len(failed), len(failed)))
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(json.dumps({"checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in RESULTS]}, indent=1), encoding="utf-8")
    if failed:
        return 1
    if marker:
        MARKER.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(PATTERNS.read_bytes()).hexdigest()
        MARKER.write_text("4.13 LANDED: scripts/redaction_patterns.json version %s, internal test passed (%d checks), sha256 %s\n"
                          % (data["version"], len(RESULTS), digest), encoding="utf-8")
        print("wrote build/evidence/wp03/LANDED-4.13.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
