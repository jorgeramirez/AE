#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spea
import m3as
import moacs
import nsga
import sys
from solution import *
from metric import *


def main():
    # Recibe por terminal el nro. de instancia a resolver.
    instance = int(sys.argv[1]) - 1
    pareto_set_true = ParetoSet(None)
    
    pareto_set_spea = spea.test_qap(i = instance)
    pareto_front_spea = ParetoFront(pareto_set_spea)
    pareto_set_true.update(pareto_set_spea.solutions)
    
    pareto_set_nsga = nsga.test_qap(i = instance)
    pareto_front_nsga = ParetoFront(pareto_set_nsga)
    pareto_set_true.update(pareto_set_nsga.solutions)
    
    pareto_set_m3as = m3as.testQap(i = instance)
    pareto_front_m3as = ParetoFront(pareto_set_m3as)    
    pareto_set_true.update(pareto_set_m3as.solutions)
    
    pareto_set_moacs = moacs.testQap(i = instance)
    pareto_front_moacs = ParetoFront(pareto_set_moacs)    
    pareto_set_true.update(pareto_set_moacs.solutions)
    
    pareto_front_true = ParetoFront(pareto_set_true)
    pareto_front_true.draw()
    
    m1 = DistanceMetric(pareto_front_true)
    m2 = DistributionMetric(1000.0)
    m3 = ExtensionMetric()
    
    print "\nSPEA:"
    print "Distancia: " + str(m1.evaluate(pareto_front_spea))
    print "Distribución:" + str(m2.evaluate(pareto_front_spea))
    print "Extensión:" +  str(m3.evaluate(pareto_front_spea))
    print "\nNSGA:"
    print "Distancia: " + str(m1.evaluate(pareto_front_nsga))
    print "Distribución:" + str(m2.evaluate(pareto_front_nsga))
    print "Extensión:" +  str(m3.evaluate(pareto_front_nsga))
    print "\nM3AS:"
    print "Distancia: " + str(m1.evaluate(pareto_front_m3as))
    print "Distribución:" + str(m2.evaluate(pareto_front_m3as))
    print "Extensión:" +  str(m3.evaluate(pareto_front_m3as))
    print "\nMOACS:"
    print "Distancia: " + str(m1.evaluate(pareto_front_moacs))
    print "Distribución:" + str(m2.evaluate(pareto_front_moacs))
    print "Extensión:" +  str(m3.evaluate(pareto_front_moacs))
    
    return 0

if __name__ == '__main__':
    main()

