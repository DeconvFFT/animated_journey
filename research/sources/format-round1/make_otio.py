import json, os, sys
import opentimelineio as otio
tl = json.load(open("timeline169.json")); fps = tl["fps"]
t = otio.schema.Timeline(name="life_journey_test")
t.global_start_time = otio.opentime.RationalTime(0, fps)
v = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
for i, s in enumerate(tl["shots"]):
    ref = otio.schema.ExternalReference(target_url=os.path.abspath(s["file"]),
        available_range=otio.opentime.TimeRange(otio.opentime.RationalTime(0, fps), otio.opentime.RationalTime(int(s["dur"]*fps), fps)))
    c = otio.schema.Clip(name=s["id"], media_reference=ref,
        source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(0, fps), otio.opentime.RationalTime(int(s["dur"]*fps), fps)),
        metadata={"life_journey": {"move": s["move"]}})
    v.append(c)
t.tracks.append(v)
a = otio.schema.Track(name="A1", kind=otio.schema.TrackKind.Audio)
a.append(otio.schema.Clip(name="voice", media_reference=otio.schema.ExternalReference(target_url=os.path.abspath(tl["audio"]["voice"]),
    available_range=otio.opentime.TimeRange(otio.opentime.RationalTime(0, fps), otio.opentime.RationalTime(20*fps, fps))),
    source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(0, fps), otio.opentime.RationalTime(20*fps, fps))))
t.tracks.append(a)
otio.adapters.write_to_file(t, "out.otio")
for fmt, ext in (("cmx_3600", "edl"), ("fcpx_xml", "fcpxml"), ("kdenlive", "kdenlive"), ("mlt_xml", "mlt")):
    try:
        otio.adapters.write_to_file(t, f"out_otio.{ext}", adapter_name=fmt)
        print("WROTE", fmt, os.path.getsize(f"out_otio.{ext}"), "bytes")
    except Exception as e:
        print("FAIL ", fmt, type(e).__name__, str(e)[:200])
# round trip read
r = otio.adapters.read_from_file("out.otio")
print("read back clips:", [c.name for c in r.find_clips()])
