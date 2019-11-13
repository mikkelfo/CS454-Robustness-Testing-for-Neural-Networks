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
    single_img_reshaped = np.transpose(np.reshape(single_img, (3, 32, 32)), (1, 2, 0))
    return single_img_reshaped

def show_img(img):
    Image.fromarray(img, 'RGB').show()


batch = load_data("data_batch_1")

image = get_img(batch, 1)

show_img(image)

