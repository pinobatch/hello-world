#!/usr/bin/env python3
"""
Generate an NES emulator palette resembling the Game Boy's

Copyright 2021 Damian Yerrick
License: MIT (Expat variant)

"""
# NES colors 00, 07, 17, 27, 37, 20 from a palette generated with
# Bisqwit's web application, the same palette used in savtool.py
gbcolors = bytes.fromhex(
    "0000005a1a009f4a00ef9a49f8d5b4ffffff"
)

# 31-3C becomes 37
# 10, 21-2C, 3D becomes 27
# 00, 11-1C, 2D becomes 17
# 01-0C becomes 07


brightness_offsets = [2] + [1]*12 + [0, -4, -4]
brightnesses = [b + o for b in range(4) for o in brightness_offsets]
brightnesses[0x1D] = 0
brightnesses[0x20] = 5
brightnesses = [min(5, max(0, b)) for b in brightnesses]
print("\n".join(repr(brightnesses[i:i + 16]) for i in range(0, 64, 16)))

nescolors = b"".join(gbcolors[b * 3:b * 3 + 3] for b in brightnesses)
with open("nes_sepia.pal", "wb") as outfp:
    outfp.write(nescolors)
