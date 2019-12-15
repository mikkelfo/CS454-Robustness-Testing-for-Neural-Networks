import random
from validity import validate, validate_point, validate_list
from scipy.spatial import Delaunay
from operator import itemgetter


class Shape:
    def __init__(self, k, dim=299):
        assert 2 <= k <= 9
        assert dim > 0
        self.dim = dim                              # Given
        self.centerPoint = self.init_center()        # Random initialization
        self.listOfPoints = self.init_points(k)      # Random initialization
        self.changeRGB = self.init_RGB()             # Random initialization

        # Below values are set to None, so our program cant run, e.g. call Shape.area, before Shape.update() is called
        self.insidePoints = None                    # Calculation
        self.area = None                            # Calculation
        self.change = None                          # Calculation

        # call update
        self.update()

    def init_center(self):
        x, y = random.randrange(0, self.dim), random.randrange(0, self.dim)
        return x, y

    def init_points(self, k, diff=30):
        r = random.randint(2, k)
        points = [self.centerPoint]

        # Creates {r} random points
        for _ in range(r):
            points.append(self.create_random_point(diff))

        # If invalid points, recursively try again
        if not validate(points):
            return self.init_points(k, diff)

        return points

    def create_random_point(self, diff=30):
        xCenter, yCenter = self.centerPoint
        xRange, yRange = [xCenter - diff, xCenter +
                          diff], [yCenter - diff, yCenter + diff]

        # Picks x, y based on centerPoint +- {diff}
        x, y = random.randint(xRange[0], xRange[1]), random.randint(
            yRange[0], yRange[1])

        # If invalid point (out of range), recursively try again
        if not validate_point((x, y)):
            return self.create_random_point(diff)

        return x, y

    @staticmethod
    def init_RGB():
        return random.sample(range(-255, 255), 3)

    def get_inside_points(self):
        def _in_hull(p):
            return hull.find_simplex(p) >= 0

        # Finds the bounding box of listOfPoints
        points = self.listOfPoints
        min_x, max_x = min(points, key=itemgetter(0))[0], \
            max(points, key=itemgetter(0))[0]
        min_y, max_y = min(points, key=itemgetter(1))[1], \
            max(points, key=itemgetter(1))[1]

        # Finds points inside ConvexHull
        hull = Delaunay(points)
        points = []
        for x in range(min_x - 1, max_x + 1):
            for y in range(min_y - 1, max_y + 1):
                t = (x, y)
                if _in_hull(t):
                    points.append(t)

        return points

    def update(self):
        self.insidePoints = self.get_inside_points()
        self.area = len(self.insidePoints)
        self.change = self.area * sum([abs(val) for val in self.changeRGB])

    # Moves the shape to random place within the specified limit
    def move_shape(self, limit=30):
        xShift = random.randint(-limit, limit)
        yShift = random.randint(-limit, limit)

        evaluationList = [(x + xShift, y + yShift)
                          for (x, y) in self.listOfPoints]
        evaluationCenter = (
            self.centerPoint[0] + xShift, self.centerPoint[1] + yShift)

        # Checks if new points are within the picture
        if not validate_list(evaluationList):
            return self.move_shape(limit)

        self.centerPoint = evaluationCenter
        self.listOfPoints = evaluationList

    # Create new random point and adds it to shape
    def add_point(self):
        self.listOfPoints.append(self.create_random_point())

    # Removes point IFF it doesn't invalidate the shape
    def remove_point(self):
        newList = self._remove_point()
        if validate(newList):
            self.listOfPoints = newList

    # Moves point IFF it doesn't invalidate the shape
    def move_point(self):
        newList = self._remove_point()
        newList.append(self.create_random_point())
        if validate(newList):
            self.listOfPoints = newList

    # Helper function for remove_point()
    def _remove_point(self):
        newList = self.listOfPoints.copy()
        randIndex = random.randrange(1, len(newList))
        del newList[randIndex]

        return newList
