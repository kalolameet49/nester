from shapely.ops import unary_union


def evaluate(layout, sheet_w, sheet_h):
    """
    Evaluate nesting layout efficiency
    Returns utilization %
    """

    if not layout:
        return {
            "layout": [],
            "util": 0,
            "W": sheet_w,
            "H": sheet_h
        }

    try:
        union = unary_union(layout)
        used_area = union.area
    except Exception:
        used_area = sum(p.area for p in layout)

    sheet_area = sheet_w * sheet_h

    utilization = (used_area / sheet_area) * 100 if sheet_area else 0

    return {
        "layout": layout,
        "util": utilization,
        "W": sheet_w,
        "H": sheet_h
    }
