import random
import colorsys
import struct


####################################################################
#			Global Parameters (default)
####################################################################
VISU = True
PLOT = False
SMOOTH = True
ECHO = False
SAVE = True

COLORS = [(230, 41, 41), (189, 41, 230), (50, 41, 230), (41, 183, 230), (41, 230, 88), (221, 230, 41), (230, 164, 41)]
random.shuffle(COLORS)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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