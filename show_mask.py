import matplotlib.pyplot as plt
import pickle
from mask import Mask
import fitnessfunction
import edit_images as editor
import copy
import numpy as np


#read population
read = open('pareto_pop', 'rb')
population = pickle.load(read)
read.close()

#load model, images, label
inception = fitnessfunction.load_model()
original_images = fitnessfunction.get_images()
labels = fitnessfunction.get_labels()

img_number = 0
number_of_images = 1000

#get original stats
processed_images = np.zeros((number_of_images, 299, 299, 3))
for i in range(number_of_images):
    processed_image = fitnessfunction.preprocess_for_eval(original_images[i])
    processed_images[i] = processed_image
classes = inception.predict(processed_images)
class_numbers = np.argmax(classes, 1)
print ("Original class: " + str(labels[img_number]))
print ("Original predicted class: " + str(class_numbers[img_number]))
picture = original_images[img_number]
#plt.imshow(picture.astype(int))
#plt.show()

#show different masks on specified image
masked_images = np.zeros((len(population), 299, 299, 3))
for i in range(len(population)):
    masked = editor.apply_mask(copy.deepcopy(original_images), population[i])
    processed_image = fitnessfunction.preprocess_for_eval(masked[img_number])
    masked_images[i] = processed_image
    print("Image number: " + str(i))
    masked_picture = masked[img_number]
    plt.imshow(masked_picture.astype(int))
    plt.show()
#all predicted classes of the masks fot that image
classes = inception.predict(masked_images)
class_numbers = np.argmax(classes, 1)
print ("Masked classes: ")
print(class_numbers)