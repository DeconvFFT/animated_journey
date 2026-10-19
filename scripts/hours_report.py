#!/usr/bin/env python3
"""hours_report.py - weekly totals from the maker's hours log (ops/hours.csv).

WHAT IT DOES
  Reads the hours log, checks every row, adds up the maker's minutes per week and per
  activity, and prints an INDICATIVE reading of the runtime rule W-02. It is read-only:
  it never writes, moves or deletes anything, and it never prints the `note` column.

HOW TO RUN (Python 3 standard library only; use -I so no stray module is picked up)
  python3 -I scripts/hours_report.py ops/hours.csv
  python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19
  python3 -I scripts/hours_report.py ops/hours.csv --week-start 2026-10-19 --json
  Windows: py -3 -I scripts\\hours_report.py ops\\hours.csv --week-start 2026-10-19
  (UNVERIFIED on Windows: only run on Linux here; the code is plain standard-library Python.)

  --week-start DATE   report one window of --days days (default 7) starting on DATE
                      (a Monday gives Monday to Sunday, the calendar of ROADMAP.md).
                      Without it, every Monday-start week that has rows is reported.
  --days N            window length for --week-start (default 7)
  --json              print the result as one JSON object instead of text

WHAT IT PRINTS
  Per week: total hours, hours by activity, and the W-02 reading. `who` must be `maker` or
  `agent` (nothing else is accepted: in a public repository a `who` column is a name slot).
  Only `maker` rows count towards the maker's hours (H); `agent` rows are listed as not counted.
  Problems are printed with the file line number and nothing else is reported. Free text
  echoed in a problem (activity, shot_or_chapter, who) is masked: first two characters, then
  asterisks, because a mistyped column may hold a name.

THE W-02 READING (DECISIONS.md W-02; always printed as indicative)
  under 8 h          : the 6-minute F-0 would become the plan on Sun 1 Nov, 9 the stretch
  8 h to under 14 h  : plan 9 minutes
  14 h to under 16 h : 12 minutes only if hours are added or captions bought, else 9
  16 h or more       : plan 12 minutes
  The maker's reliable-hours number in writing (O-01) decides, not this report.

EXIT CODES (build plan 4.3)
  0 all rows valid (or no rows yet); 1 a row or the header is invalid (line numbers
  printed); 2 bad usage or an unreadable file.

PRIVACY (D-26: the repository is public)
  The note column is never printed. Only the file's base name is printed, never a
  directory path, so a profile folder can not leak into pasted output.
"""
import argparse
import csv
import datetime
import io
import json
import os
import re
import sys

HEADER = ["date", "shot_or_chapter", "activity", "minutes", "who", "note"]
ACTIVITIES = [
    "gather", "scan", "story", "brief_G0", "style_G1", "review_G2", "craft_refine_G3",
    "chapter_G4", "dignity_G5", "tech_G6", "sound", "grade", "mix", "captions", "master",
    "qc", "admin", "learn", "rework", "event",
]
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
MAKER = "maker"
WHO_VALUES = ("maker", "agent")  # a `who` column in a public repository is a name slot: two words only
# W-02 thresholds, in minutes of one week (8 h, 14 h, 16 h).
F0_BELOW = 8 * 60
NINE_BELOW = 14 * 60
TWELVE_AT = 16 * 60
INDICATIVE = ("indicative only: this is one logged window; the maker's reliable-hours "
              "number in writing (O-01, due Sun 25 Oct, Sun 15 Nov at the latest) decides")


def reading(minutes):
    """Return the W-02 reading for one week's maker minutes."""
    if minutes < F0_BELOW:
        return ("under about 8 hours: the 6-minute F-0 would become the plan on Sun 1 Nov "
                "and 9 minutes the stretch (W-02)")
    if minutes < NINE_BELOW:
        return "8 to under 14 hours: plan 9 minutes (W-02)"
    if minutes < TWELVE_AT:
        return ("14 to under 16 hours: 12 minutes only if you add hours or buy captions; "
                "otherwise 9 minutes (W-02)")
    return "16 hours or more: plan 12 minutes (W-02)"


def hours_text(minutes):
    """Minutes as hours with one decimal, rounded half up (570 -> 9.5, 575 -> 9.6)."""
    tenths = (minutes * 10 + 30) // 60
    return "%d.%d" % (tenths // 10, tenths % 10)


def read_text(path):
    """Read a CSV file as text. Handles UTF-8 (with or without BOM) and UTF-16 with BOM,
    which Windows tools write; falls back to Windows-1252 and says so."""
    with open(path, "rb") as fh:
        raw = fh.read()
    note = None
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16"), "UTF-16 with BOM"
    if raw[:3] == b"\xef\xbb\xbf":
        return raw[3:].decode("utf-8"), "UTF-8 with BOM"
    try:
        return raw.decode("utf-8"), note
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace"), "Windows-1252 (not UTF-8)"


def parse(text):
    """Return (rows, problems). rows: list of (line, dict). problems: list of (line, msg).
    Line numbers are physical file lines (header is line 1)."""
    rows, problems = [], []
    reader = csv.reader(io.StringIO(text, newline=""))
    last = 0
    first = True
    try:
        for rec in reader:
            start = last + 1
            last = reader.line_num
            if first:
                first = False
                cells = [c.strip() for c in rec]
                if cells != HEADER:
                    hint = ""
                    if len(cells) == 1 and ";" in cells[0]:
                        hint = " (this looks semicolon-separated: save as CSV, comma delimited)"
                    problems.append((start, "header must be exactly: " + ",".join(HEADER)
                                     + " (found: " + ",".join(cells)[:120] + ")" + hint))
                    return rows, problems
                continue
            if not any(c.strip() for c in rec):
                continue  # blank line or ",,,,,": spreadsheets add these
            if len(rec) != len(HEADER):
                problems.append((start, "expected %d columns, found %d (a comma inside "
                                 "note? remove it or put the note in quotes)"
                                 % (len(HEADER), len(rec))))
                continue
            row = dict(zip(HEADER, [c.strip() for c in rec]))
            probs = check_row(row)
            for msg in probs:
                problems.append((start, msg))
            if not probs:
                rows.append((start, row))
    except csv.Error as exc:
        problems.append((reader.line_num or 1, "not readable as CSV: %s" % exc))
    if first:
        problems.append((1, "the file is empty: the header line is missing"))
    return rows, problems


def masked(value):
    """First two characters, then asterisks: free text echoed in a message may be a name."""
    value = value[:40]
    return value[:2] + "*" * min(max(len(value) - 2, 0), 10)


def check_row(row):
    msgs = []
    d = row["date"]
    if not DATE_RE.match(d):
        msgs.append("date '%s' must look like 2026-10-19 (year-month-day; a spreadsheet may "
                    "have changed it: format the column as Text)" % d[:20])
    else:
        try:
            datetime.date.fromisoformat(d)
        except ValueError:
            msgs.append("date '%s' is not a real calendar date" % d)
    s = row["shot_or_chapter"]
    if s != "-" and not ID_RE.match(s):
        msgs.append("shot_or_chapter '%s' must be an ID such as C01 or LJ-C01-S002, or '-' "
                    "until shots exist" % masked(s))
    a = row["activity"]
    if a not in ACTIVITIES:
        hint = ""
        for cand in ACTIVITIES:
            if cand.lower() == a.lower():
                hint = " (activity words are lower-case except the G-codes: did you mean '%s'?)" % cand
        msgs.append("activity '%s' is not one of: %s%s" % (masked(a), "|".join(ACTIVITIES), hint))
    m = row["minutes"]
    if not re.match(r"^[0-9]{1,4}$", m) or not (1 <= int(m) <= 1440):
        msgs.append("minutes '%s' must be a whole number from 1 to 1440 (no 'h', no decimals)" % m[:12])
    if row["who"] not in WHO_VALUES:
        msgs.append("who '%s' must be exactly maker or agent (the repository is public: no names here)"
                    % (masked(row["who"]) if row["who"] else ""))
    return msgs


def monday_of(d):
    return d - datetime.timedelta(days=d.weekday())


def summarise(rows, start, days):
    """Rows (line, dict) -> summary for the window [start, start+days)."""
    end = start + datetime.timedelta(days=days)
    by_act, day_set = {}, set()
    maker_min = other_min = in_window = 0
    for _line, row in rows:
        d = datetime.date.fromisoformat(row["date"])
        if not (start <= d < end):
            continue
        in_window += 1
        mins = int(row["minutes"])
        if row["who"] == MAKER:
            maker_min += mins
            by_act[row["activity"]] = by_act.get(row["activity"], 0) + mins
            day_set.add(d)
        else:
            other_min += mins
    return {
        "window_start": start.isoformat(),
        "window_end_inclusive": (end - datetime.timedelta(days=1)).isoformat(),
        "weekday_of_start": start.strftime("%a"),
        "rows_in_window": in_window,
        "maker_minutes": maker_min,
        "maker_hours": hours_text(maker_min),
        "days_with_rows": len(day_set),
        "by_activity_minutes": {k: by_act[k] for k in ACTIVITIES if k in by_act},
        "not_counted_minutes": other_min,
        "reading": reading(maker_min) if in_window else None,
    }


def format_window(s):
    lines = []
    lines.append("Window %s (%s) to %s" % (s["window_start"], s["weekday_of_start"],
                                          s["window_end_inclusive"]))
    if s["rows_in_window"] == 0:
        lines.append("  no rows in this window")
        return lines
    lines.append("  total: %s h (%d minutes) over %d day(s) with rows"
                 % (s["maker_hours"], s["maker_minutes"], s["days_with_rows"]))
    for act, mins in s["by_activity_minutes"].items():
        lines.append("    %-16s %6s h" % (act, hours_text(mins)))
    if s["not_counted_minutes"]:
        lines.append("  not counted (who is not '%s'): %d minutes" % (MAKER, s["not_counted_minutes"]))
    lines.append("  reading: " + s["reading"])
    lines.append("  " + INDICATIVE)
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Weekly totals from ops/hours.csv (read-only).")
    ap.add_argument("csv_path", help="the hours log, normally ops/hours.csv")
    ap.add_argument("--week-start", help="first day of the window, YYYY-MM-DD (a Monday gives Mon-Sun)")
    ap.add_argument("--days", type=int, default=7, help="window length in days (default 7)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = ap.parse_args(argv)

    if args.days < 1 or args.days > 366:
        ap.error("--days must be between 1 and 366")
    start = None
    if args.week_start:
        if not DATE_RE.match(args.week_start):
            ap.error("--week-start must look like 2026-10-19")
        try:
            start = datetime.date.fromisoformat(args.week_start)
        except ValueError:
            ap.error("--week-start is not a real calendar date")
    try:
        text, enc_note = read_text(args.csv_path)
    except OSError as exc:
        print("hours_report: cannot read %s (%s)" % (os.path.basename(args.csv_path), exc.strerror),
              file=sys.stderr)
        return 2

    name = os.path.basename(args.csv_path)
    rows, problems = parse(text)
    if problems:
        print("%s: %d problem(s); nothing is reported until they are fixed" % (name, len(problems)))
        for line, msg in problems:
            print("  line %d: %s" % (line, msg))
        return 1

    windows = []
    if start is not None:
        windows.append(summarise(rows, start, args.days))
    else:
        mondays = sorted({monday_of(datetime.date.fromisoformat(r["date"])) for _l, r in rows})
        for mon in mondays:
            windows.append(summarise(rows, mon, 7))

    result = {"file": name, "rows": len(rows), "encoding_note": enc_note, "windows": windows,
              "indicative": INDICATIVE}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print("hours_report: %s, %d row(s)" % (name, len(rows)))
    if enc_note:
        print("  note: file read as %s" % enc_note)
    if not rows:
        print("  no rows yet: log your real hours (see HOURS-HOWTO.md); the first logged week is read on Sun 1 Nov")
        return 0
    if start is not None and windows[0]["rows_in_window"] == 0:
        print("  %d row(s) exist, but none falls in the window below" % len(rows))
    for w in windows:
        for line in format_window(w):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
