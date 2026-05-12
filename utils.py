import math

from svgpathtools import svg2paths

DENSITY = {

"MS": 7850,

"SS": 8000

}

def read_svg_area(uploaded_file):

paths, attributes = svg2paths(uploaded_file) total_area = 0

for p in paths:

xmin, xmax, ymin, ymax = p.bbox()

area = abs((xmax - xmin) * (ymax - ymin))

total_area += area

return total_area

def calculate_weight(area_mm2, thickness_mm, material):

density = DENSITY[material]

volume_m3 = (area_mm2 * thickness_mm) / 1e9

weight = volume_m3 * density

return weight

def sheet_utilization(part_area, sheet_area):

util = (part_area / sheet_area) * 100

scrap = 100 - util

return util, scrap
