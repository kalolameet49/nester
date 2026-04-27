import random
from shapely.affinity import translate
from geometry import generate_rotations
from nfp import no_fit_polygon


def place_part(part, placed, gap, margin):

    best = None
    best_score = float('inf')

    rotations = generate_rotations(part)

    candidates = [(margin, margin)]

    for p in placed:
        minx, miny, maxx, maxy = p.bounds
        candidates += [(maxx, miny), (minx, maxy), (maxx, maxy)]

    random.shuffle(candidates)

    for r in rotations:
        for x, y in candidates:

            trial = translate(r, x, y)

            if not no_fit_polygon(trial, placed):
                continue

            score = trial.bounds[1] + trial.bounds[0] * 0.2

            if score < best_score:
                best = trial
                best_score = score

    return best
