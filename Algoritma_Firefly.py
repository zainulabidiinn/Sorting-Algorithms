import math
import random

class Firefly:
    def __init__(self, num_cities):
        self.position = list(range(1, num_cities + 1))
        random.shuffle(self.position)
        self.intensity = 0

def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_intensity(firefly, cities):
    total_distance = 0
    num_cities = len(firefly.position)
    for i in range(num_cities):
        city1 = cities[firefly.position[i]-1]
        city2 = cities[firefly.position[(i + 1) % num_cities]-1]
        total_distance += calculate_distance(city1, city2)
    return 1 / total_distance

def move_firefly(firefly, other_firefly, attractiveness, beta):
    num_cities = len(firefly.position)
    for i in range(num_cities):
        if firefly.intensity < other_firefly.intensity:
            city1 = cities[firefly.position[i]-1]  # Mengambil koordinat kota dari list cities
            city2 = cities[other_firefly.position[i]-1]  # Mengambil koordinat kota dari list cities
            distance = calculate_distance(city1, city2)
            attractiveness_factor = attractiveness * math.exp(-beta * distance**2)
            random_factor = random.uniform(0, 1)
            if random_factor < attractiveness_factor:
                firefly.position[i], other_firefly.position[i] = other_firefly.position[i], firefly.position[i]

def firefly_algorithm(cities, num_fireflies, num_iterations, attractiveness, beta):
    num_cities = len(cities)
    fireflies = [Firefly(num_cities) for _ in range(num_fireflies)]

    for _ in range(num_iterations):
        for i in range(num_fireflies):
            fireflies[i].intensity = calculate_intensity(fireflies[i], cities)
            for j in range(num_fireflies):
                if fireflies[j].intensity > fireflies[i].intensity:
                    move_firefly(fireflies[i], fireflies[j], attractiveness, beta)

    best_firefly = max(fireflies, key=lambda x: x.intensity)
    best_route = best_firefly.position
    best_distance = 1 / best_firefly.intensity

    return best_route, best_distance

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

# Parameter algoritma Firefly
num_fireflies = 50
num_iterations = 100
attractiveness = 1.0
beta = 1.0

# Jalankan algoritma Firefly
best_route, best_distance = firefly_algorithm(
    cities, num_fireflies, num_iterations, attractiveness, beta)

# Cetak hasil
print("Rute terpendek:", best_route)
print("Jarak terpendek:", best_distance)