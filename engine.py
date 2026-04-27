from multiprocessing import Pool
from placement import place_part
from evaluator import evaluate
from evolution import select, mutate
from sheet_optimizer import split_into_sheets


class ProNester:

    def __init__(self, gap=3, margin=5,
                 population_size=10,
                 generations=6,
                 mutation_rate=0.3):

        self.gap = gap
        self.margin = margin
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def build_layout(self, parts):

        parts = sorted(parts, key=lambda p: -p.area)
        placed = []

        for part in parts:
            pos = place_part(part, placed, self.gap, self.margin)
            if pos:
                placed.append(pos)

        return placed

    def nest(self, parts, sheet_w, sheet_h, return_all=False):

        with Pool(2) as pool:
            population = pool.map(self.build_layout, [parts]*self.population_size)

        history = []

        for _ in range(self.generations):

            scored = [evaluate(p, self.margin, sheet_w, sheet_h) for p in population]
            survivors = select(scored)

            new_pop = [s["layout"] for s in survivors]

            while len(new_pop) < self.population_size:
                child = self.build_layout(parts)
                child = mutate(child, self.mutation_rate)
                new_pop.append(child)

            population = new_pop
            history.extend(scored)

        best = max(history, key=lambda x: x["util"])

        best["sheets"] = split_into_sheets(best["layout"], sheet_w, sheet_h, self.margin)

        return (best, history[:10]) if return_all else best


if __name__ == "__main__":
    pass
