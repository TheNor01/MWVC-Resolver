
"""

ALDO FIORITO 1000038099
"TheNor" repo.
https://github.com/TheNor01/MWVC_res



Resolving MWVC using genetic algorithms

"""
from modules.classes import Graph
from modules.mutation import Mutation
from modules.utiity import *
from settings import setting
import pandas as pd
import time


"""

(20,60); (20,120); (25,150); (100,500); (100,2000); (200,750); 
(200,3000); e  (800,10000).


"""


# Todo 
# 1) Improved genetic crossver n parents
# 2) debug istanza 20_120_01
# 3) relazione


import sys
sys.setrecursionlimit(9999) #change according python version and you system

import random
INSTANCE_PATH = "instances/"

OUTPUT_CSV = "output/results.csv"

if __name__ == "__main__":

    #LOAD SETTINGS
    setting.init()

    print("STARTING ... \n")

    print("choose input filename")

    file_pathInput = input("Insert file/s to resolve (without .txt) and separated by ',' :\n")
    #file_pathAll = ["vc_20_60_01","vc_20_120_01","vc_25_150_01","vc_100_500_01","vc_100_2000_01","vc_200_750_01","vc_200_3000_01"]

    file_pathAll = file_pathInput.strip().split(",")
    file_pathList,timeList,scoreList, = [],[],[]
    for file_path in file_pathAll:

        
        print("Processing input: " + str(file_path)+"\n")

        f = open(INSTANCE_PATH+file_path+".txt", "r")
        inputLines = f.read().splitlines()


        file_pathList.append(file_path)

        nodes_number = int(inputLines[0])
        node_weights = inputLines[1] #array, contains space, have to split it

        
        node_weights = [int(s) for s in node_weights.split() if s.isdigit()]
        best_scores = [] 

        #build links
        links_lines = inputLines[2:]
        linksStructure = []
        for i in links_lines:
            i = [int(s) for s in i.split() if s.isdigit()]
            linksStructure.append(i)

        graph = Graph(nodes_number, linksStructure,node_weights) 

        print("Population setting: "+str(setting.POPULATION))
        ALL_POPULATION = []
        random.seed()

        if(setting.POPULATION <= 1):
            print("SET A POPULATION > 1")
            exit()

        FE = 1

        #SETUP POPULATION
        st = time.time()
        for i in range(setting.POPULATION):
            print("sol:"+str(i))

            while(True): #we start from valid cover
                mutationTool = Mutation(graph.vertices)
                if(mutationTool.isValid()):
                    print(mutationTool.population)
                    mutationTool.fitness()
                    print(mutationTool.scoreFitness)
                    break
                
            ALL_POPULATION.append(mutationTool)

        #PROCESSING
        iteration=True
        while(iteration):

            valid_population = []

            for _ in range(int(setting.POPULATION)): 
    #----------------------------------------------------
                #SELECTION
                    #0 : roulette
                    #1 : Tournament
                    #2 : random
                print("SELECTION PHASE...")
                parentA, parentB = Selection(1,ALL_POPULATION,2)

               
    #----------------------------------------------------
                #CROSSOVER 
                crossPA = Mutation(graph.vertices)
                crossPB = Mutation(graph.vertices)

                if random.random() <= setting.CROSS_P:
                    print("CROSSOVER PHASE...")
                    parentAP,parentBP = Crossover(0,parentA,parentB,nodes_number)

                    crossPA.SetPopulation(parentAP)
                    crossPA.fitness()
                    
                    crossPB.SetPopulation(parentBP)
                    crossPB.fitness()

                    FE +=2

                  
                else:
                    print("NOT CROSSOVER PHASE...")
                    crossPA.SetPopulation(parentA.population)
                    crossPB.SetPopulation(parentB.population)
                    crossPA.fitness()
                    crossPB.fitness()

                    FE +=2

    #----------------------------------------------------

                print("MUTATION PHASE...")
            
                if random.random() <= setting.MUTATION_P:
                    print("changing bit 1")
                    j = random.randint(0, nodes_number - 1)
                    crossPA.population[j] = 1 - crossPA.population[j]

                
                if random.random() <= setting.MUTATION_P:
                    print("changing bit 2")
                    j2 = random.randint(0, nodes_number - 1)
                    crossPB.population[j2] = 1 - crossPB.population[j2]

                crossPA.fitness()
                crossPB.fitness()

                print(' '.join(map(str, crossPA.population))  +  " - score: " +str(crossPA.scoreFitness))
                print(' '.join(map(str, crossPB.population))  +  " - score: " +str(crossPB.scoreFitness))

                FE +=2

                if (not (crossPA.isValid()) and (not crossPA in valid_population) and (not crossPA in ALL_POPULATION)):
                    print("adding crossPa")
                    valid_population.append(crossPA)

                if (not (crossPB.isValid()) and (not crossPB in valid_population) and (not crossPB in ALL_POPULATION)):
                    print("adding crossPb")
                    valid_population.append(crossPB)

                #we sum the 2 population in order to pass them into other iteration 
                ALL_POPULATION = sorted(ALL_POPULATION + valid_population, key = lambda i: i.scoreFitness, reverse = False)[0:setting.POPULATION]


                best_fitness = min([i.scoreFitness for i in ALL_POPULATION]) # best values of the fitness
                best_scores.append(best_fitness)

                
                if(FE > setting.LIMIT_ITER):
                    et = time.time()

                    elapsed_time = et - st
                    print("MAX Fitness evaluation")
                    scoreList.append(best_fitness)
                    timeList.append(elapsed_time)
                    iteration = False

        save_plt(best_scores,file_path)

    fullInfoDf = pd.DataFrame(data=zip(file_pathList,scoreList,timeList),columns=['file','bestScore','time'])
    fullInfoDf.to_csv(OUTPUT_CSV, sep='\t',index=False)