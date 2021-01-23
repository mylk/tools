#!/usr/bin/env python

from datetime import datetime
import os
import qrcode
import sys

url = sys.argv[1]

now = datetime.now().strftime('%Y%m%d%H%M%S')
filename = "/tmp/qr_{}.png".format(now)

img = qrcode.make(url)
img.save(filename)

os.system('/usr/bin/firefox --new-tab {}'.format(filename))

