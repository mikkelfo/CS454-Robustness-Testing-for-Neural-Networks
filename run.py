import GA
import fitnessfunction
import edit_images as editor
import random
import numpy as np
import timeit

populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 299
crossoverRate = 0.9
mutationRate = 0.05
evaluationBudget = 20
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
    print("running update: " + str(i))
    start = timeit.default_timer()
    population[i].update(inception, editor.apply_mask(
        original_images, population[i]), labels, original_accuracy)
    stop = timeit.default_timer()
    print("Fitness: " + f"{population[i].fitness:e}")  # <- sci-notation
    print("time to run update: ", stop - start)
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (population[i].change, len(population[i].shapes)))
    evaluationBudget -= 1

    generation = 0
while evaluationBudget > 0:
    print("\nGeneration: " + str(generation))
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
        print("running update: " + str(i))
        start = timeit.default_timer()
        new_pop[i].update(inception, editor.apply_mask(
            original_images, new_pop[i]), labels, original_accuracy)
        stop = timeit.default_timer()
        print("Fitness: " + f"{new_pop[i].fitness:e}")  # <- sci-notation
        print("time to run update: ", stop - start)
        print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
              (new_pop[i].change, len(new_pop[i].shapes)))
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
