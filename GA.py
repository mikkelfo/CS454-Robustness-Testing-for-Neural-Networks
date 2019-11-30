# change coordinates to an array of tuples instead of just an array
# make a function to get the center point. the center point can spawn anywhere
# the points that spawns outside the picture gets discarded, every shape needs a minimum of 3 points
# define and write the mutation function
# make sure the RGB values doesn't go ovr 255 or under 0
# shape should have the amount of changed pixels and rgb change, mask should have a sum of all shapes
# keep the points relative

import random

from mask import *


def initPopulation(popSize, maxShapes, shapeSize, maxPoints, imageSize):
    population = []
    for i in range(0, popSize):
        nrOfShapes = random.randint(1, maxShapes)
        shapes = []
        for j in range(0, nrOfShapes):
            # change to passing random amount of points 3 to max
            shapes.append(Shape(random.randint(3, maxPoints)))

        # get the shapes into mask using new function
        population.append(Mask(shapes))

    return population


def crossover(parent1, parent2):
    nr1 = random.randint(1, len(parent1.shapes))
    nr2 = random.randint(1, len(parent2.shapes))

    child = []
    temp1 = random.sample(parent1.shapes, nr1)
    for i in temp1:
        child.append(i)
    temp2 = random.sample(parent2.shapes, nr2)
    for i in temp2:
        child.append(i)

    # get children shapes into mask
    return Mask(child)


def mutation(mutationrate):
    changeShape = False
    changeCenpoint = False
    changeRGB = False

    # Decide how many things will be mutated
    numOfMut = random.randint(1, 3)

    num_set = {1, 2, 3}

    # Pull out the things that will be mutated and set their value to 'True'
    choice_set = random.sample(num_set, numOfMut)

    if 1 in choice_set:
        changeShape = True
    if 2 in choice_set:
        changeCenpoint = True
    if 3 in choice_set:
        changeRGB = True


#   we can mutate center position, shape and rgb values. one or all three can be mutated.
#   centerpoint is mutated by randomising a new point
#   shape is mutated by either removing or adding x points (and moving?)
#   rgb values can either decrease or increase with value y. all or only one value can be changed. (roll to see how many values, then again to see which values)


populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 256

# mutation(2)

pop = initPopulation(populationSize, maxShapes,
                     shapeSize, maxPoints, imageSize)

for i in range(0, len(pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (pop[i].getMaskChange(), len(pop[i].shapes)))

new_pop = []
for i in pop:
    selection = random.sample(pop, 2)
    new_pop.append(crossover(selection[0], selection[1]))

for i in range(0, len(new_pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (new_pop[i].getMaskChange(), len(new_pop[i].shapes)))