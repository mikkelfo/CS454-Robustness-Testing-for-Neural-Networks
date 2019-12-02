# change coordinates to an array of tuples instead of just an array
# make a function to get the center point. the center point can spawn anywhere
# the points that spawns outside the picture gets discarded, every shape needs a minimum of 3 points
# define and write the mutation function
# make sure the RGB values doesn't go ovr 255 or under 0
# shape should have the amount of changed pixels and rgb change, mask should have a sum of all shapes
# keep the points relative

import random
from numpy.random import choice

from mask import *


def initPopulation(popSize, maxShapes, shapeSize, maxPoints, imageSize):
    population = []
    for i in range(0, popSize):
        nrOfShapes = random.randint(1, maxShapes)
        shapes = []
        for j in range(0, nrOfShapes):
            # change to passing random amount of points 3 to max
            shapes.append(Shape(random.randint(2, maxPoints)))

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


# Mutation, when called, will always mutate at least ONE thing and up to five.
def mutation(shape):
    # Decide how many things will be mutated
    numOfMut = random.randint(1, 1)

    numSet = [1, 2, 3, 4, 5]

    # Pull out the things that will be mutated
    choiceSet = choice(numSet, numOfMut, replace=False,
                       p=[0, 0, 0, 1, 0])  # <-Change probabilities here

    # Mutate shape by moving a point
    if 1 in choiceSet:
        shape.listOfPoints.pop(random.randrange(len(shape.listOfPoints)))
        shape.listOfPoints.append(shape.createRandomPoint())

    # Mutate shape by adding a point
    if 2 in choiceSet:
        shape.listOfPoints.append(shape.createRandomPoint())

    # Mutate shape by removing a point
    if 3 in choiceSet:
        shape.listOfPoints.pop(random.randrange(len(shape.listOfPoints)))

    # Mutate shape position by moving centerpoint. Change to numpy array and add shift value. Move centerpoint by +-10
    if 4 in choiceSet:
        shape.moveShape(30)

    # Mutate RGB-values. Between 1-3 RGB-values will be changed.
    if 5 in choiceSet:
        numRGBSet = {1, 2, 3}
        numOfRGBMut = random.randint(1, 3)
        RGBRange = 20
        RBGToChangeSet = random.sample(numRGBSet, numOfRGBMut)

        # Mutate R
        if 1 in RBGToChangeSet:
            shape.changeRGB[0] = legalRGBValue(shape.changeRGB[0], RGBRange)

        # Mutate G
        if 2 in RBGToChangeSet:
            shape.changeRGB[1] = legalRGBValue(shape.changeRGB[1], RGBRange)

        # Mutate B
        if 3 in RBGToChangeSet:
            shape.changeRGB[2] = legalRGBValue(shape.changeRGB[2], RGBRange)


# Returns a RGB value that is within the given range. If RGB is close to min or max, the function
# will dynamically adjust. Example if value is 253 and range is 20, the function will pick random number between
# [-18, 2] as to not go out of bounds.
def legalRGBValue(RGBValue, RGBRange):
    rDiffFromMax = abs(RGBValue - 255)
    rDiffFromMin = abs(RGBValue + 255) - 255
    smallestDiff = min(rDiffFromMax, rDiffFromMin)

    if smallestDiff >= RGBRange / 2:
        RGBValue += random.randint(-RGBRange / 2, RGBRange / 2)
    elif rDiffFromMax < RGBRange / 2:
        RGBValue += random.randint((-RGBRange / 2) - ((RGBRange/2) - rDiffFromMax), rDiffFromMax)
    elif rDiffFromMin < RGBRange / 2:
        RGBValue += random.randint(-rDiffFromMin, (RGBRange / 2) + ((RGBRange/2) - rDiffFromMin))

    return RGBValue


#   we can mutate center position, shape and rgb values. one or all three can be mutated.
#   centerpoint is mutated by randomising a new point
#   shape is mutated by either removing or adding x points (and moving?)
#   rgb values can either decrease or increase with value y. all or only one value can be changed. (roll to see how many values, then again to see which values)


populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 256
mutationRate = 0.02

pop = initPopulation(populationSize, maxShapes,
                     shapeSize, maxPoints, imageSize)

for i in range(0, len(pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (pop[i].getMaskChange(), len(pop[i].shapes)))

new_pop = []
for i in pop:
    selection = random.sample(pop, 2)
    childMask = crossover(selection[0], selection[1])
    for shape in childMask.shapes:
        if random.random() < mutationRate:
            mutation(shape)

    new_pop.append(childMask)

for i in range(0, len(new_pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %
          (new_pop[i].getMaskChange(), len(new_pop[i].shapes)))
