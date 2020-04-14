import random


class Individual:
    def __init__(self, g):
        self.genes = g
        self.fitness = 0

    def breed_with(self, other):
        new_dna = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for index in range(self.genes.__len__()):
            split = random.randint(0, self.genes.__len__())
            for i in range(0, split):
                new_dna[i] = self.genes[i]
            for j in range(split, self.genes.__len__()):
                new_dna[j] = other.genes[j]
        return new_dna

    def mutate(self):
        mutation_rate = 0.01
        for i in range(self.genes.__len__()):
            if random.random() < mutation_rate:
                self.genes[i] = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


dice = [1, 2, 3, 4, 5, 6]
possibilities = []
for i in dice:
    for j in dice:
        possibilities.append(i+j)


population = []

for i in range(150):
    new_genes = []
    for x in range(10):
        new_genes.append(random.choice(possibilities))
    population.append(Individual(new_genes))


def run_game():
    for p in population:
        count = 0
        temp = p.genes.copy()
        done = False
        while not done:
            count = count + 1
            roll = random.choice(possibilities)
            if roll in temp:
                temp.remove(roll)
            if temp.__len__() == 0 or count >= 110:
                done = True
        p.fitness = count


def run_gen():
    run_game()
    #get_most_fit()
    mating_pool = []
    for individual in population:
        n = int(pow((110/individual.fitness), 2))
        for x in range(n):
            mating_pool.append(individual)

    for p in range(population.__len__()):
        mommy = random.choice(mating_pool)
        daddy = random.choice(mating_pool)

        baby = Individual(mommy.breed_with(daddy))
        baby.mutate()

        population[p] = baby


def get_most_fit():
    top_score = 110
    best = None
    for p in population:
        if p.fitness < top_score:
            top_score = p.fitness
            best = p

    print(best.genes)
    print(best.fitness)
    print("--------------")


for i in range(10000):
    run_gen()

run_game()

indexes = [[], [], [], [], [], [], [], [], [], []]


for p in population:
    p.genes = sorted(p.genes)
    for i in range(len(indexes)):
        indexes[i].append(p.genes[i])


def avg(list):
    return sum(list) / len(list)


new_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


for i in range(len(new_arr)):
    new_arr[i] = avg(indexes[i])

print(new_arr)










































