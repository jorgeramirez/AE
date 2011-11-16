#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cparser import parse_qap, parse_tsp
from objectivefunction import TSPObjectiveFunction, QAPObjectiveFunction
from ga import GaSolution, GeneticOperators
from solution import ParetoSet, ParetoFront

import numpy as np
import matplotlib.pyplot as plt

import random, math

class NSGA:
    def __init__(self, num_objectives, genetic_operators, p, q, 
                 cr=1.0, mr=0.1):
        """
        @param num_objectives: numero de objetivos
        @param genetic_operators: objeto que representa a los operadores 
                                  genéticos
        @param p: número de variables.
        @param q: número de soluciones óptimas diferentes deseadas.
        @param cr: crossover rate
        @param mr: mutation rate
        """
        self.num_objectives = num_objectives
        self.genetic_operators = genetic_operators
        self.crossover_rate = cr
        self.mutation_rate = mr
        
        #calculamos sigma_share de acuerdo a Deb 1999
        self.sigma_share = 0.5 / math.pow(float(q), 1.0/float(p))
    
    def run(self, P, num_generations):
        """
        Ejecuta el algoritmo NSGA
        
        @param P: la poblacion inicial
        @param num_generations: el numero maximo de generaciones
        """
        for i in xrange(num_generations):
            fronts = self.classify_population(P)
            self.fitness_sharing(fronts)
            del P[:]
            #juntamos los frentes para formar P
            for front in fronts.values():
                P.extend(front)
            mating_pool = self.selection(P)
            P = self.next_generation(mating_pool, len(P))

    def classify_population(self, population):
        """
        Clasifica la población en regiones no dominadas.
        En una primera pasada se calcula el primer frente. Luego, para calcular
        los demas frentes se basa en la idea de que los elementos en el nuevo
        frente solo son dominados por elementos que se encuentran en el frente
        anterior.
        
        @param population: la población a clasificar.
        """
        fronts = {}
        n = {} # {p => k} k individuos dominan a p
        S = {} # {p => [s1, ... , sn]} p domina a s1 ... sn
        for p in population:
            S[p] = []
            n[p] = 0
        
        fronts[1] = [] #primer frente
        pop_size = len(population)
        for p in population:
            for q in population:
                if p == q:
                    continue
                elif p.dominates(q):
                    S[p].append(q)
                elif q.dominates(p):
                    n[p] += 1
            if n[p] == 0:
                p.fitness = float(pop_size)
                fronts[1].append(p)
        
        #calcular los demas frentes
        i = 1
        while(len(fronts[i]) != 0):
            next_front = []
            for r in fronts[i]:
                for s in S[r]:
                    n[s] -= 1
                    if n[s] == 0:
                        next_front.append(s)
            i += 1
            fronts[i] = next_front
        return fronts
    
    def fitness_sharing(self, fronts):
        """
        Realiza el fitness sharing hasta que cada individuo tenga el 
        valor de fitness asignado.
        
        @param fronts: Diccionario de frentes
        """
        for i, front in fronts.items():
            min_dummy_fitness = 0.0
            if i > 1: # para las siguientes poblaciones se asigna el dummy 
                      # fitness como un valor un poco 
                      # menor al valor mínimo del frente anterior
                min_dummy_fitness = min([s.fitness for s in fronts[i-1]])
                min_dummy_fitness = min_dummy_fitness * 0.8
            for sol in front:
                if i > 1:
                    sol.fitness = min_dummy_fitness
                m = self.niche_count(sol, front)
                if m > 0:
                    sol.fitness = sol.fitness / m
        
    def niche_count(self, sol, front):
        """
        Calcula el niche count.
        
        @param sol: solucion del cual se desea calcular su niche count
        @param front: el frente al cual pertenece la solucion
        """
        m = 0.0
        import sys
        uppers = [0 for _ in xrange(len(sol.objectives))]
        lowers = [sys.maxint for _ in xrange(len(sol.objectives))]
        for solution in front:
            for i, v in enumerate(solution.evaluation):
                if v > uppers[i]:
                    uppers[i] = v
                if v < lowers[i]:
                    lowers[i] = v
        for r in front:
            if r == sol: continue
            sh = 0.0 #sharing function value
            dist = sol.distance(r, uppers, lowers)
            if dist <= self.sigma_share:
                sh = 1.0 - dist / self.sigma_share
            m += sh
        return m + 1
    
    def selection(self, population):
        """
        Realiza la selección y retorna el mating_pool
        """
        pool = []
        pool_size = len(population)
        probs = self.probabilities(population)
        limits = [sum(probs[:i+1]) for i in xrange(len(probs))]
        while len(pool) < pool_size:
            aux = random.random()
            for i in xrange(len(limits)):
                if aux <= limits[i]:
                    pool.append(population[i])
                    break
        return pool
    
    def probabilities(self, population):
        """
        Utiliza el fitness de cada solucion para retornar una lista de 
        probabilidades de seleccionar dicho elemento
        """
        probs = []
        total_fitness = 0.0
        for p in population:
            total_fitness += p.fitness
        for p in population:
            probs.append(p.fitness / total_fitness)
        return probs
    
    def next_generation(self, mating_pool, pop_size):
        """
        Crea la siguiente generacion a partir del mating_pool y los operadores 
        genéticos
        
        @param mating_pool: mating pool utilizada para construir la siguiente 
                            generación de individuos
        """
        Q = []
        
        #cruzamiento
        while len(Q) < pop_size:
            parents = []
            parents.append(random.choice(mating_pool))
            other = random.choice(mating_pool)
            parents.append(other)
            if random.random() < self.crossover_rate:
                children = self.genetic_operators.crossover(parents[0], parents[1])
                Q.extend(children)
            else:
                Q.extend(parents)
        
        for ind in Q:
            if random.random() < self.mutation_rate:
                self.genetic_operators.mutation(ind)
                ind.evaluation = ind.evaluate()
        return Q


def test_tsp(n = 5, i = 0):
    total_ind = 10
    total_generations = 100
    p, q = 2, 5
    op = GeneticOperators()
    instancias = parse_tsp()
    cost_mats = instancias[i]
    objs = []
    for cost_mat in cost_mats:
        objs.append(TSPObjectiveFunction(cost_mat))
    num_cities = len(objs[0].mat)
    nsga = NSGA(len(objs), op, p, q, mr=0.2)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        pop = []
        for i in xrange(total_ind):
            sol = range(num_cities)
            random.shuffle(sol)
            pop.append(GaSolution(sol, objs))        
        nsga.run(pop, total_generations)
        pareto_set.update(pop)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()


def test_qap(n = 5, i = 0):
    total_ind = 20
    total_generations = 100
    p, q = 2, 5
    op = GeneticOperators()
    instancias = parse_qap()
    flux_mats = instancias[i][:-1]
    dist_mat = instancias[i][-1]
    num_loc = len(flux_mats[0]) #nro de localidades
    objs = []
    for cost_mat in flux_mats:
        objs.append(QAPObjectiveFunction(dist_mat, cost_mat))
    nsga = NSGA(len(objs), op, p, q, mr=0.2)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        pop = []
        for i in xrange(total_ind):
            sol = range(num_loc)
            random.shuffle(sol)
            pop.append(GaSolution(sol, objs))
        nsga.run(pop, total_generations)
        pareto_set.update(pop)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()