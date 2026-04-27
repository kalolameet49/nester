import streamlit as st
from parser import extract_from_dxf, extract_from_svg
from nesting import ProNester
from gcode import generate_gcode
from jobs import create_job
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_layout(layout, W, H, title="Layout"):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_aspect('equal')

    # Draw sheet boundary
    ax.add_patch(patches.Rectangle((0, 0), W, H, fill=False, linewidth=2))

    # Draw parts
    for poly in layout:
        try:
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha=0.6)
        except:
            continue

    ax.set_title(title)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)

    return fig


def nesting_ui():

    st.header("📐 Advanced Sheet Nesting")

    # -------- SETTINGS --------
    col1, col2 = st.columns(2)

    with col1:
        gap = st.slider("Gap (mm)", 0.0, 10.0, 3.0)
        margin = st.slider("Margin (mm)", 0.0, 20.0, 5.0)

    with col2:
        tries = st.slider("Generate Layouts", 1, 20, 10)
        sheet_mode = st.selectbox("Sheet Mode", ["Auto Size", "Fixed Sheet"])

    sheet_w = sheet_h = None

    if sheet_mode == "Fixed Sheet":
        c1, c2 = st.columns(2)
        sheet_w = c1.number_input("Sheet Width (mm)", value=2440)
        sheet_h = c2.number_input("Sheet Height (mm)", value=1220)

    # -------- FILE UPLOAD --------
    files = st.file_uploader("Upload DXF / SVG", type=["dxf", "svg"], accept_multiple_files=True)

    if files:
        parts = []

        st.subheader("📦 Set Quantity")

        for f in files:
            shapes = extract_from_svg(f) if f.name.endswith(".svg") else extract_from_dxf(f)

            if shapes:
                c1, c2 = st.columns([3, 1])
                c1.write(f"✅ {f.name}")
                qty = c2.number_input("Qty", 1, 100, 1, key=f.name)

                for _ in range(qty):
                    parts.extend(shapes)

        # -------- RUN --------
        if st.button("🚀 Run Nesting"):

            if not parts:
                st.error("No valid shapes found!")
                return

            with st.spinner("Generating optimized layouts..."):

                engine = ProNester(gap=gap, margin=margin, tries=tries)

                best, all_layouts = engine.nest(
                    parts,
                    sheet_w=sheet_w,
                    sheet_h=sheet_h,
                    return_all=True
                )

            # -------- BEST RESULT --------
            st.success(
                f"""
📐 Sheet Size: **{best['W']:.0f} x {best['H']:.0f} mm**  
📊 Utilization: **{best['util']:.2f}%**
"""
            )

            create_job(
                st.session_state.user,
                "Nesting Job",
                {"W": best["W"], "H": best["H"], "util": best["util"]}
            )

            fig = draw_layout(best["layout"], best["W"], best["H"], "Best Layout")
            st.pyplot(fig)

            # -------- DOWNLOAD --------
            gcode = generate_gcode(best["layout"])
            st.download_button("📥 Download G-Code", gcode, "nesting.nc")

            # -------- ALTERNATIVE LAYOUTS --------
            st.subheader("🔄 Alternative Layouts")

            sorted_layouts = sorted(all_layouts, key=lambda x: -x["util"])

            for i, lay in enumerate(sorted_layouts[:5]):

                with st.expander(f"Layout {i+1} — Utilization {lay['util']:.2f}%"):

                    fig_alt = draw_layout(lay["layout"], lay["W"], lay["H"], f"Layout {i+1}")
                    st.pyplot(fig_alt)
