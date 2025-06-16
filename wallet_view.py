import streamlit as st
import pandas as pd
from bq_utils import get_wallet_transactions
from export_utils import export_csv

def wallet_view(address: str):
    st.subheader(f"📬 Wallet Overview: `{address}`")

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date")
    end_date = col2.date_input("End Date")

    with st.form("filter_form"):
        from_filter = st.text_input("From Address Filter")
        to_filter = st.text_input("To Address Filter")
        submitted = st.form_submit_button("Apply Filters")

    df = get_wallet_transactions(
        address=address,
        start_date=start_date,
        end_date=end_date,
        from_filter=from_filter,
        to_filter=to_filter
    )

    if df.empty:
        st.warning("No transactions found for this address.")
    else:
        st.metric("Total Txns", len(df))
        st.metric("Total Inflow", df[df['to_address'] == address]['value'].sum())
        st.metric("Total Outflow", df[df['from_address'] == address]['value'].sum())

        st.dataframe(df, use_container_width=True)
        export_csv(df)
