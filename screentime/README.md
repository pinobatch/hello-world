Screen time analysis scripts
============================

The only good spyware is self-spyware.

After the pandemic, I experienced a time management skill issue.
Something was leaving me with no time to engage with my hobbies.
It came to a head in 2026, when I felt overwhelmed and said
something in a chat room that deeply hurt another member.
That's when I wrote these scripts to get to the bottom of this
by monitoring how I spend my time on my computer outside work.

No LLM tools were used in the production of these scripts.

analyze_journal.py
------------------

I manually wrote down what I was doing at all times each day for 28
days. I ended up discovering that I had [Discord] open outside work
for over 5 hours each day.  I realized that this could not continue.

A log file has three kinds of items: countable activities, dates,
and activity start times.  Countable activities can set up a synonym
(with `as`) or not.  Dates are in ISO 8601 format, optionally
preceded by a day of week.  Activity start times are in 24-hour
format, where the end time is the start time of the next activity.
For example, 17:05 followed by 17:08 means three minutes.

    count Slashdot
    count Wikipedia
    count Bluesky
    count Mastodon
    count shower as hygiene
    count care of teeth as hygiene
    count care of nails as hygiene
    count nap as screen off

    Mon yyyy-mm-dd
    hh:mm activity
    hh:mm activity

    Tue yyyy-mm-dd
    hh:mm activity
    hh:mm activity

If a log line contains the name of more than one activity, time
between that line and the next is divided up evenly among them.

fxscreentime.py
---------------

Uses [xdotool] to read the name of the open Firefox window and parse
it to find which Discord server is active.  It should work on Xfce
or any other desktop environment for X Window System.

It writes the local date to a log file when it starts.  Then every
15 seconds, it calls xdotool to query Firefox's process identifier
(pid) and window names associated with that pid.  If Discord is the
active tab, it writes the current local time and what it thinks is
the server name or the other participants in a group chat.

    ignore Friends
    ignore @Alice Boss
    ignore @Bob Coworker

    Sun 2026-07-26
    15:13:45 BlastEm
    15:14:00 gbdev
    15:14:15 gbdev
    15:14:30 gbadev
    15:14:45 Friends

Servers to disregard are specified at the top of the log with ignore
lines.  "Friends" represents time when Discord is open and I am not
interacting with it.  Other servers and usernames may represent time
spent at work.

On the next run, it rereads the log, counts how long the browser's
window name showed each server, and shows the servers viewed for the
longest time each day.  If a sample is missing, such as if Discord
was not active during the sample, it extends the previous sample up
to one minute.  This accounts for, say, opening another website to
do research while composing a message.

Use of xdotool inspired by [Volker Siegel's answer]

### Why not Wayland?

Wayland focuses on security over functionality.  It lacks widely used
protocol extensions for several things that are possible under X.
This [breaks workflows], including screen time monitoring.

Further reading
---------------

* "[Quantified self]" on Wikipedia
* [r/QuantifiedSelf] on Reddit
* [selfspy], a larger-scope self-monitoring daemon for desktop
  computers

[Discord]: https://discord.com/
[xdotool]: https://github.com/jordansissel/xdotool
[Volker Siegel's answer]: https://unix.stackexchange.com/a/306146/119806
[breaks workflows]: https://xkcd.com/1172/
[Quantified self]: https://en.wikipedia.org/wiki/Quantified_self
[r/QuantifiedSelf]: https://www.reddit.com/r/QuantifiedSelf/
[selfspy]: https://github.com/selfspy/selfspy
