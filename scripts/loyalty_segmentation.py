"""
File Name: loyalty_segmentation.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function segments clients into loyalty categories based on their visit frequency and recency.
Args:
    - data (DataFrame): DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): Directory to save the output CSV.
Output:
    - A CSV file named 'loyalty_segmentation.csv' saved to the specified directory.
"""

import pandas as pd
import numpy as np

def loyalty_segmentation(data, output_dir):
    """
    Segments clients into loyalty categories based on their visit frequency and recency.

    Args:
    - data (DataFrame): DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): Directory to save the output CSV.

    Output:
    - A CSV file named 'loyalty_segmentation.csv' saved to the specified directory.
    """
    data['date'] = pd.to_datetime(data['date'])

    visit_counts = data.groupby('id')['date'].count().reset_index(name='total_visits')
    last_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')

    last_visits['days_since_last_visit'] = (pd.Timestamp.today() - last_visits['last_visit_date']).dt.days

    segmentation = pd.merge(visit_counts, last_visits, on='id')

    conditions = [
        (segmentation['total_visits'] >= 12) & (segmentation['days_since_last_visit'] <= 30),
        (segmentation['total_visits'] >= 12) & (segmentation['days_since_last_visit'] > 30),
        (segmentation['total_visits'] >= 6) & (segmentation['total_visits'] < 12) & (segmentation['days_since_last_visit'] <= 90),
        (segmentation['total_visits'] >= 6) & (segmentation['total_visits'] < 12) & (segmentation['days_since_last_visit'] > 90),
        (segmentation['total_visits'] >= 2) & (segmentation['total_visits'] < 6) & (segmentation['days_since_last_visit'] <= 180),
        (segmentation['total_visits'] >= 2) & (segmentation['total_visits'] < 6) & (segmentation['days_since_last_visit'] > 180),
        (segmentation['total_visits'] < 2)
    ]
    choices = [
        'Low Risk',  # Frequent visits, recent
        'Medium Risk',  # Frequent visits, not recent
        'Moderate Risk',  # Moderate visits, recent
        'Elevated Risk',  # Moderate visits, not recent
        'High Risk',  # Low visits, recent
        'Highest Risk',  # Low visits, not recent
        'New'  # Very few visits
    ]

    segmentation['loyalty_segment'] = np.select(conditions, choices, default='Unknown')

    unknowns = segmentation[segmentation['loyalty_segment'] == 'Unknown']
    if not unknowns.empty:
        print("Warning: Some records were assigned 'Unknown'. Investigate these cases:")
        print(unknowns)

    segmentation.to_csv(f"{output_dir}/loyalty_segmentation.csv", index=False)
    print("Loyalty Segmentation complete: loyalty_segmentation.csv generated.")
