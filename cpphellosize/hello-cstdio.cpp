/* to build and run:

sudo apt install g++-mingw-w64
x86_64-w64-mingw32-g++ --version
x86_64-w64-mingw32-g++ -Wall -s -Os -ffunction-sections -Wl,--gc-sections hello-cstdio.cpp -o hello-cstdio.exe
wine hello-cstdio.exe
wc -c hello-cstdio.exe

output:
x86_64-w64-mingw32-g++ (GCC) 10-win32 20220324
[GPL notice omitted]
hello world
13824 hello-cstdio.exe

*/
#include <cstdio>
int main() { std::puts("hello world"); return 0; }
