#!/usr/bin/env python3
"""
Tool to analyze a journal and sum time into categories

Copyright 2026 Damian Yerrick
SPDX-License-Identifier: Apache-2.0
"""
import os, sys, argparse, re
from collections import defaultdict

dateRE = re.compile(r"""
^.{0,10}  # allow leading day of week but not sentence-internal dates
(2[0-2][0-9][0-9])-([0-9][0-9])-([0-9][0-9])\b
""", re.VERBOSE)
timeRE = re.compile(r"""
([0-2][0-9]):([0-5][0-9])\s+(.*)
""", re.VERBOSE)


def load_journal(lines):
    categories = {}

    lines_by_date = defaultdict(list)
    key = None
    for line in infp:
        line = line.strip()
        if not line: continue
        if line.startswith("count "):
            kw = line[6:].split(" as ", 1)
            synonym, category = kw[0].strip().lower(), kw[-1].strip()
            categories[synonym] = category
            categories[category.lower()] = category
            continue
        m = dateRE.search(line)
        if m:
            key = m.groups()
            continue
        if key is None:
            print("leading line", line, file=sys.stderr)
            continue
        m = timeRE.match(line)
        if m:
            lines_by_date[key].append(m.groups())
            continue
        if False: print("stray line", line, file=sys.stderr)
    return lines_by_date, categories

def get_durations(events):
    last_minute = last_thing = None
    out = []
    for hour, minute, thing in events:
        end_minute = int(hour) * 60 + int(minute)
        if last_minute is not None:
            if last_minute >= end_minute:
                print("reverse for %02d:%02d to %02d:%02d"
                      % (*divmod(last_minute, 60),  *divmod(end_minute, 60)),
                      file=sys.stderr)
            out.append((end_minute - last_minute, last_thing))
        last_minute, last_thing = end_minute, thing
    return out

with open("/home/pino/Documents/journal 2026-06.txt", "r") as infp:
    journal, categories = load_journal(infp)
keyword_time = {keyword: 0.0 for keyword in categories.values()}
nonkeyword_time = []
total_minutes = 0
for k, v in journal.items():
    for minutes, thing in get_durations(v):
        total_minutes += minutes
        thing_lower = thing.lower()
        found_words = {v for k, v in categories.items() if k in thing_lower}
        if found_words:
            for k in found_words:
                keyword_time[k] += minutes / len(found_words)
        else:
            nonkeyword_time.append((minutes, thing))
keyword_time = sorted(((t, k) for k, t in keyword_time.items()),
                      reverse=True)
total_keyword_time = sum(x[0] for x in keyword_time)
print("Classified time: %4d:%02d (%4.1f%%)"
      % (*divmod(total_keyword_time, 60),
         ((total_keyword_time) * 100.0 / total_minutes)))
print("\n".join(
    "%4d:%02d (%4.1f%%) %s"
    % (*divmod(t, 60), t * 100.0 / total_minutes, k)
    for t, k in keyword_time
))
total_nonkeyword_minutes = total_minutes - total_keyword_time
print("Unclassified time: %4d:%02d (%4.1f%%)"
      % (*divmod(total_nonkeyword_minutes, 60),
         ((total_nonkeyword_minutes) * 100.0 / total_minutes)))
print("\n".join(
    "%4d:%02d %s" % (*divmod(t, 60), k) for t, k in nonkeyword_time
))
