import streamlit as st

from weight_calculator import weight_page
from nesting_custom_sheet import custom_nesting_page
from nesting_auto_sheet import auto_sheet_page
from stock_manager import stock_page
from time_estimator import time_page

st.set_page_config(page_title="ProNester", layout="wide")

st.title("⚙️ ProNester Industrial Suite")
st.markdown("### Smart SVG Nesting + Estimation Platform")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Weight Calculator",
        "Custom Sheet Nesting",
        "Auto Sheet Selection",
        "Stock Manager",
        "Cutting Time Estimator"
    ]
)

if menu == "Weight Calculator":
    weight_page()

elif menu == "Custom Sheet Nesting":
    custom_nesting_page()

elif menu == "Auto Sheet Selection":
    auto_sheet_page()

elif menu == "Stock Manager":
    stock_page()

elif menu == "Cutting Time Estimator":
    time_page()
