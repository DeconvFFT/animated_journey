#!/usr/bin/env python3
"""Check a saved copy of the Minecraft Usage Guidelines page against the quotes we rely on.

Usage:  python check_mojang_quotes.py PAGE.html [PAGE2.html ...]

PAGE can be raw HTML (live page, or a Wayback "id_" snapshot) or plain text.
For each file it prints the SHA-256 of the extracted text, then PRESENT or MISSING
for each quote. Exit code 1 if any quote is missing in any file.

Extraction method (fixed on purpose, so hashes are comparable between runs):
  1. drop <script> and <style> blocks, 2. replace block-level tags (p, div, li, br,
  headings, table cells, ...) with a space and delete inline tags (b, a, span, ...)
  without a space, so "big-<b>screen</b>" stays one word, 3. HTML-unescape, 4. turn curly quotes/apostrophes and non-breaking spaces into
  plain ones, 5. collapse all whitespace to single spaces, 6. UTF-8 encode, SHA-256.
Hashes made with other methods (the two in the round-1 excerpt files) will not match.

Quotes are verbatim from research/excerpts/games-round1-followup-2026-10-18.txt and
research/sources/minecraft-usage-guidelines-2026-10-18.txt (captured 2026-10-18).
Standard library only. Run with: python -I check_mojang_quotes.py PAGE.html
"""
import hashlib
import html
import re
import sys

QUOTES = [
    ("personal use", "We are very relaxed about things you create for yourself."),
    ("sharing = commercial", "When you decide to share your content with the community (whether you plan to make money off it or not), you are doing what we consider to be a commercial thing."),
    ("physical locations", "The gameplay is not displayed or projected publicly within physical locations, for example:"),
    ("example 1", "Promoting or advertising big-screen Minecraft gameplay inside any commercial venue like restaurants"),
    ("example 2", "Charging money for Minecraft gameplay, leagues, or competitions in theaters where gameplay is projected onto movie screens"),
    ("free to view", "All videos (in their entirety) are free to view"),
    ("no selling copies", "You don't sell copies of the videos or streams"),
    ("credits outside game", "You place any title card, end credits, sponsorship notices, and other callouts outside of the actual game content."),
    ("150 participants", "The event must be limited to no more than approximately 150 participants"),
    ("no profit sponsors", "You may not accept sponsorships for purposes of profit"),
    ("name not the title", "You may not use the Minecraft name as the primary or dominant name or title."),
    ("change clause", "We reserve the right to change our mind at any time"),
]


def extract(raw: str) -> str:
    s = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", raw)
    s = re.sub(r"(?is)</?(p|div|li|ul|ol|br|h[1-6]|tr|td|th|table|section|article|header|footer|blockquote|hr)\b[^>]*>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    return norm(html.unescape(s))


def norm(s: str) -> str:
    table = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x00A0: " "}
    return re.sub(r"\s+", " ", s.translate(table)).strip()


def main(paths):
    missing_any = False
    for p in paths:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            text = extract(f.read())
        print(f"== {p}")
        print(f"   extracted text: {len(text)} chars, sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()}")
        for label, q in QUOTES:
            ok = norm(q) in text
            missing_any |= not ok
            print(f"   {'PRESENT' if ok else 'MISSING'}  {label}")
    return 1 if missing_any else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
