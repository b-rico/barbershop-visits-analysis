"""
File Name: client_lifetime_value.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function estimates the Client Lifetime Value (CLV) based on the number of visits and 
    an assumed average revenue per visit.

Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.
    - avg_revenue_per_visit (float): The assumed average revenue generated per visit (default is $50).

Output:
    - A CSV file named 'client_lifetime_value.csv' saved to the specified output directory.
"""

import pandas as pd

def client_lifetime_value(data, output_dir):
    """
    This function estimates the Client Lifetime Value (CLV) for each client by 
    summing the 'revenue' field from all of their visits.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with at least
      'id', 'date', and 'revenue' columns.
    - output_dir (str): The directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'client_lifetime_value.csv' saved to the specified output directory,
      containing columns ['id', 'lifetime_value'].
    """
    # 1) Group by client ID and sum the revenue of all visits
    clv_df = data.groupby('id')['revenue'].sum().reset_index()
    clv_df.rename(columns={'revenue': 'lifetime_value'}, inplace=True)

    # 2) Save the results
    clv_df.to_csv(f"{output_dir}/client_lifetime_value.csv", index=False)
    print("Client Lifetime Value Analysis complete: client_lifetime_value.csv generated.")
