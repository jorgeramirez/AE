#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import *

class Moaco():
	
	def __init__(self, beta, cost_mats, total_ants):
		self.beta = beta
		self.total_ants = total_ants
		self.visib_mats = []
		self.pareto_set = []
		for cost_mat in xrange(len(cost_mats)):
			visib_mat = []
			for row in xrange(len(cost_mat)):
				visib_mat.append([1.0/e for e in row])
			self.visib_mats.append(visib_mat)
		
	def run():
		raise NotImplementedError("evaluate method has to be implemented.")

	
	
	
