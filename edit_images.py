def apply_mask(img, mask):
    for shape in mask:
        change = shape.changeRGB
        for (x, y) in shape.getInsidePoints():
            img[y][x] = [val+change for val in img[y][x]]

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
