import pickle
import numpy as np
from PIL import Image


def load_data(file, path='cifar-10-batches-py/'):
    with open(path + file, 'rb') as fo:
        dic = pickle.load(fo, encoding='bytes')
    return dic


def get_img(file, i):
    images = file[b'data']
    single_img = np.array(images[i])
    single_img_reshaped = np.transpose(
        np.reshape(single_img, (3, 32, 32)), (1, 2, 0))
    return single_img_reshaped


def show_img(img):
    Image.fromarray(img, 'RGB').show()


def apply_mask(img, inside_points, mask):
    for x, y in inside_points:
        img[y][x] = boundary(img[y][x] + mask)

    return img


def boundary(pixels):
    new_array = []
    for val in pixels:
        if val not in range(0, 255):
            if val < 0:
                val = 0
            elif val > 255:
                val = 255
        new_array.append(val)
    return new_array
