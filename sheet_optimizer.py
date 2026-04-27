from shapely.affinity import translate


def split_into_sheets(layout, sheet_w, sheet_h, margin):

    sheets = []
    current = []

    for part in layout:

        if not current:
            current.append(part)
            continue

        maxx = max(p.bounds[2] for p in current)
        maxy = max(p.bounds[3] for p in current)

        px, py, px2, py2 = part.bounds

        if max(px2, maxx) > sheet_w or max(py2, maxy) > sheet_h:
            sheets.append(current)
            current = [translate(part, margin, margin)]
        else:
            current.append(part)

    if current:
        sheets.append(current)

    return sheets
