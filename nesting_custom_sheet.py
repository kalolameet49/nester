import streamlit as st
import matplotlib.pyplot as plt
import math

from utils import (
    read_svg_area,
    simple_nesting_layout
)

from svg_visualizer import visualize_svg


def nesting_page():

    st.header("📐 Industrial Sheet Nesting")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    sheet_w = st.number_input(
        "Sheet Width",
        value=2440
    )

    sheet_h = st.number_input(
        "Sheet Height",
        value=1220
    )

    qty = st.number_input(
        "Quantity",
        value=10
    )

    gap = st.number_input(
        "Gap Between Parts",
        value=10
    )

    if svg_file:

        # SVG PREVIEW

        fig_svg = visualize_svg(svg_file)

        st.pyplot(fig_svg)

        area = read_svg_area(svg_file)

        # APPROX PART SIZE

        part_w = math.sqrt(area)

        part_h = math.sqrt(area)

        st.info(
            f"Approx Part Size: "
            f"{part_w:.1f} x {part_h:.1f} mm"
        )

        # RUN NESTING BUTTON

        if st.button("🚀 Run Nesting"):

            positions, placed = simple_nesting_layout(
                sheet_w,
                sheet_h,
                part_w,
                part_h,
                qty,
                gap
            )

            utilization = (
                (area * placed)
                /
                (sheet_w * sheet_h)
            ) * 100

            scrap = 100 - utilization

            st.success(
                f"Placed Parts: {placed}"
            )

            st.success(
                f"Utilization: {utilization:.2f}%"
            )

            st.success(
                f"Scrap: {scrap:.2f}%"
            )

            # DRAW SHEET

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            sheet = plt.Rectangle(
                (0, 0),
                sheet_w,
                sheet_h,
                fill=False,
                linewidth=3
            )

            ax.add_patch(sheet)

            # DRAW PARTS

            for x, y in positions:

                rect = plt.Rectangle(
                    (x, y),
                    part_w,
                    part_h,
                    fill=False
                )

                ax.add_patch(rect)

            ax.set_xlim(0, sheet_w)

            ax.set_ylim(0, sheet_h)

            ax.set_aspect('equal')

            ax.invert_yaxis()

            ax.set_title("Nesting Layout")

            st.pyplot(fig)
