import random
import matplotlib.pyplot as plt

population_size = 100                                # individuals in one generation
population = [None] * population_size
avg_scores = []
gene_length = 10                                     # the size of the "bingo" board for dice rolling
mutation_rate = 0.001                                # how often do genes mutate during reproduction
valid_genes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]   # possible gene values
possibilities = [2,
                 3, 3,
                 4, 4, 4,
                 5, 5, 5, 5,
                 6, 6, 6, 6, 6,
                 7, 7, 7, 7, 7, 7,                   # possible die rolls during a game
                 8, 8, 8, 8, 8,
                 9, 9, 9, 9,
                 10, 10, 10,
                 11, 11,
                 12]


class Genotype:
    """
    The Genotype class represents an individual within the population.

    Genes: An integer array of 10 items; each item can have a value between 2 and 12
    Fitness: The calculated effectiveness of the genotype in playing the dice bingo game

    note: In a conventional genetic algorithm, there exists a separation between the genotype and phenotype of an
    individual. The genotype is how the expressed information is encoded and the phenotype is how that information
    is expressed. In this program, the genotype and phenotype are identical as the encoding (int between 2 and 12)
    is the same as its expression (a "bingo" field corresponding to a dice roll).
    """
    def __init__(self, g):
        self.genes = g
        self.fitness = 0

    """
    Sexually reproduces with the given partner.
    :param other: The Genotype to reproduce with
    :return: Child gene array
    """
    def breed_with(self, other):
        # Pick a random index at which we will splice the parent dna
        split = random.randint(0, gene_length)
        # Create a hybrid array by splicing the parent dna
        new_dna = self.genes[0:split] + other.genes[split: gene_length]
        # Mutate the array in order to introduce new genes into the population
        for g in range(gene_length):
            if random.random() < mutation_rate:
                new_dna[g] = random.choice(valid_genes)

        return new_dna


def make_initial_population():
    """
    Generates the initial population.
    """
    for n in range(population_size):
        new_genes = [None] * gene_length
        for z in range(gene_length):
            new_genes[z] = random.choice(possibilities)
        population[n] = Genotype(new_genes)


def get_game_scores():
    """
    This counts how many rolls it takes for each individual to cross off everything on their "bingo" card.
    The number of rolls is their raw fitness, 10 being best and 100 the worst.
    """
    for p in population:
        count = 0
        temp = p.genes.copy()
        done = False
        while not done:
            count = count + 1
            roll = random.choice(possibilities)
            if roll in temp:
                temp.remove(roll)
            if temp.__len__() == 0 or count >= population_size:
                done = True
        p.fitness = count


def calculate_true_fitness(fitness):
    """
    Transforms the raw fitness value (game score) into a weighed true fitness. The strength of true fitness grows
    exponentially, rather than linearly. This way, good genotypes will reproduce notably more than the weak ones.
    Whereas raw fitness is better when lower (10 > max), higher true fitness is better than low.
    :param fitness: raw fitness score
    :return: true fitness
    """
    return int(pow((population_size/fitness), 2))


def next_generation():
    """
    Creates the next generation by breeding the old generation.
    """
    mating_pool = []

    for individual in population:
        true_fitness = calculate_true_fitness(individual.fitness)
        for x in range(true_fitness):       # The more fit an individual is, the more times he is going to
            mating_pool.append(individual)  # be added to the mating pool, meaning they will get to reproduce more.

    for v in range(population_size):
        parent_a = random.choice(mating_pool)
        parent_b = random.choice(mating_pool)
        baby = Genotype(parent_a.breed_with(parent_b))
        population[v] = baby


def get_most_fit():
    """
    :return: Best (which means lowest in this context) raw fitness score within the population
    """
    top_score = population_size
    best = None
    for u in population:
        if u.fitness < top_score:
            top_score = u.fitness
            best = u
    return best


def get_avg_fit():
    """
    :return: Average fitness of the population
    """
    total = 0
    for r in population:
        total = total + r.fitness
    return total/population_size


def show_results():
    """
    Prints the average values in the final genotype arrays.
    """
    indexes = [[], [], [], [], [], [], [], [], [], []]

    for p in population:
        p.genes = sorted(p.genes)
        for y in range(gene_length):
            indexes[y].append(p.genes[y])

    results = [None] * gene_length

    for i in range(gene_length):
        results[i] = sum(indexes[i]) / len(indexes[i])

    print(results)


def run_iteration():
    get_game_scores()  # Calculate fitness for all individuals in the population
    avg_score = get_avg_fit()
    avg_scores.append(avg_score)
    next_generation()  # Reproduce and create next generation


if __name__ == '__main__':
    iterations = 1000
    make_initial_population()
    for iteration in range(iterations):
        run_iteration()
    show_results()
    plt.plot([l for l in range(iterations)], avg_scores)
    plt.show()








































