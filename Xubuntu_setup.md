Once Xubuntu is installed, it's time to set it up.

Fixing Dell laptops
-------------------
**Before you shut down your computer for the first time,** the
absolute first thing if you have a Dell laptop whose keyboard isn't
backlit is to turn off keyboard backlighting.  Otherwise, a bug
in Linux itself causes the system to hang during the second boot
([Bug 107651]).  Open a terminal and disable this feature:

    sudo systemctl mask systemd-backlight@leds\:dell\:\:kbd_backlight.service

If your laptop is a Dell Inspiron 11 3000 series, its keyboard
controller has a [hardware bug], where Home (Fn+Left), End
(Fn+Right), Page Up (Fn+Up), and Page Down (Fn+Down) send only make
(key down) scancodes, not break (key up) scancodes.  Because of how
X11 works, this means these keys work only once after a restart.
It's broken in some Windows applications as well, but Windows treats
repeated makes without break differently in general.  (Also
[reported in Manjaro].)  The file you edit to fix this is fairly
[sensitive to formatting].

    sudo nano /etc/udev/hwdb.d/95-custom-keyboard.hwdb

    # Dell Inspiron 3179
    # That's one space before each `KEYBOARD_KEY` and no blank lines
    evdev:atkbd:dmi:bvn*:bvr*:bd*
     KEYBOARD_KEY_c7=!home
     KEYBOARD_KEY_cf=!end
     KEYBOARD_KEY_c9=!pageup
     KEYBOARD_KEY_d1=!pagedown

    sudo sh -c "udevadm hwdb --update && udevadm trigger"

Some Dell Inspiron models have a quirky XHCI (USB host) driver that
occasionally prevents the laptop from going to sleep properly.
When this occurs, the laptop will become unresponsive after opening
the lid, instead needing a hard power cycle.  To work around this,
add [ioggstream's sleep fix script] to the
`/lib/systemd/system-sleep` folder.  (A comment to
[Chris Smart's article] points out that Debian and Ubuntu place it
in `/lib`, not `/usr/lib` where other distributions put it.)
For convenience, I have mirrored it as `system-sleep-xkci.sh`.

[Bug 107651]: https://bugzilla.kernel.org/show_bug.cgi?id=107651
[hardware bug]: https://www.dell.com/community/Linux-General/Dell-Inspiron-3179-keyboard-not-sends-KEY-RELEASE-events-key-up/td-p/5114299
[reported in Manjaro]: https://forum.manjaro.org/t/dell-inspiron-3162-keyboard-issue-fn-key-keyrelease-event-not-triggered/15524
[sensitive to formatting]: https://wiki.archlinux.org/index.php/Dell_Inspiron_11_3000_(3162)#Keyboard
[ioggstream's sleep fix script]: https://gist.github.com/ioggstream/8f380d398aef989ac455b93b92d42048
[Chris Smart's article]: https://blog.christophersmart.com/2016/05/11/running-scripts-before-and-after-suspend-with-systemd/

First round of apt-get
----------------------
Open a terminal, check for updated software, and install it:

    sudo sh -c "apt update && apt dist-upgrade"

While that's running, open Terminal preferences:

* Change the font to Ubuntu Mono 9 to fit two terminals
  side-by-side on a 1024-pixel-wide display.
* Set the default geometry to 35 rows tall.
* Set the background to transparent, with 0.90 opacity, and the
  background color to actual black (`#000000`)

At this point, APT will have installed an updated `linux-image`
package.  Updates to `linux-image` require a reboot.

Uninstall a proprietary plug-in that was made obsolete by HTML5.
Even Adobe has [deprecated SWF] in favor of renting Animate CC
and using it to reexporting the original FLA to HTML5.

    sudo apt remove flashplugin-installer

Then install useful free software:

    sudo apt install build-essential git vorbis-tools audacity ghex \
      python3-numpy hexchat python3-pil idle3 ffmpeg sox p7zip-full \
      libreoffice-impress libreoffice-draw sqlite3 flac advancecomp \
      oidentd gnome-font-viewer whois vlc guvcview python3-pip gimp \
      lame inkscape libjpeg-turbo-progs
    # 125 MB download, 607 MB disk space

Ubuntu since 16.04 installs `python3-pil` by default to support HP
printers, but the built-in Printers control panel doesn't support
reading ink level.  So install compatibility with Qt 5 applications:

    sudo apt install hplip-gui sqlitebrowser
    # 6 MB download, 24 MB disk space

[deprecated SWF]: https://blogs.adobe.com/conversations/2017/07/adobe-flash-update.html

Set up the panel
----------------

Add a second panel, semi-inspired by a cross between Unity's panel
and my [LCARS mockup]:

1. Deskbar orientation, always autohide, 128px wide, 75% length;
   appearance: 75% background alpha.
2. Drag it to the bottom left corner and lock it.
3. Add a Quicklauncher to the new panel.
4. Move the window buttons to the new panel below the Quicklauncher,
   and turn off Show flat buttons.

Quicklauncher is 2 columns:

1. `firefox` and `mousepad`
2. `xfce4-terminal` and `gnome-calculator`
3. `gimp` and ???

With the window buttons out of the way, we have room for other things
on the top panel:

1. Change the Whisker Menu to display icon and title, and change its
   title to Start.
2. Add Directory Menu and Show Desktop to the right of Start.
3. Add CPU Graph to the right of the big separator, and set update
   interval to 1 s, width to 30, and no current usage bars.
4. Change the clock's format to a custom format: `%a %m-%d %H:%M`

[LCARS mockup]: https://pineight.com/mw/index.php?title=File:Lcars_taskbar_shown.png

Keyboard shortcuts
------------------

In Settings > Keyboard > Application Shortcuts, add these commands:

* `xfce-taskmanager`: Ctrl+Shift+Esc

In Settings > Window Manager > Keyboard, change these commands to
match [keyboard shortcuts in Windows], which I use at my day job:

* Switch window for same application: Alt+F6
* Switch application: Super+Tab
* Maximize window: Super+Up
* Hide window (that is, iconify or minimize): Super+Down
* Show desktop: Super+D
* Add adjacent workspace: Ctrl+Super+D
* Delete active workspace: Ctrl+Super+F4
* Left and Right workspace: Ctrl+Super+Left and Ctrl+Super+Right  
  *or is it Previous and Next workspace?*

[keyboard shortcuts in Windows]: https://support.microsoft.com/en-us/help/126449/keyboard-shortcuts-for-windows

Timidity conflict
-----------------
There are reports that after upgrading to Debian 10 "buster", the
MIDI synthesizer service (Timidity or FluidSynth) grabs the sound
card before PulseAudio has a chance to. (See [Debian bug 901148] and
[PulseAudio troubleshooting on ArchWiki].)  If the Output Devices
pane of PulseAudio mixer (`pavucontrol`)  shows "Dummy output" under
"All Output Devices" or "No output devices available" under "Hardware
Output Devices", check if Timidity is installed.  Then try stopping
Timidity and restarting PulseAudio.

    # Ensure ALSA is detecting your sound card
    aplay -L
    # Try playing sound, changing -D as needed
    aplay -D sysdefault:CARD=Intel /path/to/some/file.wav
    
    # See what owns the output devices
    sudo fuser -v /dev/snd/*
    
    # If Timidity entries exist but no PulseAudio entries, continue
    sudo service timidity stop
    pulseaudio --kill
    pulseaudio --start

Look at the mixer again.  If this caused your sound card to appear,
attempt to reconfigure the service to use PulseAudio.

[Debian bug 901148]: https://bugs.debian.org/901148
[PulseAudio troubleshooting on ArchWiki]: https://wiki.archlinux.org/index.php/PulseAudio/Troubleshooting

Other personalizations
----------------------

Download [Jester] from Dafont.  Then install it:

    mkdir -p ~/.fonts
    cd ~/.fonts
    unzip ~/Downloads/jester.zip
    ls

Make sure `Jester.ttf` shows up in the list.  Then spray it over
the rest of the UI:

* In Appearance, set the default font to Jester 10.
* In Window Manager, set the title font to Jester Bold 10 and the
  theme to Daloa, which has frames thicker than 1 pixel to allow
  practical resizing.
* In Window Manager Tweaks, change the key used to grab windows
  to Super, so as not to interfere with GIMP's use of Alt.

To set the font in Qt 4 applications, open `.config/Trolltech.conf`,
and under `[Qt]`, change or add the following:

    font="Jester,9,-1,5,50,0,0,0,0,0"

Other fonts to download include Wasted Collection, Comic Neue,
and Patrick Hand.

Power Manager:

* When laptop lid is closed on battery: Suspend
* Suspend when inactive for 15 minutes on battery
* On critical battery power (10%), ask
* Blank screen after 5 minutes on battery or 15 minutes plugged in
* Put display to sleep one minute after blanking

**Experimental:** Some laptops' trackpads come set to treat
accidental touches while typing as mouse clicks.  Try turning on
[palm detection] so that touching the trackpad while typing doesn't
move the insertion point or (worse) focus.  Add this to the end of
`.profile` (or to `.bash_profile` if that exists instead):

    synclient PalmDetect=1

If that doesn't work, in Settings > Mouse and Touchpad, have it
disable the touchpad for 0.5 seconds after typing.

GIMP:

* Enable single-window mode
* Tool Options:
    1. Change to Pixel brush at size 1
    2. Patterns: Change to Clipboard
    3. Save Tool Options Now
* Theme: Small
* Default grid: 8 pixel spacing, color #800000
* Default image size: 256x240 pixels
* Toolbox: Resize to 7 tools wide
* Left dock: Tool Options, Layers, and Colormap
* Right dock: Empty

IDLE 3:

* Font: Ubuntu Mono 9
* Create a new Custom Key Set called `Reduced Fkeys`
* Change `run-module` to `<Control-Key-r>`

Mousepad:

* Show line numbers
* Wrap long lines
* Highlight matching brackets
* Highlight current line
* Colors: Kate
* Font: Ubuntu Mono 9

Mousepad languages:

1. Download <https://gist.github.com/Sanqui/5176862> as `rgbasm.lang`
2. Change the text inside `<property name="globs">` to `*.asm;*.z80`
3. Copy `ca65.lang` (from this repository) and `rgbasm.lang` to where
   GTKSourceView looks for languages:
   `~/.local/share/gtksourceview-2.0/language-specs`
   and `~/.local/share/gtksourceview-3.0/language-specs`

ReText:

* Editor font: Ubuntu Mono 9
* Preview font: Jester 12

Xfce Task Manager:

* Refresh rate: 2 s

HexChat:

* Update EFnet server list, with `irc.servercentral.net` at top
* Set my nick
* Set my real name in Preferences > Chatting > Advanced

[Jester]: http://www.dafont.com/jester.font
[palm detection]: https://github.com/advancingu/XPS13Linux/issues/3

Firefox
-------
There used to be an extension called "Ubuntu modifications for
Firefox" ([xul-ext-ubufox]) that reminded the user to restart
Firefox after APT upgrades it.  It no longer works with any
supported version of Mozilla Firefox.

    sudo apt remove xul-ext-ubufox

Change these preferences:

* In General > Language and Appearance > Fonts & Colors > Advanced,
  set Proportional to Serif and Serif to Jester.
* In Privacy and Security > Browser Privacy > Tracking Protection,
  set Use Tracking Protection to Always.  This blocks scripts and
  1-pixel images from domains that track users across sites, based
  on the list used by the Disconnect extension.

Install these extensions: [Stylus] and [HTTPS Everywhere]

Firefox 57 has Ctrl+Q as a shortcut for Quit.  Ctrl+Q is fine for
applications with only one window, not a [tabbed MDI] like that
of most web browsers since NetCaptor.  When the user reaches for
Ctrl+Tab or Ctrl+W, he may accidentally press Ctrl+Q and lose data in
those HTML forms that Restore Previous Session cannot restore.  The
extension that's supposed to fix this ([Disable Ctrl-Q and Cmd-Q])
is not compatible with GNU/Linux because of [bug 1325692].

The workaround is to open `about:config`
and set the preferences `browser.showQuitWarning` and
`browser.warnOnQuit` to `true`.
Both must be set because of obscure decisions about the logic
of the quit action, documented in [bug 502908 comment 40] and
[bug 1325692 comment 26].  I assume these were intended to reduce
alert box fatigue for users of Restore Previous Session.

Some of Firefox's default settings are thought to waste Internet
data transfer allowance and trigger denial of service  mitigations
on overly sensitive firewalls. To keep Firefox from hitting your ISP
cap or causing a SYN flood, change these settings in `about:config`:

- Reduce `network.http.speculative-parallel-limit` to `0`
- Change `network.prefetch-next` to `false`

Some websites are deliberately incompatible with Firefox tracking
protection for one of two reasons.  One, as seen on MIT Tech Review,
is to strengthen user identity measurement when enforcing a metered
paywall.  The more common reason is that a site's operator fails to
consider how to serve [ads that don't track] users across websites.
(This is a hard problem because third-party ad networks pay out
[three times as much] for ads based on tracking than for ads not
based on tracking.)  A [JavaScript switcher] extension works for
some but not all sites.  So I just ignore articles on those sites and
block them at the DNS level to keep from visiting them by mistake.
Others are social networks that build a [shadow profile] (a dossier
about non-members' viewing habits), but which are left out of
Disconnect's list for the benefit of members.

    gksudo mousepad /etc/hosts
    
    # Sites deliberately incompatible with tracking protection
    0.0.0.0 www.wired.com
    0.0.0.0 www.theinquirer.net
    0.0.0.0 www.theatlantic.com
    0.0.0.0 www.jellynote.com
    0.0.0.0 tvtropes.org
    
    # Social networks to which I don't belong
    0.0.0.0 www.facebook.com
    0.0.0.0 connect.facebook.net

[xul-ext-ubufox]: https://apps.ubuntu.com/cat/applications/xul-ext-ubufox/
[tabbed MDI]: https://en.wikipedia.org/wiki/Tab_(GUI)
[Disable Ctrl-Q and Cmd-Q]: https://addons.mozilla.org/en-US/firefox/addon/disable-ctrl-q-and-cmd-q/?src=search
[bug 1325692]: https://bugzilla.mozilla.org/show_bug.cgi?id=1325692
[bug 502908 comment 40]: https://bugzilla.mozilla.org/show_bug.cgi?id=502908#c40
[bug 1325692 comment 26]: https://bugzilla.mozilla.org/show_bug.cgi?id=1325692#c26
[Stylus]: https://addons.mozilla.org/en-US/firefox/addon/styl-us/
[HTTPS Everywhere]: https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/
[ads that don't track]: https://blogs.harvard.edu/doc/2016/04/15/get-it-right-forbes/
[three times as much]: http://images.politico.com/global/2014/02/09/beales_eisenach_daa_study.pdf
[JavaScript switcher]: https://addons.mozilla.org/en-US/firefox/addon/quick-js-switcher/
[shadow profile]: https://spideroak.com/articles/facebook-shadow-profiles-a-profile-of-you-that-you-never-created

Building applications from source
---------------------------------
Install prerequisites to build cc65, FCEUX, RGBDS, Scale2x, and
gmewav from source code.

    sudo apt install byacc flex pkg-config libpng-dev scons \
      libsdl-image1.2-dev libgtk2.0-dev libdumb1-dev libgme-dev
    # 34 MB download, 159 MB disk space

Build cc65, an assembler targeting the NES, Super NES, and other
6502 and 65816 platforms.

    mkdir ~/develop
    cd ~/develop
    git clone https://github.com/cc65/cc65.git
    cd cc65
    nice make -j2
    make install PREFIX="$HOME/.local"
    which cc65

Build ASM6, a simpler non-linking assembler targeting 6502 platforms.

    mkdir ~/develop/asm6
    cd ~/develop/asm6
    wget https://3dscapture.com/NES/asm6.zip
    unzip asm6.zip asm6.c
    gcc -Os asm6.c -o ~/.local/bin/asm6

The last step should show `/home/<username>/.local/bin/cc65`.  If it
does not, add `~/.local/bin` to your `PATH` for next time you log in.
And while you're at it, add a path for locally installed shared
libraries and manual pages and a path for header files belonging to
locally installed compilers and assemblers.

    mousepad ~/.bashrc

    if [ -d "$HOME/.local/bin" ] ; then
        export PATH="$HOME/.local/bin:$PATH"
    fi
    if [ -d "$HOME/.local/lib" ] ; then
        export LD_LIBRARY_PATH="$HOME/.local/lib/:${LD_LIBRARY_PATH}"
    fi
    if [ -d "$HOME/.local/man" ] ; then
        export MANPATH="$HOME/.local/man:$MANPATH"
    fi
    if [ -d "$HOME/.local/share/cc65" ] ; then
        export CC65_HOME="$HOME/.local/share/cc65"
    fi

Build RGBDS, an assembler targeting the Game Boy.

    cd ~/develop
    git clone https://github.com/rednex/rgbds.git
    cd rgbds
    make
    make install PREFIX="$HOME/.local"
    man rgbds

Build WLA DX, an assembler targeting Z80 machines among others.
The final call to `cmake` works around its makefile's inability to
receive a `$PREFIX` from the environment ([WLA DX issue #265]).

    cd ~/develop
    git clone https://github.com/vhelin/wla-dx.git
    cd wla-dx
    cmake -G "Unix Makefiles" .
    make -j4
    cmake -D CMAKE_INSTALL_PREFIX="$HOME/.local" -P cmake_install.cmake

Build Scale2x to enlarge PNG images.  The repository uses Autotools
to generate the `./configure` file but doesn't describe how to run
the Autotools to build from the repository rather than from a
source tarball.

    cd ~/develop
    wget https://github.com/amadvance/scale2x/releases/download/v4.0/scale2x-4.0.tar.gz
    tar zxf scale2x-4.0.tar.gz
    cd scale2x-4.0
    ./configure --prefix=$HOME/.local
    nice make -j2
    make install

Build FCEUX (SDL) from source because the version in Git is newer
than the one in Ubuntu's repository.  Until April 2018, FCEUX was
maintained in an SVN repository on SourceForge, and cloning SVN was
very slow because `git svn` works revision by revision.  But now it's
in a Git repository on GitHub.

    cd ~/develop
    git clone https://github.com/TASVideos/fceux.git
    cd fceux
    nice scons -j2
    scons --prefix=$HOME/.local install

Build MEKA, a ColecoVision, Sega Master System, and Game Gear
emulator.  The `sed` line changes the makefile from requiring
Allegro version 5.0 to allowing any 5.x, including the 5.2
included in Ubuntu 18.04.

(Install instructions are currently not available, nor are
instructions to make MEKA play nicely with smaller monitors.)

    sudo apt install liballegro5-dev
    # 2 MB download, 9 MB disk
    git clone --recursive https://github.com/ocornut/meka.git
    cd meka/meka/srcs
    sed -e 's/-5[.]0/-5/g' Makefile > Makefile_
    mv Makefile_ Makefile
    make -j3

Debian and Ubuntu package the free Game Boy Color and Game Boy
Advance emulator mGBA as `mgba-qt`.  Its GBA emulation is great.
Its GBC emulation needs work (to put it nicely) but is good enough
for game logic if your device can't run Wine or proprietary software.
Even if your distribution has outdated mGBA, if your `sources.list`
has source URIs, you can use `sudo apt build-dep mgba-qt` to grab
build prerequisites.  (Debian appears to provide source URIs by
default; Ubuntu doesn't.)  If not, use the dependencies listed at
[Debian source package mgba].  These ended up using 225 MB of space.

    # TODO: Get source URIs in sources.list
    sudo apt build-dep mgba-qt
    # or
    sudo apt install cmake debhelper desktop-file-utils libavcodec-dev \
      libavformat-dev libavresample-dev libavutil-dev libedit-dev \
      libmagickwand-dev libpng-dev libqt5opengl5-dev libsdl2-dev \
      libsqlite3-dev libswscale-dev libzip-dev pkg-config \
      qtbase5-dev qtmultimedia5-dev qttools5-dev-tools zlib1g-dev

    cd ~/develop
    git clone https://github.com/mgba-emu/mgba.git
    cd mgba
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=$HOME/.local ..
    make -j2
    make install

Mozilla maintains a fork of the JPEG image encoder library
libjpeg-turbo, called [MozJPEG].  It improves the rate-distortion
performance compared to libjpeg with trellis quantization and
smarter progressive coding, reducing size by 5% at a given
quality level.  Images containing both photographic elements
and black-on-white text or line art fare even better thanks to
[deringing] work by Kornel Lesiński.

The MozJPEG distribution includes counterparts to the `cjpeg`,
`djpeg`, and `jpegtran` command-line tools included with libjpeg.
Mozilla intends that image editor developers add MozJPEG as their
JPEG export plug-in, but GIMP in Ubuntu 18.04 has not.  In the
meantime, build the command-line tools from source.  These
instructions are based on [MozJPEG instructions] by Andrew Welch.

    sudo apt install libtool nasm libpng-dev
    cd ~/develop
    git clone https://github.com/mozilla/mozjpeg.git
    cd mozjpeg
    mkdir build
    cd build
    cmake -G"Unix Makefiles" ../
    make -j2
    strip cjpeg-static jpegtran-static
    cp cjpeg-static ~/.local/bin/mozcjpeg
    cp jpegtran-static ~/.local/bin/mozjpegtran

Then it can be used as follows:

    # This produces output with 4:2:0 chroma subsampling
    mozcjpeg -quality 75 kitten.png > kitten.jpg
    # This produces output with full-resolution chroma,
    # useful for pictures containing both hard edges
    mozcjpeg -quality 75 -sample 1x1 kitten.png > kitten.jpg
    # Recompressing an existing JPEG image, as with AdvanceCOMP
    # (but you won't get the trellis quantization)
    mozjpegtran -progressive -optimize puppy.jpg > puppy-opt.jpg
    mozjpegtran -progressive -optimize -outfile puppy.jpg puppy.jpg

Build the NSF, GBS, and S3M to WAVE converter [gmewav], which is
part of the [little things] collection:

    cd ~/develop
    git clone https://github.com/pinobatch/little-things-nes.git
    cd little-things-nes/gmewav
    make
    cp ./gmewav ~/.local/bin

Build *NetPuzzleArena*, a work-in-progress *Puzzle League* clone by
Josh "NovaSquirrel" Hoffman:

    sudo apt install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    cd ~/develop
    git clone https://github.com/NovaSquirrel/NetPuzzleArena.git
    cd NetPuzzleArena
    make -j2

As of 2017-07-01, Microsoft has ended service for the previous Skype
client (version 4.3), and versions 5 and later run in Electron, a
cut-down version of the Chrome web browser that requires hundreds of
megabytes of RAM just for chat.  So perhaps the most efficient way
to communicate with your existing Skype contacts without hogging a
browser content process is to use Eion Robb's [skype4pidgin], a
Pidgin plug-in that uses the same JSON-based protocol as Skype for
Web.  Its biggest drawback is that as of mid-2017, leaving suspend
produces "Failed getting PPFT value", requiring a visit to the Buddy
List to reconnect.

    sudo apt install libpurple-dev libjson-glib-dev
    cd ~/develop
    git clone git://github.com/EionRobb/skype4pidgin.git
    cd skype4pidgin/skypeweb
    mkdir build
    cd build
    cmake ..
    cpack
    sudo dpkg -i skypeweb-1.4.0-Linux.deb

The same developer made the [Purple Discord] plug-in to connect to
Discord, whose official client also uses Electron.  But because it
lacks retrieval of older messages, the line separating new messages
from old, reactions, emoji selection, editing, pins, and other
distinctive features of Discord, it's not quite as convenient as a
RAM-saving tool.  In addition, use alongside Discord for Web will
likely cause one of the two to stop receiving messages.  But for
the sake of completeness:

    cd ~/develop
    git clone git://github.com/EionRobb/purple-discord.git
    cd purple-discord
    make
    sudo make install

Set up Git to identify you when committing changes to your own
repositories.  (These are commented out to discourage copying and
pasting without the address changed.)

    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"
    #git config --global core.editor "nano"

[WLA DX issue #265]: https://github.com/vhelin/wla-dx/issues/265
[Debian source package mgba]: https://packages.debian.org/source/sid/mgba
[MozJPEG]: https://github.com/mozilla/mozjpeg
[deringing]: https://kornel.ski/deringing/
[MozJPEG instructions]: https://nystudio107.com/blog/installing-mozjpeg-on-ubuntu-16-04-forge
[gmewav]: https://forums.nesdev.com/viewtopic.php?p=200347#p200347
[little things]: https://github.com/pinobatch/little-things-nes
[skype4pidgin]: https://github.com/EionRobb/skype4pidgin
[Purple Discord]: https://github.com/EionRobb/purple-discord

Wine is not an emulator
-----------------------
Install Microsoft proprietary fonts needed for some applications and
websites.  Ubuntu has a package for this, but the download locations
in Ubuntu 16.04's package are out of date.  This causes configuration
to fail, which in turn causes Update Notifier to make repeated
pop-ups.  So if you use 16.04, install Debian's newer package.
(This is fixed in 18.04.)

    wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
    sudo dpkg -i ttf-mscorefonts-installer_3.6_all.deb

Install compatibility with 32- and 64-bit Windows applications.
As of Ubuntu 18.04, the administrator must explicitly choose between
installing older `wine-stable` and newer `wine-development`.  The
`wine-binfmt` package makes running Wine programs from the terminal
more convenient.

    sudo apt install wine-development wine-binfmt winetricks
    # 103 MB download, 743 MB disk space

Run `winecfg` to create a Wine prefix.  This may take a couple
minutes, much like the "Hi" screen the first time you log in to a
Windows account after installing a service pack or feature update.
Make some customizations:

* In Desktop Integration > Appearance, change Active Title Text,
  Menu Text, Message Box Text, and Tooltip Text to Jester Regular 9.

The things I'm most likely to run in Wine:

* OpenMPT (free sample-based music editor, formerly ModPlug Tracker)
* FCEUX (free NES emulator with debugger)
* FamiTracker (free NES music editor)
* NO$SNS (proprietary Super NES emulator, which runs at full speed on
  an Atom unlike bsnes-plus or Mesen-S)
* BGB (proprietary Game Boy emulator)
* Gens Kmod (Genesis/Mega Drive emulator with debugging)

To make launching Windows program from the terminal more convenient,
put a shell script in `~/.local/bin` that handles slash conversion.

    nano ~/.local/bin/famitracker

    #!/bin/sh
    filetoopen=$1
    if [ -n "$filetoopen" ]; then
        filetoopen=`winepath -w "$filetoopen"`
    fi
    '/home/pino/.wine/drive_c/Program Files (x86)/FamiTracker/j0CC-Famitracker-j0.5.3.exe' "$filetoopen"

    chmod +x ~/.local/bin/famitracker

Some software, such as NO$SNS, doesn't play nice with PulseAudio in
Wine 3.6, giving an error like this followed by a crash:

    Assertion 'pa_sample_spec_valid(spec)' failed at pulse/sample.c:67,
    function pa_frame_size(). Aborting.

To fix this, try [changing Wine's audio output API] from PulseAudio
to ALSA.  Other programs may work better with PulseAudio.

    winetricks sound=alsa
    winetricks sound=pulse

[changing Wine's audio output API]: https://askubuntu.com/q/77210/232993

Proprietary crap
----------------
Get the Ubuntu .deb matching your distribution from [Dropbox].

Install it and fetch its dependencies:

    sudo dpkg -i ~/Downloads/dropbox_2015.10.28_amd64.deb

After running `dpkg -i`, you need to install `--fix-broken` (or
`-f` for short), a pseudo-package that causes APT to look in the
repositories for unmet dependencies of recently installed packages.

    sudo apt install -f

Then sign in to Dropbox.

[Dropbox]: https://www.dropbox.com/install-linux
