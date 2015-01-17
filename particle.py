
class Particle():
	"""ID, state and type of a particle"""
	def __init__(self, id, type, state):
		self.id = id
		self.type = type
		self.state = state

	@classmethod
	def from_stype(cls, id, stype):
		"""Initialize particle from stype"""
		return cls(id, stype[0], int(stype[1]))

	def stype(self):
		""" Letter/number formalism """
		return self.type+str(self.state)

	def __repr__(self):
		return "(%d, %s)" % (self.id, self.stype())


if __name__ == '__main__':
	p = Particle(4, 'a', 0)
	print p

	q = Particle.from_stype(1, 'a0')
	print q