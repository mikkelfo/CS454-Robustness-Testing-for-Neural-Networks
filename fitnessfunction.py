import numpy as np
import os
import tensorflow as tf
from tensorflow import keras


def download_base_model():
    if not os.path.isdir('neuralNetwork'):
        os.mkdir('neuralNetwork')
    save_dir = os.path.join(os.getcwd(), 'neuralNetwork')
    model_name = 'inceptionv3_base_model.hdf5'
    base_model = tf.keras.applications.InceptionV3(
        include_top=True, weights='imagenet')
    model_path = os.path.join(save_dir, model_name)
    base_model.save(model_path)
    print("Model downloaded!")


def preprocess_for_eval(image):
    image /= 255.
    image -= 0.5
    image *= 2.
    return image


def get_accuracy(val_labels, class_numbers):
    number_of_images = val_labels.size
    number_of_correct = 0
    for i in range(number_of_images):
        if val_labels[i] == class_numbers[i]:
            number_of_correct += 1
    accuracy = number_of_correct / number_of_images
    return accuracy


def get_images():
    number_of_images = 1000

    # get images from folder
    datagen = keras.preprocessing.image.ImageDataGenerator()
    image_generator = datagen.flow_from_directory(
        'imagenet',
        color_mode='rgb',
        target_size=(299, 299),
        shuffle=False,
        batch_size=number_of_images,
        class_mode=None)

    images = image_generator.next()
    return images


def load_model():
    inception = keras.models.load_model(
        'neuralNetwork/inceptionv3_base_model.hdf5', compile=False)
    return inception


def get_labels():
    number_of_images = 1000
    # read labels from file
    with open('val.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    string_array = content[0:number_of_images]
    val_labels_list = [int(i) for i in string_array]
    val_labels = np.asarray(val_labels_list)
    return val_labels


def fitness_value(inception_model, masked_images, labels):
    number_of_images = 1000
    val_labels = labels

    # preprocess images
    processed_images = np.empty((number_of_images, 299, 299, 3))
    for i in range(number_of_images):
        processed_image = preprocess_for_eval(masked_images[i])
        processed_images[i] = processed_image

    # classify
    classes = inception_model.predict(processed_images)
    class_numbers = np.argmax(classes, 1)
    accuracy = get_accuracy(val_labels, class_numbers)
    return accuracy
