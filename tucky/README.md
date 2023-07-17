Tucky is a simplistic video compositor.

FFmpeg and Pygame must be installed.

Invoking

- `edl_filename`  
  Filename of EDL
- `sz`  
  Size of the render canvas and most input videos
- `ffmpeg`  
  Command for FFmpeg decoder.  Use `ffmpeg` for system FFmpeg
- `outspec`  
  usually passed to encoder
- `enc_cmd`  
  Formula to encode raw RGB24 video of `encode_sz` size, expected
  frame rate, and `outspec` to an intermediate file for later
  remuxing.  
- `contact_period`  
  Time between frames on the contact sheet.
- `contact_ht`  
  Height in pixels of each frame on the contact sheet.

These values are often changed in preview renders:

- `encode_sz`  
  Usually set to `sz`; use a smaller size for a reduced preview.
- `frameratefactor`  
  Usually set to 1; use a higher number for a low-frame-rate preview.
- `with_safearea`  
  If true, draw a rectangle around the center 90 percent of the
  output, with edges 5% away from the picture edges.
- `timecode_font_name`  
  If not `None`, use the TrueType font with this filename to draw
  the segment name at top left.

An edit decision list (EDL) is a JSON file consisting of an array of
segments.  Each segment is an object with these keys:

- `disable`  
  Set to a nonzero value to skip this segment in a render.
- `file` (required)  
  A solid color, image file, or video file that FFmpeg can open.
- `segtitle`  
  Title of the segment.  If not specified, use filename.
- `skiptime`  
  Value of `-ss` option
- `keeptime` (required)  
  Value of `-t` option, or length to display solid color or image file
- `vf`  
  Value of `-vf` (video filter chain) option
- `insize`  
  Size of resulting video after `vf` chain completes, if not the same
  size as the virtual render output.
- `panscan`  
  Array whose elements represent
  `[starttime, speed, zoom level, x center, y center, focus]`
  where speed and zoom level are normally 1.0, the centers range from
  0.0 to 1.0 and focus can be anywhere from 2.0 to half the encode
  size, where `null` means half the encode size.
  The form `[endtime, null]` discards video from endtime to
  the starttime of the following segment.
  The form `[endtime, null, "fade", length]` dissolves the
  frames from endtime - length through endtime with the frames from
  starttime through starttime + length.
  with a fade of some sort; details are pending.
- `subtitles`  
  A list of the form `[[[starttime, endtime], text, color], ...]`
  where `starttime` and `endtime` are in seconds, `text` can be
  multiline, and color can be omitted
- `fadetime`  
  Time in seconds to overlap the end of this segment with the start
  of the next using a dissolve transition
- `par`  
  Pixel aspect ratio of input (default: 1.0)  
