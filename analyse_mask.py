import matplotlib.pyplot as plt
import pickle
from mask import Mask
import fitnessfunction
import edit_images as editor
import copy
import numpy as np

read = open('pareto_pop', 'rb')
population = pickle.load(read)
read.close()

inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()
labels = fitnessfunction.get_labels()

number_of_images = 1000
mask_analysis = 18

processed_images = np.zeros((number_of_images, 299, 299, 3))
for i in range(number_of_images):
    processed_image = fitnessfunction.preprocess_for_eval(original_images[i])
    processed_images[i] = processed_image
classes = inception.predict(processed_images)
class_numbers = np.argmax(classes, 1)

masked = editor.apply_mask(copy.deepcopy(original_images), population[mask_analysis])
print(population[mask_analysis].accuracy)
print(population[mask_analysis].change)

processed_images = np.zeros((number_of_images, 299, 299, 3))
for i in range(number_of_images):
    processed_image = fitnessfunction.preprocess_for_eval(masked[i])
    processed_images[i] = processed_image
masked_classes = inception.predict(processed_images)
masked_class_numbers = np.argmax(masked_classes, 1)

for i in range(number_of_images):
    if (class_numbers[i] != labels[i]):
        continue
    if (class_numbers[i] != masked_class_numbers[i]):
        picture = original_images[i]
        masked_picture = masked[i]
        print(class_numbers[i])
        print(masked_class_numbers[i])
        plt.imshow(masked_picture.astype(int))
        plt.show()