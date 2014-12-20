
class Particle():
	"""ID, state and type of a particle"""
	def __init__(self, id, type, state):
		self.id = id
		self.type = type
		self.state = state

	def stype(self):
		return self.type+str(self.state)

if __name__ == '__main__':
	p = Particle(4, 'a', 0)
	print p.stype()