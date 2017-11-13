Once Xubuntu is installed, it's time to set it up.

**Before you shut down your computer for the first time,** the
absolute first thing if you have a Dell laptop whose keyboard isn't
backlit is to turn off keyboard backlighting.  Otherwise, a bug
in Linux itself causes the system to hang during the second boot
([Bug 107651]).  Open a terminal and disable this feature:

    sudo systemctl mask systemd-backlight@leds\:dell\:\:kbd_backlight.service

[Bug 107651]: https://bugzilla.kernel.org/show_bug.cgi?id=107651

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

    sudo apt install build-essential git vorbis-tools audacity ffmpeg
    sudo apt install python3-numpy hexchat python3-pil idle3 ghex sox
    sudo apt install libreoffice-impress libreoffice-draw sqlite3 vlc
    sudo apt install oidentd advancecomp gksu gnome-font-viewer whois
    sudo apt install gimp p7zip-full guvcview python3-pip lame flac
    sudo apt install inkscape libjpeg-turbo-progs

Interestingly enough, as of 16.04, `python3-pil` is installed by
default to support HP printers, but the built-in Printers control
panel doesn't support reading ink level.  So install compatibility
with Qt 4 applications, which adds 64 MB to the HDD footprint:

    sudo apt install hplip-gui

Also Install compatibility with Qt 5 applications, which adds 123 MB
to the HDD footprint:

    sudo apt install retext sqlitebrowser

[deprecated SWF]: https://blogs.adobe.com/conversations/2017/07/adobe-flash-update.html

Set up the panel
----------------

Add a second panel, semi-inspired by a cross between Unity's panel
and my LCARS mockup:

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
* In Configure Wine > Desktop Integration > Appearance, change
  Active Title Text, Menu Text, Message Box, and Tooltip Text to
  Jester Regular 9.
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
freeze for 0.3 seconds after typing.

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
Remove Ubuntu modifications for Firefox ([xul-ext-ubufox]), which
interferes with multiprocess operation. The most useful thing it
does is remind the user to restart Firefox after APT upgrades it.

    sudo apt remove xul-ext-ubufox

Prior to Firefox 55, it was recommended to follow the beta channel by
adding `ppa:mozillateam/firefox-next`.  As of September 2017, this is
no longer recommended because Keybinder will stop working in
Firefox 57, and the replacement ([Disable Ctrl-Q and Cmd-Q]) is not
compatible with GNU/Linux because of [bug 1325692].  Because
Andy McKay has decided that bug 1325692 will not be fixed in Firefox
57, the only way to prevent data loss in those HTML forms that
Restore Previous Session cannot restore is to
[downgrade to Firefox 52 ESR].

    sudo add-apt-repository ppa:jonathonf/firefox-esr
    sudo apt update
    sudo apt install firefox-esr

Change these preferences:

* Default serif font for Latin script: Jester
* `browser.tabs.remote.autostart`: true  
  This enables e10s.
* `privacy.trackingprotection.enabled`: true  
  Firefox Private Browsing blocks domains that track users across
  sites based on the list used by the Disconnect extension.
  This enables tracking protection even outside Private Browsing.
* `network.http.pipelining`: true  
  This requests multiple resources at a time from a web server.
* `browser.cache.use_new_backend`: 1  
  This enables an experimental non-blocking HTTP cache.

Some of these preferences take effect once Firefox is restarted.
So install some extensions, some of which also require a restart:

* [Stylish]
* [HTTPS Everywhere]
* [Keybinder]

After restarting, open Keybinder and disable Ctrl+Q to quit.  Ctrl+Q
is fine for applications that have only one window, not a tabbed MDI
like that of most web browsers since NetCaptor.

Some sites are deliberately incompatible with Firefox tracking
protection because their operators fail to figure out how to serve
[ads that don't track] users across websites.  So I just ignore
articles on those sites and block them at the DNS level to keep from
visiting them by mistake.  Others are social networks that build a
[shadow profile] (a dossier about non-members' viewing habits), but
which are left out of Disconnect's list for the benefit of members.

    gksudo mousepad /etc/hosts
    
    # Sites deliberately incompatible with tracking protection
    0.0.0.0 www.wired.com
    0.0.0.0 www.theinquirer.net
    0.0.0.0 www.theatlantic.com
    0.0.0.0 www.jellynote.com
    
    # Social networks to which I don't belong
    0.0.0.0 www.facebook.com
    0.0.0.0 connect.facebook.net

[xul-ext-ubufox]: https://apps.ubuntu.com/cat/applications/xul-ext-ubufox/
[Stylish]: https://addons.mozilla.org/en-US/firefox/addon/stylish/?src=search
[HTTPS Everywhere]: https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/
[Keybinder]: https://addons.mozilla.org/en-US/firefox/addon/keybinder/
[Disable Ctrl-Q and Cmd-Q]: https://addons.mozilla.org/en-US/firefox/addon/disable-ctrl-q-and-cmd-q/?src=search
[bug 1325692]: https://bugzilla.mozilla.org/show_bug.cgi?id=1325692
[downgrade to Firefox 52 ESR]: https://askubuntu.com/q/894871/232993
[ads that don't track]: https://blogs.harvard.edu/doc/2016/04/15/get-it-right-forbes/
[shadow profile]: https://spideroak.com/articles/facebook-shadow-profiles-a-profile-of-you-that-you-never-created

Building applications from source
---------------------------------
Build cc65, an assembler targeting the NES, Super NES, and other
6502 and 65816 platforms.

    mkdir ~/develop
    cd ~/develop
    git clone https://github.com/cc65/cc65.git
    cd cc65
    nice make -j2
    make install PREFIX=~/.local
    which cc65

The last step should show `/home/<username>/.local/bin/cc65`.  If it
does not, add `~/.local/bin` to your `PATH` for next time you log in:

    mousepad ~/.bashrc

    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$HOME/.local/bin:$PATH"
    fi

Build RGBDS, an assembler targeting the Game Boy.

    sudo apt install byacc flex pkg-config libpng-dev
    cd ~/develop
    git clone https://github.com/rednex/rgbds.git
    cd rgbds
    make
    make install PREFIX="$HOME/.local"
    man rgbds

Build Scale2x to enlarge PNG images:

    sudo apt install libpng12-dev
    cd ~/develop
    wget https://github.com/amadvance/scale2x/releases/download/v4.0/scale2x-4.0.tar.gz
    tar zxf scale2x-4.0.tar.gz
    cd scale2x-4.0
    ./configure --prefix=$HOME/.local
    make
    make install

Build FCEUX (SDL) from source because the version in SVN is newer
than the one in Ubuntu's repository.

    sudo apt install git-svn scons libsdl-image1.2-dev libgtk2.0-dev
    sudo apt install libgd-dev liblua5.1-0-dev
    cd ~/develop
    git svn clone svn://svn.code.sf.net/p/fceultra/code/fceu/trunk fceux
    cd fceux
    nice scons -j2
    scons --prefix=$HOME/.local install

Once a month, track latest changes:

    cd ~/develop/fceux
    git svn rebase
    nice scons -j2
    scons --prefix=$HOME/.local install

Build *NetPuzzleArena*, a work-in-progress *Puzzle League* clone by
Josh "NovaSquirrel" Hoffman:

    sudo apt install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    cd ~/develop
    git clone https://github.com/NovaSquirrel/NetPuzzleArena.git
    cd NetPuzzleArena
    make -j2

Build the NSF and S3M to WAVE converter [gmewav]:

    sudo apt install libdumb1-dev libgme-dev
    mkdir -p ~/develop/gmewav
    wget -O gmewav.zip https://forums.nesdev.com/download/file.php?id=9899
    unzip gmewav.zip
    make
    cp ./gmewav ~/.local/bin

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

[gmewav]: https://forums.nesdev.com/viewtopic.php?p=200347#p200347
[skype4pidgin]: https://github.com/EionRobb/skype4pidgin
[Purple Discord]: https://github.com/EionRobb/purple-discord

Wine is not an emulator
-----------------------
Install Microsoft proprietary fonts needed for some applications and
websites.  Ubuntu has a package for this, but the download locations
in its package are out of date.  This causes configuration to fail,
which in turn causes Update Notifier to make repeated pop-ups.
So install Debian's newer package.

    wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
    sudo dpkg -i ttf-mscorefonts-installer_3.6_all.deb

Install compatibility with 32- and 64-bit Windows applications, which
adds 735 MB to the HDD footprint:

    sudo apt install wine

The things I'm most likely to run in Wine:

* OpenMPT (free sample-based music editor, formerly ModPlug Tracker)
* FCEUX (free NES emulator with debugger)
* FamiTracker (free NES music editor)
* NO$SNS (proprietary Super NES emulator, which runs at full speed on
  an Atom unlike bsnes-plus)
* BGB (proprietary Game Boy emulator)

Proprietary crap
----------------
Get the Ubuntu .deb from for [Dropbox] matching your distribution.

Install it and fetch its dependencies:

    sudo dpkg -i ~/Downloads/dropbox_2015.10.28_amd64.deb

After running `dpkg -i`, you need to install `--fix-broken` (or
`-f` for short), a pseudo-package that causes APT to look in the
repositories for unmet dependencies of recently installed packages.

    sudo apt install -f

Then sign in to Dropbox.

[Dropbox]: https://www.dropbox.com/install-linux
