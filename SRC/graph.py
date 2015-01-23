#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import random

import ubigraph
from particle import *
from globals import *


###############################################################################
#
#					Graph Class
#
###############################################################################

class Graph():
	"""Interactions between particles"""
	def __init__(self, l_particles, m_adj, f):
		self.l_particles = l_particles
		self.d_state_type = self.compute_d_state_type()
		self.m_adj = m_adj
		self.d_pair = self.compute_d_pair()
		self.f = f

	@classmethod
	def from_particles_init(cls, d_init_part, d_init_graph, f):
		"""Initialize particle from init dictionary of particles"""

		id_part = 0
		l_part = []
		l_connect = []
		d = {}

		# Create particles from init interaction graph
		for interaction in d_init_graph.keys():
			l_init_graph = interaction.replace(' ', '').split('-')
			i = 0
			nb_graph = d_init_graph[interaction]
			while i < nb_graph:
				for j in range(len(l_init_graph) - 1):
					l_connect.append((id_part, id_part+1))
					l_part.append( Particle.from_stype(id_part, l_init_graph[j]) )
					increment_dict(d, l_init_graph[j])
					id_part += 1
				l_part.append( Particle.from_stype(id_part, l_init_graph[-1]) )
				id_part += 1
				increment_dict(d, l_init_graph[-1])
				i += 1 

		# Create particles from init particles dictionary
		for stype in d_init_part.keys():
			try : i = d[stype]
			except KeyError: i = 0

			nb_st_part = d_init_part[stype]
			while i < nb_st_part:
				l_part.append( Particle.from_stype(id_part, stype) )	
				i += 1
				id_part += 1

		# Save simulation
		map(lambda x: f.write('%s ' % x.stype()), l_part )
		f.write('\n')

		# Compute adjacency matrix
		mat = np.zeros((id_part+1, id_part+1))
		for pair in range(len(l_connect)):
			i, j = l_connect[pair] 
			mat[i][j] = 1
			mat[j][i] = 1
			f.write("%s %s %s\n" % (i, j, 1))

		return cls(l_part, mat, f)


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

	def recompute_pair_dict(self):
		""" Reinit all dictionary from adjacency matrix """ 
		self.d_pair = self.compute_d_pair()

	def link(self, id_part0, id_part1, rule):
		""" Link two particles (defined by there id) according to the given rule """
		self.m_adj[id_part0][id_part1] = 1
		self.m_adj[id_part1][id_part0] = 1
		self.f.write("%s %s %s\n" % (id_part0, id_part1, 1))


	def unlink(self, pair, key, rule):
		""" Unink two particles (defined by a pair of id) according to the given rule """
		self.m_adj[pair[0]][pair[1]] = 0
		self.m_adj[pair[1]][pair[0]] = 0
		self.f.write("%s %s %s\n" % (pair[0], pair[1], -1))

	def modify_state_of_pair(self, pair, rule):
		""" Change state of each particle if the rule say so """
		if rule.is_state_modified( 0 ) : self.change_part_state(pair[0], rule.get_final_state(0))
		if rule.is_state_modified( 1 ) : self.change_part_state(pair[1], rule.get_final_state(1))

	def change_part_state(self, id, state):
		""" Modify the state of a given particle (defined by id) """
		rm_from_dict(self.d_state_type, self.l_particles[id].stype(), id )
		self.l_particles[id].state = state
		add_to_dict(self.d_state_type, self.l_particles[id].stype(), id)
		self.f.write("%s %s %s\n" % (id, state, 0))

	def pair_already_exist(self, key, pair):
		""" Check if a pair is in the dictionary of pairs """
		return key in self.d_pair.keys() and pair in self.d_pair[key]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def rm_from_dict(d, key, value):
	d[key].remove(value)
	if d[key] == []:
		del d[key]

def add_to_dict(d, key, value):
	try :
		d[key].append(value)
	except KeyError:
		d[key] = [value]

def increment_dict(d, key):
	try:
		d[key] += 1
	except KeyError:
		d[key] = 1

def make_key_and_id_pair(type1, type2, id1, id2):
	if type1 > type2:
		return type1+type2, (id1, id2) 
	else:
		return type2+type1, (id2, id1)

def make_key_pair(type1, type2):
	return type1+type2 if type1 > type2 else type2 + type1

def make_tpl(int1, int2):
	return (int1, int2) if int1 > int2 else (int2, int1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
