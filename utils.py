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


def get_svg_bounds(uploaded_file):

    uploaded_file.seek(0)

    paths, attributes = svg2paths(uploaded_file)

    min_x = 999999
    min_y = 999999

    max_x = -999999
    max_y = -999999

    for p in paths:

        xmin, xmax, ymin, ymax = p.bbox()

        min_x = min(min_x, xmin)
        min_y = min(min_y, ymin)

        max_x = max(max_x, xmax)
        max_y = max(max_y, ymax)

    width = max_x - min_x
    height = max_y - min_y

    return width, height


def extract_svg_points(uploaded_file):

    uploaded_file.seek(0)

    paths, attributes = svg2paths(uploaded_file)

    all_shapes = []

    for path in paths:

        points = []

        for seg in path:

            points.append((
                seg.start.real,
                seg.start.imag
            ))

            points.append((
                seg.end.real,
                seg.end.imag
            ))

        all_shapes.append(points)

    return all_shapes


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
