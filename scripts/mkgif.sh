#!/usr/bin/bash
# Video to GIF script using FFmpeg and GIMP to optimize
# By ISSOtm (Eldred Habert), licensed Creative Commons Zero as of 2021-09-01
# Usage: mkgif.sh kitten.webm kitten.gif
ffmpeg -y -i "$1" -c:v huffyuv -an /tmp/gif.avi
ffmpeg -y -i /tmp/gif.avi -filter_complex "[0:v] palettegen=255" /tmp/gif.png
ffmpeg -y -i /tmp/gif.avi -i /tmp/gif.png -filter_complex "[0:v][1:v] paletteuse=bayer:4" /tmp/gif.gif
gimp -nib "
(let* ((img      (car (gimp-file-load 1 \"/tmp/gif.gif\" \"/tmp/gif.gif\")))
       (drawable (car (gimp-image-get-active-drawable img))))
      (if (= 1 (car (gimp-drawable-is-indexed drawable)))
          (gimp-image-convert-rgb img)
          ())
      (gimp-image-convert-indexed img 1 0 255 0 0 \"\")
      (let* ((img (car (plug-in-animationoptimize 1 img 0))) (drawable (car (gimp-image-get-active-drawable img))))
            (file-gif-save 1 img drawable \"$2\" \"$2\" 0 1 100 0))
(gimp-quit 1))"
