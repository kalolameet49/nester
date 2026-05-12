import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ProNester", layout="wide")

st.title("⚙️ ProNester Industrial Suite")

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

# -------------------------
# Weight Calculator
# -------------------------

if menu == "Weight Calculator":

    st.header("⚖️ Weight Calculator")

    material = st.selectbox("Material", ["MS", "SS"])

    thickness = st.number_input("Thickness (mm)", value=5.0)

    width = st.number_input("Width (mm)", value=1000.0)

    height = st.number_input("Height (mm)", value=1000.0)

    qty = st.number_input("Quantity", value=1)

    density = 7850 if material == "MS" else 8000

    volume = (width * height * thickness * qty) / 1e9

    weight = volume * density

    st.success(f"Estimated Weight: {weight:.2f} kg")


# -------------------------
# Custom Nesting
# -------------------------

elif menu == "Custom Sheet Nesting":

    st.header("📐 Custom Sheet Nesting")

    sheet_w = st.number_input("Sheet Width", value=2440)

    sheet_h = st.number_input("Sheet Height", value=1220)

    part_w = st.number_input("Part Width", value=200)

    part_h = st.number_input("Part Height", value=100)

    qty = st.number_input("Quantity", value=10)

    cols = int(sheet_w // part_w)

    rows = int(sheet_h // part_h)

    fit = cols * rows

    util = ((part_w * part_h * qty) / (sheet_w * sheet_h)) * 100

    st.success(f"Parts Per Sheet: {fit}")

    st.success(f"Utilization: {util:.2f}%")

    fig, ax = plt.subplots(figsize=(10, 5))

    rect = plt.Rectangle((0, 0), sheet_w, sheet_h, fill=False)

    ax.add_patch(rect)

    ax.set_xlim(0, sheet_w)

    ax.set_ylim(0, sheet_h)

    st.pyplot(fig)


# -------------------------
# Auto Sheet Selection
# -------------------------

elif menu == "Auto Sheet Selection":

    st.header("🤖 Auto Sheet Selection")

    area = st.number_input("Required Area mm²", value=1000000)

    sheets = [
        (2440, 1220),
        (3000, 1500),
        (6000, 1500)
    ]

    best = None

    for w, h in sheets:

        util = (area / (w * h)) * 100

        if util < 100:

            if best is None or util > best[2]:
                best = (w, h, util)

    if best:

        st.success(f"Recommended Sheet: {best[0]} x {best[1]}")

        st.success(f"Utilization: {best[2]:.2f}%")


# -------------------------
# Stock Manager
# -------------------------

elif menu == "Stock Manager":

    st.header("📦 Stock Manager")

    data = {
        "Material": ["MS", "SS"],
        "Thickness": [5, 10],
        "Width": [2440, 3000],
        "Height": [1220, 1500],
        "Qty": [10, 5]
    }

    df = pd.DataFrame(data)

    st.dataframe(df)


# -------------------------
# Time Estimator
# -------------------------

elif menu == "Time Estimator":

    st.header("⏱ Cutting Time Estimator")

    cut_length = st.number_input("Cut Length mm", value=10000)

    speed = st.number_input("Cut Speed mm/min", value=2000)

    pierce = st.number_input("Pierce Count", value=10)

    pierce_time = st.number_input("Pierce Time sec", value=3)

    cut_time = cut_length / speed

    pierce_total = (pierce * pierce_time) / 60

    total = cut_time + pierce_total

    st.success(f"Estimated Time: {total:.2f} min")
