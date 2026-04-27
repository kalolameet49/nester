import streamlit as st
from nesting_ui import nesting_ui
from jobs import get_jobs

def dashboard_page():

    st.sidebar.write(f"👤 {st.session_state.user}")

    menu = st.sidebar.selectbox("Menu", ["Nesting", "Job History"])

    if menu == "Nesting":
        nesting_ui()

    elif menu == "Job History":
        st.header("📂 Job History")

        jobs = get_jobs(st.session_state.user)

        for j in jobs:
            st.write(j)
