### bq_utils.py
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
import json

# Load credentials from Streamlit secrets if available
if "GOOGLE_CREDENTIALS" in os.environ:
    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    client = bigquery.Client(credentials=credentials)
else:
    client = bigquery.Client()

def get_wallet_transactions(address, start_date, end_date, from_filter=None, to_filter=None):
    base_query = f"""
        SELECT timestamp, tx_hash, from_address, to_address, value, fee, block_number
        FROM `bitwave-solutions.solutions_canton_test.canton_mock_data`
        WHERE (from_address = '{address}' OR to_address = '{address}')
          AND DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
    """

    if from_filter:
        base_query += f" AND from_address = '{from_filter}'"
    if to_filter:
        base_query += f" AND to_address = '{to_filter}'"

    df = client.query(base_query).to_dataframe()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp', ascending=False)

