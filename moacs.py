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


	def run(self):
		for g in xrange(self.total_generations):
			print g
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

class TspMoacs(Moacs):
	def __init__(self, qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations):
		Moacs.__init__(self, qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations)
		for cost_mat in cost_mats:
			self.objectives.append(TSPObjectiveFunction(cost_mat)) #construye matrices de objetivos (distancias)

class QapMoacs(Moacs):
	def __init__(self, qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations, dist_mat):
		Moacs.__init__(self, qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations)
		for cost_mat in cost_mats:
		    self.objectives.append(QAPObjectiveFunction(dist_mat, cost_mat))

def testTsp(n =5, i = 0):
	beta = 1
	rho = 0.1
	qsubzero = 0.9
	tausubzero = 0.0000000000001
	total_ants = 10
	total_generations = 100
	instancias = parse_tsp()
	cost_mats = instancias[i]
	tspMoacs = TspMoacs(qsubzero, tausubzero, beta, rho, cost_mats, total_ants, total_generations)
	pareto_set = ParetoSet(None)
	for i in xrange(n):
		result = tspMoacs.run()
		pareto_set.update(result.solutions)
	pareto_front = ParetoFront(pareto_set)
	pareto_front.draw()
	return pareto_set

def testQap(n = 5, i = 0):
	beta = 1
	rho = 0.1
	qsubzero = 0.9
	tausubzero = 0.0000000000001
	total_ants = 10
	total_generations = 100
	instancias = parse_qap()
	flux_mats = instancias[i][:-1]
	dist_mat = instancias[i][-1]
	qapMoacs = QapMoacs(qsubzero, tausubzero, beta, rho, flux_mats, total_ants, total_generations, dist_mat)
	pareto_set = ParetoSet(None)
	for i in xrange(n):
		result = qapMoacs.run()
		pareto_set.update(result.solutions)
	pareto_front = ParetoFront(pareto_set)
	pareto_front.draw()
	return pareto_set

if __name__ == '__main__':
	testQap()
	testTsp()
