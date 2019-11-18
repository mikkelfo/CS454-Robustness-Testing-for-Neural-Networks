from scipy.spatial import ConvexHull, Delaunay

from operator import itemgetter

from edit_images import load_data, get_img, show_img

def in_hull(hull, p):
    return hull.find_simplex(p) >= 0

def check_hull_boundary(points):
    min_x, max_x = min(points,key=itemgetter(0))[0], max(points,key=itemgetter(0))[0]
    min_y, max_y = min(points,key=itemgetter(1))[1], max(points,key=itemgetter(1))[1]

    hull = Delaunay(points)
    p = []
    for x in range(min_x - 1, max_x + 1):
        for y in range(min_y - 1, max_y + 1):
            t = (x, y)
            if in_hull(hull, t):
                p.append(t)
    return p

# TODO: check overflow
def apply_mask(img, inside_points, mask):
    img = img.astype(int)
    for x, y in inside_points:
        img[y][x] = img[y][x] + mask
    return img


points = [(5,5), (12,16), (16,16), (17,8), (9,7)]
batch = load_data("data_batch_1")
image = get_img(batch, 1)
rgb = [100, 100, 100]

inside_points = check_hull_boundary(points)

pixelsChanged = len(inside_points)
print(pixelsChanged)

image = apply_mask(image, inside_points, rgb)

show_img(image)
