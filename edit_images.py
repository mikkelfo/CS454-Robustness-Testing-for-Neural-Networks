# TODO: Change this to mask matrix
def apply_mask(img, mask):
    for shape in mask:
        change = shape.changeRGB
        for (x, y) in shape.getInsidePoints():
            img[y][x][0] += change[0]
            img[y][x][1] += change[2]
            img[y][x][2] += change[3]

    return img

def boundary(pixels):
    new_array = []
    for val in pixels:
        if val < 0:
            val = 0
        elif val > 255:
            val = 255
        new_array.append(val)
    return new_array
