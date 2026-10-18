"""Q1 (follow-up round 1): measure x-height, cap-height and line pitch of ffmpeg `subtitles` FontSize=20/23/26
as a percentage of picture height at 1080p (cross-check 2160p). Usage: python3 -I caption_xheight.py WORKDIR [FONT_FILE FONT_FAMILY_NAME]
Needs ffmpeg with libass, numpy and Pillow. With no font arguments it measures the five fonts named in FONTS (fontconfig, Linux).
With FONT_FILE and FONT_FAMILY_NAME (round 2, for the maker's own caption font, Windows included) it copies the file into WORKDIR/fonts, passes it to libass with
fontsdir=, measures only that font, and checks the result against the font's own metrics (a large gap means libass fell back to another font).
Round 2 change: ffmpeg runs with the working directory set to WORKDIR and relative file names, so a Windows path such as C:\\Users\\... never reaches the
filter string (its colon would break `subtitles=`). Set FFMPEG=C:\\path\\ffmpeg.exe to choose the build. Results for the default fonts are unchanged.
The font-metric cross-check in the notes used fontTools separately (hhea ascender, descender and the glyph height of 'x')."""
import os, sys, subprocess, json, shutil
import numpy as np
from PIL import Image, ImageFont
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
work = os.path.abspath(sys.argv[1])
os.makedirs(work, exist_ok=True)
USER_FONT = None
if len(sys.argv) >= 4:
    os.makedirs(os.path.join(work, "fonts"), exist_ok=True)
    shutil.copyfile(sys.argv[2], os.path.join(work, "fonts", os.path.basename(sys.argv[2])))
    USER_FONT = (sys.argv[3], sys.argv[2])
FONTS = {  # name -> file (for metric lookup only; ffmpeg picks the font by name through fontconfig)
 "DejaVu Sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
 "Liberation Sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
 "Inter": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
 "Carlito": "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
 "FreeSans": "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
}
def render(text_lines, font, size, W, H, tag, extra=""):
    srt = f"{tag}.srt"
    with open(os.path.join(work, srt), "w") as f:
        f.write("1\n00:00:00,000 --> 00:00:01,000\n" + "\n".join(text_lines) + "\n")
    style = f"FontSize={size},Outline=0,Shadow=0,PrimaryColour=&HFFFFFF&,BackColour=&H000000&"
    if font: style = f"FontName={font}," + style
    style += extra
    png = f"{tag}.png"
    # original_size makes libass use the real frame size for the PlayRes mapping only if given; we do NOT give it,
    # so this is the default ffmpeg behaviour that format.md describes (288-line canvas for .srt).
    vf = f"subtitles={srt}" + (":fontsdir=fonts" if USER_FONT else "") + f":force_style='{style}'"
    subprocess.run([FFMPEG,"-v","error","-y","-f","lavfi","-i",f"color=black:s={W}x{H}:d=1:r=1","-vf",vf,"-frames:v","1",png],check=True,cwd=work)
    return np.asarray(Image.open(os.path.join(work, png)).convert("L"),dtype=np.float32)/255.0
def vextent(a):
    """Vertical extent in px, sub-pixel: rows where max coverage>0.5 plus partial edge rows (coverage of the edge row)."""
    prof = a.max(axis=1)
    rows = np.where(prof>0.5)[0]
    top, bot = rows.min(), rows.max()
    # sub-pixel edges from the first partially covered row beyond the thresholded rows
    t = top - prof[top-1] if top>0 else top          # partially covered row above adds its coverage
    b = bot + 1 + prof[bot+1] if bot+1<len(prof) else bot+1  # partially covered row below adds its coverage
    return float(b-t), int(top), int(bot)
def lines_pitch(a):
    prof = (a>0.5).any(axis=1)
    idx = np.where(prof)[0]
    # split into two text blocks at the biggest gap
    gaps = np.diff(idx); k = gaps.argmax()
    return idx[0], idx[k], idx[k+1], idx[-1]
res = []
for font in ([USER_FONT[0]] if USER_FONT else [None] + list(FONTS)):
    for size in (20,23,26):
        for (W,H) in ((1920,1080),(3840,2160)):
            tag = f"{(font or 'default').replace(' ','_')}_{size}_{H}"
            xh = vextent(render(["xxxxxxxxxxxxxxxx"], font, size, W, H, tag+"_x"))[0]
            # x, v, w, z, y are flat-topped; "xvwz" avoids round overshoot of o/e/a/s
            cap = vextent(render(["HHHHHHHHHHHH"], font, size, W, H, tag+"_H"))[0]
            a2 = render(["HHHHHHHH","HHHHHHHH"], font, size, W, H, tag+"_2")
            t1, b1, t2, b2 = lines_pitch(a2)
            pitch = t2 - t1   # baseline-to-baseline pitch of two H lines = top-of-H to top-of-H
            res.append(dict(font=font or "default(fontconfig)", size=size, H=H, xh_px=round(xh,2), xh_pct=round(100*xh/H,2),
                            cap_px=round(cap,2), cap_pct=round(100*cap/H,2), pitch_px=int(pitch), pitch_pct=round(100*pitch/H,2)))
json.dump(res, open(os.path.join(work,"q1_results.json"),"w"), indent=1)
for r in res:
    if r["H"]==1080: print(r)
if USER_FONT:
    # expected x-height % from the font's own metrics: 100 * FontSize / 288 * xHeight / (ascent + descent)   (FQ1 formula; .srt through ffmpeg uses a 288-line canvas)
    big = ImageFont.truetype(USER_FONT[1], 1000)
    asc, desc = big.getmetrics()
    bb = big.getbbox("x"); xh = bb[3] - bb[1]
    for r in res:
        if r["H"] == 1080:
            exp = 100.0 * r["size"] / 288.0 * xh / (asc + desc)
            r["expected_xh_pct"] = round(exp, 2); r["gap_pts"] = round(r["xh_pct"] - exp, 2)
            print(f"FontSize={r['size']}: measured {r['xh_pct']}%  expected from font metrics {exp:.2f}%  gap {r['xh_pct']-exp:+.2f} pts", "(OK)" if abs(r["xh_pct"]-exp) <= 0.25 else "(CHECK: libass may have used a different font)")
    json.dump(res, open(os.path.join(work,"q1_results.json"),"w"), indent=1)
