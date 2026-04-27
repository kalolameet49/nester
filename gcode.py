def generate_gcode(layout):

    lines = []
    lines.append("G21 ; mm mode")
    lines.append("G90 ; absolute")

    for poly in layout:
        coords = list(poly.exterior.coords)

        if not coords:
            continue

        start = coords[0]
        lines.append(f"G0 X{start[0]:.2f} Y{start[1]:.2f}")

        for x, y in coords[1:]:
            lines.append(f"G1 X{x:.2f} Y{y:.2f}")

        lines.append("G0")

    return "\n".join(lines)
