#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GeneticOperators:
	
	def crossover(self, sol_a, sol_b):
		raise NotImplementedError("crossover method has to be implemented.")
	
	def mutation(self, sol):
		raise NotImplementedError("mutation method has to be implemented.")
	

class TspGeneticOperators(GeneticOperators):
	
	def crossover(self, sol_a, sol_b):
		pass		
	
	def mutation(self, sol):
		pass

class QapGeneticOperators(GeneticOperators):
	
	def crossover(self, sol_a, sol_b):
		pass
	
	def mutation(self, sol):
		pass
