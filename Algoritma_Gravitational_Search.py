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

def initialize_population(num_cities, population_size):
    population = []
    for _ in range(population_size):
        individual = generate_individual(num_cities)
        population.append(individual)
    return population

def calculate_mass(fitness_value):
    if fitness_value == 0:
        return float('inf')
    else:
        return 1 / fitness_value

def calculate_gravitational_constant(current_iteration, max_iterations):
    G0 = 100
    G = G0 * math.exp(-current_iteration / max_iterations)
    return G

def calculate_acceleration(mass, distance, G):
    epsilon = 1e-10  # Nilai epsilon yang sangat kecil
    if distance < epsilon:
        distance = epsilon
    return (G * mass) / (distance**2)

def calculate_attraction(position, best_position, G):
    return G * (best_position - position)

def update_position(position, acceleration):
    return position + acceleration

def gravitational_search_algorithm(cities, population_size, num_generations):
    num_cities = len(cities)

    # Initialize population
    population = initialize_population(num_cities, population_size)

    # Find the best individual
    best_individual = min(population, key=lambda x: calculate_fitness(x, cities))
    best_distance = calculate_fitness(best_individual, cities)

    # Main loop
    for generation in range(num_generations):
        for i in range(population_size):
            current_individual = population[i]

            # Calculate mass and fitness
            current_fitness = calculate_fitness(current_individual, cities)
            current_mass = calculate_mass(current_fitness)

            # Calculate gravitational constant
            G = calculate_gravitational_constant(generation, num_generations)

            # Calculate acceleration
            acceleration = [0] * num_cities
            for j in range(num_cities):
                for k in range(population_size):
                    if k != i:
                        other_individual = population[k]
                        distance = calculate_distance(cities[current_individual.route[j]], cities[other_individual.route[j]])
                        current_acceleration = calculate_acceleration(current_mass, distance, G)
                        acceleration[j] += current_acceleration

            # Update position
            random.shuffle(current_individual.route)

        # Update the best individual
        current_best_individual = min(population, key=lambda x: calculate_fitness(x, cities))
        current_best_distance = calculate_fitness(current_best_individual, cities)
        if current_best_distance < best_distance:
            best_individual = current_best_individual
            best_distance = current_best_distance

    best_route = best_individual.route
    return best_route, best_distance

# Koordinat kota
cities = [(2, 5), (8, 3), (6, 9), (4, 7), (10, 2), (12, 6), (3, 10), (9, 8), (5, 4), (11, 1),
          (7, 12), (1, 9), (10, 5), (4, 3), (8, 11), (6, 1), (3, 7), (9, 4), (12, 10), (2, 2)]

population_size = 50
num_generations = 100

best_route, best_distance = gravitational_search_algorithm(cities, population_size, num_generations)
print("Best Route:", best_route)
print("Best Distance:", best_distance)
