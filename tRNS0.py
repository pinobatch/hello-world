#!/usr/bin/env python3
"""
Tool to change a PNG image's transparent color
Copyright 2024 Damian Yerrick
License: zlib
"""
import os, sys, argparse, struct, zlib
helpText="Sets color 0 in an indexed PNG image as transparent."

def parse_argv(argv):
    p = argparse.ArgumentParser(description=helpText)
    p.add_argument("input", 
                   help="image to modify")
    p.add_argument("output", nargs="?",
                   help="output image (default: overwrite original)")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv[1:])

png_header = b'\x89PNG\r\n\x1A\n'
def png_read_chunks(infp):
    header = infp.read(8)
    if header != png_header:
        raise ValueError("expected PNG header; got %s" % header.hex())
    while True:
        chunk_size = infp.read(4)
        if len(chunk_size) < 4: return
        chunk_size = struct.unpack(">I", chunk_size)[0]
        chunk_type = infp.read(4)
        if len(chunk_type) < 4: return
        chunk_body = infp.read(chunk_size)
        if len(chunk_body) < chunk_size: return
        chunk_crc = infp.read(4)
        if len(chunk_crc) < 4: return
        chunk_crc = struct.unpack(">I", chunk_crc)[0]
        yield chunk_type, chunk_body, chunk_crc

def main(argv=None):
    args = parse_argv(argv or sys.argv)
    with open(args.input, "rb") as infp:
        chunks = list(png_read_chunks(infp))

    # Read PNG file
    out_chunks = []
    previous_tRNS = None
    new_tRNS = bytes([0])
    seen_IEND = False
    seen_first_IDAT = False
    for t, body, crc in chunks:
        # CRC covers the type and body of a chunk.  It does not cover
        # the size; the next chunk's CRC covers that.
        if args.verbose:
            expected_crc = zlib.crc32(t+body)
            print("%s size%6s crc %08X=%08X"
                  % (t.decode("ascii"), len(body), crc, expected_crc))
        if t == b'tRNS':
            previous_tRNS = body
            continue
        if t == b'IDAT' and not seen_first_IDAT:
            out_chunks.append((b'tRNS', new_tRNS))
            seen_first_IDAT = True
        out_chunks.append((t, body))
        if t == b'IEND':
            seen_IEND = True
            break

    # Validations
    if not seen_IEND or not seen_first_IDAT:
        print("tRNS0.py: %s: not a PNG image (no IDAT and IEND chunk)"
              % (args.input,), file=sys.stderr)
        exit(1)
    if new_tRNS == previous_tRNS:
        if args.verbose:
            print("tRNS0.py: %s: tRNS chunk unchanged"
                  % (args.input,), file=sys.stderr)
        if not args.output: return

    # Write PNG file
    with open(args.output or args.input, "wb") as outfp:
        outfp.write(png_header)
        for t, body in out_chunks:
            tbody = b''.join((t, body))
            outfp.write(struct.pack(">I", len(body)))
            outfp.write(tbody)
            outfp.write(struct.pack(">I", zlib.crc32(tbody)))

if __name__=='__main__':
    if 'idlelib' in sys.modules:
        main("""
./tRNS0.py -v Original_indexed_pink.png tRNS0out.png
""".split())
    else:
        main()
