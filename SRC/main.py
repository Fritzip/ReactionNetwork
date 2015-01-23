#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt

from reactor import *
import ubigraph


####################################################################
#			Initialisation
####################################################################

test = 7
if test == 1:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a2a1']
	l_type = ['a']
	
if test == 2:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a1a2']
	l_type = ['a']
	
if test == 3:
	d_init_part = {'a0':N, 'b0':N, 'b1':1}
	d_init_grap = {}	
	l_rules = ['a0+b1=a1b2', 'a1b3=a2b2', 'a0+a1=a2a1', 'b2+b0=b3b2' ]
	l_type = ['a', 'b']

if test == 4:
	d_init_part = {'a0':N, 'a1':1}
	d_init_grap = {}	
	l_rules = ['a0+a1=a0a1','a0a1=a2a3', 'a3a2=a0a1', 'a0a1=a0+a1']
	l_type = ['a']

if test == 5:
	d_init_part = {'a0':N, 'a1':10, 'b0':N, 'b1':10, 'c0':N, 'c1':10}
	d_init_grap = {}	
	l_rules = ['*0+*1=*2*2', '*0+#2=*1#2', '*2#2=*2+#1']
	l_type = ['a', 'b', 'c']

if test == 6:
	d_init_part = {'a0':N, 'a1':10, 'b0':N, 'b1':10, 'c0':N, 'c1':10}
	d_init_grap = {"a0-a1":5, "b0-b1":5, "c0-c1":5}	
	l_rules = ['*0+#1=*0#1', '*0#1=*2+#0']
	l_type = ['a', 'b', 'c']

if test == 7:
	l_type = ['a', 'b', 'c', 'd', 'e', 'f']
	d_init_part = {'a0':N, 'b0':N, 'c0':N, 'd0':N, 'e0':N, 'f0':N}
	d_init_grap = {"e8-a1-b1-c1-d1-f1":1}	
	l_rules = ['e8+e0 = e4e3', '*4#1 = *2#5', '*5+*0 = *7*6', '*3+#6 = *2#3', '*7#3 = *4#3', 'f4f3 = f8+f8', '*2#8 = *9#1', '*9#9 = *8+#8']


####################################################################
#			Launch Gillespie Algorithm
####################################################################
if RUN:
	f = open(PATH,'w')
	start = time.time()

	r = Reactor.from_particles_init(d_init_part, d_init_grap, l_rules, l_type, kcoll, kconf, tmax, f) 

	t = r.gillespie()
	if t < tmax : print "\n%sOut before end of time. Cause : no more reaction available%s" %(KYEL, KNRM)

	end = time.time()
	print "%sExecution time : %.3f sec%s" % (KGRN, end - start, KNRM)

	f.close()


####################################################################
#			Output
####################################################################

if VISU:
	import subprocess
	bashCommand = "./ubigraph_server &"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	time.sleep(1)
	
	import ubigraph
	U = ubigraph.Ubigraph()
	U.clear()

	d_adj = {}
	d_state = {}
	l_vert = []
	d_edges = {}

	d_col = {l_type[i] : COLORS[i] for i in range(len(l_type))}

	f = open(PATH, 'r')
	l_part = f.readline().split()
	for i, stype in enumerate(l_part):
		d_adj[i] = 0
		d_state[i] = int(stype[1])
		col = get_col(d_col[stype[0]], stype[1])
		l_vert.append( U.newVertex( visible = True, shape = "sphere", color = col ) )

	for line in f:
		time.sleep(0.01)
		i, j, k = map(int, line.split())
		if abs(k) == 1:
			d_adj[i] += k
			d_adj[j] += k
			if   k ==  1: d_edges[make_tpl(i,j)] = U.newEdge(l_vert[i], l_vert[j], width = 3, color = '#FFFFFF', strength = 0.3)
			elif k == -1: d_edges[make_tpl(i,j)].destroy()
			if d_adj[i] : l_vert[i].set(visible=True)
			else : l_vert[i].set(visible=False)
			if d_adj[j] : l_vert[j].set(visible=True)
			else : l_vert[j].set(visible=False)
			if d_adj[i] : l_vert[i].set(size=0.7*d_adj[i])
			if d_adj[j] : l_vert[j].set(size=0.7*d_adj[j])

		elif k == 0:
			d_state[i] = j


if PLOT:
	fig = plt.figure()
	cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

	plt1 = fig.add_subplot(1,2,1)
	for key in r.d_y_evol_type.keys():
		x, y = r.time_vect, r.d_y_evol_type[key]
		try: x, y = smoothinterp(x, y) 
		except: pass
		plt.plot(x, y, linewidth=2, label=key)
	plt.legend(loc='best')

	plt2 = fig.add_subplot(1,2,2)
	for key in r.d_y_evol_pair.keys():
		x, y = r.time_vect, r.d_y_evol_pair[key]
		try: x, y = smoothinterp(x, y) 
		except: pass
		plt.plot(x, y, linewidth=2, label=key)
	plt.legend(loc='best')

	plt.show(block=True)
