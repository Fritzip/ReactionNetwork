import math 
import random
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from rule import *
from graph import *


class Reactor():
	"""Init and run Gillespie algorithm"""
	def __init__(self, graph, l_rules, kcoll, kconf, tmax):
		self.g = graph
		self.l_rules = [Rule(elem) for elem in l_rules]
		self.kconf = kconf
		self.kcoll = kcoll
		self.tmax = tmax

		self.time_vect = []
		self.d_y_evol_type = {}
		self.d_y_evol_pair = {}


	@classmethod
	def from_particles_init(cls, d_init_part, d_init_graph, l_regex_rules, l_type, kconf, kcoll, tmax):
		"""Initialize reactor from init dictionary of particles and interactions"""
		return cls(Graph.from_particles_init(d_init_part, d_init_graph), RuleGenerator(l_regex_rules, l_type).l_rules, kconf, kcoll, tmax)

	def compute_speed( self, rule ):
		if rule.op[0] == '+':
			nb_reac0 = len(self.g.d_state_type[rule.left[0]]) if rule.left[0] in self.g.d_state_type.keys() else 0
			nb_reac1 = len(self.g.d_state_type[rule.left[1]]) if rule.left[1] in self.g.d_state_type.keys() else 0
			return (nb_reac0 + nb_reac1)*self.kcoll if nb_reac0 != 0 and nb_reac1 != 0 else 0

		elif rule.op[0] == '.':
			key_pair = make_key_pair(rule.left[0], rule.left[1]) 
			return len(self.g.d_pair[ key_pair ])*self.kconf if key_pair in self.g.d_pair.keys() else 0

	def apply_reaction(self, rule):
		if rule.op[0] == '+':
			id_part0 = random.choice(self.g.d_state_type[rule.left[0]])
			id_part1 = random.choice(self.g.d_state_type[rule.left[1]])

			if id_part0 == id_part1: return -1
			key, id_pair = make_key_and_id_pair(rule.left[0], rule.left[1], id_part0, id_part1)
			if self.g.pair_already_exist(key, id_pair): return -1
			id_pair = (id_part0, id_part1)

			self.g.link(id_part0, id_part1, rule)

		elif rule.op[0] == '.':
			key = make_key_pair(rule.left[0], rule.left[1])
			try: id_pair = random.choice(self.g.d_pair[ key ])
			except KeyError: return -1
			if rule.op[1] == '+':
				self.g.unlink(id_pair, key, rule)
			if key != rule.left[0]+rule.left[1] : id_pair = id_pair[::-1]


		self.g.modify_state_of_pair(id_pair, rule)

		self.g.recompute_all()
		return id_pair

	def compute_plot_dict(self, d_y_evol, d_part, size ):
		d_length = {key: len(value) for key, value in d_part.items()}

		for part_type in d_y_evol.keys():
			if part_type not in d_length.keys():
				d_length[part_type] = 0

		for part_type in d_length.keys():
			if part_type not in d_y_evol.keys():
				d_y_evol[part_type] = [0]*(size)
			d_y_evol[part_type].append(d_length[part_type])

	def gillespie( self ):
		ECHO = 0
		PLOT = 0
		t = 0
		
		while t < self.tmax:
			ai = [ self.compute_speed(rule) for rule in self.l_rules ]
			sumai = sum(ai)
			if sumai == 0 : break
			t += -math.log(random.random())/sumai
			rand = random.uniform(0, 1)
			n = 0
			mv = 0
			while mv < rand:
				mv += ai[n]/sumai
				n += 1

			id_part = self.apply_reaction(self.l_rules[n-1])
			update_progress("Progression", t, self.tmax, "sec")

			if ECHO and id_part != -1:
				print "############ t = %.3f ###########" % t
				print "# ai = ", ai
				print "# reac = ", self.l_rules[n-1].rule
				print "# id = ", id_part
				print "#", r.g.d_state_type
				print "#", r.g.d_pair
				print "##################################\n\n"

			self.compute_plot_dict( self.d_y_evol_type, self.g.d_state_type, len(self.time_vect) )
			self.compute_plot_dict( self.d_y_evol_pair, self.g.d_pair, len(self.time_vect) )
			self.time_vect.append(t)

		return t
		
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
	sys.stdout.write('\r{2:<20} [{0}] {1:3d}% \t {3:.3f}/{4:.3f} {5}'.format('#'*(progress/int(100./bar_length))+'-'*(bar_length-(progress/int(100./bar_length))), progress, label, nb, nbmax, unit ))
	sys.stdout.flush()


def quit_figure(event):
	if event.key == 'q' or event.key == 'escape':
		plt.close('all')

if __name__ == '__main__':
	start = time.time()

	N = 200
	kcoll = 0.2
	kconf = 0.8
	tmax = 100

	test = 7
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

	r = Reactor.from_particles_init(d_init_part, d_init_grap, l_rules, l_type, kcoll, kconf, tmax) 

	print r.g.d_state_type
	print r.g.d_pair
	t = r.gillespie()
	if t < tmax : print "\n Out before end of time. Cause : no more reaction available"
	# print r.g.d_state_type
	# print r.g.d_pair

	end = time.time()
	print end - start


	PLOT = 1
	SMOOTH = 1

	fig = plt.figure()
	cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

	if PLOT:
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
