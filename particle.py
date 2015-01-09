
class Particle():
	"""ID, state and type of a particle"""
	def __init__(self, id, type, state):
		self.id = id
		self.type = type
		self.state = state

	def stype(self):
		""" Letter/number formalism """
		return self.type+str(self.state)

	def __repr__(self):
		return "(%d, %s)" % (self.id, self.stype())

if __name__ == '__main__':
	p = Particle(4, 'a', 0)
	print p