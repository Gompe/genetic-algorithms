# -*- coding: utf-8 -*-
"""

General Purpose Genetic Algorithm.

class Blob corresponds to a specific individual.

class Population corresponds to several blobs (individuals).

Fitness function and bitstring size are problem-dependent and
are imported from an external "Problem.py" file containing 
nothing more than a fitness function.

"""

from timeit import default_timer
import random
import numpy as np
import matplotlib.pyplot as plt

# Fitness function
import Problem

fitness = Problem.fitness
bitstringSize = Problem.bitstringSize

# Hyperparameters
eps = 1e-5 # avoid integer underflow
pCrossover = 0.5
pMutation = 0.01
pRandomOne = 0.1 

class Population:
    
    maxPopulationSize = 1100
    
    def __init__(self, numBlobs=50):
        self.individuals = []
        for _ in range(numBlobs):
            self.individuals.append(Blob.randomBlob())
        self.bestBlob = None
        self.findBestBlob()
    
    @property
    def size(self):
        return len(self.individuals)
    
    def diversity(self):
        table = set()
        for blob in self.individuals:
            table.add(blob.genome)
        return len(table)
    
    def averageFitness(self):
        totalFitness = 0
        for blob in self.individuals:
            totalFitness += blob.fitness-eps
        return totalFitness/self.size
    
    def findBestBlob(self):
        """
        Updates the bestBlob attribute.
        """
        for blob in self.individuals:
            if self.bestBlob is None or self.bestBlob.fitness <= blob.fitness:
                self.bestBlob = blob
    
    def fitSelection(self):
        """
        Randomly outputs two blobs based on their fitness.
        """
        totalFitness = sum((blob.fitness for blob in self.individuals))
        blobs = [None, None]
        for i in range(2):
            pAux = totalFitness*random.random()
            ii, weight = 0, self.individuals[0].fitness
            while weight < pAux:
                ii += 1
                weight += self.individuals[ii].fitness
            blobs[i] = self.individuals[ii]
        return blobs

    def generation(self):
        """
        Moves to the next generation.
        """
        newindividuals = []
        while len(newindividuals) < min(Population.maxPopulationSize-2, self.size-1):
            blob1, blob2 = self.fitSelection()
            blob1, blob2 = Blob.combine(blob1, blob2)
            newindividuals.append(blob1)
            newindividuals.append(blob2)
            
        self.individuals = newindividuals
        # Now we do a check to keep the best blob
        previousBest = self.bestBlob
        self.findBestBlob()
        if self.bestBlob is previousBest:
            self.individuals.append(self.bestBlob)
    
    def __str__(self):
        res = ""
        for i in range(5):
            res += "Individual {}\n".format(i)
            res += str(self.individuals[i])
        res += "Average fitness: {}\n".format(self.averageFitness())
        return res
            
class Blob:
    
    size = bitstringSize
    def __init__(self, bitstring):
        assert len(bitstring) == Blob.size
        self.genome = bitstring
        self.fitness = fitness(bitstring)+eps
    
    def copy(self):
        return Blob(self.genome)
    
    def mutate(self):
        """
        Mutates Blob by returning a new mutated version of self.
        """
        # Probability of mutation in any individual bit
        pBitMutation = pMutation/Blob.size
        res = []
        for ii in range(len(self.genome)):
            if random.random() < pBitMutation:
                # Mutation changes the bit in position ii
                res.append( '1' if self.genome[ii]=='0' else '0' )
            else:
                res.append(self.genome[ii])
        return Blob(''.join(res))
    
    @staticmethod
    def crossover(blob1, blob2):
        """ 
        Returns two new Blobs that result from the crossover between blob1 and
        blob2. Notice that blob1 and blob2 remain the same.
        """
        crossingPoint = random.randint(0,Blob.size-2)
        genome1, genome2 = blob1.genome, blob2.genome
        newblob1 = Blob(genome1[:crossingPoint+1]+genome2[crossingPoint+1:])
        newblob2 = Blob(genome2[:crossingPoint+1]+genome1[crossingPoint+1:])
        return newblob1,newblob2
    
    @staticmethod
    def combine(blob1, blob2):
        if random.random() < pCrossover:
            blob1,blob2 = Blob.crossover(blob1,blob2)
        else:
            blob1,blob2 = blob1.copy(), blob2.copy()
        blob1 = blob1.mutate()
        blob2 = blob2.mutate()
        return blob1, blob2
    
    @staticmethod
    def randomBlob():
        randomBitstring = ''
        for _ in range(Blob.size):
            randomBitstring+= '1' if random.random()<pRandomOne else '0'
        return Blob(randomBitstring)
    
    def __str__(self):
        return "{} :\n{}\n".format(self.genome, self.fitness-eps)
    

        
    