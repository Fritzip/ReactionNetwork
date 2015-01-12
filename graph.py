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
			add_to_dict(d, self.l_particles[i].stype(), i)
		return d

	def compute_d_pair(self):
		""" Initialize dict of pair """
		d = {}
		n = self.m_adj.shape[0]
		for i in range(n):
			for j in range(i,n):
				if self.m_adj[i][j]:
					key, pair = make_key_and_id_pair(self.l_particles[i].stype(), self.l_particles[j].stype(), i, j)
					add_to_dict( d, key, pair )
		return d

	def recompute_all(self):
		""" Reinit all dictionary from adjacency matrix """ 
		self.d_state_type = self.compute_d_state_type()
		self.d_pair = self.compute_d_pair()

	def link(self, id_part0, id_part1, rule):
		""" Link two particles (defined by there id) according to the given rule """
		self.m_adj[id_part0][id_part1] = 1
		self.m_adj[id_part1][id_part0] = 1
		key, id_pair = make_key_and_id_pair(rule.right[0], rule.right[1], id_part0, id_part1)
		add_to_dict(self.d_pair, key, id_pair)
		if rule.is_state_modified( 0 ) : self.change_part_state(id_part0, rule.get_final_state(0))
		if rule.is_state_modified( 1 ) : self.change_part_state(id_part1, rule.get_final_state(1))

	def change_part_state(self, id, state):
		""" Modify the state of a given particle (defined by id) """
		rm_from_dict(self.d_state_type, self.l_particles[id].stype(), id )
		self.l_particles[id].state = state
		add_to_dict(self.d_state_type, self.l_particles[id].stype(), id)

	def modify_state_of_linked_pair(self, pair, rule):
		rm_from_dict(self.d_pair, make_key_pair(rule.left[0], rule.left[1]), pair)
		if rule.is_state_modified( 0 ) : self.change_part_state(pair[0], rule.get_final_state(0))
		if rule.is_state_modified( 1 ) : self.change_part_state(pair[1], rule.get_final_state(1))
		key, id_pair = make_key_and_id_pair(rule.right[0], rule.right[1], pair[0], pair[1])
		add_to_dict(self.d_pair, key, id_pair)

	def unlink(self, pair, rule):
		""" Unink two particles (defined by a pair of id) according to the given rule """
		self.m_adj[pair[0]][pair[1]] = 0
		self.m_adj[pair[1]][pair[0]] = 0
		rm_from_dict(self.d_pair, make_key_pair(rule.left[0], rule.left[1]), pair)
		if rule.is_state_modified( 0 ) : self.change_part_state(pair[0], rule.get_final_state(0))
		if rule.is_state_modified( 1 ) : self.change_part_state(pair[1], rule.get_final_state(1))

	def pair_already_exist(self, key, pair):
		return 1 if key in self.d_pair.keys() and pair in self.d_pair[key] else 0


def rm_from_dict(d, key, value):
	d[key].remove(value)
	if d[key] == []:
		del d[key]

def add_to_dict(d, key, value):
	if key in d.keys():
		d[key].append(value)
	else:
		d[key] = [value]

def make_key_and_id_pair(type1, type2, id1, id2):
	if type1 > type2:
		return type1+type2, (id1, id2) 
	else:
		return type2+type1, (id2, id1)

def make_key_pair(type1, type2):
	return type1+type2 if type1 > type2 else type2 + type1


if __name__ == '__main__':
	nb_part = 10
	part_type = ['a', 'b', 'c', 'd', 'e', 'f']
	part_state = range(9)
	part = []
	for part_id in xrange(0,nb_part):
		part.append( Particle(part_id, random.choice(part_type), random.choice(part_state) ))

	b = np.random.random_integers(0, 1,size=(nb_part, nb_part))
	mat = (b + b.T)/2
	print mat
	G = Graph(part, mat)