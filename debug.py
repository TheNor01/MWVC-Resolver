from modules.classes import Graph
from modules.mutation import Mutation
from modules.localsearch import LocalSA
from modules.utiity import *
from settings import setting
import pandas as pd
import time
"""

(20,60); (20,120); (25,150); (100,500); (100,2000); (200,750); 
(200,3000); e  (800,10000).


"""

import sys
sys.setrecursionlimit(9999)

import random
INSTANCE_PATH = "instances/"

OUTPUT_CSV = "output/results.csv"

if __name__ == "__main__":

    #LOAD SETTINGS
    setting.init()

    print("STARTING ... \n")

    #print("choose input filename")
    #file_pathAll = ["vc_20_60_01","vc_20_120_01","vc_25_150_01","vc_100_500_01","vc_100_2000_01","vc_200_750_01","vc_200_3000_01"]
    #file_pathAll = ["vc_100_2000_02","vc_200_750_02","vc_200_3000_02"]
    #file_pathAll = ["vc_20_60_02","vc_20_120_02","vc_25_150_02","vc_100_500_02","vc_100_2000_02","vc_200_750_02","vc_200_3000_02"]
    file_pathAll = ["vc_20_60_01"]
    

    file_pathList,timeList,scoreList, = [],[],[]
    #file_path = input()


    #define local search 



    doMultiCross = 0
    doMutation = 0
    doLocal = 1
    for file_path in file_pathAll:

        #file_pathList.clear()
        #timeList.clear()
        #scoreList.clear()
        
        print("Processing input: " + str(file_path)+"\n")

        f = open(INSTANCE_PATH+file_path+".txt", "r")
        inputLines = f.read().splitlines()

        #print(inputLines)

        file_pathList.append(file_path)

        nodes_number = int(inputLines[0])
        node_weights = inputLines[1] #array, contains space, have to split it

        

        #print(node_weights)
        node_weights = [int(s) for s in node_weights.split() if s.isdigit()]
        


        mean_scores = [] 
        best_scores = [] 

        #build links
        links_lines = inputLines[2:]
        linksStructure = []
        for i in links_lines:
            i = [int(s) for s in i.split() if s.isdigit()]
            linksStructure.append(i)

        #print(linksStructure)

        #we got all inputs; How to handle linking?

        graph = Graph(nodes_number, linksStructure,node_weights) 

        #init LocalSA
        localSearch = LocalSA(5000,nodes_number,2500,0.95)


        #Checking settings file

        print("Population setting: "+str(setting.POPULATION))

        #We should create a set of random solution

        ALL_POPULATION = []
        random.seed()

        if(setting.POPULATION <= 1):
            print("SET A POPULATION > 1")
            exit()

        FE = 1    

        #SETUP POPULATION
        st = time.time()
        for i in range(setting.POPULATION):
            #print("sol:"+str(i))

            i = 0
            valid = True
            pop = None
            while(valid): #we start from valid cover
                    mutationTool = Mutation(graph.vertices)
                    if(mutationTool.isValid()):
                        valid = False
                        pop  = mutationTool.population


            mutationTool = Mutation(graph.vertices)
            mutationTool.SetPopulation(pop)
            mutationTool.fitness()
            ALL_POPULATION.append(mutationTool) #every mutation has a population and a fitness

            #bug fitness is always zero --> solved

        #PROCESSING
        iteration=True

        allTimeBest = 999999999
        counter = 8000

        while(iteration):

            valid_population = []
            #selection step

            for _ in range(int(setting.POPULATION / 2)): #to check
            #for _ in range(1): #test
    #----------------------------------------------------
                #SELECTION
                    #0 : roulette
                    #1 : Tournament
                    #2 : random

                #solution  --> fix
                #Assignment statements in Python do not copy objects, they create bindings between a target and an object.

                #print("SELECTION PHASE...")
                parentA, parentB = Selection(0,ALL_POPULATION,2) #method, pop, how many parents

                #print(' '.join(map(str, parentA.population)) + " - score: " +str(parentA.scoreFitness))
                #print(' '.join(map(str, parentB.population)) + " - score: " +str(parentB.scoreFitness))

    #----------------------------------------------------
                #CROSSOVER  https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)



                #init new parents
                crossPA = Mutation(graph.vertices)
                crossPB = Mutation(graph.vertices)


                """
                print("----")
                print(' '.join(map(str, crossPA.population))  +  " - score: " +str(crossPA.scoreFitness))
                print(' '.join(map(str, crossPB.population))  +  " - score: " +str(crossPB.scoreFitness))
                print("----")
                """

                if random.random() <= setting.CROSS_P:
                    #print("CROSSOVER PHASE...")

                    #crossover population base
                    parentAP,parentBP = Crossover(1,parentA,parentB,nodes_number)


                    #we can extend the base crossover using allPopulation (it will be sorted already)
                    if(doMultiCross):
                        parentAP = MultiParentCrossover(crossPA,parentA,ALL_POPULATION,3)
                        parentBP = MultiParentCrossover(crossPB,parentB,ALL_POPULATION,3)



                    #print(parentAP)
                    #print("POST CROSS A")
                    crossPA.SetPopulation(parentAP)
                    crossPA.fitness()
                    
                    #print("POST SET A")
                    #print(crossPA.population)

                    #print(crossPB.population)
                    crossPB.SetPopulation(parentBP)
                    crossPB.fitness()

                    #parentAP,parentBP = Crossover(2,crossPA,crossPB,nodes_number)
                    FE +=2

                    #print(' '.join(map(str, crossPA.population))  +  " - score: " +str(crossPA.scoreFitness))
                    #print(' '.join(map(str, crossPB.population))  +  " - score: " +str(crossPB.scoreFitness))

                else:
                    #print("NOT CROSSOVER PHASE...")
                    crossPA.SetPopulation(parentA.population)
                    crossPB.SetPopulation(parentB.population)
                    crossPA.fitness()
                    crossPB.fitness()

                    FE +=2

    #----------------------------------------------------
                #MUTATION, alter a single bit(iteration??)

                #print("MUTATION PHASE...")

                if(doMutation):
            
                    if random.random() <= setting.MUTATION_P:
                        #print("changing bit 1")
                        j = random.randint(0, nodes_number - 1)
                        crossPA.population[j] = 1 - crossPA.population[j]
                        j_ = random.randint(0,nodes_number-1)
                        while j==j_:
                            j_=random.randint(0,nodes_number-1)
                        crossPA.population[j_] = 1 - crossPA.population[j_]
                    
                    #for i in range(nodes_number):
                    if random.random() <= setting.MUTATION_P:
                        #print("changing bit 2")
                        j2 = random.randint(0, nodes_number - 1)
                        crossPB.population[j2] = 1 - crossPB.population[j2]
                        j2_ = random.randint(0,nodes_number-1)
                        while j2==j2_:
                            j2_=random.randint(0,nodes_number-1)
                        crossPB.population[j2_] = 1 - crossPA.population[j2_]


                crossPA.fitness()
                crossPB.fitness()

                FE +=2

                #tested until here
                
                #Evaluate? Genetic is over
                # we want to select all nodes that links each nodes with mininum weights
                    #check links cover

                #replace population?
                if (not (crossPA.isValid()) and (not crossPA in valid_population) and (not crossPA in ALL_POPULATION)):
                    valid_population.append(crossPA)

                if (not (crossPB.isValid()) and (not crossPB in valid_population) and (not crossPB in ALL_POPULATION)):
                    valid_population.append(crossPB)

                #WE iterate over valid cover set again

                #NEXT ITER

                #EVOLUTION, according to #https://aicorespot.io/evolution-strategies-from-the-ground-up-in-python/

                #print(len(ALL_POPULATION))
                #print(len(valid_population))

                #we sum the 2 population in order to pass them into other iteration 
                ALL_POPULATION = sorted(ALL_POPULATION + valid_population, key = lambda i: i.scoreFitness, reverse = False)[0:setting.POPULATION]


                best_fitness = min([i.scoreFitness for i in ALL_POPULATION]) # best values of the fitness
                best_scores.append(best_fitness)

                if(best_fitness < allTimeBest): 
                    allTimeBest=best_fitness
                    counter = 8000

                if(allTimeBest == best_fitness): counter = counter - 1 

                #print("Best:"+str(best_fitness))
                
                if(FE > setting.LIMIT_ITER or counter==0):
                    et = time.time()
                    # get the execution time
                    elapsed_time = et - st
                    print("Fitness evaluation LIMIT")
                    best_all_fitness = min([i.scoreFitness for i in ALL_POPULATION])
                    print("min score F: "+str(best_all_fitness))
                    print("-------------")
                    scoreList.append(best_fitness)
                    timeList.append(elapsed_time)
                    iteration = False


                    if(doLocal):
                        #CALL LOCAL SEARCH using a subset population
                        mutation = ALL_POPULATION[0]
                        #print(mutation)
                        solution,fitness = localSearch.simulated_annealing(mutation)

                        print("LOCAL SA debug")
                        print(' '.join(map(str, solution))  +  " - score: " +str(fitness))
                    
                    break


        save_plt(best_scores,file_path)

    fullInfoDf = pd.DataFrame(data=zip(file_pathList,scoreList,timeList),columns=['file','bestScore','time'])
    fullInfoDf.to_csv(OUTPUT_CSV, sep='\t',index=False)