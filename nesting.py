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

    # ---------- ROTATIONS ----------
    def generate_rotations(self, part):
        angles = [0, 90, 180, 270]
        angles += [random.randint(0, 360) for _ in range(2)]

        result = []
        for a in angles:
            r = rotate(part, a, origin='centroid')
            minx, miny, _, _ = r.bounds
            r = translate(r, -minx, -miny)
            result.append(r)

        return result

    # ---------- NFP APPROX ----------
    def no_fit_check(self, part, placed):
        for p in placed:
            if part.buffer(self.gap).intersects(p):
                return False
        return True

    # ---------- HOLE NESTING ----------
    def try_place_inside(self, part, placed):

        for p in placed:
            if not isinstance(p, Polygon):
                continue

            holes = list(p.interiors)

            for hole in holes:
                hole_poly = Polygon(hole)

                if hole_poly.area > part.area * 1.1:

                    moved = translate(part,
                                      hole_poly.bounds[0],
                                      hole_poly.bounds[1])

                    if hole_poly.contains(moved):
                        return moved

        return None

    # ---------- CANDIDATES ----------
    def get_candidates(self, placed):
        pts = [(self.margin, self.margin)]

        for p in placed:
            minx, miny, maxx, maxy = p.bounds
            pts.append((maxx, miny))
            pts.append((minx, maxy))

        random.shuffle(pts)
        return pts

    # ---------- PLACE ----------
    def place_part(self, part, placed):

        # 🔥 TRY HOLE FIRST
        inside = self.try_place_inside(part, placed)
        if inside:
            return inside

        best = None
        best_score = float('inf')

        rotations = self.generate_rotations(part)
        candidates = self.get_candidates(placed)

        for r in rotations:
            for cx, cy in candidates:

                trial = translate(r, cx, cy)

                if not self.no_fit_check(trial, placed):
                    continue

                score = trial.bounds[1] + trial.bounds[0] * 0.1 + random.random() * 2

                if score < best_score:
                    best = trial
                    best_score = score

        return best

    # ---------- BUILD ----------
    def build_layout(self, parts):

        parts = parts.copy()

        parts.sort(key=lambda p: p.area * random.uniform(0.8, 1.2), reverse=True)
        parts = [p.buffer(self.gap / 2) for p in parts]

        placed = []

        for part in parts:
            pos = self.place_part(part, placed)

            if pos:
                placed.append(pos)
            else:
                placed.append(translate(part, self.margin, self.margin))

        return placed

    # ---------- FITNESS ----------
    def evaluate(self, layout, sheet_w=None, sheet_h=None):

        union = unary_union(layout)
        minx, miny, maxx, maxy = union.bounds

        W = sheet_w if sheet_w else maxx + self.margin
        H = sheet_h if sheet_h else maxy + self.margin

        total_area = sum(p.area for p in layout)
        util = (total_area / (W * H)) * 100

        return {
            "layout": layout,
            "W": W,
            "H": H,
            "util": util
        }

    # ---------- GA ----------
    def nest(self, parts, sheet_w=None, sheet_h=None, return_all=False):

        population = [self.build_layout(parts) for _ in range(self.population_size)]

        history = []

        for _ in range(self.generations):

            scored = [self.evaluate(p, sheet_w, sheet_h) for p in population]
            scored.sort(key=lambda x: -x["util"])

            survivors = scored[:max(2, int(self.population_size * 0.4))]
            new_population = [s["layout"] for s in survivors]

            while len(new_population) < self.population_size:

                parent = random.choice(survivors)["layout"]

                child = self.build_layout(parts)

                # mutation
                if random.random() < self.mutation_rate:
                    child = [rotate(p, random.randint(0, 360), origin='centroid') for p in child]

                new_population.append(child)

            population = new_population
            history.extend(scored)

        final = [self.evaluate(p, sheet_w, sheet_h) for p in population]
        final.sort(key=lambda x: -x["util"])

        best = final[0]

        unique = []
        seen = set()

        for r in history:
            key = round(r["util"], 2)
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return (best, unique[:10]) if return_all else best
