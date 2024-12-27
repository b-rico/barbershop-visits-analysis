"""
File Name: main.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This script serves as the main entry point for running the client retention and loyalty analysis.
    It orchestrates the

Args:
    - None

Output:
    - Various CSV files containing the results of the analysis.
"""

import os
import pandas as pd
from scripts.gen_visits_table import gen_visits_table
from scripts.gen_clients_table import gen_clients_table
from scripts.client_visit_frequency_analysis import client_visit_frequency_analysis
from scripts.client_retention_loyalty_metrics import client_retention_loyalty_metrics
from scripts.trend_analysis import trend_analysis
from scripts.predictive_analytics import predictive_analytics
from scripts.client_lifetime_value import client_lifetime_value
from scripts.churn_analysis import churn_analysis
from scripts.loyalty_segmentation import loyalty_segmentation
from scripts.visit_patterns import visit_patterns
from scripts.predictive_analytics_survival import predictive_analytics_survival_df
from scripts.time_series_forecast import time_series_forecast

output_dir = './output'
data_dir = './data'
file_path = './data/visits_table.csv'

os.makedirs(output_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

def ensure_visits_table_exists():
    """
    Checks if visits_table.csv exists. If not, it runs gen_visits_table and gen_clients_table
    to generate the data, then loads and returns the visits DataFrame.
    """
    if not os.path.exists(file_path):
        print(f"File not found at {file_path}. Generating new data...")
        gen_visits_table(data_dir)
        gen_clients_table(data_dir)
    else:
        print(f"File found at {file_path}. Skipping data generation.")

    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])
    data['first_visit'] = pd.to_datetime(data['first_visit'])
    return data

def main():
    data = ensure_visits_table_exists()

    client_visit_frequency_analysis(data, output_dir)
    client_retention_loyalty_metrics(data, output_dir)
    trend_analysis(data, output_dir)
    predictive_analytics(data, output_dir)
    client_lifetime_value(data, output_dir)
    churn_analysis(data, output_dir)
    loyalty_segmentation(data, output_dir)
    visit_patterns(data, output_dir)
    predictive_analytics_survival_df(data, output_dir)
    time_series_forecast(data, output_dir, forecast_days=60)


if __name__ == "__main__":
    main()
