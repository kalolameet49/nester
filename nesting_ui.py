import streamlit as st
from parser import extract_from_dxf, extract_from_svg
from nesting import ProNester
from gcode import generate_gcode
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

    # SETTINGS
    gap = st.slider("Gap (mm)", 0.0, 10.0, 3.0)
    margin = st.slider("Margin (mm)", 0.0, 20.0, 5.0)

    population = st.slider("Population", 6, 30, 12)
    generations = st.slider("Generations", 3, 20, 8)

    sheet_mode = st.selectbox("Sheet Mode", ["Auto", "Fixed"])

    sheet_w = sheet_h = None

    if sheet_mode == "Fixed":
        c1, c2 = st.columns(2)
        sheet_w = c1.number_input("Width", value=2440)
        sheet_h = c2.number_input("Height", value=1220)

    files = st.file_uploader("Upload DXF / SVG", type=["dxf", "svg"], accept_multiple_files=True)

    if files:
        parts = []

        for f in files:
            shapes = extract_from_svg(f) if f.name.endswith(".svg") else extract_from_dxf(f)

            qty = st.number_input(f"{f.name} qty", 1, 100, 1)

            for _ in range(qty):
                parts.extend(shapes)

        if st.button("🚀 Run Nesting"):

            engine = ProNester(
                gap=gap,
                margin=margin,
                population_size=population,
                generations=generations
            )

            best, layouts = engine.nest(parts, sheet_w, sheet_h, return_all=True)

            st.success(f"Utilization: {best['util']:.2f}%")

            fig = draw_layout(best["layout"], best["W"], best["H"])
            st.pyplot(fig)

            # GCODE
            gcode = generate_gcode(best["layout"])
            st.download_button("Download G-code", gcode, "nest.nc")

            # ALT LAYOUTS
            st.subheader("Alternatives")

            for i, lay in enumerate(layouts[:5]):
                with st.expander(f"Layout {i+1} - {lay['util']:.2f}%"):
                    fig2 = draw_layout(lay["layout"], lay["W"], lay["H"])
                    st.pyplot(fig2)
