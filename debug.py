


INSTANCE_PATH = "instances/"

if __name__ == "__main__":


    print("STARTING ... \n")


    file_path = "vc_20_60_01"

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

    exit()
