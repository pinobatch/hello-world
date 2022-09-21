#!/usr/bin/bash
# Video to GIF script using FFmpeg and GIMP to optimize
# By ISSOtm (Eldred Habert), licensed Creative Commons Zero as of 2021-09-01
# Usage: mkvid.sh bgb-1567896789.*
files=()
for f in "$@"; do
	files+=(-i "$f")
done

set -ex
ffmpeg -f avi $files -c:v libvpx-vp9 -b:v 0 -crf 30 -pix_fmt yuv420p -pass 1 -f webm -y /dev/null
ffmpeg $files -c:v libvpx-vp9 -b:v 0 -crf 30 -pix_fmt yuv420p -pass 2 output.webm
