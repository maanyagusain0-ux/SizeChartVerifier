import streamlit as st
import pandas as pd
from io import BytesIO

from main import generate_report   # We'll create this function in main.py

st.set_page_config(
    page_title="Size Chart Verifier",
    page_icon="📏",
    layout="wide"
)

st.title("📏 Size Chart Verifier")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    st.write("Preview")

    st.dataframe(df.head())

    if st.button("Generate Report"):

        with st.spinner("Verifying Size Charts..."):

            report_df = generate_report(df)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            report_df.to_excel(writer, index=False)

        st.success("Report Generated Successfully!")

        st.download_button(
            label="📥 Download Report",
            data=output.getvalue(),
            file_name="SizeChartReport.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )