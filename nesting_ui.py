import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from parser import extract_from_dxf, extract_from_svg
from engine import ProNester
from gcode import generate_gcode
from db import create_job


def draw_layout(layout, W, H):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_aspect('equal')

    ax.add_patch(patches.Rectangle((0, 0), W, H, fill=False))

    for poly in layout:
        try:
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha=0.5)
        except:
            pass

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    return fig


def nesting_ui():

    st.header("📐 Sheet Nesting")

    gap = st.slider("Gap (mm)", 0.0, 10.0, 3.0)
    margin = st.slider("Margin (mm)", 0.0, 20.0, 5.0)

    population = st.slider("Population", 6, 30, 12)
    generations = st.slider("Generations", 3, 20, 8)

    sheet_w = st.number_input("Sheet Width", value=2440)
    sheet_h = st.number_input("Sheet Height", value=1220)

    files = st.file_uploader("Upload DXF / SVG", type=["dxf", "svg"], accept_multiple_files=True)

    if not files:
        return

    parts = []

    for f in files:
        try:
            shapes = extract_from_svg(f) if f.name.endswith(".svg") else extract_from_dxf(f)
            qty = st.number_input(f"{f.name} qty", 1, 100, 1)

            for _ in range(qty):
                parts.extend(shapes)

        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")
            return

    if st.button("🚀 Run Nesting"):

        try:
            with st.spinner("Running industrial nesting..."):

                engine = ProNester(
                    gap=gap,
                    margin=margin,
                    population_size=population,
                    generations=generations
                )

                best, layouts = engine.nest(parts, sheet_w, sheet_h, return_all=True)

            st.success(f"Utilization: {best['util']:.2f}%")

            create_job({
                "utilization": best["util"],
                "parts": len(parts)
            })

            fig = draw_layout(best["layout"], best["W"], best["H"])
            st.pyplot(fig)

            gcode = generate_gcode(best["layout"])
            st.download_button("Download G-code", gcode, "nest.nc")

            st.subheader("📦 Sheets Used")

            for i, sheet in enumerate(best["sheets"]):
                st.write(f"Sheet {i+1}")
                fig2 = draw_layout(sheet, best["W"], best["H"])
                st.pyplot(fig2)

        except Exception as e:
            st.error(f"Nesting failed: {e}")
