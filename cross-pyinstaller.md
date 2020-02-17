Cross-compiling Python scripts to Windows executables
=====================================================

Upgrading Wine
--------------

I tried the instructions at "How to cross-compile a Python script
into a Windows executable on Linux" by Andrea Fortuna.[1]
But the installer failed, apparently due to a defect in Wine 3.6.
I tried these steps:

    sudo apt install wine-development
    wget https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe
    wine ./python-3.8.1-amd64.exe /passive

This ended up creating a folder called
`/home/pino/.wine/drive_c/users/pino/Local Settings/Application Data/Package Cache/{edfa99b7-1514-493a-aeaf-a37eeec724d2}`
with absolutely no permissions (`ls -ld` showed `d---------`).
Even when I tried adding the permissions and running the installer
again, it just ended up either recreating the folder without
permissions or removing the permissions:

    $ chmod u+rwx $HOME/'.wine/drive_c/users/pino/Local Settings/Application Data/Package Cache'/*
    $ ls -l $HOME/'.wine/drive_c/users/pino/Local Settings/Application Data/Package Cache'
    total 4
    drwx------ 2 pino pino 4096 Feb 16 17:16 {edfa99b7-1514-493a-aeaf-a37eeec724d2}
    $ wine ./python-3.8.1-amd64.exe /passive
    $ ls -l $HOME/'.wine/drive_c/users/pino/Local Settings/Application Data/Package Cache'
    total 4
    d--------- 2 pino pino 4096 Feb 16 17:16 {edfa99b7-1514-493a-aeaf-a37eeec724d2}

Broken permissions with `CreateDirectoryW` appears to be a known
issue in some versions of Wine.  The Python installer works out of
the box on Wine 4.14, but the Ubuntu 18.04 repository has Wine 3.6.
(See "Some of the created directories have no permissions"[2] on the
WineHQ forum.)

So I decided to upgrade by switching to WineHQ's repository.[3][4]
This involved uninstalling distro-provided Wine completely,
installing WineHQ-provided Wine, and reenabling binfmt support.[5]

    sudo apt remove libwine-development libwine-development:i386
    sudo dpkg --add-architecture i386
    wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add -
    sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
    sudo add-apt-repository ppa:cybermax-dexter/sdl2-backport
    sudo apt update
    sudo apt install --install-recommends winehq-stable

To check that it was installed:

    $ which wine && wine --version
    /usr/bin/wine
    wine-5.0

Unlike Canonical Wine, WineHQ Wine does not by default enable the
`binfmt-misc` mechanism to use Wine as the interpreter for Windows
executables that have the `x` bit set.

    echo $'package wine\ninterpreter /usr/bin/wine\nmagic MZ' | sudo tee /usr/share/binfmts/wine
    sudo update-binfmts --import wine

Installing PyInstaller
----------------------

With new wine in the old bottle, Python for Windows installed without
a problem.

    wine ./python-3.8.1-amd64.exe /passive
    wine py -c 'import sys;print(sys.platform)'
    wine py -m pip install --upgrade pip
    wine py -m pip install pyinstaller

This produced a diagnostic message:

> WARNING: The scripts `pyi-archive_viewer.exe`, `pyi-bindepend.exe`,
> `pyi-grab_version.exe`, `pyi-makespec.exe`, `pyi-set_version.exe`
> and `pyinstaller.exe` are installed in
> '`C:\users\pino\Local Settings\Application Data\Programs\Python\Python38\Scripts`'
> which is not on `PATH`.
> Consider adding this directory to `PATH` or, if you prefer to
> suppress this warning, use `--no-warn-script-location`.

Which I was able to solve by adding this folder to `Path` in the
registry.  Each time Wine starts, it appends the value in
`[HKEY_CURRENT_USER\Environment]Path` to the built-in path.

    $ wineserver -p3600
    $ wine cmd /c echo %Path%
    C:\windows\system32;C:\windows;C:\windows\system32\wbem
    $ wine regedit /E path.reg.utf16 "HKEY_CURRENT_USER\Environment"
    $ iconv -f UTF-16 -t UTF-8 path.reg.utf16 -o path.reg
    $ cat path.reg
    Windows Registry Editor Version 5.00

    [HKEY_CURRENT_USER\Environment]
    "TEMP"="C:\\users\\pino\\Temp"
    "TMP"="C:\\users\\pino\\Temp"
    $ echo '"Path"="C:\\users\\pino\\Local Settings\\Application Data\\Programs\\Python\\Python38\\Scripts"' >> path.reg
    $ wine regedit /C path.reg
    $ wine cmd /c echo %Path%
    C:\windows\system32;C:\windows;C:\windows\system32\wbem;C:\users\pino\Local Settings\Application Data\Programs\Python\Python38\Scripts
    $ wine pyinstaller.exe
    usage: pyinstaller [-h] [-v] [-D] [-F] [--specpath DIR] [-n NAME]
    [snip]
    pyinstaller: error: the following arguments are required: scriptname

We're set.  Now to try it:

    $ ~/develop/lorom-template/tools
    $ wine pyinstaller.exe ../lorom-template/tools/wav2brr.py
    $ wine dist/wav2brr/wav2brr.exe ../lorom-template/audio/selnow.wav selnow.brr

It appears to do something.  The one drawback is size: it turned a
9.6 kB script into a 21.7 MB folder that zips to 9.4 MB.

There is an option to make it emit a file instead of a folder, but
it is fraught with bugs:
https://github.com/pyinstaller/pyinstaller/issues/4423

    $ wine pyinstaller.exe --onefile -d bootloader ../lorom-template/tools/wav2brr.py
    $ wine wav2brr.exe
    [44] PyInstaller Bootloader 3.x
    [44] LOADER: executable is Z:\home\pino\develop\pyinstallerwin\dist\wav2brr.exe
    [44] LOADER: homepath is Z:\home\pino\develop\pyinstallerwin\dist
    [44] LOADER: _MEIPASS2 is NULL
    [44] LOADER: archivename is Z:\home\pino\develop\pyinstallerwin\dist\wav2brr.exe
    [44] LOADER: Extracting binaries
    [44] INTERNAL ERROR: cannot create temporary directory!
    [44] LOADER: temppath is 
    [44] LOADER: Error extracting binaries


[1]: https://www.andreafortuna.org/2017/12/27/how-to-cross-compile-a-python-script-into-a-windows-executable-on-linux/
[2]: https://forum.winehq.org/viewtopic.php?f=2&t=31849
[3]: https://wiki.winehq.org/Ubuntu
[4]: https://tecadmin.net/install-wine-on-ubuntu/
[5]: https://www.winehq.org/pipermail/wine-devel/2016-August/114478.html
