import streamlit as st

from utils import read_svg_area
from svg_visualizer import visualize_svg


def time_page():

    st.header("⏱ Time Estimator")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    qty = st.number_input(
        "Quantity",
        value=10
    )

    speed = st.number_input(
        "Cut Speed mm/min",
        value=2000
    )

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        area = read_svg_area(svg_file)

        perimeter = (area ** 0.5) * 4

        total_cut = perimeter * qty

        time = total_cut / speed

        st.success(
            f"Estimated Time: "
            f"{time:.2f} min"
        )
