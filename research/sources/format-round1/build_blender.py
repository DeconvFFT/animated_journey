"""Blender VSE, headless via the `bpy` pip module (5.2.2): timeline.json + captions.srt -> mp4. Usage: python build_blender.py timeline169.json captions.srt out.mp4"""
import bpy, json, os, re, sys
tl_path, srt, out = sys.argv[1:4]
tl = json.load(open(tl_path)); fps = tl["fps"]; xf = int(tl["crossfade"]*fps)
sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
sc.render.fps = fps; sc.render.resolution_x = 960; sc.render.resolution_y = 540   # draft size for the test
sc.view_settings.view_transform = 'Standard'
sc.sequence_editor_create(); se = sc.sequence_editor
frame = 1; prev = None; strips = []
for i, s in enumerate(tl["shots"]):
    n = int(s["dur"]*fps) + xf
    st = se.strips.new_image(s["id"], os.path.abspath(s["file"]), channel=1 + (i % 2), frame_start=frame)
    st.frame_final_duration = n
    st.transform.scale_x = st.transform.scale_y = 1.0
    strips.append(st)
    if prev is not None:
        # crossfade over the overlap frames
        eff = se.strips.new_effect(f"x{i}", 'CROSS', channel=3, frame_start=frame, length=xf, input1=prev, input2=st)
    prev = st; frame += int(s["dur"]*fps)
end = frame + xf - 1
# captions: parse the SRT, add one TEXT strip per cue (Blender 5.2.2 has no SRT import operator)
def t2f(h, m, s_, ms): return int(round((int(h)*3600 + int(m)*60 + int(s_) + int(ms)/1000) * fps)) + 1
blocks = re.split(r"\n\s*\n", open(srt, encoding="utf8").read().strip())
for b in blocks:
    ls = b.splitlines()
    m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", ls[1])
    f0, f1 = t2f(*m.groups()[:4]), t2f(*m.groups()[4:])
    tx = se.strips.new_effect("cap" + ls[0], 'TEXT', channel=5, frame_start=f0, length=f1 - f0)
    tx.text = "\n".join(ls[2:]); tx.font_size = 38; tx.color = (1, 1, 1, 1)
    tx.location = (0.5, 0.08); tx.anchor_x = 'CENTER'; tx.anchor_y = 'BOTTOM'
    tx.use_shadow = True; tx.shadow_color = (0, 0, 0, 1); tx.use_outline = True; tx.outline_color = (0, 0, 0, 1); tx.outline_width = 0.1
a = tl["audio"]
se.strips.new_sound("voice", os.path.abspath(a["voice"]), channel=6, frame_start=1)
mu = se.strips.new_sound("music", os.path.abspath(a["music"]), channel=7, frame_start=1); mu.volume = 10 ** (a["music_gain_db"]/20)
sc.frame_start, sc.frame_end = 1, int(sum(s["dur"] for s in tl["shots"])*fps)
r = sc.render; r.image_settings.media_type = 'VIDEO'; r.image_settings.file_format = 'FFMPEG'
r.ffmpeg.format = 'MPEG4'; r.ffmpeg.codec = 'H264'; r.ffmpeg.constant_rate_factor = 'MEDIUM'; r.ffmpeg.audio_codec = 'AAC'; r.ffmpeg.audio_bitrate = 192
r.filepath = os.path.abspath(out)
bpy.ops.render.render(animation=True)
print("RENDERED", out)
