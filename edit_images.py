def apply_mask(img, inside_points, mask):
    for x, y in inside_points:
        img[y][x] = boundary(img[y][x] + mask)

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
