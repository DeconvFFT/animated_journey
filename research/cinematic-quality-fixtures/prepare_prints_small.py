"""Round 2: fetch only the two small Smithsonian Open Access (CC0) prints from prepare_prints.py (p2, p3), skipping the large LoC TIFF.
Run:  python3 -I prepare_prints_small.py WORKDIR     (writes WORKDIR/src/p2_small_bw_{4k,1080}.png and p3_soft_group_{4k,1080}.png)
Same crops as prepare_prints.py. Archival images, used only for measurement, not redistributed."""
import sys, os, urllib.request, io
from PIL import Image
work = sys.argv[1]; os.makedirs(os.path.join(work, "src"), exist_ok=True)
def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "lj-research/1.0"}), timeout=300).read()
def mk(name, im, box):
    for tag, (w, h) in (("4k", (3840, 2160)), ("1080", (1920, 1080))):
        im.resize((w, h), Image.LANCZOS, box=box).save(os.path.join(work, "src", f"{name}_{tag}.png"), compress_level=3)
mk("p2_small_bw", Image.open(io.BytesIO(fetch("https://ids.si.edu/ids/deliveryService?id=NMAAHC-2011_36_119_001&max=6000"))).convert("RGB"), (560, 740, 2640, 1910))
mk("p3_soft_group", Image.open(io.BytesIO(fetch("https://ids.si.edu/ids/deliveryService?id=NMAAHC-2013_244_36_001&max=6000"))).convert("RGB"), (250, 700, 2760, 2112))
print("ok")
