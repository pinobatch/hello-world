#!/usr/bin/env python3
"""
Rotation tool for pixel art
By Damian Yerrick

See versionText and algorithmText.

"""
from itertools import chain, zip_longest
from PIL import Image
import sys
import os
import argparse

versionText = """0.02 (2018-03-01)

Copyright 2012 Damian Yerrick
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
"""
descriptionText = "Rotates pixel art without making it blurry or jagged."
algorithmText = """%prog uses the following algorithm:

1. Enlarge the image by a factor of 8, smoothing pixel contours
   with the EPX/Scale2x algorithm.
2. Rotate the image and apply stretch factors with point sampling.
3. Apply a 3x3 pixel majority (mode) filter to smooth edges that
   were roughened by rotation.
4. Grid fitting: Loop through the rotated image to find the center
   of rotation (x, y), where x and y are in [0-7], where the fewest
   sample points fall on pixels whose neighbors differ.
5. Downsample by a factor of 8 with point sampling at this center.

This is based on the description of Xenowhirl's RotSprite, but
without single-pixel detail restoration and without special
treatment of "similar" colors at edges.
<http://forums.sonicretro.org/index.php?showtopic=8848&view=findpost&p=159754>"""


def grouper(stride, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * stride
    return zip_longest(fillvalue=fillvalue, *args)

def get_ebdfh(im, bgcolor=None):
    """Get a generator of rows of pixels in a PIL image with their neighbors.

Each result is a tuple of 5-tuples (center, above, left, right, below).
Out-of-bounds pixels are replaced with bgcolor (which defaults to
None).

"""

    px = im.getdata()
    iter(im.getdata())
    wid = im.size[0]
    blankRow = [bgcolor] * wid
    rows = list(grouper(im.size[0], px))
    rows = zip(rows, rows[1:] + [blankRow])
    prevRow = blankRow
    for (row, nextRow) in rows:
        prevPx = (bgcolor,) + row[:-1]
        nextPx = row[1:] + (bgcolor,)
        ebdfh = zip(row, prevRow, prevPx, nextPx, nextRow)
        prevRow = row
        yield ebdfh

def scale2x(im, bgcolor=None):
    """Apply Eric's Pixel Expansion (EPX) aka Scale2x to a PIL image."""

    # Need to expand each row to two rows
    outPixels = []
    for ebdfh in get_ebdfh(im):

        # This is the scale2x algorithm, equivalent to the EPX
        # algorithm used in old lucasarts games for Mac
        crossmatches = [(e,
                         b != h and d != f,
                         d if b == d and d is not None else e,
                         f if b == f and f is not None else e,
                         d if d == h and d is not None else e,
                         f if f == h and f is not None else e)
                        for (e, b, d, f, h) in ebdfh]
        row0 = [(tl, tr) if crossdiff else (e, e)
                for (e, crossdiff, tl, tr, bl, br) in crossmatches]
        row1 = [(bl, br) if crossdiff else (e, e)
                for (e, crossdiff, tl, tr, bl, br) in crossmatches]
        outPixels.extend(chain(*row0))
        outPixels.extend(chain(*row1))
        
    wid, ht = im.size
    newimg = Image.new(im.mode, (wid * 2, ht * 2))
    newimg.putdata(outPixels)
    if im.mode == 'P':
        newimg.putpalette(im.getpalette())
    return newimg

# Reference implementation of find_fewest_edges().
# Not actually used by rotpixels().
def find_edges(im, bgcolor=None):
    """Make an image highlighting pixels that don't match their neighbors."""

    outPixels = []
    for ebdfh in get_ebdfh(im, bgcolor):
        diffs = [(0 if b is None or e == b else 50)
                 + (0 if d is None or e == d else 50)
                 + (0 if f is None or e == f else 50)
                 + (0 if h is None or e == h else 50)
                 for (e, b, d, f, h) in ebdfh]
        outPixels.extend(diffs)
    newimg = Image.new('L', im.size)
    newimg.putdata(outPixels)
    return newimg

def find_fewest_edges(im, grid_w, grid_h, bgcolor=None):
    from PIL import Image

    outPixels = [[0] * grid_w] * grid_h
    for (y, ebdfh) in enumerate(get_ebdfh(im, bgcolor)):
        diffs = [(0 if b is None or e == b else 1)
                 + (0 if d is None or e == d else 1)
                 + (0 if f is None or e == f else 1)
                 + (0 if h is None or e == h else 1)
                 for (e, b, d, f, h) in ebdfh]
        diffs = [sum(o) for o in zip_longest(*grouper(grid_w, diffs))]
        y = y % grid_h
        outPixels[y] = [p + d for (p, d) in zip(outPixels[y], diffs)]
    minEdges = min(min(row) for row in outPixels)
    
    outPixels = [[(n - minEdges,
                   (2 * x - grid_w + 1) * (2 * x - grid_w + 1)
                   + (2 * y - grid_h + 1) * (2 * y - grid_h + 1), x, y)
                  for (y, n) in enumerate(row)]
                 for (x, row) in enumerate(outPixels)]
    outPixels = sorted(chain(*outPixels))
    return [row[2:] for row in outPixels[:4]]

def prove_top_left(im):
    """Prove that PIL NEAREST resizing samples at the top left.

Return a tiny red image.  If PIL NEAREST used center samples, it'd
be green.  If something else, it'd be yellow or black.

"""
    im = Image.new('RGB', (16, 16))
    r = (255,0,0)
    g = (0,255,0)
    y = (255,255,0)
    k = (0, 0, 0)
    ida = [r,y,k,k,k,k,k,y,r,y,k,k,k,k,k,y,
           y,y,k,k,k,k,k,y,y,y,k,k,k,k,k,y,
           k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,
           k,k,k,y,y,y,k,k,k,k,k,y,y,y,k,k,
           k,k,k,y,g,y,k,k,k,k,k,y,g,y,k,k,
           k,k,k,y,y,y,k,k,k,k,k,y,y,y,k,k,
           k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,
           y,y,k,k,k,k,k,y,y,y,k,k,k,k,k,y]
    im.putdata(ida*2)
    return im.resize((2, 2))

def my_rotate(im, angle=0.0, scale=1.0, inpar=1.0, outpar=1.0, outsize=None):
    """Rotate, scale, and pixel-aspect-ratio correct an image.

im -- a PIL image
angle -- angle (in anticlockwise degrees) by which to rotate
scale -- scale factor
inpar -- pixel aspect ratio of input
outpar -- pixel aspect ratio of output
outsize -- size of box for output

The transformation uses point sampling, and rotations are about
the image's center.

"""
    import math
    from PIL import Image

    outsize = outsize or im.size
    angle = -angle * math.pi / 180
    c = math.cos(angle) / scale
    s = math.sin(angle) / scale
    ow, oh = outsize
    iw, ih = im.size
    matrix = [c * outpar / inpar, s / inpar, 0, -s * outpar, c, 0]

    # stay centered
    matrix[2] = (iw - (ow * matrix[0] + oh * matrix[1])) / 2.0
    matrix[5] = (ih - (ow * matrix[3] + oh * matrix[4])) / 2.0
    t = im.transform(outsize, Image.AFFINE, matrix)
    return t

def rotpixels(im, croprect=None, outsize=None,
              angle=0.0, scale=1.0, inpar=1.0, outpar=1.0):
    """Make a smoothly rotated copy of a PIL image containing pixel art.

croprect -- tuple (left, top, right, bottom) or None
outsize -- tuple (width, height) or None
angle -- counterclockwise angle in degrees or 0.0
scale -- scale factor
inpar -- input pixel aspect ratio
outpar -- input pixel aspect ratio

If croprect is None, the entire image is used.
If outsize is None, it's based on the croprect scaled by the scale
factor, with the width adjusted to fit the difference between pixel
aspect ratios.

The algorithm is described in algorithmText.

"""
    from PIL import ImageFilter, ImageChops

    if croprect:
        im = im.crop(croprect)
    else:
        croprect = (0, 0) + im.size
    if not outsize:
        ow = (croprect[2] - croprect[0]) * scale * outpar / inpar
        oh = (croprect[3] - croprect[1]) * scale
        outsize = (int(round(ow)), int(round(oh)))
    bgc = (0, 0, 0)

    # The slow parts of this are scale2x, majority filter, and
    # find_fewest_edges.  Those would support a rewrite in C once I
    # find an image loading library that doesn't bring in a whole
    # GUI toolkit.
    
    # Enlarge the image by a factor of eight, or more in the
    # case of a huge scale factor.
    im = scale2x(scale2x(scale2x(im, bgc), bgc), bgc)
    while scale > 1.8:
        scale /= 2.0
        im = scale2x(im)

    # Rotate it nearest neighbor.
    im = my_rotate(im, angle=angle, scale=scale,
                   inpar=inpar, outpar=outpar,
                   outsize=(outsize[0] * 8, outsize[1] * 8))

    # Nearest neighbor rotation introduces roughness artifacts
    # near corners.  Use majority(3x3) filter to smooth these off.
    im = im.filter(ImageFilter.ModeFilter)

    # Find which of the 64 sampling offsets lies on the fewest edges
    offsets = find_fewest_edges(im, 8, 8)
    offx, offy = offsets[0]

    # And resize it down.
    return ImageChops.offset(im, -offx, -offy).resize(outsize)

usageText = "%prog [options] [-i] input.png [[-o] output.png]"

def parserect(s):
    m = [int(c.strip()) for c in s.split(',')]
    if (len(m) != 4
        or m[0] < 0 or m[1] < 0 or m[2] <= m[0] or m[3] <= m[1]):
        raise ValueError(repr(m))
    return tuple(m)

def parsesize(s):
    m = [int(c.strip()) for c in s.split(',')]
    if (len(m) != 2
        or m[0] <= 0 or m[1] <= 0):
        raise ValueError(repr(m))
    return tuple(m)

def getopt(argv):
    parser = argparse.ArgumentParser(usage=usageText, description=descriptionText)
    parser.add_argument("--help2", dest="help2",
                        default=False, action="store_true",
                        help="explain the algorithm in detail and exit")
    parser.add_argument("--version", action="version", version=versionText)
    parser.add_argument("-i", "--input", dest="infilename", metavar="FILE",
                      help="read image from FILE (BMP or PNG format)")
    parser.add_argument("-o", "--output", dest="outfilename", metavar="FILE",
                        help="write rotated image to FILE (if omitted, use the system's image viewer)")
    parser.add_argument("--crop", dest="croprect", type=parserect,
                        help="crop input to rectangle L,T,R,B", metavar="L,T,R,B")
    parser.add_argument("--pad", dest="outsize", type=parsesize,
                        help="crop or pad output to size W,H", metavar="W,H")
    parser.add_argument('-r', "--rotate", '--angle',
                        dest="angle", type=float, default=0.0,
                        help="rotate counterclockwise by ANGLE degrees (use -ANGLE for clockwise)", metavar="ANGLE")
    parser.add_argument('-s', "--scale",
                        dest="scale", type=float, default=1.0,
                        help="scale output by SCALE (e.g. 2.0)", metavar="SCALE")
    parser.add_argument("--in-par", dest="inpar", type=float, default=1.0,
                        help="set input pixel aspect ratio to RATIO (e.g. 1.14)",
                        metavar="RATIO")
    parser.add_argument("--out-par", dest="outpar", type=float, default=1.0,
                        help="set output pixel aspect ratio to RATIO",
                        metavar="RATIO")
    parser.add_argument("pargs", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv[1:])
    if args.help2:
        print(algorithmText.replace('%prog', prog))
        sys.exit(0)

    # Because argparse does not allow a single argument to be
    # either optional or positional, such as "[-i] INFILE",
    # handle positional arguments manually
    pargs = iter(args.pargs)
    prog = os.path.basename(sys.argv[0])
    if args.infilename is None:
        try:
            args.infilename = next(pargs)
        except StopIteration:
            parser.error("no input file; try %s --help" % prog)
    if args.outfilename is None:
        try:
            args.outfilename = next(pargs)
        except StopIteration:
            pass
    try:
        next(pargs)
    except StopIteration:
        pass
    else:
        parser.error("too many filenames")

    return args

def main(argv=None):
    opt = getopt(argv or sys.argv)
    im = Image.open(opt.infilename)
    out = rotpixels(im, croprect=opt.croprect, outsize=opt.outsize,
                    angle=opt.angle, scale=opt.scale,
                    inpar=opt.inpar, outpar=opt.outpar)
    if opt.outfilename:
        out.save(opt.outfilename)
    else:
        out.show()

if __name__=='__main__':
    main()
##    main(['rots', '--angle', '-11.25',
##          '--crop', '16, 12, 48, 44',
##          '--in-par', '1.1429', '--out-par', '1.1429', '--scale', '2',
##          "../a53vol4/tilesets/screenshots/default.png", 'rotated.png'])
