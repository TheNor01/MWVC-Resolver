import random
import math


import numpy as np

class LocalSA:
    def __init__(self,max_iter,vertex_numbers,initial_temperature,cooling_rate):
        self.max_iterations = max_iter
        self.vertex = vertex_numbers
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate


    def swap_solution(self,solution):
        neighbor = solution.copy()
        i, j = random.sample(range(self.vertex), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor
    

    def simulated_annealing(self,mutation):
        current_solution = mutation.population
        mutation.fitness()
        current_distance = mutation.scoreFitness

        
        best_solution = current_solution.copy()
        
        best_distance = current_distance
        #print(type(best_solution))
        temperature = self.initial_temperature

        tabu_list = []
        tabu_list_size = 10

        for iteration in range(self.max_iterations):
            neighbor = self.swap_solution(current_solution).copy() #swap popolation

            mutation.SetPopulation(neighbor)
            mutation.fitness()
    

            neighbor_distance = mutation.scoreFitness

            #if score is lower, we check if is VALID
            #print(type(neighbor))
            is_in_list = np.any(np.all(neighbor == tabu_list, axis=0))
            if(not mutation.isValid() and not is_in_list):

                if(len(tabu_list) > tabu_list_size): #fare spazio al nuovo
                    tabu_list.pop(0)

                if (neighbor_distance < current_distance):

                    #print("VALID")
                    current_solution = neighbor.copy()
                    current_distance = neighbor_distance
                    if neighbor_distance < best_distance:
                        best_solution = neighbor.copy()
                        best_distance = neighbor_distance
                else:
                    # Calculate the probability of accepting a worse solution and not valid
                    #t = temperature / float(iteration + 1)
                    t = temperature
                    x = (-(current_distance - neighbor_distance) / t)


                    #print((current_distance,neighbor_distance,t))
                    #print(x)
                    acceptance_probability = np.exp(x)
                    if random.random() < acceptance_probability:
                        current_solution = neighbor.copy()
                        current_distance = neighbor_distance

                # Reduce the temperature

                tabu_list.append(neighbor)
                if len(tabu_list) > 10:
                    tabu_list.pop()
                temperature *= self.cooling_rate

        return best_solution, best_distance