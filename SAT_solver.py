# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 20:45:59 2021

@author: gomes
"""

import blobs as gs
import random

bitstringSize = 0
fitness = None 


class SolverSAT:
    
    def __init__(self, clauses):
        """

        clauses should be a list of lists.
        
        If the problem is (x1 or x2) and (x3 or not x1), clauses should be 
        [[1, 2], [3, -1]].
        
        """
        
        # self.hash_map = self.give_variables_names(clauses)
        
        self.num_real_variables = self.count_distinct_variables(clauses)
        self.num_variables = self.num_real_variables
        
        self.formula = self.clean_clauses(clauses)
        
        self.assignment = [False] * (self.num_variables + 1)
        
        
        ## We define the GA algorithm population
        # bitstring[x] = assignment of variable x+1
        
        self.population = \
            gs.Population(numBlobs=30,
                          fitness_function = lambda b : SolverSAT.fitness_SAT(self, b),
                          bitstring_size = self.num_variables
                          )
        
    
    ## Auxiliar methods for __init__
    
    def count_distinct_variables(self, clauses):
        
        """ 
        Counts the number of distinct variables in clauses.
        
        """
        
        st = set()
        
        for clause in clauses:
            for x in clause:
                x = abs(x)
                st.add(x)
                
        return len(st)
        
    
    ## Methods for reducing to 3-SAT
        
    def clause_to_3SAT(self, clause):    
        """
        Breaks a clause into a number of 3SATs.
        """
        
        if len(clause) <= 3:
            return [clause]
        
        k = self.num_variables+1
        self.num_variables += 1
        
        mid = len(clause)//2
        
        clause_left  = clause[:mid] + [k]
        clause_right = clause[mid:] + [-k]
        
        formula_left  = self.clause_to_3SAT(clause_left)
        formula_right = self.clause_to_3SAT(clause_right)
        
        return formula_left + formula_right
        
    
    def formula_to_3SAT(self, clauses):
        
        """
        Reduces a CNF formula to 3_SAT format.
        """
        
        formula = []
        
        for clause in clauses:
            formula += self.clause_to_3SAT(clause)
            
        return formula
        
    
    def clean_clauses(self, clauses):
        
        clauses = self.formula_to_3SAT(clauses)
        
        clauses_no_repetition = []
        set_of_clauses = set()
        
        for clause in clauses:
            
            clause.sort()
            
            if tuple(clause) not in set_of_clauses:
                
                set_of_clauses.add( tuple(clause) )
                clauses_no_repetition.append(clause)
        
        return clauses_no_repetition
        
    ## Randomizing a bit
    
    def set_random_assignment(self):
        
        ## TODO: Maybe better heuristics are possible
        for i in range( self.num_variables ):
            self.assignment[i] = (0.5 < random.random())
        
    
    ## Fitness function
    
    def num_clauses_satisfied(self):
        
        res = 0
        for clause in self.formula:
            for x in clause:
                if x > 0 and self.assignment[x]:
                    res += 1
                    break
                if x < 0 and not self.assignment[x]:
                    res += 1
                    break
        
        return res
    
    @staticmethod
    
    def fitness_SAT(solver_sat, bitstring):
        
        if solver_sat.num_variables != len(bitstring):
            raise ValueError()
            
        res = 0
        for clause in solver_sat.formula:
            for x in clause:
                if x > 0 and bitstring[x-1] == '1':
                    res += 1
                    break
            
                if x < 0 and not bitstring[-x-1] == '0':
                    res += 1
                    break
        
        return res
    
    
    # def give_variables_names(self, clauses):
    #     """
        
    #     Renames the variables from 0 to n-1. Should only be called on __init__.
        
    #     """
    #     mex = 0
    #     hash_map = {}
        
    #     for i in range( len(clauses) ):
    #         for j in range( len(clauses[i]) ):
                
    #             var = clauses[i][j]
    #             if var not in hash_map:
    #                 # var is named as mex
    #                 hash_map[var] = mex
    #                 mex += 1
                    
    #             clauses[i][j] = hash_map[var]
        
    #     inverse_hash_map = {}
    #     for name in hash_map:
    #         inverse_hash_map[ hash_map[name] ] = name
            
    #     self.num_variables = mex
    #     self.hash_map = inverse_hash_map
            


## testing functions

def test1(f = None):
    
    if f is None:
        f = [[7, 1, 3, 4, 5], [2, 6, 3, 2], [1, 4, 5], [1, 4, 5]]
    
    agent = SolverSAT(f)
    
    print()
    
    # print("Formula = {}".format(agent.formula))
    print()
    
    print("Number of variables = {}".format(agent.num_variables))
    print()
    
    print("Number of clauses = {}".format( len(agent.formula)) )
    print()
    
    print("Count Satisfied = {}".format(agent.num_clauses_satisfied()))
    print()
    
    print(agent.population.head())
    print()
    
    print(agent.population.bestBlob.fitness_value)
    print()
    
    for _ in range(30):
        agent.population.generation()
    
    print("After 30 generations:\n")
    
    print(agent.population.head())
    print()
    
    print(agent.population.bestBlob.fitness_value)
    print()
    
    return agent

def test2(n = 15, m = 5000):
    
    
    chosen = [False]*(n+1)
    clauses = []
    
    for i in range(m):
        
        new_clause = []
            
        for _ in range(3):
            
            x = random.randint(1, n)
            
            chosen[x] = True
            
            if random.random() > 0.5:
                new_clause.append(x)
            else:
                new_clause.append(-x)
                
        clauses.append(new_clause)
    
    for i in range(1,n+1):
        if not chosen[i]:
            k = random.randint(0, m-1)
            clauses[k].append(i)
    
    return test1( clauses )
    
    

