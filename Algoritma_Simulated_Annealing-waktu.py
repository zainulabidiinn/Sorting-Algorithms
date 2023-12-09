import random
import math

# Informasi pekerjaan
jobs = {
    1: {
        "Ukuran": 30,  # dalam KB
        "Eksekusi": 40000  # dalam Hz
    },
    2: {
        "Ukuran": 100,  # dalam KB
        "Eksekusi": 500000  # dalam Hz
    },
    3: {
        "Ukuran": 10000,  # dalam KB
        "Eksekusi": 40000  # dalam Hz
    },
    4: {
        "Ukuran": 50,  # dalam KB
        "Eksekusi": 200000  # dalam Hz
    },
    5: {
        "Ukuran": 500,  # dalam KB
        "Eksekusi": 1000000  # dalam Hz
    },
    6: {
        "Ukuran": 200,  # dalam KB
        "Eksekusi": 600000  # dalam Hz
    },
    7: {
        "Ukuran": 1000,  # dalam KB
        "Eksekusi": 300000  # dalam Hz
    },
    8: {
        "Ukuran": 150,  # dalam KB
        "Eksekusi": 700000  # dalam Hz
    },
    9: {
        "Ukuran": 1000,  # dalam KB
        "Eksekusi": 200000  # dalam Hz
    },
    10: {
        "Ukuran": 2000,  # dalam KB
        "Eksekusi": 900000  # dalam Hz
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
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
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
        data_size = jobs[job]["Ukuran"]
        execution_time = calculate_time(job, device)
        transfer_time = calculate_transfer_time(device, "Fog", data_size)
        total_time += execution_time + transfer_time

    return total_time

# Fungsi untuk menghasilkan kombinasi awal
def generate_initial_solution():
    combination = {}

    for job in range(1, 11):
        devices_copy = list(devices.keys())
        random.shuffle(devices_copy)
        device = devices_copy[0]
        combination[job] = device

    return combination

# Fungsi untuk menghasilkan tetangga baru berdasarkan permutasi dua tugas
def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    random.shuffle(jobs)
    job1, job2 = jobs[:2]
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

# Fungsi untuk menghitung nilai waktu
def calculate_time_value(solution):
    total_time = calculate_total_time(solution)
    return total_time

# Fungsi untuk menerima perubahan solusi berdasarkan suhu dan nilai waktu
def accept_change(delta_time, temperature):
    if delta_time < 0:
        return True
    acceptance_probability = math.exp(-delta_time / temperature)
    return random.random() < acceptance_probability

# Fungsi untuk menjalankan simulated annealing
def simulated_annealing():
    # Inisialisasi suhu awal dan suhu akhir
    initial_temperature = 100
    final_temperature = 0.1

    # Inisialisasi solusi awal
    current_solution = generate_initial_solution()
    best_solution = current_solution.copy()

    # Hitung nilai waktu solusi awal
    current_time = calculate_time_value(current_solution)
    best_time = current_time

    # Looping simulated annealing
    while initial_temperature > final_temperature:
        # Generasi solusi tetangga
        neighbor_solution = generate_neighbor(current_solution)

        # Hitung nilai waktu solusi tetangga
        neighbor_time = calculate_time_value(neighbor_solution)

        # Hitung perbedaan nilai waktu antara solusi tetangga dan solusi saat ini
        delta_time = neighbor_time - current_time

        # Terima atau tolak perubahan solusi berdasarkan suhu dan nilai waktu
        if accept_change(delta_time, initial_temperature):
            current_solution = neighbor_solution
            current_time = neighbor_time

        # Perbarui solusi terbaik jika ditemukan solusi yang lebih baik
        if current_time < best_time:
            best_solution = current_solution.copy()
            best_time = current_time

        # Kurangi suhu
        initial_temperature *= 0.9

    return best_solution, best_time

# Jalankan simulated annealing
best_solution, best_time = simulated_annealing()

# Print hasil solusi terbaik
print("Solusi terbaik:")
print(best_solution)
print("Nilai waktu terbaik:")
print(best_time)
