#! /usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import os
import argparse
import struct
from datetime import datetime

import numpy as np
from scipy.interpolate import interp1d


####################################################################
#			Global functions
####################################################################

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def get_col(rgb_col, state):
	return '#'+struct.pack('BBB',*rgb_col).encode('hex')

def quit_figure(event):
	if event.key == 'q' or event.key == 'escape':
		plt.close('all')

def smoothinterp(t, y):
	window_size = 31
	order = 1

	tnew = np.linspace(t[0], t[-1], 400)
	f = interp1d(t, y, kind='linear')
	y = f(tnew)

	y = savitzky_golay(y, window_size, order)

	return tnew, y

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
	import numpy as np
	from math import factorial

	try:
		window_size = np.abs(np.int(window_size))
		order = np.abs(np.int(order))
	except ValueError, msg:
		raise ValueError("window_size and order have to be of type int")
	if window_size % 2 != 1 or window_size < 1:
		raise TypeError("window_size size must be a positive odd number")
	if window_size < order + 2:
		raise TypeError("window_size is too small for the polynomials order")
	order_range = range(order+1)
	half_window = (window_size -1) // 2
	# precompute coefficients
	b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
	m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
	firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
	lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
	y = np.concatenate((firstvals, y, lastvals))
	return np.convolve( m[::-1], y, mode='valid')

def update_progress(label, nb, nbmax, unit="", bar_length=25 ): # small 20, medium 25, large 50
	progress = int(nb*100/nbmax)
	if progress > 100 : progress = 100
	sys.stdout.write('\r{2:<20} [{0}] {1:3d}% \t {3:.2f}/{4:.2f} {5}'.format('#'*(progress/int(100./bar_length))+'-'*(bar_length-(progress/int(100./bar_length))), progress, label, nb, nbmax, unit ))
	sys.stdout.flush()
	

####################################################################
#			Colors
####################################################################
# For plots
HEADER = '\033[1m' # bold
KBLU = '\033[94m' # blue
KGRN = '\033[92m' # green
KYEL = '\033[93m' # yellow
KRED = '\033[91m' # red
UNDERLINE = '\033[4m'
KNRM = '\033[0m' # back to normal

# For graph
COLORS = [(230, 41, 41), (189, 41, 230), (50, 41, 230), (41, 183, 230), (41, 230, 88), (221, 230, 41), (230, 164, 41)]
random.shuffle(COLORS)
COLORS = COLORS*2

####################################################################
#			Global Parameters (default)
####################################################################
VISU = True
PLOT = False
ECHO = False
RUN = True
PROGRESS = True

####################################################################
#			Arguments parser
####################################################################
parser = argparse.ArgumentParser(description="Biological Reaction Network Simulator",usage='%(prog)s [options]')
group = parser.add_mutually_exclusive_group()
filegrp = parser.add_mutually_exclusive_group()

group.add_argument("-v", "--verbose", action="store_true", default=0)
group.add_argument("-q", "--quiet", action="store_true", default=0)
parser.add_argument("--no-progress", action="store_true", default=0, help="Disable the progress bar")

parser.add_argument("-p","--plot", action="store_true", default=0, help="Plot particles evolution")
parser.add_argument("-x","--novisu", action="store_true", default=0, help="Disable dynamic graph visualisation")


DEFAULT_FILE = '../DATA/last_run'
filegrp.add_argument("-i", dest="inputfile", help="Launch a simulation from a file", nargs='?', metavar="FILE", type=lambda x: is_valid_file(parser, x), const=DEFAULT_FILE)
filegrp.add_argument("-o", dest="outputfile", help="Save the simulation into a file", nargs='?', metavar="FILE", const=DEFAULT_FILE)

args = parser.parse_args()

print args

if args.verbose:
	ECHO=True
	PROGRESS = False
elif args.quiet:
	ECHO=False
	PROGRESS = False

if args.no_progress:
	PROGRESS = False

if args.novisu:
	VISU = False

if args.plot:
	PLOT = True

if args.inputfile == DEFAULT_FILE:
	print "default input"
	PATH = DEFAULT_FILE
	RUN = False
elif args.inputfile:
	print "input"
	RUN = False
	PATH = args.inputfile


if args.outputfile == DEFAULT_FILE:
	print "timed output"
	PATH = '../DATA/simulation-'+datetime.now().strftime('%H:%M:%S')
	RUN = True
elif args.outputfile:
	print "specified output"
	PATH = args.outputfile
	RUN = True

if args.outputfile == None and args.inputfile == None:
	print "last run output save"
	PATH = DEFAULT_FILE
	RUN = True

if not os.path.exists("../DATA"):
	os.makedirs("../DATA")