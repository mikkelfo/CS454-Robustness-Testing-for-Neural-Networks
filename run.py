import GA
import fitnessfunction
import mask
import random
import numpy as np

populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 299
crossoverRate = 0.9
mutationRate = 0.05
evaluationBudget = 10000
download = False

tournamentSize = 4
matingPoolSize = 2

if download:
    fitnessfunction.download_base_model()

inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()
labels = fitnessfunction.get_labels()

# get the original accuracy (no masks applied)
original_accuracy = fitnessfunction.fitness_value(
    inception, original_images, labels)
print("Original Accuracy: " + f"{original_accuracy:e}")

# initialise empty mask population
population = GA.init_population(populationSize)

# evaluate/update first generation
for i in range(0, len(population)):
    # Function can be made instead of direct access -PUT IN FUNCTION?-
    # first generation will have same accuracy as original as it's a population
    # of empty masks
    population[i].accuracy = original_accuracy
    population[i].change = population[i].mask_change()
    population[i].fitness = population[i].accuracy / population[i].change
    print("Fitness: " + f"{population[i].fitness:e}")  # <- Prints sci-notation
    # we've already used it so not sure if evaluation budget required
    # evaluationBudget -= 1

    generation = 0
while evaluationBudget > 0:
    print("Generation: " + str(generation))
    new_pop = []

    selection = GA.tournament(population, tournamentSize, matingPoolSize)
    for i in range(0, len(selection), 2):
        # selection = random.sample(population, 2) # <- Old random selection
        if random.random() < crossoverRate:
            childMask = GA.crossover(selection[i], selection[i + 1])
            for shape in childMask.shapes:
                if random.random() < mutationRate:
                    GA.mutation(shape)
                shape.update()
            new_pop.append(childMask)

    for i in range(0, len(new_pop)):
        # apply mask here and update fitness
        print("running update: " + str(i))
        new_pop[i].update(inception, original_images,
                          labels)
        print("Fitness_new: " + f"{new_pop[i].fitness:e}")  # <- sci-notation
        evaluationBudget -= 1

    print("spawned " + str(len(new_pop)) + " children")

    # next generation selection TODO change selection alg
    combined_population = population + new_pop
    combined_population_fitness = np.empty(populationSize + len(new_pop))
    for i in range(0, populationSize):
        combined_population_fitness[i] = population[i].fitness
    for i in range(0, len(new_pop)):
        combined_population_fitness[i + populationSize] = new_pop[i].fitness
    for i in range(0, populationSize):
        max_fitness_index = np.argmax(combined_population_fitness)
        population[i] = combined_population[max_fitness_index]
        combined_population_fitness[max_fitness_index] = 0

    print("End Generation " + str(generation))
    generation += 1
