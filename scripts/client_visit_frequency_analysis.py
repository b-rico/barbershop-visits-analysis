"""
File Name: client_visit_frequency_analysis.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function calculates the average time between client visits based on their visit data.
Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.
Output:
    - A CSV file named 'avg_time_between_visits.csv' saved to the specified output directory.
"""


import pandas as pd

def client_visit_frequency_analysis(data, output_dir):
    data['visit_gap'] = data.groupby('id')['date'].diff().dt.days
    avg_time_between_visits = data.groupby('id')['visit_gap'].mean().reset_index()
    avg_time_between_visits.to_csv(f"{output_dir}/avg_time_between_visits.csv", index=False)
    print("Client Visit Frequency Analysis complete: avg_time_between_visits.csv generated.")
