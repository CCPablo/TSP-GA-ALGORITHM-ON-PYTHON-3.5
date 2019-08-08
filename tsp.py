import random
import json

import numpy
import matplotlib.pyplot as plt

from deap import algorithms
from deap import base as d_base
from deap import creator
from deap import tools

##
##  Importing data from JSON file
##

with open("exercise1.json", "r") as jsondata:
    jsondata = json.load(jsondata)

cities = jsondata["cities"]
cities_name = [i["name"] for i in cities]
cities_reward = [i["reward"] for i in cities]
city_base = next((index for (index,d) in enumerate(cities) if d["base"] == True))
ncities = len(cities)

connections = jsondata["connections"]
connections_from = [i["from"] for i in connections]
connections_to = [i["to"] for i in connections]
connections_cost = [i["cost"] for i in connections]
nconnections = len(connections);

#   This matrix contains the fuel cost for travelling throught cities

cost_matrix = [[0 for i in range(ncities)] for j in range(ncities)]

for i in range(ncities):
    for j in range(nconnections):
        if(connections_from[j] == cities_name[i]):
            cost_matrix[i][cities_name.index(connections_to[j])] = connections_cost[j]
            cost_matrix[cities_name.index(connections_to[j])][i] = connections_cost[j]


#%%

##
##  Auxialiary functions for the GA
##
    
#   Set the first generator for the feneration of individual
#   First and last city known (Madrid)
#   Rest uniformly random
def routeInit():
    route = random.sample(range(9),7)
    route[0] = city_base;
    route[-1] = city_base;
    return route

#   Evaluation function
def evalTSP(individual):
    cost = 0
    incentive = 0;
    
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        cost += cost_matrix[gene1][gene2]
        
    for i in range(len(individual)):
        if(i in individual):
            incentive += cities_reward[i];
        
    return (incentive - cost),

#   Feasible function is used for penalize indivuals with wrong structure
#   Penalty will be equal to 20 plus a bonus taken from routeQ function (line 141)
def feasible(individual):
    if ((individual[0]!=city_base) or (individual[-1]!=city_base)):
        return False
        
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        if (cost_matrix[gene1][gene2] == 0):
            return False
        
    return True

#   RouteQ determines the amount of penalization given to the individual
#   Penalization bigger if not begging and finalizing route in Madrid
def routeQ(individual):
    q = 0
    
    if (individual[0]!=city_base):
        q += 20
    if (individual[-1]!=city_base):
        q += 20

    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        if (cost_matrix[gene1][gene2] == 0):
            q += 4
        
    return q

#   Plot the evolution of the algorithm when it's finished
#   Reresents minimun and maximun of each generation
def evolucion(log):
    
    gen = log.select("gen")
    fit_mins = log.select("min")
    fit_maxs = log.select("max")
    fit_ave = log.select("avg")
    
    fig, ax1 = plt.subplots()
    ax1.plot(gen, fit_mins, "b")
    ax1.plot(gen, fit_maxs, "r")
    ax1.plot(gen, fit_ave, "--k")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.legend(["Min", "Max", "Avg"])
    plt.grid(True)
    plt.savefig("evolution.png")

    plt.show()


#%%

##
##  GA implementational functions for the eaSimple algorithm
##

creator.create("FitnessMax", d_base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = d_base.Toolbox()

toolbox.register("indices", routeInit)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.1) # mutation
toolbox.register("select", tools.selTournament, tournsize=3) # selection
toolbox.register("evaluate", evalTSP) # evaluation
toolbox.decorate("evaluate", tools.DeltaPenalty(feasible,-20, routeQ)) # penalization


#%%

def main():
    random.seed(80)
    
    #   As the algorithm converge rapidly to a solution and tends to stay around it,
    #   the population is set to a higher value, and number of generations to a lower value
    #   This will provide the algorithm with a better ability to match with the optimal solution
    CXPB, MUTPB, NIND, NGEN = 0.8, 0.1, 500, 40
    pop = toolbox.population(NIND)

    #   Save best individual and register data
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    logbook = tools.Logbook()
    
    pop, logbook= algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats=stats, 
                        halloffame=hof)

    return pop, hof, logbook 
    
if __name__ == "__main__":
    pop, hof, log = main()
    print("Best solution: ", hof)
    print("Best solution fitness: ", hof[0].fitness.values) 
    evolucion(log)
