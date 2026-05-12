import streamlit as st

from utils import read_svg_area, calculate_weight

def weight_page():

st.header(" Weight Calculator")

svg_file = st.file_uploader("Upload SVG", type=["svg"])

thickness = st.number_input("Thickness (mm)", value=5.0) weight = calculate_weight(area, thickness, material)

st.success(f"Part Area: {area:.2f} mm²")

st.success(f"Estimated Weight: {weight:.2f} kg")
