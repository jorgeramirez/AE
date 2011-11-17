#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class Metric():
    def evaluate(self, pareto_front):
        raise NotImplementedError("evaluate method has to be implemented.")

    def distance(self, a, b):
        """
        Calcula la distancia Euclidiana entre a y b
                """
        dist = 0.0
        for v1, v2 in zip(a, b):
            dist += math.pow(v1-v2, 2)
        return math.sqrt(dist)
        
        
class DistanceMetric(Metric):
    def __init__(self, y_true):
        self.y_true = y_true
        
    def evaluate(self, pareto_front):
        suma = 0
        for p in pareto_front.pareto_front:
            dist = []
            for y  in self.y_true.pareto_front:
                dist.append(self.distance(p,y))
            suma = suma + min(dist)
        return suma/len(pareto_front.pareto_front)
                

        
class DistributionMetric(Metric):
    def __init__(self, sigma):
        self.sigma = sigma
        
    def evaluate(self, pareto_front):
        suma = 0
        for p1 in pareto_front.pareto_front:
            for p2 in pareto_front.pareto_front:
                if p1 != p2 and self.distance(p1, p2) > self.sigma:
                    suma = suma + 1
        if len(pareto_front.pareto_front) - 1 > 0:             
            result = suma/(len(pareto_front.pareto_front) - 1)
        else:
            result = suma
        return result
    
class ExtensionMetric(Metric):
    def evaluate(self, pareto_front):
        dist_x = []
        dist_y = []
        n = len(pareto_front.pareto_front)
        pareto = pareto_front.pareto_front
        for i in range(n - 1):
            for j in range(i + 1, n):
                dist_x.append(math.pow((pareto[i][0] - pareto[j][0]), 2))
                dist_y.append(math.pow((pareto[i][1] - pareto[j][1]), 2))
            
        return math.sqrt(max(dist_x) + max(dist_y))
