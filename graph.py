import numpy as np

class Graph():
	"""Interactions between particles"""
	def __init__(self, l_ptcl, m_adj):
		self.l_ptcl = l_ptcl
		self.d_state_type = self.compute_d_state_type()
		self.m_adj = m_adj
		self.d_pair = self.compute_d_pair()

	def compute_d_state_type(self):
		d = {}
		for i in range(len(self.l_ptcl)):
			if self.l_ptcl[i].stype() in d.keys():
				d[self.l_ptcl[i].stype()]. append(i)
			else
				d[self.l_ptcl[i].stype()] = [i]
		return d

	def compute_d_pair(self):
		d = {}
		for i in range(self.m_adj.shape[0]):
			for j in range(self.m_adj.shape[1]):
				typei = self.l_ptcl[i].stype()
				typej = self.l_ptcl[j].stype()
				if typei+typej in d.keys
				if self.m_adj[i][j].stype() in d.keys():
					d[self.l_ptcl[i].stype()+self.l_ptcl[i].stype()]. append(i)
				else
					d[self.l_ptcl[i].stype()] = [i]