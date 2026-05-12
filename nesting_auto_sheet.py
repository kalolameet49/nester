import streamlit as st

from utils import read_svg_area

STANDARD_SHEETS = [

(2440, 1220),

(3000, 1500),

(6000, 1500)

]

def auto_sheet_page():

st.header(" Auto Sheet Selection")

svg_file = st.file_uploader("Upload SVG", type=["svg"])

if svg_file:

area = read_svg_area(svg_file)

best = None

for w, h in STANDARD_SHEETS:

sheet_area = w * h

util = (area / sheet_area) * 100

if util < 100:

if best is None or util > best[2]:

best = (w, h, util)

if best:

st.success(f"Recommended Sheet: {best[0]} x {best[1]}")

st.success(f"Utilization: {best[2]:.2f}%")
