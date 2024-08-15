import pandas as pd
import numpy as np

def loyalty_segmentation(data, output_dir):
    """
    This function segments clients into loyalty categories based on their visit frequency 
    and recency. The segmentation helps in identifying highly loyal, potentially loyal, 
    and at-risk clients.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'loyalty_segmentation.csv' saved to the specified output directory.
    """
    # Ensure the date column is in datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Calculate total visits and the date of the last visit for each client
    visit_counts = data.groupby('id')['date'].count().reset_index(name='total_visits')
    latest_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')
    
    # Calculate the number of days since the last visit
    latest_visits['days_since_last_visit'] = (pd.to_datetime('today') - latest_visits['last_visit_date']).dt.days
    
    # Define loyalty segments based on visit counts and recency
    conditions = [
        (visit_counts['total_visits'] >= 10) & (latest_visits['days_since_last_visit'] <= 90),
        (visit_counts['total_visits'] >= 5) & (visit_counts['total_visits'] < 10) & (latest_visits['days_since_last_visit'] <= 180),
        (visit_counts['total_visits'] < 5) | (latest_visits['days_since_last_visit'] > 180)
    ]
    choices = ['Highly Loyal', 'Potentially Loyal', 'At Risk']
    
    # Create a loyalty segment column
    visit_counts['loyalty_segment'] = np.select(conditions, choices, default='New')
    
    # Merge the visit counts and latest visits to include all relevant data
    loyalty_data = pd.merge(visit_counts, latest_visits, on='id')
    
    # Save the results
    loyalty_data.to_csv(f"{output_dir}/loyalty_segmentation.csv", index=False)
    print("Loyalty Segmentation complete: loyalty_segmentation.csv generated.")
