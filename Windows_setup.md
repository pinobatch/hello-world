Common programs with EXE/MSI installers:
Dropbox, Notepad++, Python 3, Git (with Bash and Coreutils),
devkitARM, Transmission, GIMP, 7-Zip, Firefox, OpenMPT

Specialized programs that may require playing with zipfiles and/or
SmartScreen "More info":
j0CC-FamiTracker, FCEUX, BGB, RGBDS, Make, cc65, Info-ZIP,
AdvanceCOMP

In a PowerShell window, install a few Python packages from PyPI:

    py -m pip install --upgrade pip
    py -m pip install pygame
    py -m pip install numpy
    py -m pip install pillow

To install:
Audacity, LAME, oggenc, FFmpeg, VLC

For command-line zipfile support, install Zip and UnZip programs published by
[Info-ZIP].  But handle `unz600xn.exe` carefully, as it's a self-extracting
filebomb that produces multiple files in the current working directory.

[Info-ZIP]: ftp://ftp.info-zip.org/pub/infozip/win32/

Install Git and MSYS
--------------------
[Git for Windows] comes with the MSYS ports of Bash and GNU Coreutils.  
But because it omits GNU Make, follow [evanwill's instructions] to
download the latest Make without Guile from [ezwinports] and merge it
into `C:\Program Files\Git\mingw64`.  If you go this route, it appears to
automatically add to your Path a folder called `bin` directly inside your
user profile folder, such as `C:\Users\Pino\bin`, so you can put things
like `ca65.exe` there.

Copy the following commands into a text editor, uncomment them, edit them,
and copy them into Git Bash.  They are commented to discourage running them
unedited.

    # git config --global user.email "jdoe@example.com"
	# git config --global user.name "John Doe"

(Or was adding `~/bin` a result of having tried to install devkitPro MSYS?)

[Git for Windows]: https://git-scm.com/download/win
[evanwill's instructions]: https://gist.github.com/evanwill/0207876c3243bbb6863e65ec5dc3f058
[ezwinports]: https://sourceforge.net/projects/ezwinports/files/

Configure Notepad++
-------------------
In Notepad++, open Settings > Preferences and change these:

* Editing > Vertical Edge Settings > Show vertical edge, line mode, 69 columns
* [Auto-Completion] > From `3` th character

Open Settings > Style Configurator > Language: Global Styles > Style: Default
Style, and change Font Style to Consolas 9.

[Auto-Completion]: http://docs.notepad-plus-plus.org/index.php/Auto_Completion

Configure Transmission
----------------------
Choose a port in the 6881-6889 range and configure your home Internet gateway
to forward it to your PC.  Then in Edit > Preferences > Networking, set an
upload speed limit of 100 kB/s, download speed limit of 1000 kB/s, and the
port you chose.
