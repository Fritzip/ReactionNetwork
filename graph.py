import numpy as np
import random

from particle import *

class Graph():
	"""Interactions between particles"""
	def __init__(self, l_ptcl, m_adj):
		self.l_ptcl = l_ptcl
		self.d_state_type = self.compute_d_state_type()
		self.m_adj = m_adj
		self.d_pair = self.compute_d_pair()

	def compute_d_state_type(self):
		""" """
		d = {}
		for i in range(len(self.l_ptcl)):
			if self.l_ptcl[i].stype() in d.keys():
				d[self.l_ptcl[i].stype()]. append(i)
			else:
				d[self.l_ptcl[i].stype()] = [i]
		return d

	def compute_d_pair(self):
		""" Initialize dict of pair"""
		d = {}
		n, m = self.m_adj.shape
		for i in range(n):
			for j in range(i,m):
				typei = self.l_ptcl[i].stype()
				typej = self.l_ptcl[j].stype()
				typeij = typei+typej if typei > typej else typej + typei
				if typeij in d.keys():
					d[typeij].append((i,j))
				else:
					d[typeij] = [(i,j)]


if __name__ == '__main__':
	nb_part = 40
	part_type = ['a', 'b', 'c', 'd']
	part_state = range(4)
	part = []
	for part_id in xrange(0,nb_part):
		part.append( Particle(part_id, random.choice(part_type), random.choice(part_state) ))

	# print part
	b = np.random.random_integers(0, 1,size=(nb_part, nb_part))
	mat = (b + b.T)/2
	# print mat
	G = Graph(part, mat)