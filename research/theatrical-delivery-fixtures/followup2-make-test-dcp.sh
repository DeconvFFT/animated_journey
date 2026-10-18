#!/usr/bin/env bash
# Follow-up round 2 (2026-10-18): rebuild the DCP-o-matic 2.18.51 tests on Linux without installing anything.
# Run in an empty scratch directory. Needs: ffmpeg, dpkg-deb, apt-get download (or manual libs), python3.
# 1. Get the official command-line package (Ubuntu 24.04) and unpack it; do not install it.
#    curl -L -o dcpomatic-cli.deb "https://dcpomatic.com/dl?id=ubuntu-24.04-x86-cli&version=2.18.51"
#    dpkg-deb -x dcpomatic-cli.deb ./deb-extract
# 2. Two libraries were missing on a bare Ubuntu 24.04 container: libfmt9 and libxmlsec1t64-openssl (and libhpdf-2.3.0 for the verifier).
#    apt-get download libfmt9 libxmlsec1t64-openssl libhpdf-2.3.0 ; dpkg-deb -x each .deb into ./deb-libs
# 3. Environment (resources are found relative to the executable; libdcp resources via APPDIR):
#    export LD_LIBRARY_PATH=$PWD/deb-libs/usr/lib/x86_64-linux-gnu APPDIR=$PWD/deb-extract HOME=$PWD/home DCPO_BIN=$PWD/deb-extract/usr/bin
set -euo pipefail
B=${DCPO_BIN:?set DCPO_BIN}
# Colour-patch clip: 9 vertical bars (black, 10%, 25%, 50%, 75%, 90%, white, red, green), ProRes 422 HQ, BT.709 tagged, 2 s, stereo 24-bit.
ffmpeg -hide_banner -loglevel error -y \
 -f lavfi -i "color=c=black:s=1920x1080:r=24:d=2,format=rgb24,drawbox=x=0:y=0:w=213:h=1080:color=0x000000:t=fill,drawbox=x=213:y=0:w=213:h=1080:color=0x1a1a1a:t=fill,drawbox=x=426:y=0:w=213:h=1080:color=0x404040:t=fill,drawbox=x=639:y=0:w=213:h=1080:color=0x808080:t=fill,drawbox=x=852:y=0:w=213:h=1080:color=0xbfbfbf:t=fill,drawbox=x=1065:y=0:w=213:h=1080:color=0xe6e6e6:t=fill,drawbox=x=1278:y=0:w=213:h=1080:color=0xffffff:t=fill,drawbox=x=1491:y=0:w=213:h=1080:color=0xff0000:t=fill,drawbox=x=1704:y=0:w=216:h=1080:color=0x00ff00:t=fill,scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le" \
 -f lavfi -i "sine=f=1000:r=48000:d=2" -f lavfi -i "sine=f=500:r=48000:d=2" \
 -filter_complex "[1:a][2:a]amerge=inputs=2[a]" -map 0:v -map "[a]" \
 -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a pcm_s24le -ar 48000 -r 24 patches_prores422hq.mov
# Films: default colour preset (follows the file's BT.709 tag), and Rec. 1886 chosen by hand.
$B/dcpomatic2_create -n LJTest -c SHR --twok --container-ratio 185 -f 24 patches_prores422hq.mov -o film_default
$B/dcpomatic2_create -n LJTest -c SHR --twok --container-ratio 185 -f 24 --colourspace rec1886 patches_prores422hq.mov -o film_rec1886
# Name and settings without encoding:
$B/dcpomatic2_cli dump film_default
# Encode (4 threads), then verify and decode one frame to raw XYZ for followup2-patch_levels.py:
python3 -I followup2-measure_dcpo.py 4 film_default
python3 -I followup2-measure_dcpo.py 4 film_rec1886
$B/dcpomatic2_verify_cli -q film_default/LJTest_SHR-1_F-178_XX-XX_20_2K_*_SMPTE_OV
ffmpeg -y -i film_default/LJTest*/j2c_*.mxf -frames:v 1 -f rawvideo -pix_fmt xyz12le f709.raw
ffmpeg -y -i film_rec1886/LJTest*/j2c_*.mxf -frames:v 1 -f rawvideo -pix_fmt xyz12le f1886.raw
python3 -I followup2-patch_levels.py
