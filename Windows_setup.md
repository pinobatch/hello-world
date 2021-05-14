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
Audacity, LAME, oggenc, FFmpeg, VLC media player

For command-line zipfile support, install Zip and UnZip programs published by
[Info-ZIP].  But handle `unz600xn.exe` carefully, as it's a self-extracting
filebomb that produces multiple files in the current working directory.

[Info-ZIP]: ftp://ftp.info-zip.org/pub/infozip/win32/

Configure Windows
-----------------
Many Windows laptops come set to switch from sleep (suspend to RAM)
to hibernation (suspend to HDD) too soon.  Michael Linenberger
described some [power settings to change].

* In Start > Settings > System > Power & sleep > Additional Power
  Settings > Change plan settings > Change advanced power settings >
  Sleep > Hibernate after, change "Plugged in" to 1440 minutes (one
  day) and "On battery" to 600 minutes (ten hours).  Ten hours should
  be long enough to span a full-time work day for a laptop stored in
  a locker during that time.
* In Start > Settings > System > Power & sleep > Additional Power
  Settings > Choose what the power buttons do, turn on "Change
  settings that are currently unavailable" and "Hibernate: Show in
  Power menu".  This lets you manually suspend to disk if you know
  you aren't going to be using your laptop for quite a while.
* Some laptops lack a fan, such as the Dell Inspiron 11 3000
  series.  These laptops can be passively cooled because they draw
  so little power.  For these, it may be convenient to increase the
  "When plugged in, PC goes to sleep after" time to an hour or more,
  especially if you often use it on a desk with an external monitor.

[power settings to change]: https://www.michaellinenberger.com/blog/four-windows-10-power-settings-you-should-probably-change-hibernation-and-sleep/

Install Git and MSYS
--------------------
[Git for Windows] comes with the MSYS ports of Bash and GNU Coreutils.
When installing Git for Windows, change the option to use the Windows
terminal instead of the terminal included with Git in order to make
native applications such as Python work.

Because Git omits GNU Make, follow [evanwill's instructions] to
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

Generate an SSH key for this PC

    ssh-keygen -t rsa
    cat ~/.ssh/id_rsa.pub

Add this public key to your keyring on your repository host and then
test your connection by cloning one of your own repositories.
See also [Connecting to GitHub with SSH].

[Git for Windows]: https://git-scm.com/download/win
[evanwill's instructions]: https://gist.github.com/evanwill/0207876c3243bbb6863e65ec5dc3f058
[ezwinports]: https://sourceforge.net/projects/ezwinports/files/
[Connecting to GitHub with SSH]: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

Configure Notepad++
-------------------
In Notepad++, open Settings > Preferences and change these:

* Editing > Vertical Edge Settings > Show vertical edge, line mode, 69 columns
* [Auto-Completion] > From `3` th character
* Language > Tab Settings > [Default] > Turn on "Replace by space".
  Notepad++ always uses [Default] tab settings for user-defined
  languages, such as assembly languages for 8-bit CPUs.
* Language > Tab Settings > makefile > Turn off "Use default value"
  and "Replace by space".  Make is the only language for which I
  use tabs instead of spaces.

Open Settings > Shortcut Mapper > Run, and remove the F5 shortcut.

Open Settings > Style Configurator > Language: Global Styles > Style: Default
Style, and change Font Style to Consolas 9.

Open Run > Run..., enter the following command, and save it as "Make
in Parent" with shortcut F5.

    cmd /C "cd $(CURRENT_DIRECTORY)\.. && "C:\Program Files\Git\mingw64\bin\make.exe" || pause"

[Auto-Completion]: http://docs.notepad-plus-plus.org/index.php/Auto_Completion

Configure Transmission
----------------------
Choose a port in the 6881-6889 range and configure your home Internet gateway
to forward it to your PC.  Then in Edit > Preferences > Networking, set an
upload speed limit of 100 kB/s, download speed limit of 1000 kB/s, and the
port you chose.
