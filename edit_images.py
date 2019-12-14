import numpy as np
import timeit


def apply_mask(images, mask):

    # Constructs Mask matrix
    start = timeit.default_timer()
    matrix = np.zeros((299, 299, 3))
    for shape in mask.shapes:
        change = shape.changeRGB
        for (x, y) in shape.insidePoints:
            matrix[y][x] += change

    # Applies mask to the images
    for i in range(len(images)):
        images[i] += matrix

    # Adjust all affected pixels to range(0, 255)
    images = np.clip(images, 0, 255, images)
    stop = timeit.default_timer()
    print("time to apply masks: ", stop - start)

    return images
