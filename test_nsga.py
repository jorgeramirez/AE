#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nsga

import random, sys

def test_tsp():
    '''
    tsp_parsed = cparser.parse_tsp()
    op = TspGeneticOperators()
    objs = [TSPObjectiveFunction(tsp_parsed[0][0]), 
            TSPObjectiveFunction(tsp_parsed[0][1])]
    P = []
    p, q = 2, 5
    n = len(objs[0].mat[0])
    pop_size = 10
    sigma = 10000
    for i in xrange(pop_size):
        sol = range(n)
        random.shuffle(sol)
        P.append(GaSolution(sol, objs))
    nsga = NSGA(len(objs), op, p, q, sigma, mr=0.2)
    nsga.run(P, 100)
    ps = ParetoSet()
    ps.update(P)
    pf = ParetoFront(ps)
    draw(P, pf)
    '''
    nsga.test_tsp()
    

    
def draw(population, pareto_front):
    """
    Dibuja la población y el frente pareto.
    """
    # parte gráfica
    fig = plt.figure()

    # population 
    pop_ax = fig.add_subplot(211)
    for p in population:
        p_eval = p.evaluate()
        pop_ax.scatter(p_eval[0], p_eval[1], marker='o', facecolor='blue')

    pop_ax.set_title(u"Evaluación de la última Generación")

    # pareto front
    pf_ax = fig.add_subplot(212)
    pf_ax.set_title(u"Frente Pareto")

    for p in pareto_front.pareto_front:
        pf_ax.scatter(p[0], p[1], marker='o', facecolor='blue')

    plt.show()

    
def test_qap():
    '''
    qap_parsed = cparser.parse_qap()
    op = QapGeneticOperators()  # [ [ [obj 1], [ obj 2], [dist] ],[ [obj 1] , [obj 2] , [dist] ] ]
    objs = [QAPObjectiveFunction(qap_parsed[0][2], qap_parsed[0][0]), 
            QAPObjectiveFunction(qap_parsed[0][2], qap_parsed[0][1])]
    P = []
    p, q = 2, 5
    n = len(objs[0].dist_mat[0])
    for i in xrange(10):
        sol = range(n)
        random.shuffle(sol)
        P.append(GaSolution(sol, objs))
    
    nsga = NSGA(len(objs), op, 15000 ,p, q)
    nsga.run(P, 5)
    ps = ParetoSet()
    ps.update(P)
    pf = ParetoFront(ps)
    draw(P, pf)
    '''
    nsga.test_qap()

def usage():
    print "Usage: python test_nsga.py [tsp | qap]"
    sys.exit(1)

if __name__ == "__main__":
    d = {"tsp": test_tsp, "qap": test_qap}
    if len(sys.argv) == 1 or not d.has_key(sys.argv[1].lower()):
        usage()
    d[sys.argv[1].lower()]()
