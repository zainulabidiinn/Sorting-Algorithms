import random

# Informasi pekerjaan
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

# Informasi perangkat mobile
devices = {
    i: {
        "CPU": random.uniform(1.0, 2.0),  # dalam GHz
        "Battery": random.uniform(3.0, 6.0),  # dalam AH
        "TransferRate": random.uniform(10, 50)  # dalam Mbps
    }
    for i in range(1, 51)
}

# Informasi transfer energi
transfer_energy = {
    "Fog": 0.01,  # dalam AH per KB
    "Cloud": 0.01  # dalam AH per KB
}

# Fungsi untuk menghitung waktu
def calculate_time(job, device):
    job_size = jobs[job]["Size"]
    execution_freq = jobs[job]["Execution"]
    cpu_freq = devices[device]["CPU"]

    # Hitung waktu eksekusi pada perangkat
    execution_time = job_size / (execution_freq / cpu_freq)

    return execution_time

# Fungsi untuk menghitung waktu transfer data
def calculate_transfer_time(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]

    # Hitung waktu transfer data
    transfer_time = data_size / transfer_rate

    return transfer_time

# Fungsi untuk menghitung total waktu
def calculate_total_time(combination):
    total_time = 0

    for job, device in combination.items():
        data_size = jobs[job]["Size"]
        execution_time = calculate_time(job, device)
        transfer_time = calculate_transfer_time(device, "Fog", data_size)
        total_time += execution_time + transfer_time

    return total_time

# Fungsi untuk menghasilkan kombinasi awal
def generate_initial_solution():
    combination = {}

    for job in range(1, 11):
        device = random.choice(list(devices.keys()))
        combination[job] = device

    return combination

# Fungsi untuk menghasilkan tetangga baru berdasarkan permutasi dua tugas
def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    job1, job2 = random.sample(jobs, 2)
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

# Fungsi untuk menghitung nilai energi
def calculate_energy(solution):
    total_time = calculate_total_time(solution)
    return total_time

# Fungsi untuk menjalankan Differential Evolution
def differential_evolution():
    population_size = 10
    crossover_rate = 0.5
    scaling_factor = 0.5
    max_generations = 100

    # Inisialisasi populasi awal
    population = [generate_initial_solution() for _ in range(population_size)]

    generation = 0
    while generation < max_generations:
        new_population = []

        for i in range(population_size):
            # Pilih tiga solusi acak
            candidates = random.sample(population, 3)
            x1, x2, x3 = candidates

            # Buat tetangga baru
            neighbor = generate_neighbor(population[i])

            # Crossover
            trial_solution = {}
            for j in range(1, 11):
                if random.random() < crossover_rate:
                    trial_solution[j] = neighbor[j]
                else:
                    trial_solution[j] = population[i][j]

            # Mutasi
            mutated_solution = {}
            for j in range(1, 11):
                if random.random() < scaling_factor:
                    mutated_solution[j] = random.choice(list(devices.keys()))
                else:
                    mutated_solution[j] = trial_solution[j]

            # Evaluasi energi
            energy = calculate_energy(population[i])
            mutated_energy = calculate_energy(mutated_solution)

            # Seleksi
            if mutated_energy < energy:
                new_population.append(mutated_solution)
            else:
                new_population.append(population[i])

        # Ganti populasi dengan populasi baru
        population = new_population

        # Increment generation counter
        generation += 1

    # Cari solusi terbaik
    best_solution = min(population, key=calculate_energy)
    best_energy = calculate_energy(best_solution)

    return best_solution, best_energy

# Jalankan algoritma Differential Evolution
best_solution, best_energy = differential_evolution()

# Tampilkan hasil
print("Solusi Terbaik:")
print(best_solution)
print("Energi Terbaik:", best_energy)