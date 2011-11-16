#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ObjectiveFunction:
    def evaluate(self, solution):
        """ 
        @param solution: solución que se evaluaré con respecto a la
                         función objetivo.
        """
        raise NotImplementedError("evaluate method has to be implemented.")
    

class TSPObjectiveFunction(ObjectiveFunction):
    def __init__(self, mat):
        """ 
        @param mat: matriz de adyacencia de distancias parseada.
        """
        self.mat = mat
        
    def evaluate(self, solution):
        """ 
        @param solution: solución TSP con formato:
                         [0,1,5,...,n]. siendo n la última ciudad
                         visitada.
        """ 
        path = solution.solution
        path_cost = 0
        for i in xrange(len(path)-1):
            s = path[i]
            d = path[i+1]
            path_cost = path_cost + self.mat[s][d]
        return path_cost

    def cost_i_to_j(self, i, j):
        return self.mat[i][j]

class QAPObjectiveFunction(ObjectiveFunction):
    def __init__(self, dist_mat, flux_mat):
        """ 
        @param dist_mat: matriz de adyacencias de distancias parseada.
        @para flux_mat: matriz de adyacencias de flujos parseada.
        """
        self.dist_mat = dist_mat
        self.flux_mat = flux_mat
        
    def evaluate(self, solution):
        """ 
        @param solution: solución QAP con formato:
                         [2,3,5,...,n]. Se lee el edificio 2 se ubica en
                         la localidad 0.
                         .
        """ 
        path = solution.solution
        path_cost = 0
        for i in xrange(len(path)):
            for j in xrange(i, len(path)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[path[i]][path[j]]
                    path_cost = path_cost + distance * flux
        return path_cost

    def cost_i_to_j(self, k, l):
        path = [k, l]
        path_cost = 0
        for i in xrange(len(path)):
            for j in xrange(i, len(path)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[path[i]][path[j]]
                    path_cost = path_cost + distance * flux
        return path_cost

