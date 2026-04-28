import random
from shapely.affinity import translate


def select(population, retain=0.5):
    """
    Select top-performing layouts
    """
    if not population:
        return []

    population = sorted(population, key=lambda x: x["util"], reverse=True)

    retain_length = max(1, int(len(population) * retain))
    return population[:retain_length]


def mutate(layout, mutation_rate=0.2):
    """
    Mutate layout slightly
    """
    new_layout = []

    for part in layout:
        if random.random() < mutation_rate:
            dx = random.uniform(-5, 5)
            dy = random.uniform(-5, 5)
            moved = translate(part, xoff=dx, yoff=dy)
            new_layout.append(moved)
        else:
            new_layout.append(part)

    return new_layout
