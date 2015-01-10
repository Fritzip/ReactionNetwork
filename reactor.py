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
		if rule.op1 == '+':
			lenl1 = len(self.g.d_state_type[rule.l1]) if rule.l1 in self.g.d_state_type.keys() else 0
			lenl2 = len(self.g.d_state_type[rule.l2]) if rule.l2 in self.g.d_state_type.keys() else 0
			return (lenl1 + lenl2)*self.kcoll if lenl1 != 0 and lenl2 != 0 else 0

		elif rule.op1 == '.':
			return len(self.g.d_pair[rule.l1+rule.l2])*self.kconf if rule.l1+rule.l2 in self.g.d_pair.keys() else 0

	def gillespie(self):
		t = 0
		while t < self.tmax:
			ai = [ self.compute_speed(rule) for rule in self.l_rules ]
			print ai
			sumai = sum(ai)
			if sumai == 0 : break
			t += -math.log(random.random())/sum(ai)
			rand = random.uniform(0, 1)
			n = 0
			mv = 0
			while mv < rand:
				mv += ai[n]/sum(ai)
				n += 1
			# state += stoc[n-1]
			# print t, state.tolist()[0]


if __name__ == '__main__':
	nb_part = 10
	part_type = ['a', 'b', 'c']
	part_state = range(3)
	part = []
	for part_id in xrange(0,nb_part):
		part.append( Particle(part_id, random.choice(part_type), random.choice(part_state) ))
	b = np.random.random_integers(0, 1, size=(nb_part, nb_part))
	mat = (b + b.T)/2
	print mat
	G = Graph(part, mat)
	# print G.d_pair
	r = Reactor(G, ['a1a2=a2+a3', 'b1 +b2= c1. c3', 'a1b3=a2b2', 'b2+b0=b3+b1'], 0.1, 0.2, 120)
	r.gillespie()
	# print r.g.d_pair