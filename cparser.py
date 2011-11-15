#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

bp = "instancias" + os.sep

tsp_instances = [bp + "KROAB100.TSP.TXT", bp + "kroac100.tsp.txt"]
qap_instances = [bp + "qapUni.75.0.1.qap.txt", bp + "qapUni.75.p75.1.qap.txt"]


def parse_tsp():
				  # [   instancia uno     ] [  instancia dos    ]
	mat_objs = [] # [ [ [obj 1], [ obj 2] ],[ [obj 1] , [obj 2] ] ]
	for s, ins in enumerate(tsp_instances):
		f = open(ins, "r")
		n = int(f.readline()) # nro ciudades
		k = int(f.readline()) # nro objetivos
		mat_objs.append([])
		for i in xrange(k):
			mat_objs[s].append([])
			for j in xrange(n):
				mat_objs[s][i].append([float(e) for e in f.readline().split()])
			f.readline()
		f.close()
	return mat_objs


def parse_qap():
				  # [        instancia uno        ] [        instancia dos 	     ]
	mat_objs = [] # [ [ [obj 1], [ obj 2], [dist] ],[ [obj 1] , [obj 2] , [dist] ] ]
	for s, ins in enumerate(qap_instances):
		f = open(ins, "r")
		n = int(f.readline()) # nro localidades
		mat_objs.append([])
		for i in xrange(3):
			mat_objs[s].append([])
			for j in xrange(n):
				mat_objs[s][i].append([int(e) for e in f.readline().split()])
			f.readline()
		f.close()
	return mat_objs

	
if __name__ == "__main__":
	print len(parse_tsp())
	print len(parse_qap())