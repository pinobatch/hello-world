#!/usr/bin/env python3
"""
Tool to count screen time in Discord in Firefox

Copyright 2026 Damian Yerrick
SPDX-License-Identifier: Apache-2.0

Requires X11 and xdotool
"""
import os, sys, time, datetime, re
import subprocess as sp
from collections import defaultdict

# Data collection ###################################################

getpid_cmd = """
xdotool search --onlyvisible --class ? getwindowpid %@
""".split()
searchname_cmd = """
xdotool search --all --pid ? --name ? getwindowname
""".split()
classRE = r"""firefox"""
nameRE = r"""Discord \| """
logname = "/home/pino/Documents/fxscreentime_log_2026-07.txt"

xdo_last_error = None

def xdo_get_names_by_class(classRE, nameRE):
    """Search for window names matching an X11 class and name.

Call xdotool to perform the search, which treats classRE and nameRE
as case-insensitive extended regular expressions as defined by POSIX:

classRE -- regular expression matching the X11 "class" of a process
nameRE -- regular expression matching window names belonging to
    that process

Return a list of window names.

Based on Volker Siegel's answer at
https://unix.stackexchange.com/a/306146/119806
"""
    global xdo_last_error

    # Get browser PID
    cmd = list(getpid_cmd)
    cmd[cmd.index('?')] = classRE
    try:
        pid = sp.check_output(cmd)
    except sp.CalledProcessError as e:
        err = "Firefox not open (status %d)" % e.returncode
        if err != xdo_last_error:
            xdo_last_error = err
            print(err, file=sys.stderr)
        return []
    pid = pid.split(None, 1)[0].decode("ascii")

    # Get browser's window names
    cmd = list(searchname_cmd)
    cmd[cmd.index('?')] = pid
    cmd[cmd.index('?')] = nameRE
    try:
        output = sp.check_output(cmd)
    except sp.CalledProcessError as e:
        err = ("Discord not active tab (Firefox pid %s, status %d)"
               % (pid, e.returncode))
        if err != xdo_last_error:
            xdo_last_error = err
            print(err, file=sys.stderr)
        return []

    xdo_last_error = None  # print first error after valid sample
    return output.decode("utf-8").strip().split("\n")

def extract_server(name):
    """Given a Firefox window name, extract a Discord server name.

Window names take one of the following forms, where an em dash
separates the page title from the browser name and then pipes
separate the platform, channel name, and server name.

    Platform | Server — Browser
    Platform | #channel | Server — Browser
"""
    minus_firefox = name.split("—", 1)[0]
    minus_discord = minus_firefox.split("|", 1)[-1].strip()
    if minus_discord.startswith("#"):
        minus_channel = minus_discord.split("|", 1)[-1].strip()
    else:
        minus_channel = minus_discord
    return minus_channel

MAX_NAP_LENGTH = 3

def sleep_until(end_time):
    """Sleep until a given timestamp.

If the program is running in IDLE's Python Shell, every
MAX_NAP_LENGTH seconds, write the empty string to standard output
to let the shell check for KeyboardInterrupt.
"""
    if 'idlelib' not in sys.modules:
        now = time.time()
        naptime = min(MAX_NAP_LENGTH, end_time - now)
        if naptime > 0: time.sleep(naptime)
        return
        
    while True:
        sys.stdout.write("")  # tickle IDLE
        now = time.time()
        naptime = min(MAX_NAP_LENGTH, end_time - now)
        if naptime <= 0: return
        time.sleep(naptime)

def log_to_fp(logfp, sample_period=15):
    """Log the frontmost Discord window to a file.

First print the current local date to logfp in the form:

    Dow yyyy-mm-dd

Then every sample_period seconds, print the local time and name of
the visible server to both sys.stdout and logfp in the form:

    hh:mm:ss server name

While the browser is not open or Discord is not the active tab, pause
writing to logfp and occasionally print a diagnostic to sys.stderr.
"""
    now = int(round(time.time() / sample_period) + 1) * sample_period
    dtnow = datetime.datetime.now()
    print(dtnow.strftime("%a %Y-%m-%d"), file=logfp)
    since_fflush = 0
    while True:
        next_sample = (int(round(time.time() / sample_period) + 1)
                       * sample_period)
        sleep_until(next_sample)
        names = xdo_get_names_by_class(classRE, nameRE)
        since_fflush += 1
        if names:
            dtnext = datetime.datetime.fromtimestamp(next_sample, datetime.timezone.utc).astimezone()
            logline = ("%s %s\n"
                       % (dtnext.strftime("%H:%M:%S"), extract_server(names[0])))
            sys.stdout.write(logline)
            logfp.write(logline)
            if since_fflush >= 4:
                since_fflush = 0
                logfp.flush()

# Data analysis #####################################################

log_eventRE = re.compile(r"""
^\s*([0-2][0-9]):([0-5][0-9]):([0-5][0-9])\s+(.*)
""", re.VERBOSE)
log_dateRE = re.compile(r"""
^.{0,10}  # allow leading day of week but not sentence-internal dates
(2[0-2][0-9][0-9])-([0-1][0-9])-([0-3][0-9])\b
""", re.VERBOSE)

# If next sample not within next 60 seconds, assume the previous
# sample lasted 60 seconds.  This takes into account browsing
# the web to research an answer to a question asked in a server.
event_sticky_time = 60
    
def read_log(logfp):
    last_date, last_name, last_hms = None, None, 0
    events = []
    no_match_lines = set()
    servers_to_ignore = set()
    for line in logfp:
        line = line.strip()
        if not line or line.startswith("#"): continue

        if line.startswith("ignore "):
            servers_to_ignore.add(line[7:].strip())
            continue
            
        m = log_eventRE.match(line)
        if m:
            # Line includes a local time of day and a server name
            hour, minute, second, name = m.groups()
            hms = (int(hour) * 60 + int(minute)) * 60 + int(second)
            if last_name is not None:
                duration = (hms - last_hms
                            if last_hms <= hms <= last_hms + event_sticky_time
                            else event_sticky_time)
                if duration > 0:
                    events.append((last_date, last_name, duration))
            last_date, last_name, last_hms = date, name, hms
            continue

        m = log_dateRE.match(line)
        if m:
            date = "-".join(m.groups())  # YYYY-MM-DD
            continue

        if line not in no_match_lines:
            no_match_lines.add(line)
            print("no match", line)

    totals = defaultdict(lambda: defaultdict(int))
    for date, name, duration in events:
        if name in servers_to_ignore: continue
        totals[date][name] += duration

    totals = [
        (date, sorted(daytotals.items(), key=lambda x: x[1], reverse=True))
        for date, daytotals in sorted(totals.items(), key=lambda x: x[0])
    ]
    for date, daytotals in totals:
        daytotal = sum(duration for name, duration in daytotals)
        print("%s: %.2f minutes" % (date, daytotal / 60))
##        totalbreak = min(i for i, (name, duration) in enumerate(daytotals)
##                         if i > 0 and duration <= daytotals[0][1] // 5)
        totalbreak = 4
        print("\n".join("%6.2f (%4.1f%%) %s"
                        % (duration / 60, duration * 100 / daytotal, name)
                        for name, duration in daytotals[:totalbreak]))
        other = sum(duration for name, duration in daytotals[totalbreak:])
        if other > 0:
            print("%6.2f (%4.1f%%) %s"
                  % (other / 60, other * 100 / daytotal, "Other"))

    grandtotals = defaultdict(int)
    for date, daytotals in totals:
        for name, duration in daytotals:
            grandtotals[name] += duration
    grandtotals = sorted(grandtotals.items(), key=lambda x: x[1], reverse=True)
    grandtotal = sum(duration for name, duration in grandtotals)
    print("Grand totals")
    print("\n".join("%6.2f (%4.1f%%) %s"
                    % (duration / 60, duration * 100 / grandtotal, name)
                    for name, duration in grandtotals[:10]))
    other = sum(duration for name, duration in grandtotals[10:])
    print("%6.2f (%4.1f%%) %s"
          % (other / 60, other * 100 / grandtotal, "Other"))

def main():
    with open(logname, "r") as logfp:
        read_log(logfp)
    with open(logname, "a") as logfp:
        print("fxscreentime: logging Discord to %s"
              % logname, file=sys.stderr)
        log_to_fp(logfp)

if __name__=='__main__':
    main()
