#!/usr/bin/env python
# coding: utf-8

"""Parse bank statements
"""

__author__  = 'Giovanni Tardini'
__version__ = '0.1.1'
__date__    = '12.10.2021'

import logging

fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logging.root.addHandler(hnd)
logging.root.setLevel(logging.INFO)

from .parse_bank_statements import *

import encodings.utf_8
