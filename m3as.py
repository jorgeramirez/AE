#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cparser import *
from moaco import *

class M3as(Moaco):
	def __init__(self, taumax, taumin, beta, rho, cost_mats, total_ants, total_generations):
		super(TspM3AS, self).__init__(beta, rho,  cost_mats, total_ants, total_generations)
		self.taumax = taumax
		self.taumin = taumin
		self.ferom_mat = []
		n = len(cost_mats[0])
		self.ferom_mat = []
		for i in xrange(n):
			ferom_mat[i] = [taumax for j in range(len(n))]
		self.objectives = []
		self.max_values = []
		for cost_mat in cost_mats:
			max_val = 0
			for i in xrange(n):
				if max(cost_mat[i]) > max_val:
					max_val = max(cost_mat[i])
			self.max_values.append(max_val)
			self.objectives.append(TSPObjectiveFunction(cost_mat))
		
	def run():
		for g in xrange(len(self.total_generations)):
			for ant_number in xrange(len(self.total_ants)):
				ant = M3ASAnt(self.beta, ant_number, self.total_ants, self.ferom_mat, self.visib_mats, self.objectives)
				solution = ant.build_solution()
				self.pareto_set.update([solution])
			self.evaporate_feromones()
			self.update_feromones()
		return self.pareto_front
				
	def evaporate_feromones():
		n = len(self.ferom_mat)
		for i in xrange(n):
			for j in xrange(n):
				self.ferom_mat[i][j] = self.ferom_mat[i][j] * (1.0 - self.rho)
				if self.ferom_mat[i][j] < self.taumin:
					self.ferom_mat[i][j] =  self.taumin
					
	def update_feromones():
		for solution in self.pareto_set.solutions:
			evaluation = solution.evaluate()
			divisor = sum([evaluation[i]/max_values[i] for i in len(evaluation)])
			deltaTau = 1.0/divisor
			self.taumax = deltaTau/(1.0 - self.rho)
			self.taumin = taumax/(2 * self.total_ants)
			for i in xrange(len(solution)-1):
				s = solution[i]
				d = solution[i+1]
				self.ferom_mat[s][d] = self.ferom_mat[s][d] + deltaTau
				if self.ferom_mat[s][d] > self.taumax:
					self.ferom_mat[s][d] = self.taumax
			
				
def main():
	taumax = 0.0023
	taumin = 0.000071
	beta = 1
	rho = 0.02
	total_ants = 100
	total_generations = 100
	cost_mats = parse_tsp()
	tspM3as = M3as(taumax, taumin, beta, rho, cost_mats, total_ants, total_generations)
	print tspM3as.run()
	return 0

if __name__ == '__main__':
	main()

