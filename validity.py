from scipy.spatial import Delaunay


def validate(listOfPoints):
    if validate_list(listOfPoints):
        try:
            Delaunay(listOfPoints)
            return True
        except:
            return False
    else:
        return False


def validate_list(listOfPoints):
    for point in listOfPoints:
        if not validate_point(point):
            return False
    return True


def validate_point(point, dim=299):
    x, y = point
    if x in range(0, dim) and y in range(0, dim):
        return True
    else:
        return False
