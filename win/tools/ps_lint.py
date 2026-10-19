#!/usr/bin/env python3
"""ps_lint.py: a conservative PowerShell 5.1-compatibility and read-only lint (standard library only).

WHAT IT DOES
  Reads .ps1 files and the ```powershell fences of .md files, blanks out comments and string contents,
  and checks what is left against the project's rules (build plan 4.7):
    * syntax Windows PowerShell 5.1 does not have: ??, ??=, ?., ?[ ], ternary, && and || chains,
      ForEach-Object -Parallel, -AsHashtable, -AsByteStream, -Encoding utf8NoBOM/utf8BOM, $IsWindows and
      friends without a Get-Variable guard, ConvertFrom-Json -Depth, Join-Path with 3 or more positional
      arguments, a few PowerShell 7-only cmdlets and switches;
    * ConvertTo-Json without -Depth 6 or more;
    * Set-ExecutionPolicy at any scope except Process (machine, user and policy scopes, or no scope, are errors);
    * non-ASCII characters in a .ps1 file (Windows PowerShell 5.1 reads a BOM-less file as ANSI);
    * (default, "read-only" mode) cmdlets that write, delete, install, download or change settings, and
      anything that asks for administrator rights. Use --allow-write for a script whose name says it writes.
  Redirection (> and >>) is a warning: Windows PowerShell 5.1 writes UTF-16 with a BOM that way.
  It is a safety net, not a proof: a parse by pwsh (ps_parse.sh) and the maker's first run are the proof.

USAGE
  python3 -I win/tools/ps_lint.py [--allow-write] FILE [FILE ...]      (.ps1 or .md)
EXIT CODES  0 no errors (warnings allowed), 1 at least one error, 2 bad usage or unreadable file.
Windows behaviour is UNVERIFIED until the maker's first real run.
"""
import re
import sys

JSON_DEPTH_MIN = 6

FORBIDDEN_7ONLY = [
    (r"(?<![\w-])-Parallel\b", "R05", "ForEach-Object -Parallel does not exist in Windows PowerShell 5.1"),
    (r"(?<![\w-])-AsHashtable\b", "R06", "-AsHashtable (ConvertFrom-Json) is PowerShell 6+"),
    (r"(?<![\w-])-AsByteStream\b", "R07", "-AsByteStream (Get-Content) is PowerShell 6+; use -Encoding Byte only in 5.1-specific code"),
    (r"(?i)-Encoding\s+['\"]?utf8NoBOM\b", "R09", "-Encoding utf8NoBOM is PowerShell 6+; write with [System.IO.File]::WriteAllText and UTF8Encoding($false)"),
    (r"(?i)-Encoding\s+['\"]?utf8BOM\b", "R09", "-Encoding utf8BOM is PowerShell 6+"),
    (r"(?i)\bConvertFrom-Json\b[^|\n]*\s-Depth\b", "R10", "ConvertFrom-Json -Depth is PowerShell 6.2+"),
    (r"(?i)\bConvertTo-Json\b[^|\n]*\s-EnumsAsStrings\b", "R10", "-EnumsAsStrings is PowerShell 7+"),
    (r"(?i)\bTest-Json\b", "R10", "Test-Json is PowerShell 6.1+"),
    (r"(?i)\bJoin-String\b", "R10", "Join-String is PowerShell 7+"),
    (r"(?i)\bGet-Error\b", "R10", "Get-Error is PowerShell 7+"),
    (r"\$PSStyle\b", "R10", "$PSStyle is PowerShell 7.2+"),
    (r"(?i)\bSplit-Path\b[^|\n]*\s-LeafBase\b", "R10", "Split-Path -LeafBase is PowerShell 6+"),
    (r"(?i)-SkipCertificateCheck\b", "R10", "-SkipCertificateCheck is PowerShell 6+ (and unsafe)"),
    (r"(?i)\[Environment\]::ProcessPath\b", "R10", "ProcessPath needs .NET 6; not in Windows PowerShell 5.1"),
    (r"(?i)-ThrottleLimit\b", "R10", "-ThrottleLimit with ForEach-Object is PowerShell 7+"),
]

IS_VARS = re.compile(r"\$Is(Windows|Linux|MacOS|CoreCLR)\b")

READONLY_BANNED = [
    (r"(?i)\bRemove-Item\b|\bRemove-ItemProperty\b|\bClear-Content\b|\bClear-ItemProperty\b|\brmdir\b|\bdel\s", "delete", "deletes files or settings"),
    (r"(?i)\bSet-ItemProperty\b|\bNew-ItemProperty\b|\bSet-Content\b|\bAdd-Content\b|\bOut-File\b|\bMove-Item\b|\bRename-Item\b|\bCopy-Item\b", "write", "writes or moves files or registry values"),
    (r"(?i)\bInvoke-WebRequest\b|\bInvoke-RestMethod\b|\bStart-BitsTransfer\b|\bcurl\b|\bwget\b|\bNew-Object\s+(System\.)?Net\.WebClient\b", "network", "uses the network"),
    (r"(?i)\bInstall-(Module|Package|Script|WindowsFeature|Module)\b|\bwinget\s+(install|upgrade|uninstall)\b|\bchoco\b|\bmsiexec\b|\bscoop\s+install\b", "install", "installs or upgrades software"),
    (r"(?i)\b(Set|Stop|Start|Restart|New|Remove)-Service\b|\bStop-Process\b|\bRegister-ScheduledTask\b|\bschtasks\b|\bEnable-\w+|\bDisable-\w+|\bSet-NetFirewall\w*|\bnetsh\b|\breg\s+(add|delete|import)\b|\bbcdedit\b|\bSet-MpPreference\b", "settings", "changes a service, process, task or system setting"),
    (r"(?i)-Verb\s+['\"]?RunAs\b|#requires\s+-RunAsAdministrator", "admin", "asks for administrator rights"),
    (r"(?i)\bInvoke-Expression\b|(?<![\w-])iex\b", "eval", "runs text as code"),
    (r"(?i)\bGet-Credential\b|\bConvertTo-SecureString\b", "secret", "handles credentials"),
]


def _hide(chunk):
    """Hide the inside of a string: keep newlines, replace everything else with x."""
    return "".join(ch if ch == "\n" else "x" for ch in chunk)


def blank_code(text):
    """Return text with comments blanked and string contents replaced by x (newlines and length kept), so the
    rules only see code. A string keeps its quote marks, so it still counts as one token."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if c == "<" and nxt == "#":
            j = text.find("#>", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in text[i:j]))
            i = j
        elif c == "#":
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif c == "@" and nxt in "'\"" and re.match(r"[ \t]*\r?\n", text[i + 2:i + 40] or ""):
            q = nxt
            m = re.search(r"\n" + re.escape(q) + "@", text[i + 2:])
            j = n if not m else i + 2 + m.end()
            out.append(q + _hide(text[i + 1:j - 1]) + q if j - i > 2 else text[i:j])
            i = j
        elif c == "'":
            j = i + 1
            while j < n:
                if text[j] == "'":
                    if j + 1 < n and text[j + 1] == "'":
                        j += 2
                        continue
                    break
                j += 1
            j = min(n, j + 1)
            out.append("'" + _hide(text[i + 1:j - 1]) + "'" if j - i >= 2 else text[i:j])
            i = j
        elif c == '"':
            j = i + 1
            while j < n:
                if text[j] == "`":
                    j += 2
                    continue
                if text[j] == '"':
                    if j + 1 < n and text[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            j = min(n, j + 1)
            out.append('"' + _hide(text[i + 1:j - 1]) + '"' if j - i >= 2 else text[i:j])
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def join_path_arg_count(code, start):
    """Count positional arguments of a Join-Path command starting right after the cmdlet name."""
    i, n = start, len(code)
    depth = 0
    positional = 0
    expect_value_for_named = False
    tokens = 0
    while i < n:
        c = code[i]
        if c == "\n" and depth == 0:
            break
        if depth == 0 and c in ";|":
            break
        if depth == 0 and c == ")":
            break
        if c.isspace() and depth == 0:
            i += 1
            continue
        # read one token
        j = i
        d = 0
        while j < n:
            cj = code[j]
            if cj in "([{":
                d += 1
            elif cj in ")]}":
                if d == 0:
                    break
                d -= 1
            elif d == 0 and (cj.isspace() or cj in ";|"):
                break
            j += 1
        tok = code[i:j]
        i = j
        if not tok:
            break
        if tok.startswith("-") and re.match(r"-[A-Za-z]", tok):
            expect_value_for_named = True
            continue
        if expect_value_for_named:
            expect_value_for_named = False
            continue
        positional += 1
    return positional


def lint_text(name, text, allow_write, is_ps1, line_offset=0):
    errs, warns = [], []
    if is_ps1:
        for ln, line in enumerate(text.split("\n"), 1):
            for ch in line:
                if ord(ch) > 127:
                    errs.append((ln + line_offset, "R14", "non-ASCII character: Windows PowerShell 5.1 reads a BOM-less file as ANSI and garbles it (use ASCII only, or save with a BOM)"))
                    break
    code = blank_code(text)
    lines = code.split("\n")
    orig_lines = text.split("\n")
    for ln, line in enumerate(lines, 1):
        L = ln + line_offset
        orig = orig_lines[ln - 1] if ln - 1 < len(orig_lines) else line
        if re.search(r"\?\?=?", line):
            errs.append((L, "R01", "null-coalescing ?? / ??= is PowerShell 7+"))
        if re.search(r"\?\.\s*[A-Za-z_$]|\?\[", line):
            errs.append((L, "R02", "null-conditional ?. / ?[ ] is PowerShell 7+"))
        if re.search(r"(?<!\|)\s\?\s+(?!\{)[^|{}]*\s:\s", line) and not re.search(r"\|\s*\?\s", line):
            errs.append((L, "R03", "ternary ? : is PowerShell 7+ (use if/else)"))
        if re.search(r"&&|\|\|", line):
            errs.append((L, "R04", "pipeline chain operator && or || is PowerShell 7+"))
        for rx, rid, msg in FORBIDDEN_7ONLY:
            # -Encoding takes its value as a string, which the blanked copy hides: read the original line for that one rule
            subject = orig if (rid == "R09" and "-Encoding" in line) else line
            if re.search(rx, subject):
                errs.append((L, rid, msg))
        if IS_VARS.search(line) and "Get-Variable" not in line:
            errs.append((L, "R08", "$IsWindows / $IsLinux / $IsMacOS are undefined in 5.1; test $env:OS -eq 'Windows_NT' or guard with Get-Variable"))
        for m in re.finditer(r"(?i)\bConvertTo-Json\b", line):
            tail = line[m.end():]
            d = re.search(r"(?i)-Depth\s+(\d+)", tail)
            head = line[:m.start()]
            if not d:
                d = re.search(r"(?i)-Depth\s+(\d+)", lines[ln - 1])
            if not d or int(d.group(1)) < JSON_DEPTH_MIN:
                errs.append((L, "R11", "ConvertTo-Json needs -Depth %d or more (the default depth truncates nested data)" % JSON_DEPTH_MIN))
        for m in re.finditer(r"(?i)\bJoin-Path\b", line):
            # statement may continue on the same line only; the project style is two arguments per call
            cnt = join_path_arg_count(line, m.end())
            if cnt >= 3:
                errs.append((L, "R12", "Join-Path with 3 or more positional arguments is PowerShell 6+; nest two calls"))
        for m in re.finditer(r"(?i)\bSet-ExecutionPolicy\b", line):
            stmt = orig[m.end():]
            sc = re.search(r"(?i)-Scope\s+['\"]?(\w+)", stmt)
            if not sc:
                errs.append((L, "R13", "Set-ExecutionPolicy without -Scope Process changes machine policy (needs admin and is not allowed)"))
            elif sc.group(1).lower() != "process":
                errs.append((L, "R13", "Set-ExecutionPolicy -Scope %s is not allowed; only -Scope Process (this window only)" % sc.group(1)))
        if re.search(r"(?<![<>=-])\s>>?\s*[^=\s]", line) and not re.search(r"-(gt|lt|ge|le)\b", line):
            warns.append((L, "W01", "redirection > or >>: Windows PowerShell 5.1 writes UTF-16 with a BOM; write with [System.IO.File]::WriteAllText"))
        if not allow_write:
            for rx, rid, msg in READONLY_BANNED:
                if re.search(rx, line):
                    errs.append((L, "RO-" + rid, "read-only script: " + msg))
    # the cmdlet Set-ExecutionPolicy mentioned inside a comment-only context is ignored (comments are blanked)
    return errs, warns


def fences(md_text):
    """Yield (first_line_number, text) for each ```powershell fence."""
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*```\s*(powershell|pwsh|ps1)\s*$", lines[i], re.I)
        if m:
            start = i + 2
            body = []
            i += 1
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                body.append(lines[i])
                i += 1
            yield start - 1, "\n".join(body)
        i += 1


def main(argv):
    allow_write = False
    files = []
    for a in argv:
        if a == "--allow-write":
            allow_write = True
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("--"):
            print("ps_lint: unknown option %s" % a, file=sys.stderr)
            return 2
        else:
            files.append(a)
    if not files:
        print("usage: ps_lint.py [--allow-write] FILE [FILE ...]", file=sys.stderr)
        return 2
    total_err = total_warn = 0
    for f in files:
        try:
            text = open(f, encoding="utf-8").read()
        except (OSError, UnicodeError):
            print("ps_lint: cannot read %s" % f, file=sys.stderr)
            return 2
        results = []
        if f.lower().endswith(".md"):
            n = 0
            for first, body in fences(text):
                n += 1
                results.append(lint_text(f, body, allow_write, False, first - 1))
            label = "%s (%d powershell fence(s))" % (f, n)
        else:
            results.append(lint_text(f, text, allow_write, True))
            label = f
        e = [x for r in results for x in r[0]]
        w = [x for r in results for x in r[1]]
        for ln, rid, msg in sorted(e):
            print("%s:%d: error [%s] %s" % (f, ln, rid, msg))
        for ln, rid, msg in sorted(w):
            print("%s:%d: warning [%s] %s" % (f, ln, rid, msg))
        print("%s: %d error(s), %d warning(s)" % (label, len(e), len(w)))
        total_err += len(e)
        total_warn += len(w)
    print("TOTAL: %d error(s), %d warning(s) in %d file(s)" % (total_err, total_warn, len(files)))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
