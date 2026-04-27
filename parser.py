import ezdxf
import io
import svgelements
from shapely.geometry import Polygon
from shapely.affinity import translate

def extract_from_svg(file):
    svg = svgelements.SVG.parse(io.StringIO(file.getvalue().decode()))
    polys = []

    for e in svg.elements():
        if isinstance(e, svgelements.Path):
            pts = [(p.x, p.y) for p in e.as_points()]
            if len(pts) > 2:
                poly = Polygon(pts)
                if poly.area > 1:
                    polys.append(translate(poly, -poly.bounds[0], -poly.bounds[1]))

    return polys

def extract_from_dxf(file):
    doc = ezdxf.read(io.BytesIO(file.getvalue()))
    msp = doc.modelspace()

    polys = []

    for e in msp:
        try:
            points = [(p.dxf.location.x, p.dxf.location.y) for p in e]
            if len(points) > 2:
                poly = Polygon(points)
                polys.append(poly)
        except:
            pass

    return polys
