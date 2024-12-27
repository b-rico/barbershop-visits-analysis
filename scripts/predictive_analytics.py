"""
File Name: predictive_analytics.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function predicts the next visit date for each client based on the average time 
    between their previous visits.
Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): Directory where the output CSV file will be saved.
Output:
    - A CSV file named 'predicted_next_visits.csv' saved to the specified directory.
"""

import pandas as pd

def predictive_analytics(data, output_dir):
    """
    Predicts the next visit date for each client based on the average time 
    between their previous visits.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): Directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'predicted_next_visits.csv' saved to the specified directory.
    """
    data['date'] = pd.to_datetime(data['date'])
    data['visit_gap'] = data.groupby('id')['date'].diff().dt.days

    visit_gaps = data.groupby('id', as_index=False).agg({'visit_gap': 'mean'}).rename(columns={'visit_gap': 'avg_visit_gap'})
    visit_gaps['avg_visit_gap'] = visit_gaps['avg_visit_gap'].round()
    visit_gaps['avg_visit_gap'] = visit_gaps['avg_visit_gap'].fillna(0)

    latest_visits = data.groupby('id', as_index=False).agg({'date': 'max'}).rename(columns={'date': 'last_visit_date'})

    predicted_next_visit = pd.merge(latest_visits, visit_gaps, on='id', how='left')
    predicted_next_visit['predicted_next_visit'] = predicted_next_visit.apply(
        lambda row: row['last_visit_date'] + pd.to_timedelta(row['avg_visit_gap'], unit='d') 
        if row['avg_visit_gap'] > 0 else pd.NaT, axis=1
    )

    predicted_next_visit[['id', 'last_visit_date', 'predicted_next_visit']].to_csv(f"{output_dir}/predicted_next_visits.csv", index=False)
    print("Predictive Analytics complete: predicted_next_visits.csv generated.")
