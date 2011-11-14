#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from solution import Solution

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
        
        return Solution(child, sol_a.objectives)
    
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
        Crossover de las soluciones dadas como parametros.
        Elige tres posiciones al azar y luego genera el primer hijo
        en base a sol_a, pero con los elementos de sol_b en las posiciones
        sorteadas. De manera análoga para el segundo hijo.
        Luego se retorna el mejor de los dos hijos.
        
        @param sol_a: Primera solucion
        @param sol_b: Segunda solucion
        """     
        pos, child_1, child_2 = [], [], []
        n = len(sol_a.solution) - 1
        child_1.extend(sol_a.solution)
        child_2.extend(sol_b.solution)
        for i in xrange(3):
            while True:
                j = random.randint(0, n)
                if j not in pos:
                    break
            pos.append(j)
        for p in pos:
            child_1[p], child_2[p] = child_2[p], child_1[p]
        child_1 = Solution(child_1, sol_a.objectives)
        child_2 = Solution(child_2, sol_a.objectives)
        if child_1.dominates(child_2):
            return child_1
        else:
            return child_2
        
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
    from solution import Solution
    s1 = Solution(range(1,9), [])
    s2 = Solution([8,5,2,1,3,6,4,7], [])
    op = TspGeneticOperators()
    print op.crossover(s1, s2).solution
    print "antes: " + str(s1.solution)
    op.mutation(s1)
    print "despues:" + str(s1.solution)
    
    op = QapGeneticOperators()
    print op.crossover(s1, s2).solution
    print "antes: " + str(s1.solution)
    op.mutation(s1)
    print "despues:" + str(s1.solution)
