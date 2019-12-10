import fitnessfunction


class Mask:
    def __init__(self, shapes):
        self.shapes = shapes
        self.accuracy = 0
        self.change = self.maskChange()
        self.fitness = 0

    def calculateFitness(self, inception_model, masked_images):
        self.accuracy = fitnessfunction.fitness_value(inception_model, masked_images)
        return self.accuracy / self.change

    def maskChange(self):
        return sum([shape.getShapeChange() for shape in self.shapes])

    def updateMaskChange(self):
        self.change = self.maskChange()
