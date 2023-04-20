#!/usr/bin/env python3
"""
SNT to FamiTracker Namco wave converter
Copyright 2023 Damian Yerrick
insert zlib license here
"""
import os, sys, argparse

helpText = """
Converts waveforms in an SNT file made with LSDj Wave Cruncher
to text that can be pasted into FamiTracker as a Namco instrument.
"""
helpEndText = """For SNT files, see <https://github.com/psgcabal/lsdjsynths>"""

def parse_argv(argv):
    p = argparse.ArgumentParser(description=helpText, epilog=helpEndText)
    p.add_argument("input",
                   help="sequence of 16-byte GB wave RAM dumps")
    return p.parse_args(argv[1:])

def main(argv=None):
    args = parse_argv(argv or sys.argv)
    with open(args.input, "rb") as infp:
        waveforms = infp.read()
    waveforms = [waveforms[i:i + 16] for i in range(0, len(waveforms), 16)]
    waveforms = [
        [(b >> shift) & 0x0F for b in w for shift in (4, 0)]
        for w in waveforms
    ]
    wavetxt = "".join(
        "".join("%d " % sample for sample in w) + ";\n"
        for w in waveforms
    )
    print(wavetxt)

if __name__=='__main__':
    if 'idlelib' in sys.modules:
##        main("""./snttoft.py --help""".split())
        main("""./snttoft.py lsdjsynths-master/piano.snt""".split())
    else:
        main()
