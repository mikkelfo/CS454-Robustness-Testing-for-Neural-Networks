# change coordinates to an array of tuples instead of just an array
# make a function to get the center point. make sure the shape can't go out of bounds
# define and write the mutation function
# make sure the RGB values doesn't go ovr 255 or under 0
# shape should only have the RGB values changed and mask should have amount of pixels changed
# changed the point to be absolute instead of relative

import numpy as np
import random

class mask:
    def __init__(self, shapes=[]):
        self.shapes = shapes
        self.change = 0
        self.accuracy = 0
        
    def getMaskChange(self):
        value = 0
        for i in self.shapes:
            value += i.change
        self.change = value
        return self.change
    
    
class shape:
    def __init__(self, center=[], points=[], RGBValues=[]):
        self.center = center
        self.points = points
        self.RGBValues = RGBValues
        self.change = 0
        
    #This needs to be replaced or we need to sort the points
    def polygonArea(self):
        x = self.points[0::2]
        y = self.points[1::2]
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

    def getShapeChange(self):
        rgbChange = 0
        for i in self.RGBValues:
            rgbChange += abs(i)
        self.change= self.polygonArea() + rgbChange
        return self.change

def getRandomPoints(size, maxPoints):
    if size % 2 != 0:
        size -= 1
    nrOfPoints = random.randint(3,maxPoints)
    points = []
    for i in range(0, nrOfPoints):
        x = random.randint(-size/2,(size/2))
        y = random.randint(-size/2,(size/2))        
        points.append(x)
        points.append(y)
    return points
    
def getRandomRGBValues():
    rgb = []
    rgb.append(random.uniform(-255.0,255.0))
    rgb.append(random.uniform(-255.0,255.0))
    rgb.append(random.uniform(-255.0,255.0))
    return rgb

def initPopulation(popSize, maxShapes, shapeSize, maxPoints, imageSize):
    population = []
    for i in range(0, popSize):
        nrOfShapes = random.randint(1, maxShapes)
        shapes = []
        for j in range(0, nrOfShapes):
            points = getRandomPoints(shapeSize, maxPoints)
            rgb = getRandomRGBValues()
            center = []
            center.append(random.randint(0,imageSize))
            center.append(random.randint(0,imageSize))
            tempShape = shape(center, points, rgb)
            tempShape.getShapeChange()
            shapes.append(tempShape)
    
        tempMask = mask(shapes)
        tempMask.getMaskChange()
        population.append(tempMask)

    return population

def crossover(parent1, parent2):
    nr1 = random.randint(1,len(parent1.shapes))
    nr2 = random.randint(1,len(parent2.shapes))
    
    child = []
    temp1 = random.sample(parent1.shapes, nr1)
    for i in temp1:
        child.append(i)
    temp2 = random.sample(parent2.shapes, nr2)
    for i in temp2:
        child.append(i)
    child = mask(child)
    return child

#def mutation(mutationrate):
#   we can mutate center position, shape and rgb values. one or all three can be mutated.
#   centerpoint is mutated by randomising a new point
#   shape is mutated by either removing or adding x points
#   rgb values can either decrease or increase with value y. all or only one value can be changed. (roll to see how many values, then again to see which values)

populationSize = 10
maxShapes = 20
shapeSize = 25
maxPoints = 8
imageSize = 256

pop = initPopulation(populationSize, maxShapes, shapeSize, maxPoints, imageSize)
for i in range(0,len(pop)):
    print("Change of the mask: %8.3f Number of shapes in the mask: %d" %(pop[i].change, len(pop[i].shapes)))

