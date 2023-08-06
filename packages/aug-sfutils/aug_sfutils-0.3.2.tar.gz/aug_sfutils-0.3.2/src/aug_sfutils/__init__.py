#!/usr/bin/env python

# sfutils

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/~git/pyaug/sfread.html

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.3.2'
__date__    = '14.10.2021'

import sys, logging

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
hnd.setLevel(level=logging.INFO)
logger = logging.getLogger('aug_sfutils')
logger.addHandler(hnd)
logger.setLevel(logging.INFO)
logger.propagate = False

from .sfread import *
from .sf2equ import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *
try:
    from .ww import *
    from .sfh import *
except:
    logger.warning('ww and sfh not loaded, SFREAD and EQU available')
    pass

import encodings.utf_8
