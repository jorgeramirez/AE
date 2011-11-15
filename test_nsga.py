#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import cparser
from objectivefunction import TSPObjectiveFunction
from ga import GaSolution, TspGeneticOperators
from solution import ParetoSet, ParetoFront
from nsga import NSGA

import numpy as np
import matplotlib.pyplot as plt


tsp_parsed = cparser.parse_tsp()
op = TspGeneticOperators()
objs = [TSPObjectiveFunction(tsp_parsed[0][0]), 
        TSPObjectiveFunction(tsp_parsed[0][1])]
P = []
p, q = 2, 5
n = len(objs[0].mat[0])
for i in xrange(20):
    sol = range(n)
    random.shuffle(sol)
    P.append(GaSolution(sol, objs))
nsga = NSGA(len(objs), op, p, q)
nsga.run(P, 100)
ps = ParetoSet()
ps.update(P)
pf = ParetoFront(ps)

# parte gráfica
fig = plt.figure()

# population 
pop_ax = fig.add_subplot(211)
for p in P:
    p_eval = p.evaluate()
    pop_ax.scatter(p_eval[0], p_eval[1], marker='o', facecolor='blue')

pop_ax.set_title(u"Evaluación de la última Generación")

# pareto front
pf_ax = fig.add_subplot(212)
pf_ax.set_title(u"Frente Pareto")

for p in pf.pareto_front:
    pf_ax.scatter(p[0], p[1], marker='o', facecolor='blue')

plt.show()

