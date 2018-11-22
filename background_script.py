# !/usr/bin/env python

import signal
import subprocess
import sys
from gfxhat import touch


def handler(channel, event):
    print("Got {} on channel {}".format(event, channel))
    pid = subprocess.Popen([sys.executable, "manager.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
    exit(0)


for x in range(6):
    touch.on(x, handler)

signal.pause()
