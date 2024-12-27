"""
File Name: trend_analysis.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function analyzes the trends in client visits over time by aggregating visit counts 
    on a monthly basis. It helps to identify seasonal patterns or trends in client behavior.
Args:
    - data (DataFrame): The DataFrame containing client visit data with at least 'date' column.
    - output_dir (str): The directory where the output CSV file will be saved.
Output:
    - A CSV file named 'monthly_visits_trend.csv' saved to the specified output directory.
"""

import pandas as pd

def trend_analysis(data, output_dir):
    """
    This function analyzes the trends in client visits over time by aggregating visit counts 
    on a monthly basis. It helps to identify seasonal patterns or trends in client behavior.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with at least 'date' column.
    - output_dir (str): The directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'monthly_visits_trend.csv' saved to the specified output directory.
    """
    data['date'] = pd.to_datetime(data['date'])

    monthly_visits = data.groupby(data['date'].dt.to_period('M')).size().reset_index(name='visit_count')
    monthly_visits['date'] = monthly_visits['date'].astype(str)
    
    monthly_visits.to_csv(f"{output_dir}/monthly_visits_trend.csv", index=False)
    print("Trend Analysis complete: monthly_visits_trend.csv generated.")
