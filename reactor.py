import math 
import random
import numpy as np
import time
import sys

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
	def from_particles_init(cls, d_init_part, d_init_graph, l_regex_rules, l_type, kconf, kcoll, tmax, f):
		"""Initialize reactor from init dictionary of particles and interactions"""
		return cls(Graph.from_particles_init(d_init_part, d_init_graph, f), RuleGenerator(l_regex_rules, l_type).l_rules, kconf, kcoll, tmax)

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
			update_progress("Progression", t, self.tmax, "time.unit.")

			if ECHO and id_part != -1:
				print "############ t = %.3f ###########" % t
				print "# ai = ", ai
				print "# reac = ", self.l_rules[n-1].rule
				print "# id = ", id_part
				print "#", r.g.d_state_type
				print "#", r.g.d_pair
				print "##################################\n\n"

			if PLOT:
				self.compute_plot_dict( self.d_y_evol_type, self.g.d_state_type, len(self.time_vect) )
				self.compute_plot_dict( self.d_y_evol_pair, self.g.d_pair, len(self.time_vect) )
				self.time_vect.append(t)

		return t

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_progress(label, nb, nbmax, unit="", bar_length=25 ): # small 20, medium 25, large 50
	progress = int(nb*100/nbmax)
	if progress > 100 : progress = 100
	sys.stdout.write('\r{2:<20} [{0}] {1:3d}% \t {3:.2f}/{4:.2f} {5}'.format('#'*(progress/int(100./bar_length))+'-'*(bar_length-(progress/int(100./bar_length))), progress, label, nb, nbmax, unit ))
	sys.stdout.flush()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	