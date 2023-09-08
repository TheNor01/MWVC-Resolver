from modules.classes import Graph
from modules.mutation import Mutation
from modules.utiity import *
from settings import setting

import random
INSTANCE_PATH = "instances/"

if __name__ == "__main__":

    #LOAD SETTINGS
    setting.init()



    print("STARTING ... \n")

    #print("choose input filename")
    file_path = "vc_20_60_01"

    #file_path = input()

    print("Processing input: " + str(file_path)+"\n")

    f = open(INSTANCE_PATH+file_path+".txt", "r")
    inputLines = f.read().splitlines()

    #print(inputLines)

    nodes_number = int(inputLines[0])
    node_weights = inputLines[1] #array, contains space, have to split it
    #print(node_weights)
    node_weights = [int(s) for s in node_weights.split() if s.isdigit()]
    


    print(nodes_number)
    print(node_weights)

    #build links
    links_lines = inputLines[2:]
    linksStructure = []
    for i in links_lines:
        i = [int(s) for s in i.split() if s.isdigit()]
        linksStructure.append(i)

    #print(linksStructure)

    #we got all inputs; How to handle linking?

    graph = Graph(nodes_number, linksStructure,node_weights) 

    print(graph.edges) # alphabet is working!
    #print(graph.linking_structure)

    #NB. Some links are reduntat. Trucante it if needed


    #Checking settings file

    print("Population setting: "+str(setting.POPULATION))

    #We should create a set of random solution

    ALL_POPULATION = []

    if(setting.POPULATION <= 1):
        print("SET A POPULATION > 1")
        exit()

    FE = 1 #F E = 2 × 104 as the maximum number for objective function evaluations.

    for i in range(setting.POPULATION):
        print("sol:"+str(i))
        mutationTool = Mutation(graph.vertices)


        print(mutationTool.population)
        mutationTool.fitness()
        print(mutationTool.scoreFitness)

        ALL_POPULATION.append(mutationTool) #every mutation has a population and a fitness

        #bug fitness is always zero --> solved

    for iteration in range(setting.LIMIT_ITER):

        #selection step

        #for _ in range(int(setting.POPULATION / 2)): #to check
        for _ in range(1): #test

            #SELECTION
                #0 : roulette
                #1 : Tournament
                #2 : random


            ## !!!!!!!!! doesn't change, Try different name

            #solution  --> fix
            #Assignment statements in Python do not copy objects, they create bindings between a target and an object.



            print("SELECTION PHASE...")
            parentA, parentB = Selection(2,ALL_POPULATION,2) #method, pop, how many parents

            print(parentA.population)
            print(parentA.scoreFitness)
            print(parentB.population)
            print(parentB.scoreFitness)

            #CROSSOVER  https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
            crossPA = Mutation(graph.vertices)
            crossPB = Mutation(graph.vertices)

            if random.random() <= setting.CROSS_P:

                print("CROSSOVER PHASE...")
                parentAP,parentBP = Crossover(3,parentA,parentB,nodes_number)

                crossPA.SetPopulation(parentAP)
                crossPA.fitness()

                crossPB.SetPopulation(parentBP)
                crossPB.fitness()

                FE +=2

                print(crossPA.population)
                print(crossPA.scoreFitness)
                print(crossPB.population)
                print(crossPB.scoreFitness)

            else:
                crossPA.SetPopulation(parentA.population)
                crossPB.SetPopulation(parentB.population)


            #Mutation, alter a single bit(iteration??)
            for i in range(nodes_number):
                if random.random() <= setting.MUTATION_P:
                    j = random.randint(0, nodes_number - 1)
                    crossPA.population[j] = 1 - crossPA.population[j]
            
                    j2 = random.randint(0, nodes_number - 1)
                    crossPB.population[j2] = 1 - crossPB.population[j2]

            crossPA.fitness()
            crossPB.fitness()

            print(crossPA.scoreFitness)
            print(crossPB.scoreFitness)

            FE +=2
            
            #Evaluate? Genetic is over




            
        
        pass
