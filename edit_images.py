import numpy as np


def apply_mask(images, mask):

    # Constructs Mask matrix
    matrix = np.empty((300, 300, 3))
    for shape in mask:
        change = shape.changeRGB
        for (x, y) in shape.insidePoints:
            matrix[y][x] += change

    # Applies mask to the images
    for i in range(len(images)):
        images[i] += matrix

    # Adjust all affected pixels to range(0, 255)
    for j in range(len(images)):
        row, col, idx = np.nonzero(images[j] < 0)
        for i in range(len(row)):
            images[j][row[i]][col[i]][idx[i]] = 0
            # images[j] is a singular image
            # row[i] is the row number
            # col[i] is the column number
            # idx[i] is the index

        row, col, idx = np.nonzero(images[j] > 255)
        for i in range(len(row)):
            images[j][row[i]][col[i]][idx[i]] = 255

    return images
