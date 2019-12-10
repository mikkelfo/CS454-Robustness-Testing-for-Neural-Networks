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
from mask import Mask
from shape import Shape


def initPopulation(popSize, maxShapes, shapeSize, maxPoints, imageSize):
    population = []

    # Generates population
    for _ in range(popSize):
        shapes = []
        nrOfShapes = random.randint(1, maxShapes)

        # Generates shapes for Mask
        for _ in range(nrOfShapes):
            nrOfPoints = random.randint(2, maxPoints)
            shape = Shape(nrOfPoints)
            shapes.append(shape)

        # Makes individual and adds to population
        indv = Mask(shapes)
        population.append(indv)

    return population

# Picks n, m of parents' shapes to pass to child
def crossover(parent1, parent2):
    # Number of shapes from parents
    n = random.randint(1, len(parent1.shapes))
    m = random.randint(1, len(parent2.shapes))

    # Adds parent genes to child
    child = []
    child += random.sample(parent1.shapes, n)
    child += random.sample(parent2.shapes, m)

    return Mask(child)


# Mutation, when called, will always mutate at least ONE thing and up to five.
def mutation(shape, prob=None):
    if prob is None:
        prob = [0.2, 0.2, 0.2, 0.2, 0.2]

    numOfMut = random.randint(1, 5)
    numOptions = [1, 2, 3, 4, 5]

    # Randomly chooses {numOfMut} amount of mutation operations
    choiceSet = choice(numOptions, numOfMut, replace=False, p=prob)  # <-Change probabilities here

    # Adds a point
    if 1 in choiceSet:
        shape.add_point()

    # Removes a point
    if 2 in choiceSet:
        shape.remove_point()

    # Moves a point
    if 3 in choiceSet:
        shape.move_point()

    # Moves entire shape
    if 4 in choiceSet:
        shape.moveShape()

    # Mutates RGB-values. Between 1-3 RGB-values will be changed.
    if 5 in choiceSet:
        numRGBSet = {1, 2, 3}
        numOfRGBMut = random.randint(1, 3)
        RGBRange = 20
        RBGToChangeSet = random.sample(numRGBSet, numOfRGBMut)

        # Mutate R
        if 1 in RBGToChangeSet:
            shape.changeRGB[0] = _legalRGBValue(shape.changeRGB[0], RGBRange)

        # Mutate G
        if 2 in RBGToChangeSet:
            shape.changeRGB[1] = _legalRGBValue(shape.changeRGB[1], RGBRange)

        # Mutate B
        if 3 in RBGToChangeSet:
            shape.changeRGB[2] = _legalRGBValue(shape.changeRGB[2], RGBRange)


# Returns a RGB value that is within the given range. If RGB is close to min or max, the function
# will dynamically adjust. Example if value is 253 and range is 20, the function will pick random number between
# [-18, 2] as to not go out of bounds.
def _legalRGBValue(RGBValue, RGBRange):
    rDiffFromMax = abs(RGBValue - 255)
    rDiffFromMin = RGBValue  # TODO: Changed this from      rDiffFromMin = abs(RGBValue + 255) - 255
    smallestDiff = min(rDiffFromMax, rDiffFromMin)

    if smallestDiff >= RGBRange / 2:
        RGBValue += random.randint(-RGBRange / 2, RGBRange / 2)
    elif rDiffFromMax < RGBRange / 2:
        RGBValue += random.randint((-RGBRange / 2) - ((RGBRange / 2) - rDiffFromMax), rDiffFromMax)
    elif rDiffFromMin < RGBRange / 2:
        RGBValue += random.randint(-rDiffFromMin, (RGBRange / 2) + ((RGBRange / 2) - rDiffFromMin))

    return RGBValue


# takes in the population, how many of the population to enter in the tournament and how many winners to return
def tournament(population, tournamentSize, matingPoolSize):
    matingPool = []

    # fills matingPool until matingPoolSize is reached
    for _ in range(matingPoolSize):

        contestants = random.sample(population, tournamentSize)
        best = contestants[0]

        # TODO: This needs fixing. What's the purpose of 'x not in matingPool'. We could end up with only 1 individual
        # loop through every contestant and save the best one
        for x in contestants:
            if x.fitness > best.fitness and x not in matingPool:
                best = x
        matingPool.append(best)
    return matingPool
