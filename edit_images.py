import numpy as np


#apply the mask to the images (changes the images!)
def apply_mask(images, mask):
    # Constructs Mask matrix
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

    return images