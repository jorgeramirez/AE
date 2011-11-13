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
		

class M3ASTSPAnt(Ant):
	sol = []
	visited = []
	def build_solution():
		
		

