from shapely.affinity import rotate


def generate_rotations(polygon, angles=[0, 90, 180, 270]):
    """
    Generate rotated versions of polygon
    """
    rotations = []

    for angle in angles:
        try:
            r = rotate(polygon, angle, origin='centroid')
            rotations.append(r)
        except:
            continue

    return rotations
