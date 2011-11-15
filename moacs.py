#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cparser import *
from moaco import *
from ant import *

class Moacs(Moaco):
	def __init__(self, qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations):
		Moaco.__init__(self, beta, rho, cost_mats, total_ants, total_generations)
		self.qsubzero = qsubzero
		self.tausubzero = tausubzero
		self.ferom_mat = []
		n = len(cost_mats[0])
		for i in xrange(n):
			self.ferom_mat.append([tausubzero for j in range(n)]) #inicializar feromonas
		self.objectives = []
		self.max_values = []
		for cost_mat in cost_mats:
			self.objectives.append(TSPObjectiveFunction(cost_mat)) #construye matrices de objetivos (distancias)


	def run(self):
		for g in xrange(self.total_generations):
			for ant_number in xrange(self.total_ants):
				ant = MOACSAnt(self.beta, ant_number, self.total_ants, self.ferom_mat, self.visib_mats, \
					self.objectives, self.tausubzero, self.qsubzero, self.rho)
				solution = ant.build_solution()
				self.pareto_set.update([solution])
				product = 1
				
				for objective_number in xrange(len(ant.average_obj)):
					product = product * ant.average_obj[objective_number]
				tausubzerop = 1 / len(self.ferom_mat) * product #len ferom_mat es la cant de nodos

				if(tausubzerop > self.tausubzero):
					self.tausubzero = tausubzerop
					reinitialize_ferom_mat()
				else:
					self.global_updating(product)

		return self.pareto_set


	def global_updating(self, product):
		for solution in self.pareto_set.solutions: #solution es una lista que tiene cada nodo de la solucion como elemento
			for i in xrange(len(solution.solution)-1):
				s = solution.solution[i]
				d = solution.solution[i+1]
				self.ferom_mat[s][d] = (1 - self.rho) * self.ferom_mat[s][d] + self.rho / product


	def reinitialize_ferom_mat(self):
		n = len(ferom_mat)
		for i in xrange(n):
			self.ferom_mat.append([self.tausebzero for j in range(n)])

def main():
	beta = 1
	rho = 0.1
	qsubzero = 0.9
	tausubzero = 1 #REVISAR
	total_ants = 10
	total_generations = 100
	instancias = parse_tsp()
	cost_mats = instancias[0]
	tspMoacs = Moacs(qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations)
	result = tspMoacs.run()
	pareto_front = ParetoFront(result)
	pareto_front.draw()
	return 0

if __name__ == '__main__':
	main()

