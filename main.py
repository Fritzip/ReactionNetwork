import time
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import colorsys

from reactor import *
import ubigraph


####################################################################
#			Initialisation
####################################################################

N = 200
kcoll = 0.1
kconf = 0.9
tmax = 1000

test = 6
if test == 1:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a2a1']
	l_type = ['a']
	
if test == 2:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a1a2']
	l_type = ['a']
	
if test == 3:
	d_init_part = {'a0':N, 'b0':N, 'b1':1}
	d_init_grap = {}	
	l_rules = ['a0+b1=a1b2', 'a1b3=a2b2', 'a0+a1=a2a1', 'b2+b0=b3b2' ]
	l_type = ['a', 'b']

if test == 4:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a0a1','a0a1=a2a3', 'a3a2=a0a1']
	l_type = ['a']

if test == 5:
	d_init_part = {'a0':N, 'a1':10, 'b0':N, 'b1':10, 'c0':N, 'c1':10}
	d_init_grap = {}	
	l_rules = ['*0+*1=*2*2', '*0+#2=*1#2', '*2#2=*2+#1']
	l_type = ['a', 'b', 'c']

if test == 6:
	d_init_part = {'a0':N, 'a1':10, 'b0':N, 'b1':10, 'c0':N, 'c1':10}
	d_init_grap = {}	
	l_rules = ['*0+#1=*0#1']
	l_type = ['a', 'b', 'c']

if test == 7:
	l_type = ['a', 'b', 'c', 'd', 'e', 'f']
	d_init_part = {'a0':N/6, 'b0':N/6, 'c0':N/6, 'd0':N/6, 'e0':N/6, 'f0':N/6}
	d_init_grap = {"e8-a1-b1-c1-d1-f1":1}	
	l_rules = ['e8+e0 = e4e3', '*4#1 = *2#5', '*5+*0 = *7*6', '*3+#6 = *2#3', '*7#3 = *4#3', 'f4f3 = f8+f8', '*2#8 = *9#1', '*9#9 = *8#8']


####################################################################
#			Launch Gillespie Algorithm
####################################################################
f = open('simu','w')
start = time.time()

r = Reactor.from_particles_init(d_init_part, d_init_grap, l_rules, l_type, kcoll, kconf, tmax, f) 

# print r.g.d_state_type
# print r.g.d_pair
t = r.gillespie()
if t < tmax : print "\n Out before end of time. Cause : no more reaction available"
# print r.g.d_state_type
# print r.g.d_pair

end = time.time()
print end - start

f.close()


####################################################################
#			Output
####################################################################

if VISU and SAVE:
	import subprocess
	bashCommand = "./ubigraph_server &"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	time.sleep(1)
	
	import ubigraph
	U = ubigraph.Ubigraph()
	U.clear()

	d_adj = {}
	d_state = {}
	l_vert = []
	d_edges = {}

	f = open('simu', 'r')
	l_part = f.readline().split()
	for i, part in enumerate(l_part):
		d_adj[i] = 0
		d_state[i] = int(part[1])
		l_vert.append( U.newVertex( visible = True, shape = "sphere" ) )

	for line in f:
		time.sleep(0.01)
		i, j, k = map(int, line.split())
		if abs(k) == 1:
			d_adj[i] += k
			d_adj[j] += k
			if   k ==  1: d_edges[make_tpl(i,j)] = U.newEdge(l_vert[i], l_vert[j])
			elif k == -1: d_edges[make_tpl(i,j)].destroy()
			# opt : mod size vert and visibility
			# if d_adj[i] : l_vert[i].set(visible=True)
			# else : l_vert[i].set(visible=False)
			# if d_adj[j] : l_vert[j].set(visible=True)
			# else : l_vert[j].set(visible=False)
			if d_adj[i] : l_vert[i].set(size=0.7*d_adj[i])
			if d_adj[j] : l_vert[j].set(size=0.7*d_adj[j])

		elif k == 0:
			d_state[i] = j
			# opt : mod label + couleur

	# print l_part
	# print d_adj
	# print d_state



if PLOT:
	fig = plt.figure()
	cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

	plt1 = fig.add_subplot(1,2,1)
	for key in r.d_y_evol_type.keys():
		x, y = r.time_vect, r.d_y_evol_type[key]
		try:
			if SMOOTH: x, y = smoothinterp(x, y) 
		except: pass
		plt.plot(x, y, linewidth=2, label=key)
	plt.legend(loc='best')

	plt2 = fig.add_subplot(1,2,2)
	for key in r.d_y_evol_pair.keys():
		x, y = r.time_vect, r.d_y_evol_pair[key]
		try:
			if SMOOTH:x, y = smoothinterp(x, y) 
		except: pass
		plt.plot(x, y, linewidth=2, label=key)
	plt.legend(loc='best')

	plt.show(block=True)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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