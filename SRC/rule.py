#! /usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
#
#					Rule Classs
#
###############################################################################

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


###############################################################################
#
#					Rule Generator Classs
#
###############################################################################

class RuleGenerator():
	""" Given a list of regex rules, create a list of rules """
	def __init__(self, l_regex_rules, l_type):
		self.l_regex_rules = l_regex_rules
		self.l_rules = []

		while self.l_regex_rules:
			idx_star = find(self.l_regex_rules[0], '*')
			idx_sharp = find(self.l_regex_rules[0], '#')
			if idx_star or idx_sharp:
				for part_type_star in l_type:
					for part_type_sharp in l_type:
						current = self.l_regex_rules[0]
						for star in idx_star: 
							current = replace_at_idx( current, part_type_star, star )
						for sharp in idx_sharp:
							current = replace_at_idx( current, part_type_sharp, sharp )
						self.l_rules.append(current)
			else:
				self.l_rules.append(self.l_regex_rules[0])

			self.l_regex_rules.pop(0)

		self.l_rules = list(set(self.l_rules))
		# print self.l_rules


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def replace_at_idx(s, ch, idx):
	return s[:idx] + ch + s[idx+1:]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == '__main__':
	r = Rule("a0+a1 = a1a2")
	print r
	print r.get_final_state(1)	