#!/usr/bin/env python

# sfutils

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/~git/pyaug/sfread.html

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.2.9'
__date__    = '12.10.2021'

import sys, logging

fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logging.root.addHandler(hnd)
logging.root.setLevel(logging.INFO)
log = logging.getLogger()

from .sfread import *
from .sf2equ import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *
try:
    from .ww import *
    from .sfh import *
except:
    log = logging.getLogger()
    log.warning('ww and sfh not loaded, SFREAD and EQU available')
    pass

import encodings.utf_8
