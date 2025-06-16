from google.cloud import bigquery
import pandas as pd

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
