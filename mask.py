import fitnessfunction
import random
from shape import Shape


class Mask:
    def __init__(self, shapes=None):
        if shapes is None:
            self.shapes = self.init_shapes()    # Initialization
        else:
            self.shapes = shapes                # Set value

        # Below values are set to None, so our program cant run, e.g. call Mask.fitness, before Mask.update() is called
        self.accuracy = None                    # Calculated
        self.change = None                      # Calculated
        self.fitness = None                     # Calculated

    def mask_change(self):
        return sum([shape.change for shape in self.shapes])

    def update(self, inception_model, masked_images, labels, original_accuracy):
        self.accuracy = fitnessfunction.fitness_value(
            inception_model, masked_images, labels)
        print(self.accuracy)
        self.change = self.mask_change()
        self.fitness = (original_accuracy - self.accuracy) / self.change

    @staticmethod
    def init_shapes(maxShapes=25, maxPoints=9):
        nrOfShapes = random.randint(1, maxShapes)
        return [Shape(random.randint(2, maxPoints)) for _ in range(nrOfShapes)]
