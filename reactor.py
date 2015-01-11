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
			nb_reac1 = len(self.g.d_state_type[rule.left[0]]) if rule.left[0] in self.g.d_state_type.keys() else 0
			nb_reac2 = len(self.g.d_state_type[rule.left[1]]) if rule.left[1] in self.g.d_state_type.keys() else 0
			return (nb_reac1 + nb_reac2)*self.kcoll if nb_reac1 != 0 and nb_reac2 != 0 else 0

		elif rule.op[0] == '.':
			return len(self.g.d_pair[rule.left[0]+rule.left[1]])*self.kconf if rule.left[0]+rule.left[1] in self.g.d_pair.keys() else 0

	def apply_reaction(self, rule):
		if rule.op[0] == '+':
			id_part1 = random.choice(self.g.d_state_type[rule.left[0]])
			id_part2 = random.choice(self.g.d_state_type[rule.left[1]])
			if id_part1 == id_part2: 
				print "Youps id picked are the same : %d" %(id_part1)
				return -1
			try:
				if make_tpl(id_part1, id_part2) in self.g.d_pair[make_key_pair(rule.left[0], rule.left[1])] : 
					return -1
			except KeyError: pass

			self.g.link(id_part1, id_part2, rule)

		elif rule.op[0] == '.':
			if rule.op[1] == '+':
				pass
			elif rule.op[1] == '.':
				pass

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
			self.apply_reaction(self.l_rules[n-1])
			# state += stoc[n-1]
			# print t, state.tolist()[0]
		return t


if __name__ == '__main__':
	start = time.time()
	nb_part = 100
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

	r = Reactor(G, ['a0+a1=a1a0'], 0.1, 0.2, 10) #, 'b1 +b2= c1. c3', 'a1b3=a2b2', 'b2+b0=b3+b1'
	print r.g.d_state_type
	print r.g.d_pair
	print r.gillespie()
	print r.g.d_state_type
	print r.g.d_pair
	end = time.time()
	print end - start
