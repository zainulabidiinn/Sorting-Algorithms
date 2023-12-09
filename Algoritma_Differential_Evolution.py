import random
import math

class Individual:
    def __init__(self, route):
        self.route = route

def calculate_distance(city1, city2):
    x_diff = city2[0] - city1[0]
    y_diff = city2[1] - city1[1]
    distance = math.sqrt(x_diff**2 + y_diff**2)
    return distance

def calculate_fitness(individual, cities):
    num_cities = len(cities)
    total_distance = 0
    for i in range(num_cities):
        city1 = cities[individual.route[i]]
        city2 = cities[individual.route[(i + 1) % num_cities]]
        distance = calculate_distance(city1, city2)
        total_distance += distance
    return total_distance

def generate_individual(num_cities):
    route = list(range(num_cities))
    random.shuffle(route)
    individual = Individual(route)
    return individual

def differential_evolution(cities, population_size, num_generations):
    num_cities = len(cities)
    
    # Generate initial population
    population = []
    for _ in range(population_size):
        individual = generate_individual(num_cities)
        population.append(individual)
    
    # Evolve the population
    for generation in range(num_generations):
        for i in range(population_size):
            target_individual = population[i]
            
            # Select three distinct individuals from population
            candidates = random.sample(population, 3)
            candidate1, candidate2, candidate3 = candidates
            
            # Generate a trial individual
            trial_route = []
            for j in range(num_cities):
                if random.random() < 0.5:
                    trial_route.append(candidate1.route[j])
                else:
                    mutation = candidate2.route[j] - candidate3.route[j]
                    trial_route.append((candidate1.route[j] + mutation) % num_cities)
            
            trial_individual = Individual(trial_route)
            
            # Compare trial individual with target individual
            target_fitness = calculate_fitness(target_individual, cities)
            trial_fitness = calculate_fitness(trial_individual, cities)
            
            if trial_fitness < target_fitness:
                population[i] = trial_individual
    
    # Find the best individual
    best_individual = min(population, key=lambda x: calculate_fitness(x, cities))
    best_route = best_individual.route
    best_distance = calculate_fitness(best_individual, cities)
    
    return best_route, best_distance

# Example usage
# Koordinat kota-kota
cities = [
    (2, 5),
    (8, 3),
    (6, 9),
    (4, 7),
    (10, 2),
    (12, 6),
    (3, 10),
    (9, 8),
    (5, 4),
    (11, 1),
    (7, 12),
    (1, 9),
    (10, 5),
    (4, 3),
    (8, 11),
    (6, 1),
    (3, 7),
    (9, 4),
    (12, 10),
    (2, 2)
]
population_size = 50
num_generations = 100

best_route, best_distance = differential_evolution(cities, population_size, num_generations)
print("Best Route:", best_route)
print("Best Distance:", best_distance)