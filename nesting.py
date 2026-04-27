import random
from shapely.affinity import translate, rotate
from shapely.ops import unary_union

class ProNester:

    def __init__(self, gap=3.0, margin=5.0, rotations=(0, 90, 180, 270), tries=10):
        self.gap = gap
        self.margin = margin
        self.rotations = rotations
        self.tries = tries

    # ---------- helpers ----------
    def _norm(self, poly):
        minx, miny, _, _ = poly.bounds
        return translate(poly, -minx, -miny)

    def _rotations(self, poly):
        res = []
        for a in self.rotations:
            r = rotate(poly, a, origin='centroid')
            res.append(self._norm(r))
        return res

    def _intersects_any(self, poly, placed):
        return any(poly.intersects(p) for p in placed)

    def _in_sheet(self, poly, sheet_w, sheet_h):
        if sheet_w is None or sheet_h is None:
            return True
        minx, miny, maxx, maxy = poly.bounds
        return (minx >= 0 and miny >= 0 and maxx <= sheet_w and maxy <= sheet_h)

    # candidate anchor points (BL corners + origin)
    def _candidates(self, placed):
        pts = {(self.margin, self.margin)}
        for p in placed:
            minx, miny, maxx, maxy = p.bounds
            pts.add((maxx + self.gap, miny))  # to the right
            pts.add((minx, maxy + self.gap))  # above
        # sort bottom-left preference
        return sorted(list(pts), key=lambda t: (t[1], t[0]))

    def _place_one(self, poly, placed, sheet_w, sheet_h):
        best = None
        best_key = (float('inf'), float('inf'))  # (y, x)

        for r in self._rotations(poly):
            for (cx, cy) in self._candidates(placed):
                trial = translate(r, cx, cy)

                if not self._in_sheet(trial, sheet_w, sheet_h):
                    continue
                if self._intersects_any(trial, placed):
                    continue

                tx, ty, _, _ = trial.bounds
                key = (ty, tx)  # bottom-left preference
                if key < best_key:
                    best = trial
                    best_key = key

        return best

    # push parts left/down greedily to compact gaps
    def _compact(self, placed, sheet_w, sheet_h, iters=3):
        moved = placed[:]
        for _ in range(iters):
            # try move each poly left, then down
            for i, p in enumerate(moved):
                # move left
                step = max(self.gap, 1.0)
                while True:
                    trial = translate(p, -step, 0)
                    if not self._in_sheet(trial, sheet_w, sheet_h):
                        break
                    if any(trial.intersects(moved[j]) for j in range(len(moved)) if j != i):
                        break
                    p = trial
                # move down
                while True:
                    trial = translate(p, 0, -step)
                    if not self._in_sheet(trial, sheet_w, sheet_h):
                        break
                    if any(trial.intersects(moved[j]) for j in range(len(moved)) if j != i):
                        break
                    p = trial

                moved[i] = p
        return moved

    def _layout_bounds(self, placed):
        if not placed:
            return 0, 0
        u = unary_union(placed)
        minx, miny, maxx, maxy = u.bounds
        return maxx + self.margin, maxy + self.margin

    def _utilization(self, parts, W, H):
        if W == 0 or H == 0:
            return 0.0
        total = sum(p.area for p in parts)
        return (total / (W * H)) * 100.0

    # ---------- public ----------
    def nest(self, parts, sheet_w=None, sheet_h=None, return_all=False):
        """
        parts: list of shapely polygons (mm units)
        sheet_w, sheet_h: optional constraints (mm)
        return_all: if True, return all candidate layouts (for "10 layouts" feature)
        """

        # buffer gap
        base_parts = [self._norm(p).buffer(self.gap / 2.0) for p in parts]

        candidates = []

        for t in range(self.tries):
            # shuffle to explore different sequences
            parts_shuffled = base_parts[:]
            random.shuffle(parts_shuffled)

            placed = []

            for p in parts_shuffled:
                pos = self._place_one(p, placed, sheet_w, sheet_h)
                if pos is None:
                    # fallback: try origin-ish placement
                    fallback = translate(p, self.margin, self.margin)
                    if self._in_sheet(fallback, sheet_w, sheet_h) and not self._intersects_any(fallback, placed):
                        placed.append(fallback)
                    else:
                        # if sheet constrained and cannot place, skip (or break)
                        continue
                else:
                    placed.append(pos)

            # compaction pass
            placed = self._compact(placed, sheet_w, sheet_h, iters=3)

            W, H = self._layout_bounds(placed)
            util = self._utilization(base_parts, W, H)

            candidates.append({
                "W": W,
                "H": H,
                "layout": placed,
                "util": util
            })

        # pick best
        best = max(candidates, key=lambda x: x["util"]) if candidates else {"W":0,"H":0,"layout":[],"util":0}

        if return_all:
            return best, candidates
        return best["W"], best["H"], best["layout"], best["util"]
