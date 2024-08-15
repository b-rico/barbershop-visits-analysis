import pandas as pd

def churn_analysis(data, output_dir, churn_threshold=180):
    """
    This function performs churn analysis by identifying clients who have not visited within 
    a specified number of days (churn threshold). These clients are considered to have churned.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.
    - churn_threshold (int): The number of days since the last visit after which a client is 
                             considered to have churned (default is 180 days).

    Output:
    - A CSV file named 'churn_analysis.csv' saved to the specified output directory.
    """
    # Ensure the date column is in datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Get the most recent visit date for each client
    latest_visits = data.groupby('id')['date'].max().reset_index(name='last_visit_date')
    
    # Calculate the number of days since the last visit
    latest_visits['days_since_last_visit'] = (pd.to_datetime('today') - latest_visits['last_visit_date']).dt.days
    
    # Determine whether the client has churned
    latest_visits['churned'] = latest_visits['days_since_last_visit'] > churn_threshold
    
    # Save the results
    latest_visits.to_csv(f"{output_dir}/churn_analysis.csv", index=False)
    print("Churn Analysis complete: churn_analysis.csv generated.")
