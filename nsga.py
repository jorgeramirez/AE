#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        for p in population:
            for q in population:
                if p == q:
                    continue
                elif p.dominates(q):
                    S[p].append(q)
                elif q.dominates(p):
                    n[p] += 1
            if n[p] == 0:
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
            fronts[i].append(next_front)
        
        return fronts
    
    def fitness_sharing(self, fronts):
        """
        Realiza el fitness sharing hasta que cada individuo tenga el 
        valor de fitness asignado.
        
        @param fronts: Diccionario de frentes
        """
        pass
        
        
    def niche_count(sol, front):
        """
        Calcula el niche count.
        
        @param sol: solucion del cual se desea calcular su niche count
        @param front: el frente al cual pertenece la solucion
        """
        m = 0.0
        for r in front:
            if r == sol: continue
            sh = 0 #sharing function value
            dist = sol.distance(r)
            if dist < self.sigma_share:
                sh = 1.0 - dist / self.sigma_share
            m += sh
        return m
