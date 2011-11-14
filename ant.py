#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Ant:
	def __init__(self, ferom_mat, pareto_set, objectives):
		""" 
		@param ferom_mat: matriz de feromonas.
						 
		@param pareto_set: conjunto pareto de soluciones.
		"""
		self.ferom_mat = ferom_mat
		self.pareto_set = pareto_set
		self.objectives = objectives
		
	def build_solution():
		"""
		Construye una solución al problema planteado.
		"""
		raise NotImplementedError("build_solution method has to be implemented.")

	def probability(ant_number, total_ants, city_number, ferom_mat, visib_mat_1, visib_mat_2, feasible_nodes, beta):
		"""
		@param city_number: ciudad actual.

		@param ferom_mat: matriz de feromonas.

		@param visib_mat_1: matriz de visibilidades para el objetivo 1.

		@param visib_mat_2: matriz de visibilidades para el objetivo 2.

		@feasible_nodes: lista de posibles ciudades a ser visitadas en el siguiente movimiento.

		@param beta: ponderacion relativa entre los objetivos
		"""
		lamda = ant_number / total_ants #lambda es una palabra reservada
		total = 0
		prob_list = list() #cada elemento tiene el numero de ciudad y su probabilidad asociada
		for j in feasible_nodes:
			total = total + ferom_mat[city_number][j] * visib_mat_1[city_number][j] ** (lamda * beta) * visib_mat_2[city_number][j] ** ((1 - lamda) * beta)

		for j in feasible_nodes:
			prob = (ferom_mat[city_number][j] * visib_mat_1[city_number][j] ** (lamda * beta) * visib_mat_2[city_number][j] ** ((1 - lamda) * beta)) / 					total
			prob_list.append([j, prob])

		return prob_list
		
		

class M3ASTSPAnt(Ant):
	sol = []
	visited = []
	def build_solution():
