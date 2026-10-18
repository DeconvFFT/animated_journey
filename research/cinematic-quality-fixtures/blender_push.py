"""Round 2: a Blender (bpy 5.2.2 LTS, Cycles CPU) camera push on a textured plane, rendered to numbered PNG frames, for the MO8 check.
Run with a Python that has the `bpy` wheel (pip install bpy; Python 3.13 wheel exists for bpy 5.2.2):
  python -I blender_push.py OUTDIR STILL.png [--interp Linear|Closest|Cubic|Smart] [--motion-blur] [--shutter 0.5] [--samples 32]
                            [--frames 96] [--fps 24] [--amount 0.04] [--filter BLACKMAN_HARRIS|BOX|GAUSSIAN] [--filter-width 1.5] [--kind push|pan] [--pan-px 760]
Scene: a 16 x 9 plane with the still as an emission texture (no lighting, no tone mapping: view transform Standard, dither 0), camera 50 mm on a 36 mm
sensor looking straight at it. Push = camera z keyframes d0 -> d0/(1+amount) with SINE ease-in-out (Blender F-curve easing; the apparent zoom is within a
few tenths of a percent of the cosine in-out of the Pillow reference). Pan = camera x keyframes, SINE ease-in-out, scale 1:1 on a 3840-wide still shown at half
size, so pan_px output pixels = pan_px/2 still pixels... (the plane is 2x the frame width).
"Sub-frame sampling" here is Cycles motion blur: each sample's time is jittered inside the shutter, so a frame is the average of the push over `shutter` frames.
Without it every sample of a frame is taken at exactly the frame time."""
import sys, os, math, argparse
import bpy

ap = argparse.ArgumentParser()
ap.add_argument("outdir"); ap.add_argument("still")
ap.add_argument("--interp", default="Linear"); ap.add_argument("--motion-blur", action="store_true")
ap.add_argument("--shutter", type=float, default=0.5); ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--frames", type=int, default=96); ap.add_argument("--fps", type=int, default=24)
ap.add_argument("--amount", type=float, default=0.04); ap.add_argument("--filter", default="BLACKMAN_HARRIS")
ap.add_argument("--filter-width", type=float, default=1.5); ap.add_argument("--kind", default="push")
ap.add_argument("--pan-px", type=float, default=760.0); ap.add_argument("--first", type=int, default=None); ap.add_argument("--last", type=int, default=None)
a = ap.parse_args(sys.argv[1:])

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = a.samples
sc.cycles.use_denoising = False
sc.cycles.pixel_filter_type = a.filter
sc.cycles.filter_width = a.filter_width
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
sc.render.fps = a.fps
sc.frame_start, sc.frame_end = 1, a.frames
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.view_settings.exposure = 0.0; sc.view_settings.gamma = 1.0
sc.display_settings.display_device = "sRGB"
sc.render.dither_intensity = 0.0
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"; sc.render.image_settings.color_depth = "8"
sc.render.use_motion_blur = bool(a.motion_blur)
sc.render.motion_blur_shutter = a.shutter
sc.render.motion_blur_position = "CENTER"
sc.render.threads_mode = "AUTO"

# plane: 16 x 9 (pan: 32 x 18 so that 1:1 mapping holds when the frame shows 16 x 9 units... the still is 3840 wide => 2 px per frame px at plane width 16)
img = bpy.data.images.load(os.path.abspath(a.still)); img.colorspace_settings.name = "sRGB"
pw = 16.0 if a.kind == "push" else 32.0
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
plane = bpy.context.active_object; plane.scale = (pw, pw * 9 / 16, 1.0)
mat = bpy.data.materials.new("m"); mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img; tex.interpolation = a.interp; tex.extension = "CLIP"
emi = nt.nodes.new("ShaderNodeEmission"); emi.inputs["Strength"].default_value = 1.0
out = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(tex.outputs["Color"], emi.inputs["Color"]); nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
plane.data.materials.append(mat)

cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 50.0; cam_data.sensor_width = 36.0; cam_data.sensor_fit = "HORIZONTAL"
cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam
d0 = 16.0 / (2 * 18.0 / 50.0)          # distance at which a 16-unit-wide plane exactly fills the frame
cam.location = (0, 0, d0); cam.rotation_euler = (0, 0, 0)

def key(frame, idx, value):
    cam.location[idx] = value
    cam.keyframe_insert(data_path="location", index=idx, frame=frame)

if a.kind == "push":
    key(1, 2, d0); key(a.frames, 2, d0 / (1 + a.amount)); idx = 2
else:
    # frame shows 16 units over 1920 px => 120 px per unit; 3840-px still over 32 units = 120 still px per unit, i.e. output px = still px / ... 1:1 on screen
    dx = a.pan_px / 1920 * 16.0
    key(1, 0, 0.0); key(a.frames, 0, -dx); idx = 0       # camera moves left => content moves right (+x)
    cam.location[2] = d0
fc = cam.animation_data.action
# Blender 5 layered actions: walk the fcurves of the slot
def fcurves(action):
    try:
        return list(action.fcurves)
    except Exception:
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    out.extend(cb.fcurves)
        return out
for f in fcurves(fc):
    for kp in f.keyframe_points:
        kp.interpolation = "SINE"; kp.easing = "EASE_IN_OUT"

os.makedirs(a.outdir, exist_ok=True)
sc.render.filepath = os.path.join(a.outdir, "f_")
if a.first is not None:
    sc.frame_start, sc.frame_end = a.first, a.last or a.first
bpy.ops.render.render(animation=True)
print("blender_push done", a.interp, "motion_blur" if a.motion_blur else "no_motion_blur", a.samples, "samples")
