# r4_photo2vox.py: photo -> 64x36 luminance relief -> MagicaVoxel .vox file (for a Goxel and Blender chain).
# Source: research/toolchain.md, recipe R4. Code verbatim; this header added by the scribe.
# Ran on: Python (version not recorded), Pillow and numpy (versions not recorded), Ubuntu 24.04 sandbox.
#   Date run: 2026-10-18 [RUN]. The chain in the notes was:
#     python3 r4_photo2vox.py scene.jpg scene.vox
#     xvfb-run -a goxel scene.vox --export scene.obj      (Goxel 0.11.0, 0.24 s; xvfb-run is for servers only)
#   Then r4_render_voxel.py in Blender (bpy 5.2.2).
# Caveat: depth comes from brightness, so the result is a crude relief, not a modelled room.
#   Use it as plumbing. For hero objects, hand-model in MagicaVoxel, Goxel or Blockbench (playbook Decision 3).
# Output: .vox, RIFF-style chunks MAIN/SIZE/XYZI/RGBA, version 150 [57]. The file is Z-up.
# Pip: pip install pillow numpy   (TODO(verify on the maker's PC))

import struct, sys, numpy as np
from PIL import Image                                   # pip install pillow
src, out = sys.argv[1:3]; W, H, DEPTH = 64, 36, 16
im = Image.open(src).convert('RGB').resize((W, H), Image.LANCZOS)
q = im.quantize(colors=64, method=Image.MEDIANCUT); pal = q.getpalette()[:64*3]; idx = np.array(q)
lum = np.array(im.convert('L'), dtype=float) / 255.0
# x = image x, z = image row (flipped so the top of the photo is up), y = depth: relief grows toward -y
vox = [(x, DEPTH-1-d, H-1-row, int(idx[row, x]) + 1) for row in range(H) for x in range(W)
       for d in range(1 + int(lum[row, x] * (DEPTH-1)))]          # colour index is 1-based
chunk = lambda cid, c, ch=b'': cid + struct.pack('<ii', len(c), len(ch)) + c + ch
size = chunk(b'SIZE', struct.pack('<iii', W, DEPTH, H))          # x, y (depth), z (up)
xyzi = chunk(b'XYZI', struct.pack('<i', len(vox)) + b''.join(struct.pack('<4B', *v) for v in vox))
rgba = b''.join(bytes((*pal[i*3:i*3+3], 255)) if i < 64 else bytes((0, 0, 0, 255)) for i in range(256))
open(out, 'wb').write(b'VOX ' + struct.pack('<i', 150) + chunk(b'MAIN', b'', size + xyzi + chunk(b'RGBA', rgba)))
