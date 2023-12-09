import math
import random

class Particle:
    def __init__(self, num_cities):
        self.position = list(range(1, num_cities + 1))
        random.shuffle(self.position)
        self.velocity = [0] * num_cities
        self.best_position = self.position.copy()
        self.best_fitness = math.inf

def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_fitness(position, cities):
    total_distance = 0
    num_cities = len(position)
    for i in range(num_cities):
        city1 = cities[position[i]]
        city2 = cities[position[(i + 1) % num_cities]]
        total_distance += calculate_distance(city1, city2)
    return total_distance

def update_particle_velocity(particle, global_best_position, inertia_weight, cognitive_weight, social_weight):
    num_cities = len(particle.position)
    for i in range(num_cities):
        r1 = random.random()
        r2 = random.random()

        cognitive_component = cognitive_weight * r1 * (particle.best_position[i] - particle.position[i])
        social_component = social_weight * r2 * (global_best_position[i] - particle.position[i])

        particle.velocity[i] = inertia_weight * particle.velocity[i] + cognitive_component + social_component

def update_particle_position(particle, cities):
    num_cities = len(particle.position)
    for i in range(num_cities):
        position = int(round(particle.position[i] + particle.velocity[i])) % num_cities
        particle.position[i] = position + 1

    current_fitness = calculate_fitness(particle.position, cities)
    if current_fitness < particle.best_fitness:
        particle.best_position = particle.position.copy()
        particle.best_fitness = current_fitness

def particle_swarm_optimization(cities, num_particles, num_iterations, inertia_weight, cognitive_weight, social_weight):
    num_cities = len(cities)
    particles = [Particle(num_cities) for _ in range(num_particles)]
    global_best_position = particles[0].best_position.copy()
    global_best_fitness = particles[0].best_fitness

    for _ in range(num_iterations):
        for particle in particles:
            update_particle_velocity(particle, global_best_position, inertia_weight, cognitive_weight, social_weight)
            update_particle_position(particle, cities)

            if particle.best_fitness < global_best_fitness:
                global_best_position = particle.best_position.copy()
                global_best_fitness = particle.best_fitness

    return global_best_position, global_best_fitness

# Koordinat kota-kota
cities = {
    1: (2, 5),
    2: (8, 3),
    3: (6, 9),
    4: (4, 7),
    5: (10, 2),
    6: (12, 6),
    7: (3, 10),
    8: (9, 8),
    9: (5, 4),
    10: (11, 1),
    11: (7, 12),
    12: (1, 9),
    13: (10, 5),
    14: (4, 3),
    15: (8, 11),
    16: (6, 1),
    17: (3, 7),
    18: (9, 4),
    19: (12, 10),
    20: (2, 2)
}

# Parameter algoritma Particle Swarm Optimization
num_particles = 50
num_iterations = 100
inertia_weight = 0.8
cognitive_weight = 1.0
social_weight = 1.0

# Jalankan algoritma Particle Swarm Optimization
best_route, best_distance = particle_swarm_optimization(
    cities, num_particles, num_iterations, inertia_weight, cognitive_weight, social_weight)

# Cetak hasil
print("Rute terpendek:", best_route)
print("Jarak terpendek:", best_distance)