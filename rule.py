import re

class Rule():
	"""Transform a formated rule into stochastic matrix"""
	def __init__(self, rule):
		left, right = rule.replace(' ','').split('=')

		if len(left) == 4:
			self.l1, self.l2 = left[0:2], left[2:4]
			self.op1 = '.'
		elif len(left) == 5:
			self.op1 = left[2]
			self.l1, self.l2 =  left.split(self.op1)
		else:
			print "Error : not valid rule"

		if len(right) == 4:
			self.r1, self.r2 = right[0:2], right[2:4]
			self.op2 = '.'
		elif len(right) == 5:
			self.op2 = right[2]
			self.r1, self.r2 =  right.split(self.op2)
		else:
			print "Error : not valid rule"


		self.rule = "%s%s%s=%s%s%s" % (self.l1, self.op1, self.l2, self.r1, self.op2, self.r2)


	def __repr__(self):
		return self.rule

if __name__ == '__main__':
	r = Rule("a0+a1 = a1a2")
	print r		