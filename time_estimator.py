import streamlit as st

def time_page():

st.header("⏱ Cutting Time Estimator")

cut_length = st.number_input("Total Cutting Length (mm)", value=10000)

cutting_speed = st.number_input("Cutting Speed mm/min", value=2000)

pierce_count = st.number_input("Pierce Count", value=10)

pierce_time = st.number_input("Pierce Time/sec", value=3)

if st.button("Estimate Time"):

cut_time = cut_length / cutting_speed

pierce_total = (pierce_count * pierce_time) / 60

total = cut_time + pierce_total

st.success(f"Estimated Cutting Time: {total:.2f} min")
