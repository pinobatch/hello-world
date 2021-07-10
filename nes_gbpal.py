#!/usr/bin/env python3
"""
Generate an NES emulator palette resembling the Game Boy's

Copyright 2021 Damian Yerrick
License: MIT (Expat variant)

"""
# NES colors 0B, 1A, 29, 38 from a palette generated with
# Bisqwit's web application, the same palette used in savtool.py
gbcolors = bytes.fromhex(
    "003d1007770485bc2fe4dca8"
)

# 20, 30-3C becomes 38
# 10, 21-2C, 3D becomes 29
# 00, 11-1C, 2D becomes 1A
# 01-0C, 0D, 1D, xE, xF becomes 0B
brightness_offsets = [1] + [0]*12 + [-1, -3, -3]
brightnesses = [min(3, max(0, b + o))
                for b in range(4)
                for o in brightness_offsets]

nescolors = b"".join(gbcolors[b * 3:b * 3 + 3] for b in brightnesses)
with open("nes_gb.pal", "wb") as outfp:
    outfp.write(nescolors)
