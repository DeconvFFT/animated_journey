"""Prepare the three public-domain scanned prints used in M-C7b (follow-up round 1) and the pan validation.
Run from an empty work directory:  python3 -I prepare_prints.py WORKDIR
Downloads (needs network):
  p1 faded colour  : Library of Congress, 'South of India. Women Grinding and Children', photochrom print ca. 1890-1910 (Photoglob),
                     https://www.loc.gov/item/2017657625/  master TIFF https://tile.loc.gov/storage-services/master/pnp/ppmsca/41400/41470u.tif
                     LoC rights statement read 2026-10-18: "No known restrictions on publication."
  p2 small b/w     : Smithsonian NMAAHC 'Photograph of A. J. Wiseman', ca. 1895, albumen print on a card mount (11.1 x 8.6 cm), Open Access CC0,
                     https://ids.si.edu/ids/deliveryService?id=NMAAHC-2011_36_119_001&max=6000
  p3 soft group    : Smithsonian NMAAHC 'Albumen print of U. S. Colored Troops at Ft. Douglas', 1896-1899 (9.5 x 11.8 cm), Open Access CC0,
                     https://ids.si.edu/ids/deliveryService?id=NMAAHC-2013_244_36_001&max=6000
Each is cropped to 16:9 around the print area and resampled (Lanczos) to 3840x2160 ('_4k') and 1920x1080 ('_1080').
Native pixels in the crop: p1 6400x3600 (real 4K detail), p2 2080x1170 and p3 2510x1412 (so their 4K files are 1.5-1.8x up-samples).
Personal material is never used; these are archival images used only for measurement and are not redistributed."""
import sys, os, urllib.request, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
work = sys.argv[1]; os.makedirs(os.path.join(work, "src"), exist_ok=True)
def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "lj-research/1.0"}), timeout=300).read()
def mk(name, im, box):
    for tag, (w, h) in (("4k", (3840, 2160)), ("1080", (1920, 1080))):
        im.resize((w, h), Image.LANCZOS, box=box).save(os.path.join(work, "src", f"{name}_{tag}.png"), compress_level=3)
mk("p1_faded_colour", Image.open(io.BytesIO(fetch("https://tile.loc.gov/storage-services/master/pnp/ppmsca/41400/41470u.tif"))).convert("RGB"), (700, 1700, 7100, 5300))
mk("p2_small_bw", Image.open(io.BytesIO(fetch("https://ids.si.edu/ids/deliveryService?id=NMAAHC-2011_36_119_001&max=6000"))).convert("RGB"), (560, 740, 2640, 1910))
mk("p3_soft_group", Image.open(io.BytesIO(fetch("https://ids.si.edu/ids/deliveryService?id=NMAAHC-2013_244_36_001&max=6000"))).convert("RGB"), (250, 700, 2760, 2112))
