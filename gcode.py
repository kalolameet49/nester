def generate_gcode(layout):

    lines = ["G21", "G90"]

    for poly in layout:
        coords = list(poly.exterior.coords)

        if not coords:
            continue

        start = coords[0]
        lines.append(f"G0 X{start[0]:.2f} Y{start[1]:.2f}")

        for x, y in coords[1:]:
            lines.append(f"G1 X{x:.2f} Y{y:.2f}")

    return "\n".join(lines)
