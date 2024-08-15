import os
import pandas as pd
import numpy as np

# Ensure the output directory exists
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# Load the data
file_path = './data/barbershop_client_frequency_data.csv'
data = pd.read_csv(file_path)

# Convert date columns to datetime format
data['date'] = pd.to_datetime(data['date'])
data['first_visit'] = pd.to_datetime(data['first_visit'])

# Script 1: Client Visit Frequency Analysis
def client_visit_frequency_analysis(data, output_dir):
    # Calculate time between visits
    data['visit_gap'] = data.groupby('id')['date'].diff().dt.days
    avg_time_between_visits = data.groupby('id')['visit_gap'].mean().reset_index()

    # Save the results
    avg_time_between_visits.to_csv(os.path.join(output_dir, 'avg_time_between_visits.csv'), index=False)
    print("Client Visit Frequency Analysis complete: avg_time_between_visits.csv generated.")

# Script 2: Client Retention and Loyalty Metrics
def client_retention_loyalty_metrics(data, output_dir):
    # Calculate retention (returning clients)
    retention = data.groupby('id')['date'].count().reset_index(name='visit_count')
    retention['retained'] = retention['visit_count'] > 1

    # Save the results
    retention.to_csv(os.path.join(output_dir, 'client_retention_loyalty.csv'), index=False)
    print("Client Retention and Loyalty Metrics complete: client_retention_loyalty.csv generated.")

# Script 3: Trend Analysis
def trend_analysis(data, output_dir):
    # Analyze visits over time
    monthly_visits = data.groupby(data['date'].dt.to_period('M')).size().reset_index(name='visit_count')

    # Save the results
    monthly_visits.to_csv(os.path.join(output_dir, 'monthly_visits_trend.csv'), index=False)
    print("Trend Analysis complete: monthly_visits_trend.csv generated.")

# Script 4: Predictive Analytics (Next Visit Prediction)
def predictive_analytics(data, output_dir):
    # Predict the next visit date based on historical gaps
    visit_gaps = data.groupby('id')['visit_gap'].mean().reset_index()
    latest_visits = data.groupby('id')['date'].max().reset_index()
    predicted_next_visit = latest_visits.merge(visit_gaps, on='id')
    predicted_next_visit['predicted_next_visit'] = predicted_next_visit['date'] + pd.to_timedelta(predicted_next_visit['visit_gap'], unit='d')

    # Save the results
    predicted_next_visit[['id', 'date', 'predicted_next_visit']].to_csv(os.path.join(output_dir, 'predicted_next_visits.csv'), index=False)
    print("Predictive Analytics complete: predicted_next_visits.csv generated.")

# Script 5: Client Lifetime Value
def client_lifetime_value(data, output_dir):
    # Calculate the total number of visits and average time between visits
    visit_counts = data.groupby('id')['date'].count().reset_index(name='total_visits')
    avg_time_between_visits = data.groupby('id')['visit_gap'].mean().reset_index(name='avg_time_between_visits')
    
    # Assume an average revenue per visit (e.g., $50) for simplicity
    avg_revenue_per_visit = 50
    visit_counts['lifetime_value'] = visit_counts['total_visits'] * avg_revenue_per_visit
    
    # Save the results
    visit_counts.to_csv(os.path.join(output_dir, 'client_lifetime_value.csv'), index=False)
    print("Client Lifetime Value Analysis complete: client_lifetime_value.csv generated.")

# Script 6: Churn Analysis
def churn_analysis(data, output_dir):
    # Calculate the time since the last visit for each client
    latest_visits = data.groupby('id')['date'].max().reset_index()
    latest_visits['days_since_last_visit'] = (pd.to_datetime('today') - latest_visits['date']).dt.days
    
    # Assume churn if the last visit was more than 180 days ago
    churn_threshold = 180
    latest_visits['churned'] = latest_visits['days_since_last_visit'] > churn_threshold
    
    # Save the results
    latest_visits.to_csv(os.path.join(output_dir, 'churn_analysis.csv'), index=False)
    print("Churn Analysis complete: churn_analysis.csv generated.")

# Script 7: Loyalty Segmentation
def loyalty_segmentation(data, output_dir):
    # Segmentation based on visit frequency and recency
    visit_counts = data.groupby('id')['date'].count().reset_index(name='total_visits')
    latest_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')
    latest_visits['days_since_last_visit'] = (pd.to_datetime('today') - latest_visits['last_visit_date']).dt.days
    
    # Define loyalty segments
    conditions = [
        (visit_counts['total_visits'] >= 10) & (latest_visits['days_since_last_visit'] <= 90),
        (visit_counts['total_visits'] < 10) & (latest_visits['days_since_last_visit'] <= 90),
        (latest_visits['days_since_last_visit'] > 90)
    ]
    segments = ['Loyal', 'Potentially Loyal', 'At Risk']
    visit_counts['loyalty_segment'] = np.select(conditions, segments, default='New')

    # Merge with latest visits to include all necessary data
    loyalty_data = pd.merge(visit_counts, latest_visits, on='id')

    # Save the results
    loyalty_data.to_csv(os.path.join(output_dir, 'loyalty_segmentation.csv'), index=False)
    print("Loyalty Segmentation complete: loyalty_segmentation.csv generated.")

# Script 8: Visit Patterns
def visit_patterns(data, output_dir):
    # Identify common patterns in visit frequency
    data['day_of_week'] = data['date'].dt.day_name()
    data['month'] = data['date'].dt.month_name()
    
    day_of_week_patterns = data['day_of_week'].value_counts().reset_index(name='visit_count')
    month_patterns = data['month'].value_counts().reset_index(name='visit_count')
    
    # Save the results
    day_of_week_patterns.to_csv(os.path.join(output_dir, 'day_of_week_patterns.csv'), index=False)
    month_patterns.to_csv(os.path.join(output_dir, 'month_patterns.csv'), index=False)
    print("Visit Patterns Analysis complete: day_of_week_patterns.csv and month_patterns.csv generated.")

# Update the main script to include the new analyses
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
