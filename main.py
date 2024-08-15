import os
import pandas as pd

# Import the scripts from the scripts directory
from scripts.client_visit_frequency_analysis import client_visit_frequency_analysis
from scripts.client_retention_loyalty_metrics import client_retention_loyalty_metrics
from scripts.trend_analysis import trend_analysis
from scripts.predictive_analytics import predictive_analytics
from scripts.client_lifetime_value import client_lifetime_value
from scripts.churn_analysis import churn_analysis
from scripts.loyalty_segmentation import loyalty_segmentation
from scripts.visit_patterns import visit_patterns

# Ensure the output directory exists
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# Load the data
file_path = './data/barbershop_client_frequency_data.csv'
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])
data['first_visit'] = pd.to_datetime(data['first_visit'])

# Run each analysis script
def main():
    client_visit_frequency_analysis(data, output_dir)
    client_retention_loyalty_metrics(data, output_dir)
    trend_analysis(data, output_dir)
    predictive_analytics(data, output_dir)
    client_lifetime_value(data, output_dir)
    churn_analysis(data, output_dir)
    loyalty_segmentation(data, output_dir)
    visit_patterns(data, output_dir)

if __name__ == "__main__":
    main()
