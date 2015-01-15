import math 
import random
import numpy as np
import time
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

	# def update_y(self, d_y_evol, part_type, nb, size, d_col ):
	# 	if part_type not in d_y_evol.keys():
	# 		d_y_evol[part_type] = [0]*(size)
	# 		# d_col[part_type] = COL
	# 	d_y_evol[part_type].append(nb)

	def compute_plot_dict(self, d_y_evol, d_part, size, d_col, col_count ):
		d_length = {key: len(value) for key, value in d_part.items()}

		for part_type in d_y_evol.keys():
			if part_type not in d_length.keys():
				d_length[part_type] = 0
			if part_type not in d_col.keys():
				d_col[part_type] = col_count
				col_count += 1

		for part_type in d_length.keys():
			if part_type not in d_y_evol.keys():
				d_y_evol[part_type] = [0]*(size)
			d_y_evol[part_type].append(d_length[part_type])

			if part_type not in d_col.keys():
				d_col[part_type] = col_count
				col_count += 1


			# self.update_y(d_y_evol, part_type, d_length[part_type], size, d_col)


	def gillespie( self ):
		ECHO = 0;
		PLOT = 0;
		SMOOTH = 1;
		t = 0
		time_vect = []
		nb_part = len(self.g.l_particles)

		if PLOT:
			plt.ion()
			
			col_count_type = 0
			col_count_pair = 0
			d_col_type = {}
			d_col_pair = {}

			d_y_evol_type = {}
			d_y_evol_pair = {}

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

			pair = self.apply_reaction(self.l_rules[n-1])
			if ECHO and pair != -1:
				print "############ t = %.3f ###########" % t
				print "# ai = ", ai
				print "# reac = ", self.l_rules[n-1].rule
				print "# id = ", pair
				print "#", r.g.d_state_type
				print "#", r.g.d_pair
				print "##################################\n\n"


			if PLOT:
				self.compute_plot_dict( d_y_evol_type, self.g.d_state_type, len(time_vect), d_col_type, col_count_type )
				self.compute_plot_dict( d_y_evol_pair, self.g.d_pair, len(time_vect), d_col_pair, col_count_pair )
				time_vect.append(t)
				plt.figure(1)
				plt.pause(0.00001)
				plt.cla()
				for key in d_y_evol_type.keys():
					plt.plot(time_vect, d_y_evol_type[key], linewidth=2, label=key)
					plt.legend()

				plt.draw()
				plt.xlim([0, t+5])
				plt.ylim(0, plt.ylim()[1])

				plt.figure(2)
				plt.pause(0.00001)
				plt.cla()
				for key in d_y_evol_pair.keys():
					plt.plot(time_vect, d_y_evol_pair[key], linewidth=2, label=key)
					plt.legend()

				plt.draw()

				plt.xlim([0, t+5])
				plt.ylim(0, plt.ylim()[1])

		return t
		
if __name__ == '__main__':
	start = time.time()

	N = 200
	kcoll = 0.2
	kconf = 0.7
	tmax = 100

	test = 4
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
		d_init_part = {'a0':N, 'b0':N, 'b1':1}
		d_init_grap = {}	
		l_rules = ['*0+*1=*2*2']
		l_type = ['a', 'b', 'c']

	if test == 6:
		d_init_part = {'a0':N, 'b0':N, 'b1':1}
		d_init_grap = {}	
		l_rules = ['*0+#1=*0#1']
		l_type = ['a', 'b', 'c']

	r = Reactor.from_particles_init(d_init_part, d_init_grap, l_rules, l_type, kcoll, kconf, tmax) 

	# print r.g.d_state_type
	# print r.g.d_pair
	print r.gillespie()
	# print r.g.d_state_type
	# print r.g.d_pair
	end = time.time()
	print end - start
	plt.show(block=True)
