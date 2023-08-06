#!/usr/bin/env python

"""GUI for running ControlRoom, parallel, with interfaces to TRANSP, ASCOT, TORIC

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.0.1'
__date__    = '16.10.2021'

import os, sys, logging
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
hnd = logging.StreamHandler()
hnd.setFormatter(fmt)
logger = logging.getLogger('ControlRoom')
logger.addHandler(hnd)
logger.setLevel(logging.INFO)

from .fi2nspec import *
