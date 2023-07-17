#!/usr/bin/env python3
"""
Tucky, a simple video encoder
written by Damian Yerrick in 2015, ported to Python 3 in 2023
"""
from contextlib import closing
import shlex, subprocess, json, os, sys

edl_filename = 'Shorts.tucky.json'
with_safearea = False
# if nonzero, force all clip lengths to that length
introscan = 0
# crop assumes the final output scales to sz
sz = (480,648)
# actual encode scales to encode_sz, which can be smaller when previewing
encode_sz = (480,648)
# output frame rate
framerate = 30
# normally 1; increase this to use fewer fps when previewing
frameratefactor = 1
# seconds per contact sheet
contact_period = 3
contact_ht = 36

if False:
    frameratefactor = 2
    encode_sz = (320, 180)
    with_safearea = True

timecode_font_name = "/home/pino/.local/share/fonts/ComicMono-Bold.ttf"
timecode_font_name = None
subtitle_font_name = "/home/pino/.local/share/fonts/Jester.ttf"
ffmpeg = 'ffmpeg'

outspec = "-c:v zmbv tucky-out.avi"
##outspec = "-c:v libx264 -movflags +faststart tucky-out.mp4"
##outspec = "-crf 16 -b:v 800k -threads 2 tucky-out.webm"
enc_cmd = (r"""%s -f rawvideo -r %f -pix_fmt rgb24 -s "%dx%d" -y -an -i - %s"""
           % (ffmpeg, framerate / frameratefactor, encode_sz[0], encode_sz[1], outspec))
args = shlex.split(enc_cmd)

# each row of panscan is time, speed (1=normal),
# digital zoom factor (1=1:1),  x position (0-1), y position (0-1),
# blur width (640=max detail)
# or a (time, None) to skip a segment entirely
with open(edl_filename, 'r') as infp:
    segs2 = json.load(infp)

def searchlerp(followdata, t):
    import bisect
    followdata_key = (t,)
    endidx = bisect.bisect_right(followdata, followdata_key)
    startidx = max(0, endidx - 1)
    endidx = min(len(followdata) - 1, endidx)
    startrow = list(followdata[startidx])
    if startrow[1] is None:
        return (None, startidx, startrow)
    startrow[5] = startrow[5] or -(-encode_sz[0] // 2)
    endrow = list(followdata[endidx])
    if endrow[1] is None:
        endrow = startrow
    endrow[5] = endrow[5] or -(-encode_sz[0] // 2)
    if endrow[0] > startrow[0]:
        lerpfac = (t - startrow[0]) / (endrow[0] - startrow[0])
        lerped = [a + lerpfac * (b - a)
                  for a, b in zip(startrow[1:], endrow[1:])]
    else:
        lerped = list(startrow[1:])
    return lerped

def getcrop(followdata, t, in_w, in_h, out_w, out_h):
    if followdata:
        row = searchlerp(followdata, t)
        if row[0] is None:
            return row
    else:
        row = [1.0, 1.0, 0.5, 0.5, None]
    (speed, zoomfac, xfrac, yfrac, blur_w) = row
    out_w = int(round(out_w / zoomfac))
    out_h = int(round(out_h / zoomfac))
    xbase = int(round(xfrac * (in_w - out_w)))
    ybase = int(round(yfrac * (in_h - out_h)))
    return (speed, xbase, ybase, out_w, out_h, blur_w or out_w)

def test_getcrop():
    part7pans = segs2[6]['panscan']
    for i in range(270):
        t = i / 2.0
        cropped = getcrop(part7pans, t, 960, 360, 640, 360)
        print("time: %5.1f; lerped: %s" % (t, cropped))
    
def crop_frame(framedata, in_w, out_w, out_h, in_x=None, in_y=None):
    rowlength = 3 * out_w
    in_h = len(framedata) // (3 * in_w)
    if in_x is None:
        in_x = (in_w - out_w) // 2
    if in_y is None:
        in_y = (in_h - out_h) // 2
    out_lines = []

    # Pad at top if necessary
    if in_y < 0:
        out_lines.append('\0' * rowlength * -in_y)
        out_h += in_y
        in_y = 0

    # Generate padding for sides if necessary
    left_border = right_border = b''
    if in_x < 0:
        left_border = bytes(3 * -in_x)
        out_w += in_x
        in_x = 0
    if out_w > in_w:
        right_border = bytes(out_w - in_w)
        out_w = in_w

    # Crop each line
    lines_to_copy = min(out_h, in_h)
    in_base = (in_w * in_y + in_x) * 3
    assert in_base >= 0
    in_offsets = range(in_base, in_base + lines_to_copy * in_w * 3, in_w * 3)
    out_lines.extend(
        b''.join((left_border, framedata[i:i + out_w * 3], right_border))
        for i in in_offsets
    )

    if out_h > lines_to_copy:
        # pad at bottom
        out_lines.append(bytes(rowlength * (out_h - lines_to_copy)))
    return b''.join(out_lines)

def motion_crop(frames, insize):
    from pygame.image import fromstring as strtosurface
    # yes, it's still called fromstring in Python 3 Pygame
    from pygame.transform import smoothscale, average_surfaces as motionblur

    # Keep only first frame if only two frames, to avoid artifacts
    # in frameratefactor
    if len(frames) <= frameratefactor:
        frames = frames[0:1]
    croppedsurfs = [
        strtosurface(crop_frame(framedata, insize[0],
                                crop_w, crop_h, in_x, in_y),
                     (crop_w, crop_h), 'RGB')
        for ((speed, in_x, in_y, crop_w, crop_h, blur_w), framedata)
        in frames
    ]
    crop_w = frames[0][0][3]
    blur_w = frames[0][0][5]
    frames = None

    # Scale surfaces to blur them
    if min(encode_sz[0], crop_w) > blur_w * 2:
        blur_sz = (int(round(blur_w)), int(round(blur_w * crop_h / crop_w)))
    else:
        blur_sz = encode_sz

##    scalecount = [im.get_size() for im in croppedsurfs if im.get_size() != blur_sz]
##    if scalecount:
##        print("%d of %d need scaling: %s"
##              % (len(scalecount), len(croppedsurfs), repr(scalecount)))

    blurredsurfs = [smoothscale(im, blur_sz)
                    if im.get_size() != blur_sz
                    else im
                    for im in croppedsurfs]

    # Motion blur surfaces in accum buffer
    # but only if blurring more than the frame rate
    sumsurf = (motionblur(blurredsurfs)
               if len(blurredsurfs) > 1
               else blurredsurfs[0])
    if sumsurf.get_size() != encode_sz:
        sumsurf = smoothscale(sumsurf, encode_sz)

    return sumsurf

def fade_frame(from_frame, to_frame, from_strength):
    import pygame
    from_frame.set_alpha(int(round(255 * from_strength)))
    to_frame.blit(from_frame, (0, 0))
    return to_frame

def render_multiline_subtitle(font, lines, color=(255, 255, 255), lh=None):
    from pygame import Surface, SRCALPHA
    from pygame.transform import smoothscale
    from pygame.image import save as imsave

    offsets = [(1, 0), (3, 0), (0, 1), (5, 2), (0, 3), (5, 4), (2, 5), (4, 5)]
    lh = lh or font.get_linesize() // 2
    if isinstance(lines, basestring):
        lines = lines.split('\n')

    imsz = ((max(font.size(line)[0] for line in lines) + 6) // 2 * 2,
            len(lines) * lh * 2 + 6)
    shadowtmp1 = Surface(imsz, SRCALPHA, 32)
    for i, txt in enumerate(lines):
        ovl = font.render(txt, True, (0, 0, 0))
        dstpos = ((imsz[0] - ovl.get_width()) // 2 - 2,
                  i * lh * 2)
        shadowtmp1.blit(ovl, dstpos)
        del ovl
    
    out = Surface(imsz, SRCALPHA, 32)
    for dstpos in offsets:
        out.blit(shadowtmp1, dstpos)
    del shadowtmp1
    for i, txt in enumerate(lines):
        ovl = font.render(txt, True, color)
        dstpos = ((imsz[0] - ovl.get_width()) // 2,
                  i * lh * 2 + 2)
        out.blit(ovl, dstpos)
    
    out = smoothscale(out, (out.get_width() // 2, out.get_height() // 2))
    return out

framebytes = encode_sz[0] * encode_sz[1] * 3

class StillFrameSource(object):
    def __init__(self, filename, framesize=None, skiptime=0, keeptime=None, vf=None):
        from pygame.image import load as imload, tostring as surfacetostr
        self.keeptime = int(keeptime * framerate)
        im = imload(filename)
        self.framesize = im.get_size()
        self.imdata = surfacetostr(im, "RGB")

    def __iter__(self):
        return self

    def __next__(self):
        if self.keeptime <= 0:
            self.close()
        if not self.imdata:
            raise StopIteration
        self.keeptime -= 1
        return self.imdata

    def close(self):
        self.imdata = None

    __del__ = close

class SolidFrameSource(StillFrameSource):
    import re as _re

    hexcolor6RE = _re.compile('#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$')
    hexcolor3RE = _re.compile('#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])$')

    color_names = {
        "aqua": (0, 255, 255), "black": (0, 0, 0), "blue": (0, 0, 255), 
        "cyan": (0, 255, 255), "fuchsia": (255, 0, 255), "gray": (128, 128, 128),
        "green": (0, 128, 0), "lime": (0, 255, 0), "magenta": (255, 0, 255),
        "maroon": (128, 0, 0), "navy": (0, 0, 128), "olive": (128, 128, 0),
        "orange": (255, 165, 0), "purple": (128, 0, 128), "red": (255, 0, 0),
        "silver": (192, 192, 192), "teal": (0, 128, 128), "white": (255, 255, 255),
        "yellow": (255, 255, 0)
    }

    @classmethod
    def translate_color(cls, colorspec):
        if isinstance(colorspec, (tuple, list)):
            if len(colorspec) != 3:
                raise ValueError("color must have 3 components")
            if not all(0 <= c <= 255 for c in colorspec):
                raise ValueError("components must be 0-255")
            return tuple(colorspec)
        m = cls.hexcolor6RE.match(colorspec)
        if m:
            return tuple(int(lvl, 16) for lvl in m.groups())
        m = cls.hexcolor3RE.match(colorspec)
        if m:
            return tuple(int(lvl, 16) * 17 for lvl in m.groups())
        return cls.color_names[colorspec]

    def __init__(self, filename, framesize=None, skiptime=0, keeptime=None, vf=None):
        rgb = bytes(self.translate_color(filename))
        self.keeptime = int(keeptime * framerate)
        self.framesize = framesize
        self.imdata = rgb * (framesize[0] * framesize[1])

class FFmpegFrameSource(object):
    def __init__(self, filename, framesize, skiptime=0, keeptime=None, vf=None, gray=False):
        import subprocess
        args = [ffmpeg, '-v', 'error', '-i', filename]
        if skiptime > 0:
            args.extend(['-ss', str(skiptime)])
        if keeptime:
            args.extend(['-t', str(keeptime)])
        if vf:
            args.extend(['-vf', vf])
        args.extend(['-an', '-f', 'rawvideo',
                     '-pix_fmt', 'gray' if gray else 'rgb24', '-'])
        self.framesize = framesize
        try:
            cnpg = subprocess.CREATE_NEW_PROCESS_GROUP
        except AttributeError:
            cnpg = 0
        targs = shlex.join(args)
        print(targs)
        self.inpipe = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       creationflags=cnpg)
        self.par = 1
        self.channels = 1 if gray else 3

    def __iter__(self):
        return self

    def __next__(self):
        if not self.inpipe:
            raise StopIteration
        inbytes = self.framesize[0] * self.framesize[1] * self.channels
        rframe = self.inpipe.stdout.read(inbytes)
        if len(rframe) < inbytes:
            self.close()
            raise StopIteration
        return rframe

    def close(self):
        if not self.inpipe: return
        # Send a Ctrl+C signal to the decoding FFmpeg process
        # and wait for it to end
        try:
            from signal import CTRL_C_EVENT as SIGINT
        except ImportError:
            from signal import SIGINT
        self.inpipe.send_signal(SIGINT)
        self.inpipe.communicate()
        self.inpipe = None

    __del__ = close

def get_framesrc_class(filename):
    from os.path import splitext

    try:
        csp = SolidFrameSource.translate_color(filename)
    except (ValueError, KeyError) as e:
        pass
    else:
        return SolidFrameSource    

    name, ext = splitext(filename)
    ext = ext.lstrip('.').lower()
    if ext in ['jpg', 'jpeg', 'gif', 'png', 'bmp']:
        return StillFrameSource
    if ext in ['avi', 'mov', 'vob', 'ts', 'mpg', 'mp4', 'flv', 'ogv',
               'webm', 'mkv']:
        return FFmpegFrameSource
    raise ValueError("unknown extension " + ext)

def draw_safearea(frame):
    """Add 5% overscan markers to each side."""
    from pygame.draw import rect

    w, h = frame.get_size()
    leftedge = w // 20
    topedge = h // 20
    bounds = (leftedge, topedge, w - 2 * leftedge, h - 2 * topedge)
    rect(frame, (0, 0, 0), bounds, 1)

def decode_segment(framesrc, panscan=None, subs=None, segtitle=None):
    from pygame.font import init as fi, get_init as wi, Font

    subs = subtitle_font_name and subs
    if (subs or timecode_font_name) and not wi():
        fi()
        
    timecode_font = (Font(timecode_font_name, encode_sz[1] // 15)
                     if timecode_font_name
                     else None)
    subtitle_font = (Font(subtitle_font_name, 2 * encode_sz[1] // 15)
                     if subs
                     else None)
    subs = iter(subs) if subs else None

    cur_subtitle = sub_im = None
    outtime = 0
    framesread = 0
    rdata = []
    speedupfactor = 1
    last_ten = 0
    insize = framesrc.framesize
    crop_width = int(round(sz[0] / framesrc.par))
    last_panscan_null_row = 0
    
    if timecode_font and segtitle:
        from pygame import Surface, SRCALPHA
        ovl = timecode_font.render(segtitle, True, (0, 0, 0))
        segtitle_sz = (ovl.get_width() + 2, ovl.get_height() + 2)
        segtitle_img = Surface(segtitle_sz, SRCALPHA, 32)
        segtitle_img.blit(ovl, (2, 2))
        ovl = timecode_font.render(segtitle, True, (255, 255, 255))
        segtitle_img.blit(ovl, (0, 0))
        ovl = None
    else:
        segtitle_img = None

    for rframe in framesrc:
        if not isinstance(rframe, bytes):
            print("%s yielded unexpected frame type %s"
                  % (type(framesrc).__name__, type(rframe).__name__),
                  file=sys.stderr)
        srctime = framesread / framerate
        cropparams = getcrop(panscan, srctime,
                             insize[0], insize[1], crop_width, sz[1])
        framesread += 1
        if cropparams[0]:
            rdata.append((cropparams, rframe))
        else:
            rownum = cropparams[1]
            if last_panscan_null_row < rownum or outtime == 0:
                last_panscan_null_row = rownum
                rowdata = cropparams[2][2:]
                if rowdata:
                    yield rowdata
            outtime += 1
        if framesread // (10 * framerate) > last_ten:
            last_ten = (10 * framerate)
            print("%d" % (10 * last_ten))
        if framesread <= outtime:
            continue

        speed = sum(row[0][0] for row in rdata) * frameratefactor / len(rdata)
        while framesread > outtime:
            if speed < 1:
                while framesread > outtime:
                    cropparams = getcrop(panscan, outtime / framerate,
                                         insize[0], insize[1], crop_width, sz[1])
                    if cropparams[0]:
                        rdata[0] = (cropparams, rdata[0][1])
                        break
                    outtime += speed
            frame = motion_crop(rdata, insize)
            if speed >= 1:
                del rdata[:]

            if with_safearea:
                draw_safearea(frame)
            if timecode_font:
                timecode_text = "%.2f" % srctime
                ovl = timecode_font.render(timecode_text, True, (0, 0, 0))
                timecode_x = encode_sz[0] - ovl.get_width()
                frame.blit(ovl, (timecode_x, 2))
                ovl = timecode_font.render(timecode_text, True, (255, 255, 255))
                frame.blit(ovl, (timecode_x - 2, 0))
                ovl = None
            if segtitle_img:
                frame.blit(segtitle_img, (0, 0))
            if subs:
                if cur_subtitle and srctime >= cur_subtitle[0][1]:
                    cur_subtitle = sub_im = None
                try:
                    cur_subtitle = cur_subtitle or subs.next()
                except StopIteration:
                    subs = None
            if cur_subtitle and srctime >= cur_subtitle[0][0]:
                if len(cur_subtitle) >= 3 and cur_subtitle[2]:
                    subcolor = SolidFrameSource.translate_color(cur_subtitle[2])
                else:
                    subcolor = (255, 255, 128)
                if not sub_im:
                    sub_im = render_multiline_subtitle(
                        subtitle_font, cur_subtitle[1], subcolor
                    )
                dstpos = ((encode_sz[0] - sub_im.get_width()) // 2,
                          encode_sz[1] - (encode_sz[1] // 12) - sub_im.get_height())
                frame.blit(sub_im, dstpos)
            yield frame
            outtime += speed
        del rdata[:]

def write_contactsheets(frames, filename):
    import pygame
    n_cols = 10
    in_w, in_h = frames[0].get_size()
    num_rows = -(-len(frames) // n_cols)
    out = pygame.Surface((in_w * n_cols, (in_h + 4) * num_rows))
    out.fill((223, 223, 223))
    x = y = 0
    for framedata in frames:
        out.blit(framedata, (x * in_w, y * (in_h + 4) + 2))
        x += 1
        if x >= n_cols:
            x = 0
            y += 1

    pygame.image.save(out, filename)

def main():
    import time
    from pygame.transform import smoothscale
    from pygame.image import tostring as surfacetostr
    enabled_segs = [seg for seg in segs2 if not seg.get('disable')]
    total_keeptime = sum(seg['keeptime'] for seg in enabled_segs)
    coding_start_time = time.time()
    encpipe = subprocess.Popen(args, stdin=subprocess.PIPE)
    accum_keeptime = 0
    frames_till_contact = 0
    contactsheets = []
    fadeinq = []
    num_frames = 0
    framesrc = None
    try:
        for seg in enabled_segs:

            # Set up decode job
            insize = seg.get('insize', sz)
            skiptime = seg.get('skiptime', 0)
            try:
                keeptime = introscan or seg['keeptime']
            except KeyError:
                ttime = 'the remainder'
            else:
                ttime = '%.2f seconds' % keeptime
            vf = seg.get('vf')
            panscan = seg.get('panscan')
            inpar = seg.get('inpar', 1)
            try:
                inpar = inpar[0] / inpar[1]
            except TypeError:
                pass
            panscan = panscan and [tuple(row) for row in panscan]
            finalfadeoutlen = int(seg.get('fadetime', 0) * framerate // frameratefactor)
            fadeinlen = len(fadeinq)
            if fadeinlen:
                print("fading %d frames from previous clip" % fadeinlen)

            panscan_maxfadetime = 0
            if panscan:
                panscan_fades = [
                    row[3] for row in panscan
                    if row[1] is None and len(row) > 2 and row[2] == 'fade'
                ]
                if panscan_fades: panscan_maxfadetime = max(panscan_fades)
                if panscan_maxfadetime > 0:
                    print("longest internal dissolve: %.2f s"
                          % (panscan_maxfadetime,))
            fadeinq_len = max(finalfadeoutlen, int(panscan_maxfadetime * framerate // frameratefactor))

            print("Seeking %.2f seconds into %s"
                  % (seg.get('skiptime', 0), seg['file']))
            framereader = get_framesrc_class(seg['file'])
            framesrc = framereader(seg['file'], insize, skiptime, keeptime, vf)
            framesrc.par = inpar
            encpipe.stdin.flush()
            with_vf = "\nwith filter %s" % vf if vf else ''
            print("Transcoding %s%s" % (ttime, with_vf))
            if fadeinq_len:
                print("holding %d frames for dissolves" % fadeinq_len)

            this_seg_frames = 0
            outputq = []
            if fadeinlen or finalfadeoutlen:
                print("fade in %d, out %d" % (fadeinlen, finalfadeoutlen))
            try:
                segtitle = seg['segtitle']
            except KeyError:
                segtitle = os.path.splitext(os.path.basename(seg['file']))[0]
            outframes = decode_segment(framesrc, panscan, seg.get('subtitles'),
                                       segtitle)
            for framedata in outframes:
                # Handle dissolve within clip
                if isinstance(framedata, list):
                    if framedata[0] == 'fade':
                        fadeoutlen = int(framedata[1]  * framerate // frameratefactor)
                        fadeinq.extend(outputq[-fadeoutlen:])
                        fadeinlen = len(fadeinq)
                        del outputq[-fadeoutlen:]
                        print("Sending %d frames to internal dissolve"
                              % (fadeoutlen))
                    else:
                        print("Got list instead of frame: %s" % repr(framedata))
                    continue
                
                # Handle dissolve from previous clip
                if fadeinq:
                    fadealpha = (len(fadeinq) - .5) / fadeinlen
                    framedata = fade_frame(fadeinq.pop(0), framedata, fadealpha)

                # Queue up frames for dissolve to next clip
                outputq.append(framedata)
                if len(outputq) <= fadeinq_len: continue
                framedata = outputq.pop(0)
                encpipe.stdin.write(surfacetostr(framedata, 'RGB'))
                num_frames += 1
                this_seg_frames += 1
                if frames_till_contact <= 0:
                    frames_till_contact += framerate * contact_period // frameratefactor
                    contact_sz = (int(round(encode_sz[0] * contact_ht / encode_sz[1])),
                                  contact_ht)
                    contactsheets.append(smoothscale(framedata, contact_sz))
                frames_till_contact -= 1
                framedata = None
            framesrc.close()
            framesrc = None

            # Pass fade-out frames from the output queue to the next
            # segment's fade-in, and encode frames in the output
            # queue that precede the dissolve.
            if finalfadeoutlen > 0:
                fadeinq.extend(outputq[-finalfadeoutlen:])
                del outputq[-finalfadeoutlen:]
            while outputq:
                encpipe.stdin.write(surfacetostr(outputq[0], 'RGB'))
                del outputq[0]

            # calculate elapsed time
            print("%.2f seconds encoded to %.2f seconds"
                  % (seg['keeptime'], this_seg_frames * frameratefactor / framerate))
            accum_keeptime += seg['keeptime']
            elapsed = time.time() - coding_start_time
            if accum_keeptime > 0:
                secs_left = ((total_keeptime - accum_keeptime)
                             * elapsed / accum_keeptime) // 1
                elapsed = elapsed // 1
                print("Elapsed %d:%02d; ETA %d:%02d"
                      % (elapsed // 60, elapsed % 60,
                         secs_left // 60, secs_left % 60))
    finally:
        if framesrc:
            framesrc.close()
        video_length = num_frames * frameratefactor // framerate
        print("Finishing encode of duration %d:%02d with %d timeline frames"
              % (video_length // 60, video_length % 60, len(contactsheets)))
        encpipe.stdin.close()
        if contactsheets:
            write_contactsheets(contactsheets, "tucky-contact.jpg")
        encpipe.communicate()

if __name__=='__main__':
    main()
