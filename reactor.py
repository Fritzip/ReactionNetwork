import math 
import random
import numpy as np

from rule import *
from graph import *

class Reactor():
	"""Init and run Gillespie algorithm"""
	def __init__(self, graph, l_rules, kconf, kcoll):
		self.l_rules = [Rule(elem) for elem in l_rules]
		self.kconf = kconf
		self.kcoll = kcoll
		self.m_stoc = self.compute_stochastic_matrix()
		self.graph = graph

	def compute_stochastic_matrix(self):
		""" Compute the stochastic matrix from the list of rules """
		l_stype = set()
		
		for rule in self.l_rules:
			[ l_stype.add(x) for x in [rule.l1, rule.l2, rule.r1, rule.r2] ]
		
		l_stype = list(l_stype)

		size = len(l_stype)
		m = np.zeros(shape = (size, size))

		for rule in self.l_rules:
			i = l_stype.index(rule.l1)
			j = l_stype.index(rule.l2)
			if rule.op1 == '+':
				m[i][j] = self.kcoll
				m[j][i] = self.kcoll
			elif rule.op1 == '.':
				m[i][j] = self.kconf
				m[j][i] = self.kconf
				
		return m

	def gillespie(self):
		# while t < tmax and min(state.tolist()[0]) > 0:
		# 	ai = [(nA+nB)*rC, nC*rC, nC*rP]
		# 	t += -math.log(random.random())/sum(ai)
		# 	rand = random.uniform(0, 1)
		# 	n = 0
		# 	mv = 0
		# 	while mv < rand:
		# 		mv += ai[n]/sum(ai)
		# 		n += 1
			
		# 	state += stoc[n-1]
		# 	print t, state.tolist()[0]
		pass


if __name__ == '__main__':
	nb_part = 10
	part_type = ['a', 'b', 'c', 'd', 'e', 'f']
	part_state = range(9)
	part = []
	for part_id in xrange(0,nb_part):
		part.append( Particle(part_id, random.choice(part_type), random.choice(part_state) ))

	# print part
	b = np.random.random_integers(0, 1,size=(nb_part, nb_part))
	mat = (b + b.T)/2
	print mat
	G = Graph(part, mat)
	r = Reactor(G, ['a1a2=a2+a3', 'b1 +b2= c1. c3', 'a1b3=a2b2', 'b2+b0=b3+b1'], 0.1, 0.2)
	print r.m_stoc