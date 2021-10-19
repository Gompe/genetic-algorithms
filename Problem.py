# -*- coding: utf-8 -*-
"""

Example of a problem that can be solved by Genetic Algorithms: The Knapsack
problem.


"""

import random

#random.seed(0)

bitstringSize = 0
fitness = None

def set_knapsack(Items,maxWeight):
    """
    Sets the fitness function to be the knapsack problem.
    """
    def newFitness(bitstring):
        value = 0
        weight = 0
        for ii, bit in enumerate(bitstring):
            if bit=='0':
                continue
            weight += Items[ii][0]
            if weight > maxWeight:
                return 0
            value += Items[ii][1]
        return value
    global fitness, bitstringSize
    bitstringSize = len(Items)
    fitness = newFitness
    

def randomItems(numElements = 70, Ifprint = True):
    """
    Creates a random instance of the Knapsack problem with numElements
    items.
    """
    totalWeight = 0
    res = []
    for _ in range(numElements):
        w = random.randint(1,20)
        v = random.randint(1,15)
        totalWeight += w
        res.append((w,v))
        
    totalWeight = int( random.random()*totalWeight )
    if Ifprint:
        print("Items: ", res)
        print("Total Weight = ", totalWeight)
    return res, totalWeight

## This line will generate a random instance of the knapsack problem
## and set it for the genetic algorithm to solve.
set_knapsack( *randomItems() )