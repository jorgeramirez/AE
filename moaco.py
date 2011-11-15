#!/usr/bin/env python
# -*- coding: utf-8 -*-

from solution import *

class Moaco():
	
	def __init__(self, beta, rho, cost_mats, total_ants, total_generations):
		self.beta = beta
		self.rho = rho
		self.total_ants = total_ants
		self.total_generations = total_generations
		self.visib_mats = []
		self.pareto_set = ParetoSet(None)
		for cost_mat in xrange(len(cost_mats)):
			visib_mat = []
			for row in xrange(len(cost_mat)):
				visib_mat.append([1.0/e for e in row])
			self.visib_mats.append(visib_mat)
		
	def run():
		raise NotImplementedError("run method has to be implemented.")

	
	
	
