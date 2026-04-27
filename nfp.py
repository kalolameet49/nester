import pyclipper

SCALE = 1000


def scale_up(poly):
    return [(int(x * SCALE), int(y * SCALE)) for x, y in poly.exterior.coords]


def scale_down(path):
    return [(x / SCALE, y / SCALE) for x, y in path]


def minkowski_nfp(polyA, polyB):

    A = scale_up(polyA)
    B = scale_up(polyB)

    solution = pyclipper.MinkowskiSum(A, B, True)

    if not solution:
        return None

    largest = max(solution, key=lambda p: abs(pyclipper.Area(p)))
    return scale_down(largest)


def no_fit_polygon(part, placed):

    for p in placed:
        nfp = minkowski_nfp(p, part)

        if nfp is None:
            continue

        pc = pyclipper.Pyclipper()
        pc.AddPath(scale_up(part), pyclipper.PT_SUBJECT, True)
        pc.AddPath(scale_up_path(nfp), pyclipper.PT_CLIP, True)

        if pc.Execute(pyclipper.CT_INTERSECTION):
            return False

    return True


def scale_up_path(path):
    return [(int(x * SCALE), int(y * SCALE)) for x, y in path]
