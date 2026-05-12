import streamlit as st

import matplotlib.pyplot as plt

from utils import read_svg_area, sheet_utilization

def custom_nesting_page():

st.header(" Custom Sheet Nesting")

svg_file = st.file_uploader("Upload SVG", type=["svg"])

sheet_w = st.number_input("Sheet Width", value=2440)

sheet_h = st.number_input("Sheet Height", value=1220)

if svg_file:

part_area = read_svg_area(svg_file)

sheet_area = sheet_w * sheet_h

util, scrap = sheet_utilization(part_area, sheet_area)

st.success(f"Utilization: {util:.2f}%")

st.success(f"Scrap: {scrap:.2f}%")

fig, ax = plt.subplots(figsize=(10, 5))

rect = plt.Rectangle((0, 0), sheet_w, sheet_h, fill=False)

ax.add_patch(rect)

ax.set_xlim(0, sheet_w)

ax.set_ylim(0, sheet_h)

st.pyplot(fig)
