import fitnessfunction
import random
from shape import Shape


class Mask:
    #initialize mask(list of shapes), update has to be called for accuracy and change
    def __init__(self, shapes=None, maxShapes=40, maxPoints=9):
        if shapes is None:
            self.shapes = self.init_shapes(maxShapes, maxPoints) # Initialization
        else:
            self.shapes = shapes                # Set value

        # Below values are set to None, Mask.update() has to be called to use them
        self.accuracy = None                    # Calculated
        self.change = None                      # Calculated
        self.fitness = None                     # Calculated, not used but can maybe be used for further research

    #fitness value for the amount of change(sum of change of all shapes)
    def mask_change(self):
        return sum([shape.change for shape in self.shapes])

    #calculate accuracy and update attributes
    def update(self, inception_model, masked_images, labels, original_accuracy):
        self.accuracy = fitnessfunction.fitness_value(
            inception_model, masked_images, labels)
        self.change = self.mask_change()
        self.fitness = (original_accuracy - self.accuracy) / self.change

    #initialize a random number of shapes with random amount of points
    @staticmethod
    def init_shapes(maxShapes=40, maxPoints=9):
        nrOfShapes = random.randint(1, maxShapes)
        return [Shape(random.randint(2, maxPoints)) for _ in range(nrOfShapes)]
