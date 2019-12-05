import random
import numpy as np

from scipy.spatial import Delaunay
from operator import itemgetter


class Shape:
    def __init__(self, k, dim=299):
        assert dim > 0
        self.dim = dim
        # If changing centerPoint, we also need to change listOfPoints
        self.centerPoint = self.initCenter()
        self.listOfPoints = np.array(self.initPoints(k))
        self.changeRGB = self.initRGB()
        self.area = self.area()
        self.change = self.shapeChange(self.changeRGB, self.area)

    def initCenter(self):
        x, y = random.randint(0, self.dim), random.randint(0, self.dim)
        return x, y

    def initPoints(self, k, diff=10):
        assert 2 <= k <= 9
        r = random.randint(2, k)

        points = [self.centerPoint]
        for _ in range(r):
            points.append(self.createRandomPoint(diff))

        try:
            Delaunay(points)
        except:
            return self.initPoints(k, diff)

        return points

    def createRandomPoint(self, diff=30):
        xc, yc = self.centerPoint
        xr, yr = [xc - diff, xc + diff], [yc - diff, yc + diff]

        x, y = random.choice(range(xr[0], xr[1])), random.choice(
            range(yr[0], yr[1]))

        if x not in range(0, self.dim) or y not in range(0, self.dim):
            return self.createRandomPoint(diff)

        return x, y

    @staticmethod
    def initRGB():
        return random.sample(range(-255, 255), 3)

    def area(self):
        return self.getInsidePoints()

    def getInsidePoints(self):
        def in_hull(p):
            return hull.find_simplex(p) >= 0
        points = self.listOfPoints
        min_x, max_x = min(points, key=itemgetter(0))[
            0], max(points, key=itemgetter(0))[0]
        min_y, max_y = min(points, key=itemgetter(1))[
            1], max(points, key=itemgetter(1))[1]

        hull = Delaunay(points)
        points = []
        for x in range(min_x - 1, max_x + 1):
            for y in range(min_y - 1, max_y + 1):
                t = (x, y)
                if in_hull(t):
                    points.append(t)
        return len(points)

    # Calculates shape change for fitness
    def shapeChange(self, changeRGB, area):
        absChange = 0
        for i in changeRGB:
            absChange += abs(i)
        return area + absChange

    # Gets the change value from the shape
    def getShapeChange(self):
        self.change = self.shapeChange(self.changeRGB, self.area)
        return self.change

    # Moves the shape to random place within the specified limit
    def moveShape(self, limit):
        xShift = random.randint(-limit, limit)
        yShift = random.randint(-limit, limit)

        evaluationList = self.listOfPoints + (xShift, yShift)
        evaluationCenter = (self.centerPoint[0] + xShift, self.centerPoint[1] + yShift)

        # Checks if new points are within the picture
        if evaluationList.max() not in range(0, self.dim) or evaluationList.min() not in range(0, self.dim):
            return self.moveShape(limit)

        if evaluationCenter[0] not in range(0, self.dim) or evaluationCenter[1] not in range(0, self.dim):
            return self.moveShape(limit)

        self.centerPoint = (self.centerPoint[0] + xShift, self.centerPoint[1] + yShift)
        self.listOfPoints += (xShift, yShift)
