/*
Duff's device, a way to express unrolled code in C

Given a straightforward loop to copy pixels to a graphics circuit,
the VAX C compiler was generating a loop with 2 instruction movw
(move word) and sobleq (subtract one and branch if less or equal,
analogous to Z80 djnz or 68K dbf).  Tom Duff found that unrolling the
loop reduced the overhead time spent in sobleq and figured out a way
to interleave the code for a single unrolled iteration with the code
for a fraction thereof.  This doubled the animation's frame rate.

Translated by Pino from pre-standard C to C99
*/

#include <stddef.h>
typedef short pixel_t;

/**
 * Copies pixel values from an array to an autoincrementing MMIO port
 * @param to    port address
 * @param from  address of pixel data
 * @param count number of pixels to copy
 */
void send_original(volatile pixel_t *restrict to,
                   const pixel_t *restrict from,
                   size_t count) {
{
  do {
    *to = *from++;
  } while (--count > 0);
}
    
void send_unrolled(volatile pixel_t *restrict to,
                   const pixel_t *restrict from,
                   size_t count) {
  size_t iterations = (count + 7) / 8;
  switch(count % 8) {
    case 0: do {
            *to = *from++;  // fall through
    case 7: *to = *from++;  // fall through
    case 6: *to = *from++;  // fall through
    case 5: *to = *from++;  // fall through
    case 4: *to = *from++;  // fall through
    case 3: *to = *from++;  // fall through
    case 2: *to = *from++;  // fall through
    case 1: *to = *from++;
    } while (--iterations > 0);
  }
}
