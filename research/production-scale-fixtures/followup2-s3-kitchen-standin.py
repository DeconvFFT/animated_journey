"""
Spike S3, round 2: a STAND-IN stylised voxel kitchen, built only from primitives.
It contains no photographs, no family imagery and no real textures.
It is NOT the maker's real kitchen set (that set does not exist yet; the vertical
slice C01 builds it). It is the closest honest thing we can time today.

Usage (bpy 5.2.2 LTS from PyPI in a venv):
  python followup2-s3-kitchen-standin.py -- OUT_DIR WIDTH HEIGHT SAMPLES DENOISE(0/1) ADAPTIVE(0/1) [save_blend]

Prints one line:  RESULT w h samples denoise adaptive wall_s render_s peak_rss_mb
"""
import bpy, bmesh, sys, time, os, math, resource
from mathutils import Vector, Euler

args = sys.argv[sys.argv.index("--") + 1:]
OUT, W, H, SAMPLES, DEN, ADA = args[0], int(args[1]), int(args[2]), int(args[3]), args[4] == "1", args[5] == "1"
SAVE_BLEND = len(args) > 6 and args[6] == "save_blend"
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def mat(name, rgb, rough=0.6, metal=0.0, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


M = {
    "floorA": mat("floorA", (0.80, 0.62, 0.40), 0.18),
    "floorB": mat("floorB", (0.55, 0.38, 0.24), 0.18),
    "wall": mat("wall", (0.86, 0.80, 0.68), 0.85),
    "cab": mat("cab", (0.30, 0.52, 0.55), 0.45),
    "top": mat("top", (0.92, 0.90, 0.85), 0.20),
    "wood": mat("wood", (0.50, 0.30, 0.16), 0.55),
    "chair": mat("chair", (0.72, 0.25, 0.20), 0.55),
    "metal": mat("metal", (0.85, 0.85, 0.88), 0.25, 1.0),
    "fruitR": mat("fruitR", (0.8, 0.1, 0.08), 0.35),
    "fruitY": mat("fruitY", (0.95, 0.75, 0.1), 0.35),
    "leaf": mat("leaf", (0.15, 0.55, 0.18), 0.7),
    "pot": mat("pot", (0.65, 0.35, 0.22), 0.8),
    "rug": mat("rug", (0.78, 0.30, 0.34), 0.95),
    "sky": mat("sky", (1, 1, 1), 1.0, 0.0, (0.75, 0.88, 1.0), 6.0),
    "lamp": mat("lamp", (1, 1, 1), 0.5, 0.0, (1.0, 0.85, 0.6), 40.0),
}

# --- one mesh per material, made of many unit cubes (the voxel look) -------------
meshes = {}


def box(key, x0, y0, z0, x1, y1, z1):
    if key not in meshes:
        meshes[key] = bmesh.new()
    bm = meshes[key]
    sx, sy, sz = x1 - x0, y1 - y0, z1 - z0
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r["verts"])
    bmesh.ops.translate(bm, vec=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), verts=r["verts"])


# Room: 12 wide (x), 10 deep (y), 6 high (z). Unit = one block.
for x in range(12):
    for y in range(10):
        box("floorA" if (x + y) % 2 == 0 else "floorB", x, y, -0.2, x + 1, y + 1, 0)

# back wall (y = -0.3..0) with a window hole x 4..8, z 2..5
for x in range(12):
    for z in range(6):
        if 4 <= x < 8 and 2 <= z < 5:
            continue
        box("wall", x, -0.3, z, x + 1, 0, z + 1)
# left wall (x = -0.3..0)
for y in range(10):
    for z in range(6):
        box("wall", -0.3, y, z, 0, y + 1, z + 1)
# window sill and frame
box("wood", 4, -0.35, 1.9, 8, 0.2, 2.0)
box("wood", 3.9, -0.35, 2, 4.0, 0.1, 5)
box("wood", 8.0, -0.35, 2, 8.1, 0.1, 5)
box("wood", 4, -0.35, 5.0, 8, 0.1, 5.1)
box("wood", 5.95, -0.35, 2, 6.05, 0.1, 5)
box("wood", 4, -0.35, 3.45, 8, 0.1, 3.55)
# sky card behind the window
box("sky", 3, -4, 1, 9, -3.9, 6)

# base cabinets along the back wall (two runs), counter top, doors as relief blocks
for (xa, xb) in ((0, 4), (8, 12)):
    box("cab", xa, 0, 0, xb, 2, 1.8)
    box("top", xa, 0, 1.8, xb, 2.1, 2.0)
    for i in range(int(xb - xa)):
        box("wood", xa + i + 0.1, 2.0, 0.2, xa + i + 0.9, 2.08, 1.6)
        box("metal", xa + i + 0.4, 2.08, 1.3, xa + i + 0.6, 2.2, 1.45)
# upper cabinets
for (xa, xb) in ((0, 3), (9, 12)):
    box("cab", xa, 0, 3.6, xb, 1.2, 5.4)
    for i in range(int(xb - xa)):
        box("wood", xa + i + 0.1, 1.2, 3.7, xa + i + 0.9, 1.28, 5.3)
# side run along left wall
box("cab", 0, 2.0, 0, 1.8, 8, 1.8)
box("top", 0, 2.0, 1.8, 2.0, 8, 2.0)
# shelf with jars on the left wall
box("wood", 0, 3, 3.3, 0.7, 7, 3.4)
for i in range(6):
    box("top", 0.15, 3.2 + i * 0.6, 3.4, 0.55, 3.55 + i * 0.6, 3.9)

# table (4 x 3), legs, top
box("wood", 4, 4, 2.0, 8, 7, 2.25)
for (lx, ly) in ((4.1, 4.1), (7.6, 4.1), (4.1, 6.6), (7.6, 6.6)):
    box("wood", lx, ly, 0, lx + 0.3, ly + 0.3, 2.0)
# two chairs
for (cx, cy) in ((5, 3.0), (6.4, 7.7)):
    box("chair", cx, cy, 1.2, cx + 1.2, cy + 1.2, 1.4)
    for (dx, dy) in ((0, 0), (0.95, 0), (0, 0.95), (0.95, 0.95)):
        box("chair", cx + dx, cy + dy, 0, cx + dx + 0.25, cy + dy + 0.25, 1.2)
    back_y = cy if cy < 5 else cy + 0.95
    box("chair", cx, back_y, 1.4, cx + 1.2, back_y + 0.25, 2.8)
# rug
box("rug", 3, 3.2, 0.0, 9, 7.8, 0.03)
# a plant on the counter, voxel pot and leaf blocks
box("pot", 10.2, 0.4, 2.0, 10.9, 1.1, 2.6)
for (dx, dy, dz) in ((0.15, 0.15, 2.6), (0.35, 0.25, 2.9), (0.05, 0.35, 3.1), (0.45, 0.05, 3.2)):
    box("leaf", 10.2 + dx, 0.4 + dy, dz, 10.2 + dx + 0.3, 0.4 + dy + 0.3, dz + 0.45)
# kettle and mugs as blocks
box("metal", 1.0, 0.5, 2.0, 1.9, 1.3, 2.7)
box("metal", 2.2, 0.6, 2.0, 2.6, 1.0, 2.35)
box("chair", 2.8, 0.6, 2.0, 3.2, 1.0, 2.35)
# table-top still life: bowl of blocks, fruit as cubes (voxel fruit)
box("pot", 5.6, 5.0, 2.25, 6.8, 6.2, 2.4)
for i, (dx, dy, k) in enumerate(((0.1, 0.1, "fruitR"), (0.5, 0.2, "fruitY"), (0.25, 0.55, "fruitR"), (0.7, 0.6, "fruitY"), (0.4, 0.35, "fruitR"))):
    box(k, 5.6 + dx, 5.0 + dy, 2.4 + (0.12 if i == 4 else 0), 5.6 + dx + 0.38, 5.0 + dy + 0.38, 2.4 + 0.38 + (0.12 if i == 4 else 0))
box("top", 7.0, 4.4, 2.25, 7.5, 4.9, 2.6)
# pendant lamp: emissive block on a cord
box("wood", 5.95, 5.45, 4.2, 6.05, 5.55, 6.0)
box("lamp", 5.3, 5.0, 3.7, 6.7, 6.0, 4.2)

for key, bm in meshes.items():
    me = bpy.data.meshes.new(key)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(key, me)
    ob.data.materials.append(M[key])
    scene.collection.objects.link(ob)

# smooth, round items to keep it from being cubes only: kettle dome and fruit sphere (UV spheres)
for (loc, r, k) in (((1.45, 0.9, 2.95), 0.45, "metal"), ((6.2, 5.6, 2.9), 0.28, "fruitR")):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=loc)
    o = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    o.data.materials.append(M[k])

# --- lights ------------------------------------------------------------------------
sun = bpy.data.lights.new("sun", "SUN")
sun.energy = 4.0
sun.angle = math.radians(2.0)
so = bpy.data.objects.new("sun", sun)
so.rotation_euler = Euler((math.radians(55), 0, math.radians(15)), "XYZ")
scene.collection.objects.link(so)

pl = bpy.data.lights.new("pendant", "POINT")
pl.energy = 600
pl.shadow_soft_size = 0.4
po = bpy.data.objects.new("pendant", pl)
po.location = (6.0, 5.5, 3.5)
scene.collection.objects.link(po)

world = bpy.data.worlds.new("world")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.55, 0.7, 0.95, 1)
bg.inputs["Strength"].default_value = 0.6
scene.world = world

# --- camera ------------------------------------------------------------------------
cam = bpy.data.cameras.new("cam")
cam.lens = 24
co = bpy.data.objects.new("cam", cam)
co.location = (10.5, 14.5, 4.2)
look = Vector((5.2, 3.0, 2.0))
d = look - co.location
co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
scene.collection.objects.link(co)
scene.camera = co

# --- render settings ---------------------------------------------------------------
scene.render.engine = "CYCLES"
c = scene.cycles
c.device = "CPU"
c.samples = SAMPLES
c.use_adaptive_sampling = ADA
c.use_denoising = DEN
if DEN:
    c.denoiser = "OPENIMAGEDENOISE"
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 100
scene.render.threads_mode = "AUTO"
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX" if "AgX" in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items.keys() else "Standard"
tag = f"k_{W}x{H}_s{SAMPLES}_{'dn' if DEN else 'nodn'}_{'ada' if ADA else 'fix'}"
scene.render.filepath = os.path.join(OUT, tag + ".png")

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "kitchen_standin.blend"))

t0 = time.time()
bpy.ops.render.render(write_still=True)
dt = time.time() - t0
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
tris = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
print(f"RESULT {W}x{H} samples={SAMPLES} denoise={int(DEN)} adaptive={int(ADA)} wall_s={dt:.1f} peak_rss_mb={rss:.0f} faces={tris}", flush=True)
