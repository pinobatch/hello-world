#!/usr/bin/env python3
"""
Velocity dithering exmaple

Copyright 2022 Damian Yerrick
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
"""

"""
A real-time video game for an 8-bit platform doesn't need to store
subpixel displacement, only subpixel velocity. It can use the same
subpixel displacement for all actors that move during a game tick,
adding a constant to this displacement after each tick.  This can be
viewed as a dither value.  To update an object's displacement on each
tick, a game's physics routine adds dither to subpixel velocity,
rounds down to the nearest pixel, and adds that to the displacement.

Numberphile's video about the golden ratio uses a continued fraction
argument to explain how numbers can be "more irrational" than others.
<https://www.youtube.com/watch?v=sj8Sg8qnjOg>

The golden ratio, also called phi, is defined as (sqrt(5) + 1)/2.
The inverse golden ratio 1/phi is thus (sqrt(5) + 1)/2.  To reach
all values of the dither variable, the algorithm must add an odd
value each tick.  Thus it adds 256/phi rounded to the nearest odd
number, or 159, to dither each tick.

Thus it takes four 8-bit bytes to store an actor's position and
velocity:

- X velocity (subpixels/tick), X velocity (pixels/tick)
- X displacement (pixels), X displacement (256 pixels)
- Y velocity (subpixels/tick), Y velocity (pixels/tick)
- Y displacement (pixels), Y displacement (256 pixels)

run this:
./velocity_dither.py | head -n40
"""
INV_PHI = 159
dither = 0
position, velocity = 0, 205  # Move at speed of 4/5 pixel per tick
for tick in range(256):
    # Do this for all actors
    position_add = velocity + dither
    position += position_add // 256
    print("at tick %3d, dither:%3d; effvel:%3d//256 == %d; position=%3d"
          % (tick, dither, position_add, position_add // 256, position))
    # Do this only once between each tick and the next
    dither = (dither + INV_PHI) % 256
