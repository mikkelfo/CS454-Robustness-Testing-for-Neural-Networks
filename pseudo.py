import random
from scipy.spatial import ConvexHull, Delaunay

from operator import itemgetter
def createRandomPoint():
    return

class Mask:
    def __init__(self):
        self.listOfShapes = self.initShapes()
        fitness = 0
        self.accuracy = 0

    @staticmethod
    def initShapes():
        return []

    def calculateFitness(self):
        for shape in self.listOfShapes:
            fitness = len(shape.area) + sum([abs(x) for x in shape.changeRGB]) + self.accuracy
        return

class Shape:
    def __init__(self, k):
        self.centerPoint = (0, 0)
        self.listOfPoints = self.initPoints(k)
        self.changeRGB = self.initRGB()
        self.area = self.area()

    @staticmethod
    def initPoints(k):
        assert 3 <= k <= 10
        r = random.randint(3, k)

        points = []
        for _ in range(r):
            points.append(createRandomPoint())

        assert(len(points) >= 3)

        return points

    @staticmethod
    def initRGB():
        return random.sample(range(-255, 255), 3)

    def area(self):
        return self.get_inside_points()

    def get_inside_points(self):
        def in_hull(hull, p):
            return hull.find_simplex(p) >= 0

        points = self.listOfPoints
        min_x, max_x = min(points, key=itemgetter(0))[0], max(points, key=itemgetter(0))[0]
        min_y, max_y = min(points, key=itemgetter(1))[1], max(points, key=itemgetter(1))[1]

        hull = Delaunay(points)
        points = []
        for x in range(min_x - 1, max_x + 1):
            for y in range(min_y - 1, max_y + 1):
                t = (x, y)
                if in_hull(hull, t):
                    points.append(t)
        return points
