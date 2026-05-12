import streamlit as st

from utils import read_svg_area
from svg_visualizer import visualize_svg


def auto_sheet_page():

    st.header("🤖 Auto Sheet Selection")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    qty = st.number_input(
        "Quantity",
        value=10
    )

    sheets = [
        (2440, 1220),
        (3000, 1500),
        (6000, 1500)
    ]

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        area = read_svg_area(svg_file)

        total_area = area * qty

        best = None

        for w, h in sheets:

            util = (
                total_area
                /
                (w * h)
            ) * 100

            if util <= 100:

                if best is None or util > best[2]:

                    best = (w, h, util)

        if best:

            st.success(
                f"Recommended Sheet: "
                f"{best[0]} x {best[1]}"
            )

            st.success(
                f"Utilization: "
                f"{best[2]:.2f}%"
            )
