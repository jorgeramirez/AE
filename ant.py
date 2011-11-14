#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import *
from solution import *

class Ant:
	def __init__(self, ferom_mat, visib_mats, objectives):
		""" 
		@param ferom_mat: matriz de feromonas.
		@param visib_mats: matrices de visibilidad. Una por objetivo.				 
		@param objectives:
		"""
		self.ferom_mat = ferom_mat
		self.objectives = objectives
		self.visib_mats = visib_mats
		
	def build_solution():
		"""
		Construye una solución al problema planteado.
		"""
		raise NotImplementedError("build_solution method has to be implemented.")
		

class M3ASAnt(Ant):
	def build_solution():
		sol_len = len(self.ferom_mat)
		sol = []
		while(len(sol < sol_len):
			probs = self.probability(sol)
			limits = [sum(probs[:i+1][1]) for i in range(len(probs))]
			aux = random()
			for i in xrange(limits):
				if aux <= limits[i]:
				sol.append(probs[i][0])
		return Solution(sol, self.objectives)
		
