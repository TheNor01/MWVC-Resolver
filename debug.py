from modules.classes import Graph
from modules.mutation import Mutation
from settings import setting
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

    for i in range(setting.POPULATION):
        print("sol:"+str(i))
        mutationTool = Mutation(graph.vertices)


        print(mutationTool.population)
        mutationTool.fitness()
        print(mutationTool.scoreFitness)

        ALL_POPULATION.append(mutationTool) #every mutation has a population and a fitness

        #bug fitness is always zero --> solved

    exit()
