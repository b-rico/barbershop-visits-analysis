"""
File Name: client_retention_loyalty_metrics.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function calculates client retention and loyalty metrics based on their visit data.
    
    - Retention is defined as clients who have visited more than once.
    - The function will also calculate the total number of visits for each client.

Args:
    - data (DataFrame): The DataFrame containing client visit data with at least 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.

Output:
    - A CSV file named 'client_retention_loyalty.csv' saved to the specified output directory.
"""

import pandas as pd
import numpy as np

def client_retention_loyalty_metrics(data, output_dir):
    data['date'] = pd.to_datetime(data['date'])

    visit_counts = data.groupby('id')['date'].count().reset_index(name='visit_count')
    
    last_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')
    last_visits['days_since_last_visit'] = (pd.Timestamp.today() - last_visits['last_visit_date']).dt.days

    retention = pd.merge(visit_counts, last_visits, on='id')

    retention['retained'] = retention['visit_count'] > 1

    conditions = [
        (retention['visit_count'] >= 12) & (retention['days_since_last_visit'] <= 30),
        (retention['visit_count'] >= 12) & (retention['days_since_last_visit'] > 30),
        (retention['visit_count'] >= 6) & (retention['visit_count'] < 12) & (retention['days_since_last_visit'] <= 90),
        (retention['visit_count'] >= 6) & (retention['visit_count'] < 12) & (retention['days_since_last_visit'] > 90),
        (retention['visit_count'] >= 2) & (retention['visit_count'] < 6) & (retention['days_since_last_visit'] <= 180),
        (retention['visit_count'] >= 2) & (retention['visit_count'] < 6) & (retention['days_since_last_visit'] > 180),
        (retention['visit_count'] < 2) & (retention['days_since_last_visit'] > 180)
    ]
    choices = [
        'Extremely Loyal',  # Frequent visits, recent
        'Highly Loyal',  # Frequent visits, not recent
        'Moderate Loyal',  # Moderate visits, recent
        'Elevated Risk',  # Moderate visits, not recent
        'Low Loyal',  # Few visits, recent
        'At Risk',  # Few visits, not recent
        'New'  # Very few visits
    ]

    retention['loyalty'] = np.select(conditions, choices, default='Unknown')

    unknowns = retention[retention['loyalty'] == 'Unknown']
    if not unknowns.empty:
        print("Warning: Some records were assigned 'Unknown'. Investigate these cases:")
        print(unknowns)

    retention.to_csv(f"{output_dir}/client_retention_loyalty.csv", index=False)
    print("Client Retention and Loyalty Metrics complete: client_retention_loyalty.csv generated.")
