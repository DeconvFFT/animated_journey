# r4_render_voxel.py: Blender side of the voxel chain. Import the Goxel OBJ, vertex-colour material, warm light, 960x540 still.
# Source: research/toolchain.md, recipe R4 (Blender part). Code verbatim; this header added by the scribe.
# Ran on: bpy 5.2.2 (Python 3.13), Ubuntu 24.04 sandbox, 4 vCPU, no GPU, Cycles CPU, 24 samples with denoise.
#   Date run: 2026-10-18 [RUN]: about 8 s for the 960x540 still.
# Needs: ./scene.obj next to this file (from r4_photo2vox.py and Goxel).
# Writes: ./voxel_still.png
# Axis: the Goxel OBJ is Z-up, and Blender's OBJ importer assumes Y-up, so forward_axis='Y', up_axis='Z' is required.
# Not tested: the turntable. The notes give the plan only: parent the camera to an Empty at the object's centre,
#   keyframe the Empty's Z rotation from 0 to 360 degrees, and render the PNG sequence.
# Run:    blender -b --factory-startup -P r4_render_voxel.py   (or python3 with bpy installed)

import bpy, math, os
W = os.path.abspath(os.path.dirname(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=os.path.join(W, 'scene.obj'), forward_axis='Y', up_axis='Z')   # default is Y-up
obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
mat = bpy.data.materials.new('vox'); mat.use_nodes = True; nt = mat.node_tree
ca = nt.nodes.new('ShaderNodeAttribute'); ca.attribute_name = obj.data.color_attributes[0].name   # 'Color'
nt.links.new(ca.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color']); obj.data.materials.append(mat)
sc = bpy.context.scene
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(60), 0, math.radians(-30)))
sun = bpy.context.object; sun.data.energy = 4; sun.data.color = (1.0, 0.78, 0.55); sun.data.angle = math.radians(8)   # warm key
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
bg = sc.world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.9, 0.62, 0.4, 1); bg.inputs['Strength'].default_value = 0.6
dims = obj.dimensions
bpy.ops.object.camera_add(location=(0, -dims.x * 1.5, 0), rotation=(math.radians(90), 0, 0))   # front view from -y
sc.camera = bpy.context.object; sc.camera.data.lens = 50
sc.view_settings.view_transform = 'Standard'; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.filepath = os.path.join(W, 'voxel_still.png'); bpy.ops.render.render(write_still=True)
