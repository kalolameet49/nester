import ezdxf
from shapely.geometry import Polygon, MultiLineString
from shapely.ops import unary_union, polygonize
from shapely.affinity import translate
import io
import svgelements


def extract_from_svg(file):
    svg = svgelements.SVG.parse(io.StringIO(file.getvalue().decode()))
    polys = []

    for e in svg.elements():
        if isinstance(e, svgelements.Path):
            pts = [(p.x, p.y) for p in e.as_points()]
            if len(pts) > 2:
                poly = Polygon(pts)
                if not poly.is_valid:
                    poly = poly.buffer(0)
                if poly.area > 1:
                    polys.append(translate(poly, -poly.bounds[0], -poly.bounds[1]))

    return polys


def extract_from_dxf(file):
    doc = ezdxf.read(io.BytesIO(file.getvalue()))
    msp = doc.modelspace()
    segs = []

    for e in msp:
        try:
            for p in ezdxf.path.make_paths(e):
                v = list(p.flattening(0.1))
                for i in range(len(v) - 1):
                    segs.append([(v[i].x, v[i].y), (v[i+1].x, v[i+1].y)])
        except:
            pass

    merged = unary_union(MultiLineString(segs))
    polys = list(polygonize(merged))

    return [translate(p, -p.bounds[0], -p.bounds[1]) for p in polys if p.area > 1]
