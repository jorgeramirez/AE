#!/usr/bin/env python
# -*- coding: utf-8 -*-

import m3as
import sys
from solution import *

def main():
    # Recibe por terminal el nro. de instancia a resolver.
    instance = int(sys.argv[1]) - 1
    print instance
    print type(instance)
    pareto_set_true = ParetoSet(None)
    pareto_set_m3as = m3as.testQap(i = instance)
    pareto_set_true.update(pareto_set_m3as.solutions)
    return 0

if __name__ == '__main__':
    main()

