#!/usr/bin/env python

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/aug/manuals/aug_sfutils

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.3.4'
__date__    = '15.10.2021'

import sys, logging

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logger = logging.getLogger('aug_sfutils')
logger.addHandler(hnd)
logger.setLevel(logging.INFO)

try: # wrapper classes, available only with afs-client and kerberos access
    from .ww import *
    from .sfh import *
    from .journal import *
except:
    logger.warning('ww and sfh not loaded, SFREAD and EQU available')
    pass

from .sfread import *
from .sf2equ import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *

import encodings.utf_8
