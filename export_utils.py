import streamlit as st
import io

def export_csv(df):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    st.download_button(
        label="📥 Download CSV",
        data=buffer.getvalue(),
        file_name="transactions.csv",
        mime="text/csv",
    )
