import math 
import random
import numpy as np
import time

from rule import *
from graph import *


class Reactor():
	"""Init and run Gillespie algorithm"""
	def __init__(self, graph, l_rules, kconf, kcoll, tmax):
		self.g = graph
		self.l_rules = [Rule(elem) for elem in l_rules]
		self.kconf = kconf
		self.kcoll = kcoll
		self.tmax = tmax

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

			self.g.link(id_part0, id_part1, rule)
			return id_pair

		elif rule.op[0] == '.':
			try: pair = random.choice(self.g.d_pair[make_key_pair(rule.left[0], rule.left[1])])
			except KeyError: return -1
			if rule.op[1] == '+':
				self.g.unlink(pair, rule)
			elif rule.op[1] == '.':
				self.g.modify_state_of_linked_pair(pair, rule)
			return pair
				
	def gillespie( self ):
		t = 0
		while t < self.tmax:
			print "############ t = %.3f ###########" % t
			ai = [ self.compute_speed(rule) for rule in self.l_rules ]
			print "# ai = ", ai
			sumai = sum(ai)
			if sumai == 0 : break
			t += -math.log(random.random())/sumai
			rand = random.uniform(0, 1)
			n = 0
			mv = 0
			while mv < rand:
				mv += ai[n]/sumai
				n += 1
			print "# reac = ", self.l_rules[n-1].rule
			print "# id = ", self.apply_reaction(self.l_rules[n-1])
			print "#", r.g.d_state_type
			print "#", r.g.d_pair
			print "##################################\n\n"

		return t


if __name__ == '__main__':
	start = time.time()
	nb_part = 10
	part_type = ['a', 'b', 'c']
	part_state = range(2)
	part = []
	for part_id in xrange(0,nb_part):
		part.append( Particle(part_id, 'a', random.choice(part_state) )) #random.choice(part_type)
	# b = np.random.random_integers(0, 1, size=(nb_part, nb_part))
	mat = np.zeros((nb_part, nb_part))
	# mat = (b + b.T)/2
	# print mat
	G = Graph(part, mat)

	r = Reactor(G, ['a0+a1=a2a3','a2a3=a4a5', 'a4a5=a1+a0'], 0.5, 0.2, 2) #, 'b1 +b2= c1. c3', 'a1b3=a2b2', 'b2+b0=b3+b1'
	print r.g.d_state_type
	print r.g.d_pair
	print r.gillespie()
	print r.g.d_state_type
	print r.g.d_pair
	end = time.time()
	print end - start
