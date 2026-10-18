import sys, os, numpy as np
from PIL import Image
out = sys.argv[1]
rng = np.random.default_rng(1)
def noise(h, w): return rng.integers(0, 256, size=(h, w), dtype=np.uint8)
def smooth(h, w):
    y = np.linspace(0, 255, h, dtype=np.float32)[:, None]
    x = np.linspace(0, 255, w, dtype=np.float32)[None, :]
    return ((x + y) / 2).astype(np.uint8)
def save(name, arr, comp, rps):
    im = Image.fromarray(arr, "L")
    p = os.path.join(out, name)
    kw = {}
    if comp: kw["compression"] = comp
    im.save(p, tiffinfo={278: rps}, **kw)
    with Image.open(p) as t:
        tags = t.tag_v2
        counts = tags.get(279)
        print(name, "size", os.path.getsize(p), "rps", tags.get(278), "strips", len(counts), "max strip bytes", max(counts), "comp", tags.get(259))
H = W = 12000
a = noise(H, W)
save("unc_single_noise_12000sq.tif", a, None, H)
save("unc_rps64_noise_12000sq.tif", a, None, 64)
save("deflate_single_noise_12000sq.tif", a, "tiff_adobe_deflate", H)
save("deflate_rps64_noise_12000sq.tif", a, "tiff_adobe_deflate", 64)
b = smooth(H, W)
save("lzw_single_smooth_12000sq.tif", b, "tiff_lzw", H)
save("deflate_single_smooth_12000sq.tif", b, "tiff_adobe_deflate", H)
save("unc_single_smooth_12000sq.tif", b, None, H)
# boundary: exactly 128 MiB and one row more
save("unc_single_exact_16384x8192.tif", noise(8192, 16384), None, 8192)
save("unc_single_plusrow_16384x8193.tif", noise(8193, 16384), None, 8193)
