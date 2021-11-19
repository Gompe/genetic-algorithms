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

fitness = None
bitstringSize = None

# Hyperparameters
eps = 1e-5 # avoid integer underflow
pCrossover = 0.5
pMutation = 0.01
pRandomOne = 0.5


def set_fitness( new_fitness ):
    
    if not isinstance(new_fitness, type(lambda x:1)):
        raise ValueError("The fitness function must have function type")
    
    global fitness 
    fitness = new_fitness
    
def set_bitstringSize( bitstring_size ):
    
    if (not isinstance(bitstring_size, int)) or (bitstring_size <= 0):
        raise ValueError("The bitstring size must be a positive integer")
        
    global bitstringSize
    bitstringSize = bitstring_size
    
    

class Population:
    
    maxPopulationSize = 1100
    
    def __init__(self, numBlobs=50, fitness_function = None, bitstring_size = None):
        
        self.fitness_function = fitness if fitness_function is None else fitness_function
        self.bitstring_size   = bitstringSize if bitstring_size is None else bitstring_size
        
        self.individuals = []
        
        for _ in range(numBlobs):
            self.individuals.append(Blob.randomBlob(fitness_function, bitstring_size))
            
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
            totalFitness += blob.fitness_value-eps
        return totalFitness/self.size
    
    def findBestBlob(self):
        """
        Updates the bestBlob attribute.
        """
        for blob in self.individuals:
            if self.bestBlob is None or self.bestBlob.fitness_value <= blob.fitness_value:
                self.bestBlob = blob
    
    def fitSelection(self):
        """
        Randomly outputs two blobs based on their fitness.
        """
        totalFitness = sum((blob.fitness_value for blob in self.individuals))
        blobs = [None, None]
        for i in range(2):
            pAux = totalFitness*random.random()
            ii, weight = 0, self.individuals[0].fitness_value
            while weight < pAux:
                ii += 1
                weight += self.individuals[ii].fitness_value
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
    
    def head(self, n=5, simple=True):
        
        n = min(self.size, n)
        
        res = ""
        for i in range(n):
            res += "Individual {}\n".format(i)
            
            if simple:
                
                prefix = str(self.individuals[i])
                prefix = prefix[: min(5, len(prefix))]
                
                res += prefix + '\n'
                
            else:
                res += str(self.individuals[i])
                
        res += "Average fitness: {}\n".format(self.averageFitness())
        return res
    
    def __str__(self):
        return self.head()
            
class Blob:
    
    def __init__(self, bitstring, fitness_function = None):
        
        self.size    = len(bitstring)
        self.genome  = bitstring
        
        self.fitness_function = fitness if fitness_function is None \
                                else fitness_function
                                
        self.fitness_value    = self.fitness_function(bitstring)+eps
    
    def copy(self):
        return Blob(self.genome, self.fitness_function)
    
    def mutate(self):
        """
        Mutates Blob by returning a new mutated version of self.
        """
        # Probability of mutation in any individual bit
        pBitMutation = pMutation/self.size
        res = []
        
        for ii in range(self.size):
            if random.random() < pBitMutation:
                # Mutation changes the bit in position ii
                res.append( '1' if self.genome[ii]=='0' else '0' )
            else:
                res.append(self.genome[ii])
                
        return Blob(''.join(res), self.fitness_function)
    
    @staticmethod
    def crossover(blob1, blob2):
        """ 
        Returns two new Blobs that result from the crossover between blob1 and
        blob2. Notice that blob1 and blob2 remain the same.
        
        Supports blobs with different fitness functions. However, it requires
        that they are of the same size.
        
        """
        
        if blob1.size != blob2.size:
            raise ValueError("Bitstrings should have equal size for crossover")
        
        if random.random() < 0.5:
            blob1, blob2 = blob2, blob1 
        
        crossingPoint = random.randint(0, blob1.size-2)
        genome1, genome2 = blob1.genome, blob2.genome
        
        newblob1 = Blob(genome1[:crossingPoint+1]+genome2[crossingPoint+1:],
                        blob1.fitness_function)
        
        newblob2 = Blob(genome2[:crossingPoint+1]+genome1[crossingPoint+1:],
                        blob2.fitness_function)
        
        return newblob1,newblob2
    
    @staticmethod
    def combine(blob1, blob2):
        """
        Returns the two descendants produced by blob1 and blob2.        

        """
        if random.random() < pCrossover:
            blob1,blob2 = Blob.crossover(blob1,blob2)
            
        else:
            blob1,blob2 = blob1.copy(), blob2.copy()
            
        blob1 = blob1.mutate()
        blob2 = blob2.mutate()
        
        return blob1, blob2
    
    @staticmethod
    def randomBlob(fitness_function = None, bitstring_size = None):
        """
        Creates a random Blob.
        """
        
        bitstring_size = bitstringSize if bitstring_size is None \
                         else bitstring_size
        
        randomBitstring = ''
        
        for _ in range( bitstring_size ):
            randomBitstring+= '1' if random.random()<pRandomOne else '0'
            
        return Blob(randomBitstring, fitness_function)
    
    def __str__(self):
        return "{} :\n{}\n".format(self.genome, self.fitness_value-eps)
    

        
    