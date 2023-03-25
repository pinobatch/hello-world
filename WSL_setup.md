Setting up Windows Subsystem for Linux
======================================

How to get GNU on Windows 10 (feature update 22H2) or Windows 11
on a PC with an x86-64 (not 32-bit, not ARM) processor, at least
Nehalem or Opteron:

 1. Open Settings > Update & Security > Windows Update.
    Check for updates, install all available updates, and restart.
 2. Open Settings > Update & Security > Windows Update.
    Check for updates, install all available updates, and restart.
 3. Open Settings > Update & Security > Windows Update.
    Check for updates, install all available updates, and restart.
 4. Search the web for how to open UEFI setup on your make and model
    of computer.  Write it down, or search on a phone or tablet.
 5. Open and close Microsoft Store.  This updates the catalog of
    GNU/Linux distributions available in WSL.
 6. In PowerShell, run this command:
    wsl --install -d Ubuntu
 7. Restart.  Instead of starting Windows this time, start your
    computer's UEFI setup.
 8. Turn on Intel Virtualization Technology (Intel VT) or AMD-V.
    Save changes and exit to Windows.
 9. From the Start Menu, choose Ubuntu.
10. Type the name and password for your Linux user account within the
    virtual machine.

Inside Ubuntu, set up a Game Boy toolchain.

    sudo apt update
    sudo apt upgrade
    sudo apt install build-essential libpng-dev git pkg-config bison cc65 python3-pil
    ln -s /mnt/c/Users/pino/Desktop ~/Desktop
    mkdir -p ~/develop/assemblers
    cd ~/develop/assemblers
    git clone https://github.com/gbdev/rgbds.git
    cd rgbds
    make
    sudo make install

Test the toolchain by compiling two of Pino's projects.

    cd ~/develop
    git clone https://github.com/pinobatch/240p-test-mini.git
    git clone https://github.com/pinobatch/libbet.git
    cd libbet
    make libbet.gb
    cp libbet.gb ~/Desktop/
    cd ~/develop/240p-test-mini/gameboy
    make gb240p.gb
    cp gb240p.gb ~/Desktop/
    cd ../nes
    make 240pee.nes
    cp 240pee.nes ~/Desktop/

The virtual machine may not include support for emulators or other
graphical applications.  Install emulators in Windows to test the
built ROMs.

 1. In File Explorer, open This PC > C:
 2. Create a folder called `emulators`
 3. Inside the folder `emulators`, create a folder called
    `sameboy`
 4. In Edge, visit <https://sameboy.github.io> and follow the link
    "Downloads" then "Download for Windows".
 6. In File Explorer, open the Downloads folder, open the downloaded
    SameBoy zipfile, and drag all files into the
    `C:\emulators\sameboy` folder.
 7. In `C:\emulators\sameboy`, right-click `sameboy_debugger.exe`,
    and choose Properties.  If there is a "This file came from
    another computer" section at the bottom, check Unblock next
    to it.  Click OK.
 8. Unblock `sameboy.exe` in the same manner and run it
 9. Press Esc to open the menu, then in Options > Control Options,
    set your button bindings.
10. Drag one of the built ROMs from the desktop onto the window.
11. In Edge, visit <https://mesen.ca> and follow the link
    "Windows (Dev Build)".
12. In your Downloads folder, open the Mesen zipfile and
    drag `Mesen.exe` into `C:\emulators`.
13. Unblock `Mesen.exe` and run it.
14. When prompted to install a new version of .NET, click Yes.
    This should begin a download in Edge.
15. In your Downloads folder, open the executable whose name
    begins with `windowsdesktop-runtime` and follow the prompts
    to install .NET 6 for Windows.
16. Run `Mesen.exe` again.
17. Under Settings, set your button bindings for each platform
    (NES, SNES, Game Boy).
18. Drag one of the built ROMs from the desktop onto the window.
