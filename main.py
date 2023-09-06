
"""

ALDO FIORITO 1000038099
"TheNor" repo.
Resolving MWVC using genetic algorithms

TO DO:
variables and name formats

def is_valid_cover(solution, vertices):

        A candidate solution S is a valid solution, called Vertex Cover, 
        if each edge in G has at least one endpoint in S. 
        The objective function value ω(S) of a candidate solution S is defined as the sum of the weights of the vertices in S. 
        The objective of the MWVC problem is then to find a valid candidate solution that minimizes the objective function.
        for i in range(len(solution)):
            if solution[i] == 0:
                for j in range(len(vertices[i].neighbors)):
                    if solution[int(vertices[i].neighbors[j].name)] == 0:
                        return True
        return False

"""


if __name__ == "__main__":
    pass