import GA
import fitnessfunction
import mask
import random

populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 256
mutationRate = 0.02
evaluationBudget = 10000
download = False

if (download):
    fitnessfunction.download_base_model()

inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()

pop = GA.initPopulation(populationSize, maxShapes,
                     shapeSize, maxPoints, imageSize)

for i in range(0, len(pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (pop[i].getMaskChange(), len(pop[i].shapes)))

new_pop = []
for i in pop:
    selection = random.sample(pop, 2)
    childMask = GA.crossover(selection[0], selection[1])
    for shape in childMask.shapes:
        if random.random() < mutationRate:
            GA.mutation(shape)

    new_pop.append(childMask)

for i in range(0, len(new_pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (new_pop[i].getMaskChange(), len(new_pop[i].shapes)))