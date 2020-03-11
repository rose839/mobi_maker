# -*- coding: utf-8 -*-

import platform
import os

import mobi_maker

path = mobi_maker.__path__[0]

system = platform.system()

if system == "Linux":
    kindlegen = os.path.join(path, 'bin/linux/kindlegen')
elif system == "Darwin":
    kindlegen = os.path.join(path, 'bin/mac/kindlegen')
else:
    raise Exception("Not supported system: {}.".format(system))