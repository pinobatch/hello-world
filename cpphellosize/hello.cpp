/* to build and run:

sudo apt install g++-mingw-w64
x86_64-w64-mingw32-g++ --version
x86_64-w64-mingw32-g++ -Wall -s -Os -ffunction-sections -static-libstdc++ -static-libgcc -Wl,--gc-sections hello.cpp -o hello.exe
wine hello.exe
wc -c hello.exe

output:
x86_64-w64-mingw32-g++ (GCC) 10-win32 20220324
[GPL notice omitted]
hello world
893952 hello.exe
*/
#include <iostream>
int main() { std::cout << "hello world\n"; return 0; }
