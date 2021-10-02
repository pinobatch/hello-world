#!/usr/bin/env python3
"""
Making one argparse argument that can be either positional or optional

I'm trying to make a program in Python 3.5 (the Python version
shipped by Debian 9) that takes two command line arguments: an input
file name and an output file name.

* The input file name must either precede the output file name or
  itself be preceded by `-i`.
* The output file name is optional.  If present, and the input file
  name is not preceded by `-i`, it must either follow the input file
  name or itself be preceded by `-o`.

Thus I want to accept the following command lines:

    programname.py infilename
    programname.py -i infilename
    programname.py infilename outfilename
    programname.py -i infilename outfilename
    programname.py infilename -o outfilename
    programname.py -i infilename -o outfilename
    programname.py outfilename -i infilename
    programname.py -o outfilename -i infilename
    programname.py -o outfilename infilename

But I can't tell from the
[documentation of the `argparse` module](https://docs.python.org/3/library/argparse.html#argparse-remainder)
how to express this in arguments to `add_argument()`.
When I give two names for a single argument, one positional and one
named, `add_argument()` raises an exception:

    ValueError: mutually exclusive arguments must be optional

I searched Stack Overflow for similar questions and found
[hpaulj's answer](https://stackoverflow.com/a/47314075/2738262) to
"Python argparse - mandatory argument - either positional or optional",
which uses a group of two mutually exclusive arguments, one
positional and one named.  But trying to parse
`-i infilename outfilename` or even `--help` with a parser built
this way produces an exception with 9 to 12 layers of traceback
inside `argparse.py`:

    IndexError: list index out of range

The deprecated `optparse` module stored positional arguments in a
separate list, which code that runs after parsing could read to fill
in each argument that `is None`.  The direct counterpart to this list
in `argparse` is
`parser.add_argument('args', nargs=argparse.REMAINDER)`.
Is handling positional arguments manually after calling
`parse_args()` the only way to accept all four command lines shown
above using `argparse`?
"""
import argparse
import traceback

def mkparser1():
    """Raise an error.

ValueError: invalid option string 'infilename': must start with a character '-'
"""
    parser = argparse.ArgumentParser()
    parser.add_argument("infilename", "-i", metavar="INFILE")
    parser.add_argument("outfilename", "-o", required=False, metavar="OUTFILE")
    return parser

def mkparser2():
    """Do not raise an error but return an inadequate parser.

When asked -i infilename outfilename
"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("infilename", nargs="?", metavar="INFILE")
    group.add_argument('-i', dest="infilename", metavar="INFILE")
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("outfilename", nargs="?", metavar="OUTFILE")
    parser.add_argument("-o", dest="outfilename", metavar="OUTFILE")
    return parser

def test():
    parser = mkparser2()
    argstrings = [
        "infilename",
        "-i infilename",
        "infilename outfilename",
        "-i infilename outfilename",
        "infilename -o outfilename",
        "-i infilename -o outfilename",
        "outfilename -i infilename",
        "-o outfilename -i infilename",
        "-o outfilename infilename",
        "--help",
    ]
    for s in argstrings:
        print("for", s)
        try:
            pargs = parser.parse_args(s.split())
        except Exception as e:
            traceback.print_exc()
        else:
            print("infilename is %s and outfilename is %s"
                  % (pargs.infilename, pargs.outfilename))

if __name__=='__main__':
    test()
