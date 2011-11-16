#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cparser import parse_qap, parse_tsp
from objectivefunction import TSPObjectiveFunction, QAPObjectiveFunction
from ga import GaSolution, GeneticOperators
from solution import ParetoSet, ParetoFront
import random
from cluster import Cluster
import sys
class SPEA:
    def __init__(self, num_objectives, genetic_operators, max_pareto_points, cr=1.0, mr=0.1):
        pareto_set = ParetoSet(None)
        self.num_objectives = num_objectives
        self.genetic_operators = genetic_operators
        self.crossover_rate = cr
        self.mutation_rate = mr
        self.max_pareto_points = max_pareto_points

    def run(self, P, num_generations):
        """
        Ejecuta el algoritmo SPEA
        
        @param P: la poblacion inicial
        @param num_generations: el numero maximo de generaciones
        """
        ps = ParetoSet()
        for i in xrange(num_generations):
            ps.update(P)
            for s in ps.solutions:
                if s in P:
                    P.remove(s)

            if len(ps.solutions) > self.max_pareto_points:
                self.reduce_pareto_set(ps)
            self.fitness_assignment(ps, P)
            mating_pool = self.selection(P, ps)
            P = self.next_generation(mating_pool, len(P))

    def fitness_assignment(self, pareto_set, population):
        for pareto_ind in pareto_set.solutions:
            count = 0
            for population_ind in population:
                if pareto_ind.dominates(population_ind):
                    count = count + 1
            strength = count / (len(population) + 1)
            if strength != 0:
                pareto_ind.fitness = 1 / strength

        for population_ind in population:
            suma = 0.0
            for pareto_ind in pareto_set.solutions:
                if pareto_ind.dominates(population_ind):
                    suma = suma + 1.0/pareto_ind.fitness
            suma = suma + 1.0
            pareto_ind.fitness = 1 / suma


    def reduce_pareto_set(self, par_set):
        """
        Realiza el clustering
        """
        lista_cluster=[]
        for solucion in par_set.solutions:
            cluster = Cluster()
            cluster.agregar_solucion(solucion)
            lista_cluster.append(cluster)
  
        while len(lista_cluster) > self.max_pareto_points:
            print len(lista_cluster)
            min_distancia = sys.maxint
            for i in range (0,len(lista_cluster)-1):
                for j in range(i+1, len(lista_cluster)-1): 
                    c = lista_cluster[i]
                    distancia = c.calcular_distancia(lista_cluster[j])
                    #if min_distancia == -1 or distancia < min_distancia:
                    if distancia < min_distancia:
                        min_distancia = distancia
                        c1 = i
                        c2 = j
               
            cluster = lista_cluster[c1].unir(lista_cluster[c2]) #retorna un nuevo cluster 
            del lista_cluster[c1]
            del lista_cluster[c2]

            lista_cluster.append(cluster)
        
        par_set=[]
        for cluster in lista_cluster:
            solucion = cluster.centroide()
            par_set.append(solucion)
            
        return par_set 

    def selection(self, population, pareto_set):
        """
        Realiza la selección y retorna el mating_pool
        """
        pool = []
        unido = []
        unido.extend(population)
        unido.extend(pareto_set.solutions)
        pool_size = len(unido) / 2
        while len(pool) < pool_size:
            c1 = random.choice(unido)
            c2 = random.choice(unido)
            while c1 == c2:
                c2 = random.choice(unido)
            if c1.fitness > c2.fitness:
                pool.append(c1)
            else:
                pool.append(c2)
        return pool

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
    max_pareto_size = 20
    op = GeneticOperators()
    instancias = parse_tsp()
    cost_mats = instancias[i]
    objs = []
    for cost_mat in cost_mats:
        objs.append(TSPObjectiveFunction(cost_mat))
    num_cities = len(objs[0].mat)
    spea = SPEA(len(objs), op, max_pareto_size)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        pop = []
        for i in xrange(total_ind):
            sol = range(num_cities)
            random.shuffle(sol)
            pop.append(GaSolution(sol, objs))        
        spea.run(pop, 100)
        pareto_set.update(pop)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()
    return pareto_set


def test_qap(n = 5, i = 0):
    total_ind = 10
    total_generations = 100
    max_pareto_size = 20
    op = GeneticOperators()
    instancias = parse_qap()
    flux_mats = instancias[i][:-1]
    dist_mat = instancias[i][-1]
    num_loc = len(flux_mats[0]) #nro de localidades
    objs = []
    for cost_mat in flux_mats:
        objs.append(QAPObjectiveFunction(dist_mat, cost_mat))
    spea = SPEA(len(objs), op, max_pareto_size)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        pop = []
        for i in xrange(total_ind):
            sol = range(num_loc)
            random.shuffle(sol)
            pop.append(GaSolution(sol, objs))
        spea.run(pop, total_generations)
        pareto_set.update(pop)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()
    return pareto_set
