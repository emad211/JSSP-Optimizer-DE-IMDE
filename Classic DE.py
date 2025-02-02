import random

class JSSPInstance:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as f:
            line = f.readline().strip().split()
            self.n, self.m = int(line[0]), int(line[1])
            self.jobs = []
            for _ in range(self.n):
                arr = list(map(int, f.readline().strip().split()))
                ops = [(arr[2*i], arr[2*i+1]) for i in range(self.m)]
                self.jobs.append(ops)
        self.total_ops = self.n * self.m

class Individual:
    def __init__(self, float_vec, permutation):
        self.float_vec = float_vec
        self.permutation = permutation
        self.makespan = None

class Population:
    def __init__(self, size: int, instance: JSSPInstance, strategy="DE/rand/1", F=0.8, CR=0.9):
        self.size = size
        self.instance = instance
        self.F = F
        self.CR = CR
        self.strategy = strategy
        self.individuals = []
        self.initialize()

    def initialize(self):
        for _ in range(self.size):
            vec = [random.uniform(0, self.instance.total_ops-1) for _ in range(self.instance.total_ops)]
            perm = self.repair(vec)
            ind = Individual(vec, perm)
            self.individuals.append(ind)

    def repair(self, float_vec):
        n, m = self.instance.n, self.instance.m
        t = n*m
        int_vec = [int(round(x)) % t for x in float_vec]
        sel = [[False]*m for _ in range(n)]
        perm = []
        for op_id in int_vec:
            j = op_id // m
            o = op_id % m
            if not sel[j][o]:
                perm.append((j, o))
                sel[j][o] = True
        missing = []
        for jj in range(n):
            for oo in range(m):
                if not sel[jj][oo]:
                    missing.append((jj, oo))
        perm.extend(missing)
        return perm[:t]

    def evaluate(self):
        for ind in self.individuals:
            ind.makespan = self.calculate_makespan(ind.permutation)

    def calculate_makespan(self, permutation):
        jobs = self.instance.jobs
        n, m = self.instance.n, self.instance.m
        machine_count = max(op[0] for job in jobs for op in job)+1
        machine_time = [0]*machine_count
        job_time = [0]*n
        for j, o in permutation:
            mm, d = jobs[j][o]
            start = max(job_time[j], machine_time[mm])
            end = start + d
            job_time[j] = end
            machine_time[mm] = end
        return max(job_time)

    def mutation(self, target_idx, population):
        t = self.instance.total_ops
        idxs = list(range(self.size))
        idxs.remove(target_idx)
        random.shuffle(idxs)
        if self.strategy == "DE/rand/1":
            x1 = population[idxs[0]].float_vec
            x2 = population[idxs[1]].float_vec
            x3 = population[idxs[2]].float_vec
            donor = [x1[k] + self.F * (x2[k] - x3[k]) for k in range(t)]
        elif self.strategy == "DE/best/1":
            best = min(population, key=lambda x: x.makespan)
            x2 = population[idxs[0]].float_vec
            x3 = population[idxs[1]].float_vec
            donor = [best.float_vec[k] + self.F * (x2[k] - x3[k]) for k in range(t)]
        elif self.strategy == "DE/rand-to-best/1":
            best = min(population, key=lambda x: x.makespan)
            target = population[target_idx].float_vec
            x1 = population[idxs[0]].float_vec
            x2 = population[idxs[1]].float_vec
            donor = [target[k] + self.F * (best.float_vec[k] - target[k]) + self.F * (x1[k] - x2[k]) for k in range(t)]
        else:
            raise ValueError(f"Unsupported strategy: {self.strategy}")
        donor = [d % self.instance.total_ops for d in donor]
        return donor

    def crossover(self, parent_vec, donor_vec):
        t = len(parent_vec)
        trial = []
        j_rand = random.randint(0, t-1)
        for j in range(t):
            if random.random() < self.CR or j == j_rand:
                trial.append(donor_vec[j])
            else:
                trial.append(parent_vec[j])
        return trial

    def selection(self, parent, trial):
        return trial if trial.makespan < parent.makespan else parent

    def run_generation(self):
        self.evaluate()
        parent_pop = self.individuals
        new_pop = []
        for i, parent in enumerate(parent_pop):
            donor = self.mutation(i, parent_pop)
            trial_vec = self.crossover(parent.float_vec, donor)
            trial_perm = self.repair(trial_vec)
            trial_ind = Individual(trial_vec, trial_perm)
            trial_ind.makespan = self.calculate_makespan(trial_perm)
            winner = self.selection(parent, trial_ind)
            new_pop.append(winner)
        self.individuals = new_pop

import csv

if __name__ == "__main__":
    instances = ["ft06.txt", "la01.txt", "ft10.txt", "la16.txt", "abz5.txt"]
    num_tests = 50
    strategies = ["DE/rand/1", "DE/best/1", "DE/rand-to-best/1"]
    results_summary = {}

    for instance_file in instances:
        print(f"\nProcessing instance: {instance_file}\n")
        instance = JSSPInstance(instance_file)
        instance_results = {}

        for strategy in strategies:
            print(f"Running strategy: {strategy}\n")
            results = []

            for test_run in range(1, num_tests + 1):
                print(f"Test Run {test_run} for strategy {strategy}:")
                pop = Population(200, instance, strategy=strategy, F=0.8, CR=0.9)
                G_max = 50

                for gen in range(G_max):
                    pop.run_generation()

                pop.evaluate()
                best = min(pop.individuals, key=lambda x: x.makespan)
                print(f"Final best makespan: {best.makespan}")
                print(f"Some operations: {best.permutation[:10]}\n")

                results.append(best.makespan)

            avg_makespan = sum(results) / len(results)
            std_makespan = (sum((x - avg_makespan) ** 2 for x in results) / len(results)) ** 0.5

            print(f"Strategy: {strategy} - Average Best Makespan: {avg_makespan}, Standard Deviation: {std_makespan}\n")

            instance_results[strategy] = {
                "results": results,
                "average": avg_makespan,
                "std_dev": std_makespan
            }

        results_summary[instance_file] = instance_results

    # Save results to a CSV file
    with open("results_summary.csv", "w", newline='') as csvfile:
        fieldnames = ["Instance", "Strategy", "Average Makespan", "Standard Deviation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for instance_file, instance_results in results_summary.items():
            for strategy, summary in instance_results.items():
                writer.writerow({
                    "Instance": instance_file,
                    "Strategy": strategy,
                    "Average Makespan": summary["average"],
                    "Standard Deviation": summary["std_dev"]
                })

    print("\nResults summary saved to 'results_summary.csv'.")

