# r8_vse_xfade.py: Blender video sequencer used as a scriptable editor. Two clips with a 25-frame CROSS dissolve.
# Source: research/toolchain.md, recipe R8. The notes show only the lines marked [R8]. The scene, path and render
#   lines marked TODO(verify) are the scribe's minimal completion. They were NOT run as a file.
# Ran on: the [R8] lines in bpy 5.2.2 (Python 3.13), Ubuntu 24.04 sandbox. Date run: 2026-10-18 [RUN]:
#   a 1920x1080, 224-frame H.264 crossfade rendered in 11 s with the notes' lines.
# Needs: ./kbA.mp4 and ./kbB.mp4 next to this file (for example from r1_kenburns.sh).
# Lessons (Blender 5.2): the sequencer collection is `strips` (older versions: `sequences`); new_effect takes
#   `length`, not `frame_end`; set media_type = 'VIDEO' before file_format = 'FFMPEG'. Probe with dir() before
#   trusting a remembered call.
# Run:    blender -b --factory-startup -P r8_vse_xfade.py   (or python3 with bpy installed)
# Windows run (PowerShell, from this folder): TODO(verify on the maker's PC)
#         & "<path>\blender.exe" -b --factory-startup -noaudio --python-exit-code 3 -P .\r8_vse_xfade.py

import bpy, os
W = os.path.abspath(os.path.dirname(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)          # TODO(verify): scribe addition
sc = bpy.context.scene                                    # TODO(verify): scribe addition
sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 1920, 1080, 25   # TODO(verify): scribe addition; tested at 25, UNVERIFIED at 24: the project rate is 24 (DECISIONS.md W-14, S-01)
sc.frame_start, sc.frame_end = 1, 224                     # the notes' run rendered 224 frames
sc.render.image_settings.media_type = 'VIDEO'; sc.render.image_settings.file_format = 'FFMPEG'   # 5.x: media_type first  [R8]
sc.render.ffmpeg.format = 'MPEG4'; sc.render.ffmpeg.codec = 'H264'; sc.render.ffmpeg.audio_codec = 'NONE'   # [R8]
se = sc.sequence_editor_create(); coll = se.strips                                               # 5.x: `strips` (older: `sequences`)  [R8]
a = coll.new_movie('A', os.path.join(W, 'kbA.mp4'), channel=1, frame_start=1)                    # [R8]; absolute path: TODO(verify)
b = coll.new_movie('B', os.path.join(W, 'kbB.mp4'), channel=2, frame_start=100)                  # 25-frame overlap  [R8]
coll.new_effect('xf', 'CROSS', channel=3, frame_start=100, length=25, input1=a, input2=b)       # 5.x: `length`, not `frame_end`  [R8]
sc.render.filepath = os.path.join(W, 'xfade.mp4')         # TODO(verify): scribe addition
bpy.ops.render.render(animation=True)                    # TODO(verify): scribe addition
