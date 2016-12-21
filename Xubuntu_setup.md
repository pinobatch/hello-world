Once Xubuntu is installed, it's time to set it up.

The absolute first thing is to turn off keyboard backlighting on
machines that don't have it.  Otherwise, a bug in Linux itself causes
the system to hang during boot ([Bug 107651]).  Open a terminal
and disable this feature:

    sudo systemctl mask systemd-backlight@leds\:dell\:\:kbd_backlight.service

[Bug 107651]: https://bugzilla.kernel.org/show_bug.cgi?id=107651

First round of apt-get
----------------------

Open a terminal, check for updated software, and install it:

    sudo apt-get update
    sudo apt-get dist-upgrade

While that's running, open Terminal preferences:

* Change the font to Ubuntu Mono 9 to fit two terminals
  side-by-side on a 1024-pixel-wide display.
* Set the default geometry to 35 rows tall.
* Set the background to transparent, with 0.90 opacity, and the
  background color to actual black (`#000000`)

At this point, APT will have installed an updated `linux-image`
package.  Updates to `linux-image` require a reboot.

Then install useful free software:

    sudo apt install build-essential gimp git vorbis-tools audacity
    sudo apt install python3-numpy hexchat python3-pil idle3 ffmpeg
    sudo apt install libreoffice-impress libreoffice-draw sqlite3
    sudo apt install oidentd advancecomp

Interestingly enough, `python3-pil` comes with Xubuntu 16.04.

Install compatibility with Qt applications, which adds 123 MB to the
HDD footprint:

    sudo apt install retext sqlitebrowser

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

Other fonts to download include Wasted Collection, Comic Neue,
and Patrick Hand.

Power Manager:

* When laptop lid is closed on battery: Suspend
* Suspend when inactive for 15 minutes on battery
* On critical battery power (10%), ask
* Blank screen after 5 minutes on battery or 15 minutes plugged in
* Put display to sleep one minute after blanking

GIMP:

* Enable single-window mode
* Tool Options: Change to Pixel brush at size 1
* Patterns: Change to Clipboard
* Save Tool Options Now
* Theme: Small
* Default grid spacing: 8 pixels
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

* Update EFnet server list
* Set my nick
* Set my real name in Preferences > Chatting > Advanced

[Jester]: http://www.dafont.com/jester.font

Firefox
-------
Firefox beta is stable enough for me, plus 51 is more likely to offer
multiprocess windows (aka Electrolysis or e10s) to Ubuntu users than
50 because the Ubuntu Modifications extension isn't explicitly marked
as compatible with e10s.

    sudo add-apt-repository ppa:mozillateam/firefox-next
    sudo apt-get update
    sudo apt-get upgrade

Change these preferences:

* Default serif font for Latin script: Jester
* `browser.tabs.remote.autostart`: true  
  (This enables e10s.)
* `privacy.trackingprotection.enabled`: true  
  (This enables tracking blocking similar to the Disconnect extension
  even outside Private Browsing windows.)

Some of these preferences take effect once Firefox is restarted.
So install some extensions that also require a restart:

* Stylish
* HTTPS Everywhere

Some sites are deliberately incompatible with Disconnect because
their administrators fail to figure out how to serve ads that don't
track users across websites.  So I just ignore articles on those
sites and block them at the DNS level to keep from visiting them by
mistake.  Others are social networks that build a dossier about
non-members' viewing habits, but which are left out of Disconnect's
list for the benefit of members.

    gksudo mousepad /etc/hosts
    
    # Sites deliberately incompatible with tracking protection
    0.0.0.0 www.wired.com
    0.0.0.0 www.theinquirer.net
    0.0.0.0 www.theatlantic.com
    
    # Social networks to which I don't belong
    0.0.0.0 www.facebook.com

Building applications from source
---------------------------------
Build cc65:

    mkdir ~/develop
    cd ~/develop
    git clone https://github.com/cc65/cc65.git
    cd cc65
    nice make -j2
    make install prefix=~/.local

And add it to your `PATH` for next time you log in:

    mousepad ~/.bashrc

    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$HOME/.local/bin:$PATH"
    fi

FCEUX (SDL) in SVN is newer than the one in Ubuntu's repository.

    sudo apt install git-svn scons libsdl-image1.2-dev libgtk2.0-dev
    sudo apt install libgd-dev liblua5.1-0-dev
    cd ~/develop
    git svn clone svn://svn.code.sf.net/p/fceultra/code/fceu/trunk fceux
    cd fceux
    nice scons -j2
    scons --prefix=$HOME/.local install

Build *NetPuzzleArena*, a work-in-progress *Puzzle League* clone by
Josh "NovaSquirrel" Hoffman:

    sudo apt install libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    cd ~/develop
    git clone https://github.com/NovaSquirrel/NetPuzzleArena.git
    cd NetPuzzleArena
    make -j2

Set up Git to identify you when committing changes to your own
repositories.  (These are commented out to discourage copying and
pasting without the address changed.)

    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"

Wine is not an emulator
-----------------------

Install Microsoft proprietary fonts needed for some applications and
websites.  Ubuntu has a package for this, but the download locations
in its package are out of date.  This causes configuration to fail,
which in turn causes Update Notifier to fail.  So install Debian's
newer package.

    wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
    sudo dpkg -i ttf-mscorefonts-installer_3.6_all.deb

Install compatibility with 32- and 64-bit Windows applications, which
adds 735 MB to the HDD footprint:

    sudo apt install wine

The things I'm most likely to run in Wine:

* ModPlug Tracker (free sample-based music editor)
* FCEUX (free NES emulator with debugger)
* FamiTracker (free NES music editor)
* NO$SNS (proprietary Super NES emulator, which runs at full speed on
  an Atom unlike bsnes)

Proprietary crap
----------------
Get the Ubuntu .deb from for [Dropbox] matching your distribution.
Also install [Skype 4.3] for Ubuntu 12.04 "Precise" (32-bit), which
uses less RAM than the Chromium-based Skype for Linux alpha.

Then install them and their dependencies:

    sudo dpkg -i ~/Downloads/dropbox_2015.10.28_amd64.deb
    sudo dpkg -i ~/Downloads/skype-ubuntu-precise_4.3.0.37-1_i386.deb
    sudo apt-get -f install

Then sign in to Dropbox and Skype.

Skype settings:

* Style: GTK+
* Save files to `~/Downloads`
* Allow chats from anybody
* Disable Skype WiFi

[Dropbox]: https://www.dropbox.com/install-linux
[Skype 4.3]: https://www.skype.com/
