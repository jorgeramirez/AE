#!/usr/bin/env python
# -*- coding: utf-8 -*-

import m3as
import moacs
import nsga
import sys
from solution import *

def main():
    # Recibe por terminal el nro. de instancia a resolver.
    instance = int(sys.argv[1]) - 1
    pareto_set_true = ParetoSet(None)
    pareto_set_nsga = nsga.test_tsp(i = instance)
    pareto_set_true.update(pareto_set_nsga.solutions)
    pareto_set_m3as = m3as.testTsp(i = instance)
    pareto_set_true.update(pareto_set_m3as.solutions)
    pareto_set_moacs = moacs.testTsp(i = instance)
    pareto_set_true.update(pareto_set_moacs.solutions)
    return 0

if __name__ == '__main__':
    main()
