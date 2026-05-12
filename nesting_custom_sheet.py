import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from utils import (
    read_svg_area,
    simple_nesting_layout,
    get_svg_bounds,
    extract_svg_points
)

from svg_visualizer import visualize_svg


def nesting_page():

    st.header("📐 True SVG Shape Nesting")

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
        "Gap",
        value=10
    )

    if svg_file:

        fig_svg = visualize_svg(svg_file)

        st.pyplot(fig_svg)

        area = read_svg_area(svg_file)

        part_w, part_h = get_svg_bounds(svg_file)

        shapes = extract_svg_points(svg_file)

        st.success(
            f"Part Size: "
            f"{part_w:.1f} x {part_h:.1f}"
        )

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

            # DRAW TRUE SHAPES

            fig, ax = plt.subplots(
                figsize=(14, 7)
            )

            # SHEET

            sheet = plt.Rectangle(
                (0, 0),
                sheet_w,
                sheet_h,
                fill=False,
                linewidth=3
            )

            ax.add_patch(sheet)

            # DRAW SVG SHAPES

            for px, py in positions:

                for shape in shapes:

                    shifted = []

                    for x, y in shape:

                        shifted.append((
                            x + px,
                            y + py
                        ))

                    poly = Polygon(
                        shifted,
                        closed=False,
                        fill=False
                    )

                    ax.add_patch(poly)

            ax.set_xlim(0, sheet_w)

            ax.set_ylim(0, sheet_h)

            ax.set_aspect('equal')

            ax.invert_yaxis()

            ax.set_title(
                "True SVG Nesting Layout"
            )

            st.pyplot(fig)
