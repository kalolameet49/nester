import streamlit as st

from utils import read_svg_area
from svg_visualizer import visualize_svg


def weight_page():

    st.header("⚖️ SVG Weight Calculator")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    material = st.selectbox(
        "Material",
        ["MS", "SS"]
    )

    thickness = st.number_input(
        "Thickness (mm)",
        value=5.0
    )

    qty = st.number_input(
        "Quantity",
        value=1
    )

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        area = read_svg_area(svg_file)

        density = 7850 if material == "MS" else 8000

        volume = (area * thickness * qty) / 1e9

        weight = volume * density

        st.success(f"Area: {area:.2f} mm²")

        st.success(f"Weight: {weight:.2f} kg")
