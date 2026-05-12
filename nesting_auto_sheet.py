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


def auto_sheet_page():

    st.header("🤖 Auto SVG Nesting")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    qty = st.number_input(
        "Quantity",
        value=10
    )

    gap = st.number_input(
        "Gap",
        value=10
    )

    sheets = [
        (2440, 1220),
        (3000, 1500),
        (6000, 1500)
    ]

    if svg_file:

        fig_svg = visualize_svg(svg_file)

        st.pyplot(fig_svg)

        area = read_svg_area(svg_file)

        part_w, part_h = get_svg_bounds(svg_file)

        shapes = extract_svg_points(svg_file)

        best = None

        for w, h in sheets:

            util = (
                (area * qty)
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

            if st.button("🚀 Run Auto Nesting"):

                positions, placed = simple_nesting_layout(
                    best[0],
                    best[1],
                    part_w,
                    part_h,
                    qty,
                    gap
                )

                fig, ax = plt.subplots(
                    figsize=(14, 7)
                )

                sheet = plt.Rectangle(
                    (0, 0),
                    best[0],
                    best[1],
                    fill=False,
                    linewidth=3
                )

                ax.add_patch(sheet)

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

                ax.set_xlim(0, best[0])

                ax.set_ylim(0, best[1])

                ax.set_aspect('equal')

                ax.invert_yaxis()

                ax.set_title(
                    "Auto SVG Nesting Layout"
                )

                st.pyplot(fig)
