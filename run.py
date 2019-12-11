import GA
import fitnessfunction
import mask
import random

populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 299
mutationRate = 0.02
evaluationBudget = 10000
download = False

tournamentSize = 4
matingPoolSize = 2

if (download):
    fitnessfunction.download_base_model()

inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()
labels = fitnessfunction.get_labels()

original_accuracy = fitnessfunction.fitness_value(inception, original_images, labels)
print(original_fitness)

population = GA.initPopulation(populationSize, maxShapes, shapeSize, maxPoints, imageSize)
#population.append(mask.Mask([]))

for i in range(0, len(population)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (population[i].getMaskChange(), len(population[i].shapes)))

#getFitnessValues
for i in range(0, len(population)):
    fitness = population[i].calculateFitness(inception, original_images, labels, original_accuracy) #masked images here !CAUTION! This takes very long(the whole reason we use a GA)
    print (fitness)
    evaluationBudget -= 1

new_pop = []
for i in population:
    #GA.tournament(population, tournamentSize, matingPoolSize)
    selection = random.sample(population, 2)
    childMask = GA.crossover(selection[0], selection[1])
    for shape in childMask.shapes:
        if random.random() < mutationRate:
            GA.mutation(shape)

    new_pop.append(childMask)

for i in range(0, len(new_pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (new_pop[i].getMaskChange(), len(new_pop[i].shapes)))