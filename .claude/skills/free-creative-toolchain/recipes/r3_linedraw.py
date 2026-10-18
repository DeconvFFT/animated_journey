# r3_linedraw.py: SVG line-draw reveal. One SVG per frame, dash offset from full path length to 0.
# Source: research/toolchain.md, recipe R3. Python code verbatim; this header and the render lines added by the scribe.
# Ran on: svgpathtools (version not recorded in the notes), librsvg rsvg-convert 2.58.0, ffmpeg 6.1.1,
#   Ubuntu 24.04 sandbox. Date run: 2026-10-18 [RUN]: 48 frames at 1280 px rendered in 1.9 s.
# Trap: librsvg 2.58 ignored pathLength="1", so every frame looked finished. The real length L is computed
#   from d below. Never type L in by hand.
# Set d to the path's d= attribute copied from Inkscape (XML editor, Ctrl+Shift+X).
# Run:    python3 r3_linedraw.py          (writes frames/f_0000.svg ... f_0047.svg in the current folder)
# Then render PNGs and encode: see the commented bash lines at the end (run from the same folder, tested).
# Windows: the PowerShell frame-render loop is in the playbook (Exercise 6), TODO(verify on the maker's PC).

import os
from svgpathtools import parse_path
os.makedirs('frames', exist_ok=True)
d = "M 60 300 C 140 80, 240 80, 300 200 S 460 330, 580 60"   # copy the path's d= from Inkscape (XML editor, Ctrl+Shift+X)
L = parse_path(d).length(); n = 48
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 640 360">
<rect width="640" height="360" fill="#f7f1e3"/>
<path d="%s" fill="none" stroke="#222" stroke-width="6" stroke-linecap="round"
 stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f"/></svg>'''
ease = lambda t: t*t*(3-2*t)                                   # smoothstep ease in-out
for i in range(n):
    open('frames/f_%04d.svg' % i, 'w').write(svg % (d, L, L, L*(1-ease(i/(n-1)))))

# --- render and encode (bash, as tested in the notes; run after the Python above) ---
# for f in frames/f_*.svg; do rsvg-convert -w 1280 "$f" -o "${f%.svg}.png"; done   # or: inkscape --export-type=png --export-width=1280 --export-filename=x.png f.svg
# ffmpeg -framerate 24 -i frames/f_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p linedraw.mp4
