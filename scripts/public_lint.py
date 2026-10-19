#!/usr/bin/env python3
"""public_lint.py: is it safe to publish this? (repository is PUBLIC, D-26.) Standard library only. READ-ONLY.

WHAT IT CHECKS (a finding is printed MASKED: category, file:line, the first two characters of the hit and asterisks)
  1. identifying data, using ONLY the categories of scripts/redaction_patterns.json (build plan 4.13): e-mail,
     IPv4, IPv6, MAC, Windows and Linux profile paths, token shapes, GUIDs/serials, at-sign handles. This file
     carries no regex of its own for any of them. /home/user and <scratch> are the generic placeholders and pass;
     /home/<any other name> does not.
  2. NUL bytes (a binary file), files over 1 MB (not scanned further), and media/image files that .gitignore
     already blocks but that are tracked or staged anyway (git add -f).
  3. the path denylist: a file named like a raw PC report (pc_report*.json, colour_patch_pc*.json,
     maker-pc*.json) anywhere except under tests/win/fixtures/.
  4. the optional local deny list scripts/public_lint.deny.local.txt (git-ignored; the maker's real names and PC
     name, one per line, loaded on the maker's machine only, never printed). The file itself is a finding (exit 2)
     when it is tracked or staged, or when it exists but git does not ignore it (default mode and --all).
  5. --theme: D-28 exclusions (Mughal, Islamic, mosque, minaret, Taj Mahal, Red Fort, church, cathedral,
     crucifix, nativity, Christmas, ...) in NEW theme-bearing files. A keyword scan cannot judge iconography;
     a person (and the Fable review) must look at the pictures. Existing playbooks and research are INFO only.
     A line in a .md file with an exclusion cue (no, never, not, excluded, avoid, out of scope, left out ...) within
     40 characters BEFORE the keyword is a rule statement and prints as a NOTE; everything else is a finding,
     always so under pipeline/scenes/ and in pipeline/phone/test_strings.json (scripts/public_lint.config.json).

HOW TO RUN   (python3 -I on Linux, py -3 -I on Windows)
  python3 -I scripts/public_lint.py                 added lines of the diff against HEAD + untracked files (before a commit)
  python3 -I scripts/public_lint.py --staged        only what is staged
  python3 -I scripts/public_lint.py --paths A B     whole files / folders under the repository root (no git needed);
                                                    a path outside --root is a USAGE error, exit 2 (it would not be read)
  python3 -I scripts/public_lint.py --all           every tracked and untracked file (a whole-tree audit)
  python3 -I scripts/public_lint.py --theme [--paths ...]    the D-28 keyword guard on new theme-bearing files
  python3 -I scripts/public_lint.py --self-test     the 4.13 disagreement test (every consumer, every sample)
  python3 -I scripts/public_lint.py --pattern-self-test SAMPLES.json     the consumer contract (prints one JSON object)
  Options: --root DIR, --patterns F, --config F, --json OUT.json, --no-allow (ignore the config allow list),
           --fail-on-skip (self-test: a consumer that has not landed is a failure; WP-11b's final run)

EXIT CODES (build plan 4.3)
  0 clean   1 a hygiene or theme finding (binary, over 1 MB, ignored-but-tracked media, theme keyword,
  self-test disagreement)   2 identifying data found (any 4.13 category, a denylisted file name, a local deny
  word, a local deny list that is not git-ignored), or bad usage (a --paths path outside --root), or the pattern file
  is missing or invalid (fail closed)   3 environment (git missing).
It writes only the file named by --json, never changes the tree, never touches the network, and prints only
repo-relative paths and masked hits.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parent
PATTERNS_DEFAULT = HERE / "redaction_patterns.json"
CONFIG_DEFAULT = HERE / "public_lint.config.json"

REQUIRED_IDS = ("email", "ipv4", "ipv6", "mac", "profile_path_windows", "profile_path_linux", "token_shape", "guid_serial", "handle")
SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__"}


class FailClosed(Exception):
    """The pattern file is missing or unusable (exit 2)."""


class Usage(Exception):
    """Bad command line (exit 2)."""


# ----------------------------------------------------------------------------- helpers
def _join(x):
    return "".join(x) if isinstance(x, list) else str(x)


def mask(value, keep=2, fill="*", cap=8):
    value = str(value)
    if len(value) <= keep:
        return fill * max(1, len(value))
    return value[:keep] + fill * min(len(value) - keep, cap)


_GLOB = {}


def glob_match(rel, pat):
    """Path-aware glob: * and ? stop at a slash, ** crosses slashes. A pattern starting with **/ also matches at the top."""
    rx = _GLOB.get(pat)
    if rx is None:
        out, i = "", 0
        while i < len(pat):
            if pat.startswith("**/", i):
                out += "(?:.*/)?"
                i += 3
                continue
            if pat.startswith("**", i):
                out += ".*"
                i += 2
                continue
            c = pat[i]
            out += "[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c)
            i += 1
        rx = _GLOB[pat] = re.compile("^" + out + "$")
    return bool(rx.match(rel))


def decode_bytes(raw):
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", errors="replace")
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    if len(raw) >= 4 and raw[1:2] == b"\x00" and raw[3:4] == b"\x00":
        return raw.decode("utf-16-le", errors="replace")
    return raw.decode("utf-8", errors="replace")


def is_utf16(raw):
    return raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff") or (len(raw) >= 4 and raw[1:2] == b"\x00" and raw[3:4] == b"\x00" and raw[0:1] != b"\x00")


# ----------------------------------------------------------------------------- the 4.13 pattern file
class Patterns:
    def __init__(self, data):
        self.data = data
        self.version = data.get("version")
        self.cats = []
        for c in data["categories"]:
            apply_to = c.get("apply_to")
            self.cats.append({"id": c["id"], "scope": c.get("scope", "both"),
                              "rx": re.compile(c["regex"], re.I if "i" in c.get("flags", "") else 0),
                              "apply_to": [x.lower() for x in apply_to] if apply_to else None,
                              "pos": [_join(s) for s in c.get("positive_samples", [])], "neg": [_join(s) for s in c.get("negative_samples", [])]})
        self.exemptions = []
        for e in data.get("exemptions", []):
            cats = e.get("category") or e.get("categories")
            cats = [cats] if isinstance(cats, str) else (list(cats) if cats else None)
            self.exemptions.append({"id": e.get("id", ""), "cats": cats, "rx": re.compile(e["regex"], re.I if "i" in e.get("flags", "") else 0)})
        self.placeholders = set(str(x) for x in data.get("placeholders", []))
        mk = data.get("mask") or {}
        self.keep, self.fill, self.cap = int(mk.get("keep", 2)), str(mk.get("fill", "*")) or "*", int(mk.get("cap", 8))
        self.denylist = list(data.get("path_denylist", []))
        self.deny_exempt_dirs = list(data.get("path_denylist_exempt_dirs", []))
        ld = data.get("local_deny")
        if isinstance(ld, dict):
            ld = ld.get("path") or ld.get("file")
        self.local_deny = ld or "scripts/public_lint.deny.local.txt"
        self.samples = data.get("samples", [])

    def mask(self, v):
        return mask(v, self.keep, self.fill, self.cap)

    def applies(self, cat, rel):
        """Is this category applied to this file? (scope text/both; handle only to its apply_to extensions)"""
        if cat["scope"] not in ("text", "both"):
            return False
        if cat["apply_to"]:
            return Path(rel).suffix.lower() in [a.replace("*", "") for a in cat["apply_to"]]
        return True

    def scan_line(self, line, rel=None, kind=None):
        """Return [(category_id, matched_text, start)] for one line, honouring placeholders and exemptions."""
        out = []
        ex_cache = {}
        for c in self.cats:
            if rel is not None and not self.applies(c, rel):
                continue
            if rel is None and c["scope"] not in ("text", "both"):
                continue
            if kind == "code" and c["id"] == "handle":
                continue
            for m in c["rx"].finditer(line):
                t = m.group(0)
                if t in self.placeholders:
                    continue
                exempt = False
                for ex in self.exemptions:
                    if ex["cats"] is not None and c["id"] not in ex["cats"]:
                        continue
                    spans = ex_cache.get(ex["id"])
                    if spans is None:
                        spans = ex_cache[ex["id"]] = [mm.span() for mm in ex["rx"].finditer(line)]
                    if any(a <= m.start() and m.end() <= b for a, b in spans):
                        exempt = True
                        break
                if not exempt:
                    out.append((c["id"], t, m.start()))
        return out


def load_patterns(path):
    p = Path(path)
    if not p.is_file():
        raise FailClosed("the pattern file scripts/redaction_patterns.json is missing; nothing was checked")
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        raise FailClosed("the pattern file does not parse as JSON; nothing was checked")
    if not isinstance(data, dict) or not isinstance(data.get("categories"), list):
        raise FailClosed("the pattern file has no categories; nothing was checked")
    ids = {c.get("id") for c in data["categories"] if isinstance(c, dict)}
    missing = [i for i in REQUIRED_IDS if i not in ids]
    if missing:
        raise FailClosed("the pattern file lacks required categories (%s); nothing was checked" % ", ".join(missing))
    try:
        return Patterns(data)
    except (KeyError, TypeError, ValueError, re.error) as e:
        raise FailClosed("the pattern file is not valid (%s); nothing was checked" % type(e).__name__)


def load_config(path):
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        raise Usage("the lint config is missing or does not parse")
    if d.get("schema") != "lj-public-lint-config/1":
        raise Usage("the lint config has the wrong schema")
    for a in d.get("allow", []):
        a["_rx"] = re.compile(a["value_regex"])
    for t in d.get("theme", {}).get("keywords", []):
        t["_rx"] = re.compile(t["regex"], re.I)
    if d.get("theme", {}).get("exclusion_cue_regex"):
        d["theme"]["_cue"] = re.compile(d["theme"]["exclusion_cue_regex"], re.I)
    return d


# ----------------------------------------------------------------------------- git
def git(root, *args, check=False):
    try:
        r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0 and check:
        return None
    return r.stdout if r.returncode == 0 else None


def is_git(root):
    out = git(root, "rev-parse", "--is-inside-work-tree")
    return bool(out and out.strip() == "true")


def parse_diff_added(diff_text):
    """{path: [(lineno, text)]} for added lines of a -U0 unified diff."""
    out = {}
    cur, ln = None, 0
    for raw in diff_text.split("\n"):
        if raw.startswith("+++ "):
            p = raw[4:]
            cur = None if p == "/dev/null" else (p[2:] if p.startswith("b/") else p)
            if cur is not None and cur.startswith('"'):
                cur = cur.strip('"')
            out.setdefault(cur, []) if cur else None
            continue
        if raw.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
            ln = int(m.group(1)) if m else 0
            continue
        if cur is None:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            out[cur].append((ln, raw[1:]))
            ln += 1
    return out


# ----------------------------------------------------------------------------- the scan
class Finding:
    __slots__ = ("kind", "category", "file", "line", "hit", "note")

    def __init__(self, kind, category, file, line=None, hit=None, note=""):
        self.kind, self.category, self.file, self.line, self.hit, self.note = kind, category, file, line, hit, note

    def text(self):
        loc = self.file + (":%d" % self.line if self.line else "")
        s = "FINDING %-11s %-20s %s" % (self.kind, self.category, loc)
        if self.hit is not None:
            s += " hit=%s" % self.hit
        if self.note:
            s += "  (%s)" % self.note
        return s

    def as_dict(self):
        return {"kind": self.kind, "category": self.category, "file": self.file, "line": self.line, "hit": self.hit, "note": self.note}


class Linter:
    def __init__(self, root, pat, cfg, use_allow=True):
        self.root, self.pat, self.cfg = Path(root), pat, cfg
        self.use_allow = use_allow
        self.findings = []
        self.notes = []
        self.suppressed = {}
        self.scanned = 0
        self.local_words = self._load_local_deny()
        self.maxb = int(cfg.get("max_file_bytes", 1000000))
        self.allow_binary = list(cfg.get("allow_binary", []))
        self.fixture = cfg.get("fixture_dirs", [])

    def _load_local_deny(self):
        p = self.root / self.pat.local_deny
        words = []
        try:
            if p.is_file():
                text = decode_bytes(p.read_bytes())
                for line in text.splitlines():
                    w = line.strip()
                    if w and not w.startswith("#"):
                        words.append(w)
        except OSError:
            pass
        return [(w, re.compile(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", re.I)) for w in words]

    # --- path level
    def check_path(self, rel):
        for pat in self.pat.denylist:
            if glob_match(rel, pat):
                if any(rel.startswith(d) for d in self.pat.deny_exempt_dirs):
                    continue
                if any(glob_match(rel, g) for g in self.cfg.get("denylist_exempt_globs", [])):
                    continue
                self.findings.append(Finding("denylist", "raw_pc_report", rel, note="a raw PC report is a hardware fingerprint; it is read in chat and never filed (4.4)"))
                break
        for w, rx in self.local_words:
            m = rx.search(rel)
            if m:
                self.findings.append(Finding("local_deny", "local_deny", rel, hit=self.pat.mask(m.group(0)), note="in the file name"))

    # --- one line
    def check_line(self, rel, ln, line, in_fence=False):
        demote = set()
        for fx in self.fixture:
            if rel.startswith(fx["dir"]):
                demote |= set(fx.get("demote", []))
        spans = None
        if rel.lower().endswith(".md"):
            spans = [m.span() for m in re.finditer(r"`[^`]*`", line)]
        for cid, text, start in self.pat.scan_line(line, rel=rel):
            if cid == "handle" and rel.lower().endswith(".md") and (in_fence or any(a <= start < b for a, b in (spans or []))):
                continue  # an at sign inside markdown code is splatting or a decorator, not a social handle
            if self.use_allow and self._allowed(cid, rel, text):
                continue
            if cid in demote:
                self.notes.append(Finding("fixture-note", cid, rel, ln, self.pat.mask(text), "synthetic fixture folder: planted values are expected here"))
                continue
            self.findings.append(Finding("identifying", cid, rel, ln, self.pat.mask(text)))
        for w, rx in self.local_words:
            m = rx.search(line)
            if m:
                self.findings.append(Finding("local_deny", "local_deny", rel, ln, self.pat.mask(m.group(0))))

    def _allowed(self, cid, rel, text):
        for a in self.cfg.get("allow", []):
            cats = a["category"] if isinstance(a["category"], list) else [a["category"]]
            if cid not in cats and "*" not in cats:
                continue
            if not any(glob_match(rel, g) for g in a.get("paths", ["**"])):
                continue
            if a["_rx"].fullmatch(text):
                self.suppressed[a["id"]] = self.suppressed.get(a["id"], 0) + 1
                return True
        return False

    # --- one file
    def check_file(self, rel, added_lines=None):
        """added_lines: [(lineno, text)] to scan only those lines (diff mode); None = the whole file."""
        if rel == self.pat.local_deny:
            return  # the local deny list is full of names by design; it is never scanned or printed, only refused if tracked (see gather)
        full = self.root / rel
        self.check_path(rel)
        try:
            if full.is_symlink() or not full.is_file():
                return
            size = full.stat().st_size
        except OSError:
            return
        self.scanned += 1
        try:
            with open(full, "rb") as fh:
                head = fh.read(8192)
        except OSError:
            return
        if b"\x00" in head and not is_utf16(head):
            if not any(glob_match(rel, g) for g in self.allow_binary):
                self.findings.append(Finding("binary", "nul_byte", rel, note="binary file (NUL byte); personal media never goes in git"))
            return
        if size > self.maxb:
            self.findings.append(Finding("size", "over_1mb", rel, note="%.1f MB; not scanned further" % (size / 1e6)))
            return
        raw = full.read_bytes()
        if b"\x00" in raw and not is_utf16(head):
            self.findings.append(Finding("binary", "nul_byte", rel, note="NUL byte after the first 8 KB"))
            return
        text = decode_bytes(raw)
        if added_lines is None:
            fence = False
            for i, line in enumerate(text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
                if rel.lower().endswith(".md") and line.lstrip().startswith(("```", "~~~")):
                    fence = not fence
                    continue
                if line:
                    self.check_line(rel, i, line, in_fence=fence)
        else:
            for ln, line in added_lines:
                if line.strip():
                    self.check_line(rel, ln, line)


OUTSIDE_ROOT = "a path given to --paths is outside the repository root (--root); run the lint from the clone, or pass --root"


def walk_paths(root, paths):
    """Expand files and folders (relative to cwd or absolute) into repo-relative posix paths. A path outside the
    repository root is a usage error (exit 2), never a silent zero: the lint opens root/rel, so it could not read it."""
    root = Path(root).resolve()
    out = []
    for p in paths:
        pp = Path(p)
        if not pp.is_absolute():
            pp = (Path.cwd() / pp) if (Path.cwd() / pp).exists() else (root / pp)
        if not pp.exists():
            raise Usage("a path given to --paths does not exist")
        pp = pp.resolve()
        try:
            pp.relative_to(root)
        except ValueError:
            # A file the lint cannot open under the root would be "scanned" as nothing and the exit code would say clean
            # (review r4, C-1). Refuse instead; the message names no path.
            raise Usage(OUTSIDE_ROOT)
        files = [pp] if pp.is_file() else []
        if pp.is_dir():
            for dp, dn, fn in os.walk(pp):
                dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
                files += [Path(dp) / f for f in sorted(fn)]
        for f in files:
            try:
                rel = f.relative_to(root).as_posix()
            except ValueError:
                raise Usage(OUTSIDE_ROOT)
            out.append(rel)
    seen, uniq = set(), []
    for r in out:
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    return uniq


def local_deny_findings(root, pat, tracked, staged, check_ignore=True):
    """The local deny list holds the maker's real names, so it must stay git-ignored. Refused (a finding, exit 2) when it is tracked
    or staged; and, while it merely sits in the working tree, when git does not ignore it, because one 'git add -A' would stage it
    (review r4, nudge 5). The file is never read here and its words are never printed."""
    lp = pat.local_deny
    if lp in tracked or lp in staged:
        return [Finding("local_deny", "local_deny_file", lp, note="the local deny list holds real names and must stay git-ignored on the maker's machine; unstage it")]
    if check_ignore and (Path(root) / lp).is_file() and git(root, "check-ignore", "-q", "--", lp) is None:
        return [Finding("local_deny", "local_deny_file", lp, note="exists but is not git-ignored; add scripts/public_lint.deny.local.txt (or *.local.*) to .gitignore before git add -A")]
    return []


def gather(root, args, pat):
    """Return (mode_label, [(rel, added_lines_or_None)], extra_findings)"""
    extra = []
    if args.paths:
        return "paths", [(r, None) for r in walk_paths(root, args.paths)], extra
    if not is_git(root):
        raise EnvironmentError("not a git repository: use --paths or --all")
    if args.all:
        tracked = (git(root, "ls-files", "-c", "-z") or "").split("\0")
        other = (git(root, "ls-files", "-o", "--exclude-standard", "-z") or "").split("\0")
        files = sorted(set(x for x in tracked + other if x))
        extra.extend(local_deny_findings(root, pat, set(tracked), set()))
        return "all", [(f, None) for f in files], extra
    out = {}
    have_head = git(root, "rev-parse", "--verify", "HEAD") is not None
    if args.staged:
        diff = git(root, "diff", "--cached", "--no-color", "-U0", "--diff-filter=ACMR") or ""
    elif have_head:
        diff = git(root, "diff", "HEAD", "--no-color", "-U0", "--diff-filter=ACMR") or ""
    else:
        diff = ""
        for f in (git(root, "ls-files", "-c", "-z") or "").split("\0"):
            if f:
                out[f] = None
    for f, lines in parse_diff_added(diff).items():
        out[f] = lines
    if not args.staged:
        for f in (git(root, "ls-files", "-o", "--exclude-standard", "-z") or "").split("\0"):
            if f:
                out[f] = None
    # binary files in the diff have no added lines but must still get the NUL check
    names = git(root, "diff", "--cached" if args.staged else "HEAD", "--name-only", "-z", "--diff-filter=ACMR") if (args.staged or have_head) else ""
    for f in (names or "").split("\0"):
        if f and f not in out:
            out[f] = []
    # the local deny list must never be tracked or staged
    tracked_now = set((git(root, "ls-files", "-c", "-z") or "").split("\0"))
    staged_now = set((git(root, "diff", "--cached", "--name-only", "-z") or "").split("\0"))
    # --staged looks at the index only, where staged-ness is the whole question; the other modes also ask whether git ignores the file
    extra.extend(local_deny_findings(root, pat, tracked_now, staged_now, check_ignore=not args.staged))
    # media that .gitignore blocks but that is tracked or staged anyway
    for f in (git(root, "ls-files", "-c", "-i", "--exclude-standard", "-z") or "").split("\0"):
        if f:
            extra.append(Finding("ignored-staged", "gitignore_media", f, note="matches .gitignore but is tracked or staged (git add -f); only a reviewed, small, non-personal image may be force-added"))
            out.setdefault(f, [])
    return ("staged" if args.staged else "diff"), sorted(out.items()), extra


# ----------------------------------------------------------------------------- theme guard
def cue_before(cue, t, pos, win):
    """True when an exclusion cue (no, never, not, excluded, avoid..., left out...) ENDS within WIN characters before
    POS in line T. A cue after the keyword never counts: 'a Mughal garden, not too dark' and 'fade out to a Taj Mahal'
    are uses. The cue is found in the whole line (not a slice) so a word cut by the window is never taken for a cue."""
    if cue is None:
        return False
    return any(0 <= pos - c.end() <= win for c in cue.finditer(t) if c.end() <= pos)


def theme_scan(root, cfg, pat, args):
    th = cfg.get("theme", {})
    findings, info, statements = [], {}, []
    cue, win = th.get("_cue"), int(th.get("exclusion_cue_window", 40))
    theme_paths = th.get("paths", [])
    in_path = lambda rel, plist: any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in plist)
    is_theme = lambda rel: in_path(rel, theme_paths)
    # Where a rule statement may be shown as a NOTE instead of a finding (review r1, C-1): prose files only. Never under
    # pipeline/scenes/ or in the phone test strings, where every string is rendered and 'out', 'no', 'without' are animation words.
    demote_suffixes = tuple(x.lower() for x in th.get("exclusion_demote_suffixes", [".md"]))
    never_demote = th.get("exclusion_never_demote", ["pipeline/scenes/", "pipeline/phone/test_strings.json"])
    can_demote = lambda rel: rel.lower().endswith(demote_suffixes) and not in_path(rel, never_demote)
    if args.paths:
        targets = [(r, None) for r in walk_paths(root, args.paths)]
        label = "explicit paths"
    else:
        if not is_git(root):
            raise EnvironmentError("not a git repository: use --paths")
        have_head = git(root, "rev-parse", "--verify", "HEAD") is not None
        diff = git(root, "diff", "HEAD", "--no-color", "-U0", "--diff-filter=ACMR") if have_head else ""
        out = {}
        for f, lines in parse_diff_added(diff or "").items():
            out[f] = lines
        for f in (git(root, "ls-files", "-o", "--exclude-standard", "-z") or "").split("\0"):
            if f:
                out[f] = None
        if not have_head:
            for f in (git(root, "ls-files", "-c", "-z") or "").split("\0"):
                if f:
                    out[f] = None
        targets = [(f, v) for f, v in sorted(out.items()) if is_theme(f)]
        label = "new or changed theme-bearing files"
    for rel, added in targets:
        full = Path(root) / rel
        try:
            if not full.is_file() or full.stat().st_size > int(cfg.get("max_file_bytes", 1000000)):
                continue
            raw = full.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw[:8192] and not is_utf16(raw[:8192]):
            continue
        lines = decode_bytes(raw).replace("\r\n", "\n").replace("\r", "\n").split("\n")
        items = [(i + 1, t) for i, t in enumerate(lines)] if added is None else added
        demotable = can_demote(rel)
        for ln, t in items:
            for kw in th.get("keywords", []):
                hits = list(kw["_rx"].finditer(t))
                if not hits:
                    continue
                # one verdict per keyword per line: a statement only if EVERY occurrence has an exclusion cue just before it
                bare = next((m for m in hits if not (demotable and cue_before(cue, t, m.start(), win))), None)
                if bare is None:
                    statements.append(Finding("theme-excl", kw["id"], rel, ln, hits[0].group(0), "the line says the motif is excluded: a statement of the rule, not a use"))
                else:
                    findings.append(Finding("theme", kw["id"], rel, ln, bare.group(0), "D-28 exclusion keyword: %s" % kw.get("why", "")))
    # INFO only: existing playbooks, skills and research (counted, never failing)
    if not args.paths and is_git(root):
        tracked = (git(root, "ls-files", "-c", "-z") or "").split("\0")
        for rel in tracked:
            if not any(rel.startswith(p) for p in th.get("info_paths", [])):
                continue
            try:
                full = Path(root) / rel
                if not full.is_file() or full.stat().st_size > 2000000:
                    continue
                raw = full.read_bytes()
            except OSError:
                continue
            if b"\x00" in raw[:8192]:
                continue
            txt = decode_bytes(raw)
            n = sum(1 for kw in th.get("keywords", []) for _ in kw["_rx"].finditer(txt))
            if n:
                top = rel.split("/")[0] if not rel.startswith(".claude/") else ".claude/skills"
                info[top] = info.get(top, 0) + n
    return label, targets, findings, info, statements


# ----------------------------------------------------------------------------- consumers and the disagreement test
def find_powershell(root):
    """(executable, flavour). PowerShell 7 first (LJ_PWSH, PATH, or the scratch install); on Windows Windows PowerShell 5.1 as a fallback."""
    env = os.environ.get("LJ_PWSH")
    if env and Path(env).exists():
        return env, "pwsh"
    w = shutil.which("pwsh")
    if w:
        return w, "pwsh"
    cand = Path(root).resolve().parent / "build-scratch" / "pwsh" / "pwsh"
    if cand.exists():
        return str(cand), "pwsh"
    if os.name == "nt":
        w = shutil.which("powershell") or shutil.which("powershell.exe")
        if w:
            return w, "powershell51"
    return None, None


def ps_version(exe):
    try:
        r = subprocess.run([exe, "-NoProfile", "-NonInteractive", "-Command", "$PSVersionTable.PSVersion.ToString()"], capture_output=True, text=True, timeout=60)
        return r.stdout.strip().splitlines()[0] if r.stdout.strip() else "unknown"
    except (OSError, subprocess.SubprocessError, IndexError):
        return "unknown"


def samples_from(pat):
    """{id: text} and {id: file_kind} and {id: expectation}"""
    texts, kinds, expect = {}, {}, {}
    for c in pat.cats:
        for k, t in enumerate(c["pos"]):
            sid = "%s.pos.%d" % (c["id"], k)
            texts[sid], expect[sid] = t, ("has", c["id"])
        for k, t in enumerate(c["neg"]):
            sid = "%s.neg.%d" % (c["id"], k)
            texts[sid], expect[sid] = t, ("hasnot", c["id"])
    for s in pat.samples:
        texts[s["id"]] = _join(s["parts"])
        kinds[s["id"]] = s.get("file_kind", "text")
        expect[s["id"]] = ("exact", list(s.get("expect", [])))
    return texts, kinds, expect


def own_answers(pat, texts, kinds):
    return {sid: sorted(set(c for c, _, _ in pat.scan_line(t, kind=kinds.get(sid)))) for sid, t in texts.items()}


def run_consumer(label, argv, cwd, timeout=180):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, errors="replace", cwd=str(cwd), timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return None, "could not run (%s)" % type(e).__name__
    if r.returncode != 0:
        return None, "exit %d" % r.returncode
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "{}")
    except ValueError:
        return None, "did not print one JSON object"
    return d, None


def self_test(root, pat, fail_on_skip=False):
    root = Path(root)
    texts, kinds, expect = samples_from(pat)
    mine = own_answers(pat, texts, kinds)
    scratch = root.resolve().parent / "build-scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    problems, skips = [], []
    with tempfile.TemporaryDirectory(prefix="lj-lint-selftest-", dir=str(scratch)) as td:
        sfile = Path(td) / "samples.json"
        sfile.write_text(json.dumps({"samples": texts, "file_kind": kinds}), encoding="utf-8")
        print("self-test: %d samples (built from fragments into <scratch>); patterns version %s" % (len(texts), pat.version))
        # 1. declared expectations against our own answers
        for sid, (how, what) in expect.items():
            got = mine[sid]
            ok = (what in got) if how == "has" else (what not in got) if how == "hasnot" else (sorted(got) == sorted(what))
            if not ok:
                problems.append("DISAGREEMENT scripts/public_lint.py vs declared expectation: sample %s: expected %s %s, got %s" % (sid, how, what, got))
        print("consumer scripts/public_lint.py: %s (own regex set read from scripts/redaction_patterns.json; %d samples)" % ("ok" if not problems else "DISAGREES with the declared expectations", len(texts)))
        report_cats = set(c["id"] for c in pat.cats if c["scope"] in ("report", "both"))
        # 2. every other consumer
        consumers = [
            ("scripts/windows_check.py", root / "scripts" / "windows_check.py", [sys.executable, "-I", str(root / "scripts" / "windows_check.py"), "--pattern-self-test", str(sfile)]),
            ("win/step0_pc_tests.ps1", root / "win" / "step0_pc_tests.ps1", None),
            ("win/kit2/run_checks_pc.ps1", root / "win" / "kit2" / "run_checks_pc.ps1", None),
        ]
        pwsh, flavour = find_powershell(root)
        ps_ver = ps_version(pwsh) if pwsh else None
        ran_on_51 = False
        for label, path, argv in consumers:
            if not path.exists():
                print("consumer %s: SKIPPED: not landed" % label)
                skips.append(label)
                continue
            if argv is None:
                if not pwsh:
                    print("consumer %s: SKIPPED: no PowerShell is available here (behaviour UNVERIFIED)" % label)
                    skips.append(label)
                    continue
                argv = [pwsh, "-NoProfile", "-NonInteractive"] + (["-ExecutionPolicy", "Bypass"] if flavour == "powershell51" else []) + ["-File", str(path), "-PatternSelfTest", str(sfile)]
                ran_on_51 = ran_on_51 or flavour == "powershell51"
            d, err = run_consumer(label, argv, root)
            if d is None:
                problems.append("DISAGREEMENT %s: could not get an answer (%s)" % (label, err))
                print("consumer %s: FAILED (%s)" % (label, err))
                continue
            if d.get("patterns_version") != pat.version:
                problems.append("DISAGREEMENT %s: patterns_version %s vs %s" % (label, d.get("patterns_version"), pat.version))
            res = d.get("results", {})
            bad = 0
            for sid in texts:
                theirs = sorted(res.get(sid, ["<no answer>"]))
                want = sorted(c for c in mine[sid] if c in report_cats)
                if theirs != want:
                    bad += 1
                    problems.append("DISAGREEMENT %s, sample %s: %s says %s, scripts/public_lint.py says %s (report-scope categories)" % (label, sid, label, theirs, want))
            via = (" via %s %s" % ("Windows PowerShell" if flavour == "powershell51" else "PowerShell", ps_ver)) if label.endswith(".ps1") else ""
            print("consumer %s: %s (%d samples compared on the report-scope categories%s)" % (label, "ok" if not bad else "%d DISAGREEMENT(S)" % bad, len(texts), via))
    for p in problems:
        print(p)
    if skips and fail_on_skip:
        problems.append("skipped consumers are failures with --fail-on-skip: %s" % ", ".join(skips))
        print(problems[-1])
    print("self-test: %s" % ("no disagreement between consumers%s" % (" (skipped: %s)" % ", ".join(skips) if skips else "") if not problems else "%d problem(s)" % len(problems)))
    if ran_on_51:
        print("note: win/step0_pc_tests.ps1 was exercised on Windows PowerShell 5.1 in this run.")
    else:
        print("note: Windows PowerShell 5.1 was not available in this run; win/step0_pc_tests.ps1 was exercised on PowerShell 7 only (5.1 behaviour UNVERIFIED until the maker's PC runs this self-test).")
    return not problems


def pattern_self_test(pat, samples_path):
    try:
        data = json.loads(Path(samples_path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        print("cannot read the samples file", file=sys.stderr)
        return 2
    kinds = {}
    if isinstance(data, dict) and isinstance(data.get("samples"), (dict, list)):
        kinds = data.get("file_kind", {}) or {}
        data = data["samples"]
    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            items[str(k)] = _join(v["text"] if isinstance(v, dict) and "text" in v else v)
    else:
        for i, v in enumerate(data):
            if isinstance(v, dict):
                items[str(v.get("id", i))] = _join(v.get("text", v.get("value", "")))
            else:
                items[str(i)] = _join(v)
    res = {}
    for sid, t in items.items():
        res[sid] = sorted(set(c for c, _, _ in pat.scan_line(t, kind=kinds.get(sid))))
    print(json.dumps({"consumer": "scripts/public_lint.py", "patterns_version": pat.version, "results": res}, separators=(",", ":")))
    return 0


# ----------------------------------------------------------------------------- main
def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog="public_lint.py", allow_abbrev=False, description="Is it safe to publish this? (read-only)")
    ap.add_argument("--paths", nargs="+", metavar="PATH")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--theme", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--fail-on-skip", action="store_true")
    ap.add_argument("--pattern-self-test", metavar="SAMPLES.json")
    ap.add_argument("--root", default=str(ROOT_DEFAULT))
    ap.add_argument("--patterns", default=str(PATTERNS_DEFAULT))
    ap.add_argument("--config", default=str(CONFIG_DEFAULT))
    ap.add_argument("--json", metavar="OUT.json")
    ap.add_argument("--no-allow", action="store_true")
    try:
        args = ap.parse_args(sys.argv[1:] if argv is None else argv)
    except SystemExit as e:
        return 2 if e.code not in (0, None) else 0
    try:
        pat = load_patterns(args.patterns)
    except FailClosed as e:
        print("PATTERNS UNAVAILABLE: %s" % e)
        return 2
    if args.pattern_self_test:
        return pattern_self_test(pat, args.pattern_self_test)
    try:
        cfg = load_config(args.config)
    except Usage as e:
        print("USAGE: %s" % e)
        return 2
    root = Path(args.root)
    if not root.is_dir():
        print("ENVIRONMENT: the root folder does not exist")
        return 3
    if args.self_test:
        return 0 if self_test(root, pat, args.fail_on_skip) else 1

    try:
        if args.theme:
            label, targets, findings, info, statements = theme_scan(root, cfg, pat, args)
            for f in findings:
                print(f.text())
            for f in statements[:12]:
                print("NOTE    " + f.text()[8:])
            if len(statements) > 12:
                print("NOTE    ... %d more exclusion statements" % (len(statements) - 12))
            print("theme guard: %d file(s) scanned (%s), %d finding(s), %d exclusion statement(s) shown as NOTE" % (len(targets), label, len(findings), len(statements)))
            print("LIMIT: this is a keyword scan of text only. It can NOT judge iconography: a person (and the Fable review) must look at every picture against D-28.")
            if info:
                print("INFO only (existing playbooks, skills and research are never failed): " + ", ".join("%s: %d keyword hit(s)" % (k, v) for k, v in sorted(info.items())))
            if args.json:
                Path(args.json).write_text(json.dumps({"findings": [f.as_dict() for f in findings], "exclusion_statements": [f.as_dict() for f in statements], "info": info}, indent=1), encoding="utf-8")
            return 1 if findings else 0
        mode, files, extra = gather(root, args, pat)
    except Usage as e:
        print("USAGE: %s" % e)
        return 2
    except EnvironmentError as e:
        print("ENVIRONMENT: %s" % e)
        return 3

    lint = Linter(root, pat, cfg, use_allow=not args.no_allow)
    lint.findings.extend(extra)
    for rel, added in files:
        lint.check_file(rel, added)
    ident = [f for f in lint.findings if f.kind in ("identifying", "denylist", "local_deny")]
    other = [f for f in lint.findings if f.kind not in ("identifying", "denylist", "local_deny")]
    for f in ident + other:
        print(f.text())
    for f in lint.notes[:10]:
        print("NOTE    " + f.text()[8:])
    if len(lint.notes) > 10:
        print("NOTE    ... %d more fixture notes" % (len(lint.notes) - 10))
    print("public_lint: mode %s, %d file(s) scanned, %d identifying-data finding(s), %d hygiene finding(s), %d fixture note(s), %d suppressed by the config allow list"
          % (mode, lint.scanned, len(ident), len(other), len(lint.notes), sum(lint.suppressed.values())))
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps({"mode": mode, "scanned": lint.scanned, "identifying": [f.as_dict() for f in ident], "hygiene": [f.as_dict() for f in other],
                                               "notes": len(lint.notes), "suppressed_by_allow": lint.suppressed, "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")}, indent=1), encoding="utf-8")
    if ident:
        return 2
    return 1 if other else 0


if __name__ == "__main__":
    sys.exit(main())
