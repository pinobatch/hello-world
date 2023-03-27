Hello World with cstdio and iostream
====================================

These programs demonstrate the difference in executable size between
a C++ program using `<cstdio>`, the I/O library that C++ inherits
from C, and an equivalent program using `<iostream>`, a newer I/O
library introduced with C++.  At times, C++ experts such as Scott
Meyers used to deprecate `<cstdio>` as legacy, unsafe, and a code
smell.  However, if you seek to pack several executables into an
8 megabyte package for distribution to your Windows-using colleagues
in your project's Discord server, the larger binary size of
`<iostream>` becomes noticeable.

Build
-----

First install MinGW-w64.  Under Ubuntu:

    sudo apt install g++-mingw-w64

Because Microsoft Windows does not ship with a standard library
suitable for dynamic linking, we link GNU libstdc++ statically.
This also requires linking libgcc statically to support structured
exception handling.

    x86_64-w64-mingw32-g++ -Wall -s -Os -ffunction-sections -Wl,--gc-sections hello-cstdio.cpp -o hello-cstdio.exe
    x86_64-w64-mingw32-g++ -Wall -s -Os -ffunction-sections -static-libstdc++ -static-libgcc -Wl,--gc-sections hello.cpp -o hello.exe

Results
-------

Under x86_64-w64-mingw32-g++ (GCC) 10-win32 20220324, as distributed
in Ubuntu 22.10:

- `hello-cstdio.exe`, which uses `<cstdio>`, is 13824 bytes.
- `hello.exe`, which uses `<iostream>`, is 893952 bytes.

Copyright 2023 Damian Yerrick.  Permission is granted to use this
software for any purpose, as if it were in the public domain,
pursuant to the Unlicense. <http://unlicense.org/>
