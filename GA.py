# change coordinates to an array of tuples instead of just an array
# make a function to get the center point. the center point can spawn anywhere
# the points that spawns outside the picture gets discarded, every shape needs a minimum of 3 points
# define and write the mutation function
# make sure the RGB values doesn't go ovr 255 or under 0
# shape should have the amount of changed pixels and rgb change, mask should have a sum of all shapes
# keep the points relative

import random
from numpy.random import choice
import numpy as np
import mask
import shape


def initPopulation(popSize, maxShapes, shapeSize, maxPoints, imageSize):
    population = []
    for i in range(0, popSize):
        nrOfShapes = random.randint(1, maxShapes)
        shapes = []
        for j in range(0, nrOfShapes):
            # change to passing random amount of points 3 to max
            shapes.append(shape.Shape(random.randint(2, maxPoints)))

        # get the shapes into mask using new function
        population.append(mask.Mask(shapes))

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
    return mask.Mask(child)


# Mutation, when called, will always mutate at least ONE thing and up to five.
def mutation(shape):
    # Decide how many things will be mutated
    numOfMut = random.randint(1, 5)

    numSet = [1, 2, 3, 4, 5]

    # Pull out the things that will be mutated
    choiceSet = choice(numSet, numOfMut, replace=False,
                       p=[0.2, 0.2, 0.2, 0.2, 0.2])  # <-Change probabilities here

    # Moves a point
    if 1 in choiceSet:
        shape.listOfPoints = np.delete(shape.listOfPoints, random.randrange(len(shape.listOfPoints)), 0)
        shape.listOfPoints = np.vstack([shape.listOfPoints, shape.createRandomPoint()])

    # Adding a point
    if 2 in choiceSet:
        shape.listOfPoints = np.vstack([shape.listOfPoints, shape.createRandomPoint()])

    # Removes a point
    if 3 in choiceSet:
        if len(shape.listOfPoints) > 3:
            shape.listOfPoints = np.delete(shape.listOfPoints, random.randrange(len(shape.listOfPoints)), 0)

    # Moves centerpoint within limit.
    if 4 in choiceSet:
        shape.moveShape(30)

    # Mutates RGB-values. Between 1-3 RGB-values will be changed.
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


# takes in the population, how many of the population to enter in the tournament and how many winners to return
def tournament(population, tournamentSize, matingPoolSize):
    matingPool = []
    # fills matingPool until matingPoolSize is reached
    for i in range(0, matingPoolSize):
        # selects as many masks from the population as passed in the argument
        contestants = random.sample(population, tournamentSize)
        best = contestants[0]
        # loop through every contestant and save the best one
        for x in contestants:
            if x.fitness > best.fitness:
                best = x
        matingPool.append(best)
    return matingPool
