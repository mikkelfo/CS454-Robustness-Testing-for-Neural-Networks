import random
from scipy.spatial import Delaunay

from operator import itemgetter


class Mask:
    def __init__(self, shapes):
        self.shapes = shapes
        fitness = 0
        self.accuracy = 0
        # use self.shapes or shapes?
        self.change = self.maskChange(shapes)

    # def calculateFitness(self, c1, c2, c3):
    #     for shape in self.listOfShapes:
    #         area = len(shape.area)
    #         rgb = len(shape.area) + sum([abs(x) for x in shape.changeRGB])
    #         acc = self.accuracy
    #         fitness = c1 * area + c2 * rgb + c3 * acc
    #     return fitness

    def maskChange(self, shapes):
        value = 0
        for i in shapes:
            value += i.getShapeChange()
        return value

    def getMaskChange(self):
        self.change = self.maskChange(self.shapes)
        return self.change


class Shape:
    def __init__(self, k, dim=96):
        assert dim > 0
        self.dim = dim
        # If changing centerPoint, we also need to change listOfPoints
        self.centerPoint = self.initCenter()
        self.listOfPoints = self.initPoints(k)
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
        except ValueError():
            return k.initPoints(k, diff)

        return points

    def createRandomPoint(self, diff=10):
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

    def shapeChange(self, changeRGB, area):
        absChange = 0
        for i in changeRGB:
            absChange += abs(i)
        return area + absChange

    def getShapeChange(self):
        self.change = self.shapeChange(self.changeRGB, self.area)
        return self.change
