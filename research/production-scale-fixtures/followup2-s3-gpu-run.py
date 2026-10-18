"""
Spike S3, GPU half, for the maker's own PC or a rented pod (use ONLY the stand-in scene, never family imagery).

Run with Blender's own Python, from a command line:
  blender -b followup2-kitchen-standin.blend -P followup2-s3-gpu-run.py -- OUT_DIR [WIDTH HEIGHT]

It tries OPTIX, CUDA, HIP, ONEAPI, METAL in that order and uses the first that lists a device;
otherwise it renders on CPU and says so. It then renders the same frame four times at 1080p:
  8 samples (warm-up; the first run also pays kernel load and shader compile: that is the "cold" number),
  64 samples with denoise, 128 samples with denoise, 128 samples without denoise.
It prints lines starting S3GPU and writes OUT_DIR/s3_gpu_result.txt. Paste that file back.
"""
import bpy, sys, time, os, platform

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else os.getcwd()
w = int(argv[1]) if len(argv) > 2 else 1920
h = int(argv[2]) if len(argv) > 2 else 1080
os.makedirs(out, exist_ok=True)
lines = []


def say(s):
    print(s, flush=True)
    lines.append(s)


scene = bpy.context.scene
scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
chosen = None
for dev_type in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
    try:
        prefs.compute_device_type = dev_type
        if hasattr(prefs, "refresh_devices"):
            prefs.refresh_devices()
        else:
            prefs.get_devices()
    except Exception:
        continue
    gpus = [d for d in prefs.devices if d.type == dev_type]
    if gpus:
        for d in prefs.devices:
            d.use = d.type == dev_type
        chosen = (dev_type, [d.name for d in gpus])
        break

c = scene.cycles
if chosen:
    c.device = "GPU"
    say(f"S3GPU device_type={chosen[0]} devices={chosen[1]}")
else:
    c.device = "CPU"
    say("S3GPU NO GPU FOUND: rendering on CPU, so these numbers are CPU numbers")
say(f"S3GPU blender={bpy.app.version_string} os={platform.platform()}")

scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = w, h, 100
c.use_adaptive_sampling = False
runs = [(8, False), (64, True), (128, True), (128, False)]
for i, (spp, dn) in enumerate(runs):
    c.samples = spp
    c.use_denoising = dn
    if dn:
        c.denoiser = "OPTIX" if (chosen and chosen[0] == "OPTIX") else "OPENIMAGEDENOISE"
    scene.render.filepath = os.path.join(out, f"s3gpu_{w}x{h}_s{spp}_{'dn' if dn else 'nodn'}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t
    tag = "cold (first render in this process)" if i == 0 else "warm"
    say(f"S3GPU {w}x{h} samples={spp} denoise={int(dn)} wall_s={dt:.2f} {tag}")

with open(os.path.join(out, "s3_gpu_result.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
