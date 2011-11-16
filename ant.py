#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import *
from solution import *

class Ant:
	def __init__(self, beta, ant_number, total_ants, ferom_mat, visib_mats, objectives):
		""" 
		@param ferom_mat: matriz de feromonas.
		@param visib_mats: matrices de visibilidad. Una por objetivo.				 
		@param objectives:
		"""
		self.beta = beta
		self.ant_number = ant_number
		self.total_ants = total_ants
		self.ferom_mat = ferom_mat
		self.objectives = objectives
		self.visib_mats = visib_mats
		
	def build_solution(self):
		"""
		Construye una solución al problema planteado.
		"""
		raise NotImplementedError("build_solution method has to be implemented.")

	def probability(self, city_number, feasible_nodes):
		"""
		@param city_number: ciudad actual.

		@feasible_nodes: lista de posibles ciudades a ser visitadas en el siguiente movimiento.
		"""
		lamda = self.ant_number / self.total_ants #lambda es una palabra reservada
		total = 0
		prob_list = list() #cada elemento tiene el numero de ciudad y su probabilidad asociada
		for j in feasible_nodes:
			total = total + self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** \
				(lamda * self.beta) * self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)
			
		for j in feasible_nodes:
			prob = (self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** (lamda * self.beta) \
				* self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)) / total
			prob_list.append([j, prob])

		return prob_list
		
class MOACSAnt(Ant):
	def build_solution(self):
		sol_len = len(self.ferom_mat)
		sol = []
		while(len(sol) < sol_len):
			q = random()
			if q < qsubzero:
				maximum = 0
				for j in feasible_nodes:
					aux = ferom_mat[city_number][j] * visib_mat_1[city_number][j] ** (lamda * beta) * \
						visib_mat_2[city_number][j] ** ((1 - lamda) * beta)
					if (aux > maximum):
						maximum = aux
				sol.append(maximum)
			else:
				probs = self.probability()
				limits = [sum(probs[:i+1][1]) for i in range(len(probs))]
				aux = random()
				for i in xrange(limits):
					if aux <= limits[i]:
						sol.append(probs[i][0])
                        break
		return Solution(sol, self.objectives)


class M3ASAnt(Ant):
    def build_solution(self):
        sol_len = len(self.ferom_mat)
        sol = [randint(0, sol_len - 1)]
        while(len(sol) < sol_len):
            probs = self.probability(sol[-1], [i for i in range(sol_len) if i not in sol])
            aux = [p[1] for p in probs]
            limits = [sum(aux[:i+1]) for i in range(len(aux))]
            aux = random()
            for i in xrange(len(limits)):
                if aux <= limits[i]:
                    sol.append(probs[i][0])
                    break
        return Solution(sol, self.objectives)

