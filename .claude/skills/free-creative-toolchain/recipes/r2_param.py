# r2_param.py: R2 (recipes/r2_parallax.py) with five environment variables, so one file serves bpy, blender -b -P and blender.exe -b -P.
# Source: research/toolchain.md, Follow-up F2 and its appendix "R2 with five parameters". The same file also sits at
#   research/toolchain-fixtures/r2_param.py. Header added by the scribe in round 2; the code is the appendix version.
# Ran on: [RUN] bpy 5.2.2 on Linux (Python 3.13), Ubuntu 24.04 sandbox, 4 vCPU, no GPU, Cycles CPU, 4 samples. Date run: 2026-10-18.
# Ran on: [RUN-WINE] blender.exe 5.2.2 (Windows x64 build) under Wine 9.0, same settings. Date run: 2026-10-18 (F2).
# Also: the step0_pc_tests.ps1 dry run (PowerShell 7.5.4 on Linux, Linux Blender 5.2.2) timed this file (F9).
#   Not run on Windows PowerShell and not yet on the maker's PC: TODO(verify on the maker's PC).
# Needs: ./layers/bg.png, ./layers/mid.png, ./layers/fg.png (RGBA, transparent where the layer is absent).
# Variables (defaults in brackets are the tested 640x360, 50-frame run of r2_parallax.py):
#   R2_DIR [this file's folder]   R2_RX, R2_RY [640, 360]   R2_NF [50]   R2_SPP [4]   R2_LAYERS [layers]   R2_OUT [renders]
# Writes: $R2_OUT/p_0001.png ... and one line that starts with R2_RESULT (frames, resolution, samples, seconds, seconds per frame).
# Run (Linux, bash): R2_RX=640 R2_RY=360 R2_NF=10 R2_OUT=r640 blender -b --factory-startup -noaudio --python-exit-code 3 -P r2_param.py
# Measure (Windows, PowerShell; TODO(verify on the maker's PC)). Close the Claude desktop app first. Run the two timed runs.
#   The D:\ path is the example from F2; use the folder you unzipped Blender into.
#   $env:R2_DIR=(Get-Location).Path; $env:R2_NF=10; $env:R2_SPP=4; $env:R2_LAYERS='layers'
#   $env:R2_RX=640;  $env:R2_RY=360;  $env:R2_OUT='r640';  & "D:\blender-5.2.2-windows-x64\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r2_param.py
#   $env:R2_RX=1920; $env:R2_RY=1080; $env:R2_OUT='r1080'; & "D:\blender-5.2.2-windows-x64\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r2_param.py
#   Get-Process blender | Select PeakWorkingSet64      (run in a second window while each render is going)
# The output folders (r640, r1080) may need to exist first: TODO(verify on the maker's PC).
# Note: Blender 5.2.2 warns that Material.use_nodes will be removed in Blender 6.0 (F2); harmless for 5.2 LTS.

import bpy, math, os, time
W = os.environ.get('R2_DIR') or os.path.abspath(os.path.dirname(__file__))
RX, RY = int(os.environ.get('R2_RX', 640)), int(os.environ.get('R2_RY', 360))
NF = int(os.environ.get('R2_NF', 50)); SPP = int(os.environ.get('R2_SPP', 4))
LAYERS = os.environ.get('R2_LAYERS', 'layers'); OUT = os.environ.get('R2_OUT', 'renders')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP
sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = RX, RY, 25
sc.frame_start, sc.frame_end = 1, NF
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
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(os.path.join(W, LAYERS, png))
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(tex.outputs['Color'], em.inputs['Color']); nt.links.new(tex.outputs['Alpha'], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface']); o.data.materials.append(m)
add_layer('bg', 'bg.png', 8, 1.25); add_layer('mid', 'mid.png', 0); add_layer('fg', 'fg.png', -5)
bpy.ops.object.camera_add(location=(-0.4, -10, 0), rotation=(math.radians(90), 0, 0))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 50; cam.data.sensor_width = 36
cam.keyframe_insert('location', frame=1)               # Bezier (eased) by default
cam.location.x = 0.4; cam.keyframe_insert('location', frame=NF)
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = os.path.join(W, OUT, 'p_')
t0 = time.time()
bpy.ops.render.render(animation=True)
dt = time.time() - t0
print('R2_RESULT frames=%d res=%dx%d spp=%d render_seconds=%.2f sec_per_frame=%.3f' % (NF, RX, RY, SPP, dt, dt / NF), flush=True)
