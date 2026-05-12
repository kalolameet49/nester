import streamlit as st
import pandas as pd


def stock_page():

    st.header("📦 Stock Manager")

    if "stock_data" not in st.session_state:
        st.session_state.stock_data = []

    material = st.selectbox(
        "Material",
        ["MS", "SS"]
    )

    thickness = st.number_input(
        "Thickness",
        value=5.0
    )

    width = st.number_input(
        "Width",
        value=2440.0
    )

    height = st.number_input(
        "Height",
        value=1220.0
    )

    qty = st.number_input(
        "Qty",
        value=1
    )

    if st.button("Add Stock"):

        st.session_state.stock_data.append({

            "Material": material,
            "Thickness": thickness,
            "Width": width,
            "Height": height,
            "Qty": qty
        })

    if st.session_state.stock_data:

        df = pd.DataFrame(
            st.session_state.stock_data
        )

        st.dataframe(df)
