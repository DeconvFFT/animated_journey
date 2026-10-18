#!/usr/bin/env bash
# r9_deliver.sh: three delivery files from one master (screening, private web link, archive), then the ffprobe check.
# Source: research/toolchain.md, recipe R9, whose commands are given in Q6 of the notes. Commands verbatim; comments added by the scribe.
# Ran on: ffmpeg 6.1.1 (Ubuntu 24.04 sandbox), date 2026-10-18 [RUN].
#   Results seen (R9): MP4 h264 High, level 41, yuv420p, 1920x1080 with aac LC 48000 Hz 2 channels;
#   ProRes yuv422p10le with pcm_s24le; FFV1 with flac.
# Caveat 1: the screening command below adds -maxrate 20M -bufsize 40M. The notes tested the same command
#   WITHOUT that pair; the pair is a safety margin. The web command with -maxrate 12M -bufsize 24M is the tested variant (Q6).
# Caveat 2: not yet run on the maker's Windows PC. TODO(verify on the maker's PC). PowerShell takes the same arguments.
# Usage:  bash r9_deliver.sh master.mov
#         (ffprobe check: step 4 at the end)

MASTER="${1:-master.mov}"

# 1) Screening: USB stick, TV or projector. H.264 High 4.1, yuv420p, BT.709 tags, AAC-LC 48 kHz stereo, faststart.
ffmpeg -i "$MASTER" -c:v libx264 -preset slow -crf 18 -maxrate 20M -bufsize 40M -profile:v high -level 4.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart deliver_usb.mp4

# 2) Private web link: CRF 20, 12 Mbps cap at 1080p.
ffmpeg -i "$MASTER" -c:v libx264 -preset slow -crf 20 -maxrate 12M -bufsize 24M -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart web_1080.mp4

# 3a) Archive A: ProRes 422 HQ in MOV, PCM 24-bit audio.
ffmpeg -i "$MASTER" -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le -c:a pcm_s24le archive_prores422hq.mov

# 3b) Archive B: FFV1 version 3 in Matroska, FLAC audio.
ffmpeg -i "$MASTER" -c:v ffv1 -level 3 -coder 1 -context 1 -g 1 -slicecrc 1 -c:a flac archive_ffv1.mkv

# 4) Check every file (playbook Step 13). Expect for the screening file: h264, High, level 41, yuv420p, 1920x1080, aac, LC, 48000, 2.
for f in deliver_usb.mp4 web_1080.mp4 archive_prores422hq.mov archive_ffv1.mkv; do
  ffprobe -v error -show_entries stream=codec_name,profile,level,pix_fmt,width,height,sample_rate,channels -of csv=p=0 "$f"
done

# 5) Optional captions (research Q6). Burn-in goes into the screening file as an extra -vf filter. Choose a font that exists on your PC.
#    -vf "subtitles=subs.srt:force_style='FontName=DejaVu Sans,FontSize=28,Outline=2,MarginV=40'"
#    TODO(verify on the maker's PC): font availability on Windows.
#    Soft subtitles (tested as muxes in Q6; TV support UNVERIFIED): MP4 -i subs.srt -map 0 -map 1 -c copy -c:s mov_text ; MKV -c:s srt
