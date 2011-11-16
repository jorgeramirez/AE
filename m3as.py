#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cparser import *
from moaco import *
from ant import *
from copy import *

class M3as(Moaco):
    def __init__(self, taumax, taumin, beta, rho, cost_mats, total_ants, total_generations):
        Moaco.__init__(self, beta, rho, cost_mats, total_ants, total_generations)
        self.taumax = taumax
        self.taumin = taumin
        self.ferom_mat = []
        n = len(cost_mats[0])
        self.ferom_mat = []
        for i in xrange(n):
            self.ferom_mat.append([taumax for j in range(n)])
        self.objectives = []
        self.max_values = []
        
		
    def run(self):
        for g in xrange(self.total_generations):
            for ant_number in xrange(self.total_ants):
                ant = M3ASAnt(self.beta, ant_number, self.total_ants, self.ferom_mat, self.visib_mats, self.objectives)
                solution = ant.build_solution()
                self.pareto_set.update([solution])
            self.evaporate_feromones()
            self.update_feromones()
            print g
        return self.pareto_set
				
    def evaporate_feromones(self):
        n = len(self.ferom_mat)
        for i in xrange(n):
            for j in xrange(n):
                self.ferom_mat[i][j] = self.ferom_mat[i][j] * (1.0 - self.rho)
                if self.ferom_mat[i][j] < self.taumin:
                    self.ferom_mat[i][j] =  self.taumin
					
    def update_feromones(self):
        for solution in self.pareto_set.solutions:
            evaluation = solution.evaluate()
            divisor = sum([evaluation[i]/self.max_values[i] for i in range(len(evaluation))])
            deltaTau = 1.0/divisor
            self.taumax = deltaTau/(1.0 - self.rho)
            self.taumin = self.taumax/(2 * self.total_ants)
            for i in xrange(len(solution.solution)-1):
                s = solution.solution[i]
                d = solution.solution[i+1]
                self.ferom_mat[s][d] = self.ferom_mat[s][d] + deltaTau
                if self.ferom_mat[s][d] > self.taumax:
                    self.ferom_mat[s][d] = self.taumax
                    
class TspM3as(M3as):
    def __init__(self, taumax, taumin, beta, rho, cost_mats, total_ants, total_generations):
        M3as.__init__(self, taumax, taumin, beta, rho, cost_mats, total_ants, total_generations)
        n = len(cost_mats[0])
        flux_mats = cost_mats #en esta variable se reciben las matrices de flujo
        for cost_mat in cost_mats:
            max_val = 0
            for i in xrange(n):
                if max(cost_mat[i]) > max_val:
                    max_val = max(cost_mat[i])
            self.max_values.append(max_val)
            self.objectives.append(TSPObjectiveFunction(cost_mat))
            
class QapM3as(M3as):
    def __init__(self, taumax, taumin, beta, rho, cost_mats, dist_mat, total_ants, total_generations):
        M3as.__init__(self, taumax, taumin, beta, rho, cost_mats, total_ants, total_generations)
        #flux_mats == cost_mats: en esta variable se recibe las matrices de flujo
        n = len(cost_mats[0])
        max_dist = 0 
        for dist_row in dist_mat:
            if max(dist_row) > max_dist:
                max_dist = max(dist_row)      
        for cost_mat in cost_mats:
            max_val = 0
            for i in xrange(n):
                if max(cost_mat[i]) > max_val:
                    max_val = max(cost_mat[i])
            self.max_values.append(max_val*max_dist)
            self.objectives.append(QAPObjectiveFunction(dist_mat, cost_mat))
            
        

        
			
				
def testTsp(n = 5, i = 0):
    taumax = 0.0023
    taumin = 0.0000071
    beta = 1
    rho = 0.02
    total_ants = 10
    total_generations = 100
    instancias = parse_tsp()
    cost_mats = instancias[i]
    tspM3as = TspM3as(taumax, taumin, beta, rho, cost_mats, total_ants, total_generations)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        result = tspM3as.run()
        pareto_set.update(result.solutions)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()
    """print "\n\nFrente Pareto"
    for p in pareto_front.pareto_front:
        print p
        print ""
    print "\n\nConjunto Pareto"    
    for r in result.solutions:
        print r.solution
        print ""
        print ""
    """
    return pareto_set

def testQap(n = 5, i = 0):
    taumax = 0.0000053
    taumin = 0.000000053
    beta = 1
    rho = 0.02
    total_ants = 10
    total_generations = 100
    instancias = parse_qap()
    flux_mats = instancias[i][:-1]
    dist_mat = instancias[i][-1]
    
    qapM3as = QapM3as(taumax, taumin, beta, rho, flux_mats, dist_mat, total_ants, total_generations)
    pareto_set = ParetoSet(None)
    for i in xrange(n):
        result = qapM3as.run()
        pareto_set.update(result.solutions)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()
    """print "\n\nFrente Pareto"
    for p in pareto_front.pareto_front:
        print p
        print ""
    print "\n\nConjunto Pareto"    
    for r in result.solutions:
        print r.solution
        print ""
        print ""
    """
    return pareto_set


if __name__ == '__main__':
    testQap()
    testTsp()
