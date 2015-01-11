import numpy as np
import random

from particle import *

class Graph():
	"""Interactions between particles"""
	def __init__(self, l_particles, m_adj):
		self.l_particles = l_particles
		self.d_state_type = self.compute_d_state_type()
		self.m_adj = m_adj
		self.d_pair = self.compute_d_pair()

	def compute_d_state_type(self):
		""" Initialize dict of state/type """
		d = {}
		for i in range(len(self.l_particles)):
			if self.l_particles[i].stype() in d.keys():
				d[self.l_particles[i].stype()]. append(i)
			else:
				d[self.l_particles[i].stype()] = [i]
		return d

	def compute_d_pair(self):
		""" Initialize dict of pair """
		d = {}
		n = self.m_adj.shape[0]
		for i in range(n):
			for j in range(i,n):
				if self.m_adj[i][j]:
					add_to_dict( d, make_key_pair(self.l_particles[i].stype(), self.l_particles[j].stype()), (i,j) )
		return d

	def recompute_all(self):
		self.d_state_type = self.compute_d_state_type()
		self.d_pair = self.compute_d_pair()

	def link(self, id_part1, id_part2, rule):
		self.m_adj[id_part1][id_part2] = 1
		self.m_adj[id_part2][id_part1] = 1
		add_to_dict(self.d_pair, make_key_pair(rule.right[0],rule.right[1]), make_tpl(id_part1, id_part2))
		if rule.is_state_modified( 0 ) : self.change_part_state(id_part1, rule.get_final_state(0))
		if rule.is_state_modified( 1 ) : self.change_part_state(id_part2, rule.get_final_state(1))

	def change_part_state(self, id, state):
		self.d_state_type[self.l_particles[id].stype()].remove(id)
		self.l_particles[id].state = state
		add_to_dict(self.d_state_type, self.l_particles[id].stype(), id)



def add_to_dict(d, key, value):
	if key in d.keys():
		d[key].append(value)
	else:
		d[key] = [value]

def make_tpl(i, j):
	return (i,j) if i < j else (j, i)

def make_key_pair(type1, type2):
	return type1+type2 if type1 > type2 else type2 + type1


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