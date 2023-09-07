

from matplotlib import pyplot as plt
import random
import numpy as np



def Selection(method,ALL_POPULATION,K):

    a =  None
    b =  None
    #Fitness proportionate
    if(method==0):
        #a, b = copy.deepcopy(random.choices(population, [1/i.fitness for i in population], k=2))
        #2 changes?! https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm
        a, b = random.choices(ALL_POPULATION, [1/i.scoreFitness for i in ALL_POPULATION], k=K) #we give weights according to fitness
    elif(method==1):
        #a = copy.deepcopy(min(random.sample(population, K), key = lambda i: 1/i.fitness))
        a = min(random.sample(ALL_POPULATION, K), key = lambda i: 1/i.scoreFitness) # we want the mininum fitness, in order to improve our score.    
        b = min(random.sample(ALL_POPULATION, K), key = lambda i: 1/i.scoreFitness)
    else:
        a, b = random.sample(ALL_POPULATION, 2) #Random Selection

    #check if a,b are equal?

    return a,b

def BaseCross(A,B,x):
    localA = np.append(A[0:x],B[x:])
    localB = np.append(B[0:x],A[x:])

    return localA,localB

def Crossover(method,parent1,parent2,vertexNumber):

    a = None
    b = None
    x = random.randint(0, vertexNumber - 2) # to slice after
    allX = random.sample(range(1, vertexNumber), 5) #for instance
    #singlePoint
    if(method==0):
        a,b = BaseCross(parent1,parent2,x)
    #Multipoint
    elif(method==1):
        for i in allX:
            a,b = BaseCross(parent1,parent2,i)
    #uniform
    else:


