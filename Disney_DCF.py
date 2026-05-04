import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Disney DCF Valuation")
st.title("🏰 Walt Disney Company — DCF Valuation Model")

# Download button at the top
with open("Disney_DCF_Valuation.xlsx", "rb") as f:
    st.download_button(
        label="📥 Download Excel Model",
        data=f,
        file_name="Disney_DCF_Valuation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")

# Load all sheets
@st.cache_data
def load_data():
    xl = pd.ExcelFile("Disney_DCF_Valuation.xlsx")
    sheets = {name: pd.read_excel(xl, sheet_name=name, header=None) for name in xl.sheet_names}
    return sheets, xl.sheet_names

sheets, sheet_names = load_data()

# Sheet selector
selected = st.selectbox("Select a sheet to preview:", sheet_names)
st.dataframe(sheets[selected], use_container_width=True, hide_index=True)
