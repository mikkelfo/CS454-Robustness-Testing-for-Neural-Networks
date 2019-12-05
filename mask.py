import fitnessfunction as fitAcc

class Mask:
    def __init__(self, shapes):
        self.shapes = shapes
        self.fitness = self.calculateFitness(1,1)
        self.accuracy = fitAcc.fitness_value()
        self.change = self.maskChange(shapes)

    def calculateFitness(self, c1, c2):
        fitness = 0
        for shape in self.shapes:
            change = self.change
            acc = self.accuracy
            fitness += c1 * change + c2 * acc
        return fitness

    def maskChange(self, shapes):
        value = 0
        for i in shapes:
            value += i.getShapeChange()
        return value

    def getMaskChange(self):
        self.change = self.maskChange(self.shapes)
        return self.change


