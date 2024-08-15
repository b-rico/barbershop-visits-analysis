import pandas as pd

def predictive_analytics(data, output_dir):
    """
    This function predicts the next visit date for each client based on the average time 
    between their previous visits. It helps in anticipating when clients are likely to return.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'predicted_next_visits.csv' saved to the specified output directory.
    """
    # Ensure the date column is in datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Calculate the time gap between consecutive visits for each client
    data['visit_gap'] = data.groupby('id')['date'].diff().dt.days
    
    # Calculate the average visit gap per client
    visit_gaps = data.groupby('id')['visit_gap'].mean().reset_index(name='avg_visit_gap')
    
    # Get the most recent visit date for each client
    latest_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')
    
    # Predict the next visit date
    predicted_next_visit = pd.merge(latest_visits, visit_gaps, on='id')
    predicted_next_visit['predicted_next_visit'] = predicted_next_visit['last_visit_date'] + pd.to_timedelta(predicted_next_visit['avg_visit_gap'], unit='d')
    
    # Save the results
    predicted_next_visit[['id', 'last_visit_date', 'predicted_next_visit']].to_csv(f"{output_dir}/predicted_next_visits.csv", index=False)
    print("Predictive Analytics complete: predicted_next_visits.csv generated.")
