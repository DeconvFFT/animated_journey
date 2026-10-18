#!/usr/bin/env python3
"""make_venue_test_kit.py: six short test files plus a checklist, to answer "what will THIS screen play?"

Research fixture for research/toolchain.md, "Follow-up research (round 2)", F15. Written and run 2026-10-18.
Contains no personal material. Each file is 10 s, 25 fps, 48 kHz stereo, with a frame counter, a bar moving at a
constant speed (judder check), a 1 kHz beep on the LEFT channel for seconds 0 to 4.9 and on the RIGHT for 5 to 10,
and a caption test. Put the files on the same USB stick that the premiere will use and play them on the venue's
real screen or player. Whatever plays tells you which export to make (Decisions 7, 8 and 9).

Run (Linux, macOS, Windows; needs only Python 3 and an ffmpeg that has libx264, libx265 and libass):
    python3 make_venue_test_kit.py                      (ffmpeg found on PATH)
    py -3 make_venue_test_kit.py "C:\\path\\to\\ffmpeg.exe"   (PowerShell; Kdenlive's bin\\ffmpeg.exe works)
Output goes to ./venue_test_kit/ . Python calls ffmpeg without a shell, so no quoting differs between shells.
Text is drawn with libass (an .ass file), NOT drawtext: the ffmpeg.exe 8.1.1 inside Kdenlive 26.08.2 has no
drawtext filter (checked 2026-10-18), but it has the subtitles and ass filters.
"""
import os, subprocess, sys

FFMPEG = sys.argv[1] if len(sys.argv) > 1 else "ffmpeg"
OUT = "venue_test_kit"
W, H, FPS, DUR = 1920, 1080, 25, 10


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Arial,64,&H00FFFFFF,&H000000FF,&H00101010,&H99000000,0,0,0,0,100,100,0,0,3,12,0,8,20,20,50,1
Style: Info,Arial,54,&H00FFFFFF,&H000000FF,&H00101010,&H99000000,0,0,0,0,100,100,0,0,3,12,0,8,20,20,150,1
Style: Mid,Arial,48,&H00FFFFFF,&H000000FF,&H00101010,&H99000000,0,0,0,0,100,100,0,0,3,12,0,8,20,20,620,1
Style: Cap,Arial,48,&H00FFFFFF,&H000000FF,&H00101010,&H99000000,0,0,0,0,100,100,0,0,3,12,0,2,20,20,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(sec):
    cs = int(round(sec * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def write_ass(path, label, burned):
    lines = [ASS_HEAD, f"Dialogue: 0,{ts(0)},{ts(DUR)},Title,,0,0,0,,{label}\n",
             f"Dialogue: 0,{ts(0)},{ts(DUR)},Mid,,0,0,0,,LEFT beep 0-5 s, RIGHT beep 5-10 s\n"]
    for n in range(DUR * FPS):                       # frame counter: one event per frame (plain text, no drawtext needed)
        lines.append(f"Dialogue: 1,{ts(n / FPS)},{ts((n + 1) / FPS)},Info,,0,0,0,,{W}x{H}  {FPS} fps  frame {n}\n")
    if burned:
        lines.append(f"Dialogue: 0,{ts(0)},{ts(DUR)},Cap,,0,0,0,,BURNED-IN CAPTION: if you can read this, burned-in text works\n")
    open(path, "w", encoding="utf-8", newline="\n").write("".join(lines))


def run(args):
    subprocess.run([FFMPEG, "-v", "error", "-y"] + args, check=True, cwd=OUT)


def make_audio(name):
    run(["-f", "lavfi", "-i", "sine=frequency=1000:sample_rate=48000:duration=5",
         "-f", "lavfi", "-i", "sine=frequency=1000:sample_rate=48000:duration=5",
         "-filter_complex",
         "[0]pan=stereo|c0=c0|c1=0*c0,apad=whole_dur=10[l];[1]pan=stereo|c0=0*c0|c1=c0,adelay=5000|5000[r];[l][r]amix=inputs=2:normalize=0",
         "-t", str(DUR), "-ar", "48000", "-c:a", "pcm_s16le", name])


def write_srt(path):
    open(path, "w", encoding="utf-8", newline="\n").write(
        "1\n00:00:01,000 --> 00:00:09,000\nSOFT SUBTITLE: if you can read this, soft subtitles work\n\n")


def picture_inputs(label, burned, wav, scale=1):
    """Inputs 0 = picture with libass text, 1 = moving box (constant 400 px/s at 1080p), 2 = tone.
    ffmpeg runs inside OUT, so the .ass name has no drive letter or colon to escape."""
    ass = f"_text_{abs(hash(label)) % 10**6}.ass"
    write_ass(os.path.join(OUT, ass), label, burned)
    w, h = W * scale, H * scale
    fd = os.environ.get("LJ_FONTSDIR")                 # only if libass finds no font: a folder with a .ttf, drive colon written as \\:
    extra = f":fontsdir='{fd}'" if fd else ""
    return ["-f", "lavfi", "-i", f"color=c=0x203040:s={w}x{h}:r={FPS}:d={DUR},subtitles={ass}{extra}",
            "-f", "lavfi", "-i", f"color=c=yellow:s={160 * scale}x{160 * scale}:r={FPS}:d={DUR}",
            "-i", wav]


def overlay(scale=1, fps_filter=""):
    return (f"[0:v][1:v]overlay=x='mod(t*{400 * scale},{W * scale - 160 * scale})':y={420 * scale}{fps_filter},format=yuv420p[v]")


def check_text_rendered(name):
    """libass draws NOTHING (and ffmpeg still exits 0) when it finds no font. Look for white text pixels in the top quarter."""
    raw = subprocess.run([FFMPEG, "-v", "error", "-ss", "3", "-i", name, "-frames:v", "1", "-vf", "scale=480:270,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, cwd=OUT, check=True).stdout
    top = raw[: 480 * 68]
    white = sum(1 for b in top if b > 200)
    if white < 200:
        sys.exit(f"TEXT DID NOT RENDER in {name} ({white} bright pixels): libass found no font. Install Arial, or set LJ_FONTSDIR "
                 "to a folder that holds a .ttf (on Windows write the drive colon as \\:, for example C\\:/Windows/Fonts).")


def main():
    os.makedirs(OUT, exist_ok=True)
    wav, srt = "_tone.wav", "_subs.srt"                 # names relative to OUT (ffmpeg runs inside OUT)
    make_audio(wav)
    write_srt(os.path.join(OUT, srt))
    x264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "26", "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p"]
    aac = ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
    common = ["-filter_complex", overlay(), "-map", "[v]", "-map", "2:a", "-shortest"]
    run(picture_inputs("A mp4 H.264 burned-in captions", True, wav) + common + x264 + aac +
        ["-movflags", "+faststart", f"venue_a_mp4_h264_burned.mp4"])
    check_text_rendered("venue_a_mp4_h264_burned.mp4")
    run(picture_inputs("B mp4 H.264 + soft subtitle track", False, wav) + ["-i", srt] +
        ["-filter_complex", overlay(), "-map", "[v]", "-map", "2:a", "-map", "3:0", "-shortest"] + x264 + aac +
        ["-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-disposition:s:0", "default", "-movflags", "+faststart",
         f"venue_b_mp4_h264_softsub.mp4"])
    run(picture_inputs("C mkv H.264 + soft subtitle track", False, wav) + ["-i", srt] +
        ["-filter_complex", overlay(), "-map", "[v]", "-map", "2:a", "-map", "3:0", "-shortest"] + x264 + aac +
        ["-c:s", "srt", "-metadata:s:s:0", "language=eng", "-disposition:s:0", "default", f"venue_c_mkv_h264_softsub.mkv"])
    x265 = ["-c:v", "libx265", "-pix_fmt", "yuv420p", "-tag:v", "hvc1", "-x265-params", "log-level=error"]
    run(picture_inputs("D mp4 HEVC 1080p", True, wav) + common + x265 + ["-preset", "medium", "-crf", "28"] + aac +
        ["-movflags", "+faststart", f"venue_d_mp4_hevc_1080.mp4"])
    run(picture_inputs("E mp4 HEVC 2160p", True, wav, 2) + ["-filter_complex", overlay(2), "-map", "[v]", "-map", "2:a", "-shortest"] +
        x265 + ["-preset", "fast", "-crf", "30"] + aac + ["-movflags", "+faststart", f"venue_e_mp4_hevc_2160.mp4"])
    run(picture_inputs("F mp4 H.264 1080p at 50 fps", True, wav) +
        ["-filter_complex", overlay(1, ",fps=50"), "-map", "[v]", "-map", "2:a", "-shortest"] + x264 + aac +
        ["-movflags", "+faststart", f"venue_f_mp4_h264_50fps.mp4"])
    for name in sorted(os.listdir(OUT)):
        if name.startswith("_"):
            os.remove(os.path.join(OUT, name))           # remove the temporary tone, srt and ass helper files
    open(os.path.join(OUT, "VENUE_CHECKLIST.txt"), "w", encoding="utf-8").write(CHECKLIST)
    print("Wrote", OUT, ":", ", ".join(sorted(os.listdir(OUT))))


CHECKLIST = """VENUE TEST KIT: what to write down (take a photo of the screen for each file)

Before: copy the six venue_*.mp4/.mkv files onto the USB stick you will use at the premiere. Note how the stick
is formatted (Windows: Get-Volume shows FileSystem: FAT32, exFAT or NTFS). Test each file on the venue's real
player, projector or TV, with the real cable, in the real room if possible.

Write down:
 1. Screen or projector: make, model, native resolution (1920x1080 or 3840x2160), size, refresh rate.
 2. Cable and path: laptop > HDMI > ? / USB stick > TV / media player box / cinema server. Any adapter?
 3. USB stick format that WAS accepted: FAT32, exFAT, NTFS (try the same files on a second stick formatted differently).
 4. For each file A to F: plays? picture right way up, no stretching? sound on both sides (left beep first, right second)?
    does the yellow box move smoothly (no stutter)? any file that does not appear in the file list at all?
 5. File A: can you read the BURNED-IN caption at the back of the room? (text height, contrast)
 6. Files B and C: does the SOFT SUBTITLE line appear, with no action, or only after switching subtitles on? Which remote button?
 7. File D (HEVC 1080p) and E (HEVC 2160p): play? If not, the film must be H.264.
 8. File F (50 fps): plays smoothly? (tells you whether the screen follows the 25 fps master or needs 50/60 conversion)
 9. Who will press play at the premiere, and from what (the maker's laptop, the venue's computer, a USB stick)?
10. Country and venue name (decides which music licence and which rules apply: jurisdiction is a charter decision).

How the answers close the decisions:
 - Decision 8 (captions): if B or C shows the soft line by default, soft subtitles are possible; otherwise burn captions in (A).
   Burned-in is the safe default whatever the result, because a person in the room cannot switch soft subtitles on mid-film.
 - Decision 7 (export set): use the container and codec of the best file that played. If only A played, ship H.264 MP4.
   If E played smoothly, 4K is possible, but only ship it if the master is 4K; 1080p is enough for most rooms.
 - Decision 9 (venue): items 1 to 3 and 9 are the venue facts; item 10 is the jurisdiction.
"""

if __name__ == "__main__":
    main()
