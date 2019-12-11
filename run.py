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

original_accuracy = fitnessfunction.fitness_value(inception, original_images, labels)
print("Original Accuracy: " + f"{original_accuracy:e}")

population = GA.initPopulation(populationSize, maxShapes, shapeSize, maxPoints, imageSize)
# population.append(mask.Mask([])) #empty mask breaks calculations

for i in range(0, len(population)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (population[i].getMaskChange(), len(population[i].shapes)))

# getFitnessValues
for i in range(0, len(population)):
    fitness = population[i].calculateFitness(inception, original_images, labels, original_accuracy) #masked images here !CAUTION! This takes very long(the whole reason we use a GA)
    # print("Fitness: %.8f" % fitness)
    print("Fitness: " + f"{fitness:e}")  # <- Prints in scientific notation
    evaluationBudget -= 1

while evaluationBudget > 0:

    new_pop = []
  
    selection = GA.tournament(population, tournamentSize, matingPoolSize)
    for i in range(0, len(selection),2):
        # selection = random.sample(population, 2) # <- Old random selection
        if random.random() < crossoverRate:
            childMask = GA.crossover(selection[i], selection[i+1])
        for shape in childMask.shapes:
            if random.random() < mutationRate:
                GA.mutation(shape)
        new_pop.append(childMask)

    for i in range(0, len(new_pop)):
        print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
               (new_pop[i].getMaskChange(), len(new_pop[i].shapes)))

    for i in range(0, len(new_pop)):
        fitness = new_pop[i].calculateFitness(inception, original_images, labels, original_accuracy) #masked images here
        print("Fitness: " + f"{fitness:e}")  # <- Prints in scientific notation
        evaluationBudget -= 1

    #next generation selection TODO change selection alg
    combined_population = population + new_pop
    combined_population_fitness = np.empty(2*populationSize)
    for i in range(0, populationSize):
        combined_population_fitness[i] = population[i].fitness
    for i in range(0, len(new_pop)):
        combined_population_fitness[i+populationSize] = new_pop[i].fitness
    for i in range(0, populationSize):
        max_fitness_index = np.argmax(combined_population_fitness)
        population[i] = combined_population[max_fitness_index]
        combined_population_fitness[max_fitness_index] = 0