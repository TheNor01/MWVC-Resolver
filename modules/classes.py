
#Input instance


"""
First line is #vertex Number
Second line are weights?! For each vertex

Then linking matrix? #Vn x #Vn, i assume


20
   80   37   50  103   26   73   41   30   31   66  107   39   46   90  102   94   54   36   76  105
 0 0 0 0 0 0 0 1 1 1 0 0 0 0 1 0 0 1 0 0
 0 0 0 1 1 0 0 1 0 1 0 0 0 0 1 1 0 1 0 1
 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 1 1 0 1 0
 0 1 0 0 0 1 0 0 1 0 0 0 0 0 0 1 0 0 1 1
 0 1 0 0 0 1 0 0 0 0 1 0 1 1 0 0 0 1 0 0
 0 0 1 1 1 0 0 0 0 0 1 0 0 0 0 1 0 0 1 0
 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 0 0 1 0 0
 1 1 0 0 0 0 0 0 1 1 1 1 0 1 1 0 0 1 0 0
 1 0 0 1 0 0 0 1 0 1 0 0 0 0 0 0 0 0 1 1
 1 1 0 0 0 0 1 1 1 0 0 0 0 1 0 1 1 0 0 0
 0 0 0 0 1 1 0 1 0 0 0 0 0 0 0 0 0 0 1 0
 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0
 0 0 0 0 1 0 1 1 0 1 0 0 1 0 1 0 0 0 0 1
 1 1 0 0 0 0 1 1 0 0 0 0 0 1 0 0 1 1 0 1
 0 1 1 1 0 1 0 0 0 1 0 0 0 0 0 0 1 1 0 0
 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 0 0 0 0
 1 1 0 0 1 0 1 1 0 0 0 0 0 0 1 1 0 0 1 1
 0 0 1 1 0 1 0 0 1 0 1 0 1 0 0 0 0 1 0 0
 0 1 0 1 0 0 0 0 1 0 0 0 0 1 1 0 0 1 0 0

"""


import string
alpha_dict = dict(enumerate(string.ascii_lowercase))


print(alpha_dict)

class Vertex:
    def __init__(self, vertex, weight):
        self.name = vertex #should be number or letter
        self.neighbors = []
        self.weight = weight
        
    def addNeighbors(self, v):
        self.neighbors.append(v)


class Graph:
    def __init__(self, vertex_numbers, linking,weights):
        self.vertices = {} # we store vertex obj
        self.vertex_numbers = vertex_numbers
        self.linking_structure = linking # matrix?
        self.edges = [] #is it redundant?

        #automatically calls init Vertex passing weights
        self.initVertex(weights)
        #automatically calls buildEdges in order to init all
        self.buildEdges()

    def initVertex(self, weight):
        for i in range(self.vertex_numbers):
            vertex = Vertex(alpha_dict[i], weight[i])
            self.vertices[i] = vertex

    def buildEdges(self):
        for i in range(self.vertex_numbers): 
            for j in range(self.vertex_numbers):
                if(self.linking_structure[i][j] == 1): #link presente
                    #aggiungi ai vicini sia lato vertice
                    self.vertices[i].addNeighbors(self.vertices[j])
                    #crea edge
                    edge = [self.vertices[i].name, self.vertices[j].name]
                    self.edges.append(edge)

    def checkLink(i,j):
        pass


