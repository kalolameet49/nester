import streamlit as st
import matplotlib.pyplot as plt
import math

from utils import (
    read_svg_area,
    simple_nesting_layout
)

from svg_visualizer import visualize_svg


def auto_sheet_page():

    st.header("🤖 Auto Sheet Selection + Nesting")

    svg_file = st.file_uploader(
        "Upload SVG",
        type=["svg"]
    )

    qty = st.number_input(
        "Quantity",
        value=10
    )

    gap = st.number_input(
        "Gap Between Parts",
        value=10
    )

    standard_sheets = [
        (2440, 1220),
        (3000, 1500),
        (6000, 1500)
    ]

    if svg_file:

        fig_svg = visualize_svg(svg_file)

        st.pyplot(fig_svg)

        area = read_svg_area(svg_file)

        part_w = math.sqrt(area)

        part_h = math.sqrt(area)

        best = None

        for w, h in standard_sheets:

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

            st.success(
                f"Expected Utilization: "
                f"{best[2]:.2f}%"
            )

            st.success(
                f"Expected Scrap: "
                f"{100 - best[2]:.2f}%"
            )

            # RUN BUTTON

            if st.button("🚀 Run Auto Nesting"):

                positions, placed = simple_nesting_layout(
                    best[0],
                    best[1],
                    part_w,
                    part_h,
                    qty,
                    gap
                )

                # DRAW LAYOUT

                fig, ax = plt.subplots(
                    figsize=(12, 6)
                )

                sheet = plt.Rectangle(
                    (0, 0),
                    best[0],
                    best[1],
                    fill=False,
                    linewidth=3
                )

                ax.add_patch(sheet)

                for x, y in positions:

                    rect = plt.Rectangle(
                        (x, y),
                        part_w,
                        part_h,
                        fill=False
                    )

                    ax.add_patch(rect)

                ax.set_xlim(0, best[0])

                ax.set_ylim(0, best[1])

                ax.set_aspect('equal')

                ax.invert_yaxis()

                ax.set_title(
                    "Auto Sheet Nesting Layout"
                )

                st.pyplot(fig)

                st.success(
                    f"Placed Parts: {placed}"
                )
