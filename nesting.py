import random
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
from shapely.geometry import Polygon


class ProNester:

    def __init__(self, gap=3.0, margin=5.0,
                 population_size=12,
                 generations=8,
                 mutation_rate=0.3):

        self.gap = gap
        self.margin = margin
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def generate_rotations(self, part):
        angles = [0, 90, 180, 270] + [random.randint(0, 360) for _ in range(2)]
        result = []

        for a in angles:
            r = rotate(part, a, origin='centroid')
            minx, miny, _, _ = r.bounds
            result.append(translate(r, -minx, -miny))

        return result

    def no_fit(self, part, placed):
        return not any(part.buffer(self.gap).intersects(p) for p in placed)

    def try_hole(self, part, placed):

        for p in placed:
            if not isinstance(p, Polygon):
                continue

            for hole in p.interiors:
                hole_poly = Polygon(hole)

                if hole_poly.area > part.area:
                    moved = translate(part, hole_poly.bounds[0], hole_poly.bounds[1])

                    if hole_poly.contains(moved):
                        return moved
        return None

    def place(self, part, placed):

        inside = self.try_hole(part, placed)
        if inside:
            return inside

        best = None
        best_score = float('inf')

        for r in self.generate_rotations(part):
            for p in placed + [None]:

                x = self.margin if p is None else p.bounds[2]
                y = self.margin if p is None else p.bounds[3]

                trial = translate(r, x, y)

                if not self.no_fit(trial, placed):
                    continue

                score = trial.bounds[1] + trial.bounds[0]

                if score < best_score:
                    best = trial
                    best_score = score

        return best

    def build(self, parts):

        parts = sorted(parts, key=lambda p: -p.area)

        placed = []

        for part in parts:
            pos = self.place(part, placed)

            if pos:
                placed.append(pos)
            else:
                placed.append(translate(part, self.margin, self.margin))

        return placed

    def evaluate(self, layout, W=None, H=None):

        union = unary_union(layout)
        minx, miny, maxx, maxy = union.bounds

        W = W or maxx + self.margin
        H = H or maxy + self.margin

        area = sum(p.area for p in layout)
        util = area / (W * H) * 100

        return {"layout": layout, "W": W, "H": H, "util": util}

    def nest(self, parts, W=None, H=None, return_all=False):

        pop = [self.build(parts) for _ in range(self.population_size)]

        history = []

        for _ in range(self.generations):

            scored = [self.evaluate(p, W, H) for p in pop]
            scored.sort(key=lambda x: -x["util"])

            survivors = scored[:max(2, len(scored)//2)]

            new_pop = [s["layout"] for s in survivors]

            while len(new_pop) < self.population_size:
                child = self.build(parts)
                new_pop.append(child)

            pop = new_pop
            history.extend(scored)

        best = max(history, key=lambda x: x["util"])

        return (best, history[:10]) if return_all else best
