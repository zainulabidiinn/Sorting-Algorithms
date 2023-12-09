import math
import random

# Fungsi untuk menghitung jarak Euclidean antara dua kota
def euclidean_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Fungsi untuk menghitung total jarak rute
def calculate_total_distance(route, cities):
    total_distance = 0
    num_cities = len(route)
    for i in range(num_cities):
        city1 = cities[route[i]]
        city2 = cities[route[(i + 1) % num_cities]]
        total_distance += euclidean_distance(city1, city2)
    return total_distance

# Fungsi untuk membuat rute awal secara acak
def generate_initial_route(num_cities):
    route = list(range(1, num_cities + 1))
    random.shuffle(route)
    return route

# Fungsi untuk melakukan pertukaran dua kota pada rute
def swap_cities(route):
    num_cities = len(route)
    index1 = random.randint(0, num_cities - 1)
    index2 = random.randint(0, num_cities - 1)
    route[index1], route[index2] = route[index2], route[index1]
    return route

# Fungsi untuk menjalankan algoritma Simulated Annealing
def simulated_annealing(cities, initial_temperature, cooling_rate, num_iterations):
    num_cities = len(cities)
    current_route = generate_initial_route(num_cities)
    current_distance = calculate_total_distance(current_route, cities)
    best_route = current_route.copy()
    best_distance = current_distance

    temperature = initial_temperature

    for _ in range(num_iterations):
        new_route = swap_cities(current_route)
        new_distance = calculate_total_distance(new_route, cities)

        delta = new_distance - current_distance

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_route = new_route
            current_distance = new_distance

        if current_distance < best_distance:
            best_route = current_route.copy()
            best_distance = current_distance

        temperature *= cooling_rate

    return best_route, best_distance

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

# Parameter algoritma Simulated Annealing
initial_temperature = 1000
cooling_rate = 0.95
num_iterations = 10000

best_route, best_distance = simulated_annealing(cities, initial_temperature, cooling_rate, num_iterations)

print("Rute terpendek:", best_route)
print("Jarak terpendek:", best_distance)