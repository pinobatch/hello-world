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

* In the Appearance pane, change the font to Ubuntu Mono 9 to fit
  two terminals side-by-side on a 1024-pixel-wide display or three
  on a 1600-pixel-wide display.
* Set the default geometry to 35 rows tall.
* Set the background to transparent, with 0.90 opacity
* In the Colors pane, change the background color to actual black
  (`#000000`).

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
    # 133 MB download, 577 MB disk space

Ubuntu since 16.04 installs `python3-pil` by default to support HP
printers in a basic manner.  To add the ability to read ink level,
install compatibility with Qt 5 applications:

    sudo apt install hplip-gui sqlitebrowser
    # 9 MB download, 36 MB disk space

These additional applications were needed for a particular purpose:

    sudo apt install wireshark
    # 23 MB download, 122 MB disk space

Some Python packages are maintained outside the distribution's
repository.  Download these using pip:

    pip3 install --upgrade --user PySimpleGUI

[deprecated SWF]: https://blogs.adobe.com/conversations/2017/07/adobe-flash-update.html

Set up the panel
----------------

Add a second panel, semi-inspired by a cross between Unity's panel
and my [LCARS mockup].  It has big launcher buttons and a window list
that appear just below the web browser's back button.

1. Deskbar orientation, always autohide, 64px wide, 3 rows,
   75% length; appearance: 75% background alpha.
2. Drag it to the bottom left corner and lock it.
3. Add six Launcher instances to the new panel. (As of Ubuntu 20.04
   and Debian 11, [Quicklauncher has been replaced] with multiple
   rows of the standard Launcher.)
4. Move the window buttons to the new panel below the launchers,
   and turn off Show flat buttons.

In each Launcher, add one application.

1. Firefox, Mousepad, GNU Image Manipulation Program
2. Terminal Emulator, MATE Calculator, ???

With the window buttons out of the way, we have room for other things
on the top panel:

1. Open the Whisker Menu's properties.  In the Panel Button pane,
   set it to display icon and title, and change its title to Start.
2. Add Directory Menu and Show Desktop to the right of Start.
3. Add CPU Graph to the right of the big separator, and set update
   interval to 1 s, width to 30, and no current usage bars.
4. Change the clock's format to a custom format: `%a %m-%d %H:%M`

[LCARS mockup]: https://pineight.com/mw/index.php?title=File:Lcars_taskbar_shown.png
[Quicklauncher has been replaced]: https://www.reddit.com/r/xfce/comments/f055qc/alternative_to_xfce4quicklauncherplugin_now_that/

Keyboard shortcuts
------------------

In Settings > Keyboard > Application Shortcuts, add these commands
if they're not already present:

* `xfce4-taskmanager`: Ctrl+Shift+Esc

In Settings > Window Manager > Keyboard, change these commands
to match [keyboard shortcuts in Windows], which I have used at
other jobs:

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

[Enable bitmap fonts] if needed.  (Use `yes-bitmaps` instead of
`force-bitmaps` because the latter has caused Firefox 112 to draw
invisible text, per [bug 1827950].)

    cd /etc/fonts/conf.d
    sudo rm 70-no-bitmaps.conf
    sudo ln -s ../conf.avail/70-yes-bitmaps.conf .
    sudo dpkg-reconfigure fontconfig

Download [Jester] from Dafont.  Then install it, either by opening
the font in the file manager and clicking Install or by copying it
into `~/.local/share/fonts`:

    mkdir -p ~/.local/share/fonts
    cd ~/.local/share/fonts
    unzip ~/Downloads/jester.zip
    ls

Make sure `Jester.ttf` shows up in the list.  Then spray it over
the rest of the UI in three panels under Start > Settings:

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

Bash aliases:

There appears to be a gradual movement away from running graphical
applications as root. This makes it more difficult for users of
graphical text editors to edit configuration files, such as to
upgrade from the `stable` version of Debian to a `testing` version
in some state of freeze. To replace the functionality of `gksu` that
has been missing since sometime in 2017, drop this snippet from
[Gabriel Sandoval's answer] in your profile.

    # first make sure .bashrc is calling .bash_aliases
    grep bash_aliases ~/.bashrc
    mousepad ~/.bash_aliases
    
    # per https://askubuntu.com/a/1067364/232993
    alias gksu='pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY'

Power Manager:

* When laptop lid is closed: Suspend
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
   and `~/.local/share/gtksourceview-4/language-specs`

ReText:

* Editor font: Ubuntu Mono 9
* Preview font: Jester 12

Xfce Task Manager:

* Refresh rate: 2 s

HexChat:

* Update EFnet server list, with `irc.servercentral.net` at top
* Set my nick
* Set my real name in Preferences > Chatting > Advanced

[Enable bitmap fonts]: https://askubuntu.com/a/1281443/232993
[bug 1827950]: https://bugzilla.mozilla.org/show_bug.cgi?id=1827950
[Jester]: http://www.dafont.com/jester.font
[Gabriel Sandoval's answer]: https://askubuntu.com/a/1067364/232993
[palm detection]: https://github.com/advancingu/XPS13Linux/issues/3

Firefox
-------
Change these preferences:

* In General > Language and Appearance > Fonts & Colors > Advanced,
  set Proportional to Serif and Serif to Jester.
* In Privacy and Security > Browser Privacy > Tracking Protection,
  set Use Tracking Protection to Always.  This blocks scripts and
  1-pixel images from domains that track users across sites, based
  on the list used by the Disconnect extension.

With the migration of Firefox to Snap packaging as of Ubuntu 22.04,
Firefox is having trouble seeing user-installed fonts.  Thus Jester
may show up in the user interface but not in web pages.

Install these extensions: [Stylus] and [Control Panel for Twitter]

Firefox for Linux has Ctrl+Q as a shortcut for Quit.  Ctrl+Q is
fine for applications with only one window, not a [tabbed MDI]
like that of most web browsers since NetCaptor.  When the user
reaches for Ctrl+Tab or Ctrl+W, the user may accidentally press
Ctrl+Q and lose data in those HTML forms that Restore Previous
Session cannot restore.  Even the shortcut Ctrl+Shift+Q is too
close to Ctrl+Shift+Tab.  (Not that extensions can change them
anyway because of years-unfixed [bug 1325692].)

The workaround is to open `about:config` and set the preferences
`browser.showQuitWarning` and `browser.warnOnQuit` to `true`.
Both must be set because of obscure decisions about the logic
of the quit action, documented in [bug 502908 comment 40] and
[bug 1325692 comment 26].  I assume these were intended to reduce
alert box fatigue for users of Restore Previous Session.

Some of Firefox's default settings are thought to waste Internet
data transfer allowance and trigger denial of service mitigations
on overly sensitive firewalls.  This appears in Wireshark as a
[SYN, SYN-ACK, RST sequence].  To keep Firefox from hitting your ISP
cap or causing a SYN flood, disable the [Race Cache with Network]
feature.  Open `about:config` and change `network.http.rcwn.enabled`
to `false`.  If that doesn't help, try these additional settings:

- Reduce `network.http.speculative-parallel-limit` to `0`
- Change `network.prefetch-next` to `false`
- Change `browser.urlbar.speculativeConnect.enabled` to `false`

Some websites are deliberately incompatible with Firefox tracking
protection for one of two reasons.  One, as seen on MIT Tech Review,
is to strengthen user identity measurement when enforcing a metered
paywall.  The more common reason is that a site's operator fails to
consider how to serve [ads that don't track] users across websites.
(This is a hard problem because third-party ad networks pay out
[three times as much] for ads based on tracking than for ads not
based on tracking.)  A [JavaScript switcher] extension works for
some but not all sites, as operators of more "premium" websites
have turned them into single-page apps to control ads and metering
more precisely.  I look for articles on these sites syndicated on
MSN.com, and if they're not there, I just ignore them and block
the sites at the DNS level to keep from visiting them by mistake.
Others are social networking services that build a [shadow profile]
(a dossier about non-members' viewing habits) yet are left out of
Disconnect's list for the benefit of members.

    pkexec mousepad /etc/hosts
    
    # Sites deliberately incompatible with tracking protection
    0.0.0.0 www.wired.com
    0.0.0.0 www.theinquirer.net
    0.0.0.0 www.theatlantic.com
    0.0.0.0 www.jellynote.com
    0.0.0.0 tvtropes.org
    
    # Social networks to which I don't belong
    0.0.0.0 www.facebook.com
    0.0.0.0 connect.facebook.net

[tabbed MDI]: https://en.wikipedia.org/wiki/Tab_(GUI)
[bug 1325692]: https://bugzilla.mozilla.org/show_bug.cgi?id=1325692
[bug 502908 comment 40]: https://bugzilla.mozilla.org/show_bug.cgi?id=502908#c40
[bug 1325692 comment 26]: https://bugzilla.mozilla.org/show_bug.cgi?id=1325692#c26
[Stylus]: https://addons.mozilla.org/en-US/firefox/addon/styl-us/
[Control Panel for Twitter]: https://addons.mozilla.org/firefox/addon/control-panel-for-twitter/
[SYN, SYN-ACK, RST sequence]: https://stackoverflow.com/q/55708231/2738262
[Race Cache with Network]: https://support.mozilla.org/en-US/questions/1267945
[ads that don't track]: https://blogs.harvard.edu/doc/2016/04/15/get-it-right-forbes/
[three times as much]: http://images.politico.com/global/2014/02/09/beales_eisenach_daa_study.pdf
[JavaScript switcher]: https://addons.mozilla.org/en-US/firefox/addon/quick-js-switcher/
[shadow profile]: https://spideroak.com/articles/facebook-shadow-profiles-a-profile-of-you-that-you-never-created

### Overriding Firefox's new tab

Firefox places severe restrictions on content retrieved from the
computer's file system using the `file:` protocol:

- Browsers treat each path on the file system as a separate origin,
  causing requests affected by the same-origin policy to fail.
- Only `http:` and `https:` sites, not files, can be pinned to
  the 6 to 8 spaces on Firefox's default new tab page.
- Extensions to customize Firefox's new tab page cannot load local
  files that transclude external images, style sheets, or scripts
  from the file system.

This makes customization of the new tab page and local development of
web pages less convenient without running a local web server in the
background all the time.

Start by creating a web root for static files, and test it.

    mkdir -p "$HOME/Documents/localhost"
    echo '<!DOCTYPE HTML><html><head><title>Localhost</title></head><body>Localhost</body></html>' > "$HOME/Documents/localhost/index.html"
    python3 --version
    python3 -m http.server 8000 --bind 127.0.0.1 --protocol HTTP/1.1 --directory "$HOME/Documents/localhost/"

If the Python version is prior to 3.11, as in Ubuntu versions prior
to 23.04 "lunar", remove the `--protocol HTTP/1.1` option.

Open Firefox and view [your local web server].  If it works, close
Firefox and stop the server, then open Start > Settings >
Session and Startup.  Add a new task:

* Name: HTTP on localhost
* Description: Serve local files on localhost:8000
* Command: `python3 -m http.server 8000 --bind 127.0.0.1 --directory /home/pino/Documents/localhost/ --protocol HTTP/1.1`
* Trigger: on login

(The home directory in "Command" is hardcoded until I can tell
whether Session and Startup allows using environment variables.)

Log out of Xfce and log back in, then view your local web server
again.  If it works, install the extension [New Tab Override] by
Sören Hentzschel and set it to use [your local web server] as its
custom URL.

Should Python's HTTP server not work well, other minimalist HTTP
servers to consider include [thttpd], [publicfile], and (if not
[repulsed by PHP from 2012]) `php -S localhost:8000`.

[your local web server]: http://localhost:8000/
[New Tab Override]: https://addons.mozilla.org/en-US/firefox/addon/new-tab-override/
[thttpd]: http://www.acme.com/software/thttpd/
[publicfile]: https://cr.yp.to/publicfile.html
[repulsed by PHP from 2012]: https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/

### Working around snap confinement

Both VLC media player and GNOME's screenshot tool save pictures in
the [XDG pictures folder].  Unlike these, FCEUX and Mesen by default
save pictures to a hidden folder.  This makes them inaccessible to
applications packaged as a snap because snap confinement blocks
applications from reading possibly sensitive data in [hidden folders]
that belong to other applications.  A symptom of this is screenshots
failing to upload to forums, Discord servers, and elsewhere.

Work around this by putting symbolic links to the XDG pictures folder
into the hidden folders.  Use relative symbolic links in case the
drive is later mounted as removable `/media` on another system.

    mkdir -p ~/.config/Mesen2 ~/.fceux ~/Pictures/mesen ~/Pictures/fceux
    cd ~/.config/Mesen2
    test -d Screenshots && mv Screenshots/* ~/Pictures/mesen/ && rmdir Screenshots
    ln -s ../../Pictures/mesen Screenshots
    cd ~/.fceux
    test -d snaps && mv snaps/* ~/Pictures/fceux/ && rmdir snaps
    ln -s ../Pictures/fceux snaps

[XDG pictures folder]: https://wiki.archlinux.org/title/XDG_user_directories
[hidden folders]: https://askubuntu.com/q/1290345/232993

Building applications from source
---------------------------------
Install prerequisites to build cc65, FCEUX, RGBDS, Scale2x, and
gmewav from source code.

    sudo apt install bison flex pkg-config libpng-dev cmake \
      libsdl-image1.2-dev libgtk2.0-dev libdumb1-dev libgme-dev \
      libminizip-dev
    # 36 MB download, 171 MB disk space

Build cc65, an assembler targeting the NES, Super NES, and other
6502 and 65816 platforms.  Using a shallow clone (`--depth=10`)
limits how many revisions Git has to download, so as to economize
storage and Internet bandwidth.

    mkdir -p ~/develop/assemblers
    cd ~/develop/assemblers
    git clone --depth=10 https://github.com/cc65/cc65.git
    cd cc65
    nice make -j2
    make install PREFIX="$HOME/.local"
    which cc65

Build ASM6, a simpler non-linking assembler targeting 6502 platforms.

    mkdir -p ~/develop/assemblers/asm6
    cd ~/develop/assemblers/asm6
    wget https://3dscapture.com/NES/asm6.zip
    unzip asm6.zip asm6.c
    gcc -Os -s asm6.c -o ~/.local/bin/asm6

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
    if [ -d "$HOME/.local/share/man" ] ; then
        export MANPATH="$HOME/.local/share/man:$MANPATH"
    fi
    if [ -d "$HOME/.local/share/cc65" ] ; then
        export CC65_HOME="$HOME/.local/share/cc65"
    fi

Build RGBDS, an assembler targeting the Game Boy.

    cd ~/develop/assemblers
    git clone --depth=10 https://github.com/gbdev/rgbds.git
    cd rgbds
    make
    make install PREFIX="$HOME/.local"
    man rgbds

Build WLA DX, an assembler targeting Z80 machines among others.
The final call to `cmake` works around its makefile's inability to
receive a `$PREFIX` from the environment ([WLA DX issue #265]).

    cd ~/develop/assemblers
    git clone --depth=10 https://github.com/vhelin/wla-dx.git
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

Build FCEUX from source because the version in Git is newer than the
one in Ubuntu's repository.  Because of the project's long history,
cloning the repository downloads 144 MiB as of second quarter 2020,
so run it on an unmetered connection.

    sudo apt install qttools5-dev libx264-dev
    cd ~/develop/emulators
    git clone --depth=10 https://github.com/TASEmulators/fceux.git
    cd fceux
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX="$HOME/.local" -DCMAKE_BUILD_TYPE=Release ..
    make -kj4
    make install

Build MEKA, a ColecoVision, Sega Master System, and Game Gear
emulator.  The `sed` line changes the makefile from requiring
Allegro version 5.0 to allowing any 5.x, including the 5.2
included in Ubuntu 18.04.

(Install instructions are currently not available, nor are
instructions to make MEKA play nicely with smaller monitors.)

    sudo apt install liballegro5-dev
    # 2 MB download, 9 MB disk
    cd ~/develop/emulators
    git clone --recursive https://github.com/ocornut/meka.git
    cd meka/meka/srcs
    sed -e 's/-5[.]0/-5/g' Makefile > Makefile_
    mv Makefile_ Makefile
    make -j3

Debian and Ubuntu package the free Game Boy Color and Game Boy
Advance emulator mGBA as `mgba-qt`.  Its GBA emulation is great.  Its
GBC emulation is progressing (to put it nicely), though good enough
for game logic if your device can't run Wine or proprietary software.
Even if your distribution has outdated mGBA, if your `sources.list`
has source URIs, you can use `sudo apt build-dep mgba` to grab
build prerequisites.  (Debian appears to provide source URIs by
default; Ubuntu doesn't.)  If not, use the dependencies listed at
[Debian source package mgba].  These ended up using 225 MB of space.

    # TODO: Get source URIs in sources.list
    sudo apt build-dep mgba
    # or
    sudo apt install debhelper desktop-file-utils libavcodec-dev \
      libavformat-dev libavresample-dev libavutil-dev libavfilter-dev \
      libmagickwand-dev libpng-dev libqt5opengl5-dev libsdl2-dev \
      libsqlite3-dev libswscale-dev pkg-config libedit-dev libelf-dev \
      liblua5.4-dev qtbase5-dev qtmultimedia5-dev qttools5-dev-tools \
      libzip-dev zlib1g-dev zipcmp zipmerge ziptool
    # 47.8 MB download, 220 MB disk
    cd ~/develop/emulators
    git clone --depth=10 https://github.com/mgba-emu/mgba.git
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
Mozilla intends that image editor developers add MozJPEG as
their JPEG export plug-in, but GIMP in Ubuntu 18.04 has not
([GIMP issue #1039]).  In the meantime, build the command-line
tools from source.  These instructions are based on
[MozJPEG instructions] by Andrew Welch.

    sudo apt install libtool nasm
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
    # useful for pictures containing both hard edges and
    # soft edges
    mozcjpeg -quality 75 -sample 1x1 kitten.png > kitten.jpg
    # Recompressing an existing JPEG image, as with AdvanceCOMP
    # (lossless, therefore without trellis quantization)
    mozjpegtran -progressive -optimize puppy.jpg > puppy-opt.jpg
    mozjpegtran -progressive -optimize -outfile puppy.jpg puppy.jpg

Build the NSF, GBS, and S3M to WAVE converter [gmewav], which is
part of the [little things] collection:

    cd ~/develop
    git clone https://github.com/pinobatch/little-things-nes.git
    cd little-things-nes/gmewav
    make
    cp ./gmewav ~/.local/bin
    cp scripts/gmeplay.sh ~/.local/bin/gmeplay

Build the demo program for [Blargg's snes_ntsc] library to preview
composite artifacts from the NES or Super NES PPU.  As it was last
updated in January 2007, it uses SDL 1.2.  So install `libsdl1.2-dev`
if you haven't.

    mkdir snes_ntsc
    cd snes_ntsc
    wget http://blargg.parodius.com/libs/snes_ntsc-0.2.2.zip
    unzip snes_ntsc-0.2.2.zip
    cd snes_ntsc-0.2.2
    gcc -Wall -O snes_ntsc.c demo.c `sdl-config --cflags --libs` -lm -o snes_ntsc

Because the demo program does not use SDL_image, it can load and
save only Windows bitmap files.  Work around that with ImageMagick.

    convert /path/to/something.png -colorspace rgb something.bmp
    ./snes_ntsc something.bmp
    convert filtered.bmp filtered.png

Build *NetPuzzleArena*, a work-in-progress *Puzzle League* clone by
NovaSquirrel:

    sudo apt install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    cd ~/develop
    git clone https://github.com/NovaSquirrel/NetPuzzleArena.git
    cd NetPuzzleArena
    make -j2

Set up Git to identify you when committing changes to your own
repositories.  (These are commented out to discourage copying and
pasting without the address changed.  Copy these lines into a
text editor, edit them there, and copy them into a terminal.)

    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"
    #git config --global core.editor "nano"
    ssh-keygen -t rsa
    cat ~/.ssh/id_rsa.pub

Add this public key to your keyring on your repository host and then
test your connection by cloning one of your own repositories.
Further instructions, including GitHub's current SSH key
fingerprints, are at [Connecting to GitHub with SSH].

[WLA DX issue #265]: https://github.com/vhelin/wla-dx/issues/265
[Debian source package mgba]: https://packages.debian.org/source/sid/mgba
[MozJPEG]: https://github.com/mozilla/mozjpeg
[deringing]: https://kornel.ski/deringing/
[GIMP issue #1039]: https://gitlab.gnome.org/GNOME/gimp/-/issues/1039
[MozJPEG instructions]: https://nystudio107.com/blog/installing-mozjpeg-on-ubuntu-16-04-forge
[gmewav]: https://forums.nesdev.com/viewtopic.php?p=200347#p200347
[little things]: https://github.com/pinobatch/little-things-nes
[Blargg's snes_ntsc]: https://www.slack.net/~ant/libs/ntsc.html#snes_ntsc
[Connecting to GitHub with SSH]: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

devkitARM
---------
devkitARM is a GCC-based toolchain published by devkitPro for
building software for Game Boy Advance and Nintendo DS.  Install
devkitARM through [devkitPro's version of pacman], the Arch Linux
package manager.  (Unrelated to any Bandai Namco product.)
In pacman, `-S` is roughly `install`, `-Sy` is `update`, and `-Syu`
is `update` then `upgrade`.  (See [Henry Barreto's comparison].)
After downloading the latest devkitPro pacman package:

    sudo dpkg -i /path/to/devkitpro-pacman.amd64.deb
    sudo dkp-pacman -Sy
    sudo dkp-pacman -S gba-dev
    # Download 64 MiB, install 295 MiB
    source /etc/profile.d/devkit-env.sh
    $DEVKITARM/bin/arm-none-eabi-gcc --version

`gba-dev` is a metapackage including devkitARM, libgba (with
examples), libfat, grit (an image converter), maxmod, and libtonc.
All this installs to `/opt/devkitpro` to keep devkitPro's software
out of the way of the system package manager (APT and dpkg).

[devkitPro's version of pacman]: https://devkitpro.org/wiki/devkitPro_pacman
[Henry Barreto's comparison]: https://dev.to/henrybarreto/pacman-s-simple-guide-for-apt-s-users-5hc4

Wine is not an emulator
-----------------------
Install Microsoft Core Fonts for the Web, which are proprietary fonts
needed for some applications and websites.

Because Core Fonts are not free software, the package in a
distribution's repository usually downloads the fonts from a separate
web host and unpacks them.  As the hosting situation changes, the
download location may fall out of date.  This causes configuration to
fail, which in turn causes Update Notifier to make repeated pop-ups.
In Ubuntu 16.04, Debian's package was needed.  (This was fixed in
18.04; I'm leaving the instructions up in case it recurs.)

    wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
    sudo dpkg -i ttf-mscorefonts-installer_3.6_all.deb

Install compatibility with 32- and 64-bit Windows applications.
As of Ubuntu 18.04, the administrator must explicitly choose between
installing older `wine-stable` and newer `wine-development`.  The
`wine-binfmt` package makes running Wine programs from the terminal
more convenient.

    sudo apt install wine-development wine-binfmt
    # 216 MB download, 1169 MB disk space

If all Windows applications that you run have 64-bit versions,
installing `wine64-development` will save a few hundred megabytes
of disk space by not installing the 32-bit (i386) system libraries.
However, be careful because 32-bit Video for Windows codecs work only
in 32-bit applications, particularly when recording video in bgb.

Run `winecfg` to create a Wine prefix.  This may take a couple
minutes, much like the "Hi" screen the first time you log in to a
Windows account after installing a service pack or feature update.
Make some customizations:

* In Desktop Integration > Appearance, change Active Title Text,
  Menu Text, Message Box Text, and Tooltip Text to Jester Regular 9.

The things I'm most likely to run in Wine:

* OpenMPT (free sample-based music editor, formerly ModPlug Tracker)
* Dn-FamiTracker (free NES music editor)
* No$sns (proprietary Super NES emulator, which may work on machines
  that cannot run Mesen 2 at full speed)
* BGB (proprietary Game Boy emulator), 32-bit version to allow
  use with CamStudio or ZMBV lossless codec
* Gens Kmod (Genesis/Mega Drive emulator with debugging)

To make launching Windows program from the terminal more convenient,
put a shell script in `~/.local/bin` for each such program that
converts slashes.

    nano ~/.local/bin/famitracker

    #!/bin/sh
    filetoopen=$1
    if [ -n "$filetoopen" ]; then
        filetoopen=`winepath -w "$filetoopen"`
    fi
    '/home/pino/.wine/drive_c/Program Files (x86)/FamiTracker/Dn-FamiTracker.exe' "$filetoopen"

    chmod +x ~/.local/bin/famitracker

Some software, such as No$sns, doesn't play nice with PulseAudio in
Wine 3.6, giving an error like this followed by a crash:

    Assertion 'pa_sample_spec_valid(spec)' failed at pulse/sample.c:67,
    function pa_frame_size(). Aborting.

To fix this, try [changing Wine's audio output API] from PulseAudio
to ALSA.  Other programs may work better with PulseAudio.

    winetricks sound=alsa
    winetricks sound=pulse

[changing Wine's audio output API]: https://askubuntu.com/q/77210/232993

Changing Mono distribution
--------------------------
Mono is a free implementation of .NET Common Language Runtime and
Windows Forms GUI toolkit for X11/Linux systems.  On the one hand,
some Linux distributions carry an outdated version of Mono.
For example, Mono 4.6.2.7 in Ubuntu 18.04 lacks features needed
by the Event Viewer in Mesen and Mesen-S.
On the other hand, sometimes the latest version of Mono introduces
regressions.  For example, Mono 6.12 breaks configuration dialog
boxes in some versions of Mesen and Mesen-S emulators compared to
6.8 and 6.10, causing them to treat both OK and Cancel as Cancel.

Upgrading from distro Mono to upstream Mono never worked for me.
For this reason, fully uninstall Mono in order to switch between
the version in the distribution's repository and the latest version
in the [Mono project repository].  This procedure is based on
[cryptoboy's answer] and UniversE's comment to the same question.

    sudo apt remove --purge --auto-remove mono-runtime
    apt list --installed '*mono*'
    # Keep the coding fonts. Uninstall anything related to the CLR.
    sudo apt install mono-complete
    mono --version

[Mono project repository]: https://www.mono-project.com/download/stable/
[cryptoboy's answer]: https://askubuntu.com/a/797007/232993

Proprietary crap
----------------
Relying on proprietary tools increases the chance of having to
start over in your search for tools should a tool maintainer get
[hit by a bus].

Get the Ubuntu .deb matching your distribution from [Dropbox].

Install it and fetch its dependencies:

    sudo dpkg -i ~/Downloads/dropbox_2015.10.28_amd64.deb

After running `dpkg -i`, you need to install `--fix-broken` (or
`-f` for short), a pseudo-package that causes APT to look in the
repositories for unmet dependencies of recently installed packages.

    sudo apt install -f

Then sign in to Dropbox.

[Emulicious] is a proprietary emulator of five 1980s gaming platforms
with 8080-family CPUs: Game Boy, Game Boy Color, Sega Master System,
Game Gear, and MSX.  Its Game Boy accuracy is comparable to that of
SameBoy.  It requires Java runtime, which is about as big as Mono:
a 46.6 MB download and 207 MB install.

    sudo apt install openjdk-14-jre

The ordinary download flow requires running server-provided script,
making it less suitable for headless operation.  Fortunately, it's
straightforward to parse the download URL out of the HTML.

    sudo apt install
    mkdir -p ~/develop/numism/emulators/emulicious
    cd ~/develop/numism/emulators/emulicious
    wget -O download.html https://emulicious.net/download/emulicious/
    wget -O Emulicious.zip "$(sed -n 's/.*downloadurl="\([^"]\+\).*/\1/p' download.html)"
    unzip Emulicious.zip
    rm Emulicious.zip download.html
    java -jar Emulicious.jar ~/develop/240p-test-mini/gameboy/gb240p.gb

[hit by a bus]: https://en.wikipedia.org/wiki/Bus_factor
[Dropbox]: https://www.dropbox.com/install-linux
[Emulicious]: https://emulicious.net/

Periodic maintenance
--------------------

Things to have an administrator do at least once a week:

    # Refresh the catalog of available DPKGs
    sudo apt update
    # Download DPKGs where one in the catalog is
    # newer than what is installed
    sudo apt -dy upgrade
    # Install (and download if needed) said newer DPKGs
    sudo apt upgrade
    
    # Download and install Snap packages newer than what is installed
    # (you may need to do this with the web browser closed)
    sudo snap refresh
    
    # Discard old systemd log entries
    # per <https://askubuntu.com/a/1238221/232993>
    sudo journalctl --vacuum-time=10d

External links
--------------
Others have described their loadouts:

- "[Linux Setup Cheat Sheet II]: let's install some software" by SteveProXNA
