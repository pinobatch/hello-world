/*
pngtrim.c
PNG image trimmer
By ax6, February 2021
Original: https://gist.github.com/aaaaaa123456789/778f18b4a1175cd1e8863c8ec4cd3bd3
License: Public domain dedication
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <stdint.h>

#if __STDC_VERSION__ >= 201112L
  #define noreturn _Noreturn void
#else
  #define noreturn void
#endif

struct buffer {
  size_t length;
  unsigned char data[];
};

int main(int, char **);
noreturn error_exit(int, const char *, ...);
struct buffer * read_data_from_file(const char *);
int write_data_to_file(const char *, const struct buffer *);
struct buffer * trim_PNG(const struct buffer * buffer);
int skippable_chunk(const unsigned char *);

int main (int argc, char ** argv) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s file.png\n", *argv);
    return 2;
  }
  struct buffer * original = read_data_from_file(argv[1]);
  if (!original) error_exit(1, "could not read file %s", argv[1]);
  struct buffer * trimmed = trim_PNG(original);
  free(original);
  if (!trimmed) error_exit(1, "file %s does not contain valid PNG data", argv[1]);
  int rv = write_data_to_file(argv[1], trimmed);
  free(trimmed);
  if (!rv) error_exit(1, "could not write to file %s", argv[1]);
  return 0;
}

noreturn error_exit (int error_code, const char * error, ...) {
  va_list ap;
  va_start(ap, error);
  fputs("error: ", stderr);
  vfprintf(stderr, error, ap);
  va_end(ap);
  fputc('\n', stderr);
  exit(error_code);
}

struct buffer * read_data_from_file (const char * filename) {
  FILE * fp = fopen(filename, "rb");
  if (!fp) return NULL;
  struct buffer * result = NULL;
  if (fseek(fp, 0, SEEK_END)) goto done;
  long size = ftell(fp);
  if (size < 0) goto done;
  rewind(fp);
  if (!(result = malloc(sizeof *result + size))) error_exit(3, "out of memory");
  result -> length = size;
  unsigned char * buf = result -> data;
  while (size) {
    int readsize = (size >= 0x10000) ? 0x10000 : size;
    int rv = fread(buf, 1, readsize, fp);
    if (rv <= 0) {
      free(result);
      fclose(fp);
      return NULL;
    }
    buf += rv;
    size -= rv;
  }
  done:
  fclose(fp);
  return result;
}

int write_data_to_file (const char * filename, const struct buffer * data) {
  FILE * fp = fopen(filename, "wb");
  if (!fp) return 0;
  const unsigned char * buf = data -> data;
  size_t remaining = data -> length;
  while (remaining) {
    int writesize = (remaining >= 0x10000) ? 0x10000 : remaining;
    int rv = fwrite(buf, 1, writesize, fp);
    if (rv <= 0) {
      fclose(fp);
      return 0;
    }
    buf += writesize;
    remaining -= writesize;
  }
  fclose(fp);
  return 1;
}

struct buffer * trim_PNG (const struct buffer * buffer) {
  if (buffer -> length < 8) return NULL;
  struct buffer * result = malloc(sizeof *result + buffer -> length);
  if (!result) error_exit(3, "out of memory");
  const unsigned char header[] = {0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a};
  if (memcmp(buffer -> data, header, sizeof header)) goto error;
  const unsigned char * current = buffer -> data + 8;
  size_t remaining = buffer -> length - 8;
  memcpy(result -> data, header, sizeof header);
  unsigned char * wp = result -> data + sizeof header;
  result -> length = sizeof header;
  while (remaining) {
    if (remaining < 4) goto error;
    uint32_t chunk_length = ((uint32_t) *current << 24) | ((uint32_t) current[1] << 16) | ((uint32_t) current[2] << 8) | current[3];
    chunk_length += 12; // length, type, CRC
    if (remaining < chunk_length) goto error;
    if (!skippable_chunk(current + 4)) {
      memcpy(wp, current, chunk_length);
      wp += chunk_length;
      result -> length += chunk_length;
    }
    current += chunk_length;
    remaining -= chunk_length;
  }
  return result;
  error:
  free(result);
  return NULL;
}

int skippable_chunk (const unsigned char * chunkID) {
  #define PRESERVE_CHUNK(ID) \
    if (!memcmp(chunkID, (unsigned char []) {(ID) >> 24, ((ID) >> 16) & 0xff, ((ID) >> 8) & 0xff, (ID) & 0xff}, 4)) return 0;
  // public and critical chunks are not skippable
  if (!((*chunkID & 0x20) || (chunkID[1] & 0x20))) return 0;
  // we don't want to lose background or transparency info
  PRESERVE_CHUNK(0x624b4744); // bKGD
  PRESERVE_CHUNK(0x74524e53); // tRNS
  // APNG is a bit... special... and thus we handle their chunks too to avoid breaking APNGs disguised as PNGs
  PRESERVE_CHUNK(0x6163544c); // acTL
  PRESERVE_CHUNK(0x6663544c); // fcTL
  PRESERVE_CHUNK(0x66644154); // fdAT
  // everything else is skippable and can be dropped
  return 1;
}