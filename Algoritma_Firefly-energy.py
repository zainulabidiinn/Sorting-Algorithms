import random
import math

jobs = {
    1: {
        "Size": 30,  # dalam KB
        "Execution": 40000  # dalam Hz
    },
    2: {
        "Size": 100,  # dalam KB
        "Execution": 500000  # dalam Hz
    },
    3: {
        "Size": 10000,  # dalam KB
        "Execution": 40000  # dalam Hz
    },
    4: {
        "Size": 50,  # dalam KB
        "Execution": 200000  # dalam Hz
    },
    5: {
        "Size": 500,  # dalam KB
        "Execution": 1000000  # dalam Hz
    },
    6: {
        "Size": 200,  # dalam KB
        "Execution": 600000  # dalam Hz
    },
    7: {
        "Size": 1000,  # dalam KB
        "Execution": 300000  # dalam Hz
    },
    8: {
        "Size": 150,  # dalam KB
        "Execution": 700000  # dalam Hz
    },
    9: {
        "Size": 1000,  # dalam KB
        "Execution": 200000  # dalam Hz
    },
    10: {
        "Size": 2000,  # dalam KB
        "Execution": 900000  # dalam Hz
    }
}

devices = {
    i: {
        "CPU": random.uniform(1.0, 2.0),  # dalam GHz
        "Battery": random.uniform(3.0, 6.0),  # dalam AH
        "TransferRate": random.uniform(10, 50)  # dalam Mbps
    }
    for i in range(1, 51)
}

transfer_energy = {
    "Fog": 0.01,  # dalam AH per KB
    "Cloud": 0.01  # dalam AH per KB
}

def calculate_time(job, device):
    job_size = jobs[job]["Size"]
    execution_freq = jobs[job]["Execution"]
    cpu_freq = devices[device]["CPU"]
    execution_time = job_size / (execution_freq / cpu_freq)
    return execution_time

def calculate_transfer_time(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]
    transfer_time = data_size / transfer_rate
    return transfer_time

def calculate_total_time(combination):
    total_time = 0
    for job, device in combination.items():
        data_size = jobs[job]["Size"]
        execution_time = calculate_time(job, device)
        transfer_time = calculate_transfer_time(device, "Fog", data_size)
        total_time += execution_time + transfer_time
    return total_time

def calculate_energy(solution):
    total_time = calculate_total_time(solution)
    return total_time

def calculate_intensity(distance):
    beta = 1  # Faktor skala intensitas
    gamma = 1  # Faktor absorpsi intensitas
    intensity = beta * math.exp(-gamma * distance)
    return intensity

def calculate_distance(solution1, solution2):
    distance = 0
    for job in solution1:
        device1 = solution1[job]
        device2 = solution2[job]
        distance += abs(devices[device1]["CPU"] - devices[device2]["CPU"])
    return distance

def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    job1, job2 = random.sample(jobs, 2)
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

def firefly_algorithm():
    population_size = 50
    max_iterations = 100
    attractiveness_alpha = 0.5

    population = []
    for _ in range(population_size):
        solution = {job: random.randint(1, len(devices)) for job in jobs}
        population.append(solution)

    for _ in range(max_iterations):
        for i in range(population_size):
            for j in range(population_size):
                if calculate_energy(population[i]) > calculate_energy(population[j]):
                    distance = calculate_distance(population[i], population[j])
                    intensity = calculate_intensity(distance)
                    for job in jobs:
                        if random.random() < intensity:
                            population[i][job] = population[j][job]

    best_solution = min(population, key=calculate_energy)
    best_energy = calculate_energy(best_solution)

    return best_solution, best_energy

# Jalankan algoritma firefly
best_solution, best_energy = firefly_algorithm()

# Tampilkan hasil
print("Solusi Terbaik:")
print(best_solution)
print("Energi Terbaik:", best_energy)