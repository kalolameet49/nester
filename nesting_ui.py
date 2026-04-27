st.subheader("📦 Sheets Used")

for i, sheet in enumerate(best["sheets"]):
    st.write(f"Sheet {i+1}")
    fig = draw_layout(sheet, best["W"], best["H"])
    st.pyplot(fig)
