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

Then install useful free software:

    sudo apt install build-essential gimp git vorbis-tools audacity
    sudo apt install python3-numpy hexchat python3-pil idle3 ffmpeg

Interestingly enough, `python3-pil` comes with Xubuntu 16.04.

Install compatibility with Qt applications, which adds 123 MB to the
HDD footprint:

    sudo apt install retext sqlitebrowser

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

Set up the panel
----------------

Add a second panel, semi-inspired by a cross between Unity's panel
and my LCARS mockup:

1. Deskbar orientation, always autohide, 128px wide, 75% length;
   appearance: 75% background alpha.
2. Drag it to the bottom left corner and lock it.
3. Add a Quicklauncher to the new panel.
4. Move the window buttons to the new panel below the Quicklauncher.

Quicklauncher is 2 columns:

1. `firefox` and `mousepad`
2. `xfce4-terminal` and `gnome-calculator`
3. `gimp` and ???

With the window buttons out of the way, we have room for other things
on the top panel:

1. Change the Whisker Menu to display icon and title, and change its
   title to Start.
2. Add Show Desktop and Directory Menu to the right of Start.
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
* `browser.tabs.remote.autostart`: True

Some of these preferences won't take effect until Firefox is
restarted.  So install some extensions, some of which also require
a restart:

* Stylish

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

Set up Git to identify you when committing changes to your own
repositories.  (These are commented out to discourage copying and
pasting without the address changed.)

    #git config --global user.email "jdoe@example.com"
    #git config --global user.name "John Doe"

Proprietary crap
----------------

Get the Ubuntu .deb from for [Dropbox] and [Skype 4.3] for Ubuntu,
12.04 "Precise" (32-bit), which uses less RAM than the Chromium-based
Skype for Linux alpha.

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

The third proprietary program I regularly use is the NO$SNS emulator
by Martin Korth, which runs at full speed on an Atom unlike anything
bsnes-based.  *TODO: describe this*

[Dropbox]: https://www.dropbox.com/install-linux
[Skype 4.3]: https://www.skype.com/
