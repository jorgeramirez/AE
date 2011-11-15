#!/usr/bin/env python
# -*- coding: utf-8 -*-

from objectivefunction import *

class Solution:
    def __init__(self, solution, objectives):
        """ 
        @param solution: solución representada.
                         
        @param objectives: lista de funciones objetivos a ser evaluadas.
        """
        self.solution = solution
        self.objectives = objectives
        
    def evaluate(self):
        """
        @return: una lista de las evaluaciones de la solución para cada
                 función objetivo
        """
        return [o.evaluate(self) for o in self.objectives]
        
    def dominates(self, other_solution):
        """ 
        @param other_solution: otra solución a comparar.
        """
        #Contexto de minimización
        band = False 
        for obj in self.objectives:
            if obj.evaluate(self) > obj.evaluate(other_solution):
                band = False
                break
            else:
                if obj.evaluate(self) <= obj.evaluate(other_solution):
                    band = True
        return band
    
    def __eq__(self, other):
        """
        operador == para objetos Solution
        @param other: la otra solucion a comparar
        """
        return self.solution == other.solution
    
    def __ne__(self, other):
        """
        operador != para objetos Solution
        @param other: la otra solucion a comparar
        """
        return self.solution != other.solution


class ParetoSet:

    def __init__(self, solutions=None):
        """
        @param solutions: lista de soluciones del frente pareto. Si no
                          se conoce previamente, utilizar solution = none
        """
        self.solutions = solutions
        
    def update(self, candidates):
        """
        @param solutions: lista de soluciones para actualizar el frente
                          pareto
        """
        if not self.solutions:
            self.solutions = [candidates[0]]
            candidates = candidates[1:]
            
        for candidate in candidates:
            band, to_delete = self.domination_check(candidate)
            if not band: #Si el candidato es no dominado con respecto al CP.
                self.solutions = [s for s in self.solutions if s not in to_delete]
                self.solutions.append(candidate)

    def domination_check(self, candidate):
        """
        @param candidate: solución candidata que se analiza
        
        @return: True si el CP domina al candidato, False en caso contrario.
        @return: Lista de elementos del CP a eliminar
        """
        to_delete = []
        for solution in self.solutions:
            if solution.dominates(candidate): #La solución del CP domina al candidato
                return True,[] #El candidato no se agrega al CP.
            else:
                if candidate.dominates(solution): #La solución del CP es dominada por el candidato
                    to_delete.append(solution) #Se agrega la solución a una lista para eliminar
                    
        #Si terminó el for, ninguna solución del CP domina al candidato,
        #por lo que debe añadirse al CP.            
        return False, to_delete #El candidato se agrega al CP y se retorna una
                                #lista de elementos dominados del CP
                                #a eliminar
                
class ParetoFront:
    def __init__(self, pareto_set):
        """
        @param pareto_set: conjunto pareto a partir del cual se construye
                       el frente pareto
        @return: una lista del formato 
                [[f1(x1),f2(x1),....fk(x1)],[f1(x2),f2(x2),....fk(x2)],....,[f1(xn),f2(xn),....fk(xn)]]
        """
        self.pareto_front = [s.evaluate() for s in pareto_set.solutions]
        
    
    
