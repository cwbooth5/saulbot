#!/usr/bin/python

import re, fileinput

nick = 'saul'

r = re.compile("<.*%s.*> (.*)" % nick)

for L in fileinput.input():
    m = r.search(L)
    if m:
        print m.group(1)


