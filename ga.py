#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, sys, math
from solution import Solution

class GaSolution(Solution, object):
    def __init__(self, solution, objectives):
        Solution.__init__(self, solution, objectives)
        self.fitness = float(sys.maxint)
    
    def distance(self, other):
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


class GeneticOperators:
    
    def crossover(self, sol_a, sol_b):
        raise NotImplementedError("crossover method has to be implemented.")
    
    def mutation(self, sol):
        raise NotImplementedError("mutation method has to be implemented.")
    

class TspGeneticOperators(GeneticOperators):

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
        while True:
            j = random.randint(0, n)
            if j != i: 
                break
        sol.solution[i], sol.solution[j] = sol.solution[j], sol.solution[i]
        

class QapGeneticOperators(GeneticOperators):

    def crossover(self, sol_a, sol_b):
        """
        Partially-Mapped Crossover o PMX Crossover
        
        @param sol_a: Primera solucion
        @param sol_b: Segunda solucion
        @return: lista de hijos
        """     
        if sol_a == sol_b:
            return []
        n = len(sol_a.solution) - 1
        beg = random.randint(0, n)
        end = beg
        while end <= beg:
            end = random.randint(0, n)
        child1, child2 = [], []
        child1.extend(sol_a.solution)
        child2.extend(sol_b.solution)
        for i in xrange(beg, end+1):
            gen1 = sol_a.solution[i]
            gen2 = sol_b.solution[i]
            if gen1 != gen2:
                # buscar ambos genes en child1 y hacer swap
                pg1 = child1.index(gen1)
                pg2 = child1.index(gen2)
                child1[pg1], child1[pg2] = child1[pg2], child1[pg1]
                
                # buscar ambos genes en child2 y hacer swap
                pg1 = child2.index(gen1)
                pg2 = child2.index(gen2)
                child2[pg1], child2[pg2] = child2[pg2], child2[pg1]                
        child1 = GaSolution(child1, sol_a.objectives)
        child2 = GaSolution(child2, sol_a.objectives)
        return [child1, child2]
        
    def mutation(self, sol):
        """
        Realiza la operación de mutación sobre la solución.
        Elige dos posiciones aleatorias y realiza un intercambio de elementos
        
        @param sol: la solución a mutar
        """
        n = len(sol.solution) - 1
        i = random.randint(0, n)
        while True:
            j = random.randint(0, n)
            if j != i: 
                break
        sol.solution[i], sol.solution[j] = sol.solution[j], sol.solution[i]


if __name__ == "__main__":
    s1 = GaSolution(range(1,9), [])
    s2 = GaSolution([8,5,2,1,3,6,4,7], [])
    print "s1: " + str(s1.solution)
    print "s2: " + str(s2.solution)
    op = TspGeneticOperators()
    print "Crossover"
    print "hijo: " + str(op.crossover(s1, s2)[0].solution)
    print "Mutation"
    print "antes: " + str(s1.solution)
    op.mutation(s1)
    print "despues:" + str(s1.solution)
    
    op = QapGeneticOperators()
    print "Crossover"
    print "hijo 1: " + str(op.crossover(s1, s2)[0].solution)
    print "hijo 2: " + str(op.crossover(s1, s2)[1].solution)
    print "Mutation"
    print "antes: " + str(s1.solution)
    op.mutation(s1)
    print "despues:" + str(s1.solution)
