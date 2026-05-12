import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from svgpathtools import svg2paths
from svg_visualizer import visualize_svg

st.set_page_config(page_title="ProNester", layout="wide")

st.title("⚙️ ProNester Industrial Suite")


# =====================================================
# SVG AREA READER
# =====================================================

def read_svg_area(uploaded_file):

    uploaded_file.seek(0)

    paths, attributes = svg2paths(uploaded_file)

    total_area = 0

    for p in paths:

        xmin, xmax, ymin, ymax = p.bbox()

        width = abs(xmax - xmin)
        height = abs(ymax - ymin)

        total_area += width * height

    return total_area


# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.radio(
    "Select Module",
    [
        "Weight Calculator",
        "Custom Sheet Nesting",
        "Auto Sheet Selection",
        "Stock Manager",
        "Time Estimator"
    ]
)

# =====================================================
# 1. WEIGHT CALCULATOR
# =====================================================

if menu == "Weight Calculator":

    st.header("⚖️ SVG Weight Calculator")

    svg_file = st.file_uploader(
        "Upload SVG File",
        type=["svg"]
    )

    material = st.selectbox("Material", ["MS", "SS"])

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

        svg_file.seek(0)

        area = read_svg_area(svg_file)

        density = 7850 if material == "MS" else 8000

        volume = (area * thickness * qty) / 1e9

        weight = volume * density

        st.success(f"SVG Area: {area:.2f} mm²")

        st.success(f"Estimated Weight: {weight:.2f} kg")


# =====================================================
# 2. CUSTOM SHEET NESTING
# =====================================================

elif menu == "Custom Sheet Nesting":

    st.header("📐 Custom Sheet Nesting")

    svg_file = st.file_uploader(
        "Upload SVG File",
        type=["svg"]
    )

    sheet_w = st.number_input(
        "Sheet Width (mm)",
        value=2440
    )

    sheet_h = st.number_input(
        "Sheet Height (mm)",
        value=1220
    )

    qty = st.number_input(
        "Part Quantity",
        value=10
    )

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        svg_file.seek(0)

        part_area = read_svg_area(svg_file)

        total_area = part_area * qty

        sheet_area = sheet_w * sheet_h

        utilization = (total_area / sheet_area) * 100

        scrap = 100 - utilization

        st.success(f"Total Part Area: {total_area:.2f} mm²")

        st.success(f"Sheet Utilization: {utilization:.2f}%")

        st.success(f"Scrap: {scrap:.2f}%")

        fig2, ax = plt.subplots(figsize=(10, 5))

        rect = plt.Rectangle(
            (0, 0),
            sheet_w,
            sheet_h,
            fill=False,
            linewidth=2
        )

        ax.add_patch(rect)

        ax.set_xlim(0, sheet_w)

        ax.set_ylim(0, sheet_h)

        ax.set_title("Sheet Layout Preview")

        st.pyplot(fig2)


# =====================================================
# 3. AUTO SHEET SELECTION
# =====================================================

elif menu == "Auto Sheet Selection":

    st.header("🤖 Auto Sheet Selection")

    svg_file = st.file_uploader(
        "Upload SVG File",
        type=["svg"]
    )

    qty = st.number_input(
        "Part Quantity",
        value=10
    )

    standard_sheets = [
        (2440, 1220),
        (3000, 1500),
        (6000, 1500)
    ]

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        svg_file.seek(0)

        area = read_svg_area(svg_file)

        total_area = area * qty

        best = None

        for w, h in standard_sheets:

            sheet_area = w * h

            util = (total_area / sheet_area) * 100

            if util <= 100:

                if best is None or util > best[2]:

                    best = (w, h, util)

        if best:

            st.success(
                f"Recommended Sheet: {best[0]} × {best[1]} mm"
            )

            st.success(
                f"Expected Utilization: {best[2]:.2f}%"
            )

            st.success(
                f"Expected Scrap: {100 - best[2]:.2f}%"
            )

        else:

            st.error("Part quantity exceeds standard sheet sizes")


# =====================================================
# 4. STOCK MANAGER
# =====================================================

elif menu == "Stock Manager":

    st.header("📦 Sheet Stock Manager")

    material = st.selectbox(
        "Material",
        ["MS", "SS"]
    )

    thickness = st.number_input(
        "Thickness",
        value=5
    )

    width = st.number_input(
        "Sheet Width",
        value=2440
    )

    height = st.number_input(
        "Sheet Height",
        value=1220
    )

    qty = st.number_input(
        "Available Quantity",
        value=1
    )

    if st.button("Add Stock"):

        stock = {
            "Material": material,
            "Thickness": thickness,
            "Width": width,
            "Height": height,
            "Qty": qty
        }

        st.success("Stock Added")

        st.write(stock)


# =====================================================
# 5. TIME ESTIMATOR
# =====================================================

elif menu == "Time Estimator":

    st.header("⏱ Cutting Time Estimator")

    svg_file = st.file_uploader(
        "Upload SVG File",
        type=["svg"]
    )

    qty = st.number_input(
        "Part Quantity",
        value=10
    )

    cutting_speed = st.number_input(
        "Cutting Speed mm/min",
        value=2000
    )

    pierce_count = st.number_input(
        "Pierce Count",
        value=10
    )

    pierce_time = st.number_input(
        "Pierce Time/sec",
        value=3
    )

    if svg_file:

        fig = visualize_svg(svg_file)

        st.pyplot(fig)

        svg_file.seek(0)

        area = read_svg_area(svg_file)

        perimeter = (area ** 0.5) * 4

        total_cut_length = perimeter * qty

        cut_time = total_cut_length / cutting_speed

        pierce_total = (pierce_count * pierce_time) / 60

        total_time = cut_time + pierce_total

        st.success(
            f"Estimated Cut Length: {total_cut_length:.2f} mm"
        )

        st.success(
            f"Estimated Cutting Time: {total_time:.2f} min"
        )
