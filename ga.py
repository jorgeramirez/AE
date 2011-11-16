#!/usr/bin/env python
# -*- coding: utf-8 -*-

from solution import Solution

import numpy as np
#from scipy.spatial.distance import pdist

import random, sys, math

class GaSolution(Solution, object):
    def __init__(self, solution, objectives):
        Solution.__init__(self, solution, objectives)
        self.fitness = float(sys.maxint)
        self.evaluation = self.evaluate()
    
    def distance(self, other, u, l):
        """
        Calcula la distancia Euclidiana entre dos individuos
        
        @param other: el otro individuo
        """
        me_objs = self.evaluation
        other_objs = other.evaluation
        dist = 0.0
        i = 0
        for v1, v2 in zip(me_objs, other_objs):
            if u[i] != l[i]:
                dist += math.pow(v1-v2, 2) / math.pow(u[i]-l[i], 2.0)
            i += 1
        return math.sqrt(dist)

    def solutions_distance(self, other):
        """
        Calcula la distancia Euclidiana entre dos individuos
        
        @param other: el otro individuo
        """
        me_objs = self.evaluate()
        other_objs = other.evaluate()
        dist = 0.0
        for v1, v2 in zip(me_objs, other_objs):
            dist += math.pow(v1-v2, 2)
        return math.sqrt(dist)
    
    def __cmp__(self, other):
        """
        Retorna negativo si x<y, cero si x==y, positivo si x>y
        """
        return self.fitness - other.fitness

    def dominates(self, other):
        """ 
        @param other: otra solución a comparar.
        """
        if other.__class__.__name__ == "Solution":
            return Solution.dominates(self, other)
        #Contexto de minimización
        band = False 
        for i, obj_eval in enumerate(self.evaluation):
            if obj_eval > other.evaluation[i]:
                band = False
                break
            else:
                if obj_eval <= other.evaluation[i]:
                    band = True
        return band


class GeneticOperators:

    def crossover(self, sol_a, sol_b):
        """
        Crossover de las soluciones dadas como parametros.
        Se toma el primer elemento de sol_a y se copia en el hijo. Luego se 
        consulta el valor del primer elemento de sol_b y se averigua su 
        posicion en sol_a, luego se copia el elemento de sol_a en el hijo
        manteniendo la posicion, asi hasta querer insertar un elemento ya
        presente en el hijo.
        
        Luego se copian los elementos restantes de sol_b en el hijo.
        
        @param sol_a: Primera solucion
        @param sol_b: Segunda solucion
        @return: lista de hijos
        """    
        child = [-1 for n in xrange(len(sol_a.solution))]
        k = 0
        
        #fijar elementos de la primera solucion
        while True:
            child[k] = sol_a.solution[k]
            k = sol_a.solution.index(sol_b.solution[k])
            if child[k] >= 0:
                break
        
        #fijar elementos de la segunda solucion
        for i, s in enumerate(sol_b.solution):
            if child[i] < 0:
                child[i] = s
        
        return [GaSolution(child, sol_a.objectives)]
    
    def mutation(self, sol):
        """
        Realiza la operación de mutación sobre la solución.
        Elige dos posiciones aleatorias y realiza un intercambio de elementos
        
        @param sol: la solución a mutar
        """
        n = len(sol.solution) - 1
        i = random.randint(0, n)
        j = random.randint(0, n)
        while i == j:
            import time
            random.seed(time.time())
            j = random.randint(0, n)
        sol.solution[i], sol.solution[j] = sol.solution[j], sol.solution[i]
