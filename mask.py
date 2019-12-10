import fitnessfunction

class Mask:
    # BIG PROBLEM
    #fitness_value takes in 3 parameters
    def __init__(self, shapes):
        self.shapes = shapes
        self.accuracy = 0
        self.change = self.maskChange(shapes)
        self.fitness = 0
        
    def calculateFitness(self, inception_model, masked_images, labels):
        self.accuracy = fitnessfunction.fitness_value(inception_model, masked_images, labels)
        self.fitness = self.accuracy/self.change
        return self.accuracy/self.change

    def maskChange(self, shapes):
        value = 0
        for i in shapes:
            value += i.getShapeChange()
        return value

    def getMaskChange(self):
        self.change = self.maskChange(self.shapes)
        return self.change


