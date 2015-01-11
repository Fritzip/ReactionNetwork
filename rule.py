
class Rule():
	"""Transform a formated rule into stochastic matrix"""
	def __init__(self, rule):
		l, r = rule.replace(' ','').split('=')
		self.op = []
		self.left = self.init_op(l)
		self.right = self.init_op(r)

		self.rule = "%s%s%s = %s%s%s" % (self.left[0], self.op[0], self.left[1], self.right[0], self.op[1], self.right[1])


	def __repr__(self):
		return self.rule

	def init_op(self, LorR):
		if len(LorR) == 4:
			self.op.append('.')
			return [LorR[0:2], LorR[2:4]]
		elif len(LorR) == 5:
			self.op.append(LorR[2])
			return LorR.split(LorR[2])
		else:
			print "Error : not valid rule"
			return -1

	def is_state_modified(self, i):
		return self.left[i][1] != self.right[i][1]

	def get_final_state(self, i):
		return self.right[i][1]

if __name__ == '__main__':
	r = Rule("a0+a1 = a1a2")
	print r.get_final_state(1)	