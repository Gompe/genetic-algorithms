# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:17:04 2021

@author: gomes
"""

"""

File for experimentation.

It is possible to use it to plot the progress of the genetic algorithm.

It's also possible to compare with other methods such as random search. 

Comparing the genetic algorithm to the random search method, it's possible to
see a clear superiority of the GA method.

"""

from blobs import *

# For the random search hypothesis
SECONDS = 0.5
    
def test(numSteps=10):
    print("==================================================================")
    print("Start test")
    p = Population()
    print(p)
    for ii in range(numSteps):
        print("Iteration {}".format(ii))
        print(p.bestBlob)
        print("Average Fitness: ", p.averageFitness())
        p.generation()
    print(p)
    print("End Test")
    print("==================================================================")

def plotProgress(numSteps=10, population=None, randomize = False):
    if randomize:
        Problem.set_knapsack( *Problem.randomItems(Ifprint=False) )
    
    p = Population() if population is None else population
    tab_n = np.arange(numSteps)
    avg_n = []
    best_n = []
    for _ in range(numSteps):
        avg_n.append( p.averageFitness() )
        best_n.append( p.bestBlob.fitness )
        p.generation()
            
    plt.plot(tab_n, avg_n, label="Average", color="red")
    plt.plot(tab_n, best_n, label="Best", color="blue")
    plt.title("Population of size {} : {} steps".format(p.size, numSteps))
    plt.show()
    
def plotRandomSearch(numTrials=1000):
    def stopCondition(start):
        global SECONDS
        return default_timer()-start > SECONDS
    
    Problem.set_knapsack( *Problem.randomItems(Ifprint=False) )
    best = None
    ii = 0
    tab_n = []
    best_n = []

    while ii < numTrials:
        randomBitstring = ''
        for _ in range(bitstringSize):
            randomBitstring+= '1' if random.random()<0.1 else '0'
        this_fitness = fitness(randomBitstring)
        best = this_fitness if (best is None or this_fitness>best) else best
        tab_n.append(ii)
        best_n.append(best)
        ii+=1
    print("End Loop")
    plt.plot(tab_n, best_n, color="green")