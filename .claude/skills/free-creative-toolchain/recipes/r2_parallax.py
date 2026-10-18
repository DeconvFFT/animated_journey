# r2_parallax.py: headless 2.5D parallax in Blender from three layer PNGs (bg, mid, fg).
# Source: research/toolchain.md, recipe R2. Code verbatim; this header added by the scribe.
# Ran on: bpy 5.2.2 (Blender 5.2.2 as a Python module, Python 3.13), Ubuntu 24.04 sandbox,
#   4 vCPU, no GPU, Cycles CPU, 4 samples. Date run: 2026-10-18 [RUN].
#   Result: 50 frames at 640x360 in about 64 s; a sky pixel read #FCCF97 against the source #FFD9A0
#   (colour kept because view_transform is Standard).
# Also run as the Windows Blender 5.2.2 build under Wine 9.0 (research Follow-up F2), as the parameterised
#   copy recipes/r2_param.py, NOT this file. Not yet run on the maker's PC: TODO(verify on the maker's PC).
# Needs: ./layers/bg.png, ./layers/mid.png, ./layers/fg.png (RGBA, transparent where the layer is absent).
#   Create ./renders/ first if it does not exist (TODO(verify on the maker's PC)).
# Writes: ./renders/p_0001.png ... p_0050.png
# Run:    blender -b --factory-startup -P r2_parallax.py     (or: python3 r2_parallax.py with bpy installed)
# Windows run (PowerShell, from this folder; use your unzipped Blender folder): TODO(verify on the maker's PC)
#         & "<path>\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r2_parallax.py
#         Use blender.exe, the console program, not blender-launcher.exe (F2).
# Draft:  to draft at 480p or change the length, edit resolution_x, resolution_y and frame_end below.
#         The file as written is the tested 640x360, 50-frame run.
# Note:   Blender 5.2.2 warns that Material.use_nodes will be removed in Blender 6.0 (F2); harmless for 5.2 LTS.

import bpy, math, os
W = os.path.abspath(os.path.dirname(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 640, 360, 25
sc.frame_start, sc.frame_end = 1, 50
sc.view_settings.view_transform = 'Standard'          # default AgX desaturates photos
def plane_height(dist):                                # fills a 16:9 frame at 50 mm / 36 mm sensor
    return (dist * 36 / 50) / (16 / 9)
def add_layer(name, png, y, margin=1.1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 0))
    o = bpy.context.object; o.name = name
    h = plane_height(10 + y) * margin                  # camera sits at y = -10
    o.scale = (h * 16 / 9, h, 1); o.rotation_euler = (math.radians(90), 0, 0)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(W, 'layers', png))
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(tex.outputs['Color'], em.inputs['Color']); nt.links.new(tex.outputs['Alpha'], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface']); o.data.materials.append(m)
add_layer('bg', 'bg.png', 8, 1.25); add_layer('mid', 'mid.png', 0); add_layer('fg', 'fg.png', -5)
bpy.ops.object.camera_add(location=(-0.4, -10, 0), rotation=(math.radians(90), 0, 0))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 50; cam.data.sensor_width = 36
cam.keyframe_insert('location', frame=1)               # Bezier (eased) by default
cam.location.x = 0.4; cam.keyframe_insert('location', frame=50)
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = os.path.join(W, 'renders', 'p_')
bpy.ops.render.render(animation=True)
# Then (bash, tested): ffmpeg -framerate 25 -i renders/p_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p parallax.mp4
