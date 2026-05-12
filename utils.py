import math
from svgpathtools import svg2paths


def read_svg_area(uploaded_file):

    uploaded_file.seek(0)

    paths, attributes = svg2paths(uploaded_file)

    total_area = 0

    for p in paths:

        xmin, xmax, ymin, ymax = p.bbox()

        width = abs(xmax - xmin)
        height = abs(ymax - ymin)

        total_area += width * height

    return total_area


def simple_nesting_layout(
    sheet_w,
    sheet_h,
    part_w,
    part_h,
    qty,
    gap=10
):

    positions = []

    cols = int(sheet_w // (part_w + gap))

    rows = int(sheet_h // (part_h + gap))

    max_parts = cols * rows

    placed = min(qty, max_parts)

    count = 0

    for r in range(rows):

        for c in range(cols):

            if count >= placed:
                break

            x = c * (part_w + gap)
            y = r * (part_h + gap)

            positions.append((x, y))

            count += 1

    return positions, placed
