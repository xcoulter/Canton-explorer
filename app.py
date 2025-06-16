import streamlit as st
from wallet_view import wallet_view
from tx_detail_view import tx_detail_view

st.set_page_config(page_title="Canton Explorer", layout="wide")
st.title("🔍 Canton Block Explorer")

query = st.text_input("Search Address or Tx Hash", "")

if query:
    if len(query) == 66:  # tx hash
        tx_detail_view(query)
    elif len(query) == 42:  # address
        wallet_view(query)
    else:
        st.warning("Invalid input. Please enter a valid address or tx hash.")
else:
    st.info("Enter a wallet address or transaction hash above.")
