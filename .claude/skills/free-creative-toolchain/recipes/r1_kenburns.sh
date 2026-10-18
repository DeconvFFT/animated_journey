#!/usr/bin/env bash
# r1_kenburns.sh: scripted Ken Burns push-in, pan and xfade dissolve.
# Source: research/toolchain.md, recipe R1. Commands verbatim; comments and the mkdir line added by the scribe.
# Ran on: ffmpeg 6.1.1 and ImageMagick 6.9.12 (IM6, so the batch line uses `mogrify`;
#   on ImageMagick 7 write `magick mogrify`). Ubuntu 24.04 sandbox, 4 vCPU, no GPU.
# Date run: 2026-10-18 [RUN].
# Not yet run on the maker's Windows PC: TODO(verify on the maker's PC).
# Inputs: ./in/*.jpg (originals, never overwritten: -path out/ writes to out/), ./photoA.jpg, ./photoB.jpg.
# Outputs: ./out/*.jpg (16:9 crops), kbA.mp4, panB.mp4, out.mp4 (1920x1080, H.264; tested at 25 fps, UNVERIFIED at 24).
# Frame rate: the project rate is 24 fps (DECISIONS.md W-14, S-01). The commands below are the tested 25 fps form;
#   after this recipe is re-run at 24 on the maker's PC, d=125 becomes d=120 and fps=25 becomes fps=24 (and on/124 becomes on/119).
#   Do not change the guard values before the re-run; do not search-and-replace.
# Rules: crop to the output shape BEFORE zoompan (a 3:2 photo stretches about 18 percent otherwise);
#   upscale to 6000 px before zoompan (standard workaround; the un-upscaled case was not tested).

mkdir -p out   # added by scribe so the batch line has a target folder (TODO(verify on the maker's PC))

# a) batch: crop every photo to 16:9 at 3840 px
mogrify -path out/ -resize 3840x -gravity center -crop 3840x2160+0+0 +repage -quality 92 in/*.jpg

# b) push-in 5 s (tested at 25 fps with d=125, UNVERIFIED at 24: project rate 24 means d=120, fps=24 after the re-run; crop to the output aspect FIRST; upscale; then zoompan)
ffmpeg -loop 1 -i photoA.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z='min(1+0.0008*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 kbA.mp4

# b2) left-to-right pan at constant zoom 1.15 (tested at 25 fps with d=125 and on/124, UNVERIFIED at 24: d=120 and on/119 after the re-run)
ffmpeg -loop 1 -i photoB.jpg -vf "crop=iw:iw*9/16,scale=6000:-1,zoompan=z=1.15:x='(iw-iw/zoom)*on/124':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080:fps=25,format=yuv420p" -t 5 -c:v libx264 -crf 18 panB.mp4

# c) 1 s dissolve starting at 4 s (other transitions: wipeleft, fadeblack, circleopen, dissolve ...)
ffmpeg -i kbA.mp4 -i panB.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
