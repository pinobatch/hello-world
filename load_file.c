/*
read a file into an array
untested! by Damian Yerrick, no rights reserved
The successive doubling looks complicated compared to fseek-ftell
solution, but it's meant to be generic enough to read piped stdin
even on platforms whose C library's realloc() is slow (like Windows).
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <limits.h>

#define LOAD_FILE_MIN_SIZE 16384

/**
 * Reads the remainder of a file until EOF into freshly allocated
 * memory.  On success, returns a data pointer, writes the size into
 * out_size if not null, and sets infp's stream state to end of file.
 * On file read failure, returns NULL, sets errno, and sets infp's
 * stream state to error.   On allocation failure, returns NULL and
 * may set errno.
 */
void *load_file_by_fp(FILE infp[restrict static 1], size_t *restrict out_size) {
  size_t capacity = LOAD_FILE_MIN_SIZE;
  unsigned char *out = calloc(1, capacity);
  size_t sz = fread(out, 1, capacity, infp);
  while (!feof(infp) && !ferror(infp) && sz < SIZE_MAX) {
    size_t cap_add = capacity;  // iterative doubling for speed on MS libc
    if (cap_add > SIZE_MAX - capacity) cap_add = SIZE_MAX - capacity;
    capacity += cap_add;
    unsigned char *newout = realloc(out, capacity);
    if (!newout) goto return_error;
    out = newout;
    sz += fread(out + sz, 1, capacity - sz, infp);
  }
  if (feof(infp)) {  // successfully read the whole file
    if (out_size) *out_size = sz;
    if (sz < sizeof(size_t)) sz = sizeof(size_t);  // avoid realloc(ptr, 0) UB
    unsigned char *newout = realloc(out, sz);  // shrinkwrap allocation
    return newout ? newout : out;
  }
return_error:
  free(out);
  return 0;
}

/**
 * Reads a file from a given path into freshly allocated memory.
 * The path must be representable in the current character encoding.
 * On success, returns a data pointer, and writes size into out_size
 * if non-null.  On failure, returns NULL and may set errno.
 */
void *load_file_by_name(const char filename[restrict static 2], size_t *restrict out_size) {
  FILE *infp = fopen(filename, "rb");
  if (!infp) return 0;
  unsigned char *out = load_file_by_fp(infp, out_size);
  fclose(infp);
  return out;
}
