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

class Particle:
    def __init__(self, num_jobs):
        self.position = [random.randint(1, 50) for _ in range(num_jobs)]
        self.velocity = [random.uniform(-1, 1) for _ in range(num_jobs)]
        self.best_position = self.position.copy()
        self.best_fitness = float('inf')

    def evaluate_fitness(self):
        total_time = 0
        total_energy = 0

        for i, job_id in enumerate(self.position):
            job = jobs[job_id]
            device = devices[i + 1]

            time = job['Ukuran'] / (device['TransferRate'] * 1024)
            energy = (job['Ukuran'] * transfer_energy['Fog']) + (job['Eksekusi'] / (device['CPU'] * 10**9))

            total_time += time
            total_energy += energy

        if total_time < self.best_fitness:
            self.best_position = self.position.copy()
            self.best_fitness = total_time

        return total_time, total_energy

class PSO:
    def __init__(self, num_particles, num_jobs, max_iter):
        self.num_particles = num_particles
        self.num_jobs = num_jobs
        self.max_iter = max_iter
        self.particles = [Particle(num_jobs) for _ in range(num_particles)]
        self.global_best_position = None
        self.global_best_fitness = float('inf')

    def optimize(self):
        for _ in range(self.max_iter):
            for particle in self.particles:
                particle.evaluate_fitness()

                if particle.best_fitness < self.global_best_fitness:
                    self.global_best_position = particle.best_position.copy()
                    self.global_best_fitness = particle.best_fitness

            for particle in self.particles:
                self.update_velocity(particle)
                self.update_position(particle)

    def update_velocity(self, particle):
        w = 0.5  # inertia weight
        c1 = 1.0  # cognitive weight
        c2 = 2.0  # social weight

        for i in range(self.num_jobs):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)

            cognitive_component = c1 * r1 * (particle.best_position[i] - particle.position[i])
            social_component = c2 * r2 * (self.global_best_position[i] - particle.position[i])
            particle.velocity[i] = w * particle.velocity[i] + cognitive_component + social_component

    def update_position(self, particle):
        for i in range(self.num_jobs):
            particle.position[i] = max(1, min(50, particle.position[i] + round(particle.velocity[i])))

    def get_best_solution(self):
        return self.global_best_position, self.global_best_fitness

    def get_best_time(self):
        return self.global_best_fitness

# Menentukan parameter PSO
num_particles = 50
num_jobs = 10
max_iterations = 100

# Membuat objek PSO
pso = PSO(num_particles, num_jobs, max_iterations)

# Menjalankan algoritma PSO
pso.optimize()

# Mendapatkan solusi terbaik
best_solution, best_fitness = pso.get_best_solution()

# Mendapatkan waktu terbaik
best_time = pso.get_best_time()

print("Solusi terbaik:", best_solution)
print("Waktu terbaik:", best_time)