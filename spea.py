#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cparser
from objectivefunction import TSPObjectiveFunction
from ga import GaSolution, TspGeneticOperators
from solution import ParetoSet, ParetoFront
import random
from cluster import Cluster
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


    def reduce_pareto_set(self, Pp):
        c1 = None
        c2 = None
        
        """inicializar clusters """
        lista_cluster=[]
        for solucion in Pp.solutions:
            cluster = Cluster()
            cluster.agregar_solucion(solucion)
            lista_cluster.append(cluster)
            
        while len(lista_cluster) > self.max_pareto_points:  
            """Calcular los dos clusteres mas cercanos""" 
            min_distancia = -1
            for i in range (0,len(lista_cluster)-1):
                for j in range(i+1, len(lista_cluster) -1): 
                    c = lista_cluster[i]
                    distancia = c.calcular_distancia(lista_cluster[j])
                    if min_distancia == -1 or distancia < min_distancia:
                        min_distancia = distancia
                        c1 = i
                        c2 = j

            cont =-1
            for solucion in lista_cluster:
                cont = cont +1
               
            print "unir: "+ str(c1) + " con " + str(c2) + " distancia: "+ str(min_distancia)
            print "\n\n"
            cluster = lista_cluster[c1].unir(lista_cluster[c2]) #retorna un nuevo cluster 

            del lista_cluster[c2]
            del lista_cluster[c1]

            lista_cluster.append(cluster)
        
        Pp=[]
        for cluster in lista_cluster:
            solucion = cluster.centroide()
            Pp.append(solucion)
            
        return Pp 

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
        while len(Q) < pop_size:
            parents = []
            parents.append(random.choice(mating_pool))
            other = random.choice(mating_pool)
            while parents[0] != other:
                other = random.choice(mating_pool)
            parents.append(other)
            if random.random() < self.crossover_rate:
                children = self.genetic_operators.crossover(parents[0], parents[1])
                if random.random() < self.mutation_rate:
                    self.genetic_operators.mutation(random.choice(children))
                Q.extend(children)
        return Q

def main():

    tsp_parsed = cparser.parse_tsp()
    op = TspGeneticOperators()
    objs = [TSPObjectiveFunction(tsp_parsed[0][0]), 
            TSPObjectiveFunction(tsp_parsed[0][1])]
    P = []
    n = len(objs[0].mat[0])
    for i in xrange(20):
        sol = range(n)
        random.shuffle(sol)
        P.append(GaSolution(sol, objs))
    spea = SPEA(len(objs), op, 20)
    spea.run(P, 100)
    ps = ParetoSet()
    ps.update(P)
    pf = ParetoFront(ps)
    print "Pareto Set"
    for s in ps.solutions:
        print s.solution
    print "\n\nPareto Front"
    print pf.pareto_front

if __name__ == '__main__':
	main()

