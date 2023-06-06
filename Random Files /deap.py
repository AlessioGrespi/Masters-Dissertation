import random
import numpy as np
from deap import algorithms, base, creator, tools

# Define the number of special points and their coordinates
NUM_SPECIAL_POINTS = 5
SPECIAL_POINTS = [(5, 5), (8, 3), (2, 7), (9, 9), (4, 2)]

# Define the main path as a list of coordinates
MAIN_PATH = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]

# Calculate the distances between points
def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

# Calculate the cost of deviating from the main path
def calculate_deviation_cost(path):
    cost = 0
    for point in path:
        min_distance = min(calculate_distance(point, main_point) for main_point in MAIN_PATH)
        cost += min_distance
    return cost

# Calculate the reward of visiting the special points
def calculate_reward(path):
    reward = 0
    for point in path:
        for special_point in SPECIAL_POINTS:
            if calculate_distance(point, special_point) <= 1:
                reward += 1
    return reward

# Create the fitness function
def evaluate_path(path):
    cost = calculate_deviation_cost(path)
    reward = calculate_reward(path)
    return cost, reward

# Create the individual and population
creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))  # Minimize cost, maximize reward
creator.create("Individual", list, fitness=creator.Fitness)
toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(MAIN_PATH)), len(MAIN_PATH))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the genetic operators
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Define the evaluation function
toolbox.register("evaluate", evaluate_path)

# Define the main algorithm
def main():
    random.seed(42)

    population_size = 100
    num_generations = 50

    pop = toolbox.population(n=population_size)

    for gen in range(num_generations):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fits):
            ind.fitness.values = fit

        pop = toolbox.select(offspring, k=len(pop))

    best_individual = tools.selBest(pop, k=1)[0]
    best_path = [MAIN_PATH[i] for i in best_individual]
    best_cost, best_reward = evaluate_path(best_path)

    print("Best path:", best_path)
    print("Cost:", best_cost)
    print("Reward:", best_reward)

if __name__ == "__main__":
    main()
