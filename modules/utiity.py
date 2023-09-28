

from matplotlib import pyplot as plt
import random
import numpy as np

import copy


def save_plt(best,problemName):
    #plt.plot(mean, label='mean_fitness')
    plt.plot(best, label='best_scores')
    plt.legend()
    plt.savefig("output/images/"+problemName+".png")
    plt.cla()
    plt.close()
    #plt.show()

def Selection(method,ALL_POPULATION,K):

    a =  None
    b =  None
    #Fitness proportionate
    if(method==0):
        #2 changes?! https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_parent_selection.htm
        a, b = copy.deepcopy(random.choices(ALL_POPULATION, [1/i.scoreFitness for i in ALL_POPULATION], k=K))#we give weights according to fitness
    elif(method==1):
        a = copy.deepcopy(min(random.sample(ALL_POPULATION, K), key = lambda i: 1/i.scoreFitness)) # we want the mininum fitness, in order to improve our score.    
        b = copy.deepcopy(min(random.sample(ALL_POPULATION, K), key = lambda i: 1/i.scoreFitness))
    else:
        a, b = copy.deepcopy(random.sample(ALL_POPULATION, 2)) #Random Selection

    #check if a,b are equal?

    return a,b

def BaseCross(A,B,x):
    localA = np.append(A[0:x],B[x:])
    localB = np.append(B[0:x],A[x:])

    return localA,localB

def UniformCross(A,B,p):
    for i in range(len(p)):
        temp = A[i]
        A[i] = B[i]
        B[i] = temp

    return A,B




def Crossover(method,parent1,parent2,vertexNumber):

    a = None
    b = None

    parent1P = parent1.population
    parent2P = parent2.population

    x = random.randint(0, vertexNumber - 2) # to slice after
    allX = random.sample(range(1, vertexNumber), 5) #for instance

    #singlePoint
    if(method==0):
        parent1P,parent2P = BaseCross(parent1P,parent2P,x)
    #Multipoint
    elif(method==1):
        for i in allX:
            parent1P,parent2P = BaseCross(parent1P,parent2P,i)
    #uniform
    else:
        p = np.random.rand(vertexNumber)
        parent1P,parent2P = UniformCross(parent1P,parent2P,p)


    #return 2 two objects with population
    out1 = copy.deepcopy(parent1P)
    out2 = copy.deepcopy(parent2P)

    return out1,out2


def MultiParentCrossover(crossPA,parent,allpopulations,K):

    #since allpopulation is sorted by score, we can retrieve the first K incremental parent and test 
    # fitness each iteration

    print("MULTIPARENTS")

    subItems = allpopulations[0:K]
    subPopulations = [x.population for x in subItems]

    print(subPopulations)
    basePopulation = parent.population
    crossPA.SetPopulation(parent.population)
    crossPA.fitness()
    baseFitness = crossPA.scoreFitness

    print("STARTING MULTI FIT: "+str(baseFitness))

    localPopulation = copy.deepcopy(basePopulation)

    print("LOCAL = "+ str(localPopulation))
    #while(isValid):
        
    popSize = len(subPopulations[0])
    print("pop size: "+str(popSize))

    index = 0
    for subP in subPopulations: #for every population
        if(localPopulation != subP):
            #noImpr=False

            print("-------------")
            print("index starts from :" + str(index))
            print("LOCAL = "+ str(localPopulation))
            print("SUBBB = "+ str(subP))
            validRange = True
            while(validRange and index < popSize):
                if(localPopulation[index] !=  subP[index]): #do the change
                    print("changing: "+str(index))

                    tmp = localPopulation[index]
                    localPopulation[index] = subP[index]

                    crossPA.SetPopulation(localPopulation)
                    crossPA.fitness()
                    newFit = crossPA.scoreFitness
                    print("FIT "+str(newFit))
                    if(newFit >= baseFitness ):
                        print("NONE Improv -> skip sub") #skip subPopulation and restart from index
                        validRange = False
                        localPopulation[index] = tmp
                        #popSize = index #restart from here
                        break #avoid increment index
                    else:
                        baseFitness = newFit

                index = index + 1
            #validRange = False 
            #if(noImpr==True): continue #skip

    print("LOCAL FINAL= "+ str(localPopulation))
    crossPA.SetPopulation(localPopulation)
    crossPA.fitness()
    newFit = crossPA.scoreFitness
    print("FIT FINAL "+str(newFit))

    return localPopulation



